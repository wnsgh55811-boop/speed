"""Whisper 단어 타임스탬프 + 무음 구간으로 대본 조각을 음성에 맞춘다.
출력: timeline.json (조각별 시작/끝, 슬라이드 전환 시각), 대조 리포트."""
import json, re, sys, difflib
sys.path.insert(0, sys.argv[1])
from chunks import SLIDES

W = sys.argv[1]
segs = json.load(open(f"{W}/tr.json", encoding="utf-8"))
AUDIO_END = float(sys.argv[2])
norm = lambda s: re.sub(r"[^0-9A-Za-z가-힣]", "", s)

# 전사 문자열 (문자 -> 단어 index)
words = [w for s in segs for w in s["words"]]
tchars, tword = [], []
for wi, w in enumerate(words):
    for ch in norm(w["w"]):
        tchars.append(ch); tword.append(wi)
T = "".join(tchars)

# 대본 문자열 (문자 -> 조각 index)
chunks = [(si, ci, c) for si, ch in enumerate(SLIDES) for ci, c in enumerate(ch)]
schars, schunk = [], []
for k, (_, _, c) in enumerate(chunks):
    for ch in norm(c):
        schars.append(ch); schunk.append(k)
Sx = "".join(schars)

sm = difflib.SequenceMatcher(None, Sx, T, autojunk=False)
s2t = [None] * len(Sx)
report = []
for op, a0, a1, b0, b1 in sm.get_opcodes():
    if op == "equal":
        for d in range(a1 - a0): s2t[a0 + d] = b0 + d
    else:
        ctx_t = (words[tword[b0]]["s"] if b0 < len(T) else AUDIO_END)
        report.append((op, Sx[a0:a1], T[b0:b1], round(ctx_t, 2),
                       chunks[schunk[a0]][:2] if a0 < len(Sx) else None))

# 조각별 첫/끝 단어
res = []
for k, (si, ci, c) in enumerate(chunks):
    idx = [i for i, kk in enumerate(schunk) if kk == k and s2t[i] is not None]
    if not idx:
        res.append(None); continue
    w0 = tword[s2t[idx[0]]]; w1 = tword[s2t[idx[-1]]]
    res.append({"slide": si + 1, "ci": ci, "text": c, "w0": w0, "w1": w1,
                "s": words[w0]["s"], "e": words[w1]["e"],
                "cover": len(idx) / len(norm(c))})

# 무음 구간
sil = []
cur = None
for line in open(f"{W}/sil2.txt"):
    m = re.search(r"silence_start: ([\d.]+)", line)
    if m: cur = float(m.group(1))
    m = re.search(r"silence_end: ([\d.]+)", line)
    if m and cur is not None: sil.append((cur, float(m.group(1)))); cur = None

def boundary(prev_e, next_s):
    """이전 조각 끝과 다음 조각 시작 사이의 경계. 그 사이(±0.25s)의 가장 긴 무음 중앙."""
    lo, hi = min(prev_e, next_s) - 0.25, max(prev_e, next_s) + 0.25
    cands = [(b - a, a, b) for a, b in sil if b > lo and a < hi]
    if cands:
        _, a, b = max(cands)
        a, b = max(a, lo), min(b, hi)
        return (a + b) / 2, True
    return (prev_e + next_s) / 2, False

out = []
for k, r in enumerate(res):
    if r is None: continue
    out.append(r)
bounds = []
for i in range(len(out) - 1):
    t, found = boundary(out[i]["e"], out[i + 1]["s"])
    bounds.append(t)
    out[i]["sil"] = found
# 첫 조각 시작 = 첫 발화 직전 무음 끝, 마지막 = 마지막 발화 직후
first = out[0]["s"]
pre = [b for a, b in sil if b <= first + 0.3]
start0 = max(pre) if pre else first
last = out[-1]["e"]
post = [a for a, b in sil if a >= last - 0.3]
end_last = min(post) if post else last
for i, r in enumerate(out):
    r["t0"] = start0 if i == 0 else bounds[i - 1]
    r["t1"] = end_last if i == len(out) - 1 else bounds[i]

json.dump({"chunks": out, "missing": [chunks[k] for k, r in enumerate(res) if r is None],
           "report": report, "audio_end": AUDIO_END},
          open(f"{W}/timeline.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("matched", len(out), "/", len(chunks))
print("low cover:", [(r["slide"], r["text"], round(r["cover"], 2)) for r in out if r["cover"] < 0.7])
print("diffs:")
for r in report: print(" ", r)
