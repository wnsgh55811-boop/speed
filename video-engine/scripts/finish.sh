#!/usr/bin/env bash
# Join the rendered pieces into the two deliverables.
#
#   bash scripts/finish.sh 6
#
# The pieces come off the same encoder with the same settings, so the join is
# a stream copy — the master is never re-encoded. The light copy's bitrate is
# computed from the real duration so the ~100MB target is hit rather than
# guessed at, and two passes put the bits where the picture needs them.
set -x
N=${1:-6}
cd /home/user
: > parts.txt
for k in $(seq 1 "$N"); do
  KK=$(printf %02d "$k")
  [ -s "part$KK.mp4" ] || { echo "missing part$KK.mp4"; exit 10; }
  echo "file '/home/user/part$KK.mp4'" >> parts.txt
done
ffmpeg -hide_banner -loglevel error -y -f concat -safe 0 -i parts.txt -c copy master.mp4 || exit 11
ffprobe -v error -show_entries stream=codec_type,codec_name,width,height,r_frame_rate -of csv=p=0 master.mp4
ffprobe -v error -show_entries format=duration,size -of csv=p=0 master.mp4

D=$(ffprobe -v error -show_entries format=duration -of csv=p=0 master.mp4)
VB=$(python3 -c "print(int((100*8*1000*1000/$D) - 128))")
echo "=== LIGHT target ${VB}k video + 128k audio ==="
ffmpeg -hide_banner -loglevel error -y -i master.mp4 -c:v libx264 -preset slow \
  -b:v ${VB}k -pass 1 -an -f mp4 /dev/null &&
ffmpeg -hide_banner -loglevel error -y -i master.mp4 -c:v libx264 -preset slow \
  -b:v ${VB}k -pass 2 -pix_fmt yuv420p -c:a aac -b:a 128k -movflags +faststart \
  light.mp4 || exit 19
ls -la master.mp4 light.mp4
ffmpeg -hide_banner -nostats -i master.mp4 -af ebur128=peak=true -f null - 2>&1 | tail -6

curl -f -X PUT -H "Content-Type: video/mp4" --upload-file master.mp4 \
  "$(cat /home/user/up/master.url)" -o /dev/null -w 'MASTER UPLOAD %{http_code}\n' || exit 20
curl -f -X PUT -H "Content-Type: video/mp4" --upload-file light.mp4 \
  "$(cat /home/user/up/light.url)" -o /dev/null -w 'LIGHT UPLOAD %{http_code}\n' || exit 21
echo "=== ALL DONE $(date -u +%T) ==="
