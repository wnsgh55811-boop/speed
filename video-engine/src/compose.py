# -*- coding: utf-8 -*-
"""Span-scene composer — the second-generation builder on top of emit.py.

emit.py maps one scene to one narration line (the 251-line film). Short,
fragmentary scripts make that choppy, so here a scene spans several lines and
everything *inside* it is timed to the line it belongs to: a bubble lands on
the sentence that says it, a bar grows on the word that names it, a token
slides across when the narrator says it was handed over.

    PROJECT=examples/hyena python3 src/compose.py [--local] [--from S --to S]

Reads  $PROJECT/{script.txt,timings.txt,plan.py,assets.json}
Writes $PROJECT/build/index.html (+ sfx.json for the mixer)

Timing contract for scene HTML: any element carrying data-t (seconds) and
data-fx gets a GSAP tween at that time. fx ∈ up fade pop left right draw growx
growy strike out move rot sweep shake on. Scenes never need their own JS.
"""
import html
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build                                                         # noqa: E402
from build import FAMILIES, IMG, ALIAS, CDN, caption_cards, motes, W, H   # noqa: E402

# captions are 50px bold here; measure them the same way so a card never wraps
build.CAP_PX, build.CAP_MAX, build.CAP_W = 50, 1580, "Bold"

PROJECT = os.path.abspath(os.environ.get("PROJECT", os.path.join(HERE, "..", "examples", "hyena")))
sys.path.insert(0, PROJECT)
LOCAL = "--local" in sys.argv


def esc(s):
    return html.escape(str(s), quote=True)


# ── time / asset context ────────────────────────────────────────────────────
class Ctx:
    def __init__(self):
        raw = open(os.path.join(PROJECT, "timings.txt"), encoding="utf-8").read()
        self.total = float(raw.split("TOTAL ")[1].split()[0])
        self.lt = [tuple(float(x) for x in p.split(","))
                   for p in raw.split("TIMES ")[1].split()]
        self.lines = [l for l in open(os.path.join(PROJECT, "script.txt"),
                                      encoding="utf-8").read().strip().split("\n")]
        assert len(self.lines) == len(self.lt), (len(self.lines), len(self.lt))
        self.assets = json.load(open(os.path.join(PROJECT, "assets.json"), encoding="utf-8"))
        self.sfx = []
        self.uses = {}
        self.rot = {}

    def T(self, line, dt=0.0):
        """Absolute seconds for a line start (+ offset)."""
        return round(self.lt[line][0] + dt, 3)

    def src(self, key):
        self.uses[key] = self.uses.get(key, 0) + 1
        if key in self.assets:
            v = self.assets[key]
        elif key in ALIAS:           # library pools: round-robin so no still repeats
            n = self.rot.get(key, 0)
            self.rot[key] = n + 1
            v = IMG[ALIAS[key][n % len(ALIAS[key])]]
        else:
            v = IMG[key]
        if v.startswith("assets/"):
            return v                              # rendered-side local file (videos)
        return v if v.startswith("http") else CDN + v


C = None   # set in main


def A(t, fx, d=None, **kw):
    """data-* attribute string for a timed effect."""
    s = f' data-t="{t:.3f}" data-fx="{fx}"'
    if d is not None:
        s += f' data-d="{d}"'
    for k, v in kw.items():
        s += f' data-{k}="{v}"'
    return s


def img(key, cls="", style=""):
    if LOCAL:
        return (f'<div class="ph-missing {cls}" style="{style}">{esc(key)}</div>')
    return f'<img class="{cls}" src="{C.src(key)}" alt="" style="{style}">'


def vid(key, t0, dur, cls="", style=""):
    """A clip's video. Local preview can't reach the CDN, so it falls back to
    a labelled placeholder; the render sandbox swaps in the processed file."""
    if LOCAL:
        return f'<div class="ph-missing {cls}" style="{style}">▶ {esc(key)}</div>'
    return (f'<video class="clip {cls}" src="{C.src(key)}" muted playsinline '
            f'data-start="{t0:.3f}" data-duration="{dur:.3f}" style="{style}"></video>')


# ── scene library ───────────────────────────────────────────────────────────
# Each returns dict(html=..., nocap=set(lines), bg=family|None, plate=bool)

def s_photo(sc, key, kb="in", tags=(), side=None, tint=True):
    """Full-bleed photograph with Ken Burns, optional timed tag pills."""
    shade = '<div class="shade"></div>' if tint else ""
    if side == "R":
        shade += '<div class="side"></div>'
    elif side == "L":
        shade += '<div class="sideL"></div>'
    h = [f'<div class="plate"><div class="kb" data-kb="{kb}">{img(key)}</div>{shade}</div>']
    for (ln, txt, pos, cls) in tags:
        h.append(f'<div style="position:absolute;{pos}"><span class="pill {cls}"'
                 f'{A(C.T(ln, .1), "pop")}>{esc(txt)}</span></div>')
    return dict(html="".join(h), plate=True)


def s_video(sc, key, side=None, title=None, rows=(), quotes=()):
    """Short generated clip as a live plate (the render side turns each 5s
    clip into a slow boomerang long enough for any scene, so it never
    freezes), with an optional timed panel on the darker side."""
    t0, t1 = sc["t0"], sc["t1"]
    shade = '<div class="shade"></div>'
    if side == "R":
        shade += '<div class="side"></div>'
    elif side == "L":
        shade += '<div class="sideL"></div>'
    h = [f'<div class="plate"><div class="kb" data-kb="in">{vid(key, t0, t1 - t0)}</div>{shade}</div>']
    if title or rows or quotes:
        pos = "right:110px" if side != "L" else "left:110px"
        h.append(f'<div style="position:absolute;{pos};top:0;height:880px;width:820px;display:flex;'
                 f'flex-direction:column;justify-content:center;gap:34px">')
        if title:
            ln, txt, cls = title
            h.append(f'<div class="big s {cls}" style="text-align:left"{A(C.T(ln, .05), "up")}>{esc(txt)}</div>')
        if rows:
            h.append('<div class="lst">')
            for r in rows:
                ln, txt, mk = r
                glyph = {"ok": "✓", "no": "✕", "q": "?", "n": "·"}.get(mk, "")
                h.append(f'<div class="li" style="font-size:50px"{A(C.T(ln, .05), "left")}><span class="ic {mk}">{glyph}</span>'
                         f'<span class="t">{esc(txt)}</span></div>')
            h.append('</div>')
        for q in quotes:
            ln, txt, st = q[0], q[1], q[2]
            who = f'<span class="who2">{esc(q[3])}</span>' if len(q) > 3 else ""
            al = "flex-end" if (len(q) > 3 and q[3] == "나") else "flex-start"
            h.append(f'<div class="qcard {st}" style="align-self:{al};margin-top:40px"{A(C.T(ln, .05), "pop")}>{who}{esc(txt)}</div>')
            C.sfx.append([C.T(ln, .05), "click"])
        h.append('</div>')
    return dict(html="".join(h), plate=True)


