# -*- coding: utf-8 -*-
"""Write ../index.html — the full 602s composition.

    python3 src/emit.py [--audio assets/audio/master.wav]

Tracks: 0 backgrounds · 1 content · 2 captions · 3 watermark.
"""
import html
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
# Project data (plan.py, chunks.json, timings.txt) lives in its own folder so
# the engine in src/ stays shared between films: PROJECT=examples/<name>.
PROJECT = os.path.abspath(os.environ.get("PROJECT", HERE))
sys.path.insert(0, PROJECT)
from build import (W, H, CDN, IMG, ALIAS, NEON_FIG, FAMILIES,   # noqa: E402
                   esc, caption_cards, motes, text_w, font, CAP_MAX)
import figs2 as F2                                               # noqa: E402
import plan as P                                                 # noqa: E402

IMG.update(getattr(P, "ASSETS", {}))
ALIAS.update(getattr(P, "ALIASES", {}))
OUT = os.path.join(HERE, "..", "index.html")


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

def fig_surge():
    """A flat line that spikes — 불안이 확 올라오는 순간."""
    d = ("M60 400 L360 400 L430 396 L500 404 L560 398 "
         "C 640 396, 690 330, 740 160 C 770 62, 800 60, 830 150 "
         "C 870 268, 920 330, 1000 344 L1180 344")
    return ('<svg width="1240" height="520" viewBox="0 0 1240 520">'
            f'<path class="edge" d="M60 400 L1180 400" opacity=".35"/>'
            f'<path class="edge-hot glow fg-draw" d="{d}"/>'
            '<circle class="node glow fg-pop" cx="830" cy="98" r="14"/>'
            f'<text class="dlabel" x="830" y="48" text-anchor="middle">불안</text>'
            '</svg>')


def fig_meter(level=0.82):
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
            + '<text class="dlabel" x="560" y="120" text-anchor="start">불안</text>'
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


