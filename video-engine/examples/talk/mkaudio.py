# -*- coding: utf-8 -*-
"""Build master.wav from the six narration blocks.

Long blocks, not per-line clips: every splice is a place where timbre and
breath can jump, so the narration is generated in six ~3-minute reads and
joined at six places instead of six hundred.

Chain: per-block silence trim -> concat with the block's own gap -> loudnorm
-> 1.2x. The speed-up happens here and only here; the blocks are generated at
the voice's natural rate.
"""
import json, os, subprocess, sys

SPEED = 1.2
VO, OUT = "vo", "out"
os.makedirs(VO, exist_ok=True)
os.makedirs(OUT, exist_ok=True)


def sh(c):
    r = subprocess.run(c, shell=True, text=True, capture_output=True)
    if r.returncode:
        sys.exit(f"FAILED: {c}\n{r.stderr[-2000:]}")
    return r.stdout


man = json.load(open("manifest.json"))
urls, gaps = man["voice"], man["gaps"]
n = len(urls)

for i, u in enumerate(urls):
    p = f"{VO}/b{i}.mp3"
    if not os.path.exists(p) or os.path.getsize(p) == 0:
        sh(f'curl -fsSL --retry 5 -o "{p}" "{u}"')
    # trim the dead air the model leaves at each end, nothing else
    sh(f'ffmpeg -hide_banner -loglevel error -i "{p}" -af '
       f'"silenceremove=start_periods=1:start_silence=0.05:start_threshold=-45dB:'
       f'detection=peak,areverse,silenceremove=start_periods=1:start_silence=0.05:'
       f'start_threshold=-45dB:detection=peak,areverse" '
       f'-ar 48000 -ac 1 "{VO}/t{i}.wav" -y')

# a real beat between blocks, and deliberately not all the same length
for i, g in enumerate(gaps[:n - 1]):
    sh(f'ffmpeg -hide_banner -loglevel error -f lavfi -i anullsrc=r=48000:cl=mono '
       f'-t {g} "{VO}/g{i}.wav" -y')

with open(f"{VO}/list.txt", "w") as f:
    for i in range(n):
        f.write(f"file 't{i}.wav'\n")
        if i != n - 1:
            f.write(f"file 'g{i}.wav'\n")

sh(f'ffmpeg -hide_banner -loglevel error -f concat -safe 0 -i "{VO}/list.txt" '
   f'-c copy "{VO}/joined.wav" -y')
sh(f'ffmpeg -hide_banner -loglevel error -i "{VO}/joined.wav" '
   f'-af "loudnorm=I=-15:TP=-1.5:LRA=11,atempo={SPEED}" '
   f'-ar 48000 -ac 2 "{OUT}/master.wav" -y')

# The composition loads this in every render worker, and a 14-minute 48k
# stereo wav is 160MB — enough to time out page load eight times over. A
# 192kbps mp3 is a tenth of a percent of the difference to a listener and
# a twelfth of the bytes.
sh(f'ffmpeg -hide_banner -loglevel error -i "{OUT}/master.wav" '
   f'-c:a libmp3lame -b:a 192k -ar 48000 -ac 2 "{OUT}/master.mp3" -y')

d = float(sh('ffprobe -v error -show_entries format=duration -of csv=p=0 '
             'out/master.wav').strip())
sz = os.path.getsize(f"{OUT}/master.mp3") / 1e6
print(f"[audio] master={d:.3f}s  ({d/60:.1f} min)  blocks={n}  mp3={sz:.1f}MB")

# the delivery targets, measured rather than assumed
m = subprocess.run(
    f'ffmpeg -hide_banner -nostats -i "{OUT}/master.mp3" '
    f'-af ebur128=peak=true -f null -', shell=True, text=True,
    capture_output=True).stderr
tail = m[m.rfind("Integrated loudness"):] if "Integrated loudness" in m else ""
for line in tail.splitlines():
    if any(k in line for k in ("I:", "LRA:", "Peak:")):
        print("[audio]  " + line.strip())