def s_typo(sc, parts, kick=None, align="center", y=0):
    """parts: [(line, text, cls)] — each line of type lands on its sentence.
    cls tokens: m s xs (size), cy am dim (colour), x (struck on the *next*
    line's time), hl (amber marker sweep)."""
    h = [f'<div class="zone"><div class="col" style="gap:26px;transform:translateY({y}px)">']
    if kick:
        ln, txt = kick
        h.append(f'<div class="kick"{A(C.T(ln), "fade")}>{esc(txt)}</div>')
    for k, p in enumerate(parts):
        ln, txt, cls = p[0], p[1], p[2] if len(p) > 2 else ""
        size = " ".join(c for c in cls.split() if c in ("m", "s", "xs"))
        col = {"cy": "c-cy", "am": "c-am", "dim": "c-dim", "red": "c-red"}
        colc = " ".join(col[c] for c in cls.split() if c in col)
        inner = esc(txt)
        extra = ""
        if "hl" in cls.split():
            inner = (f'<span class="mark"><span class="hl-bg"{A(C.T(ln, .35), "growx", .6)}>'
                     f'</span>{inner}</span>')
        if "x" in cls.split():
            xt = p[3] if len(p) > 3 and p[3] is not None else (
                C.T(parts[k + 1][0], .05) if k + 1 < len(parts) and parts[k + 1][0] > ln else C.T(ln, 1.0))
            extra = f'<i class="strk"{A(xt, "growx", .35)}></i>'
        h.append(f'<div class="big {size} {colc}" style="position:relative"'
                 f'{A(C.T(ln, .05), "up")}>{inner}{extra}</div>')
    h.append('</div></div>')
    return dict(html="".join(h))


def s_chat(sc, msgs, title="", read_at=None, typing_at=None, side="c", bgkey=None):
    """Stylised messenger thread; each bubble clicks in on its own line."""
    x = {"c": 0, "r": 380, "l": -380}[side]
    h = []
    if bgkey:
        h.append(f'<div class="plate"><div class="kb" data-kb="in">{img(bgkey)}</div>'
                 f'<div class="shade"></div><div class="{"side" if side=="r" else "sideL"}"></div></div>')
    h.append(f'<div class="zone"><div class="phone" style="transform:translateX({x}px)"'
             f'{A(sc["t0"], "up")}>')
    h.append(f'<div class="ph-top"><i></i>{esc(title)}</div>')
    for m in msgs:
        ln, who, txt = m[0], m[1], m[2]
        dt = m[3] if len(m) > 3 else 0.05
        rd = '<span class="rd">1</span>' if who == "me" and read_at is None and False else ""
        h.append(f'<div class="msg {who}"{A(C.T(ln, dt), "pop")}>{rd}<div class="b">{esc(txt)}</div></div>')
        C.sfx.append([C.T(ln, dt), "click"])
    if typing_at is not None:
        h.append(f'<div class="msg you"{A(C.T(typing_at, .2), "fade")}><div class="typing">'
                 '<i class="dot1"></i><i class="dot2"></i><i class="dot3"></i></div></div>')
    h.append('</div></div>')
    return dict(html="".join(h), plate=bool(bgkey))


def s_quotes(sc, quotes, bgkey=None, cut=None, layout="stack", side=None):
    """Quote / thought cards over a photo or a cut-out figure.
    quotes: [(line, text, style)] style ∈ y (spoken), dk (thought), am, cy."""
    h = []
    if bgkey:
        sd = {"R": "side", "L": "sideL"}.get(side, "")
        h.append(f'<div class="plate"><div class="kb" data-kb="in">{img(bgkey)}</div>'
                 f'<div class="shade"></div>{f"<div class={chr(34)}{sd}{chr(34)}></div>" if sd else ""}</div>')
    if cut:
        h.append(f'<div style="position:absolute;left:{160 if side!="L" else 1160}px;bottom:230px;'
                 f'height:640px;width:600px;display:flex;align-items:flex-end;justify-content:center"'
                 f'{A(sc["t0"], "up")}>{img(cut, "cutimg", "height:640px;width:auto;max-width:600px;object-fit:contain")}</div>')
    x0 = 330 if (cut or bgkey) and side != "L" else 0
    if side == "L":
        x0 = -330
    h.append(f'<div class="zone"><div class="col" style="gap:{"60px" if len(quotes) < 3 else "44px"};'
             f'transform:translateX({x0}px)">')
    for i, q in enumerate(quotes):
        ln, txt, st = q[0], q[1], q[2]
        cls = "thought" if st == "th" else f"qcard {st}"
        off = (i % 2) * 70 - 35 if layout == "zig" else 0
        h.append(f'<div class="{cls} flt" style="transform:translateX({off}px)"'
                 f'{A(C.T(ln, .05), "pop")}>{esc(txt)}</div>')
        C.sfx.append([C.T(ln, .05), "click"])
    h.append('</div></div>')
    return dict(html="".join(h), plate=bool(bgkey))


def s_rows(sc, items, title=None, width=None, y=0):
    """Rows that land on their own line. item: (line, text, mark, [x_at_line])
    mark ∈ ok no q n ·  — a 4th element strikes the row through at that line."""
    h = [f'<div class="zone"><div class="col" style="gap:40px;transform:translateY({y}px)">']
    if title:
        h.append(f'<div class="big xs c-am"{A(sc["t0"], "up")}>{esc(title)}</div>')
    h.append('<div class="lst">')
    for it in items:
        ln, txt, mk = it[0], it[1], it[2]
        glyph = {"ok": "✓", "no": "✕", "q": "?", "n": "·"}.get(mk, "")
        strike = ""
        if len(it) > 3 and it[3] is not None:
            strike = f'<i class="strk"{A(C.T(it[3], .1), "growx", .35)}></i>'
        h.append(f'<div class="li"{A(C.T(ln, .05), "left")}><span class="ic {mk}">{glyph}</span>'
                 f'<span class="t">{esc(txt)}{strike}</span></div>')
    h.append('</div></div></div>')
    return dict(html="".join(h))


def s_icon(sc, key, badge=None, sub=None, side="c", badge_at=None, sub_at=None):
    x = {"c": 0, "l": -420, "r": 420}[side]
    h = [f'<div class="zone"><div class="{"col" if side=="c" else "row2"}" style="gap:60px;'
         f'transform:translateX({0 if side=="c" else 0}px)">']
    tile = (f'<div class="tile flt"{A(sc["t0"], "pop")}>{img(key)}</div>')
    txt = ""
    if badge:
        txt += f'<div class="big s"{A(C.T(badge_at, .1) if badge_at is not None else sc["t0"] + .3, "up")}>{esc(badge)}</div>'
    if sub:
        txt += f'<div class="sub2"{A(C.T(sub_at, .1) if sub_at is not None else sc["t0"] + .6, "up")}>{esc(sub)}</div>'
    if side == "c":
        h.append(tile + f'<div class="col" style="gap:14px">{txt}</div>')
    else:
        h.append(tile + f'<div class="col" style="gap:20px;align-items:flex-start">{txt}</div>')
    h.append('</div></div>')
    return dict(html="".join(h))


