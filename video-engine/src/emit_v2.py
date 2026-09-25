# -*- coding: utf-8 -*-
"""Scene-group emitter: one scene spans several narration lines.

    python3 src/emit_v2.py examples/<project> [--audio assets/audio/master.wav]

emit.py gives every narration line its own scene, which at ~1.5 s a line cuts
too fast to read and leaves nothing moving inside a shot. Here a scene covers
a beat of the argument (2-6 s) and its elements reveal ON the line that names
them: any node carrying data-l="<line>" enters when that line starts. That
one convention is what keeps the motion tied to the narration instead of to
a generic entrance.

Project inputs (examples/<project>/):
  lines.json    caption lines, in narration order
  timings.txt   TOTAL <s> / TIMES a,b per line (estimate.py or align.py)
  plan.py       SCENES = [(first_line, last_line, kind, opts)], ASSETS map
Output: ../index.html plus sfx.json (cue list the audio mix reads).

Reused from the v1 engine: style.css (plates, captions, bubbles, bars),
the pictogram set, caption measuring and the dust field.
"""
import html
import json
import math
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
PROJ = os.path.abspath(sys.argv[1])
sys.path.insert(0, PROJ)
sys.path.insert(0, HERE)
import plan as P                                   # noqa: E402  (project plan)
import build                                       # noqa: E402
from emit import _PICTO                            # noqa: E402

build.CAP_PX, build.CAP_MAX = 52, 1640             # mobile-first caption size
W, H = 1920, 1080
CYAN, AMBER, RED, INK, DIM = "#5AD8F7", "#D8B368", "#E0675C", "#F4F3EF", "#918F8A"

_PICTO.update({
    "mouth": '<path d="M40 100q56 40 112 0"/><path d="M40 100q56-26 112 0"/>'
             '<path d="M70 150h52" stroke="#D8B368"/>',
    "face":  '<circle cx="96" cy="96" r="64"/><circle cx="74" cy="84" r="6" fill="currentColor" stroke="none"/>'
             '<circle cx="118" cy="84" r="6" fill="currentColor" stroke="none"/><path d="M72 120q24 8 48 0"/>',
    "eye":   '<path d="M20 96q76-72 152 0q-76 72-152 0z"/><circle cx="96" cy="96" r="22"/>'
             '<circle cx="96" cy="96" r="8" fill="currentColor" stroke="none"/>',
    "neat":  '<path d="M96 30l14 40 42 2-33 26 12 40-35-24-35 24 12-40-33-26 42-2z"/>',
    "fun":   '<circle cx="96" cy="96" r="64"/><path d="M66 110q30 34 60 0"/>'
             '<path d="M68 80h14M110 80h14"/>',
    "kind":  '<path d="M96 158s-58-34-58-72a30 30 0 0 1 58-11 30 30 0 0 1 58 11c0 38-58 72-58 72z"/>',
    "fit":   '<path d="M40 96h112M56 70v52M136 70v52M28 82v28M164 82v28"/>',
    "lock":  '<rect x="46" y="86" width="100" height="78" rx="14"/><path d="M68 86V64a28 28 0 0 1 56 0v22"/>'
             '<circle cx="96" cy="124" r="8" fill="currentColor" stroke="none"/>',
    "q":     '<circle cx="96" cy="96" r="64"/><path d="M76 76a20 20 0 1 1 26 19v14"/>'
             '<circle cx="102" cy="130" r="6" fill="currentColor" stroke="none"/>',
})


def esc(s):
    return html.escape(s, quote=True)


def picto(name, size=120, color=None):
    st = f' style="color:{color}"' if color else ""
    return (f'<svg class="picto" width="{size}" height="{size}" viewBox="0 0 192 192"{st} '
            'fill="none" stroke="currentColor" stroke-width="6" '
            f'stroke-linecap="round" stroke-linejoin="round">{_PICTO[name]}</svg>')


def asset(key):
    """Relative path the render sandbox fills (scripts/fetch_assets.py)."""
    if key.startswith(("ico_", "pic_")):
        return f"assets/keyed/{key}.png"
    ext = P.ASSETS[key].rsplit(".", 1)[-1]
    return f"assets/lib/{key}.{ext}"


# ── timing ──────────────────────────────────────────────────────────────────
raw = open(os.path.join(PROJ, "timings.txt"), encoding="utf-8").read()
TOTAL = float(raw.split("TOTAL ")[1].split()[0])
TIMES = [tuple(float(x) for x in p.split(",")) for p in raw.split("TIMES ")[1].split()]
LINES = json.load(open(os.path.join(PROJ, "lines.json"), encoding="utf-8"))
assert len(TIMES) == len(LINES), (len(TIMES), len(LINES))
HOLD = getattr(P, "END_HOLD", 2.4)
END = TIMES[-1][1] + HOLD
TOTAL = max(TOTAL, END)


def t(i):
    return TIMES[i][0]


class Ctx:
    def __init__(self, n, a, b, s0, s1):
        self.n, self.a, self.b, self.s0, self.s1 = n, a, b, s0, s1
        self.js, self.nocap = [], set()

    @property
    def d(self):
        return self.s1 - self.s0


SFX = []


def sfx(kind, at, gain=1.0):
    SFX.append({"k": kind, "t": round(at, 3), "g": gain})


def L(i, fx="up", d=0.05, ln=None, dur=None):
    """Attributes that make a node enter when narration line i starts."""
    extra = (f' data-len="{ln:.0f}"' if ln is not None else "") + (f' data-dur="{dur}"' if dur else "")
    return f'data-l="{i}" data-fx="{fx}" data-d="{d}"{extra}'


# ── backgrounds ─────────────────────────────────────────────────────────────
FAMILIES = ["bg-canvas", "bg-ink", "bg-teal", "bg-grid", "bg-spot", "bg-ember", "bg-dust"]
_prev = []


