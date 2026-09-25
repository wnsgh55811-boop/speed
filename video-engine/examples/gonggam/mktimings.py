# -*- coding: utf-8 -*-
"""Estimate line timings when there is no narration track yet.

Fitted on "공백의 태도" (251 lines against its 1.2x master):
    seconds ≈ 0.356 + 0.1244 × syllables
Lines that only lead into a quote get a hair of extra room; every line keeps
at least 0.8s so short captions are still readable.

    python3 mktimings.py   → timings.txt
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from plan import LINES, PLAN  # noqa: E402

A, B, FLOOR, GAP = 0.356, 0.1244, 0.8, 0.12

t, spans = 0.4, []
for line, (kind, _) in zip(LINES, PLAN):
    syl = len(re.findall(r"[가-힣0-9A-Za-z]", line))
    d = max(FLOOR, A + B * syl)
    if kind == "H":
        d += 0.5          # a header wants a beat to land
    spans.append((t, t + d))
    t += d + GAP
total = t + 0.8
with open(os.path.join(HERE, "timings.txt"), "w", encoding="utf-8") as f:
    f.write(f"TOTAL {total:.3f} N {len(spans)}\n")
    f.write("TIMES " + " ".join(f"{a:.2f},{b:.2f}" for a, b in spans) + "\n")
print(f"{len(spans)} lines · {total/60:.1f} min")
