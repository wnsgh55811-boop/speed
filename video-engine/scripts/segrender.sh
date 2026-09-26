#!/usr/bin/env bash
# Render one time slice of the film inside the ephemeral sandbox and ship it.
#   SEG_FROM=0 SEG_TO=80 SEG_NAME=s0 PUT_URL=<presigned> bash scripts/segrender.sh
# The sandbox only lives while a job runs, so each slice is rendered, checked
# and uploaded in one go; the final pass stitches slices and lays the audio.
set -x
cd "$(dirname "$0")/.."
export PATH=/home/user/node-v22.11.0-linux-x64/bin:$PATH
PROJECT=${PROJECT:-examples/katalk} python3 src/emit.py --from $SEG_FROM --to $SEG_TO --out index.html || exit 11
export HF_SEGMENTED_CAPTURE=true
npx hyperframes render . -o /home/user/$SEG_NAME.mp4 -q delivery -f 30 -w ${WORKERS:-6} \
  --resolution 1080p --no-browser-gpu --best-effort --browser-timeout 180 \
  --protocol-timeout 900000 --quiet || exit 16
ffprobe -v error -show_entries format=duration -of csv=p=0 /home/user/$SEG_NAME.mp4
[ -n "$PUT_URL" ] && curl -f -X PUT -H "Content-Type: video/mp4" --upload-file /home/user/$SEG_NAME.mp4 "$PUT_URL" \
  -o /dev/null -w "UPLOAD %{http_code}\n"
echo SEGDONE
