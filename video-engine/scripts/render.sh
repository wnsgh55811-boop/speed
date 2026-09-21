#!/usr/bin/env bash
# One continuous delivery render, meant to run inside an ephemeral sandbox.
#
# The sandbox is discarded seconds after a call returns, so fetch, audio, render
# and upload all have to live in this single background process — and whoever
# launches it must keep polling without a gap, or the container is reclaimed
# mid-render and the whole capture is lost.
#
#   PROJECT_ZIP=<url> PUT_URL=<presigned put> bash render.sh
set -x
cd /home/user

curl -fsSL --retry 5 -o i.zip "$PROJECT_ZIP" || exit 11
rm -rf idasa && unzip -q i.zip || exit 12

# hyperframes needs node 22+; most sandboxes ship 20
[ -d node-v22.11.0-linux-x64 ] || {
  curl -fsSL --retry 5 -o n22.tar.xz \
    https://nodejs.org/dist/v22.11.0/node-v22.11.0-linux-x64.tar.xz && tar xf n22.tar.xz
} || exit 13
export PATH=/home/user/node-v22.11.0-linux-x64/bin:$PATH
node -v

cd /home/user/idasa
npm i --no-audit --no-fund --silent hyperframes@0.8.52 || exit 15
npx hyperframes browser ensure || true

# The composition references assets/audio/master.wav. It has to exist BEFORE the
# render starts — building it in parallel fails the run in the first minute.
mkdir -p assets/audio
if [ ! -s assets/audio/master.wav ]; then
  ( cd audio && python3 mkaudio.py ) || exit 12
  python3 - <<'PYX'
import subprocess
def dur(p):
    return float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration',
                                 '-of','csv=p=0',p], capture_output=True, text=True).stdout.strip())
# Rebuilding the narration lands ~1s off the length the subtitle timings were cut
# against, which drifts the captions by the end. A ~0.2% tempo nudge is inaudible
# and locks them back together.
src, want = 'audio/out/master.wav', float(__import__('os').environ.get('TARGET_SECONDS', '0')) or dur('audio/out/master.wav')
have = dur(src)
subprocess.run(f'ffmpeg -hide_banner -loglevel error -i {src} -af "atempo={have/want:.6f}" '
               f'-ar 48000 -ac 2 assets/audio/master.wav -y', shell=True, check=True)
print(f'[audio] {have:.3f} -> {dur("assets/audio/master.wav"):.3f}', flush=True)
PYX
fi

echo "=== RENDER START $(date -u +%T) ==="
export HF_SEGMENTED_CAPTURE=true
npx hyperframes render . -o /home/user/final.mp4 \
  -q delivery -f 30 -w 8 --resolution 1080p --no-browser-gpu --best-effort \
  --browser-timeout 180 --protocol-timeout 900000 --player-ready-timeout 180000 \
  --resume --quiet
RC=$?; echo "=== RENDER END rc=$RC $(date -u +%T) ==="
[ $RC -ne 0 ] && exit 16

ffprobe -v error -show_entries stream=codec_type,codec_name -of csv=p=0 /home/user/final.mp4
ffmpeg -hide_banner -nostats -i /home/user/final.mp4 -af volumedetect -f null - 2>&1 \
  | grep -E 'mean_volume|max_volume'

# a lighter copy that opens straight from a link
ffmpeg -hide_banner -loglevel error -i /home/user/final.mp4 \
  -c:v libx264 -preset veryfast -crf 21 -pix_fmt yuv420p -c:a aac -b:a 160k \
  -movflags +faststart /home/user/share.mp4 -y || exit 19

curl -f -X PUT -H "Content-Type: video/mp4" --upload-file /home/user/final.mp4 "$PUT_URL" \
  -o /dev/null -w 'UPLOAD HTTP %{http_code}\n' || exit 20
echo "=== ALL DONE $(date -u +%T) ==="
