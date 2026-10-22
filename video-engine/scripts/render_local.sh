#!/usr/bin/env bash
# Local full render (video track only). Narration is muxed afterwards by
# scripts/master_audio.py so the WAV is never re-timed by the renderer.
cd "$(dirname "$0")/.."
export HF_SEGMENTED_CAPTURE=true
echo "=== RENDER START $(date -u +%T) ==="
npx hyperframes render . -o renders/video.mp4 -q delivery -f 30 -w 4 --resolution landscape \
  --no-browser-gpu --browser-timeout 600 --protocol-timeout 900000 --player-ready-timeout 600000 \
  --resume --keep-segments --quiet
echo "=== RENDER END rc=$? $(date -u +%T) ==="
