# -*- coding: utf-8 -*-
"""Chunk MP3s -> assets/audio/master.wav (one continuous narration).

    python3 mkmaster.py manifest.json out.wav

manifest: {"voice": [url, ...], "gaps": [sec, ...], "speed": 1.2}
Each pass is silence-trimmed, joined with the listed breaths (deliberately not
all equal), loudness-normalised to about -14.5 LUFS / -1.5 dBTP, then sped up.
If the TTS already rendered at 1.2x, set speed to 1.0 — never apply it twice.
"""
import json, os, subprocess, sys

man, out = json.load(open(sys.argv[1])), sys.argv[2]
os.makedirs("vo", exist_ok=True)
sh = lambda c: subprocess.run(c, shell=True, check=True, text=True, capture_output=True).stdout
for i, u in enumerate(man["voice"]):
    p = f"vo/c{i:02d}.mp3"
    if not os.path.exists(p) or os.path.getsize(p) == 0:
        sh(f'curl -fsSL --retry 5 -o "{p}" "{u}"')
    sh(f'ffmpeg -hide_banner -loglevel error -i "{p}" -af '
       f'"silenceremove=start_periods=1:start_silence=0.05:start_threshold=-45dB:detection=peak,'
       f'areverse,silenceremove=start_periods=1:start_silence=0.05:start_threshold=-45dB:'
       f'detection=peak,areverse" -ar 48000 -ac 1 "vo/t{i:02d}.wav" -y')
with open("vo/list.txt", "w") as f:
    for i in range(len(man["voice"])):
        f.write(f"file 't{i:02d}.wav'\n")
        if i < len(man["voice"]) - 1:
            g = man["gaps"][i]
            sh(f'ffmpeg -hide_banner -loglevel error -f lavfi -i anullsrc=r=48000:cl=mono -t {g} "vo/g{i:02d}.wav" -y')
            f.write(f"file 'g{i:02d}.wav'\n")
sh('ffmpeg -hide_banner -loglevel error -f concat -safe 0 -i vo/list.txt -c copy vo/joined.wav -y')
sp = man.get("speed", 1.0)
tempo = f",atempo={sp}" if sp != 1.0 else ""
sh(f'ffmpeg -hide_banner -loglevel error -i vo/joined.wav -af "loudnorm=I=-14.5:TP=-1.5:LRA=11{tempo}" '
   f'-ar 48000 -ac 2 "{out}" -y')
print(sh(f'ffprobe -v error -show_entries format=duration -of csv=p=0 "{out}"').strip())
