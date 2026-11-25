#!/usr/bin/env bash
# One-time setup: fonts, faster-whisper venv, checks. Safe to re-run.
set -e
CACHE="${REELKIT_HOME:-$HOME/.cache/reelkit}"
mkdir -p "$CACHE/fonts"
B=https://raw.githubusercontent.com/google/fonts/main/ofl
for f in gothica1/GothicA1-Medium.ttf gothica1/GothicA1-Bold.ttf gothica1/GothicA1-Black.ttf \
         nanumpenscript/NanumPenScript-Regular.ttf notocoloremoji/NotoColorEmoji-Regular.ttf; do
  n=$(basename "$f"); [ -s "$CACHE/fonts/$n" ] || curl -sSfL "$B/$f" -o "$CACHE/fonts/$n"
done
if [ ! -x "$CACHE/venv/bin/python" ]; then
  python3 -m venv "$CACHE/venv"
  "$CACHE/venv/bin/pip" install -q faster-whisper numpy
fi
command -v ffmpeg >/dev/null || { echo "ffmpeg missing"; exit 1; }
node -e "require('playwright')" 2>/dev/null || echo "WARN: playwright not found for node (npm i -g playwright && npx playwright install chromium)"
python3 -c "import PIL, numpy" 2>/dev/null || echo "WARN: python3 needs pillow + numpy (pip install pillow numpy)"
echo "REELKIT_HOME=$CACHE"