def s_chapter(sc, num, title, key=None):
    h = []
    if key:
        h.append(f'<div class="plate"><div class="kb" data-kb="out">{img(key)}</div>'
                 '<div class="shade" style="background:rgba(8,8,10,.55)"></div></div>')
    h.append(f'<div class="zone"><div class="col">'
             f'<div class="chap-num"{A(sc["t0"] + .05, "fade")}>CHAPTER {esc(num)}</div>'
             f'<div class="chap-rule"{A(sc["t0"] + .15, "growx", .7)}></div>'
             f'<div class="chap-t"{A(sc["t0"] + .25, "up")}>{esc(title)}</div></div></div>')
    C.sfx.append([sc["t0"] + .05, "whoosh"])
    return dict(html="".join(h), plate=bool(key), bg="bg-ember")


def s_cmp(sc, left, right):
    """Two panes. each: dict(title, cls, img, rows=[(line, text)])"""
    h = ['<div class="zone"><div class="cmp">']
    for i, p in enumerate((left, right)):
        at = C.T(p["at"]) if "at" in p else sc["t0"] + i * .25
        face = img(p["img"], "face") if p.get("img") else ""
        h.append(f'<div class="pane {p.get("cls","")}"{A(at, "up")}>'
                 f'<h3 class="c-{"am" if p.get("cls")=="am" else "cy"}">{face}{esc(p["title"])}</h3>')
        for r in p["rows"]:
            h.append(f'<div class="pl"{A(C.T(r[0], .05), "left")}><b>›</b>{esc(r[1])}</div>')
        h.append('</div>')
    h.append('</div></div>')
    return dict(html="".join(h))


def s_graph_reverse(sc, a_at, b_at, lab_a, lab_b, xlab="시간", note=None):
    """Two lines crossing: my interest climbs while their response sinks."""
    X0, Y0, X1, Y1 = 260, 640, 1660, 140
    grid = "".join(f'<path class="ln gr" d="M{X0} {Y0 - k*125} L{X1} {Y0 - k*125}"/>' for k in range(1, 5))
    lv = "".join(f'<text class="dt-s" x="{X0-26}" y="{Y0 - k*125 + 14}" text-anchor="end">{lab}</text>'
                 for k, lab in ((1, "낮음"), (4, "높음")))
    a = f"M{X0} 520 C 620 500, 900 420, 1160 300 S 1540 170, {X1} 160"
    b = f"M{X0} 250 C 620 270, 900 340, 1160 450 S 1540 580, {X1} 600"
    h = (f'<div class="zone"><svg class="dg" width="1920" height="820" viewBox="0 0 1920 820">'
         f'<g{A(sc["t0"], "fade")}>{grid}{lv}'
         f'<path class="ln ax" d="M{X0} {Y1-20} L{X0} {Y0} L{X1+40} {Y0}"/>'
         f'<text class="dt-s" x="{(X0+X1)//2}" y="{Y0+60}" text-anchor="middle">{esc(xlab)} →</text></g>'
         f'<path class="ln st-am" d="{a}"{A(C.T(a_at), "draw", 2.2)}/>'
         f'<text class="dt-am" x="{X1-10}" y="130" text-anchor="end"{A(C.T(a_at, 1.6), "fade")}>{esc(lab_a)}</text>'
         f'<path class="ln st-cy" d="{b}"{A(C.T(b_at), "draw", 2.2)}/>'
         f'<text class="dt-cy" x="{X1-10}" y="660" text-anchor="end"{A(C.T(b_at, 1.6), "fade")}>{esc(lab_b)}</text>'
         + (f'<g{A(C.T(note[0]), "pop")}><circle cx="1160" cy="375" r="16" class="fl-w"/>'
            f'<text class="dt" x="1190" y="392">{esc(note[1])}</text></g>' if note else "")
         + '</svg></div>')
    C.sfx.append([C.T(a_at), "draw"])
    C.sfx.append([C.T(b_at), "draw"])
    return dict(html=h)


def s_graph_effort(sc, draw_at, peak_at, xl=("강함", "약함"), ylab="내 노력", xlab="상대 반응"):
    """Effort climbs as the other side's response weakens."""
    X0, Y0, X1 = 330, 660, 1600
    ticks = "".join(f'<path class="ln gr" d="M{X0} {Y0 - k*110} L{X1} {Y0 - k*110}"/>'
                    f'<text class="dt-s" x="{X0-24}" y="{Y0 - k*110 + 14}" text-anchor="end">{k}</text>'
                    for k in range(1, 6))
    d = f"M{X0} 600 C 700 590, 1000 520, 1200 400 S 1500 150, {X1} 110"
    h = (f'<div class="zone"><svg class="dg" width="1920" height="820" viewBox="0 0 1920 820">'
         f'<g{A(sc["t0"], "fade")}>{ticks}'
         f'<path class="ln ax" d="M{X0} 70 L{X0} {Y0} L{X1+30} {Y0}"/>'
         f'<text class="dt-am" x="{X0-110}" y="370" text-anchor="middle" transform="rotate(-90 {X0-110} 370)">{esc(ylab)}</text>'
         f'<text class="dt-s" x="{X0+10}" y="{Y0+56}">{esc(xl[0])}</text>'
         f'<text class="dt-s" x="{X1}" y="{Y0+56}" text-anchor="end">{esc(xl[1])}</text>'
         f'<text class="dt-cy" x="{(X0+X1)//2}" y="{Y0+60}" text-anchor="middle">{esc(xlab)} →</text></g>'
         f'<path class="ln st-am" d="{d}"{A(C.T(draw_at), "draw", 2.4)}/>'
         f'<g{A(C.T(peak_at), "pop")}><circle cx="{X1}" cy="110" r="20" class="fl-am"/>'
         f'<text class="dt-am" x="{X1-40}" y="96" text-anchor="end">점점 더</text></g>'
         '</svg></div>')
    C.sfx.append([C.T(draw_at), "draw"])
    C.sfx.append([C.T(peak_at), "tick"])
    return dict(html=h)


