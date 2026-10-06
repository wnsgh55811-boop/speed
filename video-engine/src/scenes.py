# -*- coding: utf-8 -*-
"""Scene-based composition builder.

`emit.py` maps ONE scene to ONE narration line, which suited a TTS assembled
line by line. A single recorded take (e.g. a Fish Audio export) reads faster
and its lines are often under a second, so here a scene spans a run of lines
and the things inside it ("beats") arrive on the line they belong to.

    python3 src/scenes.py projects/<name>

The project folder holds
    plan.py         SCENES = [dict(a=<first line>, kind=..., bg=..., ...)]
    timings.json    [{i, s, e, t}]  per spoken line, cut against the voice
    assets.json     {key: url}      fetched into assets/img by fetch_assets.py
and the build writes <project>/index.html.

Beat timing: an int `at` is a line index (that line's onset), a float is
seconds after the scene starts. Every timed element carries data-at/data-fx
and one generic GSAP pass brings it in — so the motion follows the voice.

Reuses: style.css (design system), emit.picto (pictograms), build.caption_cards
(measured one-line captions), build.FAMILIES/motes (background rotation).
"""
import html
import importlib.util
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build                                                    # noqa: E402
from build import W, H, FAMILIES, motes, text_w, font          # noqa: E402
from emit import picto                                          # noqa: E402

esc = lambda s: html.escape(s, quote=True)                      # noqa: E731

CAP_PX, CAP_MAX = 50, 1640
build.CAP_PX, build.CAP_MAX = CAP_PX, CAP_MAX


class Ctx:
    """Per-scene context: resolves `at` values and hands out element ids."""

    def __init__(self, sid, t0, t1, st):
        self.sid, self.t0, self.t1, self.st, self.n = sid, t0, t1, st, 0

    def t(self, at):
        if at is None:
            return self.t0 + 0.1
        if isinstance(at, int):
            return max(self.t0, self.st[at] - 0.06)
        if isinstance(at, tuple):          # (line, seconds after that line starts)
            return max(self.t0, self.st[at[0]] + at[1])
        return self.t0 + at

    def a(self, at, fx="up"):
        """Attribute string for a timed element."""
        self.n += 1
        if not (self.t0 - 0.01 <= self.t(at) < self.t1 - 0.2):
            print(f"  ! {self.sid} beat {self.n} at={at!r} -> {self.t(at):.2f}s "
                  f"outside scene [{self.t0:.2f}, {self.t1:.2f})", file=sys.stderr)
        return f'id="{self.sid}-b{self.n}" data-at="{self.t(at):.2f}" data-fx="{fx}"'


def img(key, cls="", style=""):
    return f'<img class="{cls}" src="assets/img/{key}.png" alt="" style="{style}">'


def cut(key, cls="", style=""):
    return f'<img class="{cls}" src="assets/cut/{key}.png" alt="" style="{style}">'


# ── components ─────────────────────────────────────────────────────────────
def c_hook(c, quote, at_quote, kicker=None):
    """Cold open: the plate is already live on frame 0, a thought bubble types,
    then the line the voice is about to say lands big."""
    # frame 0 is already composed: shade, bubble and dots are on screen, no fade-in
    h = ['<div class="hook-shade"></div><div class="stage hook">']
    if kicker:
        h.append(f'<div class="kicker hook-k">{esc(kicker)}</div>')
    h.append('<div class="think-bub">'
             '<i class="tdot"></i><i class="tdot"></i><i class="tdot"></i></div>')
    rows = "".join(f'<span class="hq">{esc(x)}</span>' for x in quote.split("|"))
    h.append(f'<div class="hook-q" {c.a(at_quote, "slam")}>{rows}</div>')
    h.append("</div>")
    return "".join(h)


def c_checklist(c, title, items, empty_at=None, empty_text="…다음은?"):
    h = ['<div class="stage"><div class="scrim wide"></div>']
    if title:
        h.append(f'<div class="hl md gtitle" {c.a(None)}>{esc(title)}</div>')
    h.append('<div class="checks">')
    for txt, at in items:
        h.append(f'<div class="chk" {c.a(at, "left")}><i class="box">'
                 f'<svg viewBox="0 0 40 40"><path class="tickpath" pathLength="1" '
                 f'd="M9 21l8 8 15-17"/></svg></i><span>{esc(txt)}</span></div>')
    h.append("</div>")
    if empty_at is not None:
        h.append(f'<div class="sub dimmed" {c.a(empty_at, "fade")}>{esc(empty_text)}</div>')
    h.append("</div>")
    return "".join(h)


