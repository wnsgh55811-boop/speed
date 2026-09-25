# -*- coding: utf-8 -*-
"""Frame QA numbers + small inspection sheets from hyperframes snapshots.

    python3 scripts/qa_frames.py "<t1,t2,...>"

Prints per-frame exposure (mean / centre mean / % crushed / % clipped) and
per-cutout alpha checks (opaque border = plate not removed), and writes
qa/sheet_<n>.jpg (2x2 frames, 320x180 each) and qa/keyed.jpg (every keyed
icon on mid-grey) small enough to pull back as base64 for a visual pass.
"""
import glob
import os
import re
import sys

import numpy as np
from PIL import Image

times = sys.argv[1].split(",")
os.makedirs("qa", exist_ok=True)
fs = sorted(glob.glob("snapshots/frame-*.png"), key=lambda p: int(re.search(r"frame-(\d+)", p).group(1)))
print("FRAME      t  mean  ctr  crushed%  clipped%")
for f, t in zip(fs, times):
    a = np.asarray(Image.open(f).convert("L")).astype(float)
    c = a[200:880, 400:1520]
    flag = "  <- dark" if c.mean() < 45 else ""
    print(f"{t:>11} {a.mean():5.0f} {c.mean():5.0f} {100 * (a < 18).mean():8.1f} {100 * (a > 245).mean():8.1f}{flag}")
for n in range(0, len(fs), 4):
    sh = Image.new("RGB", (644, 364), (40, 40, 40))
    for j, f in enumerate(fs[n:n + 4]):
        sh.paste(Image.open(f).convert("RGB").resize((320, 180), Image.LANCZOS), ((j % 2) * 324, (j // 2) * 184))
    sh.save(f"qa/sheet_{n // 4}.jpg", quality=50)
ks = sorted(glob.glob("assets/keyed/*.png")) + sorted(glob.glob("assets/lib/cut_*.png"))
print("KEYED              border_opaque%  opaque%")
cell, cols = 104, 8
sh = Image.new("RGB", (cols * cell, ((len(ks) + cols - 1) // cols) * cell), (118, 118, 118))
for j, f in enumerate(ks):
    im = Image.open(f).convert("RGBA")
    al = np.asarray(im)[:, :, 3].astype(float)
    h, w = al.shape
    b = max(4, int(min(h, w) * 0.04))
    border = np.concatenate([al[:b].ravel(), al[-b:].ravel(), al[:, :b].ravel(), al[:, -b:].ravel()])
    print(f"{os.path.basename(f):18s} {100 * (border > 128).mean():14.1f} {100 * (al > 128).mean():8.1f}")
    im.thumbnail((cell - 6, cell - 6))
    sh.paste(im, ((j % cols) * cell + 3, (j // cols) * cell + 3), im)
sh.save("qa/keyed.jpg", quality=55)
for f in sorted(glob.glob("qa/*.jpg")):
    print(f, os.path.getsize(f))
