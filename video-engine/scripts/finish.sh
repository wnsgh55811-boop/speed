#!/usr/bin/env bash
# Join the rendered pieces into the two deliverables.
#
#   bash scripts/finish.sh 6
#
# The pieces come off the same encoder with the same settings, so the picture
# is joined by stream copy and the master is never re-encoded.
#
# The sound is not joined. Each piece carries its own AAC cut of the narration,
# and stream-copying six of those back together leaves an encoder-delay seam at
# every boundary — five audible clicks through a single continuous read, which
# is the whole artifact this narration was recorded in long blocks to avoid.
# The pieces tile the film exactly, so the master takes its video from the join
# and its audio in one piece from the narration master instead.
set -x
N=${1:-${PARTS:-6}}
P=${PROJECT:-talk}
ROOT=/home/user/proj/video-engine
AUD=$ROOT/assets/audio/master.mp3
cd /home/user
[ -s "$AUD" ] || { echo "missing $AUD"; exit 9; }
: > parts.txt
for k in $(seq 1 "$N"); do
  KK=$(printf %02d "$k")
  [ -s "part$KK.mp4" ] || { echo "missing part$KK.mp4"; exit 10; }
  echo "file '/home/user/part$KK.mp4'" >> parts.txt
done
ffmpeg -hide_banner -loglevel error -y -f concat -safe 0 -i parts.txt -c:v copy -an mute.mp4 || exit 11
ffmpeg -hide_banner -loglevel error -y -i mute.mp4 -i "$AUD" \
  -map 0:v:0 -map 1:a:0 -c:v copy -c:a aac -b:a 192k -ar 48000 -ac 2 \
  -movflags +faststart -shortest master.mp4 || exit 12
ffprobe -v error -show_entries stream=codec_type,codec_name,width,height,r_frame_rate,sample_rate -of csv=p=0 master.mp4
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
# Both deliverables must actually carry the narration, not merely declare a track.
for f in master.mp4 light.mp4; do
  echo "--- $f ---"
  ffmpeg -hide_banner -nostats -i "$f" -af ebur128=peak=true -f null - 2>&1 | tail -5
done

curl -f -X PUT -H "Content-Type: video/mp4" --upload-file master.mp4 \
  "$(cat /home/user/up/master.url)" -o /dev/null -w 'MASTER UPLOAD %{http_code}\n' || exit 20
curl -f -X PUT -H "Content-Type: video/mp4" --upload-file light.mp4 \
  "$(cat /home/user/up/light.url)" -o /dev/null -w 'LIGHT UPLOAD %{http_code}\n' || exit 21
echo "=== ALL DONE $(date -u +%T) ==="
