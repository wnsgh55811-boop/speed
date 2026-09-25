# -*- coding: utf-8 -*-
"""Close dead air in the narration and keep every timing in step.

Long TTS chunks are joined with ~0.7-0.8 s of silence, which plays as the
voice (and the picture with it) "hanging" for a beat. This removes the middle
of each listed gap so only `keep` seconds of it remain.

    python3 tighten.py audio <in.mp3> <out.mp3> s:e [s:e ...]   # sandbox, ffmpeg
    python3 tighten.py timings <project_dir> s:e [s:e ...]      # local: timings.txt

Both passes take the same gap list, so audio and line timings shift together.
KEEP must match between them.
"""
import subprocess
import sys

KEEP = 0.30


def cuts(specs):
    """[(cut_start, cut_end)] — the middle of each gap, leaving KEEP."""
    out = []
    for sp in specs:
        s, e = (float(x) for x in sp.split(":"))
        drop = (e - s) - KEEP
        if drop > 0.02:
            a = s + KEEP / 2
            out.append((round(a, 3), round(a + drop, 3)))
    return sorted(out)


def shift(t, cs):
    """Map an old timestamp onto the tightened timeline."""
    d = 0.0
    for a, b in cs:
        if t >= b:
            d += b - a
        elif t > a:
            d += t - a
    return round(t - d, 3)


def audio(src, dst, cs):
    keep, prev = [], 0.0
    for a, b in cs:
        keep.append((prev, a))
        prev = b
    parts = "".join(f"[0:a]atrim={a}:{b},asetpts=PTS-STARTPTS,afade=t=in:d=0.01,"
                    f"areverse,afade=t=in:d=0.01,areverse[p{i}];" for i, (a, b) in enumerate(keep))
    parts += f"[0:a]atrim=start={prev},asetpts=PTS-STARTPTS,afade=t=in:d=0.01[p{len(keep)}];"
    parts += "".join(f"[p{i}]" for i in range(len(keep) + 1)) + f"concat=n={len(keep) + 1}:v=0:a=1[o]"
    subprocess.run(["ffmpeg", "-v", "error", "-i", src, "-filter_complex", parts, "-map", "[o]",
                    "-c:a", "libmp3lame", "-b:a", "320k", dst, "-y"], check=True)


def timings(project, cs):
    p = f"{project}/timings.txt"
    raw = open(p, encoding="utf-8").read()
    head, times = raw.split("TIMES ")
    total = float(head.split("TOTAL ")[1].split()[0])
    pairs = [tuple(float(x) for x in q.split(",")) for q in times.split()]
    new = [(shift(a, cs), shift(b, cs)) for a, b in pairs]
    head = head.replace(f"TOTAL {total:.3f}", f"TOTAL {shift(total, cs):.3f}")
    open(p, "w", encoding="utf-8").write(head + "TIMES " + " ".join(f"{a:.2f},{b:.2f}" for a, b in new) + "\n")
    c = f"{project}/cuts.txt"
    vals = [float(x) for x in open(c).read().split()]
    open(c, "w").write(" ".join(f"{shift(v, cs):.2f}" for v in vals) + "\n")
    print(f"total {total:.3f} -> {shift(total, cs):.3f}")


if __name__ == "__main__":
    mode = sys.argv[1]
    if mode == "audio":
        cs = cuts(sys.argv[4:])
        audio(sys.argv[2], sys.argv[3], cs)
    else:
        cs = cuts(sys.argv[3:])
        timings(sys.argv[2], cs)
    print("cuts", cs)
