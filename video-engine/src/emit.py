# -*- coding: utf-8 -*-
"""Write a project's index.html — one HyperFrames composition.

    PROJECT=examples/gonggam python3 src/emit.py [--audio assets/audio/master.wav]

The project directory holds plan.py (PLAN, optionally LINES / SECTION /
WATERMARK) and timings.txt; lines come from plan.LINES or chunks.json.
Tracks: 0 backgrounds · 1 content · 2 captions · 3 watermark.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PROJECT = os.path.abspath(os.environ.get("PROJECT", os.path.join(HERE, "..", "examples", "idasa")))
sys.path.insert(0, HERE)
sys.path.insert(0, PROJECT)
from build import (W, H, CDN, IMG, ALIAS, NEON_FIG, FAMILIES,   # noqa: E402
                   esc, caption_cards, motes)
import plan as _plan                                             # noqa: E402
PLAN = _plan.PLAN

OUT = os.environ.get("OUT", os.path.join(PROJECT, "index.html"))


# ── figures (SVG) ───────────────────────────────────────────────────────────
def fig_loop4(labels=("침묵", "불안", "질문", "안심")):
    import math
    cx, cy, r = 480, 300, 205
    pts = [(cx + r * math.cos(-math.pi / 2 + 2 * math.pi * i / 4),
            cy + r * math.sin(-math.pi / 2 + 2 * math.pi * i / 4)) for i in range(4)]
    s = ['<svg width="960" height="600" viewBox="0 0 960 600">']
    for i in range(4):
        a, b = pts[i], pts[(i + 1) % 4]
        mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
        s.append(f'<path class="edge glow" d="M{a[0]:.0f} {a[1]:.0f} L{b[0]:.0f} {b[1]:.0f}"/>')
        s.append(f'<circle class="node-dim" cx="{mx:.0f}" cy="{my:.0f}" r="7"/>')
    for i, (p, lab) in enumerate(zip(pts, labels)):
        s.append(f'<circle class="node glow loop-node" cx="{p[0]:.0f}" cy="{p[1]:.0f}" r="13"/>')
        dx = 0 if abs(p[0] - cx) < 4 else (150 if p[0] > cx else -150)
        dy = 10 if abs(p[1] - cy) < 4 else (78 if p[1] > cy else -66)
        anc = "middle" if dx == 0 else ("start" if dx > 0 else "end")
        s.append(f'<text class="dlabel" x="{p[0]+dx:.0f}" y="{p[1]+dy:.0f}" '
                 f'text-anchor="{anc}">{esc(lab)}</text>')
    s.append("</svg>")
    return "".join(s)


def fig_branch():
    s = ['<svg width="1180" height="520" viewBox="0 0 1180 520">']
    s.append('<circle class="node glow" cx="150" cy="260" r="18"/>')
    for i, y in enumerate((70, 190, 330, 450)):
        s.append(f'<path class="edge glow br-edge" d="M150 260 C 430 260, 520 {y}, 830 {y}"/>')
        s.append(f'<circle class="node-dim glow br-dot" cx="860" cy="{y}" r="11"/>')
    s.append("</svg>")
    return "".join(s)


def fig_twonodes():
    s = ['<svg width="1240" height="480" viewBox="0 0 1240 480">']
    for x in (250, 990):
        s.append(f'<g class="glow tn-fig"><circle class="node" cx="{x}" cy="190" r="44"/>'
                 f'<path class="edge-hot" d="M{x-58} 330 C {x-58} 250, {x+58} 250, {x+58} 330"/></g>')
    s.append('<path class="edge-hot glow tn-arc" d="M330 150 C 560 40, 690 40, 910 150"/>')
    s.append('<path class="edge-hot glow tn-arc2" d="M910 250 C 690 360, 560 360, 330 250"/>')
    s.append("</svg>")
    return "".join(s)


def fig_qmarks(seed=0):
    s, st = ['<svg width="1500" height="640" viewBox="0 0 1500 640">'], seed * 7919 + 3
    for _ in range(22):
        st = (st * 1103515245 + 12345) & 0x7FFFFFFF
        x = 60 + (st >> 7) % 1380
        st = (st * 1103515245 + 12345) & 0x7FFFFFFF
        y = 80 + (st >> 7) % 500
        st = (st * 1103515245 + 12345) & 0x7FFFFFFF
        sz = 34 + (st >> 9) % 70
        st = (st * 1103515245 + 12345) & 0x7FFFFFFF
        op = 0.22 + (st >> 11) % 60 / 100.0
        s.append(f'<text class="qm glow" x="{x}" y="{y}" font-size="{sz}" '
                 f'font-family="Pretendard" font-weight="700" fill="#5AD8F7" '
                 f'opacity="{op:.2f}">?</text>')
    s.append("</svg>")
    return "".join(s)


def fig_panels():
    s = ['<svg width="1240" height="560" viewBox="0 0 1240 560">']
    for i in range(5):
        x, y = 140 + i * 80, 60 + i * 52
        s.append(f'<rect class="pnl" x="{x}" y="{y}" width="700" height="380" rx="16" '
                 f'fill="rgba(90,216,247,0.05)" stroke="#1E7C96" stroke-width="3"/>')
    s.append("</svg>")
    return "".join(s)


# ── extra figures ───────────────────────────────────────────────────────────
# Added so that no single diagram carries more than two moments in the film.
# Each one is shaped around the sentence it plays under, not a generic slot.

def fig_surge(label="불안"):
    """A flat line that spikes — 불안이 확 올라오는 순간."""
    d = ("M60 400 L360 400 L430 396 L500 404 L560 398 "
         "C 640 396, 690 330, 740 160 C 770 62, 800 60, 830 150 "
         "C 870 268, 920 330, 1000 344 L1180 344")
    return ('<svg width="1240" height="520" viewBox="0 0 1240 520">'
            f'<path class="edge" d="M60 400 L1180 400" opacity=".35"/>'
            f'<path class="edge-hot glow fg-draw" d="{d}"/>'
            '<circle class="node glow fg-pop" cx="830" cy="98" r="14"/>'
            f'<text class="dlabel" x="830" y="48" text-anchor="middle">{esc(label)}</text>'
            '</svg>')


def fig_meter(level=0.82, label="불안"):
    level = float(level)
    """A vertical gauge filling up — 다시 불안해집니다."""
    top, bot = 70, 470
    y = bot - (bot - top) * level
    return ('<svg width="900" height="560" viewBox="0 0 900 560">'
            f'<rect x="392" y="{top}" width="116" height="{bot-top}" rx="58" '
            'fill="rgba(90,216,247,.06)" stroke="#1E7C96" stroke-width="3"/>'
            f'<rect class="fg-fill glow" x="398" y="{y:.0f}" width="104" '
            f'height="{bot-y:.0f}" rx="52" fill="#5AD8F7"/>'
            + "".join(f'<path class="edge" d="M330 {bot-(bot-top)*t:.0f} L370 '
                      f'{bot-(bot-top)*t:.0f}" opacity=".5"/>'
                      for t in (.25, .5, .75))
            + f'<text class="dlabel" x="560" y="{max(y, 120):.0f}" text-anchor="start">{esc(label)}</text>'
            '</svg>')


def fig_repeat_strip():
    """The same four beats printed three times, fading — 이게 반복되는 겁니다."""
    rows = []
    for r, op in enumerate((1.0, .55, .28)):
        y = 120 + r * 150
        rows.append(f'<g opacity="{op}">')
        for c in range(4):
            x = 190 + c * 250
            rows.append(f'<rect x="{x}" y="{y}" width="200" height="86" rx="43" '
                        'fill="rgba(90,216,247,.10)" stroke="#1E7C96" stroke-width="3"/>')
            if c < 3:
                rows.append(f'<path class="edge" d="M{x+200} {y+43} L{x+250} {y+43}"/>')
        rows.append('</g>')
    return ('<svg width="1360" height="560" viewBox="0 0 1360 560">'
            + "".join(rows) + '</svg>')


def fig_dial(angle=-38):
    """A regulator, not a switch — 불안을 조절하는 방식의 문제."""
    import math
    cx, cy, r = 470, 330, 190
    a = math.radians(angle - 90)
    return ('<svg width="940" height="520" viewBox="0 0 940 520">'
            f'<path class="edge" d="M{cx-r} {cy} A {r} {r} 0 0 1 {cx+r} {cy}" opacity=".45"/>'
            + "".join(
                f'<circle class="node-dim" cx="{cx+r*math.cos(math.radians(t-180)):.0f}" '
                f'cy="{cy+r*math.sin(math.radians(t-180)):.0f}" r="7"/>'
                for t in (0, 45, 90, 135, 180))
            + f'<path class="edge-hot glow fg-needle" d="M{cx} {cy} '
              f'L{cx+(r-34)*math.cos(a):.0f} {cy+(r-34)*math.sin(a):.0f}"/>'
            f'<circle class="node glow" cx="{cx}" cy="{cy}" r="17"/>'
            f'<text class="dlabel-dim" x="{cx-r}" y="{cy+64}" text-anchor="middle">약</text>'
            f'<text class="dlabel-dim" x="{cx+r}" y="{cy+64}" text-anchor="middle">강</text>'
            '</svg>')


def fig_bridge(a="정보", b="사람"):
    """Two banks joined — 대화가 사람 얘기로 건너갑니다."""
    return ('<svg width="1320" height="480" viewBox="0 0 1320 480">'
            '<rect x="40" y="300" width="330" height="120" rx="12" '
            'fill="rgba(90,216,247,.07)" stroke="#1E7C96" stroke-width="3"/>'
            '<rect x="950" y="300" width="330" height="120" rx="12" '
            'fill="rgba(90,216,247,.07)" stroke="#1E7C96" stroke-width="3"/>'
            '<path class="edge-hot glow fg-draw" d="M370 300 C 560 140, 760 140, 950 300"/>'
            + "".join(f'<path class="edge" d="M{x} {y:.0f} L{x} 300"/>'
                      for x, y in ((470, 216), (660, 178), (850, 216)))
            + f'<text class="dlabel-dim" x="205" y="380" text-anchor="middle">{esc(a)}</text>'
            f'<text class="dlabel" x="1115" y="380" text-anchor="middle">{esc(b)}</text>'
            '</svg>')


def fig_flow():
    """A meandering current — 그렇게 흘러갈 수 있습니다."""
    paths = []
    for k, (op, dy) in enumerate(((1, 0), (.5, 52), (.28, -52))):
        d = (f"M60 {260+dy} C 300 {140+dy}, 420 {380+dy}, 660 {260+dy} "
             f"S 1020 {140+dy}, 1260 {250+dy}")
        cls = "edge-hot glow fg-draw" if k == 0 else "edge"
        paths.append(f'<path class="{cls}" d="{d}" opacity="{op}"/>')
    return ('<svg width="1320" height="520" viewBox="0 0 1320 520">'
            + "".join(paths)
            + '<circle class="node glow fg-pop" cx="1260" cy="250" r="13"/></svg>')


def fig_weave(a="관심", b="표현"):
    """Two strands crossing in turn — 관심, 그리고 표현."""
    pa = "M80 240 C 260 60, 440 60, 620 240 S 980 420, 1160 240"
    pb = "M80 240 C 260 420, 440 420, 620 240 S 980 60, 1160 240"
    return ('<svg width="1240" height="500" viewBox="0 0 1240 500">'
            f'<path class="edge-hot glow fg-draw" d="{pa}"/>'
            f'<path class="edge glow fg-draw2" d="{pb}" stroke="#D8B368"/>'
            '<circle class="node glow" cx="620" cy="240" r="13"/>'
            f'<text class="dlabel" x="80" y="150" text-anchor="start">{esc(a)}</text>'
            f'<text class="dlabel" x="1160" y="150" text-anchor="end">{esc(b)}</text>'
            '</svg>')


def fig_pendulum(a="상대", b="나"):
    """One weight, two ends — 다시 상대에게, 다시 나에게."""
    return ('<svg width="1180" height="540" viewBox="0 0 1180 540">'
            '<circle class="node-dim" cx="590" cy="70" r="12"/>'
            '<path class="edge" d="M250 400 A 400 400 0 0 1 930 400" opacity=".4"/>'
            '<path class="edge-hot glow" d="M590 70 L288 352"/>'
            '<path class="edge glow" d="M590 70 L892 352" opacity=".45"/>'
            '<circle class="node glow fg-pop" cx="288" cy="352" r="30"/>'
            '<circle class="node-dim glow" cx="892" cy="352" r="22"/>'
            f'<text class="dlabel" x="288" y="452" text-anchor="middle">{esc(a)}</text>'
            f'<text class="dlabel-dim" x="892" y="444" text-anchor="middle">{esc(b)}</text>'
            '</svg>')


def fig_rally():
    """A ball traced back and forth over a net — 서로 왔다 갔다."""
    dots = "".join(f'<circle class="node-dim" cx="{x}" cy="{y}" r="9" opacity="{o}"/>'
                   for x, y, o in ((250, 300, .35), (400, 170, .5), (560, 300, .65),
                                   (720, 170, .8), (880, 300, .95)))
    return ('<svg width="1180" height="500" viewBox="0 0 1180 500">'
            '<path class="edge" d="M120 380 L1060 380" opacity=".5"/>'
            '<path class="edge" d="M590 150 L590 380"/>'
            '<path class="edge-hot glow fg-draw" d="M180 330 Q 320 120 470 330 '
            'Q 620 120 770 330 Q 920 120 1030 300"/>'
            + dots + '<circle class="node glow fg-pop" cx="1030" cy="300" r="15"/></svg>')


def fig_split(a="관심", b="표현"):
    """One line separating into two named tracks — 그걸 구분하기 시작하면."""
    return ('<svg width="1280" height="500" viewBox="0 0 1280 500">'
            '<path class="edge-hot glow" d="M70 250 L430 250"/>'
            '<circle class="node glow" cx="430" cy="250" r="15"/>'
            '<path class="edge-hot glow fg-draw" d="M430 250 C 640 250, 700 120, 940 120"/>'
            '<path class="edge glow fg-draw2" d="M430 250 C 640 250, 700 380, 940 380" '
            'stroke="#D8B368"/>'
            f'<text class="dlabel" x="980" y="138" text-anchor="start">{esc(a)}</text>'
            f'<text class="dlabel" x="980" y="398" text-anchor="start">{esc(b)}</text>'
            '</svg>')


def fig_twocheck(a="상대에게 관심을", b="내 생각을 보여주기"):
    """Two things you can now do — 관심도, 내 생각도."""
    rows = []
    # centre the block on the frame: circle + gap + the longer label
    x0 = int(620 - (52 + 44 + 46 * max(len(a), len(b))) / 2) + 26
    for k, (lab, y) in enumerate(((a, 170), (b, 340))):
        rows.append(f'<circle class="node glow" cx="{x0}" cy="{y}" r="26"/>')
        rows.append(f'<path d="M{x0-18} {y} l14 16 l26 -32" stroke="#0B0B0D" stroke-width="7" '
                    'fill="none" stroke-linecap="round" stroke-linejoin="round"/>')
        rows.append(f'<text class="dlabel" x="{x0+70}" y="{y+16}" text-anchor="start">{esc(lab)}</text>')
    return ('<svg width="1240" height="500" viewBox="0 0 1240 500">'
            + "".join(rows) + '</svg>')


def fig_cutoff():
    """An answer clipped before it lands — 끝까지 기다리지 못합니다."""
    return ('<svg width="1280" height="480" viewBox="0 0 1280 480">'
            '<path class="edge-hot glow" d="M70 240 C 260 100, 360 380, 560 240"/>'
            '<path class="edge" d="M560 240 C 740 130, 860 350, 1040 240" '
            'stroke-dasharray="16 22" opacity=".42"/>'
            '<path d="M620 90 L620 390" stroke="#F0538F" stroke-width="9" '
            'stroke-linecap="round"/>'
            '<circle class="node-dim" cx="1040" cy="240" r="11" opacity=".4"/>'
            '<text class="dlabel-dim" x="1080" y="256" text-anchor="start">…</text>'
            '</svg>')


def fig_tree(items=("사실", "감정", "이유", "취향"), root="한 문장"):
    """One sentence holding several topics — 소재가 세 개, 네 개."""
    s = ['<svg width="1300" height="540" viewBox="0 0 1300 540">',
         '<rect x="60" y="216" width="330" height="108" rx="18" '
         'fill="rgba(255,255,255,.08)" stroke="rgba(255,255,255,.22)" stroke-width="3"/>',
         f'<text class="dlabel-dim" x="225" y="286" text-anchor="middle">{esc(root)}</text>']
    n = len(items)
    for k, lab in enumerate(items):
        y = 100 + k * (340 / max(n - 1, 1))
        s.append(f'<path class="edge glow" d="M390 270 C 600 270, 660 {y:.0f}, 830 {y:.0f}"/>')
        s.append(f'<circle class="node glow" cx="850" cy="{y:.0f}" r="12"/>')
        s.append(f'<text class="dlabel" x="900" y="{y+16:.0f}" text-anchor="start">{esc(lab)}</text>')
    s.append('</svg>')
    return "".join(s)


def fig_fan():
    """Many directions open at once — 여러 방향으로 갈 수 있습니다."""
    import math
    s = ['<svg width="1240" height="540" viewBox="0 0 1240 540">']
    for k in range(7):
        a = math.radians(-46 + k * 15.3)
        x, y = 260 + 900 * math.cos(a), 300 + 400 * math.sin(a)
        op = .35 + .1 * (3 - abs(k - 3))
        s.append(f'<path class="edge glow" d="M260 300 L{x:.0f} {y:.0f}" opacity="{op:.2f}"/>')
        s.append(f'<circle class="node-dim" cx="{x:.0f}" cy="{y:.0f}" r="9"/>')
    s.append('<circle class="node glow" cx="260" cy="300" r="20"/></svg>')
    return "".join(s)


def fig_lens(label="감정"):
    """A magnifier held over the sentence — 그 문장 안에 뭐가 있는지."""
    bars = "".join(f'<rect x="{200+k*0}" y="{212+k*54}" width="{760-k*150}" height="20" '
                   f'rx="10" fill="rgba(255,255,255,{0.20-k*0.05:.2f})"/>' for k in range(3))
    return ('<svg width="1260" height="520" viewBox="0 0 1260 520">'
            + bars
            + '<circle cx="800" cy="256" r="168" fill="rgba(90,216,247,.07)" '
            'stroke="#5AD8F7" stroke-width="7" class="glow fg-pop"/>'
            '<path d="M918 374 L1060 516" stroke="#5AD8F7" stroke-width="18" '
            'stroke-linecap="round" class="glow"/>'
            f'<text class="dlabel" x="800" y="274" text-anchor="middle">{esc(label)}</text>'
            '</svg>')


def fig_queue():
    """The next question already waiting in line — 이미 다음 질문이 떠 있어요."""
    s = ['<svg width="1300" height="480" viewBox="0 0 1300 480">']
    for k in range(4):
        x = 110 + k * 300
        hot = (k == 1)
        cls = ' class="glow"' if hot else ''
        s.append(f'<rect x="{x}" y="170" width="240" height="140" rx="24" '
                 f'fill="rgba(90,216,247,{".16" if hot else ".05"})" '
                 f'stroke="{"#5AD8F7" if hot else "#1E7C96"}" stroke-width="3"{cls}/>')
        s.append(f'<text class="{"dlabel" if hot else "dlabel-dim"}" x="{x+120}" y="258" '
                 f'text-anchor="middle">?</text>')
        if k < 3:
            s.append(f'<path class="edge" d="M{x+240} 240 L{x+300} 240"/>')
    s.append('</svg>')
    return "".join(s)


def fig_countdown(n=3):
    """Beats counted out — 하나. 둘. 셋."""
    s = ['<svg width="1100" height="420" viewBox="0 0 1100 420">']
    for k in range(n):
        x = 550 + (k - (n - 1) / 2) * 300
        s.append(f'<circle cx="{x:.0f}" cy="200" r="86" fill="rgba(90,216,247,.07)" '
                 'stroke="#1E7C96" stroke-width="4"/>')
        s.append(f'<circle class="node glow" cx="{x:.0f}" cy="200" r="24"/>')
    s.append('</svg>')
    return "".join(s)


def fig_stretch():
    """Three seconds that feel long — the same gap, drawn wide."""
    return ('<svg width="1360" height="440" viewBox="0 0 1360 440">'
            '<path class="edge" d="M90 220 L1270 220" opacity=".4"/>'
            '<path class="edge-hot glow fg-draw" d="M300 220 L1060 220"/>'
            '<path class="edge-hot glow" d="M300 160 L300 280"/>'
            '<path class="edge-hot glow" d="M1060 160 L1060 280"/>'
            '<text class="dlabel" x="680" y="150" text-anchor="middle">3초</text>'
            '<text class="dlabel-dim" x="680" y="330" text-anchor="middle">체감</text>'
            '</svg>')


def fig_elapsed(label="한 시간 뒤"):
    """A long stretch of talking with nothing learned — 한 시간 넘게."""
    ticks = "".join(f'<path class="edge" d="M{120+k*115} 250 L{120+k*115} '
                    f'{200 if k % 4 == 0 else 224}" opacity=".5"/>' for k in range(11))
    return ('<svg width="1320" height="440" viewBox="0 0 1320 440">'
            '<path class="edge" d="M120 250 L1270 250" opacity=".55"/>' + ticks
            + '<path class="edge-hot glow fg-draw" d="M120 250 L1270 250"/>'
            '<circle class="node glow fg-pop" cx="1270" cy="250" r="14"/>'
            '<text class="dlabel-dim" x="120" y="340" text-anchor="start">시작</text>'
            f'<text class="dlabel" x="1270" y="340" text-anchor="end">{esc(label)}</text>'
            '</svg>')


def fig_plain_chips():
    """A row of interchangeable questions — 하나하나는 너무 평범하거든요."""
    labs = ("주말에 뭐 하세요", "취미가 뭐예요", "어디 사세요", "일은 어떠세요")
    s = ['<svg width="1500" height="460" viewBox="0 0 1500 460">']
    for k, lab in enumerate(labs):
        x, y = 90 + (k % 2) * 700, 110 + (k // 2) * 170
        s.append(f'<rect x="{x}" y="{y}" width="640" height="106" rx="53" '
                 'fill="rgba(255,255,255,.055)" stroke="rgba(255,255,255,.16)" stroke-width="3"/>')
        s.append(f'<text class="dlabel-dim" x="{x+320}" y="{y+70}" '
                 f'text-anchor="middle">{esc(lab)}</text>')
    s.append('</svg>')
    return "".join(s)


def fig_ask_toss():
    """A question tossed out and nothing coming back — 질문 하나 던져요."""
    return ('<svg width="1240" height="460" viewBox="0 0 1240 460">'
            '<circle class="node glow" cx="180" cy="300" r="22"/>'
            '<path class="edge-hot glow fg-draw" d="M210 290 C 460 90, 720 90, 980 250" '
            'stroke-dasharray="0"/>'
            '<circle class="node-dim glow" cx="1010" cy="262" r="16"/>'
            '<text class="dlabel" x="595" y="120" text-anchor="middle">?</text>'
            '</svg>')


def fig_ask_again():
    """And then one more, straight after — 질문 하나 더 던집니다."""
    s = ['<svg width="1300" height="470" viewBox="0 0 1300 470">',
         '<circle class="node glow" cx="180" cy="310" r="22"/>']
    for k, (op, dy) in enumerate(((.38, 0), (1.0, -120))):
        s.append(f'<path class="edge-hot glow" d="M210 {300+dy} C 470 {110+dy}, 730 '
                 f'{110+dy}, 1000 {268+dy}" opacity="{op}"/>')
        s.append(f'<text class="{"dlabel" if k else "dlabel-dim"}" x="605" y="{140+dy}" '
                 f'text-anchor="middle">?</text>')
    s.append('<circle class="node-dim glow" cx="1030" cy="230" r="16"/></svg>')
    return "".join(s)


FIGS = {"loop4": fig_loop4, "branch": fig_branch, "twonodes": fig_twonodes,
        "qmarks": fig_qmarks, "panels": fig_panels,
        "surge": fig_surge, "meter": fig_meter, "repeatstrip": fig_repeat_strip,
        "dial": fig_dial, "bridge": fig_bridge, "flow": fig_flow, "weave": fig_weave,
        "pendulum": fig_pendulum, "rally": fig_rally, "split": fig_split,
        "twocheck": fig_twocheck, "cutoff": fig_cutoff, "tree": fig_tree,
        "fan": fig_fan, "lens": fig_lens, "queue": fig_queue,
        "countdown": fig_countdown, "stretch": fig_stretch, "elapsed": fig_elapsed,
        "plainchips": fig_plain_chips, "asktoss": fig_ask_toss, "askagain": fig_ask_again}


# ── figures added for "공감과 동의" ─────────────────────────────────────────
def fig_venn(label="공통점"):
    """Two circles sharing a middle — 공통점 / 잘 맞는 느낌."""
    return ('<svg width="1240" height="560" viewBox="0 0 1240 560">'
            '<circle cx="480" cy="280" r="220" fill="rgba(90,216,247,.07)" '
            'stroke="#1E7C96" stroke-width="4"/>'
            '<circle class="fg-pop" cx="760" cy="280" r="220" fill="rgba(216,179,104,.07)" '
            'stroke="#D8B368" stroke-width="4"/>'
            '<path class="glow" d="M620 110 A 220 220 0 0 1 620 450 A 220 220 0 0 1 620 110" '
            'fill="rgba(90,216,247,.20)"/>'
            '<text class="dlabel-dim" x="370" y="294" text-anchor="middle">상대</text>'
            '<text class="dlabel-dim" x="870" y="294" text-anchor="middle">나</text>'
            f'<text class="dlabel" x="620" y="296" text-anchor="middle" font-size="40">{esc(label)}</text>'
            '</svg>')


def fig_converge(a="A", b="B", label="이해"):
    """Two different lines meeting — 달랐는데 더 깊이 이해하게 됐다."""
    return ('<svg width="1300" height="520" viewBox="0 0 1300 520">'
            '<path class="edge-hot glow fg-draw" d="M260 110 C 520 110, 560 260, 760 260"/>'
            '<path class="edge glow fg-draw2" d="M260 410 C 520 410, 560 260, 760 260" '
            'stroke="#D8B368"/>'
            '<path class="edge-hot glow" d="M760 260 L1040 260"/>'
            '<circle class="node glow fg-pop" cx="760" cy="260" r="18"/>'
            '<circle class="node-dim" cx="260" cy="110" r="12"/>'
            '<circle cx="260" cy="410" r="12" fill="#D8B368"/>'
            f'<text class="dlabel" x="220" y="126" text-anchor="end">{esc(a)}</text>'
            f'<text class="dlabel" x="220" y="426" text-anchor="end">{esc(b)}</text>'
            f'<text class="dlabel" x="1070" y="276" text-anchor="start">{esc(label)}</text>'
            '</svg>')


def fig_thermo(level=0.3, label="미지근"):
    """A thermometer — 대화의 온도."""
    level = float(level)
    top, bot = 60, 400
    y = bot - (bot - top) * level
    marks = "".join(
        f'<path class="edge" d="M{548} {bot-(bot-top)*t:.0f} L{588} {bot-(bot-top)*t:.0f}" opacity=".6"/>'
        for t in (.2, .4, .6, .8))
    return ('<svg width="1000" height="560" viewBox="0 0 1000 560">'
            f'<rect x="440" y="{top-30}" width="100" height="{bot-top+60}" rx="50" '
            'fill="rgba(255,255,255,.05)" stroke="rgba(255,255,255,.28)" stroke-width="4"/>'
            '<circle cx="490" cy="450" r="78" fill="rgba(255,255,255,.05)" '
            'stroke="rgba(255,255,255,.28)" stroke-width="4"/>'
            '<circle class="glow" cx="490" cy="450" r="60" fill="#5AD8F7"/>'
            f'<rect class="fg-fill glow" x="462" y="{y:.0f}" width="56" height="{450-y:.0f}" '
            'rx="28" fill="#5AD8F7"/>'
            + marks +
            f'<path class="edge-hot" d="M600 {y:.0f} L650 {y:.0f}"/>'
            f'<text class="dlabel" x="670" y="{y+16:.0f}" text-anchor="start">{esc(label)}</text>'
            '<text class="dlabel-dim" x="400" y="80" text-anchor="end">뜨거움</text>'
            '<text class="dlabel-dim" x="400" y="420" text-anchor="end">차가움</text>'
            '</svg>')


def fig_wave(mode="sync"):
    """Two frequencies — 주파수를 맞춘다 / 주파수가 깨졌다."""
    import math

    def path(amp, freq, phase, x0=80, x1=1220, jitter=0.0):
        pts = []
        for k in range(0, 121):
            x = x0 + (x1 - x0) * k / 120
            j = jitter * math.sin(k * 2.7) * (1 if k % 3 else -1)
            y = 260 + amp * math.sin(freq * (x - x0) / 180 + phase) + j
            pts.append(f"{x:.0f} {y:.0f}")
        return "M" + " L".join(pts)
    if mode == "broken":
        a = path(90, 1.0, 0, x1=640)
        b = path(120, 2.6, 1.2, x0=660, jitter=26)
        return ('<svg width="1300" height="520" viewBox="0 0 1300 520">'
                f'<path class="edge-hot glow fg-draw" d="{a}"/>'
                f'<path class="edge fg-draw2" d="{b}" stroke="#F0538F" stroke-width="5"/>'
                '<path d="M650 120 L650 400" stroke="#F0538F" stroke-width="8" '
                'stroke-linecap="round" stroke-dasharray="18 16"/>'
                '<text class="dlabel" x="650" y="480" text-anchor="middle">주파수가 깨짐</text>'
                '</svg>')
    a = path(100, 1.0, 0)
    b = path(80, 1.0, 0.5)
    return ('<svg width="1300" height="520" viewBox="0 0 1300 520">'
            f'<path class="edge-hot glow fg-draw" d="{a}"/>'
            f'<path class="edge glow fg-draw2" d="{b}" stroke="#D8B368" stroke-width="5"/>'
            '<text class="dlabel-dim" x="80" y="110" text-anchor="start">상대</text>'
            '<text class="dlabel-dim" x="80" y="460" text-anchor="start">나</text>'
            '<text class="dlabel" x="1220" y="480" text-anchor="end">속도 · 감정 · 깊이</text>'
            '</svg>')


def fig_finish():
    """Running alone to the finish line — 혼자 관계의 결승선까지."""
    flag = ('<path d="M1130 120 L1130 360" stroke="#F4F3EF" stroke-width="6" stroke-linecap="round"/>'
            '<path d="M1130 124 L1230 150 L1130 180 Z" fill="#F0538F"/>')
    return ('<svg width="1320" height="480" viewBox="0 0 1320 480">'
            '<path class="edge" d="M90 360 L1230 360" opacity=".55"/>'
            + "".join(f'<path class="edge" d="M{90+k*114} 360 L{90+k*114} 340" opacity=".45"/>'
                      for k in range(11))
            + '<path class="edge-hot glow fg-draw" d="M150 360 L1110 360"/>'
            + flag +
            '<circle class="node-dim" cx="150" cy="330" r="22"/>'
            '<circle class="node glow fg-pop" cx="1100" cy="330" r="22"/>'
            '<text class="dlabel-dim" x="150" y="440" text-anchor="middle">상대</text>'
            '<text class="dlabel" x="1100" y="440" text-anchor="middle">나</text>'
            '<text class="dlabel-dim" x="1180" y="96" text-anchor="middle">결승선</text>'
            '</svg>')


def fig_balance(a="내 생각", b="상대 생각"):
    """A level scale — 둘 중 하나를 지울 필요가 없다."""
    return ('<svg width="1200" height="540" viewBox="0 0 1200 540">'
            '<path d="M600 90 L600 440 M500 450 L700 450" stroke="#F4F3EF" stroke-width="7" '
            'stroke-linecap="round" opacity=".8"/>'
            '<circle class="node glow" cx="600" cy="90" r="16"/>'
            '<path class="edge-hot glow fg-draw" d="M260 120 L940 120"/>'
            '<path class="edge" d="M260 120 L190 280 M260 120 L330 280"/>'
            '<path class="edge" d="M940 120 L870 280 M940 120 L1010 280"/>'
            '<path d="M170 280 Q 260 340 350 280 Z" fill="rgba(90,216,247,.22)" stroke="#5AD8F7" stroke-width="4"/>'
            '<path d="M850 280 Q 940 340 1030 280 Z" fill="rgba(216,179,104,.22)" stroke="#D8B368" stroke-width="4"/>'
            f'<text class="dlabel" x="260" y="400" text-anchor="middle">{esc(a)}</text>'
            f'<text class="dlabel" x="940" y="400" text-anchor="middle">{esc(b)}</text>'
            '</svg>')



FIGS.update({"venn": fig_venn, "converge": fig_converge, "thermo": fig_thermo,
             "wave": fig_wave, "finish": fig_finish, "balance": fig_balance})

# ── pictograms ──────────────────────────────────────────────────────────────
# Review note: "픽토그램 ... 최대한 많이 활용해서 다채롭게."  The line-reading
# scenes were bare typography; each one now carries a drawn mark above the
# words. One shared stroke language, so 24 different marks still read as a set.

_PICTO = {
    "think":    '<path d="M42 96a54 40 0 1 1 108 0 54 40 0 1 1-108 0"/>'
                '<path d="M74 132l-6 26 30-22"/>'
                '<circle cx="72" cy="96" r="6" fill="currentColor" stroke="none"/>'
                '<circle cx="96" cy="96" r="6" fill="currentColor" stroke="none"/>'
                '<circle cx="120" cy="96" r="6" fill="currentColor" stroke="none"/>',
    "bored":    '<circle cx="96" cy="96" r="62"/><path d="M68 82h18M106 82h18"/>'
                '<path d="M70 128q26-14 52 0"/>',
    "spoil":    '<path d="M96 24l-26 44 34 16-30 40 22 12-18 32"/>'
                '<circle cx="96" cy="96" r="70" stroke-dasharray="14 16"/>',
    "house":    '<path d="M36 94L96 44l60 50"/><path d="M54 92v62h84V92"/>'
                '<path d="M84 154v-34h24v34"/>',
    "commute":  '<rect x="52" y="44" width="88" height="86" rx="16"/>'
                '<path d="M52 96h88M66 148l-12 20M126 148l12 20"/>'
                '<circle cx="74" cy="114" r="7" fill="currentColor" stroke="none"/>'
                '<circle cx="118" cy="114" r="7" fill="currentColor" stroke="none"/>',
    "family":   '<circle cx="70" cy="72" r="22"/><circle cx="126" cy="80" r="17"/>'
                '<path d="M36 156q0-38 34-38t34 38"/><path d="M110 156q4-30 30-30t26 30"/>',
    "travel":   '<path d="M96 28l16 54 54 16-54 16-16 54-16-54-54-16 54-16z"/>'
                '<circle cx="96" cy="98" r="9" fill="currentColor" stroke="none"/>',
    "hobby":    '<path d="M96 158s-58-34-58-72a30 30 0 0 1 58-11 30 30 0 0 1 58 11c0 38-58 72-58 72z"/>',
    "badq":     '<circle cx="96" cy="96" r="64"/>'
                '<path d="M76 76a20 20 0 1 1 26 19v14"/>'
                '<circle cx="102" cy="128" r="6" fill="currentColor" stroke="none"/>'
                '<path d="M46 46l100 100" stroke="#F0538F"/>',
    "distance": '<path d="M28 96h136"/><path d="M28 74v44M164 74v44"/>'
                '<circle cx="96" cy="96" r="13" fill="currentColor" stroke="none"/>',
    "calendar": '<rect x="34" y="50" width="124" height="112" rx="14"/>'
                '<path d="M34 86h124M66 32v30M126 32v30"/>'
                '<circle cx="72" cy="114" r="7" fill="currentColor" stroke="none"/>'
                '<circle cx="112" cy="114" r="7" fill="currentColor" stroke="none"/>'
                '<circle cx="92" cy="140" r="7" fill="currentColor" stroke="none"/>',
    "pin":      '<path d="M96 168s48-52 48-84a48 48 0 1 0-96 0c0 32 48 84 48 84z"/>'
                '<circle cx="96" cy="82" r="18"/>',
    "medal":    '<circle cx="96" cy="116" r="42"/><path d="M96 98l7 15 16 2-12 12 3 16-14-8-14 8 3-16-12-12 16-2z" '
                'fill="currentColor" stroke="none"/><path d="M66 78L50 26M126 78l16-52"/>',
    "calm":     '<path d="M26 82q26-22 52 0t52 0 36-8"/><path d="M26 118q26-22 52 0t52 0 36-8"/>',
    "door":     '<rect x="52" y="34" width="88" height="128" rx="10"/>'
                '<circle cx="118" cy="100" r="7" fill="currentColor" stroke="none"/>'
                '<path d="M150 100h34m-14-14 14 14-14 14" stroke="#D8B368"/>',
    "radar":    '<circle cx="96" cy="112" r="16"/><path d="M60 112a36 36 0 0 1 72 0"/>'
                '<path d="M32 112a64 64 0 0 1 128 0" stroke-dasharray="12 14"/>',
    "relief":   '<circle cx="96" cy="92" r="50"/><path d="M76 84h4M112 84h4"/>'
                '<path d="M74 110q22 20 44 0"/>'
                '<path d="M96 150v22M70 156l-10 16M122 156l10 16" stroke="#D8B368"/>',
    "notrick":  '<rect x="34" y="72" width="124" height="80" rx="14"/>'
                '<path d="M74 72V52a22 22 0 0 1 44 0v20"/><path d="M34 106h124"/>'
                '<path d="M40 44l112 112" stroke="#F0538F"/>',
    "self":     '<circle cx="96" cy="66" r="26"/><path d="M44 160q0-44 52-44t52 44"/>'
                '<path d="M150 62h30m-30 22h22" stroke="#D8B368"/>',
    "differ":   '<path d="M96 30v132"/><path d="M40 78h112"/>'
                '<circle cx="54" cy="122" r="20"/><circle cx="138" cy="122" r="20" stroke="#D8B368"/>',
    "wonder":   '<path d="M96 22v30M96 140v30M22 96h30M140 96h30"/>'
                '<path d="M44 44l22 22M148 44l-22 22M44 148l22-22M148 148l-22-22"/>'
                '<circle cx="96" cy="96" r="26" fill="currentColor" stroke="none"/>',
    "fewer":    '<path d="M60 52h72M72 92h48M84 132h24"/><path d="M96 150v22m-14-14 14 14 14-14"/>',
    "listen":   '<path d="M118 44a44 44 0 0 0-44 44v34a22 22 0 0 0 22 22"/>'
                '<circle cx="74" cy="122" r="16"/>'
                '<path d="M140 70q18 26 0 52" stroke="#D8B368"/>',
    "mirror":   '<rect x="30" y="44" width="58" height="104" rx="10"/>'
                '<rect x="104" y="44" width="58" height="104" rx="10" stroke="#D8B368"/>'
                '<path d="M96 30v132" stroke-dasharray="10 12"/>',
}

_PICTO.update({
    "heart":    _PICTO["hobby"],
    "nolink":   '<path d="M20 60h62a14 14 0 0 1 14 14v30a14 14 0 0 1-14 14H50l-18 16v-16h-12z"/>'
                '<path d="M172 84h-62a14 14 0 0 0-14 14v30a14 14 0 0 0 14 14h32l18 16v-16h12z" stroke="#D8B368"/>'
                '<path d="M78 164l36-36" stroke="#F0538F"/>',
    "ok":       '<path d="M60 88v70H34V88z"/><path d="M60 92l30-50c16 0 20 10 16 26l-6 20h40a14 14 0 0 1 13 17l-12 44a14 14 0 0 1-14 11H60"/>',
    "blank":    '<circle cx="96" cy="64" r="30"/><path d="M40 168q0-50 56-50t56 50"/>'
                '<path d="M86 52a12 12 0 1 1 14 12v8" stroke="#D8B368"/>'
                '<circle cx="100" cy="84" r="4" fill="#D8B368" stroke="none"/>',
    "point":    '<circle cx="96" cy="96" r="66"/><path d="M96 56v50"/>'
                '<circle cx="96" cy="134" r="7" fill="currentColor" stroke="none"/>',
    "bowl":     '<path d="M28 96h136a68 58 0 0 1-136 0z"/><path d="M70 158h52"/>'
                '<path d="M70 72q-10-14 0-28M96 72q-10-14 0-28M122 72q-10-14 0-28" stroke="#F0538F"/>'
                '<path d="M124 20l44 70M140 16l40 66" stroke="#D8B368"/>',
    "mask":     '<path d="M36 50q60-24 120 0v50q0 58-60 72-60-14-60-72z"/>'
                '<path d="M60 88q12-10 24 0M108 88q12-10 24 0"/><path d="M70 128q26 18 52 0"/>',
    "chat":     '<path d="M24 38h96a14 14 0 0 1 14 14v42a14 14 0 0 1-14 14H64l-24 20v-20H24a14 14 0 0 1-14-14V52a14 14 0 0 1 14-14z"/>'
                '<path d="M150 82h18a14 14 0 0 1 14 14v36a14 14 0 0 1-14 14h-6v18l-22-18h-40a14 14 0 0 1-14-14v-6" stroke="#D8B368"/>',
    "hill":     '<path d="M14 162l58-86 34 46 22-30 50 70z"/><path d="M72 76V28l32 12-32 12" stroke="#D8B368"/>',
    "target":   '<circle cx="90" cy="102" r="64"/><circle cx="90" cy="102" r="38"/>'
                '<circle cx="90" cy="102" r="10" fill="currentColor" stroke="none"/>'
                '<path d="M92 100l72-72M140 28h24v24" stroke="#D8B368"/>',
    "dice":     '<rect x="40" y="40" width="112" height="112" rx="22" transform="rotate(12 96 96)"/>'
                '<circle cx="74" cy="74" r="8" fill="currentColor" stroke="none"/>'
                '<circle cx="96" cy="98" r="8" fill="currentColor" stroke="none"/>'
                '<circle cx="118" cy="122" r="8" fill="currentColor" stroke="none"/>',
    "eye":      '<path d="M14 96q82-86 164 0-82 86-164 0z"/><circle cx="96" cy="96" r="28"/>'
                '<circle cx="96" cy="96" r="10" fill="currentColor" stroke="none"/>',
    "shield":   '<path d="M96 22l62 22v44c0 42-26 70-62 84-36-14-62-42-62-84V44z"/>'
                '<path d="M70 96l18 18 34-36" stroke="#D8B368"/>',
    "swap":     '<path d="M30 70h124m-26-26 26 26-26 26"/><path d="M162 126H38m26-26-26 26 26 26" stroke="#D8B368"/>',
    "nod":      '<circle cx="96" cy="96" r="66"/><path d="M64 98l22 22 44-46"/>',
    "bulb":     '<path d="M96 24a50 50 0 0 0-30 90c8 7 10 14 10 22h40c0-8 2-15 10-22a50 50 0 0 0-30-90z"/>'
                '<path d="M78 156h36M84 176h24"/><path d="M96 100v36" stroke="#D8B368"/>',
    "give":     '<path d="M40 60h84a40 40 0 0 1 0 80H52"/><path d="M76 112l-28 28 28 28" stroke="#D8B368"/>',
    "bandage":  '<rect x="24" y="68" width="144" height="56" rx="28" transform="rotate(-35 96 96)"/>'
                '<rect x="72" y="72" width="48" height="48" rx="8" transform="rotate(-35 96 96)"/>'
                '<circle cx="90" cy="92" r="4" fill="currentColor" stroke="none"/>'
                '<circle cx="102" cy="100" r="4" fill="currentColor" stroke="none"/>',
    "smile":    '<circle cx="96" cy="96" r="66"/><path d="M68 80q8-10 16 0M108 80q8-10 16 0"/>'
                '<path d="M62 110q34 44 68 0z" fill="currentColor" fill-opacity=".25"/>',
    "ring":     '<circle cx="96" cy="118" r="52"/><path d="M76 52l20-24 20 24-20 18z" stroke="#D8B368"/>',
    "mic":      '<rect x="70" y="20" width="52" height="92" rx="26"/><path d="M46 92a50 50 0 0 0 100 0"/>'
                '<path d="M96 142v30M66 172h60"/><path d="M160 50q14 22 0 44M176 38q24 34 0 68" stroke="#D8B368"/>',
    "ball":     '<circle cx="96" cy="96" r="68"/><path d="M96 70l24 18-9 28H81l-9-28z" fill="currentColor" fill-opacity=".3"/>'
                '<path d="M96 70V30M120 88l36-12M111 116l22 30M81 116l-22 30M72 88l-36-12"/>',
    "weight":   '<path d="M70 56a26 26 0 1 1 52 0"/><path d="M50 60h92l20 108H30z"/>'
                '<path d="M76 118h40" stroke="#D8B368"/>',
    "puzzle":   '<path d="M30 60h40a16 16 0 1 1 32 0h40v40a16 16 0 1 0 0 32v40H102a16 16 0 1 0-32 0H30v-40a16 16 0 1 1 0-32z"/>',
    "list":     '<rect x="42" y="24" width="108" height="148" rx="14"/>'
                '<path d="M64 64l8 8 14-16M64 104l8 8 14-16M64 144l8 8 14-16"/>'
                '<path d="M98 66h30M98 106h30M98 146h30" stroke="#D8B368"/>',
    "anchor":   '<circle cx="96" cy="38" r="16"/><path d="M96 54v116M64 80h64"/>'
                '<path d="M30 118q10 50 66 52 56-2 66-52M30 118l-10 14M162 118l10 14"/>',
    "play":     '<rect x="20" y="40" width="152" height="112" rx="22"/>'
                '<path d="M82 72l42 24-42 24z" fill="currentColor" stroke-linejoin="round"/>',
})


def picto(name, size=200):
    """One line-drawn mark in the shared stroke language."""
    return (f'<svg class="picto glow" width="{size}" height="{size}" viewBox="0 0 192 192" '
            'fill="none" stroke="currentColor" stroke-width="5.5" '
            f'stroke-linecap="round" stroke-linejoin="round">{_PICTO[name]}</svg>')


# ── DOM graphic primitives ──────────────────────────────────────────────────
def g_rows(title, items, muted=(), mark=None):
    h = ['<div class="stage"><div class="scrim wide"></div>']
    if title:
        h.append(f'<div class="hl md gtitle">{esc(title)}</div>')
    h.append('<div class="rows" style="margin-top:46px">')
    for i, it in enumerate(items):
        cls = "row muted" if i in muted else "row"
        extra = ''
        if mark == "q" and i not in muted:
            extra = '<span class="qmark">?</span>'
        h.append(f'<div class="{cls}"><i class="tick"></i><span>{esc(it)}</span>{extra}</div>')
    h.append("</div></div>")
    return "".join(h)


def g_chips(title, items, hot=()):
    h = ['<div class="stage"><div class="scrim wide"></div>']
    if title:
        h.append(f'<div class="hl md gtitle">{esc(title)}</div>')
    h.append('<div class="chips" style="margin-top:50px">')
    for it in items:
        h.append(f'<span class="chip{" hot" if it in hot else ""}">{esc(it)}</span>')
    h.append("</div></div>")
    return "".join(h)


def g_bars(title, data, axis=("얕음", "깊음")):
    """A bar plus the degree it stands for.

    Review note: "그냥 바만 있어" — length alone read as decoration. Each row now
    carries a five-step rating and the block carries an axis, so the bar says how
    much, not just that there is some.
    """
    h = ['<div class="stage"><div class="scrim wide"></div>',
         f'<div class="hl md gtitle">{esc(title)}</div>' if title else '',
         '<div class="bars" style="margin-top:50px">']
    for lab, frac, tone in data:
        steps = max(1, min(5, int(round(frac * 5))))
        hot = "hot" if tone in ("hot", "cool-hot") else ""
        dots = "".join(f'<i class="{("on " + hot).strip() if k < steps else ""}"></i>'
                       for k in range(5))
        ticks = "".join(f'<span class="tickline" style="left:{q}%"></span>'
                        for q in (20, 40, 60, 80))
        h.append(f'<div><div class="bar-head"><span class="bar-lab">{esc(lab)}</span>'
                 f'<span class="bar-dots">{dots}</span></div>'
                 f'<div class="bar-track">{ticks}'
                 f'<i class="bar-fill {tone}" style="width:{int(frac*100)}%"></i></div></div>')
    h.append(f'<div class="bar-axis"><span>{esc(axis[0])}</span>'
             f'<span>{esc(axis[1])}</span></div>')
    h.append("</div></div>")
    return "".join(h)


def g_chain(items):
    h = ['<div class="stage"><div class="scrim wide"></div>',
         '<div class="chips" style="gap:16px;align-items:center">']
    for i, it in enumerate(items):
        if i:
            h.append('<span class="arrow" style="font-size:52px;color:#F0538F;'
                     'font-weight:700;padding:0 6px">&rsaquo;</span>')
        h.append(f'<span class="chip">{esc(it)}</span>')
    h.append("</div></div>")
    return "".join(h)


def g_twobranch(title, left, right):
    return ("".join([
        '<div class="stage"><div class="scrim wide"></div>',
        f'<div class="hl md gtitle">{esc(title)}</div>',
        '<svg width="1300" height="300" viewBox="0 0 1300 300" style="margin-top:26px">',
        '<path class="edge glow" d="M650 10 L650 90 M650 90 L250 90 L250 170 M650 90 L1050 90 L1050 170"/>',
        '</svg>',
        '<div style="display:flex;gap:210px;margin-top:-56px">',
        f'<div class="hl md" style="font-size:54px;color:#918F8A">{esc(left)}</div>',
        f'<div class="hl md" style="font-size:54px">{esc(right)}</div>',
        '</div></div>']))


def g_gap(mode):
    if mode == "ok":
        mid = ('<i class="dot"></i><i class="dot"></i><i class="dot"></i>')
        note = "그냥 두어도 됩니다"
    else:
        mid = ('<span class="chip hot" style="background:#F0538F;color:#fff">질문</span>')
        note = "급하게 메웁니다"
    return ("".join([
        '<div class="stage"><div class="scrim"></div>',
        f'<div class="hl md" style="margin-bottom:44px">{"공백" if mode=="ok" else "공백"}</div>',
        '<div class="gapline">',
        '<i class="seg" style="width:330px"></i>', mid, '<i class="seg" style="width:330px"></i>',
        '</div>',
        f'<div class="sub">{esc(note)}</div></div>']))


def g_lanes():
    lanes = ["상대 말을 듣기", "나를 평가하기", "다음 멘트 준비하기"]
    h = ['<div class="stage"><div class="scrim wide"></div>',
         '<div class="hl md gtitle">동시에 켜져 있는 것들</div>',
         '<div class="rows" style="margin-top:46px;gap:22px">']
    for lab in lanes:
        h.append('<div class="row" style="background:rgba(255,255,255,.07);'
                 'border-radius:18px;padding:22px 40px;width:1040px">'
                 f'<i class="tick"></i><span>{esc(lab)}</span></div>')
    h.append("</div></div>")
    return "".join(h)


def g_stack():
    h = ['<div class="stage"><div class="scrim"></div>',
         '<div class="hl md" style="margin-bottom:56px">저는 이래요</div>',
         '<div style="display:flex;flex-direction:column;align-items:center;gap:14px">']
    for i in range(5):
        h.append(f'<i class="stk" style="display:block;height:44px;border-radius:14px;'
                 f'width:{560+i*88}px;background:rgba(255,255,255,{0.10+i*0.055:.2f})"></i>')
    h.append("</div></div>")
    return "".join(h)


def g_pingpong(rich):
    rows = [("상대", "나"), ("상대", "나")] if rich else [("질문", "대답"), ("질문", "대답")]
    col = "#5AD8F7" if rich else "#918F8A"
    h = ['<div class="stage"><div class="scrim wide"></div>',
         f'<div class="hl md gtitle">{"관심과 표현" if rich else "질문과 대답"}</div>',
         '<div style="margin-top:44px;display:flex;flex-direction:column;gap:38px">']
    for i, (a, b) in enumerate(rows):
        arrow = "&rarr;" if i % 2 == 0 else "&larr;"
        h.append('<div style="display:flex;align-items:center;gap:60px;font-weight:800;'
                 'font-size:62px;text-shadow:0 3px 18px rgba(0,0,0,.7)">'
                 f'<span style="width:190px;text-align:right">{esc(a)}</span>'
                 f'<span class="pp-arrow" style="color:{col};font-size:66px">{arrow}</span>'
                 f'<span style="width:190px">{esc(b)}</span></div>')
    h.append("</div></div>")
    return "".join(h)


GRAPHICS = {
    "g_cover_anxiety": lambda: g_rows("질문으로 덮고 있는 것", ["어색함", "불안", "재미없어 하나?"], mark="q"),
    "g_question_chain": lambda: g_chain(["질문", "대답", "질문", "대답"]),
    "g_info_known": lambda: g_rows("알게 된 것", ["직업", "취미", "사는 곳"]),
    "g_info_known2": lambda: g_rows("알게 된 것", ["직업", "취미", "사는 곳", "주말"]),
    "g_info_unknown": lambda: g_rows("모르는 것", ["왜 좋아하는지", "어떤 감정인지", "무엇을 중요하게 보는지"], mark="q"),
    "g_info_questions": lambda: g_rows("정보 질문", ["몇 킬로미터", "일주일에 몇 번", "어디서", "마라톤"], muted=(0, 1, 2, 3)),
    "g_depth_flat": lambda: g_bars("대화의 깊이", [("사실", .92, "cool-hot"), ("감정", .10, "cool"), ("생각", .07, "cool"), ("가치관", .05, "cool")]),
    "g_depth_layers": lambda: g_bars("대화의 깊이", [("사실", .34, "cool"), ("감정", .58, "cool"), ("생각", .78, "cool"), ("가치관", .96, "cool-hot")]),
    "g_loop": lambda: fig_loop4(),
    "g_loop_full": lambda: fig_loop4(),
    "g_purpose": lambda: g_twobranch("질문을 하는 목적", "진짜 궁금해서", "어색함을 없애려고"),
    "g_gap_ok": lambda: g_gap("ok"),
    "g_fill_gap": lambda: g_gap("fill"),
    "g_discard": lambda: g_rows("대화가 끊기는 이유", ["새로운 질문이 없어서", "방금 한 말을 너무 빨리 버려서"], muted=(0,)),
    "g_highlight": lambda: g_chips("이 한 문장 안에", ["주말", "집", "친구", "성수", "카페"], hot=("성수", "카페")),
    "g_tags1": lambda: g_chips(None, ["주말", "집에서 쉬는 것", "친구", "성수", "카페"]),
    "g_tags2": lambda: g_chips(None, ["내향? 외향?", "어떤 카페", "친구와 보내는 시간"]),
    "g_tags3": lambda: g_chips("그 문장 안에", ["사실", "감정", "이유", "취향", "가치관"], hot=("감정", "가치관")),
    "g_three_lane": lambda: g_lanes(),
    "g_less_words": lambda: g_twobranch("말을 줄이면?", "질문을 덜 한다", "자기 표현을 넣는다"),
    "g_q_then_self": lambda: g_chain(["질문", "대답", "내 생각"]),
    "g_three_beats": lambda: g_chain(["침묵", "불안", "질문"]),
    "g_add_self": lambda: g_chain(["관심", "표현", "관심", "표현"]),
    "g_pingpong_flat": lambda: g_pingpong(False),
    "g_pingpong_rich": lambda: g_pingpong(True),
    "g_bar_compare": lambda: g_bars("소개팅에서 한 말", [("공백을 채우는 말", .88, "hot"), ("나를 보여주는 말", .16, "calm")], axis=("적음", "많음")),
    "g_not_seen": lambda: g_rows(None, ["질문은 많았다", "당신은 보이지 않았다"], muted=(0,)),
    "g_step1": lambda: g_rows("첫 번째", ["바로 다음 질문을 던지지 않기", "2초만 더 있어보기"]),
    "g_step3": lambda: g_rows("세 번째", ["질문만 하지 않기", "내 생각을 하나 붙이기"]),
    "g_stack": lambda: g_stack(),
    "g_check1": lambda: g_rows("코칭에서 같이 보는 것", ["언제 말이 빨라지는지", "반응이 약해지면 어떻게 하는지"]),
    "g_check2": lambda: g_rows("코칭에서 같이 보는 것", ["침묵이 생겼을 때", "얼마나 급하게 메우는지"]),
    "g_signs1": lambda: g_rows("불안이 드러나는 방식", ["계속 질문한다", "과하게 설명한다"]),
    "g_signs2": lambda: g_rows("불안이 드러나는 방식", ["말실수를 급하게 수습한다", "선택권을 계속 넘긴다"]),
    "g_two_branch": lambda: g_twobranch("지금 이 말은", "정말 궁금해서", "침묵이 무서워서"),
}



# ── spec-driven graphics ────────────────────────────────────────────────────
# A plan can name a graphic inline instead of registering it above:
#   rows:제목|a;b;c|q|muted   chips:제목|a;b|hot;hot   chain:a;b;c
#   two:제목|왼쪽|오른쪽      bars:제목|라벨:0.8:tone;...|왼축;오른축
#   checks:제목|a;b          nots:제목|a;b              steps:a;b;c;d
#   vs:왼머리|a;b|오른머리|c;d   react:조건=행동;...    thread:w=말;m=말
#   echo:말
# Elements marked `seq` reveal on the narration lines the scene spans.
def _sp(x):
    return [t.strip() for t in x.split(";") if t.strip()]


def g_seqrows(title, items, flag=""):
    h = ['<div class="stage"><div class="scrim wide"></div>']
    if title:
        h.append(f'<div class="hl md gtitle">{esc(title)}</div>')
    h.append('<div class="rows" style="margin-top:46px">')
    for it in items:
        cls = "row seq" + (" muted" if flag == "muted" else "")
        extra = '<span class="qmark">?</span>' if flag == "q" else ""
        h.append(f'<div class="{cls}"><i class="tick"></i><span>{esc(it)}</span>{extra}</div>')
    h.append("</div></div>")
    return "".join(h)


def g_checks(title, items):
    h = ['<div class="stage"><div class="scrim wide"></div>',
         f'<div class="hl md gtitle">{esc(title)}</div>' if title else '',
         '<div class="rows" style="margin-top:46px">']
    for it in items:
        h.append('<div class="row seq" style="color:var(--ink)"><svg class="ck" width="56" height="56" '
                 'viewBox="0 0 56 56"><circle cx="28" cy="28" r="26" fill="#5AD8F7"/>'
                 '<path d="M16 29l8 8 16-17" stroke="#0B0B0D" stroke-width="6" fill="none" '
                 f'stroke-linecap="round" stroke-linejoin="round"/></svg><span>{esc(it)}</span></div>')
    h.append("</div></div>")
    return "".join(h)


def g_nots(title, items):
    h = ['<div class="stage"><div class="scrim wide"></div>',
         f'<div class="hl md gtitle">{esc(title)}</div>' if title else '',
         '<div class="chips" style="margin-top:56px;gap:60px">']
    for it in items:
        h.append(f'<span class="chip seq nx">{esc(it)}<svg class="strike sm" viewBox="0 0 100 100">'
                 '<line x1="14" y1="14" x2="86" y2="86"/><line x1="14" y1="86" x2="86" y2="14"/></svg></span>')
    h.append("</div></div>")
    return "".join(h)


def g_steps(items):
    h = ['<div class="stage"><div class="scrim wide"></div><div class="steps">']
    for k, it in enumerate(items):
        if k:
            h.append('<i class="step-line"></i>')
        h.append(f'<div class="step seq"><div class="step-n">{k+1}</div>'
                 f'<div class="step-t">{esc(it)}</div></div>')
    h.append("</div></div>")
    return "".join(h)


def g_vs(lh, litems, rh, ritems):
    h = ['<div class="stage"><div class="scrim wide"></div><div class="vs">',
         f'<div class="vs-row"><div class="vs-h">{esc(lh)}</div><div class="vs-mid"></div>'
         f'<div class="vs-h hot">{esc(rh)}</div></div>']
    for a, b in zip(litems, ritems):
        h.append(f'<div class="vs-row vrow seq"><div class="vs-c">{esc(a)}</div>'
                 f'<div class="vs-mid">&rarr;</div><div class="vs-c hot">{esc(b)}</div></div>')
    h.append("</div></div>")
    return "".join(h)


def g_react(pairs):
    h = ['<div class="stage"><div class="scrim wide"></div>',
         '<div class="hl md gtitle">상대 반응을 보면서</div>',
         '<div class="rows" style="margin-top:46px;gap:30px">']
    for a, _, b in (p.partition("=") for p in pairs):
        h.append(f'<div class="row seq"><span style="color:var(--ink)">{esc(a)}</span>'
                 f'<span class="arrow" style="color:var(--cyan);font-weight:800">&rarr;</span>'
                 f'<span style="color:var(--amber);font-weight:700">{esc(b)}</span></div>')
    h.append("</div></div>")
    return "".join(h)


def g_thread(msgs):
    h = ['<div class="stage"><div class="thread">']
    for m in msgs:
        who, _, txt = m.partition("=")
        h.append(f'<div class="tb-row {"r" if who == "m" else "l"}">'
                 f'<div class="tb seq {who}">{esc(txt)}</div></div>')
    h.append("</div></div>")
    return "".join(h)


def g_echo(word):
    spots = ((0, 0, 1.0, 1.0), (-420, -190, .82, .72), (430, -150, .78, .62),
             (-360, 200, .7, .5), (400, 220, .64, .42), (20, -300, .56, .32))
    h = ['<div class="stage">']
    for k, (x, y, sc, op) in enumerate(spots):
        h.append(f'<div class="eb-wrap" style="transform:translate({x}px,{y}px) scale({sc});opacity:{op}">'
                 f'<div class="eb">{esc(word)}</div></div>')
    h.append("</div>")
    return "".join(h)


def g_spec(spec):
    tmpl, _, rest = spec.partition(":")
    f = rest.split("|")
    if tmpl == "rows":
        return g_seqrows(f[0], _sp(f[1]), f[2] if len(f) > 2 else "")
    if tmpl == "chips":
        return g_chips(f[0] or None, _sp(f[1]), hot=tuple(_sp(f[2])) if len(f) > 2 else ())
    if tmpl == "chain":
        return g_chain(_sp(rest))
    if tmpl == "two":
        return g_twobranch(f[0], f[1], f[2])
    if tmpl == "bars":
        data = [(a, float(b), c) for a, b, c in (x.split(":") for x in _sp(f[1]))]
        return g_bars(f[0], data, axis=tuple(_sp(f[2])) if len(f) > 2 else ("얕음", "깊음"))
    if tmpl == "checks":
        return g_checks(f[0], _sp(f[1]))
    if tmpl == "nots":
        return g_nots(f[0], _sp(f[1]))
    if tmpl == "steps":
        return g_steps(_sp(rest))
    if tmpl == "vs":
        return g_vs(f[0], _sp(f[1]), f[2], _sp(f[3]))
    if tmpl == "react":
        return g_react(_sp(rest))
    if tmpl == "thread":
        return g_thread(_sp(rest))
    if tmpl == "echo":
        return g_echo(rest)
    raise KeyError(f"unknown graphic spec {spec!r}")

# ── scene builders ──────────────────────────────────────────────────────────
def src(key):
    """Asset URL. Keyed figures carry a whole URL; the originals are CDN names."""
    v = IMG[key]
    return v if v.startswith("http") else CDN + v


_ROT = {}


def pick(alias, i):
    """Round-robin over the alias pool.

    `i % len(opts)` looked like rotation but the scene indices for a given
    alias were near-uniformly congruent, so one variant carried almost every
    use of it. A per-alias counter spreads them evenly instead — with the
    widened pools that holds every still to at most two appearances.
    """
    opts = ALIAS[alias]
    n = _ROT.get(alias, 0)
    _ROT[alias] = n + 1
    return opts[n % len(opts)]


def background(i, kind, arg, section):
    """Return (css_class, inner_html). Photos own their own plate."""
    if kind == "B":
        key = pick(arg, i)
        return "bg-photo", (f'<img id="ph{i:03d}" src="{src(key)}" alt="">'
                            f'<div class="tint"></div>')
    fam = FAMILIES[(section * 3 + i // 2) % len(FAMILIES)]
    # never three alike in a row
    if i >= 2 and fam == background.prev[-1] == background.prev[-2]:
        fam = FAMILIES[(FAMILIES.index(fam) + 3) % len(FAMILIES)]
    inner = f'<div class="motes">{motes(i)}</div>' if fam == "bg-dust" else ""
    return fam, inner


background.prev = ["", ""]


def content(i, kind, arg, line):
    sid = f"fg{i:03d}"
    if kind == "B":
        return ""
    if kind == "C":
        who, _, _bg = arg.partition("@")
        names = who.split("+")
        # each figure gets its own column and centres inside it, so nothing
        # depends on a transform the entrance tween will overwrite
        cols = ["left:0;right:0"] if len(names) == 1 else ["left:0;width:50%",
                                                          "left:50%;width:50%"]
        h = []
        for n, col in zip(names, cols):
            key = pick(n, i)
            sc = 1.0 if len(names) == 1 else 0.82
            h.append(f'<div class="cut" style="{col}">'
                     f'<img id="{sid}-c{len(h)}" class="shadowed" '
                     f'src="{src(key)}" alt="" '
                     f'style="height:{int(820*sc)}px"></div>')
        return "".join(h)
    if kind == "I":
        key, _, badge = arg.partition("|")
        h = [f'<div class="stage"><div class="scrim tight"></div>'
             f'<img id="{sid}-ic" class="icon3d" src="{src(pick(key, i))}" alt="" '
             f'style="width:560px;height:auto;filter:drop-shadow(0 22px 40px rgba(0,0,0,.6))">']
        if badge:
            h.append(f'<div class="hl md" style="margin-top:26px">{esc(badge)}</div>')
        h.append("</div>")
        return "".join(h)
    if kind == "N":
        key, _, params = arg.partition(":")
        name = NEON_FIG.get(key, key)
        if name == "qmarks":
            body = fig_qmarks(i)
        elif name == "tree" and "|" in params:
            root, _, items = params.partition("|")
            body = fig_tree(_sp(items), root)
        else:
            body = FIGS[name](*(_sp(params) if params else []))
        return f'<div class="diag"><div class="scrim wide"></div>{body}</div>'
    if kind == "P":
        mark, _, txt = arg.partition("|")
        words = txt or line
        size = "xl" if len(words) <= 14 else ("lg" if len(words) <= 26 else "md")
        return (f'<div class="stage"><div class="scrim wide"></div>'
                f'<div class="pmark">{picto(mark, 252)}</div>'
                f'<div class="hl {size}" style="margin-top:34px">{esc(words)}</div></div>')
    if kind == "T":
        txt = arg if arg else line
        parts = [p for p in txt.split("|") if p.strip()]
        size = "xl" if (len(parts) == 1 and len(parts[0]) <= 14) else "lg"
        h = ['<div class="stage"><div class="scrim wide"></div>']
        for p in parts:
            h.append(f'<div class="hl {size}">{esc(p)}</div>')
        h.append("</div>")
        return "".join(h)
    if kind == "K":
        crossed = arg.endswith("x")
        who = arg[0]
        side = "right" if who == "m" else "left"
        tag = "남자" if who == "m" else ("여자" if who == "w" else "내담자")
        strike = ('<svg class="strike" viewBox="0 0 100 100">'
                  '<line x1="10" y1="10" x2="90" y2="90"/><line x1="10" y1="90" x2="90" y2="10"/>'
                  '</svg>') if crossed else ""
        said = line.strip().strip('"\u201c\u201d')
        return (f'<div class="bub-row {side}"><div class="bub {who}">'
                f'<span class="who" data-layout-allow-overflow>{esc(tag)}</span>{esc(said)}{strike}</div></div>')
    if kind == "H":
        num, _, word = arg.partition("|")
        label = num[1:] if num.startswith("n") else (num.lstrip("0") or num)
        return (f'<div class="stage"><div class="scrim"></div>'
                f'<div class="pearl">{esc(label)}</div>'
                f'<div class="chap-word">{esc(word)}</div></div>')
    if kind == "G":
        fn = GRAPHICS.get(arg)
        body = fn() if fn else g_spec(arg)
        if arg in ("g_loop", "g_loop_full"):
            return f'<div class="diag"><div class="scrim wide"></div>{body}</div>'
        return body
    return ""


# ── main ────────────────────────────────────────────────────────────────────
def main():
    audio = None
    if "--audio" in sys.argv:
        audio = sys.argv[sys.argv.index("--audio") + 1]

    raw = open(os.path.join(PROJECT, "timings.txt"), encoding="utf-8").read()
    total = float(raw.split("TOTAL ")[1].split()[0])
    times = [tuple(float(x) for x in p.split(","))
             for p in raw.split("TIMES ")[1].split()]
    if hasattr(_plan, "LINES"):
        lines, chunk_of = _plan.LINES, _plan.SECTION
    else:
        chunks = json.load(open(os.path.join(PROJECT, "chunks.json"), encoding="utf-8"))
        lines = [l for c in chunks for l in c["lines"]]
        chunk_of = [si for si, c in enumerate(chunks) for _ in c["lines"]]
    assert len(lines) == len(times) == len(PLAN), (len(lines), len(times), len(PLAN))

    # "+" lines hand their time to the next scene, "=" lines to the previous
    # one; every other line owns a scene of its own.
    owner = [None] * len(PLAN)
    for i, (kind, _) in enumerate(PLAN):
        if kind == "=":
            owner[i] = owner[i - 1]
        elif kind != "+":
            owner[i] = i
    for i in range(len(PLAN) - 1, -1, -1):
        if PLAN[i][0] == "+":
            owner[i] = owner[i + 1]
    span, seq = {}, {}
    for i, o in enumerate(owner):
        t0, t1 = times[i]
        a0, a1 = span.get(o, (t0, t1))
        span[o] = (min(a0, t0), max(a1, t1))
        if PLAN[i][0] != "+":
            seq.setdefault(o, []).append(round(t0, 2))

    # rule 4: no image or diagram more than twice in the film
    from collections import Counter
    use = Counter()
    for kind, arg in PLAN:
        if kind == "P":
            use["P:" + arg.partition("|")[0]] += 1
        elif kind == "N":
            use["N:" + arg.partition(":")[0]] += 1
    over = {k: v for k, v in use.items() if v > 2}
    assert not over, f"used more than twice: {over}"

    bg_html, fg_html, cap_html, anim, cap_t = [], [], [], [], []
    cap_n = 0
    for i, ((kind, arg), line) in enumerate(zip(PLAN, lines)):
        if owner[i] == i:
            t0, t1 = span[i]
            # the next scene's start is this one's end, so plates never gap
            nxt = min((span[o][0] for o in span if span[o][0] > t0), default=total)
            d = max(0.4, nxt - t0)
            fam, inner = background(i, kind, arg, chunk_of[i])
            background.prev.append(fam)
            bg_html.append(
                f'<div class="clip" id="bgc{i:03d}" data-start="{t0:.2f}" '
                f'data-duration="{d:.2f}" data-track-index="0">'
                f'<div class="layer"><div class="bgmove {fam}" id="bgm{i:03d}" data-layout-allow-overflow>{inner}</div>'
                f'<div class="grain"></div><div class="vig"></div></div></div>')
            body = content(i, kind, arg, line)
            if body:
                fg_html.append(
                    f'<div class="clip" id="fg{i:03d}" data-start="{t0:.2f}" '
                    f'data-duration="{d:.2f}" data-track-index="1">{body}</div>')
            anim.append({"i": i, "t": round(t0, 2), "d": round(d, 2), "k": kind,
                         "has": bool(body), "q": seq.get(i, [])})

        # Review note: where the sentence is already on screen — set large
        # across the middle, or written inside a quote bubble — repeating it
        # along the bottom just stacks the same words on themselves. A centre
        # line that only boils the sentence down keeps its caption.
        if kind in ("H", "K"):
            continue
        if kind in ("T", "P"):
            shown = arg.partition("|")[2] if kind == "P" else arg
            if not shown or shown.replace("|", " ").strip() == line.strip():
                continue

        t0, t1 = times[i]
        d = t1 - t0
        cards = caption_cards(line)
        per = d / len(cards)
        for j, c in enumerate(cards):
            cs, cd = t0 + j * per, per
            cap_html.append(
                f'<div class="clip" id="cap{cap_n:03d}" data-start="{cs:.2f}" '
                f'data-duration="{cd:.2f}" data-track-index="2">'
                f'<div class="cap-wrap"><div class="cap-scrim" data-layout-allow-overflow></div>'
                f'<div class="cap">{esc(c)}</div></div></div>')
            cap_t.append(round(cs, 2))
            cap_n += 1

    css = open(os.path.join(HERE, "style.css"), encoding="utf-8").read()
    wm = getattr(_plan, "WATERMARK", "이다사")
    audio_tag = (f'\n  <audio id="vo" src="{audio}" data-start="0"></audio>' if audio else "")

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
<div id="root" data-composition-id="main" data-width="{W}" data-height="{H}"
     data-start="0" data-duration="{total:.3f}">
{chr(10).join(bg_html)}
{chr(10).join(fg_html)}
{chr(10).join(cap_html)}
  <div class="clip" id="wmclip" data-start="0" data-duration="{total:.3f}" data-track-index="3">
    <div class="wm">{esc(wm)}</div>
  </div>{audio_tag}
</div>
<script>
var tl = gsap.timeline({{ paused: true }});

// Tween only what exists — recipes are shared across scene kinds, and GSAP
// logs a console warning for every selector that matches nothing.
function T(sel, from, to, at) {{
  if (!document.querySelector(sel)) return;
  tl.fromTo(sel, from, to, at);
}}
var SC = {json.dumps(anim, separators=(",", ":"))};
var CAPT = {json.dumps(cap_t, separators=(",", ":"))};

// plates drift so no frame is ever dead still
SC.forEach(function (s) {{
  var id = "#bgm" + String(s.i).padStart(3, "0");
  var dir = (s.i % 2) ? 1 : -1;
  var span = Math.min(s.d, 8);
  tl.fromTo(id, {{ scale: 1.0, xPercent: 0 }},
            {{ scale: 1.045, xPercent: dir * 0.9, duration: span,
               ease: "sine.inOut" }}, s.t);
}});

// content entrances, one recipe per scene kind
SC.forEach(function (s) {{
  if (!s.has) return;
  var f = "#fg" + String(s.i).padStart(3, "0"), t = s.t + 0.08;
  var dur = Math.min(0.62, Math.max(0.34, s.d * 0.34));
  if (s.k === "T") {{
    T(f + " .hl", {{ yPercent: 42, opacity: 0 }},
              {{ yPercent: 0, opacity: 1, duration: dur, ease: "power3.out",
                 stagger: 0.09 }}, t);
  }} else if (s.k === "K") {{
    T(f + " .bub", {{ scale: 0.93, opacity: 0, yPercent: 10 }},
              {{ scale: 1, opacity: 1, yPercent: 0, duration: dur,
                 ease: "back.out(1.5)" }}, t);
    T(f + " .who", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.3,
              ease: "power1.out" }}, t + 0.14);
  }} else if (s.k === "H") {{
    T(f + " .pearl", {{ scale: 0.3, opacity: 0 }},
              {{ scale: 1, opacity: 1, duration: 0.6, ease: "back.out(1.7)" }}, t);
    T(f + " .chap-word", {{ yPercent: 50, opacity: 0 }},
              {{ yPercent: 0, opacity: 1, duration: 0.55, ease: "power3.out" }}, t + 0.18);
  }} else if (s.k === "C") {{
    T(f + " .cut", {{ yPercent: 8, opacity: 0 }},
              {{ yPercent: 0, opacity: 1, duration: dur, ease: "power2.out",
                 stagger: 0.12 }}, t);
  }} else if (s.k === "I") {{
    T(f + " .icon3d", {{ scale: 0.86, opacity: 0 }},
              {{ scale: 1, opacity: 1, duration: dur, ease: "back.out(1.3)" }}, t);
    T(f + " .hl", {{ opacity: 0, yPercent: 30 }},
              {{ opacity: 1, yPercent: 0, duration: 0.42, ease: "power2.out" }}, t + 0.2);
    var fl = Math.max(0, Math.floor((s.d - dur - 0.2) / 1.6) - 1);
    if (fl > 0 && document.querySelector(f + " .icon3d")) tl.to(f + " .icon3d", {{ yPercent: -2.2, duration: 0.8,
                ease: "sine.inOut", yoyo: true, repeat: fl }}, t + dur + 0.1);
  }} else if (s.k === "P") {{
    T(f + " .pmark", {{ opacity: 0, scale: 0.7, rotation: -6 }},
              {{ opacity: 1, scale: 1, rotation: 0, duration: 0.55, ease: "back.out(1.7)" }}, t);
    T(f + " .hl", {{ opacity: 0, yPercent: 34 }},
              {{ opacity: 1, yPercent: 0, duration: 0.46, ease: "power3.out" }}, t + 0.16);
    var pb = Math.max(0, Math.floor((s.d - 0.8) / 1.8) - 1);
    if (pb > 0 && document.querySelector(f + " .pmark"))
      tl.to(f + " .pmark", {{ yPercent: -4, duration: 0.9, ease: "sine.inOut",
                              yoyo: true, repeat: pb }}, t + 0.6);
  }} else if (s.k === "N") {{
    T(f + " svg", {{ scale: 0.94, opacity: 0 }},
              {{ scale: 1, opacity: 1, duration: dur, ease: "power2.out" }}, t);
    // strokes marked fg-draw trace themselves in
    document.querySelectorAll(f + " .fg-draw, " + f + " .fg-draw2").forEach(function (el, k) {{
      var L = el.getTotalLength ? el.getTotalLength() : 0;
      if (!L) return;
      tl.fromTo(el, {{ strokeDasharray: L, strokeDashoffset: L }},
                {{ strokeDashoffset: 0, duration: Math.min(1.4, s.d * 0.5),
                   ease: "power2.inOut" }}, t + 0.1 + k * 0.25);
    }});
    T(f + " .fg-pop", {{ scale: 0, transformOrigin: "50% 50%" }},
              {{ scale: 1, duration: 0.5, ease: "back.out(2)" }}, t + 0.5);
    T(f + " .fg-fill", {{ scaleY: 0, transformOrigin: "50% 100%" }},
              {{ scaleY: 1, duration: 0.9, ease: "power2.out" }}, t + 0.3);
  }} else if (s.k === "G") {{
    T(f + " .gtitle", {{ yPercent: 40, opacity: 0 }},
              {{ yPercent: 0, opacity: 1, duration: 0.45, ease: "power3.out" }}, t);
    var sq = document.querySelectorAll(f + " .seq"), n = sq.length, q = s.q;
    if (n > 1 && q.length > 1 && (q.length === n || q.length % n === 0)) {{
      // one element per narration line the scene spans
      var step = q.length / n;
      for (var k = 0; k < n; k++) {{
        tl.fromTo(sq[k], {{ yPercent: 30, opacity: 0, scale: 0.97 }},
                  {{ yPercent: 0, opacity: 1, scale: 1, duration: 0.42,
                     ease: "power3.out" }}, Math.max(t, q[k * step] + 0.05));
      }}
    }} else {{
      T(f + " .row, " + f + " .chip, " + f + " .bars > div, " + f + " .stk, " +
        f + " .tb, " + f + " .step, " + f + " .vrow",
                {{ yPercent: 36, opacity: 0 }},
                {{ yPercent: 0, opacity: 1, duration: 0.46, ease: "power3.out",
                   stagger: Math.min(0.22, Math.max(0.06, (s.d * 0.55) / Math.max(n, 1))) }}, t + 0.14);
    }}
    T(f + " .eb", {{ scale: 0.6, opacity: 0 }},
              {{ scale: 1, opacity: 1, duration: 0.4, ease: "back.out(1.8)",
                 stagger: 0.12 }}, t);
    T(f + " .step-line", {{ scaleX: 0 }},
              {{ scaleX: 1, duration: 0.5, ease: "power2.out", stagger: 0.2 }}, t + 0.2);
    T(f + " .bar-fill", {{ scaleX: 0 }},
              {{ scaleX: 1, duration: 0.7, ease: "expo.out", stagger: 0.1 }}, t + 0.26);
    T(f + " svg", {{ opacity: 0, scale: 0.95 }},
              {{ opacity: 1, scale: 1, duration: dur, ease: "power2.out" }}, t);
    T(f + " .pmark", {{ opacity: 0, scale: 0.84 }},
              {{ opacity: 1, scale: 1, duration: 0.52, ease: "back.out(1.6)" }}, t + 0.06);
    T(f + " .hl, " + f + " .sub, " + f + " .gapline",
              {{ opacity: 0, yPercent: 26 }},
              {{ opacity: 1, yPercent: 0, duration: 0.46, ease: "power2.out",
                 stagger: 0.08 }}, t + 0.1);
  }}
}});

// captions: one line, fading up at each card's own start
CAPT.forEach(function (ct, c) {{
  var cid = "#cap" + String(c).padStart(3, "0") + " .cap";
  tl.fromTo(cid, {{ opacity: 0, yPercent: 26 }},
            {{ opacity: 1, yPercent: 0, duration: 0.22, ease: "power2.out" }}, ct);
}});

window.__timelines["main"] = tl;
</script>
</body>
</html>
"""
    open(OUT, "w", encoding="utf-8").write(doc)
    print(f"wrote {OUT}")
    print(f"  duration {total:.2f}s · scenes {len(PLAN)} · caption cards {cap_n}")
    from collections import Counter
    print("  bg families:", dict(Counter(background.prev[2:])))


if __name__ == "__main__":
    main()
