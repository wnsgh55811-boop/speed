#!/usr/bin/env bash
# Render scene-build parts inside an ephemeral sandbox (e.g. Higgsfield
# sandbox_exec). Each call must finish inside the sandbox lease, so a call
# renders a few parts and uploads each one the moment it is done.
#
#   BRANCH=<git branch> PROJ=projects/<name> PARTS="p00 p01" \
#   PUT_p00=<presigned put url> PUT_p01=<...> QUALITY=delivery \
#   bash render_parts.sh
set -o pipefail
: "${BRANCH:?set BRANCH}" "${PROJ:?set PROJ}"   # empty BRANCH would reset to the default branch
cd /home/user
REPO=${REPO:-https://github.com/wnsgh55811-boop/speed}
if [ ! -d speed/.git ]; then git clone -q --depth 1 -b "$BRANCH" "$REPO" speed || exit 11; fi
( cd speed && git fetch -q --depth 1 origin "$BRANCH" && git reset -q --hard FETCH_HEAD ) || exit 12

# hyperframes needs node 22+
[ -d node-v22.11.0-linux-x64 ] || { curl -fsSL --retry 5 -o n22.tar.xz \
  https://nodejs.org/dist/v22.11.0/node-v22.11.0-linux-x64.tar.xz && tar xf n22.tar.xz; } || exit 13
export PATH=/home/user/node-v22.11.0-linux-x64/bin:$PATH

cd speed/video-engine
[ -x node_modules/.bin/hyperframes ] || npm i -s --no-audit --no-fund hyperframes@0.8.52 gsap@3 || exit 14
P=$PROJ
mkdir -p "$P/assets" "$P/vendor" && cp -r assets/fonts "$P/assets/" && cp node_modules/gsap/dist/gsap.min.js "$P/vendor/"
python3 scripts/fetch_assets.py "$P" > /tmp/fetch.log || { tail /tmp/fetch.log; exit 15; }
[ -s "$P/assets/cut/.done" ] || { python3 scripts/paper.py --project "$P" && echo 1 > "$P/assets/cut/.done"; } || exit 16
mkdir -p "$P/assets/audio"
[ -s "$P/assets/audio/voice.wav" ] || ffmpeg -hide_banner -loglevel error -i "$P/audio/voice.flac" "$P/assets/audio/voice.wav" -y
python3 src/scenes.py "$P" || exit 17
npx hyperframes browser ensure >/dev/null 2>&1 || true

mkdir -p /home/user/out
for part in $PARTS; do
  echo "=== $part START $(date -u +%T)"
  # The sandbox closes the launching call's stdio after ~60s; hyperframes reads
  # that as its parent exiting and cancels. Detach it into its own session.
  setsid node_modules/.bin/hyperframes render "$P/parts/$part" -o "/home/user/out/$part.mp4" -q "${QUALITY:-delivery}" -f 30 \
    -w "${WORKERS:-4}" --no-low-memory-mode --no-browser-gpu --browser-timeout 180 \
    --protocol-timeout 900000 --player-ready-timeout 180000 --quiet < /dev/null > "/home/user/out/$part.log" 2>&1 &
  wait $! || { tail -5 "/home/user/out/$part.log"; exit 18; }
  ffprobe -v error -count_frames -select_streams v -show_entries stream=nb_read_frames,width,height \
    -of csv=p=0 "/home/user/out/$part.mp4"
  url_var="PUT_$part"
  if [ -n "${!url_var}" ]; then
    curl -fsS -X PUT -H "Content-Type: video/mp4" --upload-file "/home/user/out/$part.mp4" "${!url_var}" \
      -o /dev/null -w "UPLOAD $part %{http_code}\n" || exit 19
  fi
  echo "=== $part END $(date -u +%T)"
done
echo "=== ALL DONE"
