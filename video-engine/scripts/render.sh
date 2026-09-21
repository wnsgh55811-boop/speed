#!/usr/bin/env bash
# Delivery render for one project, meant to run inside the media sandbox.
#
#   PROJECT=talk PARTS=6 ONLY=1 bash scripts/render.sh
#
# The film is emitted as PARTS scene-aligned pieces and rendered one at a time.
# A fourteen-minute capture does not fit in one sandbox lease, and the sandbox
# is reclaimed shortly after a call returns, so each piece is uploaded the
# moment it finishes: an interrupted run resumes from the pieces already in
# hand instead of starting the film again.
set -x
P=${PROJECT:-talk}
N=${PARTS:-6}
cd "$(dirname "$0")/.."
export PATH=/home/user/node22/bin:$PATH
node -v

# The composition references the narration by path, so it has to exist before
# the render starts; building it in parallel fails the run in the first minute.
mkdir -p assets/audio
if [ ! -s assets/audio/master.mp3 ]; then
  ( cd "examples/$P" && python3 mkaudio.py && cp out/master.mp3 ../../assets/audio/master.mp3 ) || exit 12
fi
[ -s assets/audio/master.mp3 ] || exit 12

# Emit the pieces, then cut the narration on the same boundaries. The pieces
# tile the film exactly, so each offset is just the sum of what came before.
cp "examples/$P/plan.py" "examples/$P/chunks.json" "examples/$P/timings.txt" src/
for k in $(seq 1 "$N"); do
  python3 src/emit.py --audio "assets/audio/part$(printf %02d "$k").mp3" --part "$k/$N" || exit 13
done
python3 - "$N" <<'PYX' || exit 13
import io, os, re, subprocess, sys
n = int(sys.argv[1])
off = 0.0
for k in range(1, n + 1):
    f = f"part{k:02d}.html"
    d = float(re.search(r'id="root"[^>]*data-duration="([\d.]+)"',
                        io.open(f, encoding="utf-8").read()).group(1))
    out = f"assets/audio/part{k:02d}.mp3"
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
                    "-ss", f"{off:.3f}", "-t", f"{d:.3f}",
                    "-i", "assets/audio/master.mp3",
                    "-c:a", "libmp3lame", "-b:a", "192k", out], check=True)
    print(f"[audio] {out} {off:.2f}+{d:.2f}s")
    off += d
PYX

# Send the workers the pixels they actually draw: six of them each fetching
# and decoding 2688x1520 plates over the network cost about ninety seconds
# apiece before the first frame.
python3 scripts/localize.py || exit 14

for k in $(seq 1 "$N"); do
  KK=$(printf %02d "$k")
  [ -n "$ONLY" ] && [ "$ONLY" != "$k" ] && continue
  [ -s "/home/user/part$KK.mp4" ] && { echo "part $KK already rendered"; continue; }
  echo "=== PART $KK START $(date -u +%T) ==="
  export HF_SEGMENTED_CAPTURE=true
  npx hyperframes render "part$KK.html" -o "/home/user/part$KK.mp4" \
    -q delivery -f 30 -w 6 --resolution 1080p --no-browser-gpu --best-effort \
    --browser-timeout 300 --protocol-timeout 1800000 \
    --player-ready-timeout 300000 --resume --quiet
  RC=$?; echo "=== PART $KK END rc=$RC $(date -u +%T) ==="
  [ $RC -ne 0 ] && exit 16
  ffprobe -v error -show_entries format=duration -of csv=p=0 "/home/user/part$KK.mp4"
  if [ -s "/home/user/up/part$KK.url" ]; then
    curl -f -X PUT -H "Content-Type: video/mp4" --upload-file "/home/user/part$KK.mp4" \
      "$(cat /home/user/up/part$KK.url)" -o /dev/null -w "PART $KK UPLOAD %{http_code}\n"
  fi
done
echo "=== PARTS DONE $(date -u +%T) ==="
