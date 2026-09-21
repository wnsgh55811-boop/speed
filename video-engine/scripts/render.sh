#!/usr/bin/env bash
# Delivery render for one project, meant to run inside the media sandbox.
#
#   PROJECT=talk bash scripts/render.sh
#
# The sandbox is reclaimed shortly after a call returns, so whoever launches
# this has to keep polling without a gap. `--resume` means a restart picks up
# the frames already captured rather than starting over.
set -x
P=${PROJECT:-talk}
cd "$(dirname "$0")/.."
export PATH=/home/user/node22/bin:$PATH
node -v

# The composition references the narration by path, so it has to exist before
# the render starts; building it in parallel fails the run in the first minute.
mkdir -p assets/audio
( cd "examples/$P" && python3 mkaudio.py && cp out/master.mp3 ../../assets/audio/master.mp3 ) || exit 12
[ -s assets/audio/master.mp3 ] || exit 12
bash build.sh "$P" --audio assets/audio/master.mp3 || exit 13

echo "=== RENDER START $(date -u +%T) ==="
export HF_SEGMENTED_CAPTURE=true
npx hyperframes render . -o /home/user/master.mp4 \
  -q delivery -f 30 -w 6 --resolution 1080p --no-browser-gpu --best-effort \
  --browser-timeout 300 --protocol-timeout 1800000 \
  --player-ready-timeout 300000 --resume --quiet
RC=$?; echo "=== RENDER END rc=$RC $(date -u +%T) ==="
[ $RC -ne 0 ] && exit 16

ffprobe -v error -show_entries stream=codec_type,codec_name,width,height \
  -of csv=p=0 /home/user/master.mp4
ffprobe -v error -show_entries format=duration,size -of csv=p=0 /home/user/master.mp4

# A copy that opens straight from a link. The target is about 100MB over
# fourteen minutes, so the bitrate is computed from the real duration rather
# than guessed, and two passes spend it where the picture needs it.
D=$(ffprobe -v error -show_entries format=duration -of csv=p=0 /home/user/master.mp4)
VB=$(python3 -c "print(int((100*8*1000*1000/$D) - 128))")
echo "=== LIGHT target ${VB}k video + 128k audio ==="
ffmpeg -hide_banner -loglevel error -y -i /home/user/master.mp4 \
  -c:v libx264 -preset slow -b:v ${VB}k -pass 1 -an -f mp4 /dev/null &&
ffmpeg -hide_banner -loglevel error -y -i /home/user/master.mp4 \
  -c:v libx264 -preset slow -b:v ${VB}k -pass 2 \
  -pix_fmt yuv420p -c:a aac -b:a 128k -movflags +faststart \
  /home/user/light.mp4 || exit 19
ls -la /home/user/master.mp4 /home/user/light.mp4

curl -f -X PUT -H "Content-Type: video/mp4" --upload-file /home/user/master.mp4 \
  "$(cat /home/user/up/master.url)" -o /dev/null -w 'MASTER UPLOAD %{http_code}\n' || exit 20
curl -f -X PUT -H "Content-Type: video/mp4" --upload-file /home/user/light.mp4 \
  "$(cat /home/user/up/light.url)" -o /dev/null -w 'LIGHT UPLOAD %{http_code}\n' || exit 21
echo "=== ALL DONE $(date -u +%T) ==="
