# -*- coding: utf-8 -*-
"""Forced alignment: master.wav + script.txt -> timings.txt

The subtitles need a start and end for each of the 668 script lines. Splitting
on detected silence was the other option and it is guesswork — the narration is
one continuous read, so the boundaries are found by transcribing the rendered
audio with word timestamps and aligning that transcript against the script.

A by-product is a check on the narration itself: the per-line match ratio says
where what was spoken drifts from what was written, which is exactly where a
block needs regenerating.
"""
import difflib, io, json, re, sys

from faster_whisper import WhisperModel

AUDIO = "out/master.wav"
lines = [l.strip() for l in io.open("script.txt", encoding="utf-8") if l.strip()]


def norm(s):
    """Compare on bare Hangul and digits; spacing and punctuation are noise."""
    return re.sub(r"[^가-힣ㄱ-ㆎ0-9a-zA-Z]", "", s)


print("[align] transcribing…", flush=True)
model = WhisperModel("medium", device="cpu", compute_type="int8")
segs, _ = model.transcribe(AUDIO, language="ko", word_timestamps=True,
                           vad_filter=False, beam_size=5)

# one character stream out of the transcript, each character carrying a time
chars, times = [], []
for seg in segs:
    for w in (seg.words or []):
        t = norm(w.word)
        if not t:
            continue
        span = max(1e-3, w.end - w.start)
        for k, ch in enumerate(t):
            chars.append(ch)
            times.append((w.start + span * k / len(t),
                          w.start + span * (k + 1) / len(t)))
hyp = "".join(chars)
print(f"[align] transcript {len(hyp)} chars, audio ends {times[-1][1]:.2f}s",
      flush=True)

# the same stream out of the script, remembering which line each char came from
ref, owner = [], []
for i, l in enumerate(lines):
    for ch in norm(l):
        ref.append(ch)
        owner.append(i)
ref = "".join(ref)
print(f"[align] script {len(ref)} chars over {len(lines)} lines", flush=True)

# map script char -> transcript char through the longest matching blocks
hit = [None] * len(ref)
for a, b, size in difflib.SequenceMatcher(None, ref, hyp,
                                          autojunk=False).get_matching_blocks():
    for k in range(size):
        hit[a + k] = b + k

starts, ends, matched = [None] * len(lines), [None] * len(lines), [0] * len(lines)
for a, li in enumerate(owner):
    if hit[a] is None:
        continue
    t0, t1 = times[hit[a]]
    if starts[li] is None:
        starts[li] = t0
    ends[li] = t1
    matched[li] += 1

# a line the transcript never matched borrows its slot from its neighbours,
# split by character count so a caption never lands on nothing
total = times[-1][1]
for i in range(len(lines)):
    if starts[i] is None:
        lo = next((ends[j] for j in range(i - 1, -1, -1) if ends[j]), 0.0)
        hi = next((starts[j] for j in range(i + 1, len(lines)) if starts[j]), total)
        run = [j for j in range(i, len(lines)) if starts[j] is None]
        run = [j for j in run if all(starts[k] is None for k in range(i, j + 1))]
        w = sum(max(1, len(norm(lines[j]))) for j in run) or 1
        acc = lo
        for j in run:
            share = (hi - lo) * max(1, len(norm(lines[j]))) / w
            starts[j], ends[j] = acc, acc + share
            acc += share

# monotonic, no overlaps, nothing shorter than a readable caption
for i in range(len(lines)):
    if i and starts[i] < ends[i - 1]:
        starts[i] = ends[i - 1]
    if ends[i] <= starts[i] + 0.25:
        ends[i] = starts[i] + 0.25
    if i and ends[i - 1] > starts[i]:
        ends[i - 1] = starts[i]
ends[-1] = max(ends[-1], total)

io.open("timings.txt", "w", encoding="utf-8").write(
    f"TOTAL {total:.3f} N {len(lines)}\nTIMES " +
    " ".join(f"{s:.2f},{e:.2f}" for s, e in zip(starts, ends)) + "\n")

# where the read drifts from the script
weak = [(i, matched[i], len(norm(lines[i])), lines[i]) for i in range(len(lines))
        if len(norm(lines[i])) >= 4 and matched[i] < 0.6 * len(norm(lines[i]))]
print(f"[align] wrote timings.txt · total {total:.2f}s")
print(f"[align] lines poorly matched: {len(weak)} / {len(lines)}")
for i, m, n, l in weak[:40]:
    print(f"   {i:3d} {m}/{n}  {l}")
json.dump({"weak": [w[0] for w in weak], "total": total},
          io.open("align_report.json", "w"))
