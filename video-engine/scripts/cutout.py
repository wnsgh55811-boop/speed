# -*- coding: utf-8 -*-
"""Key subjects out of their backgrounds for the `cut_*` assets.

    python3 cutout.py <out_dir> <key>=<url> [...]

3D icons (key starts with i_) are shot on a flat pale sweep: they are keyed
by flood-filling the background from the border, which keeps their edges
crisp. Photos of people and animals go through rembg (isnet-general-use).
Every result is trimmed to its alpha bounding box plus a small margin, so
the layout can size the figure itself. Writes <out_dir>/cut_<key>.png and a
checkerboard contact sheet sheet.jpg for a quick look.
"""
import io
import os
import sys
import urllib.request

import numpy as np
from PIL import Image, ImageFilter


def fetch(url):
    with urllib.request.urlopen(url, timeout=60) as r:
        return Image.open(io.BytesIO(r.read())).convert("RGB")


def key_flat(im, tol=26):
    """Flood the background in from the border: any pixel connected to the
    edge and within `tol` of the local sweep colour becomes transparent."""
    from collections import deque
    a = np.asarray(im).astype(np.int16)
    h, w, _ = a.shape
    bg = np.zeros((h, w), bool)
    q = deque()
    for x in range(w):
        q.append((0, x)); q.append((h - 1, x))
    for y in range(h):
        q.append((y, 0)); q.append((y, w - 1))
    ref = np.median(np.concatenate([a[0], a[-1], a[:, 0], a[:, -1]]), axis=0)
    # the sweep is a soft gradient: compare with brightness-tolerant distance
    lum = a.mean(axis=2)
    chroma = np.abs(a - a.mean(axis=2, keepdims=True)).max(axis=2)
    ok = (chroma < 18) & (lum > ref.mean() - 70)
    while q:
        y, x = q.popleft()
        if bg[y, x] or not ok[y, x]:
            continue
        bg[y, x] = True
        if y > 0: q.append((y - 1, x))
        if y < h - 1: q.append((y + 1, x))
        if x > 0: q.append((y, x - 1))
        if x < w - 1: q.append((y, x + 1))
    alpha = Image.fromarray(np.where(bg, 0, 255).astype(np.uint8))
    alpha = alpha.filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(1.2))
    out = im.convert("RGBA")
    out.putalpha(alpha)
    return out


_session = None


def key_rembg(im):
    global _session
    from rembg import new_session, remove
    if _session is None:
        _session = new_session("isnet-general-use")
    return remove(im, session=_session)


def trim(im, pad=0.04):
    bb = im.getchannel("A").point(lambda v: 255 if v > 24 else 0).getbbox()
    if not bb:
        return im
    x0, y0, x1, y1 = bb
    p = int(max(x1 - x0, y1 - y0) * pad)
    return im.crop((max(0, x0 - p), max(0, y0 - p), min(im.width, x1 + p), min(im.height, y1 + p)))


def sheet(ims, path):
    cell = 300
    s = Image.new("RGB", (cell * len(ims), cell), (255, 0, 255))
    chk = Image.new("RGB", (cell, cell))
    for y in range(0, cell, 20):
        for x in range(0, cell, 20):
            chk.paste((60, 60, 60) if (x + y) // 20 % 2 else (110, 110, 110), (x, y, x + 20, y + 20))
    for k, im in enumerate(ims):
        t = im.copy()
        t.thumbnail((cell - 10, cell - 10))
        c = chk.copy()
        c.paste(t, ((cell - t.width) // 2, (cell - t.height) // 2), t)
        s.paste(c, (k * cell, 0))
    s.save(path, quality=55)


def main():
    out = sys.argv[1]
    os.makedirs(out, exist_ok=True)
    done = []
    for arg in sys.argv[2:]:
        k, url = arg.split("=", 1)
        im = fetch(url)
        im.thumbnail((1400, 1400))
        cut = key_flat(im) if k.startswith("i_") else key_rembg(im)
        cut = trim(cut)
        cut.save(os.path.join(out, f"cut_{k}.png"), optimize=True)
        done.append(cut)
        print("cut", k, cut.size, flush=True)
    sheet(done, os.path.join(out, "sheet.jpg"))


if __name__ == "__main__":
    main()
