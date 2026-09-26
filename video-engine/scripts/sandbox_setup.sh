#!/usr/bin/env bash
# One-time prep in a fresh Higgsfield sandbox: node 22, npm deps, fonts, gsap.
set -e
cd /home/user
[ -d node-v22.11.0-linux-x64 ] || { curl -fsSL --retry 5 -o n22.tar.xz \
  https://nodejs.org/dist/v22.11.0/node-v22.11.0-linux-x64.tar.xz && tar xf n22.tar.xz; }
export PATH=/home/user/node-v22.11.0-linux-x64/bin:$PATH
cd /home/user/speed/video-engine
bash scripts/setup.sh
pip install -q pillow 2>/dev/null || true
npx hyperframes browser ensure >/dev/null 2>&1 || true
echo SETUP_OK
