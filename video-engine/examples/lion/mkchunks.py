# -*- coding: utf-8 -*-
"""script.txt -> lines.json (caption units) + chunks.json (TTS requests).

Each TTS request carries ~1100-1300 chars (three requests) so the voice keeps one continuous read
(short per-line requests drift in tone when joined). Chunks break only after
a line that closes a sentence (~다 / ~죠 / ~요 / ?).
"""
import json, re

lines = [l.strip() for l in open("script.txt", encoding="utf-8") if l.strip()]

def spoken(l):
    s = l.replace('"', "").strip()
    if s[-1] in ".?!":
        return s
    if re.search(r"(다|죠|요|네)$", s):
        return s + "."
    return s + ","

def closes(l):
    return spoken(l)[-1] in ".?!"

TARGET = 1130
chunks, cur, start = [], [], 0
for i, l in enumerate(lines):
    cur.append(spoken(l))
    n = len(" ".join(cur))
    rest = sum(len(spoken(x)) + 1 for x in lines[i + 1:])
    if closes(l) and n >= TARGET and rest > 500:
        chunks.append({"first": start, "last": i, "text": " ".join(cur)})
        cur, start = [], i + 1
chunks.append({"first": start, "last": len(lines) - 1, "text": " ".join(cur)})

json.dump(lines, open("lines.json", "w", encoding="utf-8"), ensure_ascii=False, indent=0)
json.dump(chunks, open("chunks.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
for c in chunks:
    print(c["first"], c["last"], len(c["text"]), "|", c["text"][-40:])
