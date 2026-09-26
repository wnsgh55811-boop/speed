# -*- coding: utf-8 -*-
"""Cut per-line timings out of the finished master with faster-whisper.

    python3 align.py chunks.json master.wav timings.txt [model]

Whisper gives word times; the script gives the exact words. Both are reduced
to bare hangul/alnum characters and matched with difflib, so each caption line
gets the time of its first and last matched character. Lines whisper hears
differently (ㅋㅋ read as 크크, quotes) fall back to interpolation between
their matched neighbours. Boundaries are made continuous: a line runs until
the next one starts, so the picture never drops to an empty frame.
"""
import difflib
import json
import re
import sys

from faster_whisper import WhisperModel

chunks, wav, out = sys.argv[1:4]
size = sys.argv[4] if len(sys.argv) > 4 else "small"
lines = [l for c in json.load(open(chunks, encoding="utf-8")) for l in c["lines"]]


def norm(s):
    s = re.sub(r"ㅋ+", lambda m: "크" * min(3, len(m.group())), s).replace("ㅎㅎ", "")
    return re.sub(r"[^0-9A-Za-z가-힣]", "", s)


m = WhisperModel(size, device="cpu", compute_type="int8")
segs, info = m.transcribe(wav, language="ko", word_timestamps=True, beam_size=5,
                          vad_filter=False, condition_on_previous_text=True,
                          initial_prompt=" ".join(lines[:12]))
tchars, ttimes = [], []
for s in segs:
    for w in s.words:
        t = norm(w.word)
        for k, ch in enumerate(t):
            tchars.append(ch)
            ttimes.append(w.start + (w.end - w.start) * (k / max(1, len(t))))
    print(f"{s.end:7.2f} {s.text}", flush=True)
total = info.duration

schars, sline = [], []
for i, l in enumerate(lines):
    for ch in norm(l):
        schars.append(ch)
        sline.append(i)

sm = difflib.SequenceMatcher(None, schars, tchars, autojunk=False)
first, last = [None] * len(lines), [None] * len(lines)
for a, b, n in sm.get_matching_blocks():
    for k in range(n):
        i = sline[a + k]
        t = ttimes[b + k]
        if first[i] is None:
            first[i] = t
        last[i] = t

# interpolate unmatched starts
known = [i for i in range(len(lines)) if first[i] is not None]
starts = []
for i in range(len(lines)):
    if first[i] is not None:
        starts.append(first[i])
        continue
    prv = max([k for k in known if k < i], default=None)
    nxt = min([k for k in known if k > i], default=None)
    a = first[prv] if prv is not None else 0.0
    b = first[nxt] if nxt is not None else total
    lo, hi = (prv if prv is not None else -1), (nxt if nxt is not None else len(lines))
    starts.append(a + (b - a) * (i - lo) / (hi - lo))
starts[0] = 0.0
# keep monotonic, lead each line by 60ms so the card lands with the voice
for i in range(1, len(starts)):
    starts[i] = max(starts[i - 1] + 0.25, starts[i] - 0.06)
ends = starts[1:] + [total]
miss = [i for i in range(len(lines)) if first[i] is None]
print("unmatched lines:", miss, flush=True)
with open(out, "w") as f:
    f.write(f"TOTAL {total:.3f} N {len(lines)}\n")
    f.write("TIMES " + " ".join(f"{a:.2f},{b:.2f}" for a, b in zip(starts, ends)) + "\n")
print("ratio matched", round(sm.ratio(), 3), "total", round(total, 2))
