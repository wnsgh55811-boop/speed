# -*- coding: utf-8 -*-
"""Narration chunks -> master.wav + per-line timings, inside the Higgsfield sandbox.

    python3 align.py manifest.json chunks.json        # writes out/master.wav, out/timings.txt

manifest.json: {"voice": [url_chunk0, url_chunk1, ...]}  (ElevenLabs, already brisk —
no extra 1.2x here). Chunks are joined with varied breaths, loudness-normalised to
-14 LUFS / -1 dBTP, then faster-whisper word stamps are matched back onto the script
lines by character position, so every caption lands on the syllable it belongs to.
"""
import json, os, re, subprocess, sys
from difflib import SequenceMatcher

man, chunks = json.load(open(sys.argv[1])), json.load(open(sys.argv[2]))
os.makedirs("vo", exist_ok=True); os.makedirs("out", exist_ok=True)
GAPS = [0.62, 0.74, 0.58, 0.8, 0.66]          # breaths between chunks, deliberately uneven

def sh(c):
    return subprocess.run(c, shell=True, check=True, text=True, capture_output=True).stdout

def dur(p):
    return float(sh(f'ffprobe -v error -show_entries format=duration -of csv=p=0 "{p}"'))

parts, offs, t = [], [], 0.0
for i, u in enumerate(man["voice"]):
    mp3, wav = f"vo/c{i}.mp3", f"vo/c{i}.wav"
    if not os.path.exists(mp3):
        sh(f'curl -fsSL --retry 5 -o {mp3} "{u}"')
    # trim edge silence only; internal pauses are the voice's own breathing
    sh(f'ffmpeg -hide_banner -loglevel error -i {mp3} -af "silenceremove=start_periods=1:'
       f'start_silence=0.05:start_threshold=-45dB,areverse,silenceremove=start_periods=1:'
       f'start_silence=0.05:start_threshold=-45dB,areverse" -ar 48000 -ac 1 {wav} -y')
    offs.append(t); parts.append(wav); t += dur(wav)
    if i < len(man["voice"]) - 1:
        g = GAPS[i % len(GAPS)]
        sh(f'ffmpeg -hide_banner -loglevel error -f lavfi -i anullsrc=r=48000:cl=mono -t {g} vo/g{i}.wav -y')
        parts.append(f"vo/g{i}.wav"); t += g
open("vo/list.txt", "w").write("".join(f"file '{os.path.basename(p)}'\n" for p in parts))
sh('ffmpeg -hide_banner -loglevel error -f concat -safe 0 -i vo/list.txt -c copy vo/joined.wav -y')
# two-pass loudnorm → -14 LUFS, -1 dBTP, no heavy limiting
m = json.loads(re.search(r"\{[^{}]*\"input_i\"[^{}]*\}", subprocess.run(
    'ffmpeg -hide_banner -i vo/joined.wav -af loudnorm=I=-14:TP=-1.2:LRA=11:print_format=json -f null -',
    shell=True, text=True, capture_output=True).stderr, re.S).group(0))
sh(f'ffmpeg -hide_banner -loglevel error -i vo/joined.wav -af "loudnorm=I=-14:TP=-1.2:LRA=11:'
   f'measured_I={m["input_i"]}:measured_TP={m["input_tp"]}:measured_LRA={m["input_lra"]}:'
   f'measured_thresh={m["input_thresh"]}:offset={m["target_offset"]}:linear=true" '
   f'-ar 48000 -ac 2 out/master.wav -y')

from faster_whisper import WhisperModel
model = WhisperModel(os.environ.get("WM", "small"), device="cpu", compute_type="int8", cpu_threads=8)
norm = lambda s: re.sub(r"[^0-9A-Za-z가-힣]", "", s)
starts, ends = [], []
for ci, c in enumerate(chunks):
    segs, _ = model.transcribe(f"vo/c{ci}.wav", language="ko", word_timestamps=True,
                               initial_prompt=c["tts"][:200], vad_filter=False, beam_size=1)
    chars = []                                   # (char, t0, t1) for every recognised character
    for s in segs:
        for w in s.words:
            txt = norm(w.word)
            for k, ch in enumerate(txt):
                a = w.start + (w.end - w.start) * k / max(1, len(txt))
                b = w.start + (w.end - w.start) * (k + 1) / max(1, len(txt))
                chars.append((ch, a + offs[ci], b + offs[ci]))
    hyp = "".join(x[0] for x in chars)
    ref_lines = [norm(l) for l in c["lines"]]
    ref = "".join(ref_lines)
    sm = SequenceMatcher(None, ref, hyp, autojunk=False)
    mp = {}
    for a, b, n in sm.get_matching_blocks():
        for k in range(n):
            mp[a + k] = b + k
    pos = 0
    for L in ref_lines:
        idx = [mp[p] for p in range(pos, pos + len(L)) if p in mp]
        if idx:
            starts.append(chars[idx[0]][1]); ends.append(chars[idx[-1]][2])
        else:
            starts.append(None); ends.append(None)
        pos += len(L)
# fill any unmatched lines by interpolation
n = len(starts)
for i in range(n):
    if starts[i] is None:
        j = i
        while j < n and starts[j] is None: j += 1
        lo = ends[i - 1] if i else 0.0
        hi = starts[j] if j < n else dur("out/master.wav")
        k = j - i
        for q in range(k):
            starts[i + q] = lo + (hi - lo) * q / k; ends[i + q] = lo + (hi - lo) * (q + 1) / k
total = dur("out/master.wav")
# a line holds the screen until the next one begins
cuts = [0.0] + [max(starts[i + 1] - 0.06, ends[i]) if i + 1 < n else total for i in range(n)]
cuts = [min(max(cuts[i], cuts[i - 1] + 0.3 if i else 0), total) for i in range(len(cuts))]
with open("out/timings.txt", "w") as f:
    f.write(f"TOTAL {total:.3f} N {n}\nTIMES " + " ".join(
        f"{cuts[i]:.2f},{cuts[i+1]:.2f}" for i in range(n)) + "\nSPEECH " + " ".join(
        f"{starts[i]:.2f},{ends[i]:.2f}" for i in range(n)) + "\n")
print(open("out/timings.txt").read())
print("unmatched", sum(1 for s in starts if s is None))