def plate(c, o):
    """Return (bg_html, is_media). Photos/clips own the plate; else a family."""
    if o.get("clip"):
        k = o["clip"]
        dur = min(c.d, 5.0)
        pos = o.get("focus", "50% 50%")
        return (f'<div class="bg-photo"><video class="bgv" id="v{c.n}" src="{asset(k)}" '
                f'muted playsinline data-start="{c.s0:.3f}" data-duration="{dur:.3f}" '
                f'data-media-start="{o.get("from", 0)}" style="object-position:{pos}"></video>'
                f'<div class="tint {o.get("tint", "")}"></div></div>', True)
    if o.get("photo"):
        pos = o.get("focus", "50% 50%")
        return (f'<div class="bg-photo"><img src="{asset(o["photo"])}" alt="" '
                f'style="object-position:{pos}">'
                f'<div class="tint {o.get("tint", "")}"></div></div>', True)
    fam = o.get("bg")
    if not fam:
        fam = FAMILIES[(c.n * 3) % len(FAMILIES)]
        # never the same family twice in a row (the rule is three; keep margin)
        while _prev and fam == _prev[-1]:
            fam = FAMILIES[(FAMILIES.index(fam) + 2) % len(FAMILIES)]
    _prev.append(fam)
    inner = f'<div class="motes">{build.motes(c.n)}</div>' if fam == "bg-dust" else ""
    return f'<div class="{fam}" style="position:absolute;inset:0">{inner}</div>', False


# ── shared pieces ───────────────────────────────────────────────────────────
def title_block(o, c, align="center"):
    h = []
    if o.get("kicker"):
        at = o.get("kicker_at", c.a)
        h.append(f'<div class="kick" {L(at, "fade")}>{esc(o["kicker"])}</div>')
    if o.get("title"):
        at = o.get("title_at", c.a)
        parts = o["title"].split("|")
        for j, p in enumerate(parts):
            cls = "big" + (" amber" if o.get("amber") == j else "")
            h.append(f'<div class="{cls}" {L(at, "up", 0.08 + j * 0.12)}>{esc(p)}</div>')
    return f'<div class="tblock {align}">{"".join(h)}</div>' if h else ""


def thought(text, line, side="r", tone=""):
    return (f'<div class="thought {side} {tone}" {L(line, "pop")}>'
            f'<span>{esc(text)}</span><i></i><i></i></div>')


def thought_groups(c, items):
    """Bubbles on the same side stack in one column, in narration order."""
    sides = {}
    for line, txt, sd in items:
        c.nocap.add(line)
        sides.setdefault(sd, []).append(thought(txt, line, sd))
    return "".join(f'<div class="tw {sd}">{"".join(b)}</div>' for sd, b in sides.items())


# ── scene kinds ─────────────────────────────────────────────────────────────
def k_media(c, o):
    """Photo or clip plate with optional title, tags and thought bubbles."""
    h = []
    side = o.get("side", "center")
    if o.get("title") or o.get("kicker"):
        h.append(f'<div class="panel {side}">{title_block(o, c, "left" if side != "center" else "center")}</div>')
    tags = o.get("tags", [])
    if tags:
        h.append(f'<div class="tags {o.get("tags_side", "left")}">')
        for line, txt, tone in tags:
            h.append(f'<span class="tag {tone}" {L(line, "left")}>{esc(txt)}</span>')
        h.append("</div>")
    h.append(thought_groups(c, o.get("thoughts", [])))
    if o.get("quote"):
        line, txt = o["quote"]
        c.nocap.add(line)
        h.append(f'<div class="qwrap"><div class="bub n" {L(line, "pop")}>'
                 f'{esc(txt)}</div></div>')
    return "".join(h)


def k_cut(c, o):
    figs = o["figs"]
    h = ['<div class="cutrow">']
    for j, f in enumerate(figs):
        key, at = (f, c.a) if isinstance(f, str) else f
        ht = o.get("h", 700 if len(figs) == 1 else 600)
        h.append(f'<div class="cutc" {L(at, "up", 0.05 + j * 0.1)}><img src="{asset(key)}" '
                 f'alt="" style="height:{ht}px"></div>')
    h.append("</div>")
    h.append(thought_groups(c, o.get("thoughts", [])))
    if o.get("kicker"):
        h.append(f'<div class="cutkick" {L(c.a, "fade")}>{esc(o["kicker"])}</div>')
    if o.get("tags"):
        h.append(f'<div class="tags {o.get("tags_side", "right")}">')
        for line, txt, tone in o["tags"]:
            h.append(f'<span class="tag {tone}" {L(line, "left")}>{esc(txt)}</span>')
        h.append("</div>")
    return "".join(h)


def k_type(c, o):
    """Large typography. parts: [(line, text, style)], style ∈ big/amber/dim/strike/kick."""
    h = ['<div class="typestack">']
    for line, txt, st in o["parts"]:
        if st == "kick":
            h.append(f'<div class="kick" {L(line, "fade")}>{esc(txt)}</div>')
        elif st == "strike":
            h.append(f'<div class="big dim sk" {L(line, "up")}>{esc(txt)}'
                     f'<i class="skl" {L(o.get("strike_at", line), "strike", 0.5)}></i></div>')
        else:
            cls = {"big": "big", "amber": "big amber", "dim": "big dim",
                   "cyan": "big cyan", "mid": "mid"}[st]
            h.append(f'<div class="{cls}" {L(line, "up", 0.1)}>{esc(txt)}</div>')
    h.append("</div>")
    if o.get("picto"):
        h.insert(0, f'<div class="tpicto" {L(c.a, "pop")}>{picto(o["picto"], 170, CYAN)}</div>')
    c.nocap.update(o.get("nocap", []))
    if o.get("impact"):
        sfx("impact", t(o["impact"]) + 0.08)
    return f'<div class="colstack">{"".join(h)}</div>'


def k_chips(c, o):
    """Row of pictogram chips, one per line."""
    h = []
    if o.get("head"):
        h.append(f'<div class="kick" {L(c.a, "fade")}>{esc(o["head"])}</div>')
    h.append('<div class="pchips">')
    for line, txt, pic in o["items"]:
        h.append(f'<div class="pchip" {L(line, "pop")}>{picto(pic, 110, CYAN)}'
                 f'<span>{esc(txt)}</span></div>')
    h.append("</div>")
    if o.get("after"):
        line, txt = o["after"]
        h.append(f'<div class="mid amberline" {L(line, "up")}>{esc(txt)}</div>')
    c.nocap.update(o.get("nocap", []))
    return f'<div class="colstack">{"".join(h)}</div>'


