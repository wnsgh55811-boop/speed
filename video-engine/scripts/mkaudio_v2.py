# -*- coding: utf-8 -*-
"""Join the long TTS takes into one narration track.

    python3 scripts/mkaudio_v2.py examples/<project>

Reads <project>/vo/c0.mp3, c1.mp3, ... (one ~1100-1300 char take each, so
the voice keeps one continuous read) and writes <project>/vo/vo.wav.

· edge silence trimmed per take, then a 0.5 s breath between takes
· SPEED from plan.py (default 1.2) is applied ONCE here with atempo. If the
  takes were already generated fast, set SPEED = 1.0 in the plan — never
  both, or the read ends up at 1.44x.
· no loudness pass here: mix_sfx.py normalises the final mix once
"""
import os
import subprocess
import sys

PROJ = os.path.abspath(sys.argv[1])
sys.path.insert(0, PROJ)
import plan  # noqa: E402

SPEED = getattr(plan, "SPEED", 1.2)
GAP = 0.5
VO = os.path.join(PROJ, "vo")


def sh(c):
    return subprocess.run(c, shell=True, check=True, text=True, capture_output=True).stdout


takes = sorted(f for f in os.listdir(VO) if f.startswith("c") and f.endswith(".mp3"))
assert takes, "no takes in vo/"
parts = []
for f in takes:
    src, dst = os.path.join(VO, f), os.path.join(VO, f[:-4] + ".wav")
    sh(f'ffmpeg -hide_banner -loglevel error -y -i "{src}" -af '
       '"silenceremove=start_periods=1:start_silence=0.05:start_threshold=-45dB:detection=peak,'
       'areverse,silenceremove=start_periods=1:start_silence=0.05:start_threshold=-45dB:detection=peak,'
       f'areverse" -ar 48000 -ac 1 "{dst}"')
    parts.append(dst)
sh(f'ffmpeg -hide_banner -loglevel error -y -f lavfi -i anullsrc=r=48000:cl=mono -t {GAP} "{VO}/gap.wav"')
with open(f"{VO}/list.txt", "w") as fh:
    for j, p in enumerate(parts):
        fh.write(f"file '{os.path.basename(p)}'\n")
        if j < len(parts) - 1:
            fh.write("file 'gap.wav'\n")
sh(f'ffmpeg -hide_banner -loglevel error -y -f concat -safe 0 -i "{VO}/list.txt" -c copy "{VO}/joined.wav"')
tempo = f"atempo={SPEED}" if abs(SPEED - 1.0) > 1e-3 else "anull"
sh(f'ffmpeg -hide_banner -loglevel error -y -i "{VO}/joined.wav" -af "{tempo}" -ar 48000 -ac 1 "{VO}/vo.wav"')
d = float(sh(f'ffprobe -v error -show_entries format=duration -of csv=p=0 "{VO}/vo.wav"'))
print(f"[audio] {len(parts)} takes → vo.wav {d:.2f}s (tempo {SPEED})")
