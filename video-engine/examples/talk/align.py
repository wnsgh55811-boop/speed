# -*- coding: utf-8 -*-
"""Forced alignment: the six narration blocks + script.txt -> timings.txt

The subtitles need a start and end for each of the 668 script lines. Splitting
on detected silence was the other option and it is guesswork — the narration is
one continuous read per block, so the boundaries are found by transcribing with
word timestamps and aligning that transcript against the script.

The blocks are transcribed in parallel rather than the finished master in one
pass: same work, a fraction of the wall clock, and it keeps the whole job
inside one sandbox lease. Each block's word times are then mapped onto the
master, which is the blocks joined with the gaps and then sped up by 1.2.

A by-product is a check on the narration itself: the per-line match ratio says
where what was spoken drifts from what was written, which is exactly where a
block needs regenerating.
"""
import difflib, io, json, os, re, subprocess, sys
from concurrent.futures import ProcessPoolExecutor

SPEED = 1.2
lines = [l.strip() for l in io.open("script.txt", encoding="utf-8") if l.strip()]
chunks = json.load(io.open("chunks.json", encoding="utf-8"))
gaps = json.load(io.open("manifest.json"))["gaps"]
NB = len(chunks)


def norm(s):
    """Compare on bare Hangul and digits; spacing and punctuation are noise."""
    return re.sub(r"[^가-힣ㄱ-ㆎ0-9a-zA-Z]", "", s)


def dur(p):
    return float(subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "csv=p=0", p], capture_output=True, text=True).stdout.strip())


def transcribe(i):
    from faster_whisper import WhisperModel
    m = WhisperModel("small", device="cpu", compute_type="int8", cpu_threads=2)
    segs, _ = m.transcribe(f"vo/t{i}.wav", language="ko", word_timestamps=True,
                           vad_filter=False, beam_size=1)
    return i, [(w.word, w.start, w.end) for s in segs for w in (s.words or [])]


if __name__ == "__main__":
    # where each block begins on the finished master
    blocks = [f"vo/t{i}.wav" for i in range(NB)]
    ds = [dur(b) for b in blocks]
    off, acc = [], 0.0
    for i in range(NB):
        off.append(acc)
        acc += ds[i] + (gaps[i] if i < NB - 1 else 0.0)
    total = acc / SPEED
    print(f"[align] {NB} blocks, joined {acc:.2f}s -> master {total:.2f}s",
          flush=True)

    print("[align] transcribing blocks in parallel…", flush=True)
    with ProcessPoolExecutor(max_workers=min(NB, os.cpu_count() or 2)) as ex:
        out = dict(ex.map(transcribe, range(NB)))

    # one character stream out of the transcript, each character carrying a
    # time already mapped onto the master
    chars, times = [], []
    for i in range(NB):
        for word, ws, we in out[i]:
            t = norm(word)
            if not t:
                continue
            a, b = (off[i] + ws) / SPEED, (off[i] + we) / SPEED
            span = max(1e-3, b - a)
            for k, ch in enumerate(t):
                chars.append(ch)
                times.append((a + span * k / len(t), a + span * (k + 1) / len(t)))
    hyp = "".join(chars)
    if not hyp:
        sys.exit("transcript empty")
    print(f"[align] transcript {len(hyp)} chars, last word {times[-1][1]:.2f}s",
          flush=True)

    # the same stream out of the script, remembering which line each char is in
    ref, owner = [], []
    for i, l in enumerate(lines):
        for ch in norm(l):
            ref.append(ch)
            owner.append(i)
    ref = "".join(ref)
    print(f"[align] script {len(ref)} chars over {len(lines)} lines", flush=True)

    hit = [None] * len(ref)
    for a, b, size in difflib.SequenceMatcher(
            None, ref, hyp, autojunk=False).get_matching_blocks():
        for k in range(size):
            hit[a + k] = b + k

    starts = [None] * len(lines)
    ends = [None] * len(lines)
    matched = [0] * len(lines)
    for a, li in enumerate(owner):
        if hit[a] is None:
            continue
        t0, t1 = times[hit[a]]
        if starts[li] is None:
            starts[li] = t0
        ends[li] = t1
        matched[li] += 1

    # a line the transcript never matched borrows its slot from its neighbours,
    # split by character count, so no caption lands on nothing
    i = 0
    while i < len(lines):
        if starts[i] is not None:
            i += 1
            continue
        j = i
        while j < len(lines) and starts[j] is None:
            j += 1
        lo = next((ends[k] for k in range(i - 1, -1, -1) if ends[k] is not None), 0.0)
        hi = starts[j] if j < len(lines) else total
        run = list(range(i, j))
        w = sum(max(1, len(norm(lines[k]))) for k in run)
        acc2 = lo
        for k in run:
            share = (hi - lo) * max(1, len(norm(lines[k]))) / w
            starts[k], ends[k] = acc2, acc2 + share
            acc2 += share
        i = j

    # monotonic, no overlaps, nothing shorter than a readable caption
    for i in range(len(lines)):
        if i and starts[i] < ends[i - 1]:
            starts[i] = ends[i - 1]
        if ends[i] <= starts[i] + 0.25:
            ends[i] = starts[i] + 0.25
        if i and ends[i - 1] > starts[i]:
            ends[i - 1] = starts[i]
    ends[-1] = max(ends[-1], min(total, ends[-1] + 0.4))

    io.open("timings.txt", "w", encoding="utf-8").write(
        f"TOTAL {total:.3f} N {len(lines)}\nTIMES " +
        " ".join(f"{s:.2f},{e:.2f}" for s, e in zip(starts, ends)) + "\n")

    weak = [(i, matched[i], len(norm(lines[i])))
            for i in range(len(lines))
            if len(norm(lines[i])) >= 5 and matched[i] < 0.55 * len(norm(lines[i]))]
    print(f"[align] wrote timings.txt · total {total:.2f}s")
    print(f"[align] poorly matched lines: {len(weak)} / {len(lines)}")
    for i, m, n in weak[:50]:
        print(f"   {i:3d}  {m}/{n}  {lines[i]}")
    json.dump({"weak": [w[0] for w in weak], "total": total},
              io.open("align_report.json", "w"))