def k_rows(c, o):
    """Icon (3D or pictogram) left, rows that tick in per line right."""
    h = ['<div class="rowsplit">']
    if o.get("icon"):
        h.append(f'<div class="icol" {L(c.a, "pop")}><img class="ico float" '
                 f'src="{asset(o["icon"])}" alt=""></div>')
    h.append('<div class="rcol">')
    if o.get("head"):
        h.append(f'<div class="rhead" {L(o.get("head_at", c.a), "up")}>{esc(o["head"])}</div>')
    for it in o["rows"]:
        line, txt = it[0], it[1]
        mark = it[2] if len(it) > 2 else "tick"
        right = it[3] if len(it) > 3 else ""
        m = {"tick": '<i class="rt"></i>', "check": '<i class="rck">&#10003;</i>',
             "x": '<i class="rx">&#10005;</i>', "arrow": '<i class="rt amber"></i>'}[mark]
        rr = f'<span class="rarr">&rarr;</span><b>{esc(right)}</b>' if right else ""
        h.append(f'<div class="rrow {mark}" {L(line, "left")}>{m}<span>{esc(txt)}</span>{rr}</div>')
    h.append("</div></div>")
    c.nocap.update(o.get("nocap", []))
    return "".join(h)


def k_icon(c, o):
    h = [f'<div class="icoc" {L(c.a, "pop")}><img class="ico big float" src="{asset(o["icon"])}" alt=""></div>']
    for line, txt, st in o.get("labels", []):
        cls = {"big": "mid", "amber": "mid amberline", "cyan": "mid cyanline"}[st]
        h.append(f'<div class="{cls}" {L(line, "up")}>{esc(txt)}</div>')
    c.nocap.update(o.get("nocap", []))
    return f'<div class="colstack">{"".join(h)}</div>'


def k_chat(c, o):
    """Chat thread: bubbles stack as their line starts; the thread scrolls up."""
    h = ['<div class="thread">']
    for line, who, txt in o["msgs"]:
        c.nocap.add(line)
        side = "right" if who == "m" else "left"
        tag = {"m": "남자", "w": "여자", "n": ""}[who]
        whot = f'<span class="who">{esc(tag)}</span>' if tag else ""
        h.append(f'<div class="brow {side}" {L(line, "pop", o.get("dly", 0.05))}>'
                 f'<div class="bub {who}">{whot}{esc(txt)}</div></div>')
        sfx("click", t(line) + o.get("dly", 0.05), 0.8)
    h.append("</div>")
    if o.get("note"):
        line, txt = o["note"]
        h.append(f'<div class="chatnote" {L(line, "up")}>{esc(txt)}</div>')
    solo = " solo" if len(o["msgs"]) == 1 else ""
    return f'<div class="colstack{solo}">{"".join(h)}</div>'


def k_chapter(c, o):
    sfx("low", c.s0 + 0.05)
    return (f'<div class="colstack"><div class="pearl" {L(c.a, "pop", 0.02)}>{esc(o["num"])}</div>'
            f'<div class="chap-word" {L(c.a, "up", 0.2)}>{esc(o["word"])}</div>'
            f'<div class="chap-sub" {L(c.b, "fade")}>{esc(o.get("sub", ""))}</div></div>')


def k_search(c, o):
    q = o["query"]
    n = len(q)
    h = [f'<div class="search"><div class="sbar">{picto("q", 64, DIM)}'
         f'<span class="stext" id="st{c.n}"></span><i class="caret"></i></div>',
         '<div class="sres">']
    for j, r in enumerate(o["results"]):
        h.append(f'<div class="sr" {L(c.a, "up", 0.3 + n * 0.06 + j * 0.18)}>'
                 f'<i></i><span>{esc(r)}</span></div>')
    h.append("</div></div>")
    step = 0.06
    c.js.append(f'(function(){{var q={json.dumps(q)},el=document.getElementById("st{c.n}");'
                f'var o={{k:0}};tl.to(o,{{k:q.length,duration:{n * step:.2f},ease:"none",'
                f'onUpdate:function(){{el.textContent=q.slice(0,Math.round(o.k));}}}},{c.s0 + 0.25:.3f});'
                f'tl.set(el,{{textContent:""}},0);}})();')
    sfx("type", c.s0 + 0.25, 0.6)
    return "".join(h)


def k_quiz(c, o):
    h = [f'<div class="quiz"><div class="qhead" {L(c.a, "up")}>{esc(o["q"])}</div><div class="qopts">']
    for j, op in enumerate(o["opts"]):
        h.append(f'<div class="qopt" id="q{c.n}_{j}" {L(c.a, "up", 0.25 + j * 0.1)}>'
                 f'<i>{"ABCD"[j]}</i><span>{esc(op)}</span></div>')
    h.append(f'</div><div class="qcur" id="qc{c.n}"></div></div>')
    # the cursor hunts from option to option: looking for the answer she wants
    seq, t0 = [0, 2, 1, 3, 2], c.s0 + 0.9
    span = max(0.45, (c.d - 1.2) / len(seq))
    js = []
    for j, k in enumerate(seq):
        at = t0 + j * span
        js.append(f'tl.to("#q{c.n}_{k}",{{backgroundColor:"rgba(216,179,104,.30)",'
                  f'borderColor:"rgba(216,179,104,.9)",duration:.18}},{at:.3f});'
                  f'tl.to("#q{c.n}_{k}",{{backgroundColor:"rgba(255,255,255,.07)",'
                  f'borderColor:"rgba(255,255,255,.16)",duration:.25}},{at + span * 0.8:.3f});')
    c.js.append("".join(js))
    return "".join(h)


def k_phone(c, o):
    """Stylised messenger: my message stays unread while the clock runs."""
    a = c.a
    h = [f'<div class="phwrap"><div class="phone" {L(a, "up")}>'
         f'<div class="phtop"><span>{esc(o.get("name", "그녀"))}</span>'
         f'<b id="clk{c.n}">{o["clock"][0]}</b></div>'
         f'<div class="phbody"><div class="pmsg me"><span class="unread">1</span>'
         f'<div>{esc(o["msg"])}</div></div>'
         f'<div class="ptyping" id="pty{c.n}"><i></i><i></i><i></i></div></div></div>']
    h.append('<div class="phside">')
    for line, txt in o["thoughts"]:
        c.nocap.add(line)
        h.append(thought(txt, line, "l"))
    h.append("</div></div>")
    clocks = o["clock"]
    js = [f'tl.set("#clk{c.n}",{{textContent:"{clocks[0]}"}},0);']
    for j, (line, val) in enumerate(o["clock_at"]):
        js.append(f'tl.set("#clk{c.n}",{{textContent:"{val}"}},{t(line) + 0.1:.3f});'
                  f'tl.fromTo("#clk{c.n}",{{color:"{AMBER}"}},{{color:"#C9C7C1",duration:.8}},{t(line) + 0.1:.3f});')
    js.append(f'tl.to("#pty{c.n}",{{opacity:0,duration:.3}},{t(a) + 1.2:.3f});')
    c.js.append("".join(js))
    return "".join(h)


