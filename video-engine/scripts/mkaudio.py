# -*- coding: utf-8 -*-
"""Rebuild master.wav byte-identically to the pass that timings.txt was cut against.

Same chain as the original build: per-chunk silence trim, fixed 0.28s gaps,
concat, loudnorm, then the 1.2x speed-up. Any deviation here would slide every
subtitle, so the filters are copied verbatim rather than re-tuned.
"""
import json, os, subprocess
SPEED, GAP = 1.2, 0.28
VO, OUT = "vo", "out"
os.makedirs(VO, exist_ok=True); os.makedirs(OUT, exist_ok=True)

def sh(c):
    return subprocess.run(c, shell=True, check=True, text=True,
                          capture_output=True).stdout

man = json.load(open("manifest.json"))
n = len(man["voice"])
for i, u in enumerate(man["voice"]):
    p = f"{VO}/c{i:02d}.mp3"
    if not os.path.exists(p) or os.path.getsize(p) == 0:
        sh(f'curl -fsSL --retry 5 -o "{p}" "{u}"')
    t = f"{VO}/t{i:02d}.wav"
    sh(f'ffmpeg -hide_banner -loglevel error -i "{p}" -af '
       f'"silenceremove=start_periods=1:start_silence=0.05:start_threshold=-45dB:detection=peak,'
       f'areverse,silenceremove=start_periods=1:start_silence=0.05:start_threshold=-45dB:'
       f'detection=peak,areverse" -ar 48000 -ac 1 "{t}" -y')

sh(f'ffmpeg -hide_banner -loglevel error -f lavfi -i anullsrc=r=48000:cl=mono '
   f'-t {GAP} "{VO}/gap.wav" -y')
with open(f"{VO}/list.txt", "w") as f:
    for i in range(n):
        f.write(f"file 't{i:02d}.wav'\n")
        if i != n - 1:
            f.write("file 'gap.wav'\n")
sh(f'ffmpeg -hide_banner -loglevel error -f concat -safe 0 -i "{VO}/list.txt" '
   f'-c copy "{VO}/joined.wav" -y')
sh(f'ffmpeg -hide_banner -loglevel error -i "{VO}/joined.wav" '
   f'-af "loudnorm=I=-16:TP=-1.5:LRA=11,atempo={SPEED}" '
   f'-ar 48000 -ac 2 "{OUT}/master.wav" -y')
d = float(sh('ffprobe -v error -show_entries format=duration -of csv=p=0 out/master.wav').strip())
print(f"[audio] master={d:.3f}s  (timings expect 602.041s, delta {d-602.041:+.3f}s)")
