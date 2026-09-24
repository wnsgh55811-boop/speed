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
SR = 48000
N = int((vdur + 1) * SR)
bed = [0.0] * N
rnd = random.Random(7)
def tone(kind):
    out = []
    if kind == "click":
        n = int(.03 * SR); lp = 0
        for i in range(n):
            x = rnd.uniform(-1, 1); lp = lp * .55 + x * .45
            out.append((x - lp) * math.exp(-i / (.006 * SR)) * .5)
    elif kind in ("whoosh", "whoosh_s"):
        L = .55 if kind == "whoosh" else .32; n = int(L * SR); lp = 0
        for i in range(n):
            p = i / n; a = math.sin(math.pi * p) ** 2
            k = .04 + .25 * p
            lp = lp + k * (rnd.uniform(-1, 1) - lp)
            out.append(lp * a * 1.6)
    elif kind == "tick":
        n = int(.06 * SR)
        for i in range(n):
            out.append(math.sin(2 * math.pi * 1650 * i / SR) * math.exp(-i / (.012 * SR)) * .35)
    elif kind == "draw":
        n = int(.7 * SR); lp = 0
        for i in range(n):
            p = i / n; lp = lp + .08 * (rnd.uniform(-1, 1) - lp)
            out.append(lp * math.sin(math.pi * p) * .9)
    elif kind == "impact":
        n = int(.45 * SR)
        for i in range(n):
            f = 62 + 40 * math.exp(-i / (.05 * SR))
            out.append(math.sin(2 * math.pi * f * i / SR) * math.exp(-i / (.14 * SR)) * .9)
    return out
GAIN = {"click": .16, "whoosh": .14, "whoosh_s": .10, "tick": .10, "draw": .08, "impact": .30}
cache = {}
for t, kind in json.load(open("../sfx.json")):
    if kind not in cache: cache[kind] = tone(kind)
    s0 = int(t * SR); g = GAIN.get(kind, .1)
    for i, v in enumerate(cache[kind]):
        j = s0 + i
        if 0 <= j < N: bed[j] += v * g
with wave.open("sfx.wav", "w") as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes(b"".join(struct.pack("<h", int(max(-1, min(1, v)) * 32767)) for v in bed))

# ── mix + loudness ─────────────────────────────────────────────────────────
sh('ffmpeg -v error -i vo.wav -i sfx.wav -filter_complex "[1:a]aformat=channel_layouts=stereo,'
   'volume=0.9[s];[0:a][s]amix=inputs=2:duration=first:normalize=0[m]" -map "[m]" -ar 48000 mix.wav -y')
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
sh(f"ffmpeg -v error -i video.mp4 -c:v libx264 -preset slow -b:v {vbr}k -pass 1 -an -f mp4 /dev/null -y")
sh(f"ffmpeg -v error -i video.mp4 -i final.wav -map 0:v -map 1:a -c:v libx264 -preset slow -b:v {vbr}k "
   f"-maxrate {int(vbr*1.8)}k -bufsize {vbr*3}k -pass 2 -pix_fmt yuv420p -profile:v high -c:a aac -b:a {abr}k "
   f"-shortest -movflags +faststart LIGHT.mp4 -y")
for f in ("MASTER.mp4", "LIGHT.mp4"):
    print(f, os.path.getsize(f) / 1e6, "MB", sh(f"ffprobe -v error -show_entries stream=codec_name,width,height "
          f"-show_entries format=duration -of compact=p=0 {f}").replace("\n", " | "))
print(sh(f'curl -f -X PUT -H "Content-Type: video/mp4" --upload-file MASTER.mp4 "{mp}" -o /dev/null -w "UP MASTER %{{http_code}}"'))
print(sh(f'curl -f -X PUT -H "Content-Type: video/mp4" --upload-file LIGHT.mp4 "{lp}" -o /dev/null -w "UP LIGHT %{{http_code}}"'))
print("ASSEMBLE DONE")