def s_scale(sc, steps, left="나", right="상대", drops=(), title=None):
    """A balance beam that tips a little further each time something is
    handed across. steps: [(line, deg)]; drops: [(line, label)] land on the
    right pan."""
    pivot_x, pivot_y = 960, 250
    h = ['<div class="zone"><div style="position:relative;width:1500px;height:760px">']
    if title:
        h.append(f'<div class="big xs c-am" style="position:absolute;top:-10px;left:0;right:0"'
                 f'{A(sc["t0"], "up")}>{esc(title)}</div>')
    stp = ";".join(f"{C.T(l, .1):.3f}:{d}" for l, d in steps)
    # beam group rotates about the pivot; pans hang and counter-rotate
    h.append(f'<svg class="dg" width="1500" height="760" viewBox="0 0 1500 760" style="position:absolute;inset:0">'
             f'<path class="ln ax" d="M750 250 L750 650" style="stroke-width:10;stroke:#8d8a83"/>'
             f'<path d="M620 690 L880 690 L820 650 L680 650 Z" fill="#8d8a83"/>'
             f'<g class="beam" data-steps="{stp}" style="transform-origin:750px 250px">'
             f'<path class="ln" d="M190 250 L1310 250" style="stroke:#e6e2d8;stroke-width:14"/>'
             f'<circle cx="750" cy="250" r="22" fill="#d8b368"/>'
             f'<g class="pan" data-counter="1" style="transform-origin:190px 250px">'
             f'<path class="ln" d="M190 250 L110 430 M190 250 L270 430" style="stroke:#bdbab3;stroke-width:4"/>'
             f'<path d="M80 430 L300 430 Q190 500 80 430 Z" class="fl-cy"/>'
             f'<text class="dt-cy" x="190" y="560" text-anchor="middle">{esc(left)}</text></g>'
             f'<g class="pan" data-counter="1" style="transform-origin:1310px 250px">'
             f'<path class="ln" d="M1310 250 L1230 430 M1310 250 L1390 430" style="stroke:#bdbab3;stroke-width:4"/>'
             f'<path d="M1200 430 L1420 430 Q1310 500 1200 430 Z" class="fl-am"/>'
             f'<text class="dt-am" x="1310" y="560" text-anchor="middle">{esc(right)}</text>')
    for k, (ln, lab) in enumerate(drops):
        y = 400 - k * 64
        h.append(f'<g{A(C.T(ln, .05), "drop")}><rect x="{1310-150}" y="{y-46}" width="300" height="56" rx="28" fill="#F4F1E8"/>'
                 f'<text x="1310" y="{y-6}" text-anchor="middle" style="font-weight:700;font-size:34px;fill:#1b1a16">{esc(lab)}</text></g>')
        C.sfx.append([C.T(ln, .05), "tick"])
    h.append('</g></g></svg></div></div>')
    return dict(html="".join(h))


def s_tokens(sc, items, left="나", right="상대", final=None):
    """Choices start on my side and are handed over one at a time."""
    h = ['<div class="zone"><div style="position:relative;width:1700px;height:760px">']
    h.append(f'<div style="position:absolute;left:0;top:40px;width:640px;height:620px;border-radius:40px;'
             f'border:3px dashed rgba(90,216,247,.55);background:rgba(90,216,247,.05)"{A(sc["t0"], "fade")}></div>'
             f'<div style="position:absolute;right:0;top:40px;width:640px;height:620px;border-radius:40px;'
             f'border:3px dashed rgba(216,179,104,.6);background:rgba(216,179,104,.05)"{A(sc["t0"], "fade")}></div>'
             f'<div class="big xs c-cy" style="position:absolute;left:0;width:640px;top:62px">{esc(left)}</div>'
             f'<div class="big xs c-am" style="position:absolute;right:0;width:640px;top:62px">{esc(right)}</div>'
             f'<div style="position:absolute;left:760px;top:330px;width:180px;text-align:center;font-size:90px;'
             f'color:rgba(255,255,255,.5);font-weight:800">→</div>')
    for k, (ln, lab) in enumerate(items):
        y = 190 + k * 96
        h.append(f'<div class="tok" style="left:70px;top:{y}px"{A(C.T(ln, .05), "move", .9, x=1060)}>{esc(lab)}</div>')
        C.sfx.append([C.T(ln, .05), "whoosh_s"])
    if final:
        h.append(f'<div class="big xs" style="position:absolute;left:0;right:0;top:320px"'
                 f'{A(C.T(final[0], .1), "up")}>{esc(final[1])}</div>')
    h.append('</div></div>')
    return dict(html="".join(h))


def s_iceberg(sc, top, bottom, top_at, bot_at, title_top="겉으로 보이는 것", title_bot="실제 이유"):
    h = ('<div class="zone"><svg class="dg" width="1700" height="820" viewBox="0 0 1700 820">'
         f'<path d="M0 330 L1700 330" class="ln" style="stroke:rgba(90,216,247,.6);stroke-width:4;stroke-dasharray:18 14"'
         f'{A(sc["t0"], "draw", 1.0)}/>'
         f'<path d="M850 110 L1030 330 L700 330 Z" fill="rgba(244,241,232,.92)"{A(C.T(top_at), "up")}/>'
         f'<path d="M700 330 L1030 330 L1240 520 L1110 760 L560 760 L430 540 Z" fill="rgba(90,216,247,.16)" '
         f'stroke="rgba(90,216,247,.6)" stroke-width="3"{A(C.T(bot_at), "fade", .8)}/>'
         f'<text class="dt-s" x="60" y="300">{esc(title_top)}</text>'
         f'<text class="dt-s" x="60" y="400"{A(C.T(bot_at), "fade")}>{esc(title_bot)}</text>'
         f'<text class="dt" x="1080" y="240"{A(C.T(top_at, .3), "fade")}>{esc(top)}</text>'
         f'<text class="dt-cy" x="835" y="560" text-anchor="middle" style="font-size:58px"'
         f'{A(C.T(bot_at, .4), "up")}>{esc(bottom)}</text>'
         '</svg></div>')
    return dict(html=h)


def s_timer(sc, label, at, dur, sub=None, sub_at=None, hours=False, key=None):
    """A ring that actually runs down for the seconds (or hours) it names."""
    r = 190
    circ = 2 * 3.14159 * r
    ticks = "".join(
        f'<path class="ln" d="M{300 + (r+26)*__import__("math").cos(k*3.14159/6):.1f} '
        f'{300 + (r+26)*__import__("math").sin(k*3.14159/6):.1f} L{300 + (r+42)*__import__("math").cos(k*3.14159/6):.1f} '
        f'{300 + (r+42)*__import__("math").sin(k*3.14159/6):.1f}" style="stroke:rgba(255,255,255,.35);stroke-width:4"/>'
        for k in range(12))
    tile = (f'<div class="tile flt" style="width:360px;height:360px">{img(key)}</div>' if key else "")
    h = (f'<div class="zone"><div class="row2" style="gap:90px">{tile}<div style="position:relative;width:600px;height:600px"'
         f'{A(sc["t0"], "pop")}>'
         f'<svg width="600" height="600" viewBox="0 0 600 600">{ticks}'
         f'<circle cx="300" cy="300" r="{r}" fill="none" stroke="rgba(255,255,255,.12)" stroke-width="22"/>'
         f'<circle cx="300" cy="300" r="{r}" fill="none" stroke="#5AD8F7" stroke-width="22" stroke-linecap="round" '
         f'transform="rotate(-90 300 300)" stroke-dasharray="{circ:.1f}" stroke-dashoffset="{circ:.1f}"'
         f'{A(C.T(at), "sweep", dur, len=round(circ,1))} style="filter:drop-shadow(0 0 14px rgba(90,216,247,.7))"/>'
         f'</svg><div style="position:absolute;inset:0;display:flex;align-items:center;justify-content:center;'
         f'font-size:120px;font-weight:800;color:#fff">{esc(label)}</div></div>')
    if sub:
        h += f'<div class="big s c-am"{A(C.T(sub_at, .1), "up")}>{esc(sub)}</div>'
    h += '</div></div>'
    C.sfx.append([C.T(at), "tick"])
    return dict(html=h)


