#!/bin/bash
# Second half of the build. The sandbox lease is 15 minutes, so the render runs
# in a sandbox of its own: phase A already produced the project and parked it
# on S3 as a tarball.
set -e
BUNDLE="$1"
export PATH=/opt/node22/bin:$PATH
export PRODUCER_PAGE_NAVIGATION_TIMEOUT_MS=300000
export PRODUCER_PLAYER_READY_TIMEOUT_MS=300000
export PRODUCER_PUPPETEER_PROTOCOL_TIMEOUT_MS=1800000
cd /home/user && rm -rf v2 && curl -fsSL --retry 3 -o bundle.tar "$BUNDLE" && tar -xf bundle.tar
cd v2
echo "== render =="
date +%s > out/t0
npx --yes hyperframes@0.8.56 render --quality delivery --workers 8 --no-low-memory-mode \
  --browser-timeout 300 --output /home/user/v2/out/video.mp4 > out/render.log 2>&1
echo "RENDER_EXIT=$? elapsed=$(( $(date +%s) - $(cat out/t0) ))s" > out/status.txt

ffmpeg -v error -i out/video.mp4 -i assets/audio/master.mp3 -c:v copy -c:a aac -b:a 160k \
  -map 0:v:0 -map 1:a:0 -shortest -movflags +faststart -y out/final.mp4
echo "MUX_EXIT=$?" >> out/status.txt
ffmpeg -v error -i out/final.mp4 -c:v libx264 -preset veryfast -profile:v high -b:v 1250k \
  -maxrate 1600k -bufsize 3200k -pix_fmt yuv420p -c:a aac -b:a 96k \
  -movflags +faststart -y out/final_web.mp4
echo "WEB_EXIT=$?" >> out/status.txt
ffmpeg -v error -i out/final.mp4 -vf "select='not(mod(n\,1700))',scale=640:-1,tile=3x3" \
  -frames:v 1 -y out/sheet.jpg
ls -la out/ >> out/status.txt

# Upload inside this same job: the sandbox is discarded once the call returns,
# so anything left on disk for a later call is lost.
if [ -f /home/user/up_urls.sh ]; then
  . /home/user/up_urls.sh
  curl -f -X PUT -H "Content-Type: image/jpeg" --data-binary @out/sheet.jpg "$U_SHEET" \
       -s -o /dev/null -w "sheet:%{http_code}\n" >> out/status.txt 2>&1
  curl -f -X PUT -H "Content-Type: video/mp4" --data-binary @out/final_web.mp4 "$U_WEB" \
       -s -o /dev/null -w "web:%{http_code} %{size_upload}\n" >> out/status.txt 2>&1
  curl -f -X PUT -H "Content-Type: video/mp4" --data-binary @out/final.mp4 "$U_FULL" \
       -s -o /dev/null -w "full:%{http_code} %{size_upload}\n" >> out/status.txt 2>&1
fi
echo DONE >> out/status.txt
