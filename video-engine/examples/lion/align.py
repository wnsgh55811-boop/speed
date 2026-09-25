# -*- coding: utf-8 -*-
"""Cut timings.txt against the real narration, and place the key pauses.

    python3 examples/lion/align.py

1. faster-whisper word timestamps on vo/vo.wav
2. character alignment (Hangul/digits only) between the script and the
   transcript, so misheard words still land: each line takes the time of its
   first and last matched characters, gaps are interpolated
3. PAUSES: extra silence spliced in before chosen lines (chapter turns and
   key claims), each a different length so the read never ticks evenly
Writes vo/vo_paused.wav and timings.txt (TOTAL + TIMES per line).
"""
import difflib
import json
import os
import re
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
VO = os.path.join(HERE, "vo")
LINES = json.load(open(os.path.join(HERE, "lines.json"), encoding="utf-8"))

# line index → extra seconds of silence BEFORE it
PAUSES = {26: 0.45, 29: 0.55, 41: 0.5, 48: 0.6, 50: 0.8, 79: 0.85, 119: 0.8,
          131: 0.4, 153: 0.6, 159: 0.7, 161: 0.35, 172: 0.45, 193: 0.65,
          195: 0.5, 207: 0.75, 209: 0.9}


def norm(s):
    return re.sub(r"[^가-힣0-9]", "", s)


def transcribe(path):
    from faster_whisper import WhisperModel
    m = WhisperModel("small", device="cpu", compute_type="int8")
    segs, _ = m.transcribe(path, language="ko", word_timestamps=True, vad_filter=False,
                           initial_prompt=" ".join(LINES[:12]))
    chars = []                       # (char, t)
    for s in segs:
        for w in s.words:
            cs = norm(w.word)
            for k, ch in enumerate(cs):
                chars.append((ch, w.start + (w.end - w.start) * (k + 0.5) / max(1, len(cs))))
    return chars


def main():
    chars = transcribe(os.path.join(VO, "vo.wav"))
    heard = "".join(c for c, _ in chars)
    script, owner = "", []
    for i, l in enumerate(LINES):
        n = norm(l)
        script += n
        owner += [i] * len(n)
    sm = difflib.SequenceMatcher(None, script, heard, autojunk=False)
    at = [None] * len(script)
    for a, b, size in sm.get_matching_blocks():
        for k in range(size):
            at[a + k] = chars[b + k][1]
    # interpolate unmatched characters
    known = [k for k, v in enumerate(at) if v is not None]
    for k in range(len(at)):
        if at[k] is None:
            lo = max([q for q in known if q < k], default=None)
            hi = min([q for q in known if q > k], default=None)
            if lo is None:
                at[k] = at[hi]
            elif hi is None:
                at[k] = at[lo]
            else:
                at[k] = at[lo] + (at[hi] - at[lo]) * (k - lo) / (hi - lo)
    print(f"[align] matched {len(known)}/{len(script)} chars")
    splice(spans_from(at, owner))


def spans_from(at, owner):
    spans = []
    for i in range(len(LINES)):
        ks = [k for k, o in enumerate(owner) if o == i]
        spans.append([at[ks[0]] - 0.12, at[ks[-1]] + 0.18])
    for i in range(1, len(spans)):               # keep monotonic, no overlap
        spans[i][0] = max(spans[i][0], spans[i - 1][0] + 0.25)
        spans[i - 1][1] = min(spans[i - 1][1], spans[i][0])
    return spans


def splice(spans):
    # splice pauses: cut at the midpoint of the silence before each chosen line
    dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                "-of", "csv=p=0", os.path.join(VO, "vo.wav")],
                               capture_output=True, text=True).stdout)
    cuts = sorted((max(0.0, (spans[i - 1][1] + spans[i][0]) / 2), p) for i, p in PAUSES.items() if i > 0)
    filt, prev = [], 0.0
    segs = ["[0]asplit=" + str(len(cuts) + 1) + "".join(f"[s{j}]" for j in range(len(cuts) + 1)) + ";"]
    for j, (c, p) in enumerate(cuts):
        segs.append(f"[s{j}]atrim={prev:.3f}:{c:.3f},asetpts=PTS-STARTPTS[a{j}];"
                    f"aevalsrc=0:d={p}:s=48000[z{j}];")
        filt += [f"[a{j}]", f"[z{j}]"]
        prev = c
    segs.append(f"[s{len(cuts)}]atrim={prev:.3f},asetpts=PTS-STARTPTS[a{len(cuts)}];")
    filt.append(f"[a{len(cuts)}]")
    graph = "".join(segs) + "".join(filt) + f"concat=n={len(filt)}:v=0:a=1[out]"
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", os.path.join(VO, "vo.wav"),
                    "-filter_complex", graph, "-map", "[out]", "-ar", "48000", "-ac", "1",
                    os.path.join(VO, "vo_paused.wav")], check=True)
    shift = lambda x: x + sum(p for c, p in cuts if c <= x)   # noqa: E731
    spans = [(max(0.0, shift(a)), shift(b)) for a, b in spans]
    total = shift(dur) + 0.2
    open(os.path.join(HERE, "timings.txt"), "w").write(
        f"TOTAL {total:.3f} N {len(LINES)}\nTIMES " + " ".join(f"{a:.2f},{b:.2f}" for a, b in spans) + "\n")
    print(f"[align] narration {dur:.2f}s → {total:.2f}s with {len(cuts)} pauses")


if __name__ == "__main__":
    main()