def s_share(sc, mine, theirs_at, title_l="내 몫", title_r="상대의 몫", divide_at=None, theirs_label="들어올 공간"):
    h = ['<div class="zone"><div class="row2" style="gap:120px;position:relative">']
    h.append(f'<div class="pane" style="width:720px;min-height:560px;padding:40px 50px;border-radius:36px;'
             f'background:rgba(90,216,247,.08);border:3px solid rgba(90,216,247,.6)"{A(sc["t0"], "up")}>'
             f'<div class="big xs c-cy" style="margin-bottom:34px">{esc(title_l)}</div><div class="lst">')
    for ln, t in mine:
        h.append(f'<div class="li"{A(C.T(ln, .05), "left")}><span class="ic ok">✓</span><span class="t">{esc(t)}</span></div>')
    h.append('</div></div>')
    h.append(f'<div style="width:720px;min-height:560px;border-radius:36px;border:3px dashed rgba(216,179,104,.7);'
             f'display:flex;flex-direction:column;align-items:center;justify-content:center;gap:30px;'
             f'background:rgba(216,179,104,.05)"{A(sc["t0"] + .25, "up")}>'
             f'<div class="big xs c-am">{esc(title_r)}</div>'
             f'<div class="sub2 glow-am"{A(C.T(theirs_at, .1), "pulse")}>{esc(theirs_label)}</div></div>')
    if divide_at is not None:
        h.append(f'<div style="position:absolute;left:50%;top:-20px;bottom:-20px;width:6px;margin-left:-3px;'
                 f'background:#fff;border-radius:3px;transform-origin:top"{A(C.T(divide_at), "growy", .7)}></div>')
    h.append('</div></div>')
    return dict(html="".join(h))


def s_invest(sc, pairs, lopsided=False, gap_label=None, gap_at=None):
    """Two columns of blocks. balanced: each side stacks in turn.
    lopsided: only my side grows while theirs stays an empty outline."""
    h = ['<div class="zone"><div style="position:relative;width:1300px;height:760px">'
         '<div class="big xs c-cy" style="position:absolute;left:120px;width:420px;bottom:-10px">나</div>'
         '<div class="big xs c-am" style="position:absolute;right:120px;width:420px;bottom:-10px">상대</div>'
         '<div style="position:absolute;left:80px;right:80px;bottom:90px;height:4px;background:rgba(255,255,255,.4)"></div>']
    cnt = {"L": 0, "R": 0}
    for ln, side, lab in pairs:
        k = cnt[side]
        cnt[side] += 1
        x = 120 if side == "L" else 760
        y = 760 - 90 - 20 - (k + 1) * 104
        col = "rgba(90,216,247,.92)" if side == "L" else "rgba(216,179,104,.95)"
        h.append(f'<div style="position:absolute;left:{x}px;top:{y}px;width:420px;height:92px;border-radius:18px;'
                 f'background:{col};color:#0d0e10;font-weight:800;font-size:42px;display:flex;align-items:center;'
                 f'justify-content:center"{A(C.T(ln, .05), "drop")}>{esc(lab)}</div>')
        C.sfx.append([C.T(ln, .05), "tick"])
    if lopsided and gap_label:
        h.append(f'<div style="position:absolute;left:760px;top:250px;width:420px;height:400px;border-radius:24px;'
                 f'border:4px dashed rgba(216,179,104,.75);display:flex;align-items:center;justify-content:center;'
                 f'font-size:44px;font-weight:700;color:#d8b368;text-align:center"{A(C.T(gap_at, .1), "pulse")}>{esc(gap_label)}</div>')
    h.append('</div></div>')
    return dict(html="".join(h))


def s_steps(sc, back_at, fwd_at):
    """Other steps back once; I step forward twice."""
    h = ('<div class="zone"><svg class="dg" width="1700" height="600" viewBox="0 0 1700 600">'
         '<path class="ln ax" d="M80 400 L1620 400"/>'
         + "".join(f'<path class="ln gr" d="M{x} 380 L{x} 420" style="stroke:rgba(255,255,255,.35);stroke-width:3"/>'
                   for x in range(180, 1600, 180))
         + f'<g{A(C.T(fwd_at), "move", 1.1, x=360)}><circle cx="520" cy="330" r="46" class="fl-cy"/>'
         f'<text class="dt-cy" x="520" y="250" text-anchor="middle">나</text></g>'
         f'<g{A(C.T(back_at), "move", .9, x=180)}><circle cx="1080" cy="330" r="46" class="fl-am"/>'
         f'<text class="dt-am" x="1080" y="250" text-anchor="middle">상대</text></g>'
         f'<text class="dt" x="1260" y="520" text-anchor="middle"{A(C.T(back_at, .5), "fade")}>한 걸음 뒤로</text>'
         f'<text class="dt" x="700" y="520" text-anchor="middle"{A(C.T(fwd_at, .6), "fade")}>두 걸음 앞으로</text>'
         '</svg></div>')
    return dict(html=h)


def s_center(sc, like_at, move_at):
    """'The centre of my feelings' — a glowing core leaves my circle for theirs."""
    h = ('<div class="zone"><svg class="dg" width="1600" height="700" viewBox="0 0 1600 700">'
         f'<circle cx="420" cy="330" r="220" fill="rgba(90,216,247,.07)" stroke="rgba(90,216,247,.7)" stroke-width="4"/>'
         f'<circle cx="1180" cy="330" r="220" fill="rgba(216,179,104,.07)" stroke="rgba(216,179,104,.7)" stroke-width="4"/>'
         f'<text class="dt-cy" x="420" y="620" text-anchor="middle">나</text>'
         f'<text class="dt-am" x="1180" y="620" text-anchor="middle">상대</text>'
         f'<g{A(C.T(like_at), "pop")}><path d="M800 250 c-40-60-140-30-110 40 c20 40 110 90 110 90 s90-50 110-90 c30-70-70-100-110-40z" '
         f'fill="#F0707A" opacity=".9"/><text class="dt" x="800" y="200" text-anchor="middle">좋아함</text></g>'
         f'<g{A(C.T(move_at), "move", 1.4, x=760)}><circle cx="420" cy="330" r="54" fill="#fff" '
         f'style="filter:drop-shadow(0 0 24px rgba(255,255,255,.9))"/>'
         f'<text x="420" y="345" text-anchor="middle" style="font-weight:800;font-size:34px;fill:#111">중심</text></g>'
         '</svg></div>')
    C.sfx.append([C.T(move_at), "whoosh_s"])
    return dict(html=h)


def s_eq(sc, rows):
    """A ≠ B statements; the slash draws through on the line."""
    h = ['<div class="zone"><div class="col" style="gap:56px">']
    for ln, a, b in rows:
        h.append(f'<div class="row2" style="gap:40px"{A(C.T(ln, .05), "up")}>'
                 f'<span class="pill" style="font-size:54px">{esc(a)}</span>'
                 f'<span style="position:relative;font-size:96px;font-weight:800;color:#F0707A;width:90px;text-align:center">≠</span>'
                 f'<span class="pill cy" style="font-size:54px">{esc(b)}</span></div>')
    h.append('</div></div>')
    return dict(html="".join(h))


