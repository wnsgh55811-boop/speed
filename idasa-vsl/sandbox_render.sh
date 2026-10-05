#!/usr/bin/env bash
# Parallel frame render -> segment mp4s -> concat -> HQ + preview, then upload.
#   HQ_PUT=<presigned> PV_PUT=<presigned> WORKERS=6 bash sandbox_render.sh
cd /home/user/vsl
export NODE_PATH=/usr/local/lib/node_modules
N=$(node render.js info | python3 -c "import json,sys;print(int(json.load(sys.stdin)['dur']*30)+1)")
WK=${WORKERS:-6}; CH=$(( (N + WK - 1) / WK ))
echo "frames=$N workers=$WK chunk=$CH start $(date -u +%T)"
rm -f seg_*.mp4
for i in $(seq 0 $((WK-1))); do
  S=$((i*CH)); E=$(( (i+1)*CH )); [ $E -gt $N ] && E=$N
  ( node render.js - 30 $S $E 2>>log_$i.txt | ffmpeg -hide_banner -loglevel error -f image2pipe -framerate 30 -c:v mjpeg -i - \
      -c:v libx264 -preset medium -crf 15 -pix_fmt yuv420p -r 30 seg_$i.mp4 -y && echo "seg $i done $(date -u +%T)" ) &
done
wait
ls seg_*.mp4 | sort -V | sed 's/^/file /' > segs.txt
ffmpeg -hide_banner -loglevel error -f concat -safe 0 -i segs.txt -c copy final_hq.mp4 -y
ffmpeg -hide_banner -loglevel error -i final_hq.mp4 -vf scale=1280:720:flags=lanczos -c:v libx264 -preset veryfast -crf 25 -pix_fmt yuv420p -movflags +faststart preview.mp4 -y
ffmpeg -hide_banner -loglevel error -i final_hq.mp4 -c copy -movflags +faststart idasa_hq.mp4 -y
ls -la idasa_hq.mp4 preview.mp4
[ -n "$HQ_PUT" ] && curl -fsS -X PUT -H "Content-Type: video/mp4" --upload-file idasa_hq.mp4 "$HQ_PUT" -o /dev/null -w "HQ %{http_code}\n"
[ -n "$PV_PUT" ] && curl -fsS -X PUT -H "Content-Type: video/mp4" --upload-file preview.mp4 "$PV_PUT" -o /dev/null -w "PV %{http_code}\n"
echo "ALL DONE $(date -u +%T)"
