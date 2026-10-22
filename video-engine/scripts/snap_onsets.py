# -*- coding: utf-8 -*-
"""Snap each sentence start in timeline.json to the real audio onset.

Whisper's word clock drifts up to ~0.35 s late on some sentences. For every
sentence we look for the first frame above the speech threshold between the
previous sentence's end and a little past the Whisper start, and shift that
sentence's whole char clock by the same amount.

    python3 scripts/snap_onsets.py <wav> examples/<proj>/timeline.json
"""
import json
import subprocess
import sys

import numpy as np

wav, path = sys.argv[1:3]
raw = subprocess.run(["ffmpeg", "-v", "error", "-i", wav, "-ac", "1", "-ar", "16000", "-f", "f32le", "-"],
                     capture_output=True, check=True).stdout
a = np.frombuffer(raw, np.float32)
rms = np.sqrt(np.convolve(a * a, np.ones(320) / 320, "same"))[::160]          # 10 ms frames
db = 20 * np.log10(rms + 1e-9)
thr = np.percentile(db, 20) + 18
tl = json.load(open(path, encoding="utf-8"))
L = tl["lines"]
moved = []
for k, ln in enumerate(L):
    lo = max(L[k - 1]["e"] + 0.03 if k else 0.0, ln["s"] - 0.6)
    hi = ln["s"] + 0.15
    seg = db[int(lo * 100):int(hi * 100)]
    if not len(seg) or seg.max() < thr:
        continue
    on = int(lo * 100) + int(np.argmax(seg > thr))
    d = on / 100 - ln["s"]
    if abs(d) < 0.02:
        continue
    ln["s"] += d
    ln["ct"] = [round(max(t + d, ln["s"]), 3) for t in ln["ct"]]
    moved.append(d)
for ln in L:
    ln["text"] = ln["text"].replace("땡땡", "OO")
json.dump(tl, open(path, "w", encoding="utf-8"), ensure_ascii=False)
m = np.array(moved)
print(f"snapped {len(m)}/{len(L)} sentences; shift mean {m.mean():+.3f}s, min {m.min():+.3f}s, max {m.max():+.3f}s")
