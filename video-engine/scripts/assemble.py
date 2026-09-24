# -*- coding: utf-8 -*-
"""Final assembly inside the Higgsfield sandbox.

    python3 assemble.py <vo_url> <seg_url>... --master-put URL --light-put URL

1. concat the rendered segments (stream copy — they share one encoder profile)
2. synthesize the few SFX the composer asked for (sfx.json: [t, kind]) — soft
   clicks, a muted whoosh, ticks, a low impact; nothing cartoonish, all ≥20 dB
   under the voice
3. voice + sfx → two-pass loudnorm to -14 LUFS / ≤ -1 dBTP
4. MASTER: video copy + AAC 320k.  LIGHT: two-pass x264 sized for ~100 MB,
   faststart so it plays straight from the link
"""
import json, math, os, subprocess, sys, wave, struct, random, re

def sh(c, cap=True):
    r = subprocess.run(c, shell=True, text=True, capture_output=cap)
    if r.returncode: print(r.stderr[-2000:]); raise SystemExit(c[:120])
    return (r.stdout or "") + (r.stderr or "")

args = sys.argv[1:]
mp = args[args.index("--master-put") + 1]; lp = args[args.index("--light-put") + 1]
pos = [a for a in args if not a.startswith("--") and a not in (mp, lp)]
vo, segs = pos[0], pos[1:]
os.makedirs("A", exist_ok=True); os.chdir("A")
for i, u in enumerate(segs):
    if not os.path.exists(f"s{i}.mp4"): sh(f'curl -fsSL --retry 5 -o s{i}.mp4 "{u}"')
open("l.txt", "w").write("".join(f"file 's{i}.mp4'\n" for i in range(len(segs))))
sh("ffmpeg -v error -f concat -safe 0 -i l.txt -c copy -an video.mp4 -y")
vdur = float(sh("ffprobe -v error -show_entries format=duration -of csv=p=0 video.mp4").strip())
if not os.path.exists("vo.mp3"): sh(f'curl -fsSL --retry 5 -o vo.mp3 "{vo}"')
sh("ffmpeg -v error -i vo.mp3 -ar 48000 -ac 2 vo.wav -y")
adur = float(sh("ffprobe -v error -show_entries format=duration -of csv=p=0 vo.wav").strip())
print(f"video {vdur:.3f}s  voice {adur:.3f}s")

# ── SFX bed ────────────────────────────────────────────────────────────────
import numpy as np
SR = 48000
N = int((vdur + 1) * SR)
bed = np.zeros(N, dtype=np.float32)
rng = np.random.default_rng(7)
def lowpass(x, k):
    y = np.empty_like(x); acc = 0.0
    for i in range(len(x)):
        acc += k * (x[i] - acc); y[i] = acc
    return y
def tone(kind):
    if kind == "click":
        n = int(.03 * SR); x = rng.uniform(-1, 1, n)
        return (x - lowpass(x, .45)) * np.exp(-np.arange(n) / (.006 * SR)) * .5
    if kind in ("whoosh", "whoosh_s"):
        n = int((.55 if kind == "whoosh" else .32) * SR); p = np.arange(n) / n
        return lowpass(rng.uniform(-1, 1, n), .12) * np.sin(np.pi * p) ** 2 * 1.6
    if kind == "tick":
        n = int(.06 * SR); t = np.arange(n)
        return np.sin(2 * np.pi * 1650 * t / SR) * np.exp(-t / (.012 * SR)) * .35
    if kind == "draw":
        n = int(.7 * SR); p = np.arange(n) / n
        return lowpass(rng.uniform(-1, 1, n), .08) * np.sin(np.pi * p) * .9
    if kind == "impact":
        n = int(.45 * SR); t = np.arange(n)
        f = 62 + 40 * np.exp(-t / (.05 * SR))
        return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / (.14 * SR)) * .9
    return np.zeros(1)
GAIN = {"click": .16, "whoosh": .14, "whoosh_s": .10, "tick": .10, "draw": .08, "impact": .30}
cache = {}
for t, kind in json.load(open("../sfx.json")):
    if kind not in cache: cache[kind] = tone(kind).astype(np.float32)
    s0 = int(t * SR); v = cache[kind] * GAIN.get(kind, .1)
    e = min(N, s0 + len(v))
    if s0 < N: bed[s0:e] += v[:e - s0]
with wave.open("sfx.wav", "w") as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((np.clip(bed, -1, 1) * 32767).astype("<i2").tobytes())

# ── mix + loudness ─────────────────────────────────────────────────────────
sh('ffmpeg -v error -i vo.wav -i sfx.wav -filter_complex "[1:a]aformat=channel_layouts=stereo,'
   'volume=0.9[s];[0:a][s]amix=inputs=2:duration=first,volume=2[m]" -map "[m]" -ar 48000 mix.wav -y')
m = json.loads(re.search(r"\{[^{}]*\"input_i\"[^{}]*\}", sh(
    "ffmpeg -hide_banner -i mix.wav -af loudnorm=I=-14:TP=-1.3:LRA=11:print_format=json -f null -"), re.S).group(0))
sh(f'ffmpeg -v error -i mix.wav -af "loudnorm=I=-14:TP=-1.3:LRA=11:measured_I={m["input_i"]}:'
   f'measured_TP={m["input_tp"]}:measured_LRA={m["input_lra"]}:measured_thresh={m["input_thresh"]}:'
   f'offset={m["target_offset"]}:linear=true" -ar 48000 final.wav -y')
chk = sh("ffmpeg -hide_banner -i final.wav -af loudnorm=I=-14:TP=-1.3:print_format=json -f null -")
mm = json.loads(re.search(r"\{[^{}]*\"input_i\"[^{}]*\}", chk, re.S).group(0))
print("LOUDNESS", mm["input_i"], "LUFS  TP", mm["input_tp"], "dBTP")

# ── deliverables ───────────────────────────────────────────────────────────
sh("ffmpeg -v error -i video.mp4 -i final.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 320k "
   "-shortest -movflags +faststart MASTER.mp4 -y")
target_mb = 98
abr = 128
vbr = int(target_mb * 8 * 1024 / vdur - abr)
# single pass, capped: motion graphics sit far under the cap, so quality holds
sh(f"ffmpeg -v error -i video.mp4 -i final.wav -map 0:v -map 1:a -c:v libx264 -preset faster -crf 21 "
   f"-maxrate {vbr}k -bufsize {vbr*2}k -pix_fmt yuv420p -profile:v high -c:a aac -b:a {abr}k "
   f"-shortest -movflags +faststart LIGHT.mp4 -y")
for f in ("MASTER.mp4", "LIGHT.mp4"):
    print(f, os.path.getsize(f) / 1e6, "MB", sh(f"ffprobe -v error -show_entries stream=codec_name,width,height "
          f"-show_entries format=duration -of compact=p=0 {f}").replace("\n", " | "))
for f, u in (("MASTER.mp4", mp), ("LIGHT.mp4", lp)):   # an upload miss must not kill the other
    r = subprocess.run(f'curl -s -X PUT -H "Content-Type: video/mp4" --upload-file {f} "{u}" -o /dev/null '
                       f'-w "%{{http_code}}"', shell=True, text=True, capture_output=True)
    print("UP", f, r.stdout, flush=True)
print("ASSEMBLE DONE")
