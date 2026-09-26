#!/usr/bin/env bash
# Stitch rendered slices, lay narration + sfx, master loudness, encode the
# MASTER and a ~100 MB LIGHT copy, upload both.
#   SEGS="url1 url2 ..." VOICE=<mp3 url> TOTAL=387.52 PUT_MASTER=.. PUT_LIGHT=.. bash final.sh
set -x
cd /home/user && mkdir -p fin && cd fin
i=0; : > list.txt
for u in $SEGS; do curl -fsSL --retry 5 -o s$i.mp4 "$u" || exit 21; echo "file 's$i.mp4'" >> list.txt; i=$((i+1)); done
ffmpeg -hide_banner -loglevel error -f concat -safe 0 -i list.txt -c copy video.mp4 -y || exit 22
curl -fsSL --retry 5 -o voice.mp3 "$VOICE" || exit 23
python3 /home/user/speed/video-engine/scripts/mksfx.py /home/user/speed/video-engine/examples/katalk/sfx.json $TOTAL sfx.wav || exit 24
# voice first: +0.8 dB lifts the -15.3 LUFS narration to ~-14.5; sfx sits ~20 dB under
ffmpeg -hide_banner -loglevel error -i voice.mp3 -i sfx.wav -filter_complex \
  "[0:a]aresample=48000,volume=0.8dB[v];[1:a]aresample=48000,volume=-8dB[s];[v][s]amix=inputs=2:duration=first:normalize=0,alimiter=limit=0.87:level=false[m]" \
  -map "[m]" -ar 48000 -ac 2 mix.wav -y || exit 25
ffmpeg -hide_banner -nostats -i mix.wav -af loudnorm=print_format=summary -f null - 2>&1 | grep -E "Input Integrated|Input True Peak"
ffprobe -v error -show_entries format=duration -of csv=p=0 video.mp4
ffmpeg -hide_banner -loglevel error -i video.mp4 -i mix.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 320k \
  -shortest -movflags +faststart MASTER.mp4 -y || exit 26
ffmpeg -hide_banner -loglevel error -i video.mp4 -i mix.wav -map 0:v -map 1:a -c:v libx264 -preset medium \
  -b:v ${LIGHT_KBPS:-1850}k -maxrate 3500k -bufsize 7000k -pix_fmt yuv420p -profile:v high -c:a aac -b:a 160k \
  -shortest -movflags +faststart LIGHT.mp4 -y || exit 27
ls -la MASTER.mp4 LIGHT.mp4
ffprobe -v error -show_entries stream=codec_type,codec_name,width,height -of csv=p=0 LIGHT.mp4
curl -f -X PUT -H "Content-Type: video/mp4" --upload-file MASTER.mp4 "$PUT_MASTER" -o /dev/null -w "UP_MASTER %{http_code}\n"
curl -f -X PUT -H "Content-Type: video/mp4" --upload-file LIGHT.mp4 "$PUT_LIGHT" -o /dev/null -w "UP_LIGHT %{http_code}\n"
echo FINALDONE