def c_meter(c, title, start, end, at, left="적음", right="많음", tone="cyan",
            label=None, steps=5, at_label=None, then=None):
    """A horizontal gauge whose fill moves from `start` to `end` on cue."""
    ticks = "".join(f'<span class="mtick" style="left:{q}%"><b>{k + 1}</b></span>'
                    for k, q in enumerate(range(0, 101, 100 // (steps - 1))))
    return "".join([
        '<div class="stage"><div class="scrim wide"></div>',
        f'<div class="hl md gtitle" {c.a(None)}>{esc(title)}</div>',
        f'<div class="meter" {c.a(None, "fade")}>',
        f'<div class="m-ticks">{ticks}</div>',
        f'<div class="m-track">'
        f'<i class="m-fill {tone}" data-from="{start}" data-to="{end}" '
        + (f'data-then="{then[0]}" data-then-at="{c.t(then[1]):.2f}" ' if then else "")
        + f'{c.a(at, "meter")}></i></div>',
        f'<div class="bar-axis"><span>{esc(left)}</span><span>{esc(right)}</span></div>',
        '</div>',
        (f'<div class="sub" {c.a(at if at_label is None else at_label, "fade")}>{esc(label)}</div>' if label else ""),
        '</div>'])


def c_chat(c, msgs, title=None, icon=None, xout=None):
    """Spoken lines as a chat thread. m = 남자 (right, yellow), w = 여자 (left).
    icon = a 3D icon key shown beside the title; xout = at which an X lands
    over the whole thread (questions you would never ask a friend)."""
    h = ['<div class="stage"><div class="chat">']
    if icon:
        h.append(f'<div class="chat-icon" {c.a(None, "pop")}>{img(icon, "icon3d floaty")}</div>')
    if title:
        h.append(f'<div class="chat-title" {c.a(None, "fade")}>{esc(title)}</div>')
    for m in msgs:
        who, txt, at = m[0], m[1], m[2]
        tag = m[3] if len(m) > 3 else None
        cls = "me" if who == "m" else "her"
        lines = "".join(f'<span class="bl">{esc(x)}</span>' for x in txt.split("|"))
        tg = f'<span class="btag">{esc(tag)}</span>' if tag else ""
        h.append(f'<div class="msg {cls}" {c.a(at, "msg")}>'
                 f'<div class="bubble">{lines}</div>{tg}</div>')
    if xout is not None:
        h.append(f'<svg class="xmark chat-x" {c.a(xout, "pop")} viewBox="0 0 100 100"><line x1="16" y1="16" '
                 'x2="84" y2="84"/><line x1="16" y1="84" x2="84" y2="16"/></svg>')
    h.append("</div></div>")
    return "".join(h)


def c_lines(c, title, series, xlab, ylab):
    """Conceptual line chart: axes first, then each series draws on its cue.
    series = [(label, svg path d, tone, at)] on a 1000x460 plot."""
    h = ['<div class="stage"><div class="scrim wide"></div>',
         f'<div class="hl md gtitle" {c.a(None)}>{esc(title)}</div>',
         '<svg class="chart" width="1160" height="560" viewBox="-110 -30 1160 560">',
         f'<g {c.a(0.15, "fade")}>'
         '<path class="axis" d="M0 0 V460 H1000"/>'
         + "".join(f'<path class="grid" d="M0 {y} H1000"/>' for y in (115, 230, 345)) +
         f'<text class="axl" x="1000" y="510" text-anchor="end">{esc(xlab)} →</text>'
         f'<text class="axl" x="-24" y="10" text-anchor="end">{esc(ylab)}</text>'
         '<text class="axl" x="-24" y="465" text-anchor="end">낮음</text>'
         '<text class="axl" x="-24" y="125" text-anchor="end">높음</text></g>']
    for lab, d, tone, at, lx, ly in series:
        h.append(f'<path class="sline {tone}" pathLength="1" d="{d}" {c.a(at, "draw")}/>')
        anc = "end" if lx > 900 else "start"
        h.append(f'<text class="slab {tone}" x="{lx}" y="{ly}" text-anchor="{anc}" {c.a(at + 0.9 if isinstance(at, float) else at, "fade")}>{esc(lab)}</text>')
    h.append("</svg></div>")
    return "".join(h)


def c_icon(c, key, title, sub=None, at_sub=None, orbit=False, size=560, xmark=False,
           at_x=None, side=None, waterline=30, shake=None, flash=None, at_title=None):
    """shake = at which the icon starts ringing; flash = at which a white wash
    blanks the frame (a mind going blank)."""
    cls = "icon3d" + (" floaty" if not orbit and shake is None else "") + (" shaky" if shake is not None else "")
    fl = (f'<i class="whiteout" {c.a(flash, "flash")}></i>' if flash is not None else "")
    sk = (f' data-shake-at="{c.t(shake):.2f}"' if shake is not None else "")
    o = (f'<svg class="orbit" style="--wl:{waterline}%" viewBox="0 0 600 220"><ellipse cx="300" cy="110" rx="290" ry="70"/>'
         '<circle class="orb" r="12" cx="590" cy="110"/></svg>') if orbit else ""
    x = (f'<svg class="xmark" {c.a(at_x, "pop")} viewBox="0 0 100 100"><line x1="16" y1="16" '
         'x2="84" y2="84"/><line x1="16" y1="84" x2="84" y2="16"/></svg>') if xmark else ""
    if side:
        return "".join([
            '<div class="stage row-stage"><div class="scrim wide"></div>',
            f'<div class="icon-wrap"{sk} {c.a(None, "pop")}>{img(key, cls, f"width:{size}px")}{o}{x}</div>',
            '<div class="side-txt">',
            f'<div class="hl lg left" {c.a(0.25 if at_title is None else at_title)}>{esc(title)}</div>',
            (f'<div class="sub left" {c.a(at_sub)}>{esc(sub)}</div>' if sub else ""),
            '</div></div>', fl])
    return "".join([
        '<div class="stage"><div class="scrim tight"></div>',
        f'<div class="icon-wrap"{sk} {c.a(None, "pop")}>{img(key, cls, f"width:{size}px")}{o}{x}</div>',
        f'<div class="hl md" style="margin-top:6px" {c.a(0.3 if at_title is None else at_title)}>{esc(title)}</div>',
        (f'<div class="sub" {c.a(at_sub)}>{esc(sub)}</div>' if sub else ""),
        '</div>', fl])


def c_typo(c, rows, strike=None, kicker=None):
    """rows = [(text, at, cls)]; strike = (row, at) or [(row, at), ...] puts a
    line through those rows; kicker = (text, at) sits small above them."""
    strikes = dict([strike] if isinstance(strike, tuple) else (strike or []))
    h = ['<div class="stage"><div class="scrim wide"></div>']
    if kicker:
        h.append(f'<div class="kicker" {c.a(kicker[1], "fade")}>{esc(kicker[0])}</div>')
    for k, (txt, at, cls) in enumerate(rows):
        s = ""
        if k in strikes:
            s = f'<i class="strike-line" {c.a(strikes[k], "strike")}></i>'
        h.append(f'<div class="hl {cls} tline" {c.a(at, "rise")}><span class="tl-in">{esc(txt)}{s}</span></div>')
    h.append("</div>")
    return "".join(h)


def c_depth(c, title, levels, top="표면", bottom="깊이", marker_to=None):
    """A vertical depth scale. levels = [(label, at)], shallow → deep; a probe
    dot drops to each level as it is named."""
    n = len(levels)
    h = ['<div class="stage"><div class="scrim wide"></div>',
         f'<div class="hl md gtitle" {c.a(None)}>{esc(title)}</div>',
         '<div class="depth">',
         f'<div class="d-axis" {c.a(None, "fade")}><span>{esc(top)}</span><i></i><span>{esc(bottom)}</span></div>',
         '<div class="d-levels">',
         '<div class="d-surface"></div>']
    for k, (lab, at) in enumerate(levels):
        h.append(f'<div class="d-lv" style="--k:{k}" {c.a(at, "left")}>'
                 f'<i class="d-dot" style="opacity:{0.45 + 0.55 * (k + 1) / n:.2f}"></i>'
                 f'<span>{esc(lab)}</span></div>')
    h.append("</div></div></div>")
    return "".join(h)


def c_cards(c, cards, title=None, vs=False):
    """Side-by-side cards. card = dict(n, head, body, at, photo, tone)."""
    h = ['<div class="stage"><div class="scrim wide"></div>']
    if title:
        h.append(f'<div class="hl md gtitle" {c.a(None)}>{esc(title)}</div>')
    h.append('<div class="cards">')
    for k, cd in enumerate(cards):
        if vs and k:
            h.append(f'<div class="vs" {c.a(cd.get("at"), "fade")}>vs</div>')
        ph = (f'<div class="card-ph">{img(cd["photo"])}</div>' if cd.get("photo") else "")
        num = f'<span class="card-n">{esc(cd["n"])}</span>' if cd.get("n") else ""
        body = f'<div class="card-b">{esc(cd["body"])}</div>' if cd.get("body") else ""
        h.append(f'<div class="card {cd.get("tone", "")}" {c.a(cd.get("at"), "up")}>{ph}'
                 f'<div class="card-t">{num}<div class="card-h">{esc(cd["head"])}</div>{body}</div></div>')
    h.append("</div></div>")
    return "".join(h)


def c_chapter(c, num, word, sub=None):
    return "".join([
        '<div class="stage"><div class="scrim"></div>',
        f'<div class="pearl" {c.a(None, "pop")}>{esc(num)}</div>',
        f'<div class="chap-word" {c.a(0.25, "rise")}>{esc(word)}</div>',
        (f'<div class="sub" {c.a(0.55)}>{esc(sub)}</div>' if sub else ""),
        '</div>'])


def c_morph(c, x, y, at_y, title=None, op="→", note=None, at_note=None):
    return "".join([
        '<div class="stage"><div class="scrim wide"></div>',
        (f'<div class="hl md gtitle" {c.a(None)}>{esc(title)}</div>' if title else ""),
        '<div class="morph">',
        f'<span class="mchip from" {c.a(None, "pop")}>{esc(x)}</span>',
        f'<span class="mop" {c.a(at_y, "fade")}>{esc(op)}</span>',
        f'<span class="mchip to" {c.a(at_y, "pop")}>{esc(y)}</span>',
        '</div>',
        (f'<div class="sub" {c.a(at_note)}>{esc(note)}</div>' if note else ""),
        '</div>'])


def c_tree(c, root, branches, root_at=None):
    """root node with branches [(label, photo|None, at)] fanning out."""
    n = len(branches)
    xs = [960 + (k - (n - 1) / 2) * 560 - 240 for k in range(n)]   # leaf left edges
    paths = "".join(
        f'<path class="tedge" pathLength="1" d="M960 210 C960 300 {x+240:.0f} 260 {x+240:.0f} 360" '
        f'{c.a(at, "draw")}/>' for x, (_, _, at) in zip(xs, branches))
    nophoto = all(ph is None for _, ph, _ in branches)
    h = [f'<div class="stage tree-stage{" nophoto" if nophoto else ""}"><div class="scrim wide"></div>',
         f'<svg class="tree-svg" viewBox="0 0 1920 1080">{paths}</svg>',
         f'<div class="troot" {c.a(root_at, "pop")}>{esc(root)}</div>']
    for x, (lab, ph, at) in zip(xs, branches):
        inner = (f'<div class="tph">{img(ph)}</div>' if ph else "")
        h.append(f'<div class="tleaf" style="left:{x:.0f}px" {c.a(at, "up")}>{inner}'
                 f'<div class="tlab">{esc(lab)}</div></div>')
    h.append("</div>")
    return "".join(h)


def c_sliders(c, title, rows):
    """Spectrum sliders. rows = [(left, right, pos 0..1, at)] — the knob slides
    to where her answer points, the end it lands on lights up."""
    h = ['<div class="stage"><div class="scrim wide"></div>',
         f'<div class="hl md gtitle" {c.a(None)}>{esc(title)}</div>', '<div class="sliders">']
    for left, right, pos, at in rows:
        h.append(f'<div class="sld" {c.a(at, "left")}>'
                 f'<span class="sl-l">{esc(left)}</span>'
                 f'<div class="sl-track"><i class="sl-knob" data-pos="{pos}" {c.a(at + 0.35 if isinstance(at, float) else at, "knob")}></i></div>'
                 f'<span class="sl-r">{esc(right)}</span></div>')
    h.append("</div></div>")
    return "".join(h)


def c_person(c, key, bubbles, side="left", think=False, head=None):
    """Torn-paper cutout with spoken bubbles beside it. bubbles = [(text, at)].
    head = (text, at) — a small kicker above the bubbles."""
    h = [f'<div class="person {side}">',
         f'<div class="p-fig" {c.a(None, "rise")}>{cut(key, "paper")}</div>',
         '<div class="p-bubs">']
    if head:
        h.append(f'<div class="kicker p-head" {c.a(head[1], "fade")}>{esc(head[0])}</div>')
    for txt, at in bubbles:
        cls = "pb think" if think else "pb"
        lines = "".join(f'<span class="bl">{esc(x)}</span>' for x in txt.split("|"))
        h.append(f'<div class="{cls}" {c.a(at, "msg")}>{lines}</div>')
    h.append("</div></div>")
    return "".join(h)


def c_flow(c, items, title=None, foot=None, at_foot=None, loop=False):
    """A chain of chips with arrows, each arriving on its cue."""
    h = ['<div class="stage"><div class="scrim wide"></div>']
    if title:
        h.append(f'<div class="hl md gtitle" {c.a(None)}>{esc(title)}</div>')
    h.append('<div class="flow">')
    for k, (txt, at, tone) in enumerate(items):
        if k:
            h.append(f'<span class="farrow" {c.a(at, "fade")}>›</span>')
        h.append(f'<span class="fchip {tone}" {c.a(at, "pop")}>{esc(txt)}</span>')
    if loop:
        h.append(f'<span class="farrow loop" {c.a(items[-1][1], "fade")}>↻</span>')
    h.append("</div>")
    if foot:
        h.append(f'<div class="sub" {c.a(at_foot)}>{esc(foot)}</div>')
    h.append("</div>")
    return "".join(h)


def c_distance(c, title, gap_from, gap_to, at, left="나", right="상대", note=None,
               at_note=None, chatter=False):
    """Two people and the space between them; the gap changes on cue.
    chatter=True sends message dots back and forth while the gap holds."""
    dots = ("".join(f'<i class="chat-dot" style="--k:{k}"></i>' for k in range(5))
            if chatter else "")
    return "".join([
        '<div class="stage"><div class="scrim wide"></div>',
        f'<div class="hl md gtitle" {c.a(None)}>{esc(title)}</div>',
        f'<div class="dist" data-from="{gap_from}" data-to="{gap_to}" {c.a(at, "gap")} '
        f'style="--gap:{gap_from}px" data-gap="{gap_to}">',
        f'<div class="dp">{picto("self", 150)}<span>{esc(left)}</span></div>',
        f'<div class="dline"><i class="dl"></i>{dots}</div>',
        f'<div class="dp her">{picto("self", 150)}<span>{esc(right)}</span></div>',
        '</div>',
        (f'<div class="sub" {c.a(at_note)}>{esc(note)}</div>' if note else ""),
        '</div>'])


def c_scale(c, title, left, right, tilt_at, level_at=None, left_items=3):
    """Balance scale: tips toward `left` on cue, levels out on `level_at`."""
    blocks = "".join(f'<i class="blk" style="--k:{k}" {c.a(tilt_at, "fade")}></i>'
                     for k in range(left_items))
    blocks_r = "".join(f'<i class="blk r" style="--k:{k}" {c.a(level_at, "fade")}></i>'
                       for k in range(left_items)) if level_at is not None else ""
    lv = f'data-level-at="{c.t(level_at):.2f}"' if level_at is not None else ""
    return "".join([
        '<div class="stage"><div class="scrim wide"></div>',
        f'<div class="hl md gtitle" {c.a(None)}>{esc(title)}</div>',
        f'<div class="scale" {c.a(tilt_at, "tilt")} {lv}>',
        '<div class="beam">',
        f'<div class="pan l"><div class="stackb">{blocks}</div><span>{esc(left)}</span></div>',
        f'<div class="pan r"><div class="stackb">{blocks_r}</div><span>{esc(right)}</span></div>',
        '</div><i class="post"></i><i class="base"></i></div></div>'])


def c_rows(c, title, rows, arrow=True):
    """cause → effect rows. rows = [(cause, effect, at_cause, at_effect)]."""
    h = ['<div class="stage"><div class="scrim wide"></div>']
    if title:
        h.append(f'<div class="hl md gtitle" {c.a(None)}>{esc(title)}</div>')
    h.append('<div class="crow-wrap">')
    for a, b, ta, tb in rows:
        h.append(f'<div class="crow"><span class="ca" {c.a(ta, "left")}>{esc(a)}</span>'
                 + (f'<span class="carr" {c.a(tb, "fade")}>→</span>' if arrow else "")
                 + f'<span class="cb" {c.a(tb, "left")}>{esc(b)}</span></div>')
    h.append("</div></div>")
    return "".join(h)


def c_toggle(c, q1, q2, at_q1, at_q2, lead=None):
    return "".join([
        '<div class="stage"><div class="scrim wide"></div>',
        (f'<div class="kicker" {c.a(None, "fade")}>{esc(lead)}</div>' if lead else ""),
        '<div class="tog">',
        f'<div class="tq q1" {c.a(at_q1, "left")}><i class="radio"></i><span>{esc(q1)}</span></div>',
        f'<div class="tq q2" {c.a(at_q2, "left")}><i class="radio on"></i><span>{esc(q2)}</span></div>',
        f'<i class="tq-dim" {c.a(at_q2, "dim")}></i>',
        '</div></div>'])


def c_cards10(c, title, count, at, stamp, at_stamp, key="ico_cards"):
    return "".join([
        '<div class="stage"><div class="scrim wide"></div>',
        f'<div class="hl md gtitle" {c.a(None)}>{esc(title)}</div>',
        '<div class="c10">',
        f'<div class="icon-wrap" {c.a(None, "pop")}>{img(key, "icon3d", "width:420px")}</div>',
        f'<div class="c10-n" data-count="{count}" {c.a(at, "count")}>0</div>',
        f'<div class="stamp" {c.a(at_stamp, "stamp")}>{esc(stamp)}</div>',
        '</div></div>'])


def c_cta(c, head, sub, at_sub, foot=None, at_foot=None):
    return "".join([
        '<div class="stage"><div class="cta-card" ' + c.a(None, "up") + '>',
        '<div class="cta-badge">PRIVATE</div>',
        f'<div class="cta-h">{esc(head)}</div>',
        f'<div class="cta-s" {c.a(at_sub, "fade")}>{esc(sub)}</div>',
        '</div>',
        (f'<div class="cta-foot" {c.a(at_foot, "up")}><span class="cta-arrow">↓</span>{esc(foot)}</div>'
         if foot else ""),
        '</div>'])


# ── components added for 스몰토크 ───────────────────────────────────────────
def c_photo(c, quote=None, at_quote=None, who="m", chip=None, at_chip=None, pos="low"):
    """The photo is the plate (bg="photo:key"); on top, either a spoken line as
    a bubble or a short label chip. pos = low | high (keep faces clear)."""
    h = [f'<div class="stage photo-stage {pos}">']
    if chip:
        h.append(f'<div class="ph-chip" {c.a(at_chip, "pop")}>{esc(chip)}</div>')
    if quote:
        lines = "".join(f'<span class="bl">{esc(x)}</span>' for x in quote.split("|"))
        h.append(f'<div class="msg {"me" if who == "m" else "her"} ph-msg" {c.a(at_quote, "msg")}>'
                 f'<div class="bubble">{lines}</div></div>')
    h.append("</div>")
    return "".join(h)


def c_timer(c, title, secs, at, label=None, at_label=None, tone="amber"):
    """A countdown ring that really runs `secs` seconds while the digit counts."""
    return "".join([
        '<div class="stage"><div class="scrim wide"></div>',
        f'<div class="hl md gtitle" {c.a(None)}>{esc(title)}</div>',
        f'<div class="timer {tone}" data-secs="{secs}" {c.a(at, "timer")}>',
        '<svg viewBox="0 0 300 300"><circle class="t-bg" cx="150" cy="150" r="126"/>',
        '<circle class="t-ring" cx="150" cy="150" r="126" pathLength="1"/>',
        ''.join(f'<line class="t-tick" x1="150" y1="14" x2="150" y2="34" transform="rotate({k*30} 150 150)"/>' for k in range(12)),
        '</svg><div class="t-num">0.0<small>초</small></div></div>',
        (f'<div class="sub" {c.a(at_label, "fade")}>{esc(label)}</div>' if label else ""),
        '</div>'])


def c_search(c, query, at_query, results, title=None):
    """A search bar typing the query, then results dropping in one by one."""
    h = ['<div class="stage"><div class="scrim wide"></div>']
    if title:
        h.append(f'<div class="kicker" {c.a(None, "fade")}>{esc(title)}</div>')
    h.append(f'<div class="search" {c.a(None, "up")}><svg class="s-ic" viewBox="0 0 40 40">'
             '<circle cx="17" cy="17" r="11"/><path d="M25 25l9 9"/></svg>'
             f'<span class="s-q" {c.a(at_query, "type")}>{esc(query)}</span><i class="s-caret"></i></div>')
    h.append('<div class="s-res">')
    for txt, at in results:
        h.append(f'<div class="s-row" {c.a(at, "left")}><i class="s-dot"></i><span>{esc(txt)}</span></div>')
    h.append("</div></div>")
    return "".join(h)


def c_bars(c, title, bars, at, axis=("짧음", "김"), note=None, at_note=None, tone="cyan", step=0.28):
    """Vertical bars that grow from zero to their value, one after another,
    on a 5-step scale. bars = [(label, value 0..1)]."""
    n = len(bars)
    h = ['<div class="stage"><div class="scrim wide"></div>',
         f'<div class="hl md gtitle" {c.a(None)}>{esc(title)}</div>',
         f'<div class="vbars" {c.a(0.1, "fade")}>',
         '<div class="vb-axis">' + "".join(f'<span style="bottom:{k*25}%"><b>{k+1}</b></span>' for k in range(5)) + '</div>',
         '<div class="vb-plot">',
         "".join(f'<i class="vb-grid" style="bottom:{k*25}%"></i>' for k in range(5))]
    t0 = c.t(at)
    for k, (lab, v) in enumerate(bars):
        hot = " hot" if k == n - 1 else ""
        h.append(f'<div class="vb"><i class="vb-fill {tone}{hot}" style="height:{v*100:.0f}%" '
                 f'id="{c.sid}-vb{k}" data-at="{t0 + k*step:.2f}" data-fx="grow"></i>'
                 f'<span class="vb-lab">{esc(lab)}</span></div>')
    h.append('</div>')
    h.append(f'<div class="vb-unit"><span>{esc(axis[1])}</span><span>{esc(axis[0])}</span></div>')
    h.append('</div>')
    if note:
        h.append(f'<div class="sub" {c.a(at_note, "fade")}>{esc(note)}</div>')
    h.append('</div>')
    return "".join(h)


def c_radial(c, key, items, title=None, foot=None, at_foot=None):
    """A 3D icon in the middle and what it notices placed around it; each
    spoke draws out as its item is named. items = [(text, at)]."""
    import math
    n = len(items)
    cx, cy, rx, ry = 960, 500, 600, 250
    pts = [(cx + rx * math.cos(-math.pi / 2 + 2 * math.pi * k / n),
            cy + ry * math.sin(-math.pi / 2 + 2 * math.pi * k / n)) for k in range(n)]
    sp = "".join(f'<path class="spoke" pathLength="1" d="M{cx} {cy} L{x:.0f} {y:.0f}" {c.a(at, "draw")}/>'
                 for (x, y), (_, at) in zip(pts, items))
    h = ['<div class="stage radial"><div class="scrim wide"></div>',
         f'<svg class="tree-svg" viewBox="0 0 1920 1080">{sp}</svg>']
    if title:
        h.append(f'<div class="kicker rad-title" {c.a(None, "fade")}>{esc(title)}</div>')
    h.append(f'<div class="rad-ic" {c.a(None, "pop")}>{img(key, "icon3d floaty", "width:300px")}</div>')
    for (x, y), (txt, at) in zip(pts, items):
        h.append(f'<div class="rad-chip" style="left:{x:.0f}px;top:{y:.0f}px" {c.a(at, "pop")}>{esc(txt)}</div>')
    if foot:
        h.append(f'<div class="rad-foot sub" {c.a(at_foot, "fade")}>{esc(foot)}</div>')
    h.append("</div>")
    return "".join(h)


def c_stamp(c, title, stamp, at_stamp, at_title=None):
    return "".join([
        '<div class="stage"><div class="scrim"></div>',
        f'<div class="hl lg" {c.a(at_title)}>{esc(title)}</div>',
        f'<div class="stamp big" {c.a(at_stamp, "stamp")}>{esc(stamp)}</div>',
        '</div>'])


COMP = {k[2:]: v for k, v in globals().items() if k.startswith("c_")}


# ── backgrounds ─────────────────────────────────────────────────────────────
def background(k, bg, prev):
    """bg = family name, 'photo:key' (full plate) or 'soft:key' (dim plate
    behind a graphic). Returns (css class, inner html, family tag)."""
    if bg and bg.startswith(("photo:", "soft:")):
        mode, key = bg.split(":", 1)
        return (f"bg-photo {mode}", f'<img src="assets/img/{key}.png" alt=""><div class="tint"></div>',
                "photo")
    fam = bg or FAMILIES[k % len(FAMILIES)]
    if len(prev) >= 2 and fam == prev[-1] == prev[-2]:
        fam = FAMILIES[(FAMILIES.index(fam) + 3) % len(FAMILIES)]
    inner = f'<div class="motes">{motes(k)}</div>' if fam == "bg-dust" else ""
    return fam, inner, fam


# ── captions ────────────────────────────────────────────────────────────────
def caption_cards(tl, mute):
    """Merge very short spoken lines into one-line cards; split long ones.
    Returns [(start, end, text)]. Lines in `mute` are already on screen."""
    out, buf = [], []

    def flush():
        if not buf:
            return
        s, e = buf[0]["s"], buf[-1]["e"]
        # quote marks only make sense on screen when both ends are in one card
        txt = " ".join(x["t"] for x in buf).replace('"', "")
        parts = build.caption_cards(txt)
        per = (e - s) / len(parts)
        for j, p in enumerate(parts):
            out.append([s + j * per, s + (j + 1) * per, p])
        buf.clear()

    for ln in tl:
        if ln["i"] in mute:
            flush()
            continue
        if buf:
            trial = " ".join(x["t"] for x in buf + [ln])
            # never glue two sentences together: only continue an unfinished one
            ended = buf[-1]["t"].rstrip().endswith(("다", "요", "죠", "?", ".", "\"", "”", "까"))
            short = not ended and ((buf[-1]["e"] - buf[-1]["s"] < 1.05) or (ln["e"] - ln["s"] < 0.8))
            fits = text_w(trial, font(CAP_PX)) <= CAP_MAX
            if not (short and fits and ln["e"] - buf[0]["s"] <= 3.4):
                flush()
        buf.append(ln)
    flush()
    # close small gaps so a card holds until the next one starts
    for a, b in zip(out, out[1:]):
        if 0 < b[0] - a[1] < 0.45:
            a[1] = b[0]
    return out


# ── main ────────────────────────────────────────────────────────────────────
FPS = 30
PART_MAX = 46.0   # seconds per render part: keeps each capture light and short


def frame(t):
    return round(t * FPS) / FPS


def emit_doc(plan, tl, k0, k1, T0, T1, audio):
    """One composition for scenes k0..k1-1 on [T0, T1), times shifted by -T0."""
    st = [x["s"] - T0 for x in tl]
    scenes = plan.SCENES
    bg_html, fg_html, cap_html, sc_meta, prev = [], [], [], [], []
    for k in range(k0, k1):
        sc = scenes[k]
        t0 = 0.0 if k == k0 else frame(st[sc["a"]] - 0.06 + T0) - T0
        t1 = (T1 - T0) if k == k1 - 1 else frame(st[scenes[k + 1]["a"]] - 0.06 + T0) - T0
        sid = f"s{k:03d}"
        c = Ctx(sid, t0, t1, st)
        args = {x: v for x, v in sc.items() if x not in ("a", "kind", "bg", "mute")}
        body = COMP[sc["kind"]](c, **args)
        cls, inner, tag = background(k, sc.get("bg"), plan._bgprev[:k])
        d = t1 - t0
        bg_html.append(
            f'<div class="clip" id="bg{sid}" data-start="{t0:.3f}" data-duration="{d:.3f}" '
            f'data-track-index="0"><div class="layer"><div class="bgmove {cls}" id="bm{sid}" '
            f'data-layout-allow-overflow>{inner}</div></div></div>')
        fg_html.append(
            f'<div class="clip" id="{sid}" data-start="{t0:.3f}" data-duration="{d:.3f}" '
            f'data-track-index="1"><div class="fgin" id="fi{sid}">{body}</div></div>')
        sc_meta.append({"id": sid, "t": round(t0, 3), "d": round(d, 3), "ph": tag == "photo",
                        "first": k == 0, "last": k == len(scenes) - 1})
    n = 0
    for s, e, txt in plan._caps:
        if s >= T1 or e <= T0:
            continue
        cont = ' data-cont="1"' if s < T0 - 1e-6 else ""
        s, e = max(s, T0) - T0, min(e, T1) - T0
        if e - s < 0.05:
            continue
        cap_html.append(
            f'<div class="clip" id="cap{n:03d}"{cont} data-start="{s:.3f}" data-duration="{e - s:.3f}" '
            f'data-track-index="3"><div class="cap-wrap"><div class="cap-scrim" '
            f'data-layout-allow-overflow></div><div class="cap">{esc(txt)}</div></div></div>')
        n += 1
    dur = T1 - T0
    css = open(os.path.join(HERE, "style.css"), encoding="utf-8").read()
    css += open(os.path.join(HERE, "scenes.css"), encoding="utf-8").read()
    js = open(os.path.join(HERE, "scenes.js"), encoding="utf-8").read()
    audio_tag = (f'\n  <audio id="vo" src="{audio}" data-start="0" data-duration="{dur:.3f}" '
                 f'data-track-index="5"></audio>' if audio else "")
    return f"""<!doctype html>
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
<div id="root" data-composition-id="main" data-width="{W}" data-height="{H}"
     data-start="0" data-duration="{dur:.3f}">
{chr(10).join(bg_html)}
{chr(10).join(fg_html)}
  <div class="clip" id="ovl" data-start="0" data-duration="{dur:.3f}" data-track-index="2">
    <div class="ovl"><div class="grain"></div><div class="vig"></div></div>
  </div>
{chr(10).join(cap_html)}
  <div class="clip" id="wmclip" data-start="0" data-duration="{dur:.3f}" data-track-index="4">
    <div class="wm">이다사</div>
  </div>{audio_tag}
</div>
<script>
var SC = {json.dumps(sc_meta, separators=(",", ":"))};
var CAPN = {n};
{js}
</script>
</body>
</html>
""", n


def main(proj):
    spec = importlib.util.spec_from_file_location("plan", os.path.join(proj, "plan.py"))
    plan = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(plan)
    tl = json.load(open(os.path.join(proj, "timings.json"), encoding="utf-8"))
    scenes, total = plan.SCENES, plan.TOTAL
    audio = getattr(plan, "AUDIO", "assets/audio/voice.wav")

    # background families are chosen once, globally, so parts agree with the whole
    prev = []
    for k, sc in enumerate(scenes):
        prev.append(background(k, sc.get("bg"), prev)[2])
    plan._bgprev = prev
    mute = set()
    for sc in scenes:
        mute.update(sc.get("mute", ()))
    plan._caps = caption_cards(tl, mute)

    full, ncap = emit_doc(plan, tl, 0, len(scenes), 0.0, total, audio)
    open(os.path.join(proj, "index.html"), "w", encoding="utf-8").write(full)

    # render parts: cut on scene starts, frame-aligned, each under PART_MAX
    starts = [0.0] + [frame(tl[sc["a"]]["s"] - 0.06) for sc in scenes[1:]]
    cuts, k0 = [0], 0
    for k in range(1, len(scenes)):
        if starts[k] - starts[k0] > PART_MAX - 6 or (k + 1 < len(scenes) and starts[k + 1] - starts[k0] > PART_MAX):
            cuts.append(k)
            k0 = k
    cuts.append(len(scenes))
    pdir = os.path.join(proj, "parts")
    os.makedirs(pdir, exist_ok=True)
    manifest = []
    for p, (a, b) in enumerate(zip(cuts, cuts[1:])):
        T0 = starts[a]
        T1 = total if b == len(scenes) else starts[b]
        doc, _ = emit_doc(plan, tl, a, b, T0, T1, None)
        name = f"p{p:02d}"
        d = os.path.join(pdir, name)
        os.makedirs(d, exist_ok=True)
        open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(doc)
        for ln in ("assets", "vendor"):   # each part is its own one-root project
            if not os.path.lexists(os.path.join(d, ln)):
                os.symlink(os.path.join("..", "..", ln), os.path.join(d, ln))
        manifest.append({"file": name, "t0": T0, "t1": T1, "frames": round((T1 - T0) * FPS)})
    json.dump(manifest, open(os.path.join(pdir, "manifest.json"), "w"), indent=1)

    print(f"wrote index.html: {total:.2f}s · {len(scenes)} scenes · {len(plan._caps)} caption cards")
    print(f"  {len(manifest)} render parts:", ", ".join(f"{m['t1'] - m['t0']:.1f}s" for m in manifest))
    longest = max(text_w(x[2], font(CAP_PX)) for x in plan._caps)
    print(f"  widest caption {longest}px (limit {CAP_MAX})")
    from collections import Counter
    print("  backgrounds:", dict(Counter(prev)))


if __name__ == "__main__":
    main(os.path.abspath(sys.argv[1]))