def s_cycle(sc, nodes, center, center_at):
    """Different situations, same attitude at the core."""
    import math
    cx, cy, r = 960, 450, 280
    h = ['<div class="zone"><svg class="dg" width="1920" height="820" viewBox="0 0 1920 820">']
    pts = []
    for k in range(len(nodes)):
        a = -math.pi / 2 + 2 * math.pi * k / len(nodes)
        pts.append((cx + r * 1.5 * math.cos(a), cy + r * math.sin(a)))
    arc = " ".join(f"{'M' if k==0 else 'L'}{x:.0f} {y:.0f}" for k, (x, y) in enumerate(pts + pts[:1]))
    h.append(f'<path class="ln" d="{arc}" style="stroke:rgba(255,255,255,.3);stroke-width:4;stroke-dasharray:14 12"'
             f'{A(sc["t0"], "draw", 1.2)}/>')
    for (ln, lab), (x, y) in zip(nodes, pts):
        h.append(f'<g{A(C.T(ln, .05), "pop")}><rect x="{x-170:.0f}" y="{y-50:.0f}" width="340" height="100" rx="50" '
                 f'fill="rgba(20,22,28,.9)" stroke="rgba(216,179,104,.8)" stroke-width="3"/>'
                 f'<text class="dt" x="{x:.0f}" y="{y+16:.0f}" text-anchor="middle">{esc(lab)}</text></g>')
    h.append(f'<g{A(C.T(center_at, .1), "pop")}><circle cx="{cx}" cy="{cy}" r="120" fill="rgba(90,216,247,.18)" '
             f'stroke="#5AD8F7" stroke-width="5"/><text class="dt-cy" x="{cx}" y="{cy+18}" text-anchor="middle">'
             f'{esc(center)}</text></g></svg></div>')
    return dict(html="".join(h))


def s_roots(sc, top, left, right, l_at, r_at, top_at=None):
    """Same surface, two different roots."""
    h = ['<div class="zone"><svg class="dg" width="1700" height="800" viewBox="0 0 1700 800">',
         f'<g{A(C.T(top_at) if top_at is not None else sc["t0"], "pop")}>'
         f'<rect x="530" y="40" width="640" height="130" rx="65" fill="#F6DF5A"/>'
         f'<text x="850" y="122" text-anchor="middle" style="font-weight:800;font-size:48px;fill:#1e1c16">{esc(top)}</text></g>',
         f'<path class="ln" d="M850 170 C 850 300, 420 330, 420 470" style="stroke:#5AD8F7;stroke-width:6"{A(C.T(l_at), "draw", .9)}/>',
         f'<path class="ln" d="M850 170 C 850 300, 1280 330, 1280 470" style="stroke:#d8b368;stroke-width:6"{A(C.T(r_at), "draw", .9)}/>',
         f'<g{A(C.T(l_at, .6), "up")}><rect x="120" y="480" width="600" height="140" rx="28" fill="rgba(90,216,247,.14)" stroke="#5AD8F7" stroke-width="3"/>'
         f'<text class="dt" x="420" y="566" text-anchor="middle">{esc(left)}</text></g>',
         f'<g{A(C.T(r_at, .6), "up")}><rect x="980" y="480" width="600" height="140" rx="28" fill="rgba(216,179,104,.14)" stroke="#d8b368" stroke-width="3"/>'
         f'<text class="dt" x="1280" y="566" text-anchor="middle">{esc(right)}</text></g>',
         '</svg></div>']
    return dict(html="".join(h))


def s_flip(sc, rows, title=None):
    """'fix' by flipping the behaviour: A → its opposite, same anxiety."""
    h = ['<div class="zone"><div class="col" style="gap:40px">']
    if title:
        h.append(f'<div class="big xs c-am"{A(sc["t0"], "up")}>{esc(title)}</div>')
    for a_ln, a, b_ln, b in rows:
        h.append(f'<div class="row2" style="gap:34px"><span class="pill" style="min-width:560px;justify-content:center"'
                 f'{A(C.T(a_ln, .05), "left")}>{esc(a)}</span>'
                 f'<span style="font-size:70px;color:#d8b368;font-weight:800"{A(C.T(b_ln), "fade")}>⇄</span>'
                 f'<span class="pill am" style="min-width:560px;justify-content:center"{A(C.T(b_ln, .1), "right")}>{esc(b)}</span></div>')
    h.append('</div></div>')
    return dict(html="".join(h))


def s_check(sc, num, title, quotes=(), rows=(), card=None):
    body = ""
    if card:
        body += f'<div class="card flt" style="width:640px;height:360px"{A(sc["t0"] + .3, "up")}>{img(card)}</div>'
    if rows:
        body += '<div class="lst">'
        for r in rows:
            ln, txt, mk = r[0], r[1], r[2]
            glyph = {"ok": "✓", "no": "✕", "q": "?", "n": "·"}.get(mk, "")
            body += (f'<div class="li" style="font-size:48px"{A(C.T(ln, .05), "left")}><span class="ic {mk}">{glyph}</span>'
                     f'<span class="t">{esc(txt)}</span></div>')
        body += '</div>'
    for q in quotes:
        ln, txt, st = q[0], q[1], q[2]
        strike = f'<i class="strk"{A(C.T(q[3], .1), "growx", .35)}></i>' if len(q) > 3 else ""
        body += f'<div class="qcard {st}"{A(C.T(ln, .05), "pop")}>{esc(txt)}{strike}</div>'
        C.sfx.append([C.T(ln, .05), "click"])
    if card and rows:
        body = f'<div class="row2" style="gap:70px;align-items:center">{body}</div>'
    h = (f'<div class="zone"><div class="col" style="gap:44px">'
         f'<div class="row2" style="gap:30px"{A(sc["t0"], "up")}>'
         f'<span style="width:120px;height:120px;border-radius:50%;background:var(--amber);color:#1b1408;'
         f'display:flex;align-items:center;justify-content:center;font-size:72px;font-weight:800">{esc(num)}</span>'
         f'<span class="big s" style="text-align:left">{esc(title)}</span></div>{body}</div></div>')
    C.sfx.append([sc["t0"], "impact"])
    return dict(html=h)


def s_cta(sc, lines_at):
    h = (f'<div class="zone"><div class="cta-card"{A(sc["t0"], "pop")}>'
         f'<div class="kick">PRIVATE LECTURE</div>'
         f'<div class="big s">비공개 특강</div>'
         f'<div class="sub2"{A(C.T(lines_at[0], .1), "up")}>멘트보다 먼저, 태도가 바뀌는 순간을 다룹니다</div>'
         f'<div class="sub2 c-am"{A(C.T(lines_at[2], .1), "up")}>스킬 공부만 해왔다면, 다른 관점에서</div>'
         f'<div class="cta-btn"{A(C.T(lines_at[1], .1), "pop")}>설명란에서 확인하기</div>'
         f'<div class="arrow-dn flt"{A(C.T(lines_at[1], .4), "fade")}>↓</div></div></div>')
    C.sfx.append([C.T(lines_at[1], .1), "click"])
    return dict(html=h)