# graphs share one frame so axes, ticks and labels read the same everywhere
GX0, GX1, GY0, GY1 = 170, 1250, 70, 470          # plot box inside a 1400×560 svg


def _gx(u):
    return GX0 + (GX1 - GX0) * u


def _gy(v):
    return GY1 - (GY1 - GY0) * v


def _poly(pts):
    d = "M" + " L".join(f"{_gx(u):.1f} {_gy(v):.1f}" for u, v in pts)
    ln = sum(math.hypot(_gx(b[0]) - _gx(a[0]), _gy(b[1]) - _gy(a[1])) for a, b in zip(pts, pts[1:]))
    return d, ln


def graph_frame(ylab, levels, xlab, at):
    h = [f'<g {L(at, "fade")}>',
         f'<line class="ax" x1="{GX0}" y1="{GY1}" x2="{GX1 + 20}" y2="{GY1}"/>',
         f'<line class="ax" x1="{GX0}" y1="{GY1}" x2="{GX0}" y2="{GY0 - 20}"/>']
    for j, lab in enumerate(levels):
        v = (j + 1) / len(levels)
        h.append(f'<line class="grid" x1="{GX0}" y1="{_gy(v):.1f}" x2="{GX1}" y2="{_gy(v):.1f}"/>'
                 f'<text class="gtick" x="{GX0 - 22}" y="{_gy(v) + 12:.1f}" text-anchor="end">{esc(lab)}</text>')
    h.append(f'<text class="glab" x="{GX0}" y="{GY0 - 38}" text-anchor="start">{esc(ylab)}</text>'
             f'<text class="glab" x="{GX1 + 20}" y="{GY1 + 56}" text-anchor="end">{esc(xlab)}</text></g>')
    return "".join(h)


def k_graph(c, o):
    """Line graph: frame → series drawn on their lines → end labels/highlight."""
    h = [f'<svg class="graph" width="1400" height="560" viewBox="0 0 1400 560">',
         graph_frame(o["ylab"], o["levels"], o["xlab"], c.a)]
    for s in o["series"]:
        d, ln = _poly(s["pts"])
        col = {"cyan": CYAN, "amber": AMBER, "dim": "#8E9AA3", "red": RED}[s["tone"]]
        dur = s.get("dur", 1.1)
        h.append(f'<path class="gline" d="{d}" stroke="{col}" stroke-dasharray="{ln:.0f}" '
                 f'stroke-dashoffset="{ln:.0f}" {L(s["at"], "draw", 0.1, ln, dur)}/>')
        eu, ev = s["pts"][-1]
        h.append(f'<circle cx="{_gx(eu):.1f}" cy="{_gy(ev):.1f}" r="11" fill="{col}" '
                 f'{L(s["at"], "pop", 0.1 + dur)}/>'
                 f'<text class="gname" x="{_gx(eu) + 24:.1f}" y="{_gy(ev) + 12:.1f}" fill="{col}" '
                 f'{L(s["at"], "fade", 0.1 + dur)}>{esc(s["name"])}</text>')
        sfx("draw", t(s["at"]) + 0.1, 0.5)
    for m in o.get("marks", []):
        u, v = m["pt"]
        h.append(f'<g {L(m["at"], "pop")}><circle cx="{_gx(u):.1f}" cy="{_gy(v):.1f}" r="22" '
                 f'fill="none" stroke="{AMBER}" stroke-width="4"/>'
                 f'<text class="gnote" x="{_gx(u):.1f}" y="{_gy(v) + m.get("dy", -40):.1f}" text-anchor="middle">'
                 f'{esc(m["text"])}</text></g>')
        sfx("tick", t(m["at"]) + 0.05, 0.6)
    h.append("</svg>")
    head = f'<div class="ghead" {L(c.a, "up")}>{esc(o["head"])}</div>' if o.get("head") else ""
    return f'<div class="colstack">{head}{"".join(h)}</div>'


def k_level(c, o):
    """Five-step level that drops one step per beat: a standard given up."""
    n = 5
    h = [f'<div class="colstack"><div class="ghead" {L(c.a, "up")}>{esc(o["head"])}</div>'
         '<div class="level">']
    for j in range(n):
        h.append(f'<div class="lvrow"><span class="lvlab">{n - j}</span>'
                 f'<i class="lvb" id="lv{c.n}_{n - 1 - j}"></i></div>')
    h.append('</div></div>')
    drops = o.get("drops") or [c.s0 + 0.9 + j * max(0.35, (c.d - 1.4) / 4) for j in range(4)]
    js = []
    for j, at in enumerate(drops):
        k = n - 1 - j
        js.append(f'tl.to("#lv{c.n}_{k}",{{backgroundColor:"rgba(255,255,255,.06)",'
                  f'boxShadow:"none",scaleX:.35,duration:.35,ease:"power2.in"}},{at:.3f});')
        sfx("tick", at, 0.45)
    c.js.append("".join(js))
    return "".join(h)


def k_bars(c, o):
    """Effort bars: one side grows beat by beat, the other stays put."""
    h = [f'<div class="colstack"><div class="ghead" {L(c.a, "up")}>{esc(o["head"])}</div><div class="ebars">']
    for key, lab, tone in (("me", o["me"], "cyan"), ("you", o["you"], "dim")):
        dots = "".join(f'<i id="ed{c.n}{key}{k}"></i>' for k in range(5))
        h.append(f'<div class="ebar"><div class="bar-head"><span class="bar-lab">{esc(lab)}</span>'
                 f'<span class="bar-dots">{dots}</span></div><div class="bar-track">'
                 + "".join(f'<span class="tickline" style="left:{q}%"></span>' for q in (20, 40, 60, 80))
                 + f'<i class="bar-fill {tone}" id="eb{c.n}{key}" style="width:100%"></i></div></div>')
    h.append('<div class="bar-axis"><span>적음</span><span>많음</span></div></div></div>')
    js = [f'tl.set("#eb{c.n}me",{{scaleX:.04}},0);tl.set("#eb{c.n}you",{{scaleX:.0}},0);'
          f'tl.to("#eb{c.n}you",{{scaleX:{o["you_v"]},duration:.6,ease:"power3.out"}},{c.s0 + 0.4:.3f});'
          f'tl.set("#ed{c.n}you0",{{className:"on"}},{c.s0 + 0.6:.3f});']
    for j, (line, v) in enumerate(o["steps"]):
        at = t(line) + 0.12
        js.append(f'tl.to("#eb{c.n}me",{{scaleX:{v},duration:.55,ease:"power3.out"}},{at:.3f});')
        on = max(1, min(5, round(v * 5)))
        for k in range(on):
            js.append(f'tl.set("#ed{c.n}me{k}",{{className:"on"}},{at + 0.3:.3f});')
        sfx("tick", at, 0.45)
    c.js.append("".join(js))
    return "".join(h)


