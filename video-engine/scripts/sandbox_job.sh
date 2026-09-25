#!/usr/bin/env bash
# Jobs for the Higgsfield sandbox (it reaches the asset CDN; the authoring
# container cannot). Each call pulls this branch fresh. Background work there
# lives ~15 min, so a film renders as segments that the final job joins.
#
#   snap  <branch> <proj> "<t1,t2,...>"            frame QA numbers + qa/ sheets
#   voice <branch> <proj> "<mp3,mp3,mp3>"          takes → vo.wav → align; prints
#                                                  timings.txt + spans.json to commit
#   seg   <branch> <proj> <a> <b> <PUT url>         render [a,b) silent, upload
#   final <branch> <proj> "<mp3,...>" "<seg mp4 urls>" <PUT master> <PUT light>
#                                                  audio + SFX mix, concat, master/light
set -uo pipefail
MODE=$1; BR=$2; PRJ=$3
cd /home/user
exec > >(tee -a job.log) 2>&1
echo "=== JOB $MODE $(date -u +%T) ==="

if [ ! -d work ]; then
  curl -fsSL --retry 5 "https://codeload.github.com/wnsgh55811-boop/speed/tar.gz/refs/heads/$BR" -o src.tgz || exit 11
  mkdir -p work && tar xzf src.tgz -C work --strip-components=1 || exit 12
fi
cd work/video-engine
E="examples/$PRJ"

node_setup() {
  if ! node -v | grep -q '^v2[2-9]'; then
    [ -d /home/user/node22 ] || { curl -fsSL --retry 5 -o /home/user/n22.tar.xz \
      https://nodejs.org/dist/v22.11.0/node-v22.11.0-linux-x64.tar.xz &&
      mkdir -p /home/user/node22 && tar xf /home/user/n22.tar.xz -C /home/user/node22 --strip-components=1; } || exit 13
    export PATH=/home/user/node22/bin:$PATH
  fi
  [ -d node_modules/hyperframes ] || npm i --no-audit --no-fund --silent || exit 14
  mkdir -p assets/fonts vendor
  cp node_modules/pretendard/dist/public/static/Pretendard-{Regular,Medium,SemiBold,Bold,ExtraBold}.otf assets/fonts/
  cp node_modules/gsap/dist/gsap.min.js vendor/
  npx hyperframes browser ensure >/dev/null 2>&1 || true
}
assets() {
  python3 -c "import rembg" 2>/dev/null || pip install -q rembg onnxruntime numpy pillow >/dev/null 2>&1
  python3 scripts/fetch_assets.py "$E/library.json" || exit 15
  echo "=== ASSETS READY $(date -u +%T) ==="
}
takes() {
  IFS=',' read -ra V <<< "$1"; mkdir -p "$E/vo"
  for i in "${!V[@]}"; do curl -fsSL --retry 5 -o "$E/vo/c$i.mp3" "${V[$i]}" || exit 21; done
  python3 scripts/mkaudio_v2.py "$E" || exit 22
}

case "$MODE" in
snap)
  node_setup; assets
  python3 src/emit_v2.py "$E" || exit 16
  rm -rf snapshots
  npx hyperframes snapshot . --at "$4" --no-end --timeout 20000 > snap.log 2>&1 || { tail -20 snap.log; exit 17; }
  python3 scripts/qa_frames.py "$4"
  echo "=== SNAP DONE ===" ;;
voice)
  takes "$4"
  python3 -c "import faster_whisper" 2>/dev/null || pip install -q faster-whisper >/dev/null 2>&1
  python3 "$E/align.py" || exit 23
  echo "===TIMINGS==="; cat "$E/timings.txt"
  echo "===SPANS==="; cat "$E/spans.json"; echo
  echo "=== VOICE DONE ===" ;;
seg)
  node_setup; assets
  python3 src/emit_v2.py "$E" --range "$4" "$5" || exit 24
  echo "=== SEG START $4-$5 $(date -u +%T) ==="
  npx hyperframes render . -o /home/user/seg.mp4 -q high -f 30 -w 7 --no-browser-gpu \
    --browser-timeout 180 --protocol-timeout 900000 --player-ready-timeout 180000 --quiet || exit 25
  echo "=== SEG END $(date -u +%T) ==="
  ffprobe -v error -show_entries format=duration -of csv=p=0 /home/user/seg.mp4
  curl -f -X PUT -H "Content-Type: video/mp4" --upload-file /home/user/seg.mp4 "$6" -o /dev/null -w 'SEG PUT %{http_code}\n' ;;
final)
  takes "$4"
  python3 "$E/align.py" --splice-only || exit 23
  node_setup   # caption measuring needs the Pretendard files
  python3 src/emit_v2.py "$E" --audio assets/audio/master.wav || exit 24
  python3 scripts/mix_sfx.py "$E" || exit 26
  IFS=',' read -ra S <<< "$5"; : > segs.txt
  for i in "${!S[@]}"; do curl -fsSL --retry 5 -o "seg$i.mp4" "${S[$i]}" || exit 27; echo "file 'seg$i.mp4'" >> segs.txt; done
  ffmpeg -hide_banner -loglevel error -y -f concat -safe 0 -i segs.txt -i assets/audio/master.wav \
    -map 0:v -map 1:a -c:v copy -c:a aac -b:a 320k -shortest -movflags +faststart /home/user/master.mp4 || exit 28
  DUR=$(ffprobe -v error -show_entries format=duration -of csv=p=0 /home/user/master.mp4)
  VB=$(python3 -c "print(int(96*8*1024/float('$DUR') - 160))")
  ffmpeg -hide_banner -loglevel error -y -i /home/user/master.mp4 -c:v libx264 -preset slow \
    -b:v ${VB}k -maxrate $((VB * 2))k -bufsize $((VB * 4))k -pix_fmt yuv420p \
    -c:a aac -b:a 160k -movflags +faststart /home/user/light.mp4 || exit 29
  ffprobe -v error -show_entries stream=codec_type,codec_name,width,height -of csv=p=0 /home/user/master.mp4
  ffmpeg -hide_banner -nostats -i /home/user/master.mp4 -af ebur128=peak=true -f null - 2>&1 | grep -A8 Summary
  ls -la /home/user/master.mp4 /home/user/light.mp4
  curl -f -X PUT -H "Content-Type: video/mp4" --upload-file /home/user/master.mp4 "$6" -o /dev/null -w 'MASTER PUT %{http_code}\n'
  curl -f -X PUT -H "Content-Type: video/mp4" --upload-file /home/user/light.mp4 "$7" -o /dev/null -w 'LIGHT PUT %{http_code}\n'
  echo "=== ALL DONE $(date -u +%T) ===" ;;
esac
