"""Turn the script into timed subtitle chunks.
usage: python3 -I align_lines.py <script.txt> <words.json> <audio> <chunks.json>

script.txt conventions
  - one subtitle per line (blank lines ignored). The user's line breaks ARE the subtitle breaks.
  - '**text**' or '**text' (no closing line ahead) -> that line is emphasised;
    '**first line' ... 'last line**' -> every line of the block is emphasised.
  - #CH|<n>|<title>      -> the next line starts chapter n (used by the 16:9 template header/cards).
Text shown is the script text (trailing '.' removed); whisper words only give the timing.
Starts are snapped to real speech onsets from the waveform."""
import json, re, sys, wave, difflib, subprocess, tempfile
import numpy as np

sp, wp, audio, outp = sys.argv[1:5]
raw = [l.strip() for l in open(sp, encoding="utf-8").read().split("\n") if l.strip()]
L, ch, bold = [], None, False
for k, l in enumerate(raw):
    if l.startswith("#CH|"):
        _, n, t = l.split("|", 2); ch = {"n": int(n), "t": t}; continue
    if l.startswith("**"):
        # '**a**' or '**a' with no closing line ahead = this line only; '**a' ... 'b**' = block
        closes = l.endswith("**") and len(l) > 2
        for m in raw[k + 1:]:
            if closes or m.startswith("**") or m.startswith("#CH|"): break
            if m.endswith("**"): closes = "block"; break
        bold = closes == "block"
        L.append({"t": l.replace("**", ""), "b": True, "ch": ch}); ch = None
        continue
    L.append({"t": l.replace("**", ""), "b": bold, "ch": ch}); ch = None
    if l.endswith("**"): bold = False

words = json.load(open(wp))
ok = lambda c: re.match(r"[가-힣0-9A-Za-z]", c)
wc, wt = [], []
for s, e, t in words:
    cs = [c for c in t if ok(c)]
    for k, c in enumerate(cs):
        wc.append(c); wt.append((s + (e - s) * k / len(cs), s + (e - s) * (k + 1) / len(cs)))
sc, owner = [], []
for li, l in enumerate(L):
    for c in l["t"]:
        if ok(c): sc.append(c); owner.append(li)
m = {}
for a, b, n in difflib.SequenceMatcher(None, sc, wc, autojunk=False).get_matching_blocks():
    for k in range(n): m[a + k] = b + k
span = {}
for i, li in enumerate(owner):
    if i in m:
        s, e = wt[m[i]]; span.setdefault(li, [s, e]); span[li][1] = e
missing = [i for i in range(len(L)) if i not in span]
for i in missing:  # not heard in the audio -> squeeze between neighbours (report it!)
    p = max([j for j in span if j < i], default=None); n = min([j for j in span if j > i], default=None)
    s = span[p][1] if p is not None else 0; span[i] = [s, span[n][0] if n is not None else s + 1]
if missing: print("WARNING lines not found in audio:", [L[i]["t"] for i in missing])

tmp = tempfile.mktemp(suffix=".wav")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", audio, "-ac", "1", "-ar", "16000", "-c:a", "pcm_s16le", tmp], check=True)
w = wave.open(tmp); sr = w.getframerate()
a = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
hop = sr // 100
rms = np.sqrt(np.convolve(a ** 2, np.ones(hop * 2) / (hop * 2), "same")[::hop])
db = 20 * np.log10(rms + 1e-9)
v = db > np.percentile(db, 90) - 30
i = 0
while i < len(v):  # close dips shorter than 120ms
    if not v[i]:
        j = i
        while j < len(v) and not v[j]: j += 1
        if j - i < 12 and i > 0: v[i:j] = True
        i = j
    else: i += 1
onsets = [k / 100 for k in range(1, len(v)) if v[k] and not v[k - 1]]

chunks = []
for li, l in enumerate(L):
    s, e = span[li]
    k0 = int(round((s + 0.05) * 100))
    if k0 < len(v) and not v[k0]:
        nxt = [o for o in onsets if s - 0.05 <= o <= s + 0.5]
        if nxt: s = nxt[0]
    else:
        near = [o for o in onsets if abs(o - s) <= 0.15]
        if near: s = min(near, key=lambda o: abs(o - s))
    chunks.append({"s": round(max(s - 0.03, 0), 3), "e": round(e, 3), "t": re.sub(r"\.$", "", l["t"]), "b": l["b"], "ch": l["ch"]})
DUR = round(len(a) / sr, 3)
for c, n in zip(chunks, chunks[1:]):  # hold through short pauses (no flicker)
    c["e"] = n["s"] if n["s"] - c["e"] < 0.6 else round(c["e"] + 0.2, 3)
chunks[0]["s"] = 0.0; chunks[-1]["e"] = DUR
json.dump({"dur": DUR, "chunks": chunks}, open(outp, "w"), ensure_ascii=False)
print(len(chunks), "chunks, dur", DUR)
for c in chunks:
    if c["ch"]: s = int(c["s"]); print(f'{s // 60}:{s % 60:02d} {c["ch"]["t"]}')