def two_nodes(me="나", you="상대", gap=640, y=250):
    x0, x1 = 700 - gap / 2, 700 + gap / 2
    return x0, x1, (f'<circle class="nd" cx="{x0}" cy="{y}" r="74"/><text class="ndl" x="{x0}" y="{y + 16}" text-anchor="middle">{esc(me)}</text>'
                    f'<circle class="nd you" cx="{x1}" cy="{y}" r="74"/><text class="ndl" x="{x1}" y="{y + 16}" text-anchor="middle">{esc(you)}</text>')


def k_diagram(c, o):
    kind = o["fig"]
    svg, extra = [], ""
    if kind == "boundary":
        x0, x1, nodes = two_nodes()
        svg.append(f'<g {L(c.a, "fade")}>{nodes}</g>')
        svg.append(f'<path class="dline" d="M{x0 + 90} 250 L{x1 - 110} 250" stroke-dasharray="360" '
                   f'stroke-dashoffset="360" {L(c.a, "draw", 0.2, 360)}/>'
                   f'<path class="dhead" d="M{x1 - 124} 230 L{x1 - 96} 250 L{x1 - 124} 270" {L(c.a, "fade", 0.9)}/>'
                   f'<text class="dtag" x="700" y="220" text-anchor="middle" {L(c.a, "fade", 0.6)}>내 표현</text>')
        svg.append(f'<circle class="bound" cx="{x1}" cy="250" r="150" {L(o["bound_at"], "pop")}/>'
                   f'<text class="dtag amb" x="{x1}" y="460" text-anchor="middle" {L(o["bound_at"], "fade", 0.3)}>반응은 상대의 몫</text>')
    elif kind == "handoff":
        x0, x1, nodes = two_nodes()
        svg.append(f'<g {L(c.a, "fade")}>{nodes}</g>')
        extra = f'<div class="token" id="tk{c.n}">선택권</div>'
        c.js.append(f'tl.fromTo("#tk{c.n}",{{x:-330,y:0,opacity:0}},{{opacity:1,duration:.3}},{c.s0 + 0.2:.3f});'
                    f'tl.to("#tk{c.n}",{{x:330,duration:1.0,ease:"power2.inOut"}},{c.s0 + 0.9:.3f});'
                    f'tl.to("#tk{c.n}",{{backgroundColor:"rgba(216,179,104,.95)",color:"#1E1A12",duration:.3}},{c.s0 + 1.9:.3f});')
        sfx("whoosh", c.s0 + 0.9, 0.6)
    elif kind == "venn":
        svg.append(f'<circle class="rel" cx="700" cy="250" r="235" {L(c.a, "fade")}/>'
                   f'<text class="dtag dim" x="700" y="62" text-anchor="middle" {L(c.a, "fade")}>관계</text>')
        extra = (f'<div class="vc me" id="vm{c.n}"><span>내가<br>원하는 것</span></div>'
                 f'<div class="vc you" id="vy{c.n}"><span>상대가<br>원하는 것</span></div>')
        c.js.append(f'tl.fromTo("#vy{c.n}",{{x:0,opacity:0}},{{opacity:1,duration:.4}},{c.s0 + 0.2:.3f});'
                    f'tl.fromTo("#vm{c.n}",{{x:-420,opacity:0}},{{x:0,opacity:1,duration:1.0,ease:"power3.out"}},{t(o["join_at"]) + 0.1:.3f});')
        sfx("whoosh", t(o["join_at"]) + 0.1, 0.5)
    elif kind == "steps":
        # a track of positions; she steps away once, he closes two
        xs = [220 + k * 160 for k in range(7)]
        svg.append(f'<g {L(c.a, "fade")}><line class="ax" x1="160" y1="330" x2="1240" y2="330"/>'
                   + "".join(f'<line class="grid" x1="{x}" y1="316" x2="{x}" y2="344"/>' for x in xs) + "</g>")
        extra = (f'<div class="dot me" id="dm{c.n}"><span>나</span></div>'
                 f'<div class="dot you" id="dy{c.n}"><span>상대</span></div>'
                 f'<div class="mood" id="md{c.n}"></div>')
        a = o["at"]           # smile, cold, away, closer
        c.js.append(
            f'tl.set("#dm{c.n}",{{x:{xs[1] - 700}}},0);tl.set("#dy{c.n}",{{x:{xs[4] - 700}}},0);'
            f'tl.set("#md{c.n}",{{textContent:"",opacity:0}},0);'
            f'tl.set("#md{c.n}",{{textContent:"다행이다",color:"{CYAN}"}},{t(a[0]):.3f});'
            f'tl.fromTo("#md{c.n}",{{opacity:0,y:10}},{{opacity:1,y:0,duration:.35}},{t(a[0]):.3f});'
            f'tl.set("#md{c.n}",{{textContent:"불안",color:"{RED}"}},{t(a[1]):.3f});'
            f'tl.fromTo("#md{c.n}",{{scale:1.25}},{{scale:1,duration:.4}},{t(a[1]):.3f});'
            f'tl.to("#dy{c.n}",{{x:{xs[5] - 700},duration:.7,ease:"power2.inOut"}},{t(a[2]) + 0.2:.3f});'
            f'tl.to("#dm{c.n}",{{x:{xs[3] - 700},duration:.9,ease:"power2.inOut"}},{t(a[3]) + 0.15:.3f});')
        svg.append(f'<text class="dtag" x="{xs[5]}" y="440" text-anchor="middle" {L(a[2], "fade", 0.6)}>한 걸음</text>'
                   f'<text class="dtag amb" x="{xs[2]}" y="440" text-anchor="middle" {L(a[3], "fade", 0.9)}>두 걸음</text>')
        sfx("whoosh", t(a[2]) + 0.2, 0.4)
        sfx("whoosh", t(a[3]) + 0.15, 0.5)
    elif kind == "center":
        svg.append(f'<circle class="ring" cx="700" cy="250" r="150" {L(c.a, "fade")}/>'
                   f'<circle class="core" cx="700" cy="250" r="34" {L(c.a, "pop")}/>'
                   f'<text class="dtag" x="700" y="460" text-anchor="middle" {L(o["label_at"], "fade")}>중심은 그대로</text>')
        for k in range(3):
            svg.append(f'<path class="wave" id="wv{c.n}_{k}" d="M1240 {170 + k * 0} q-40 80 0 160" />')
        js = []
        for k in range(3):
            at = t(o["wave_at"]) + k * 0.55
            js.append(f'tl.fromTo("#wv{c.n}_{k}",{{x:0,opacity:0}},{{x:-360,opacity:.9,duration:.6,ease:"power1.in"}},{at:.3f});'
                      f'tl.to("#wv{c.n}_{k}",{{opacity:0,duration:.25}},{at + 0.6:.3f});'
                      f'tl.fromTo("#rg{c.n}",{{scale:1}},{{scale:1.035,duration:.12,yoyo:true,repeat:1}},{at + 0.58:.3f});')
        c.js.append("".join(js))
        svg[0] = svg[0].replace('class="ring"', f'class="ring" id="rg{c.n}" style="transform-origin:700px 250px"')
        extra = f'<div class="dcap" {L(c.a, "fade")}>상대의 반응</div>'
    elif kind in ("fill", "space"):
        svg.append(f'<g {L(c.a, "fade")}><path class="half me" d="M700 60 A190 190 0 0 0 700 440 Z"/>'
                   f'<path class="half you" id="hy{c.n}" d="M700 60 A190 190 0 0 1 700 440 Z"/>'
                   f'<line class="ax" x1="700" y1="40" x2="700" y2="460"/></g>'
                   f'<text class="dtag" x="560" y="258" text-anchor="middle" {L(c.a, "fade")}>나</text>'
                   f'<text class="dtag" x="840" y="258" text-anchor="middle" {L(c.a, "fade")}>상대</text>')
        if kind == "fill":
            svg.append(f'<path class="flood" id="fl{c.n}" d="M700 60 A190 190 0 0 1 700 440 Z"/>')
            c.js.append(f'tl.set("#fl{c.n}",{{scaleX:0,transformOrigin:"700px 250px"}},0);'
                        f'tl.to("#fl{c.n}",{{scaleX:1,duration:1.2,ease:"power2.inOut"}},{t(o["fill_at"]) + 0.1:.3f});')
            svg.append(f'<text class="dtag amb" x="700" y="520" text-anchor="middle" {L(o["fill_at"], "fade", 0.8)}>그 자리까지 내가 채운다</text>')
            sfx("whoosh", t(o["fill_at"]) + 0.1, 0.5)
        else:
            svg.append(f'<path class="glowhalf" d="M700 60 A190 190 0 0 1 700 440 Z" {L(o["glow_at"], "fade")}/>'
                       f'<text class="dtag amb" x="700" y="520" text-anchor="middle" {L(o["glow_at"], "fade", 0.3)}>상대가 해야 할 몫은 남겨둔다</text>')
            c.js.append(f'tl.fromTo("#hy{c.n}",{{opacity:.35}},{{opacity:.9,duration:1.2,yoyo:true,repeat:{max(1, int(c.d // 1.2))}}},{c.s0:.3f});')
    elif kind == "recip":
        rows = o["rows"]
        h = ['<div class="recip">']
        if o.get("head"):
            h.append(f'<div class="ghead" {L(o.get("head_at", c.a), "up")}>{esc(o["head"])}</div>')
        for line, a_, b_ in rows:
            h.append(f'<div class="rc" {L(line, "up")}><span class="ra">{esc(a_)}</span>'
                     f'<span class="rarrs"><i>&rarr;</i><i>&larr;</i></span><span class="rb">{esc(b_)}</span></div>')
            sfx("tick", t(line) + 0.1, 0.4)
        h.append("</div>")
        return "".join(h)
    top = f'<div class="ghead" {L(c.a, "up")}>{esc(o["head"])}</div>' if o.get("head") else ""
    return (f'<div class="colstack">{top}<div class="dstage"><svg class="diagram" width="1400" height="540" '
            f'viewBox="0 -20 1400 560">{"".join(svg)}</svg>{extra}</div></div>')


