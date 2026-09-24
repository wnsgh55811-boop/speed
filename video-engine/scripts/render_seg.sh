#!/usr/bin/env bash
# Render one or more segments of a span-composed film inside the Higgsfield
# sandbox (one background job per call; the lease is ~15 min, so a job should
# carry ≤ ~3 minutes of film). Each finished segment is PUT to its presigned URL.
#
#   ZIP=<cdn url of pack.zip> bash render_seg.sh <k> <put_url> [<k> <put_url> ...]
#
# pack.zip: seg_<k>.html, vendor/gsap.min.js, clips.json
set -x
W=/home/user/R; mkdir -p $W && cd $W
[ -f pack.zip ] || curl -fsSL --retry 5 -o pack.zip "$ZIP" || exit 11
unzip -oq pack.zip || exit 12

mkdir -p assets/fonts
for w in Regular Medium SemiBold Bold ExtraBold; do
  [ -s assets/fonts/Pretendard-$w.otf ] || curl -fsSL --retry 5 -o assets/fonts/Pretendard-$w.otf \
    https://cdn.jsdelivr.net/npm/pretendard@1.3.9/dist/public/static/Pretendard-$w.otf || exit 13
done

# hyperframes wants node 22+
[ -d n22 ] || { curl -fsSL --retry 5 -o n22.tar.xz https://nodejs.org/dist/v22.11.0/node-v22.11.0-linux-x64.tar.xz \
  && mkdir n22 && tar xf n22.tar.xz -C n22 --strip-components=1; } || exit 14
export PATH=$W/n22/bin:$PATH
[ -d node_modules/hyperframes ] || npm i --no-audit --no-fund --silent hyperframes@0.8.52 || exit 15

# generated 5s clips → slow boomerangs (~40s) so no scene ever runs out of footage
SEGS=""; i=1; for a in "$@"; do [ $((i % 2)) -eq 1 ] && SEGS="$SEGS $a"; i=$((i+1)); done
python3 - $SEGS <<'PY' || exit 16
import json, os, re, subprocess
CDN = "https://d8j0ntlcm91z4.cloudfront.net/user_36TmLGicluGODkcYejmrwLWoKV7/"
import sys
need = set()
for k in sys.argv[1:]:                        # only the clips these segments use
    need |= set(re.findall(r'assets/(v_\w+)\.mp4', open(f"seg_{k}.html").read()))
for k, f in json.load(open("clips.json")).items():
    out = f"assets/{k}.mp4"
    if k not in need or os.path.exists(out): continue
    subprocess.run(f'curl -fsSL --retry 5 -o raw_{k}.mp4 "{CDN}{f}"', shell=True, check=True)
    gam = {"v_phone": 1.5, "v_hyena": 1.25, "v_date": 1.25}.get(k, 1.0)   # lift dark clips, never crush
    vf = f"setpts=1.35*PTS,scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,fps=30,eq=gamma={gam}:saturation=1.03"
    subprocess.run(f'ffmpeg -v error -i raw_{k}.mp4 -an -vf "{vf}" -c:v libx264 -preset veryfast -crf 16 -pix_fmt yuv420p f_{k}.mp4 -y', shell=True, check=True)
    subprocess.run(f'ffmpeg -v error -i f_{k}.mp4 -vf reverse -c:v libx264 -preset veryfast -crf 16 -pix_fmt yuv420p r_{k}.mp4 -y', shell=True, check=True)
    open(f"l_{k}.txt", "w").write("".join(f"file '{x}_{k}.mp4'\n" for x in "frfrfr"))
    # dense keyframes: the renderer seeks every frame, sparse GOPs freeze
    subprocess.run(f'ffmpeg -v error -f concat -safe 0 -i l_{k}.txt -c:v libx264 -preset veryfast -crf 16 -g 30 -keyint_min 30 '
                   f'-pix_fmt yuv420p -movflags +faststart {out} -y', shell=True, check=True)
    print("clip", k, flush=True)
PY

[ -f expo.json ] || python3 expo.py || exit 18

while [ $# -ge 2 ]; do
  K=$1; PUT=$2; shift 2
  cp seg_$K.html index.html
  echo "=== SEG $K START $(date -u +%T) ==="
  HYPERFRAMES_RENDER_DETACHED=1 npx hyperframes render . -o $W/seg_$K.mp4 -f 30 -w 6 --no-low-memory-mode -q delivery \
     --browser-timeout 180 --player-ready-timeout 180000 --quiet
  RC=$?; echo "=== SEG $K END rc=$RC $(date -u +%T) ==="
  [ $RC -ne 0 ] && exit 17
  ffprobe -v error -show_entries format=duration -of csv=p=0 $W/seg_$K.mp4
  curl -f -X PUT -H "Content-Type: video/mp4" --upload-file $W/seg_$K.mp4 "$PUT" -o /dev/null -w "UP $K %{http_code}\n"
done
echo "=== ALL DONE $(date -u +%T) ==="
