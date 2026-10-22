# -*- coding: utf-8 -*-
"""Narration master: the user's WAV untouched in time and pitch, plus a few
quiet SFX on visual beats, normalised to about -14.5 LUFS / -1 dBTP.

    python3 scripts/master_audio.py assets/audio/narration.wav renders/sfx.json renders/master_audio.wav
"""
import json
import subprocess
import sys

import numpy as np

SR = 48000
src, cues, out = sys.argv[1:4]


def sh(cmd):
    return subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)


raw = subprocess.run(["ffmpeg", "-v", "error", "-i", src, "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"],
                     capture_output=True, check=True).stdout
voice = np.frombuffer(raw, np.float32).copy()
n = len(voice)
rng = np.random.default_rng(7)


def env(dur, att=0.002, dec=None):
    t = np.arange(int(dur * SR)) / SR
    e = np.minimum(t / att, 1.0)
    return t, e * np.exp(-t / (dec or dur / 4))


def click():
    t, e = env(0.05, 0.001, 0.008)
    return (np.sin(2 * np.pi * 2300 * t) * 0.6 + rng.normal(0, .25, len(t))) * e


def tick():
    t, e = env(0.08, 0.002, 0.018)
    return np.sin(2 * np.pi * 1650 * t) * e


def draw():
    t, e = env(0.9, 0.25, 0.5)
    sweep = np.sin(2 * np.pi * (500 * t + 500 * t * t))
    return (rng.normal(0, .5, len(t)) * 0.4 + sweep * 0.25) * e * np.hanning(len(t))


def soft():
    t, e = env(0.6, 0.004, 0.16)
    return (np.sin(2 * np.pi * 110 * t) + 0.3 * np.sin(2 * np.pi * 220 * t)) * e


def impact():
    t, e = env(1.1, 0.003, 0.32)
    f = 62 * np.exp(-t * 1.4) + 40
    return (np.sin(2 * np.pi * np.cumsum(f) / SR) + rng.normal(0, .06, len(t))) * e


def whoosh():
    t = np.arange(int(0.55 * SR)) / SR
    noise = np.convolve(rng.normal(0, 1, len(t)), np.ones(24) / 24, "same")
    return noise * np.hanning(len(t)) * 1.6


def snap():
    t, e = env(0.12, 0.001, 0.02)
    return (rng.normal(0, .6, len(t)) + np.sin(2 * np.pi * 900 * t)) * e


# gains in dBFS peak — well under the voice (voice peaks ≈ -1.7 dBFS)
SFX = {"click": (click, -30), "tick": (tick, -32), "draw": (draw, -34), "soft": (soft, -30),
       "impact": (impact, -24), "whoosh": (whoosh, -30), "snap": (snap, -30)}
bed = np.zeros(n, np.float32)
last = -9
for t0, kind in json.load(open(cues)):
    if t0 - last < 0.22:
        continue
    last = t0
    fn, db = SFX[kind]
    s = fn().astype(np.float32)
    s *= 10 ** (db / 20) / (np.abs(s).max() + 1e-9)
    i = int(t0 * SR)
    j = min(n, i + len(s))
    if i < n:
        bed[i:j] += s[:j - i]

mix = voice + bed
tmp = out.replace(".wav", "_premix.wav")
st = np.stack([mix, mix], 1).astype(np.float32)
open(tmp + ".raw", "wb").write(st.tobytes())
sh(f'ffmpeg -v error -y -f f32le -ar {SR} -ac 2 -i "{tmp}.raw" -c:a pcm_f32le "{tmp}"')

# two-pass loudnorm, linear (gain + true-peak guard only, no dynamic squash)
r = sh(f'ffmpeg -hide_banner -i "{tmp}" -af loudnorm=I=-14.5:TP=-1.2:LRA=11:print_format=json -f null -')
js = json.loads(r.stderr[r.stderr.rindex("{"):])
af = (f"loudnorm=I=-14.5:TP=-1.2:LRA=11:linear=true:measured_I={js['input_i']}:"
      f"measured_TP={js['input_tp']}:measured_LRA={js['input_lra']}:measured_thresh={js['input_thresh']}:"
      f"offset={js['target_offset']},aresample={SR}")
sh(f'ffmpeg -v error -y -i "{tmp}" -af "{af}" -c:a pcm_s24le -ar {SR} "{out}"')
r = sh(f'ffmpeg -hide_banner -nostats -i "{out}" -af ebur128=peak=true -f null -')
tail = r.stderr[r.stderr.rindex("Summary"):]
print(" ".join(tail.split()))
d = float(sh(f'ffprobe -v error -show_entries format=duration -of csv=p=0 "{out}"').stdout)
print(f"duration {d:.3f}s (source {n / SR:.3f}s)")