def k_compare(c, o):
    h = ['<div class="cmp">']
    for key in ("l", "r"):
        line, name, txt = o[key]
        h.append(f'<div class="cmpc {key}"><div class="cmpn" {L(line, "up")}>{esc(name)}</div>'
                 f'<div class="cmpt" {L(line + 1, "up")}>{esc(txt)}</div></div>')
    h.append("</div>")
    c.nocap.update(o.get("nocap", []))
    return "".join(h)


def k_check(c, o):
    h = [f'<div class="colstack"><div class="ghead" {L(c.a, "up")}>{esc(o["head"])}</div><div class="cklist">']
    for line, txt in o["items"]:
        h.append(f'<div class="ck" {L(line, "left")}><svg width="64" height="64" viewBox="0 0 64 64">'
                 f'<rect x="4" y="4" width="56" height="56" rx="12" class="ckb"/>'
                 f'<path d="M16 33 L28 45 L49 20" class="ckm" stroke-dasharray="52" stroke-dashoffset="52" '
                 f'{L(line, "draw", 0.35, 52, 0.4)}/></svg><span>{esc(txt)}</span></div>')
        sfx("tick", t(line) + 0.35, 0.5)
    h.append("</div></div>")
    c.nocap.update(o.get("nocap", []))
    return "".join(h)


