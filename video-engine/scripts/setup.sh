#!/usr/bin/env bash
# Local deps for build + render: fonts and GSAP come from npm, not the repo.
set -e
cd "$(dirname "$0")/.."
[ -d node_modules/pretendard ] || npm i --no-audit --no-fund --silent hyperframes@0.8.78 gsap pretendard
mkdir -p assets/fonts vendor
for w in Regular Medium SemiBold Bold ExtraBold Black; do
  cp -n node_modules/pretendard/dist/public/static/Pretendard-$w.otf assets/fonts/ 2>/dev/null || true
done
cp node_modules/gsap/dist/gsap.min.js vendor/
