# -*- coding: utf-8 -*-
"""Per-image exposure for full-frame plates (run in the render sandbox).

The dark mood belongs to the backgrounds, never to the photographs. Generated
night scenes came back at a mean luma of 34-65/255 and read as black boxes on a
phone, so every plate photo is measured and lifted toward ~100/255 with its own
CSS brightness (1.0-1.55x). Also lightens the plate's top-half shade.

    python3 expo.py        # patches seg_*.html in place
"""
import glob
import io
import json
import re
import subprocess

from PIL import Image, ImageStat

segs = sorted(glob.glob("seg_*.html"))
urls = set()
for f in segs:
    urls |= set(re.findall(r'<div class="kb" data-kb="\w+"><img class="" src="([^"]+)"', open(f).read()))
fac = {}
for u in urls:
    raw = subprocess.run(["curl", "-fsSL", u], capture_output=True).stdout
    L = ImageStat.Stat(Image.open(io.BytesIO(raw)).convert("L").resize((320, 180))).mean[0]
    fac[u] = round(max(1.0, min(1.55, 102 / max(L, 1))), 2)
for f in segs:
    s = open(f).read()
    for u, b in fac.items():
        s = s.replace(f'<img class="" src="{u}" alt="" style="">',
                      f'<img class="" src="{u}" alt="" style="filter:brightness({b}) contrast(1.05) saturate(1.02)">')
    s = s.replace("rgba(6,7,10,.10) 0%, rgba(6,7,10,.08) 45%, rgba(6,7,10,.50) 100%",
                  "rgba(6,7,10,.0) 0%, rgba(6,7,10,.0) 50%, rgba(6,7,10,.45) 100%")
    open(f, "w").write(s)
json.dump(fac, open("expo.json", "w"), indent=1)
print("exposure", sorted(fac.values()))
