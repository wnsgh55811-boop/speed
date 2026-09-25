#!/usr/bin/env bash
# One self-contained job for the Higgsfield sandbox (it can reach the asset
# CDN; the authoring container cannot). Pulls this branch, installs the
# toolchain, downloads + keys the assets, builds the composition, then either
# snapshots frames for QA or renders the film.
#
#   bash sandbox_job.sh <branch> <project> snap "<t1,t2,...>"
#   bash sandbox_job.sh <branch> <project> render "<voice mp3 urls, comma-sep>" "<put master>" "<put light>"
#
# Snap output: small JPEG grids printed as base64 between ===SHEET n=== markers
# in job.log, so frames can be inspected without a shared filesystem.
set -uo pipefail
BR=$1; PRJ=$2; MODE=$3
cd /home/user
exec > >(tee -a job.log) 2>&1
echo "=== JOB $MODE $(date -u +%T) ==="

if [ ! -d work ]; then
  curl -fsSL --retry 5 "https://codeload.github.com/wnsgh55811-boop/speed/tar.gz/refs/heads/$BR" -o src.tgz || exit 11
  mkdir -p work && tar xzf src.tgz -C work --strip-components=1 || exit 12
fi
cd work/video-engine

# hyperframes needs node 22+
if ! node -v | grep -q '^v2[2-9]'; then
  [ -d /home/user/node22 ] || { curl -fsSL --retry 5 -o /home/user/n22.tar.xz \
    https://nodejs.org/dist/v22.11.0/node-v22.11.0-linux-x64.tar.xz &&
    mkdir -p /home/user/node22 && tar xf /home/user/n22.tar.xz -C /home/user/node22 --strip-components=1; } || exit 13
  export PATH=/home/user/node22/bin:$PATH
fi
node -v
[ -d node_modules/hyperframes ] || npm i --no-audit --no-fund --silent || exit 14
mkdir -p assets/fonts vendor
cp node_modules/pretendard/dist/public/static/Pretendard-{Regular,Medium,SemiBold,Bold,ExtraBold}.otf assets/fonts/
cp node_modules/gsap/dist/gsap.min.js vendor/
npx hyperframes browser ensure >/dev/null 2>&1 || true

python3 -c "import rembg" 2>/dev/null || pip install -q rembg onnxruntime numpy pillow >/dev/null 2>&1
python3 scripts/fetch_assets.py "examples/$PRJ/library.json" || exit 15
echo "=== ASSETS READY $(date -u +%T) ==="

if [ "$MODE" = "snap" ]; then
  python3 src/emit_v2.py "examples/$PRJ" || exit 16
  rm -rf snapshots
  npx hyperframes snapshot . --at "$4" --no-end --timeout 20000 >/dev/null 2>&1 || exit 17
  ls snapshots/frame-*.png | sort -V > frames.txt
  # 3 frames per grid, each 480x270 (enough to judge crop, exposure, keying)
  split -l 3 -d frames.txt grp_
  n=0
  for g in grp_*; do
    montage $(cat "$g") -tile 3x1 -geometry 480x270+2+2 -background '#222' "sheet_$n.jpg" 2>/dev/null
    convert "sheet_$n.jpg" -quality 55 "sheet_$n.jpg"
    echo "===SHEET $n $(tr '\n' ' ' < "$g")==="
    base64 -w0 "sheet_$n.jpg"; echo
    echo "===END $n==="
    n=$((n + 1))
  done
  echo "=== SNAP DONE ==="
  exit 0
fi

if [ "$MODE" = "render" ]; then
  IFS=',' read -ra VOICES <<< "$4"
  mkdir -p "examples/$PRJ/vo"
  for i in "${!VOICES[@]}"; do
    curl -fsSL --retry 5 -o "examples/$PRJ/vo/c$i.mp3" "${VOICES[$i]}" || exit 21
  done
  python3 scripts/mkaudio_v2.py "examples/$PRJ" || exit 22
  python3 "examples/$PRJ/align.py" || exit 23
  python3 src/emit_v2.py "examples/$PRJ" --audio assets/audio/master.wav || exit 24
  python3 scripts/mix_sfx.py "examples/$PRJ" || exit 25
  echo "=== RENDER START $(date -u +%T) ==="
  export HF_SEGMENTED_CAPTURE=true
  npx hyperframes render . -o /home/user/master.mp4 -q high -f 30 -w 6 --resolution 1080p \
    --no-browser-gpu --browser-timeout 180 --protocol-timeout 900000 --player-ready-timeout 180000 --quiet
  RC=$?; echo "=== RENDER END rc=$RC $(date -u +%T) ==="
  [ $RC -ne 0 ] && exit 26
  ffprobe -v error -show_entries stream=codec_type,codec_name -of csv=p=0 /home/user/master.mp4
  ffmpeg -hide_banner -nostats -i /home/user/master.mp4 -af ebur128=peak=true -f null - 2>&1 | tail -12
  # light copy: browser-safe H.264, sized for ~100MB at this length
  DUR=$(ffprobe -v error -show_entries format=duration -of csv=p=0 /home/user/master.mp4)
  VB=$(python3 -c "print(int(96*8*1024/float('$DUR') - 160))")
  ffmpeg -hide_banner -loglevel error -y -i /home/user/master.mp4 -c:v libx264 -preset slow \
    -b:v ${VB}k -maxrate $((VB * 2))k -bufsize $((VB * 4))k -pix_fmt yuv420p \
    -c:a aac -b:a 160k -movflags +faststart /home/user/light.mp4 || exit 27
  ls -la /home/user/master.mp4 /home/user/light.mp4
  curl -f -X PUT -H "Content-Type: video/mp4" --upload-file /home/user/master.mp4 "$5" -o /dev/null -w 'MASTER PUT %{http_code}\n'
  curl -f -X PUT -H "Content-Type: video/mp4" --upload-file /home/user/light.mp4 "$6" -o /dev/null -w 'LIGHT PUT %{http_code}\n'
  echo "=== ALL DONE $(date -u +%T) ==="
fi
