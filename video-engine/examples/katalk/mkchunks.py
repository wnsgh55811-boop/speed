# -*- coding: utf-8 -*-
"""script.txt (one caption line per row) -> chunks.json (3 long TTS passes).

Long passes keep the cloned voice consistent; the line list stays the unit
for captions and scene cuts.
"""
import json, re
lines = [l.strip() for l in open("script.txt", encoding="utf-8") if l.strip()]
TERM = re.compile(r'(다|요|죠|까)"?$|[?.!]"?$')

def tts_text(ls):
    out, buf = [], ""
    for j, l in enumerate(ls):
        buf = (buf + " " + l).strip()
        nxt = ls[j + 1] if j + 1 < len(ls) else ""
        if nxt.startswith(("라고", "라는")):
            continue
        if TERM.search(l):
            if not re.search(r'[?.!]"?$', buf):
                buf += "."
            out.append(buf)
            buf = ""
    if buf:
        out.append(buf + ".")
    t = "\n".join(out)
    t = re.sub(r"ㅋ+", lambda m: "크" * min(3, len(m.group())), t)
    return t.replace(" ㅎㅎ", "")

# split into 3 passes at sentence ends, near equal length
tot = sum(len(l) for l in lines)
chunks, cur, acc, k = [], [], 0, 1
for i, l in enumerate(lines):
    cur.append(l); acc += len(l)
    nxt = lines[i + 1] if i + 1 < len(lines) else ""
    if k < 3 and acc >= tot * k / 3 and TERM.search(l) and not nxt.startswith(("라고", "라는")):
        chunks.append(cur); cur = []; k += 1
chunks.append(cur)
out = [{"i": i, "lines": c, "text": tts_text(c), "chars": sum(len(x) for x in c)}
       for i, c in enumerate(chunks)]
json.dump(out, open("chunks.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
for c in out:
    print(c["i"], len(c["lines"]), c["chars"], repr(c["lines"][0]), "...", repr(c["lines"][-1]))
