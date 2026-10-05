#!/usr/bin/env bash
# Prepare the render workspace inside the Higgsfield sandbox:
# project from GitHub, fonts + gsap from npm, generated images from Higgsfield CDN.
set -e
W=/home/user/vsl; mkdir -p $W && cd $W
if [ ! -f index.html ]; then
  curl -fsSL https://codeload.github.com/wnsgh55811-boop/speed/tar.gz/refs/heads/claude/gallant-feynman-x9idy8 | tar xz --strip-components=2 --wildcards '*/idasa-vsl/*'
fi
mkdir -p raw assets
python3 - <<'PY'
import json, subprocess, os, concurrent.futures as cf
a = json.load(open('assets.json'))
def get(kv):
    k, u = kv
    if not os.path.exists(f'raw/{k}.png'):
        subprocess.run(['curl', '-fsSL', '--retry', '3', '-o', f'raw/{k}.png', u], check=True)
with cf.ThreadPoolExecutor(16) as ex: list(ex.map(get, a.items()))
from PIL import Image, ImageFilter
import numpy as np
for k in a:
    im = Image.open(f'raw/{k}.png')
    if k.startswith('p'):
        im = im.convert('RGB'); w, h = im.size; s = max(1920 / w, 1080 / h)
        im = im.resize((round(w * s), round(h * s)), Image.LANCZOS)
        L = (im.width - 1920) // 2; T = (im.height - 1080) // 2
        im = im.crop((L, T, L + 1920, T + 1080)).filter(ImageFilter.UnsharpMask(radius=1.6, percent=60, threshold=2))
        im.save(f'assets/{k}.jpg', quality=93)
    else:
        arr = np.asarray(im.convert('RGB')).astype(float)
        c = np.concatenate([arr[:20, :20].reshape(-1, 3), arr[-20:, -20:].reshape(-1, 3), arr[:20, -20:].reshape(-1, 3), arr[-20:, :20].reshape(-1, 3)])
        d = np.sqrt(((arr - np.median(c, 0)) ** 2).sum(-1)); al = np.clip((d - 6) / 22, 0, 1)
        o = Image.fromarray(np.dstack([arr, al * 255]).astype('uint8'), 'RGBA'); o = o.crop(o.getbbox())
        w, h = o.size; S = max(w, h) + 40; cv = Image.new('RGBA', (S, S), (0, 0, 0, 0)); cv.paste(o, ((S - w) // 2, (S - h) // 2))
        cv.resize((600, 600), Image.LANCZOS).save(f'assets/{k}.png')
print('assets', len(os.listdir('assets')))
PY