def fig_bridge():
    """Two banks joined — 대화가 사람 얘기로 건너갑니다."""
    return ('<svg width="1320" height="480" viewBox="0 0 1320 480">'
            '<rect x="40" y="300" width="330" height="120" rx="12" '
            'fill="rgba(90,216,247,.07)" stroke="#1E7C96" stroke-width="3"/>'
            '<rect x="950" y="300" width="330" height="120" rx="12" '
            'fill="rgba(90,216,247,.07)" stroke="#1E7C96" stroke-width="3"/>'
            '<path class="edge-hot glow fg-draw" d="M370 300 C 560 140, 760 140, 950 300"/>'
            + '<text class="dlabel-dim" x="205" y="380" text-anchor="middle">정보</text>'
            '<text class="dlabel" x="1115" y="380" text-anchor="middle">사람</text>'
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


def fig_weave():
    """Two strands crossing in turn — 관심, 그리고 표현."""
    a = "M80 240 C 260 60, 440 60, 620 240 S 980 420, 1160 240"
    b = "M80 240 C 260 420, 440 420, 620 240 S 980 60, 1160 240"
    return ('<svg width="1240" height="500" viewBox="0 0 1240 500">'
            f'<path class="edge-hot glow fg-draw" d="{a}"/>'
            f'<path class="edge glow fg-draw2" d="{b}" stroke="#D8B368"/>'
            '<circle class="node glow" cx="620" cy="240" r="13"/>'
            '<text class="dlabel" x="80" y="150" text-anchor="start">관심</text>'
            '<text class="dlabel" x="1160" y="150" text-anchor="end">표현</text>'
            '</svg>')


def fig_pendulum():
    """One weight, two ends — 다시 상대에게, 다시 나에게."""
    return ('<svg width="1180" height="540" viewBox="0 0 1180 540">'
            '<circle class="node-dim" cx="590" cy="70" r="12"/>'
            '<path class="edge" d="M250 400 A 400 400 0 0 1 930 400" opacity=".4"/>'
            '<path class="edge-hot glow" d="M590 70 L288 352"/>'
            '<path class="edge glow" d="M590 70 L892 352" opacity=".45"/>'
            '<circle class="node glow fg-pop" cx="288" cy="352" r="30"/>'
            '<circle class="node-dim glow" cx="892" cy="352" r="22"/>'
            '<text class="dlabel" x="288" y="452" text-anchor="middle">상대</text>'
            '<text class="dlabel-dim" x="892" y="444" text-anchor="middle">나</text>'
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


def fig_split():
    """One line separating into two named tracks — 그걸 구분하기 시작하면."""
    return ('<svg width="1280" height="500" viewBox="0 0 1280 500">'
            '<path class="edge-hot glow" d="M70 250 L430 250"/>'
            '<circle class="node glow" cx="430" cy="250" r="15"/>'
            '<path class="edge-hot glow fg-draw" d="M430 250 C 640 250, 700 120, 940 120"/>'
            '<path class="edge glow fg-draw2" d="M430 250 C 640 250, 700 380, 940 380" '
            'stroke="#D8B368"/>'
            '<text class="dlabel" x="980" y="138" text-anchor="start">관심</text>'
            '<text class="dlabel" x="980" y="398" text-anchor="start">표현</text>'
            '</svg>')


def fig_twocheck():
    """Two things you can now do — 관심도, 내 생각도."""
    rows = []
    for k, (lab, y) in enumerate((("상대에게 관심을", 170), ("내 생각을 보여주기", 340))):
        rows.append(f'<circle class="node glow" cx="230" cy="{y}" r="26"/>')
        rows.append(f'<path d="M212 {y} l14 16 l26 -32" stroke="#0B0B0D" stroke-width="7" '
                    'fill="none" stroke-linecap="round" stroke-linejoin="round"/>')
        rows.append(f'<text class="dlabel" x="300" y="{y+16}" text-anchor="start">{lab}</text>')
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


def fig_tree(items=("사실", "감정", "이유", "취향")):
    """One sentence holding several topics — 소재가 세 개, 네 개."""
    s = ['<svg width="1300" height="540" viewBox="0 0 1300 540">',
         '<rect x="60" y="216" width="330" height="108" rx="18" '
         'fill="rgba(255,255,255,.08)" stroke="rgba(255,255,255,.22)" stroke-width="3"/>',
         '<text class="dlabel-dim" x="225" y="286" text-anchor="middle">한 문장</text>']
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


def fig_lens():
    """A magnifier held over the sentence — 그 문장 안에 뭐가 있는지."""
    bars = "".join(f'<rect x="{200+k*0}" y="{212+k*54}" width="{760-k*150}" height="20" '
                   f'rx="10" fill="rgba(255,255,255,{0.20-k*0.05:.2f})"/>' for k in range(3))
    return ('<svg width="1260" height="520" viewBox="0 0 1260 520">'
            + bars
            + '<circle cx="800" cy="256" r="168" fill="rgba(90,216,247,.07)" '
            'stroke="#5AD8F7" stroke-width="7" class="glow fg-pop"/>'
            '<path d="M918 374 L1060 516" stroke="#5AD8F7" stroke-width="18" '
            'stroke-linecap="round" class="glow"/>'
            '<text class="dlabel" x="800" y="274" text-anchor="middle">감정</text>'
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


def fig_elapsed():
    """A long stretch of talking with nothing learned — 한 시간 넘게."""
    ticks = "".join(f'<path class="edge" d="M{120+k*115} 250 L{120+k*115} '
                    f'{200 if k % 4 == 0 else 224}" opacity=".5"/>' for k in range(11))
    return ('<svg width="1320" height="440" viewBox="0 0 1320 440">'
            '<path class="edge" d="M120 250 L1270 250" opacity=".55"/>' + ticks
            + '<path class="edge-hot glow fg-draw" d="M120 250 L1270 250"/>'
            '<circle class="node glow fg-pop" cx="1270" cy="250" r="14"/>'
            '<text class="dlabel-dim" x="120" y="340" text-anchor="start">시작</text>'
            '<text class="dlabel" x="1270" y="340" text-anchor="end">한 시간 뒤</text>'
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
    "office":   '<rect x="46" y="40" width="100" height="126" rx="8"/>'
                '<path d="M70 68h14M108 68h14M70 96h14M108 96h14M70 124h14M108 124h14"/>'
                '<path d="M84 166v-22h24v22"/>',
    "friends":  '<circle cx="66" cy="70" r="20"/><circle cx="126" cy="70" r="20"/>'
                '<path d="M30 150q0-40 36-40t36 40"/><path d="M90 150q0-40 36-40t36 40"/>'
                '<path d="M84 34h24a8 8 0 0 1 8 8v10a8 8 0 0 1-8 8h-14l-8 8v-8h-2a8 8 0 0 1-8-8V42a8 8 0 0 1 8-8z" stroke="#D8B368"/>',
    "calc":     '<rect x="48" y="30" width="96" height="132" rx="14"/><rect x="64" y="46" width="64" height="30" rx="5"/>'
                '<circle cx="74" cy="100" r="5" fill="currentColor" stroke="none"/><circle cx="96" cy="100" r="5" fill="currentColor" stroke="none"/>'
                '<circle cx="118" cy="100" r="5" fill="currentColor" stroke="none"/><circle cx="74" cy="124" r="5" fill="currentColor" stroke="none"/>'
                '<circle cx="96" cy="124" r="5" fill="currentColor" stroke="none"/><circle cx="118" cy="124" r="5" fill="currentColor" stroke="none"/>'
                '<path d="M68 146h56"/>',
    "mirror":   '<rect x="30" y="44" width="58" height="104" rx="10"/>'
                '<rect x="104" y="44" width="58" height="104" rx="10" stroke="#D8B368"/>'
                '<path d="M96 30v132" stroke-dasharray="10 12"/>',
}


def picto(name, size=200):
    """One line-drawn mark in the shared stroke language."""
    return (f'<svg class="picto glow" width="{size}" height="{size}" viewBox="0 0 192 192" '
            'fill="none" stroke="currentColor" stroke-width="5.5" '
            f'stroke-linecap="round" stroke-linejoin="round">{_PICTO[name]}</svg>')


F2.picto = picto

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


# ── scene builders ──────────────────────────────────────────────────────────
LOCAL = os.environ.get("LOCAL_ASSETS") == "1"
MANIFEST = {}


def src(key):
    """Asset URL. Keyed figures carry a whole URL; the originals are CDN names.

    With LOCAL_ASSETS=1 the page points at assets/img/ instead and the URL is
    recorded for scripts/fetch_assets.py: remote multi-MB stills were not
    always decoded by the time a frame was captured, which left empty plates.
    """
    v = IMG[key]
    url = v if v.startswith("http") else CDN + v
    if not LOCAL:
        return url
    name = key + os.path.splitext(url)[1]
    MANIFEST["assets/img/" + name] = url
    return "assets/img/" + name


_ROT = {}


def pick(alias, i):
    """Round-robin over the alias pool (per-alias counter, see README)."""
    if alias not in ALIAS:
        return alias
    opts = ALIAS[alias]
    n = _ROT.get(alias, 0)
    _ROT[alias] = n + 1
    return opts[n % len(opts)]


LIFT = set(getattr(P, "LIFT", ()))     # stills shot too dark to sit as-is


def background(i, kind, arg):
    """Return (css_class, inner_html). Photos own their own plate."""
    if kind == "H" and arg.count("|") == 2:
        arg, kind = {"bg": arg.split("|")[2]}, "M"
    if kind == "B" or (kind == "M" and isinstance(arg, dict) and arg.get("bg")):
        key = pick(arg["img"] if kind == "B" else arg["bg"], i)
        cls = "lift" if key in LIFT else ""
        soft = " soft" if kind == "M" else ""
        return "bg-photo" + soft, (f'<img id="ph{i:03d}" class="{cls}" src="{src(key)}" alt="">'
                                   f'<div class="tint"></div>')
    fam = FAMILIES[(i * 5 + i // 3) % len(FAMILIES)]
    # never three alike in a row, never the same as the one just before
    if fam == background.prev[-1] or fam == background.prev[-2]:
        for k in range(1, len(FAMILIES)):
            alt = FAMILIES[(FAMILIES.index(fam) + k) % len(FAMILIES)]
            if alt != background.prev[-1] and alt != background.prev[-2]:
                fam = alt
                break
    inner = f'<div class="motes">{motes(i)}</div>' if fam == "bg-dust" else ""
    return fam, inner


background.prev = ["", ""]


def shown_texts(kind, arg):
    """Words a scene already puts on screen — their captions are dropped."""
    out = []
    if kind == "M":
        out += [m[2] for m in arg["msgs"]]
    if isinstance(arg, dict):
        out += [t for _, t in arg.get("tags", [])]
        out += arg.get("title", [])
    if kind == "K":
        out.append(arg.partition("|")[2])
    return out


def content(i, kind, arg, lines):
    sid = f"fg{i:03d}"
    line = lines[0]
    if kind == "B":
        h = []
        if arg.get("title"):
            h.append(f'<div class="ph-title {arg.get("tpos", "")}">' + "".join(
                f'<div class="hl lg"{F2.B(k)}>{esc(t)}</div>'
                for k, t in enumerate(arg["title"])) + '</div>')
        h.append(F2.tags_html(arg.get("tags", []), arg.get("tagpos")))
        return "".join(h)
    if kind == "M":
        return F2.thread(arg["msgs"], arg.get("title", ""), arg.get("tag"), arg.get("tagcls", ""))
    if kind == "C":
        if isinstance(arg, str):
            arg = {"who": arg}
        names = arg["who"].split("+")
        cols = ["left:0;right:0"] if len(names) == 1 else ["left:0;width:50%",
                                                          "left:50%;width:50%"]
        if arg.get("side"):            # figure left, words right
            cols = ["left:0;width:50%"]
        h = []
        for n, col in zip(names, cols):
            key = pick(n, i)
            sc = 1.0 if len(names) == 1 else 0.82
            h.append(f'<div class="cut" style="{col}">'
                     f'<img id="{sid}-c{len(h)}" class="shadowed" src="{src(key)}" alt="" '
                     f'style="height:{int(760*sc)}px"></div>')
        h.append(F2.tags_html(arg.get("tags", []), arg.get("tagpos")))
        return "".join(h)
    if kind == "I":
        key, _, badge = arg.partition("|")
        h = [f'<div class="stage"><div class="scrim tight"></div>'
             f'<div class="icwrap"><img id="{sid}-ic" class="icon3d" src="{src(pick(key, i))}" alt=""></div>']
        if badge:
            h.append(f'<div class="hl md badge" data-b="0">{esc(badge)}</div>')
        h.append("</div>")
        return "".join(h)
    if kind == "N":
        if callable(arg):
            return arg()
        fn = getattr(F2, arg, None)
        if fn:
            return fn()
        return (f'<div class="diag"><div class="scrim wide"></div>'
                f'{FIGS[NEON_FIG[arg]]() if NEON_FIG[arg] != "qmarks" else fig_qmarks(i)}</div>')
    if kind == "P":
        mark, _, txt = arg.partition("|")
        words = txt or line
        size = "xl" if len(words) <= 14 else ("lg" if len(words) <= 26 else "md")
        return (f'<div class="stage"><div class="scrim wide"></div>'
                f'<div class="pmark">{picto(mark, 252)}</div>'
                f'<div class="hl {size}" style="margin-top:34px">{esc(words)}</div></div>')
    if kind == "T":
        swap = isinstance(arg, dict)
        if swap:
            arg = arg["parts"]
        parts = arg if isinstance(arg, list) else [p for p in arg.split("|") if p.strip()]
        return F2.typo(parts, swap=swap)
    if kind == "K":
        who, _, txt = arg.partition("|")
        cls = {"m": "m", "w": "w"}.get(who, "n")
        side = {"m": "right", "w": "left"}.get(who, "center")
        return (f'<div class="bub-row {side}"><div class="bub {cls}" data-b="0">'
                f'{esc(txt or line)}</div></div>')
    if kind == "H":
        num, word = arg.split("|")[:2]
        label = num.lstrip("0") or num
        return (f'<div class="stage"><div class="scrim"></div>'
                f'<div class="pearl">{esc(label)}</div>'
                f'<div class="chap-word">{esc(word)}</div></div>')
    if kind == "G":
        if callable(arg):
            return arg()
        fn = GRAPHICS.get(arg)
        return fn() if fn else ""
    return ""


def load_timeline():
    raw = open(os.path.join(PROJECT, "timings.txt"), encoding="utf-8").read()
    total = float(raw.split("TOTAL ")[1].split()[0])
    times = [tuple(float(x) for x in p.split(","))
             for p in raw.split("TIMES ")[1].split()]
    chunks = json.load(open(os.path.join(PROJECT, "chunks.json"), encoding="utf-8"))
    lines = [l for c in chunks for l in c["lines"]]
    assert len(lines) == len(times), (len(lines), len(times))
    return total, times, lines


def norm(s):
    import re
    return re.sub(r"[^0-9A-Za-z가-힣ㅋㅎ]", "", s)


# ── main ────────────────────────────────────────────────────────────────────
def main():
    arg = lambda k, d=None: sys.argv[sys.argv.index(k) + 1] if k in sys.argv else d
    audio = arg("--audio")
    out = arg("--out", OUT)
    total, times, lines = load_timeline()
    t_from = float(arg("--from", 0))
    t_to = min(total, float(arg("--to", total)))

    groups = P.GROUPS
    starts = [g[0] for g in groups]
    assert starts == sorted(starts) and starts[0] == 0, "groups must start at 0, ascending"
    bg_html, fg_html, cap_html, sc, cap_t, sfx = [], [], [], [], [], []
    for gi, (l0, kind, garg) in enumerate(groups):
        l1 = (starts[gi + 1] - 1) if gi + 1 < len(groups) else len(lines) - 1
        t0, t1 = times[l0][0], times[l1][1]
        d = t1 - t0
        beats = [round(times[k][0] - t0, 2) for k in range(l0, l1 + 1)]
        glines = lines[l0:l1 + 1]
        fam, inner = background(gi, kind, garg)
        background.prev.append(fam)
        bg_html.append(
            f'<div class="clip" id="bgc{gi:03d}" data-start="{t0:.2f}" '
            f'data-duration="{d:.2f}" data-track-index="0">'
            f'<div class="layer"><div class="bgmove {fam}" id="bgm{gi:03d}" data-layout-allow-overflow>{inner}</div>'
            f'<div class="grain"></div><div class="vig"></div></div></div>')
        body = content(gi, kind, garg, glines)
        import re as _re
        onscreen_all = norm(html.unescape(_re.sub(r"<[^>]+>", " ", body)))
        if body:
            fg_html.append(
                f'<div class="clip" id="fg{gi:03d}" data-start="{t0:.2f}" '
                f'data-duration="{d:.2f}" data-track-index="1"><div class="fgm">{body}</div></div>')
        sc.append({"i": gi, "t": round(t0, 2), "d": round(d, 2), "k": kind,
                   "has": bool(body), "b": beats,
                   "zoom": kind == "B" and not garg.get("title") and not garg.get("tags"),
                   "fx": ("coaster" if isinstance(garg, str) and "coaster" in garg else "")})
        # sound design cues, kept sparse: a soft whoosh on chapter / key type,
        # a tiny click per chat bubble
        if kind in ("H",) or (kind == "T" and gi > 0):
            sfx.append((round(t0, 2), "whoosh"))
        if kind == "M":
            for m in garg["msgs"]:
                if m[1] in ("me", "her"):
                    sfx.append((round(t0 + beats[m[0]] + 0.08, 2), "click"))

        # captions: one line each; dropped where the frame already carries the
        # same words (typography, chapter cards, chat bubbles, thought chips)
        if kind in ("T", "P"):
            continue
        onscreen = {onscreen_all}
        k = 0
        while k < len(glines):
            li = l0 + k
            txt = lines[li]
            if len(norm(txt)) >= 2 and norm(txt) in onscreen_all:
                k += 1
                continue
            cs, ce = times[li]
            # a blink-length line rides with the next one if both fit one line
            if (ce - cs) < 0.6 and k + 1 < len(glines):
                nxt = lines[li + 1]
                joined = txt + " " + nxt
                if norm(nxt) not in onscreen and text_w(joined, font(44)) <= CAP_MAX:
                    txt, ce = joined, times[li + 1][1]
                    k += 1
            cards = caption_cards(txt)
            per = (ce - cs) / len(cards)
            for j, c in enumerate(cards):
                a = cs + j * per
                cap_html.append(
                    f'<div class="clip" id="cap{len(cap_t):03d}" data-start="{a:.2f}" '
                    f'data-duration="{per:.2f}" data-track-index="2">'
                    f'<div class="cap-wrap"><div class="cap-scrim" data-layout-allow-overflow></div>'
                    f'<div class="cap">{esc(c)}</div></div></div>')
                cap_t.append(round(a, 2))
            k += 1

    # optional window for segmented renders: clips are re-timed, and the
    # master timeline is scrubbed through the matching slice of the full one
    def window(htmls):
        import re
        outl = []
        for h in htmls:
            m = re.search(r'data-start="([\d.]+)" data-duration="([\d.]+)"', h)
            s0, dd = float(m.group(1)), float(m.group(2))
            s1 = s0 + dd
            if s1 <= t_from or s0 >= t_to:
                continue
            ns, ne = max(s0, t_from) - t_from, min(s1, t_to) - t_from
            outl.append(h.replace(m.group(0), f'data-start="{ns:.3f}" data-duration="{ne-ns:.3f}"', 1))
        return outl
    seg = (t_from, t_to) != (0, total)
    if seg:
        bg_html, fg_html, cap_html = window(bg_html), window(fg_html), window(cap_html)
    dur = t_to - t_from

    css = open(os.path.join(HERE, "style.css"), encoding="utf-8").read()
    audio_tag = (f'\n  <audio id="vo" src="{audio}" data-start="0" data-track-index="4"></audio>'
                 if audio and not seg else "")
    js = open(os.path.join(HERE, "motion.js"), encoding="utf-8").read()
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
     data-start="0" data-duration="{dur:.3f}">
{chr(10).join(bg_html)}
{chr(10).join(fg_html)}
{chr(10).join(cap_html)}
  <div class="clip" id="wmclip" data-start="0" data-duration="{dur:.3f}" data-track-index="3">
    <div class="wm">이다사</div>
  </div>{audio_tag}
</div>
<script>
var SC = {json.dumps(sc, separators=(",", ":"))};
var CAPT = {json.dumps(cap_t, separators=(",", ":"))};
var WIN = [{t_from:.3f}, {t_to:.3f}];
{js}
</script>
</body>
</html>
"""
    open(out, "w", encoding="utf-8").write(doc)
    json.dump(sfx, open(os.path.join(PROJECT, "sfx.json"), "w"))
    if LOCAL:
        json.dump(MANIFEST, open(os.path.join(HERE, "..", "assets_manifest.json"), "w"), indent=0)
    print(f"wrote {out}")
    print(f"  window {t_from:.1f}-{t_to:.1f}s · groups {len(groups)} · caption cards {len(cap_t)}")
    from collections import Counter
    print("  kinds:", dict(Counter(g[1] for g in groups)))


if __name__ == "__main__":
    main()
