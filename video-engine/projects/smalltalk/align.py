# -*- coding: utf-8 -*-
"""Align spoken.txt lines to the Fish Audio voice using ASR token timestamps.

ASR (faster-whisper small, word timestamps; asr.jsonl) is a draft only: it
supplies per-word times; the words come from the confirmed script. Boundaries are then snapped to
real pauses in the waveform (audio/sil.txt from ffmpeg silencedetect).
"""
import json, re, sys
import numpy as np
asr = [json.loads(l) for l in open(sys.argv[1], encoding="utf-8") if l.strip()]
lines = open("spoken.txt", encoding="utf-8").read().splitlines()
sil = [tuple(map(float, l.split())) for l in open("audio/sil.txt")]
DUR = float(sys.argv[2])
keep = lambda s: re.sub(r"[^0-9A-Za-z가-힣]", "", s)
# ASR char stream with times
A, AT = [], []
for seg in asr:
    for ws, we, word in seg["w"]:
        c = keep(word)
        for j, ch in enumerate(c):
            A.append(ch); AT.append(ws + (we - ws) * j / max(1, len(c)))
S, SL = [], []
for li, l in enumerate(lines):
    for ch in keep(l):
        S.append(ch); SL.append(li)
n, m = len(S), len(A)
# global alignment (match 0, mismatch 1, gap 1) with traceback
D = np.zeros((n + 1, m + 1), dtype=np.int32); D[:, 0] = np.arange(n + 1); D[0, :] = np.arange(m + 1)
Av = np.array([ord(c) for c in A])
for i in range(1, n + 1):
    sub = D[i - 1, :-1] + (Av != ord(S[i - 1]))
    row = np.minimum(sub, D[i - 1, 1:] + 1)
    # left gaps need a sequential pass
    r = np.empty(m + 1, dtype=np.int32); r[0] = i
    for j in range(1, m + 1):
        v = row[j - 1]; w = r[j - 1] + 1
        r[j] = v if v < w else w
    D[i] = r
i, j, match = n, m, [None] * n
while i > 0 and j > 0:
    if D[i, j] == D[i - 1, j - 1] + (A[j - 1] != S[i - 1]):
        match[i - 1] = j - 1; i -= 1; j -= 1
    elif D[i, j] == D[i - 1, j] + 1:
        i -= 1
    else:
        j -= 1
print("edit distance", D[n, m], "of", n, file=sys.stderr)
st = [None] * len(lines); en = [None] * len(lines)
for k, li in enumerate(SL):
    if match[k] is None: continue
    t = AT[match[k]]
    if st[li] is None: st[li] = t
    en[li] = t
for li in range(len(lines)):
    assert st[li] is not None, lines[li]
# token stamps land on the syllable's onset frame; nudge earlier a touch
st = [max(0.0, t - 0.08) for t in st]
en = [t + 0.22 for t in en]
# snap each boundary to a real pause if one sits near it
for li in range(len(lines) - 1):
    b0, b1 = en[li], st[li + 1]
    best = None
    for s, e in sil:
        if e > b0 - 0.35 and s < b1 + 0.35 and (s + e) / 2 > st[li] + 0.25 \
                and (s + e) / 2 < en[li + 1] - 0.25 and (best is None or abs((s + e) / 2 - (b0 + b1) / 2) < abs((best[0] + best[1]) / 2 - (b0 + b1) / 2)):
            best = (s, e)
    if best:
        en[li] = best[0] + 0.06; st[li + 1] = max(best[1] - 0.06, en[li])
    else:
        mid = (b0 + b1) / 2 if b1 > b0 else b1
        en[li] = mid; st[li + 1] = mid
st[0] = min(st[0], 0.30)
en[-1] = min(DUR, en[-1] + 0.3)
out = [{"i": i, "s": round(st[i], 3), "e": round(en[i], 3), "t": lines[i]} for i in range(len(lines))]
json.dump(out, open("timings.json", "w", encoding="utf-8"), ensure_ascii=False, indent=0)
for o in out: print(f'{o["i"]:3d} {o["s"]:7.2f} {o["e"]:7.2f} {o["e"]-o["s"]:5.2f}  {o["t"]}')
