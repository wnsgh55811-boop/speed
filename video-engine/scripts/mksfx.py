# -*- coding: utf-8 -*-
"""sfx.json [(t, kind)] -> sfx.wav: a tiny UI click per chat bubble, a muted
whoosh on chapter / key-type cards. Synthesised, so there is nothing to
license and the level can sit well under the voice.

    python3 mksfx.py sfx.json total_seconds out.wav
"""
import json, math, random, struct, sys, wave

ev, total, out = json.load(open(sys.argv[1])), float(sys.argv[2]), sys.argv[3]
SR = 48000
buf = [0.0] * (int(total * SR) + SR)


def click(at):
    n = int(0.045 * SR)
    for i in range(n):
        t = i / SR
        env = math.exp(-t * 140)
        buf[at + i] += 0.30 * env * (math.sin(2 * math.pi * 2300 * t) + 0.4 * math.sin(2 * math.pi * 3400 * t))


def whoosh(at):
    rnd = random.Random(at)
    n = int(0.55 * SR)
    lp = 0.0
    for i in range(n):
        x = i / n
        env = math.sin(math.pi * x) ** 2
        a = 0.02 + 0.10 * x          # cutoff sweeps up: a soft rising air
        lp += a * (rnd.uniform(-1, 1) - lp)
        buf[at + i] += 0.55 * env * lp


for t, kind in ev:
    at = int(t * SR)
    if at < 0 or at >= len(buf) - SR:
        continue
    (click if kind == "click" else whoosh)(at)
w = wave.open(out, "wb")
w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
w.writeframes(b"".join(struct.pack("<h", max(-32767, min(32767, int(v * 32767)))) for v in buf))
w.close()
print("sfx events", len(ev))
