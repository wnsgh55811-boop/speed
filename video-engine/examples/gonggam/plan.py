# -*- coding: utf-8 -*-
"""Scene plan for "공감과 동의", read straight from script.txt.

Each script line is one narration sentence followed by ` >> ` and its scene
spec. Two extra codes on top of the engine's scene kinds:

  +  this line has no scene of its own — the NEXT scene starts early and
     covers it (short lead-ins like "여자가", "그러면")
  =  this line continues the PREVIOUS scene (tails like "라고 하면")

Chapter headers (H with a numeric id) bump the section counter the
background rotation keys off.
"""
import io
import os

HERE = os.path.dirname(os.path.abspath(__file__))
WATERMARK = "이다사"

LINES, PLAN, SECTION = [], [], []
_sec = 0
for raw in io.open(os.path.join(HERE, "script.txt"), encoding="utf-8"):
    raw = raw.rstrip("\n")
    if not raw.strip() or raw.startswith("#"):
        continue
    text, _, spec = raw.partition(" >> ")
    spec = spec.strip()
    kind, _, arg = spec.partition(" ")
    if kind == "H" and arg[:1].isdigit():
        _sec += 1
    LINES.append(text.strip())
    PLAN.append((kind, arg.strip()))
    SECTION.append(_sec)

assert all(k in "+=TPKNGHBCI" and len(k) == 1 for k, _ in PLAN), \
    [k for k, _ in PLAN if k not in "+=TPKNGHBCI"]