def k_timer(c, o):
    r = 170
    circ = 2 * math.pi * r
    dur = max(1.2, c.s1 - c.s0 - 0.8)
    h = [f'<div class="timer"><img class="ico tmr float" src="{asset(o["icon"])}" alt="" {L(c.a, "pop")}>'
         f'<svg width="460" height="460" viewBox="0 0 460 460" class="tring">'
         f'<circle cx="230" cy="230" r="{r}" class="trk"/>'
         f'<circle cx="230" cy="230" r="{r}" class="tprog" id="tp{c.n}" stroke-dasharray="{circ:.0f}" '
         f'stroke-dashoffset="{circ:.0f}" transform="rotate(-90 230 230)"/></svg>'
         f'<div class="tnum" id="tn{c.n}">0.0초</div></div>',
         f'<div class="tlabel" {L(o["label_at"], "up")}>{esc(o["label"])}</div>']
    c.js.append(f'(function(){{var o={{v:0}},el=document.getElementById("tn{c.n}");'
                f'tl.to("#tp{c.n}",{{strokeDashoffset:0,duration:{dur:.2f},ease:"none"}},{c.s0 + 0.4:.3f});'
                f'tl.to(o,{{v:2,duration:{dur:.2f},ease:"none",onUpdate:function(){{el.textContent=o.v.toFixed(1)+"초";}}}},{c.s0 + 0.4:.3f});'
                f'tl.set(el,{{textContent:"0.0초"}},0);}})();')
    sfx("tick", c.s0 + 0.4, 0.4)
    sfx("tick", c.s0 + 0.4 + dur / 2, 0.4)
    sfx("tick", c.s0 + 0.4 + dur, 0.5)
    return "".join(h)


def k_iceberg(c, o):
    return (f'<div class="berg"><img class="ico berg-i float" src="{asset(o["icon"])}" alt="" {L(c.a, "pop")}>'
            f'<div class="bl top" {L(o["top"][0], "left")}><i></i>{esc(o["top"][1])}</div>'
            f'<div class="bl bot" {L(o["bot"][0], "left", 0.9 if o["bot"][0] == o["top"][0] else 0.05)}>'
            f'<i></i>{esc(o["bot"][1])}</div></div>')


def k_cta(c, o):
    sfx("low", c.s0 + 0.1, 0.7)
    return (f'<div class="cta"><div class="ctab" {L(c.a, "pop")}>{picto("lock", 120, AMBER)}'
            f'<div><div class="ctak">비공개 특강</div><div class="ctat">{esc(o["title"])}</div></div></div>'
            f'<div class="ctad" {L(c.b, "up")}><span>설명란에서 확인하세요</span><i class="ctaarrow">&darr;</i></div></div>')


def k_takeaway(c, o):
    sfx("impact", c.s0 + 0.1, 0.8)
    parts = o["title"].split("|")
    h = "".join(f'<div class="take{" amber" if j else ""}" {L(c.a + min(j, c.b - c.a), "up", 0.15)}>{esc(p)}</div>'
                for j, p in enumerate(parts))
    c.nocap.update(range(c.a, c.b + 1))
    return f'<div class="colstack">{h}<div class="takerule" {L(c.b, "strike", 0.6)}></div></div>'


KINDS = {"media": k_media, "cut": k_cut, "type": k_type, "chips": k_chips, "rows": k_rows,
         "icon": k_icon, "chat": k_chat, "chapter": k_chapter, "search": k_search,
         "quiz": k_quiz, "phone": k_phone, "graph": k_graph, "level": k_level,
         "bars": k_bars, "diagram": k_diagram, "compare": k_compare, "check": k_check,
         "timer": k_timer, "iceberg": k_iceberg, "cta": k_cta, "takeaway": k_takeaway}


