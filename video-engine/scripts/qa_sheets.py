# -*- coding: utf-8 -*-
"""Frame QA for a scene-build project: snapshot real rendered frames and tile
them into labelled contact sheets you can actually look at.

    python3 scripts/qa_sheets.py projects/<name> mid            # one frame per scene
    python3 scripts/qa_sheets.py projects/<name> sme 12 40 61   # start/mid/end of scenes 12, 40, 61
    python3 scripts/qa_sheets.py projects/<name> at 1.5 30 60   # exact seconds

Frames come from `hyperframes snapshot` on the render parts (short, so each
capture loads fast), and sheets land in <project>/snapshots/sheet_*.jpg.
"""
import glob
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys

from PIL import Image, ImageDraw

proj, mode, args = sys.argv[1], sys.argv[2], sys.argv[3:]
spec = importlib.util.spec_from_file_location("plan", os.path.join(proj, "plan.py"))
plan = importlib.util.module_from_spec(spec)
spec.loader.exec_module(plan)
tl = json.load(open(os.path.join(proj, "timings.json"), encoding="utf-8"))
man = json.load(open(os.path.join(proj, "parts", "manifest.json")))
S = plan.SCENES
st = [0.0] + [round((tl[s["a"]]["s"] - 0.06) * 30) / 30 for s in S[1:]] + [plan.TOTAL]

want = []                                   # (global seconds, label)
if mode == "mid":
    want = [((st[k] + st[k + 1]) / 2, f"s{k} {S[k]['kind']}") for k in range(len(S))]
elif mode == "sme":
    for k in map(int, args):
        a, b = st[k], st[k + 1]
        want += [(a + 0.25, f"s{k} start"), ((a + b) / 2, f"s{k} mid"), (b - 0.2, f"s{k} end")]
else:
    want = [(float(x), f"{float(x):.1f}s") for x in args]

out = os.path.join(proj, "snapshots")
os.makedirs(out, exist_ok=True)
for f in glob.glob(os.path.join(out, "*")):          # stale frames from an earlier pass
    if os.path.isdir(f) and os.path.basename(f).startswith("p"):
        shutil.rmtree(f)
    elif os.path.isfile(f):
        os.remove(f)
shots = []
for m in man:
    sel = sorted((t, lab) for t, lab in want if m["t0"] <= t < m["t1"])
    if not sel:
        continue
    d = os.path.join(out, m["file"])
    ats = ",".join(f"{t - m['t0']:.2f}" for t, _ in sel)
    subprocess.run(["npx", "hyperframes", "snapshot", os.path.join(proj, "parts", m["file"]), "--at", ats,
                    "--no-end", "-o", d, "--no-browser-gpu", "--timeout", "120000", "--describe", "false"],
                   cwd=os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."),
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    fs = sorted(glob.glob(os.path.join(d, "*.png")),
                key=lambda f: float(re.search(r"([\d.]+)s?\.png$", f).group(1)) if re.search(r"([\d.]+)s?\.png$", f) else 0)
    for f, (t, lab) in zip(fs, sel):
        shots.append((f, f"{lab} @{t:.1f}s"))

W, H, per = 640, 360, 9
for n in range(0, len(shots), per):
    sub = shots[n:n + per]
    sheet = Image.new("RGB", (3 * W, ((len(sub) + 2) // 3) * H), (0, 0, 0))
    for i, (f, lab) in enumerate(sub):
        im = Image.open(f).convert("RGB").resize((W, H))
        dr = ImageDraw.Draw(im)
        dr.rectangle((0, 0, 260, 22), fill=(0, 0, 0))
        dr.text((6, 5), lab, fill=(255, 90, 90))
        sheet.paste(im, ((i % 3) * W, (i // 3) * H))
    sheet.save(os.path.join(out, f"sheet_{n // per:02d}.jpg"), quality=78)
print(len(shots), "frames ->", out)
