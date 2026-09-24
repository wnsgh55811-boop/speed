#!/usr/bin/env bash
# Take a freshly provisioned media sandbox all the way to the deliverables.
#
#   setsid nohup bash scripts/bootstrap.sh </dev/null > /home/user/b.log 2>&1 &
#
# The sandbox is reclaimed without warning and takes its whole filesystem with
# it, so this script is written to be relaunched rather than resumed by hand:
# every part that already reached the CDN is pulled back instead of rendered
# again, and the render itself only touches the parts still missing.
#
# /home/user/up/get.txt  lines of "<NN> <public url>" for parts already uploaded
# /home/user/up/partNN.url  presigned PUT target for a part not yet uploaded
set -x
P=${PROJECT:-talk}
N=${PARTS:-6}
REPO=${REPO:-wnsgh55811-boop/speed}
BR=${BR:-claude/happy-gauss-ayxyme}
ROOT=/home/user/proj/video-engine

# Node 22. The sandbox image ships an older runtime that the renderer rejects.
export PATH=/home/user/node22/bin:$PATH
if ! node -v 2>/dev/null | grep -q '^v2[2-9]'; then
  cd /home/user
  curl -fsSL -o n22.tar.xz https://nodejs.org/dist/v22.14.0/node-v22.14.0-linux-x64.tar.xz || exit 2
  rm -rf node22 && mkdir node22 && tar -xJf n22.tar.xz -C node22 --strip-components=1 || exit 2
fi
node -v || exit 2

# Project tree. node_modules is deliberately left in place on a relaunch.
cd /tmp && rm -rf sz s.zip
curl -fsSL -o s.zip "https://codeload.github.com/$REPO/zip/refs/heads/$BR" || exit 3
unzip -q s.zip -d sz || exit 3
SRC=$(echo /tmp/sz/*/video-engine)
mkdir -p "$ROOT"
cp -r "$SRC"/src "$SRC"/scripts "$SRC"/examples "$SRC"/assets "$SRC"/vendor \
      "$SRC"/build.sh "$SRC"/hyperframes.json "$SRC"/package.json "$ROOT"/ || exit 3
rm -rf "$ROOT"/src/__pycache__ "$ROOT"/part*.html

cd "$ROOT"
[ -d node_modules/hyperframes ] || npm i --no-audit --no-fund --loglevel=error || exit 4

# Pull back the parts that survived an earlier sandbox.
mkdir -p /home/user/up
if [ -s /home/user/up/get.txt ]; then
  while read -r k url; do
    [ -z "$k" ] && continue
    [ -s "/home/user/part$k.mp4" ] && continue
    # A part is only worth keeping if it decodes and runs the length a part
    # runs; a truncated or 404 body must not stand in for a rendered piece.
    if curl -fsSL -o "/home/user/part$k.mp4" "$url"; then
      D=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "/home/user/part$k.mp4" 2>/dev/null)
      case $D in ''|0*|1[0-2]*) echo "part$k recovered body unusable (${D:-no duration})"
        rm -f "/home/user/part$k.mp4";; *) echo "part$k recovered ${D}s";; esac
    else
      rm -f "/home/user/part$k.mp4"
    fi
  done < /home/user/up/get.txt
fi
ls -la /home/user/part*.mp4 2>/dev/null

# Building the narration and fetching 80-odd images costs about seven of a
# lease's fifteen minutes. The first lease does it once and publishes the
# result along with the upload targets (prep.url); every later lease is
# launched with only the archive's address (prep.get) and restores all of it.
if [ -s /home/user/up/prep.get ] && [ ! -s assets/audio/master.mp3 ]; then
  rm -rf /home/user/prep && mkdir -p /home/user/prep
  curl -fsSL "$(cat /home/user/up/prep.get)" | tar -xz -C /home/user/prep || exit 7
  mkdir -p assets/audio assets/.cache
  cp /home/user/prep/master.mp3 assets/audio/master.mp3
  cp -rn /home/user/prep/cache/. assets/.cache/
  cp -n /home/user/prep/up/* /home/user/up/ 2>/dev/null
  echo "=== PREP RESTORED $(date -u +%T) ==="
fi
if [ -s /home/user/up/prep.url ] && [ ! -s /home/user/up/prep.get ]; then
  PREP_ONLY=1 PROJECT=$P PARTS=$N bash scripts/render.sh || exit 5
  rm -rf /home/user/prep && mkdir -p /home/user/prep/up
  cp assets/audio/master.mp3 /home/user/prep/ && cp -r assets/.cache /home/user/prep/cache
  cp /home/user/up/* /home/user/prep/up/
  tar -czf /home/user/prep.tgz -C /home/user/prep . || exit 8
  curl -f -X PUT -H "Content-Type: application/octet-stream" --upload-file /home/user/prep.tgz \
    "$(cat /home/user/up/prep.url)" -o /dev/null -w 'PREP UPLOAD %{http_code}\n' || exit 8
fi
PROJECT=$P PARTS=$N bash scripts/render.sh || exit 5
[ -n "$NO_FINISH" ] && exit 0
PROJECT=$P bash scripts/finish.sh "$N" || exit 6
echo "=== BOOTSTRAP DONE $(date -u +%T) ==="
