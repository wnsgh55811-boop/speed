# -*- coding: utf-8 -*-
"""Numbers from real rendered frames, one row per second of a slice:
mean luma of the centre, share of crushed pixels, bright p90 (is the hero
element there?) and change vs 0.5 s earlier (is anything moving?).
    python3 segqa.py slice.mp4 offset_seconds
"""
import subprocess, sys
mp4, off = sys.argv[1], float(sys.argv[2])
W, H = 320, 180
raw = subprocess.run(["ffmpeg", "-v", "error", "-i", mp4, "-vf", f"fps=2,scale={W}:{H}",
                      "-f", "rawvideo", "-pix_fmt", "gray", "-"], capture_output=True).stdout
n = len(raw) // (W * H)
prev = None
for k in range(n):
    fr = raw[k * W * H:(k + 1) * W * H]
    c = [fr[y * W + x] for y in range(int(H * .12), int(H * .78)) for x in range(int(W * .2), int(W * .8))]
    c.sort()
    mean = sum(c) / len(c)
    crushed = sum(1 for v in c if v < 18) / len(c)
    p90 = c[int(len(c) * .9)]
    diff = 0 if prev is None else sum(abs(a - b) for a, b in zip(fr[::7], prev[::7])) / len(fr[::7])
    prev = fr
    if k % 2 == 0:
        print(f"{off + k / 2:6.1f} L{mean:3.0f} c{crushed:.2f} p{p90:3d} d{diff:4.1f}")
