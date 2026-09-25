# -*- coding: utf-8 -*-
"""Narration + motion SFX → assets/audio/master.wav, mastered once.

    python3 scripts/mix_sfx.py examples/<project>

Cues come from <project>/sfx.json (written by emit_v2.py at the exact times
the motions fire). The sounds are synthesised here — soft and short, sitting
well under the voice — so there is no library to license or fetch:
  click (message in) · tick (graph peak / check) · whoosh (move) ·
  draw (line draw) · type (search typing) · low (chapter) · impact (claim)
Mastering: two-pass loudnorm to -14.5 LUFS integrated, -1.5 dBTP.
"""
import json
import os
import re
import subprocess
import sys

import numpy as np

SR = 48000
PROJ = os.path.abspath(sys.argv[1])
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
rng = np.random.default_rng(7)


def env(n, a=0.004, r=None):
    t = np.arange(n) / SR
    e = np.minimum(1.0, t / a)
    return e * (np.exp(-t / r) if r else 1.0)


def bandnoise(n, lo, hi):
    x = rng.normal(0, 1, n)
    X = np.fft.rfft(x)
    f = np.fft.rfftfreq(n, 1 / SR)
    X[(f < lo) | (f > hi)] = 0
    y = np.fft.irfft(X, n)
    return y / (np.abs(y).max() + 1e-9)


def db(v):
    return 10 ** (v / 20)


def s_click():
    n = int(0.05 * SR)
    t = np.arange(n) / SR
    return (np.sin(2 * np.pi * 2300 * t) * 0.6 + bandnoise(n, 2000, 7000) * 0.4) * env(n, 0.001, 0.008) * db(-22)


def s_tick():
    n = int(0.04 * SR)
    t = np.arange(n) / SR
    return np.sin(2 * np.pi * 1760 * t) * env(n, 0.001, 0.01) * db(-24)


def s_whoosh():
    n = int(0.5 * SR)
    x = bandnoise(n, 300, 3500)
    t = np.linspace(0, 1, n)
    return x * np.sin(np.pi * t) ** 2 * db(-27)


def s_draw():
    n = int(0.8 * SR)
    x = bandnoise(n, 1500, 6000)
    t = np.linspace(0, 1, n)
    return x * (np.sin(np.pi * t) ** 1.5) * db(-33)


def s_type():
    out = np.zeros(int(1.6 * SR))
    for k in range(20):
        at = int((k * 0.075 + rng.uniform(0, 0.02)) * SR)
        c = s_click() * db(-4)
        out[at:at + len(c)] += c[:len(out) - at]
    return out


def s_low():
    n = int(0.9 * SR)
    t = np.arange(n) / SR
    body = np.sin(2 * np.pi * 62 * t) * env(n, 0.006, 0.28)
    air = bandnoise(n, 200, 1200) * env(n, 0.002, 0.05) * 0.25
    return (body + air) * db(-17)


def s_impact():
    n = int(1.2 * SR)
    t = np.arange(n) / SR
    body = (np.sin(2 * np.pi * 52 * t) + 0.45 * np.sin(2 * np.pi * 104 * t)) * env(n, 0.004, 0.35)
    hit = bandnoise(n, 150, 2500) * env(n, 0.001, 0.03) * 0.5
    return (body + hit) * db(-16)


SOUNDS = {"click": s_click, "tick": s_tick, "whoosh": s_whoosh, "draw": s_draw,
          "type": s_type, "low": s_low, "impact": s_impact}


def read(path):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-f", "f32le", "-ac", "1",
                          "-ar", str(SR), "-"], capture_output=True, check=True).stdout
    return np.frombuffer(raw, dtype=np.float32).astype(np.float64)


def main():
    vo_path = os.path.join(PROJ, "vo", "vo_paused.wav")
    voice = read(vo_path)
    total = float(open(os.path.join(PROJ, "timings.txt")).read().split("TOTAL ")[1].split()[0])
    total = max(total, float(re.search(r'data-duration="([\d.]+)"', open(os.path.join(ROOT, "index.html")).read()).group(1)))
    mix = np.zeros(int(total * SR) + SR)
    mix[:len(voice)] += voice
    cues = json.load(open(os.path.join(PROJ, "sfx.json")))
    cache = {}
    for q in cues:
        s = cache.setdefault(q["k"], SOUNDS[q["k"]]())
        at = int(q["t"] * SR)
        seg = s * q.get("g", 1.0)
        end = min(len(mix), at + len(seg))
        mix[at:end] += seg[:end - at]
    os.makedirs(os.path.join(ROOT, "assets", "audio"), exist_ok=True)
    tmp = os.path.join(PROJ, "vo", "premaster.wav")
    stereo = np.repeat(mix[:, None], 2, axis=1).astype(np.float32)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", "-",
                    tmp], input=stereo.tobytes(), check=True)
    # two-pass loudnorm: measure, then apply linearly
    m = subprocess.run(["ffmpeg", "-hide_banner", "-i", tmp, "-af",
                        "loudnorm=I=-14.5:TP=-1.5:LRA=11:print_format=json", "-f", "null", "-"],
                       capture_output=True, text=True).stderr
    j = json.loads(m[m.rindex("{"):m.rindex("}") + 1])
    af = (f"loudnorm=I=-14.5:TP=-1.5:LRA=11:measured_I={j['input_i']}:measured_TP={j['input_tp']}:"
          f"measured_LRA={j['input_lra']}:measured_thresh={j['input_thresh']}:offset={j['target_offset']}:"
          "linear=true")
    out = os.path.join(ROOT, "assets", "audio", "master.wav")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", tmp, "-af", af, "-ar", str(SR), out], check=True)
    r = subprocess.run(["ffmpeg", "-hide_banner", "-i", out, "-af", "ebur128=peak=true", "-f", "null", "-"],
                       capture_output=True, text=True).stderr
    summ = r[r.rindex("Summary:"):]
    I = re.search(r"I:\s+(-?[\d.]+) LUFS", summ).group(1)
    tp = re.search(r"Peak:\s+(-?[\d.]+) dBFS", summ).group(1)
    print(f"[mix] {len(cues)} sfx · master {total:.1f}s · I={I} LUFS · TP={tp} dBFS")


if __name__ == "__main__":
    main()
