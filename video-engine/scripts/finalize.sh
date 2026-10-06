#!/usr/bin/env bash
# Join rendered parts and lay the mastered narration under them.
#
#   PROJ=projects/<name> PARTS_DIR=<dir with p00.mp4…> OUT=<dir> bash scripts/finalize.sh
#
# MASTER: parts stream-copied (no re-encode) + AAC 320k from audio/master.wav.
# LIGHT:  two-pass x264 sized for ~100 MB, faststart, plays straight from a link.
# The narration WAV is never re-timed here; the video is cut to its length.
set -euo pipefail
cd "$(dirname "$0")/.."
: "${PROJ:?}" "${PARTS_DIR:?}" "${OUT:?}"
mkdir -p "$OUT"
NAME=$(basename "$PROJ")
python3 - "$PROJ" "$PARTS_DIR" > "$OUT/parts.txt" <<'PY'
import json, os, sys
proj, d = sys.argv[1], sys.argv[2]
for m in json.load(open(os.path.join(proj, "parts", "manifest.json"))):
    print(f"file '{os.path.abspath(os.path.join(d, m['file'] + '.mp4'))}'")
PY
AUD="$PROJ/audio/master.wav"
DUR=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$AUD")
ffmpeg -hide_banner -loglevel error -f concat -safe 0 -i "$OUT/parts.txt" -c copy "$OUT/video_only.mp4" -y
ffmpeg -hide_banner -loglevel error -i "$OUT/video_only.mp4" -i "$AUD" -map 0:v -map 1:a -c:v copy \
  -c:a aac -b:a 320k -t "$DUR" -movflags +faststart "$OUT/${NAME}_MASTER.mp4" -y

# LIGHT: aim at ~98 MB total
VB=$(python3 -c "print(int((98*8*1024*1024/$DUR - 128000)/1000))")
cd "$OUT"
ffmpeg -hide_banner -loglevel error -i "${NAME}_MASTER.mp4" -c:v libx264 -preset slow -b:v ${VB}k \
  -pix_fmt yuv420p -pass 1 -passlogfile x264light -an -f mp4 /dev/null -y
ffmpeg -hide_banner -loglevel error -i "${NAME}_MASTER.mp4" -c:v libx264 -preset slow -b:v ${VB}k \
  -maxrate $((VB * 3))k -bufsize $((VB * 4))k -pix_fmt yuv420p -pass 2 -passlogfile x264light \
  -c:a aac -b:a 128k -movflags +faststart "${NAME}_LIGHT.mp4" -y
rm -f x264light*
ls -la "${NAME}_MASTER.mp4" "${NAME}_LIGHT.mp4"
for f in "${NAME}_MASTER.mp4" "${NAME}_LIGHT.mp4"; do
  ffprobe -v error -show_entries format=duration,bit_rate:stream=codec_type,codec_name,width,height \
    -of compact "$f"
done