def s_hook(sc, title_a, title_b, key):
    """0–3s: the paradox on screen before the first sentence ends."""
    t0 = sc["t0"]
    X0, Y0 = 1060, 700
    h = (f'<div class="plate"><div class="kb" data-kb="in">{vid(key, t0, sc["t1"] - t0) if key.startswith("v_") else img(key)}</div>'
         f'<div class="shade"></div><div class="side" style="background:linear-gradient(90deg,rgba(6,7,10,.05) 0%,rgba(6,7,10,.35) 45%,rgba(6,7,10,.86) 100%)"></div></div>'
         f'<div style="position:absolute;right:120px;top:130px;width:760px" class="col">'
         f'<div class="kick" style="align-self:flex-start"{A(t0 + .05, "fade")}>연애의 역설</div>'
         f'<div class="big m" style="text-align:left;align-self:flex-start;margin-top:16px"{A(t0 + .1, "up")}>{esc(title_a)}</div>'
         f'<div class="big m c-am" style="text-align:left;align-self:flex-start"{A(t0 + .45, "up")}>{esc(title_b)}</div>'
         f'<svg class="dg" width="760" height="330" viewBox="0 0 760 330" style="margin-top:30px">'
         f'<path class="ln ax" d="M20 20 L20 300 L740 300"/>'
         f'<path class="ln st-am" d="M20 270 C 250 250, 450 120, 720 40"{A(t0 + .7, "draw", 1.6)}/>'
         f'<path class="ln st-cy" d="M20 60 C 250 80, 450 200, 720 270"{A(t0 + .9, "draw", 1.6)}/>'
         f'<text class="dt-am" x="720" y="30" text-anchor="end" style="font-size:40px"{A(t0 + 1.9, "fade")}>내 호감</text>'
         f'<text class="dt-cy" x="720" y="225" text-anchor="end" style="font-size:40px"{A(t0 + 2.1, "fade")}>상대 반응</text>'
         '</svg></div>')
    C.sfx.append([t0 + .1, "impact"])
    return dict(html=h, plate=True)


SCENES = {k[2:]: v for k, v in globals().items() if k.startswith("s_")}


# ── main ────────────────────────────────────────────────────────────────────
JS = r"""
var tl = gsap.timeline({ paused: true });
function num(el, k, d){ var v = el.getAttribute('data-' + k); return v === null ? d : parseFloat(v); }
var FX = {
  up:    function(el,t,d){ tl.fromTo(el,{opacity:0,y:46},{opacity:1,y:0,duration:d||.6,ease:"power3.out"},t); },
  fade:  function(el,t,d){ tl.fromTo(el,{opacity:0},{opacity:1,duration:d||.5,ease:"power1.out"},t); },
  pop:   function(el,t,d){ tl.fromTo(el,{opacity:0,scale:.86},{opacity:1,scale:1,duration:d||.5,ease:"back.out(1.5)"},t); },
  left:  function(el,t,d){ tl.fromTo(el,{opacity:0,x:-70},{opacity:1,x:0,duration:d||.55,ease:"power3.out"},t); },
  right: function(el,t,d){ tl.fromTo(el,{opacity:0,x:70},{opacity:1,x:0,duration:d||.55,ease:"power3.out"},t); },
  drop:  function(el,t,d){ tl.fromTo(el,{opacity:0,y:-120},{opacity:1,y:0,duration:d||.55,ease:"bounce.out"},t); },
  out:   function(el,t,d){ tl.to(el,{opacity:.28,duration:d||.4,ease:"power1.out"},t); },
  growx: function(el,t,d){ tl.fromTo(el,{scaleX:0},{scaleX:1,duration:d||.7,ease:"expo.out",transformOrigin:"left center"},t); },
  growy: function(el,t,d){ tl.fromTo(el,{scaleY:0},{scaleY:1,duration:d||.7,ease:"expo.out",transformOrigin:"center top"},t); },
  draw:  function(el,t,d){ var L = el.getTotalLength ? el.getTotalLength() : 1000;
           tl.fromTo(el,{strokeDasharray:L,strokeDashoffset:L},{strokeDashoffset:0,duration:d||1,ease:"power2.inOut"},t); },
  sweep: function(el,t,d){ var L = num(el,'len',1000);
           tl.fromTo(el,{strokeDashoffset:L},{strokeDashoffset:0,duration:d||2,ease:"none"},t); },
  move:  function(el,t,d){ tl.fromTo(el,{opacity:el.style.opacity||1},{x:num(el,'x',0),y:num(el,'y',0),duration:d||.9,ease:"power2.inOut"},t); },
  pulse: function(el,t,d){ tl.fromTo(el,{opacity:.25},{opacity:1,duration:.45,ease:"sine.inOut",yoyo:true,repeat:4},t); },
  shake: function(el,t,d){ tl.fromTo(el,{x:-6},{x:6,duration:.08,ease:"sine.inOut",yoyo:true,repeat:5},t); }
};
document.querySelectorAll('[data-fx]').forEach(function(el){
  var f = FX[el.getAttribute('data-fx')]; if (f) f(el, num(el,'t',0), num(el,'d',null));
});
// balance beam: tip in steps; pans counter-rotate so they keep hanging level
document.querySelectorAll('.beam').forEach(function(g){
  var st = (g.getAttribute('data-steps')||'').split(';').filter(Boolean);
  var pans = g.querySelectorAll('.pan');
  st.forEach(function(s){ var p = s.split(':'), t = +p[0], r = +p[1];
    tl.to(g,{rotation:r,svgOrigin:"750 250",duration:1.1,ease:"power2.inOut"},t);
    pans.forEach(function(pn,i){ var ox = i ? 1310 : 190;
      tl.to(pn,{rotation:-r,svgOrigin:ox+" 250",duration:1.1,ease:"power2.inOut"},t); });
  });
});
// every scene breathes: slow push, never dead still
SC.forEach(function(s){
  var f = document.getElementById('fgm' + s.i);
  if (f) tl.fromTo(f,{scale:1,y:0},{scale:1.028,y:-8,duration:s.d,ease:"sine.inOut"},s.t);
  var kb = document.querySelectorAll('#fg' + s.i + ' .kb');
  kb.forEach(function(k){ var m = k.getAttribute('data-kb');
    var a = {in:[1.0,1.075,0,-18], out:[1.08,1.0,0,12]}[m] || [1.0,1.06,0,0];
    tl.fromTo(k,{scale:a[0],x:0,y:0},{scale:a[1],x:a[2]+(s.i%2?22:-22),y:a[3],duration:s.d,ease:"sine.inOut"},s.t); });
  var bg = document.getElementById('bgm' + s.i);
  if (bg) tl.fromTo(bg,{scale:1,xPercent:0},{scale:1.05,xPercent:(s.i%2?1:-1),duration:s.d,ease:"sine.inOut"},s.t);
  var fl = document.querySelectorAll('#fg' + s.i + ' .flt');
  var n = Math.max(1, Math.floor(s.d / 1.4));
  fl.forEach(function(e,j){ tl.fromTo(e,{yPercent:0},{yPercent:-2.2,duration:1.4,ease:"sine.inOut",yoyo:true,repeat:n-1},s.t + .6 + j*.2); });
  var dots = document.querySelectorAll('#fg' + s.i + ' .typing i');
  dots.forEach(function(e,j){ tl.fromTo(e,{opacity:.3},{opacity:1,duration:.4,yoyo:true,repeat:Math.max(1,Math.floor(s.d/0.8)),ease:"sine.inOut"},s.t + j*.15); });
  tl.fromTo('#fg' + s.i,{opacity:0},{opacity:1,duration:.22,ease:"power1.out"},s.t);
});
CAPT.forEach(function(ct,c){
  tl.fromTo('#cap' + c + ' .cap',{opacity:0,y:14},{opacity:1,y:0,duration:.2,ease:"power2.out"},ct);
});
window.__timelines = window.__timelines || {};
window.__timelines["main"] = tl;
"""


