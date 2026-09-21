# -*- coding: utf-8 -*-
"""Fetch every remote asset once, size it to what the composition shows, and
point index.html at the local copies.

    python3 scripts/localize.py

Without this, each render worker fetches all 32 plates over the network and
decodes them at 2688x1520 — six workers spent about ninety seconds each just
getting to the first frame. The plates are drawn full-bleed at 1920x1080 and
the icons at well under 600px, so nothing here is a quality decision: it is
sending the pixels that get used.

Opaque plates become JPEG, which is where most of the saving is. Anything with
an alpha channel stays PNG, because the cutouts and 3d icons depend on it.
"""
import hashlib
import io as _io
import os
import re
import sys
import urllib.request

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
OUT = os.path.join(ROOT, "assets", "img")
CACHE = os.path.join(ROOT, "assets", ".cache")
import glob
IDX = sorted(glob.glob(os.path.join(ROOT, "*.html")))

# A full-bleed plate is drawn at 1920x1080. An icon is drawn at 560px wide and
# a cutout at 820px tall, so 1280 leaves better than 1.5x for both.
PLATE, INLINE = 1920, 1280

os.makedirs(OUT, exist_ok=True)
os.makedirs(CACHE, exist_ok=True)
pages = {f: _io.open(f, encoding="utf-8").read() for f in IDX}
urls = sorted({u for h in pages.values()
               for u in re.findall(r'src="(https://[^"]+)"', h)})
print(f"[localize] {len(IDX)} composition(s), {len(urls)} remote assets")

# which ones are background plates rather than inline elements
plates = {u for h in pages.values()
          for u in re.findall(r'<img id="ph\d+" src="(https://[^"]+)"', h)}
mapping, saved_before, saved_after = {}, 0, 0

for u in urls:
    key = hashlib.sha1(u.encode()).hexdigest()[:16]
    raw = os.path.join(CACHE, key)
    if not os.path.exists(raw) or os.path.getsize(raw) == 0:
        with urllib.request.urlopen(u, timeout=120) as r, open(raw, "wb") as f:
            f.write(r.read())
    saved_before += os.path.getsize(raw)

    im = Image.open(raw)
    im.load()
    alpha = im.mode in ("RGBA", "LA") and im.getchannel("A").getextrema()[0] < 250
    cap = PLATE if u in plates else INLINE
    if max(im.size) > cap:
        s = cap / max(im.size)
        im = im.resize((round(im.width * s), round(im.height * s)),
                       Image.LANCZOS)
    if alpha:
        name = f"{key}.png"
        im.convert("RGBA").save(os.path.join(OUT, name), optimize=True)
    else:
        name = f"{key}.jpg"
        im.convert("RGB").save(os.path.join(OUT, name), quality=92,
                               subsampling=0, optimize=True)
    saved_after += os.path.getsize(os.path.join(OUT, name))
    mapping[u] = f"assets/img/{name}"
    print(f"  {'plate' if u in plates else 'inline'} "
          f"{'alpha' if alpha else 'opaque':6s} {im.size} -> {name}")

for f, html in pages.items():
    for u, local in mapping.items():
        html = html.replace(f'src="{u}"', f'src="{local}"')
    if re.search(r'src="https://', html):
        sys.exit(f"{os.path.basename(f)}: remote assets left unmapped")
    _io.open(f, "w", encoding="utf-8").write(html)
print(f"[localize] {saved_before/1e6:.1f}MB remote -> {saved_after/1e6:.1f}MB local "
      f"({saved_after/saved_before*100:.0f}%)")