# ── main ────────────────────────────────────────────────────────────────────
def main():
    audio = sys.argv[sys.argv.index("--audio") + 1] if "--audio" in sys.argv else None
    scenes = P.SCENES
    # scenes must tile the lines exactly: no line uncovered, none twice
    cover = [ln for a, b, _, _ in scenes for ln in range(a, b + 1)]
    assert cover == list(range(len(LINES))), "scene plan does not tile the script"

    out, caps, uses = [], [], {}
    for n, (a, b, kind, o) in enumerate(scenes):
        s0 = 0.0 if n == 0 else t(a) - 0.12
        s1 = END if n == len(scenes) - 1 else t(scenes[n + 1][0]) - 0.12
        c = Ctx(n, a, b, s0, s1)
        for k in ("clip", "photo"):
            if o.get(k):
                uses[o[k]] = uses.get(o[k], 0) + 1
        bg, media = plate(c, o)
        body = KINDS[kind](c, o)
        if o.get("clip") and c.d > 5.2:
            print(f"  ! scene {n} clip {o['clip']} runs {c.d:.1f}s > 5s source", file=sys.stderr)
        out.append(
            f'<div class="clip scene" id="s{n}" data-start="{s0:.3f}" data-duration="{c.d:.3f}" '
            f'data-track-index="1"><div class="layer"><div class="bgmove" id="bm{n}" '
            f'data-layout-allow-overflow>{bg}</div><div class="grain"></div><div class="vig{" soft" if media else ""}"></div></div>'
            f'<div class="mm" id="mm{n}"><div class="mm2" id="mi{n}">{body}</div></div></div>')
        c.js.insert(0, f'SC.push([{n},{s0:.3f},{c.d:.3f},{1 if media else 0}]);')
        P_JS.extend(c.js)
        for ln in range(a, b + 1):
            if ln in c.nocap or ln in o.get("nocap", []):
                continue
            ta, tb = TIMES[ln]
            tb = t(ln + 1) - 0.05 if ln + 1 < len(LINES) else tb + 0.4
            cards = build.caption_cards(LINES[ln].replace('"', ""))
            per = (tb - ta) / len(cards)
            for j, card in enumerate(cards):
                caps.append((ta + j * per, per, card))

    over = [k for k, v in uses.items() if v > 2]
    assert not over, f"assets used more than twice: {over}"

    cap_html = []
    for j, (cs, cd, card) in enumerate(caps):
        cap_html.append(f'<div class="clip" id="cap{j}" data-start="{cs:.3f}" data-duration="{cd:.3f}" '
                        f'data-track-index="2"><div class="cap-wrap"><div class="cap-scrim" '
                        f'data-layout-allow-overflow></div><div class="cap">{esc(card)}</div></div></div>')

    css = (open(os.path.join(HERE, "style.css"), encoding="utf-8").read() + "\n" +
           open(os.path.join(HERE, "style_v2.css"), encoding="utf-8").read())
    audio_tag = f'\n<audio id="vo" src="{audio}" data-start="0" data-duration="{TOTAL:.3f}"></audio>' if audio else ""
    doc = f"""<!doctype html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width={W}, height={H}">
<script src="vendor/gsap.min.js"></script>
<style>
{css}
</style>
</head>
<body>
<div id="root" data-composition-id="main" data-width="{W}" data-height="{H}" data-start="0" data-duration="{TOTAL:.3f}">
{chr(10).join(out)}
{chr(10).join(cap_html)}
<div class="clip" id="wmclip" data-start="0" data-duration="{TOTAL:.3f}" data-track-index="3"><div class="wm">이다사</div></div>{audio_tag}
</div>
<script>
var tl = gsap.timeline({{ paused: true }});
var SC = [];
var L = {json.dumps([round(a, 3) for a, _ in TIMES])};
{chr(10).join(P_JS)}

// every scene: settle on entry, then keep breathing so no frame is dead still
SC.forEach(function (s) {{
  var n = s[0], t0 = s[1], d = s[2];
  tl.fromTo("#mm" + n, {{ opacity: 0, scale: 1.03 }}, {{ opacity: 1, scale: 1, duration: 0.55, ease: "power3.out" }}, t0);
  tl.fromTo("#mi" + n, {{ scale: 1, y: 0 }}, {{ scale: 1.022, y: -8, duration: Math.max(1, d), ease: "sine.inOut" }}, t0);
  var dir = (n % 2) ? 1 : -1;
  tl.fromTo("#bm" + n, {{ scale: s[3] ? 1.02 : 1.0, xPercent: 0 }},
            {{ scale: s[3] ? 1.075 : 1.045, xPercent: dir * 1.1, duration: Math.max(1, d), ease: "sine.inOut" }}, t0);
}});

// narration-synced beats: a node enters when its line starts
document.querySelectorAll("[data-l]").forEach(function (el) {{
  var at = L[+el.getAttribute("data-l")] + (+el.getAttribute("data-d") || 0);
  var fx = el.getAttribute("data-fx");
  if (fx === "up") tl.fromTo(el, {{ opacity: 0, y: 30 }}, {{ opacity: 1, y: 0, duration: 0.5, ease: "power3.out" }}, at);
  else if (fx === "left") tl.fromTo(el, {{ opacity: 0, x: -44 }}, {{ opacity: 1, x: 0, duration: 0.5, ease: "power3.out" }}, at);
  else if (fx === "pop") tl.fromTo(el, {{ opacity: 0, scale: 0.86 }}, {{ opacity: 1, scale: 1, duration: 0.5, ease: "back.out(1.5)" }}, at);
  else if (fx === "fade") tl.fromTo(el, {{ opacity: 0 }}, {{ opacity: 1, duration: 0.6, ease: "power1.out" }}, at);
  else if (fx === "strike") tl.fromTo(el, {{ scaleX: 0 }}, {{ scaleX: 1, duration: 0.45, ease: "power2.out" }}, at);
  else if (fx === "draw") {{
    var len = +el.getAttribute("data-len");
    tl.fromTo(el, {{ strokeDashoffset: len }}, {{ strokeDashoffset: 0, duration: +el.getAttribute("data-dur") || 1, ease: "power2.inOut" }}, at);
  }}
}});

// floating objects drift on a slow sine
document.querySelectorAll(".float").forEach(function (el, k) {{
  var sc = el.closest(".scene"), t0 = +sc.getAttribute("data-start"), d = +sc.getAttribute("data-duration");
  var reps = Math.max(0, Math.floor(d / 1.8) - 1);
  tl.fromTo(el, {{ y: 0, rotation: -1.2 }}, {{ y: -14, rotation: 1.2, duration: 1.8, ease: "sine.inOut", yoyo: true, repeat: reps }}, t0 + 0.3);
}});

// captions: one line, fading up at their own start
document.querySelectorAll(".cap").forEach(function (el) {{
  var st = +el.closest(".clip").getAttribute("data-start");
  tl.fromTo(el, {{ opacity: 0, y: 12 }}, {{ opacity: 1, y: 0, duration: 0.2, ease: "power2.out" }}, st);
}});

window.__timelines = window.__timelines || {{}};
window.__timelines["main"] = tl;
</script>
</body>
</html>
"""
    if "--range" in sys.argv:
        k = sys.argv.index("--range")
        doc = cut_range(doc, float(sys.argv[k + 1]), float(sys.argv[k + 2]))
    open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8").write(doc)
    json.dump(sorted(SFX, key=lambda s: s["t"]), open(os.path.join(PROJ, "sfx.json"), "w"), indent=0)
    print(f"wrote index.html  {TOTAL:.1f}s · {len(scenes)} scenes · {len(caps)} captions · {len(SFX)} sfx")
    print("  media uses:", {k: v for k, v in sorted(uses.items())})


P_JS = []


def cut_range(doc, a, b):
    """Rewrite the composition to cover only [a, b) of the film.

    The sandbox kills background work after ~15 min, so a long film renders
    as segments that are concatenated afterwards. Every timed element is
    shifted by -a (media that starts before a skips ahead with
    data-media-start), elements outside the window are dropped, and the
    registered timeline becomes a scrubber that plays the full timeline from
    a to b — so every tween lands exactly where it would in the full render.
    """
    b = min(b, TOTAL)

    def shift(m):
        tag, st, du, rest = m.group(1), float(m.group(2)), float(m.group(3)), m.group(4)
        s0, s1 = max(st, a), min(st + du, b)
        if s1 <= s0 and "<video" in tag:
            return f'{tag} data-start="PARK"{rest}'     # removed below
        if s1 <= s0:
            # parked past the segment end: never shown, DOM left intact
            return f'{tag} data-start="{b - a + 5:.3f}" data-duration="0.001"{rest}'
        extra = ""
        if st < a and "<video" in tag:
            ms = re.search(r'data-media-start="([\d.]+)"', rest)
            base = float(ms.group(1)) if ms else 0.0
            rest = re.sub(r' data-media-start="[\d.]+"', "", rest)
            extra = f' data-media-start="{base + a - st:.3f}"'
        return f'{tag} data-start="{s0 - a:.3f}" data-duration="{s1 - s0:.3f}"{extra}{rest}'

    doc = re.sub(r'(<(?:div|video|audio)[^>]*?) data-start="([\d.]+)" data-duration="([\d.]+)"([^>]*>)', shift, doc)
    # a parked <video> still gets its frames extracted (and fails the
    # coverage gate), so media outside the window is dropped outright
    doc = re.sub(r'<video[^>]*data-start="PARK"[^>]*></video>', "", doc)
    doc = doc.replace('window.__timelines["main"] = tl;',
                      f'var seg = gsap.timeline({{ paused: true }});\n'
                      f'seg.add(tl.tweenFromTo({a:.3f}, {b:.3f}, {{ ease: "none" }}), 0);\n'
                      'window.__timelines["main"] = seg;')
    return doc

if __name__ == "__main__":
    main()
