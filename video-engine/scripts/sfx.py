# -*- coding: utf-8 -*-
"""Build a sparse SFX bed that is synced to the composition's own beats.

    python3 scripts/sfx.py projects/<name>      # -> <project>/audio/sfx.wav

Reads the built index.html (every timed element carries data-at/data-fx),
picks only the key motions, and synthesises quiet, muted sounds for them:
message bubble -> tiny click · line/path draw and strike -> soft swish ·
stamp / chapter marker -> low soft impact · timer -> tick per second ·
white-out -> muted whoosh. No BGM. Everything sits ~20 dB under the voice.
"""
import os
import re
import sys
import wave

import numpy as np

SR = 48000
proj = sys.argv[1]
doc = open(os.path.join(proj, "index.html"), encoding="utf-8").read()
total = float(re.search(r'id="root"[^>]*data-duration="([\d.]+)"', doc).group(1))
rng = np.random.default_rng(7)


def env(n, a, d):
    t = np.arange(n) / SR
    return np.minimum(1, t / max(a, 1e-4)) * np.exp(-t / d)


def click():
    n = int(0.05 * SR)
    t = np.arange(n) / SR
    return 0.5 * np.sin(2 * np.pi * 2300 * t) * env(n, 0.0008, 0.006) + \
        0.25 * rng.normal(0, 1, n) * env(n, 0.0005, 0.003)


def swish(dur=0.45):
    n = int(dur * SR)
    x = rng.normal(0, 1, n)
    # band-limited noise with a rising-then-falling centre: a soft air movement
    spec = np.fft.rfft(x)
    f = np.fft.rfftfreq(n, 1 / SR)
    spec *= np.exp(-((f - 1800) / 1400) ** 2)
    y = np.fft.irfft(spec, n)
    w = np.sin(np.pi * np.arange(n) / n) ** 2
    return 0.9 * y / (np.abs(y).max() + 1e-9) * w


def impact():
    n = int(0.6 * SR)
    t = np.arange(n) / SR
    f = 70 + 50 * np.exp(-t / 0.05)
    body = np.sin(2 * np.pi * np.cumsum(f) / SR) * env(n, 0.002, 0.16)
    return 0.9 * body + 0.15 * swish(0.6)[:n] * env(n, 0.001, 0.05)


def tick():
    n = int(0.04 * SR)
    t = np.arange(n) / SR
    return 0.45 * np.sin(2 * np.pi * 1500 * t) * env(n, 0.0005, 0.008)


SND = {"click": (click(), -30), "swish": (swish(), -33), "impact": (impact(), -24),
       "tick": (tick(), -31), "whoosh": (swish(0.9), -29)}

ev = []
for m in re.finditer(r'<(\w+) class="([^"]*)"[^>]*?data-at="([\d.]+)" data-fx="(\w+)"', doc):
    tag, cls, at, fx = m.group(1), m.group(2), float(m.group(3)), m.group(4)
    if fx == "msg":
        ev.append((at + 0.02, "click"))
    elif fx == "draw" and ("sline" in cls or "tedge" in cls):
        ev.append((at, "swish"))
    elif fx == "strike":
        ev.append((at, "swish"))
    elif fx == "stamp":
        ev.append((at + 0.3, "impact"))
    elif fx == "pop" and "pearl" in cls:
        ev.append((at + 0.05, "impact"))
    elif fx == "flash":
        ev.append((at - 0.1, "whoosh"))
for m in re.finditer(r'data-secs="([\d.]+)" id="[^"]+" data-at="([\d.]+)" data-fx="timer"', doc):
    secs, at = float(m.group(1)), float(m.group(2))
    ev += [(at + k, "tick") for k in range(int(secs) + 1)]

# one sound per 120 ms at most, so stacked beats never pile up
ev.sort()
kept, last = [], -1
for t, k in ev:
    if t - last >= 0.12:
        kept.append((t, k))
        last = t

out = np.zeros(int((total + 1) * SR))
for t, k in kept:
    s, db = SND[k]
    i = int(t * SR)
    seg = s[: max(0, len(out) - i)] * 10 ** (db / 20)
    out[i:i + len(seg)] += seg
out = out[: int(total * SR)]
os.makedirs(os.path.join(proj, "audio"), exist_ok=True)
with wave.open(os.path.join(proj, "audio", "sfx.wav"), "wb") as w:
    w.setnchannels(1)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes((np.clip(out, -1, 1) * 32767).astype(np.int16).tobytes())
from collections import Counter  # noqa: E402
print(len(kept), "sfx events", dict(Counter(k for _, k in kept)))
