# -*- coding: utf-8 -*-
"""Fetch a scene project's stills (assets.json) into assets/img and assets/raw.

    python3 scripts/fetch_assets.py projects/<name>

Photos and 3D icons go to assets/img/<key>.png. Cutout people (cut_*) go to
assets/raw/ and are turned into torn-paper cards by `paper.py --project`.
Icons are trimmed to their alpha so the layout centres the object, not the
empty square around it. Run where the asset CDN is reachable.
"""
import json, os, subprocess, sys
from PIL import Image

proj = sys.argv[1]
assets = json.load(open(os.path.join(proj, "assets.json")))
for d in ("img", "raw"):
    os.makedirs(os.path.join(proj, "assets", d), exist_ok=True)
for k, url in assets.items():
    dst = os.path.join(proj, "assets", "raw" if k.startswith("cut_") else "img", f"{k}.png")
    if not os.path.exists(dst) or os.path.getsize(dst) == 0:
        subprocess.run(["curl", "-fsSL", "--retry", "5", "-o", dst, url], check=True)
    im = Image.open(dst)
    if k.startswith("ico_") and im.mode == "RGBA":
        bb = im.getchannel("A").point(lambda v: 255 if v > 8 else 0).getbbox()
        if bb and bb != (0, 0) + im.size:
            im.crop(bb).save(dst)
    elif k.startswith("br_"):
        # 2k stills are plenty for a 1080p plate; keep decode cheap during capture
        if im.size[0] > 2100:
            im.convert("RGB").resize((2048, round(2048 * im.size[1] / im.size[0])), Image.LANCZOS).save(dst)
    print(k, Image.open(dst).size, flush=True)
print("ASSETS DONE")
