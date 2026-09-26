# -*- coding: utf-8 -*-
"""Download every still the composition uses into assets/img/.

Photos are resized to 1920 wide (they only ever fill a 1920x1080 plate);
alpha PNGs (cutouts, 3D icons) keep their transparency.
    python3 scripts/fetch_assets.py assets_manifest.json
"""
import json, os, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
from PIL import Image

man = json.load(open(sys.argv[1]))
os.makedirs("assets/img", exist_ok=True)


def get(item):
    dst, url = item
    if os.path.exists(dst) and os.path.getsize(dst) > 0:
        return dst, "cached"
    tmp = dst + ".dl"
    subprocess.run(["curl", "-fsSL", "--retry", "5", "-o", tmp, url], check=True)
    im = Image.open(tmp)
    if im.width > 1920:
        im = im.resize((1920, round(im.height * 1920 / im.width)), Image.LANCZOS)
    im.save(dst, optimize=True)
    os.remove(tmp)
    return dst, im.mode


with ThreadPoolExecutor(8) as ex:
    for dst, mode in ex.map(get, man.items()):
        print(dst, mode)
print("ASSETS", len(man))