def segment(doc, a, b):
    """Cut [a, b) out of the full composition so a long film can be rendered
    in pieces that each fit inside one sandbox lease. Timed nodes are shifted
    by -a and trimmed; the GSAP master is scrubbed through a tweenFromTo, so
    every tween keeps its absolute authoring time."""
    def fix(m):
        tag, st, du = m.group(0), float(m.group(2)), float(m.group(3))
        s0, s1 = max(st, a), min(st + du, b)
        if s1 <= s0 + 1e-6:
            return m.group(1) + f'data-start="-1000" data-duration="0.001"'
        out = m.group(1) + f'data-start="{s0 - a:.3f}" data-duration="{s1 - s0:.3f}"'
        if m.group(1).rstrip().endswith("<video") or "<video" in m.group(1)[-80:]:
            out += f' data-media-start="{s0 - st:.3f}"'
        return out
    doc = re.sub(r'(<(?:div|video)[^>]*?)data-start="([-\d.]+)" data-duration="([\d.]+)"', fix, doc)
    doc = "\n".join(l for l in doc.split("\n")
                    if not (l.startswith('<div class="clip"') and 'data-start="-1000"' in l.split(">")[0]))
    doc = re.sub(r'(<div id="root"[^>]*?)data-start="-?[\d.]+" data-duration="[\d.]+"',
                 lambda m: m.group(1) + f'data-start="0" data-duration="{b - a:.3f}"', doc)
    doc = doc.replace('window.__timelines["main"] = tl;',
                      f'window.__timelines["main"] = gsap.timeline({{paused:true}})'
                      f'.add(tl.tweenFromTo({a:.4f}, {b:.4f}, {{ease:"none"}}));')
    return doc


def main():
    global C
    C = Ctx()
    import importlib
    plan = importlib.import_module("plan")
    SC = plan.SCENES
    lo = hi = None
    if "--from" in sys.argv:
        lo = float(sys.argv[sys.argv.index("--from") + 1])
        hi = float(sys.argv[sys.argv.index("--to") + 1])
    n = len(C.lines)
    starts = [s[0] for s in SC]
    assert starts == sorted(starts) and starts[0] == 0, "scenes must be ordered from line 0"
    bg_html, fg_html, cap_html, anim, capt = [], [], [], [], []
    nocap_all = set()
    prev = ["", ""]
    fam_i = 0
    for i, s in enumerate(SC):
        l0 = s[0]
        l1 = SC[i + 1][0] if i + 1 < len(SC) else n
        t0, t1 = C.lt[l0][0], C.lt[l1 - 1][1]
        kind, kw = s[1], (s[2] if len(s) > 2 else {})
        kw = dict(kw)
        nocap = set(kw.pop("nocap", ()))
        head = kw.pop("head", None)
        fam = kw.pop("bg", None)
        sc = dict(i=i, l0=l0, l1=l1, t0=t0, t1=t1)
        out = SCENES[kind](sc, **kw)
        if head:   # a heading that carries the lines before the diagram starts
            out["html"] += (f'<div class="big xs c-am" style="position:absolute;top:56px;left:0;right:0"'
                            f'{A(C.T(head[0], .05), "up")}>{esc(head[1])}</div>')
        nocap_all |= nocap
        d = t1 - t0
        if not out.get("plate"):
            fam = fam or out.get("bg")
            if not fam:
                fam = FAMILIES[fam_i % len(FAMILIES)]
                fam_i += 1
                if fam == prev[-1]:
                    fam = FAMILIES[fam_i % len(FAMILIES)]
                    fam_i += 1
            inner = f'<div class="motes">{motes(i)}</div>' if fam == "bg-dust" else ""
            bg_html.append(f'<div class="clip" id="bg{i}" data-start="{t0:.3f}" data-duration="{d:.3f}" '
                           f'data-track-index="0"><div class="layer"><div class="bgmove {fam}" id="bgm{i}">{inner}</div>'
                           f'<div class="grain"></div><div class="vig"></div></div></div>')
            prev.append(fam)
        else:
            prev.append("photo")
        fg_html.append(f'<div class="clip" id="fg{i}" data-start="{t0:.3f}" data-duration="{d:.3f}" '
                       f'data-track-index="1"><div class="fgm" id="fgm{i}">{out["html"]}</div>'
                       f'<div class="grain"></div></div>')
        anim.append({"i": i, "t": round(t0, 3), "d": round(d, 3)})

    cap_n = 0
    for li in range(n):
        if li in nocap_all:
            continue
        t0, t1 = C.lt[li]
        cards = caption_cards(C.lines[li])
        per = (t1 - t0) / len(cards)
        for j, c in enumerate(cards):
            cs = t0 + j * per
            cap_html.append(f'<div class="clip" id="cap{cap_n}" data-start="{cs:.3f}" data-duration="{per:.3f}" '
                            f'data-track-index="2"><div class="cap-wrap"><div class="cap-scrim"></div>'
                            f'<div class="cap">{esc(c)}</div></div></div>')
            capt.append(round(cs, 3))
            cap_n += 1

    css = open(os.path.join(HERE, "style.css"), encoding="utf-8").read() + \
        open(os.path.join(HERE, "kit.css"), encoding="utf-8").read()
    total = C.total
    js = (f"var SC = {json.dumps(anim, separators=(',', ':'))};\n"
          f"var CAPT = {json.dumps(capt, separators=(',', ':'))};\n" + JS)
    doc = f"""<!doctype html>
<html lang="ko"><head><meta charset="UTF-8">
<meta name="viewport" content="width={W}, height={H}">
<script src="vendor/gsap.min.js"></script>
<style>
{css}
</style></head><body>
<div id="root" data-composition-id="main" data-width="{W}" data-height="{H}" data-start="0" data-duration="{total:.3f}">
{chr(10).join(bg_html)}
{chr(10).join(fg_html)}
{chr(10).join(cap_html)}
<div class="clip" id="wmclip" data-start="0" data-duration="{total:.3f}" data-track-index="3"><div class="wm">이다사</div></div>
</div>
<script>
{js}
</script></body></html>
"""
    if "--seg" in sys.argv:
        a = float(sys.argv[sys.argv.index("--seg") + 1])
        b = float(sys.argv[sys.argv.index("--seg") + 2])
        doc = segment(doc, a, b)
    outdir = os.path.join(PROJECT, "build")
    os.makedirs(outdir, exist_ok=True)
    open(os.path.join(outdir, "index.html"), "w", encoding="utf-8").write(doc)
    json.dump(sorted(C.sfx), open(os.path.join(outdir, "sfx.json"), "w"))
    over = {k: v for k, v in C.uses.items() if v > 2}
    print(f"scenes {len(SC)} · captions {cap_n} · duration {total:.1f}s · sfx {len(C.sfx)}")
    if over:
        print("WARNING assets used >2x:", over)


if __name__ == "__main__":
    main()
