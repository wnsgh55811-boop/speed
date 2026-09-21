# -*- coding: utf-8 -*-
"""script.txt -> chunks.json

Six blocks of roughly three minutes each. Short per-line clips were the wrong
call: every fragment comes back read in isolation, so timbre and breath jump at
each splice. A block this long keeps one continuous read, and the per-line
subtitle timings come from forced alignment against the rendered audio instead
of from the clip boundaries.
"""
import io, json

NCHUNK = 6
CLOSERS = ("습니다", "합니다", "입니다", "니다", "겠죠", "거죠", "구요", "어요", "아요",
           "예요", "에요", "죠", "요", "다", "봅시다", "세요", "까요")

lines = [l.strip() for l in io.open("script.txt", encoding="utf-8") if l.strip()]
cum, n = [], 0
for l in lines:
    n += len(l)
    cum.append(n)
total = n
target = total / NCHUNK


def closes(i):
    """A block may only end where the narration itself finishes a thought."""
    l = lines[i]
    if l.startswith('"') or l.endswith(('보다', '아니라', '전에', '안에서', '있는')):
        return False
    nxt = lines[i + 1] if i + 1 < len(lines) else ""
    if nxt.startswith(('"', '라고', '라는', '를 ', '하고', '이렇게', '로 넘어')):
        return False
    return l.endswith(CLOSERS)


cuts = []
for k in range(1, NCHUNK):
    want = target * k
    # nearest thought-closing line to the ideal split point
    best = min((i for i in range(len(lines) - 1) if closes(i)),
               key=lambda i: abs(cum[i] - want))
    cuts.append(best + 1)
bounds = [0] + cuts + [len(lines)]

# gap between blocks: a real beat, and not all the same length
GAPS = [0.72, 0.60, 0.78, 0.62, 0.70]
out = []
for k in range(NCHUNK):
    ls = lines[bounds[k]:bounds[k + 1]]
    out.append({"i": k, "start_line": bounds[k], "lines": ls,
                "text": "\n".join(ls),
                "gap_after": GAPS[k] if k < len(GAPS) else 0.0})

json.dump(out, io.open("chunks.json", "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
print(f"chunks {len(out)}  lines {sum(len(c['lines']) for c in out)}  chars {total}")
for c in out:
    print(f"  #{c['i']}: lines {len(c['lines']):3d}  chars {len(c['text']):5d}"
          f"  ~{len(c['text'])/9.49:5.1f}s@1.2x   ends: {c['lines'][-1][:26]}")
