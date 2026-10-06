#!/usr/bin/env bash
# Join rendered parts, lay the narration under them, and write MASTER + LIGHT.
#
#   PART_URLS="<p00.mp4> <p01.mp4> ..." AUDIO=<voice.wav> TOTAL=<seconds> \
#   PUT_MASTER=<presigned put> PUT_LIGHT=<presigned put> bash finish_parts.sh
#
# Parts are cut on frame boundaries by scenes.py, so a stream-copy concat lines
# up with the voice exactly; the voice itself is muxed untouched apart from the
# AAC encode (no tempo change, no re-timing).
set -o pipefail
W=/home/user/fin; mkdir -p $W; cd $W
i=0; : > list.txt
for u in $PART_URLS; do
  f=$(printf "p%02d.mp4" $i)
  [ -s "$f" ] || curl -fsSL --retry 5 -o "$f" "$u" || exit 21
  echo "file '$f'" >> list.txt; i=$((i+1))
done
ffmpeg -hide_banner -loglevel error -f concat -safe 0 -i list.txt -c copy video.mp4 -y || exit 22
ffmpeg -hide_banner -loglevel error -i video.mp4 -i "$AUDIO" -map 0:v -map 1:a -c:v copy \
  -c:a aac -b:a 320k -ar 48000 -t "$TOTAL" -movflags +faststart MASTER.mp4 -y || exit 23
# LIGHT: same picture, web-sized, opens straight from a link
ffmpeg -hide_banner -loglevel error -i MASTER.mp4 -c:v libx264 -preset slow -crf 23 \
  -maxrate 2600k -bufsize 5200k -pix_fmt yuv420p -profile:v high -c:a aac -b:a 160k \
  -movflags +faststart LIGHT.mp4 -y || exit 24
for f in MASTER LIGHT; do
  ffprobe -v error -show_entries format=duration,size:stream=codec_name,width,height,nb_frames \
    -of compact=p=0 $f.mp4
done
ffmpeg -hide_banner -nostats -i MASTER.mp4 -af ebur128=peak=true -f null - 2>&1 | grep -A12 Summary | grep -E "I:|Peak:"
[ -n "$PUT_MASTER" ] && curl -fsS -X PUT -H "Content-Type: video/mp4" --upload-file MASTER.mp4 "$PUT_MASTER" -o /dev/null -w "UPLOAD MASTER %{http_code}\n"
[ -n "$PUT_LIGHT" ] && curl -fsS -X PUT -H "Content-Type: video/mp4" --upload-file LIGHT.mp4 "$PUT_LIGHT" -o /dev/null -w "UPLOAD LIGHT %{http_code}\n"
echo "=== FINISH DONE"
