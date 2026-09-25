# -*- coding: utf-8 -*-
"""Placeholder timings.txt from syllable counts, for layout previews only.

The real file comes from aligning the rendered narration (align.py). Rates
are for the ElevenLabs read after the single 1.2x tempo pass.
"""
import json, re
SYL, DOT, COMMA = 8.0, 0.42, 0.16
lines = json.load(open("lines.json", encoding="utf-8"))
t, out = 0.25, []
for l in lines:
    n = len(re.sub(r"[^가-힣0-9A-Za-z]", "", l))
    d = n / SYL + 0.18
    out.append((t, t + d))
    t += d + (DOT if re.search(r"(다|죠|요|\?|\.|\")$", l) else COMMA)
total = t + 2.6
open("timings.txt", "w").write(f"TOTAL {total:.3f} N {len(lines)}\nTIMES " +
                               " ".join(f"{a:.2f},{b:.2f}" for a, b in out) + "\n")
print(f"estimated total {total:.1f}s")
