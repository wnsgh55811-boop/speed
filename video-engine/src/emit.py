# -*- coding: utf-8 -*-
"""Write ../index.html — the full 602s composition.

    python3 src/emit.py [--audio assets/audio/master.wav]

Tracks: 0 backgrounds · 1 content · 2 captions · 3 watermark.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
# A project lives in its own folder (plan.py + timeline.json); default is src/.
PROJ = sys.argv[sys.argv.index("--project") + 1] if "--project" in sys.argv else HERE
sys.path.insert(0, PROJ)
from build import (W, H, CDN, IMG, ALIAS, NEON_FIG, FAMILIES,   # noqa: E402
                   esc, caption_cards, motes)
import build                                                    # noqa: E402
build.CAP_PX, build.CAP_MAX = 50, 1180       # one short line, readable on a phone
import kit2                                                     # noqa: E402

from plan import PLAN                                            # noqa: E402

OUT = os.path.join(HERE, "..", "index.html")
ROOT = os.path.join(HERE, "..")

# Prefer local copies so a render never depends on the CDN mid-capture.
for _k in list(IMG):
    for _x in (".png", ".jpg"):
        if os.path.exists(os.path.join(ROOT, "assets", "img", "lib", _k + _x)):
            IMG[_k] = f"assets/img/lib/{_k}{_x}"
for _f in sorted(os.listdir(os.path.join(ROOT, "assets", "img"))):
    if _f.endswith((".png", ".jpg")):
        _k = _f[:-4]
        IMG[_k] = f"assets/img/{_f}"
        ALIAS.setdefault(_k, [_k])


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
            + "".join(f'<path class="edge" d="M{x} {y:.0f} L{x} 300"/>'
                      for x, y in ((470, 216), (660, 178), (850, 216)))
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
    "mirror":   '<rect x="30" y="44" width="58" height="104" rx="10"/>'
                '<rect x="104" y="44" width="58" height="104" rx="10" stroke="#D8B368"/>'
                '<path d="M96 30v132" stroke-dasharray="10 12"/>',
}


def picto(name, size=200):
    """One line-drawn mark in the shared stroke language."""
    return (f'<svg class="picto glow" width="{size}" height="{size}" viewBox="0 0 192 192" '
            'fill="none" stroke="currentColor" stroke-width="5.5" '
            f'stroke-linecap="round" stroke-linejoin="round">{_PICTO[name]}</svg>')


# ── DOM graphic primitives ──────────────────────────────────────────────────
def g_rows(title, items, muted=(), mark=None):
    h = ['<div class="stage"><div class="scrim wide"></div>']
    if title:
        h.append(f'<div class="hl md gtitle bt" data-l="0">{esc(title)}</div>')
    h.append('<div class="rows" style="margin-top:46px">')
    for i, it in enumerate(items):
        cls = "row muted" if i in muted else "row"
        extra = ''
        if mark == "q" and i not in muted:
            extra = '<span class="qmark">?</span>'
        key = f'data-l="0" data-o="{.25 + i * .45:.2f}" data-k="{esc(it)}"'
        h.append(f'<div class="{cls} bt" {key}><i class="tick"></i><span>{esc(it)}</span>{extra}</div>')
    h.append("</div></div>")
    return "".join(h)


def g_chips(title, items, hot=()):
    h = ['<div class="stage"><div class="scrim wide"></div>']
    if title:
        h.append(f'<div class="hl md gtitle bt" data-l="0">{esc(title)}</div>')
    h.append('<div class="chips" style="margin-top:50px">')
    for i, it in enumerate(items):
        key = f'data-l="0" data-o="{.2 + i * .45:.2f}" data-k="{esc(it)}"'
        h.append(f'<span class="chip{" hot" if it in hot else ""} bt" {key}>{esc(it)}</span>')
    h.append("</div></div>")
    return "".join(h)


def g_bars(title, data, axis=("얕음", "깊음")):
    """A bar plus the degree it stands for.

    Review note: "그냥 바만 있어" — length alone read as decoration. Each row now
    carries a five-step rating and the block carries an axis, so the bar says how
    much, not just that there is some.
    """
    h = ['<div class="stage"><div class="scrim wide"></div>',
         f'<div class="hl md gtitle bt" data-l="0">{esc(title)}</div>' if title else '',
         '<div class="bars" style="margin-top:50px">']
    for bi, (lab, frac, tone) in enumerate(data):
        key = f'data-l="0" data-o="{.3 + bi * .6:.2f}" data-k="{esc(lab)}"'
        steps = max(1, min(5, int(round(frac * 5))))
        hot = "hot" if tone in ("hot", "cool-hot") else ""
        dots = "".join(f'<i class="{("on " + hot).strip() if k < steps else ""}"></i>'
                       for k in range(5))
        ticks = "".join(f'<span class="tickline" style="left:{q}%"></span>'
                        for q in (20, 40, 60, 80))
        h.append(f'<div class="bt" {key}><div class="bar-head"><span class="bar-lab">{esc(lab)}</span>'
                 f'<span class="bar-dots">{dots}</span></div>'
                 f'<div class="bar-track">{ticks}'
                 f'<i class="bar-fill {tone} bt-grow" {key} style="width:{int(frac*100)}%"></i></div></div>')
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


# ── motion graphics (no zoom: wipes, sweeps, orbits, drifting light) ──────
def photo_mg(i):
    """One of four overlays per photo plate, rotating so neighbours differ."""
    v = i % 4
    if v == 0:
        return '<div class="mg mg-v0"><div class="mg-sweep"></div></div>'
    if v == 1:
        return ('<div class="mg mg-v1"><svg class="mg-frame" width="1920" height="1080" viewBox="0 0 1920 1080">'
                '<path d="M120 200 L120 120 L200 120"/><path d="M1720 120 L1800 120 L1800 200"/>'
                '<path d="M120 880 L120 960 L200 960"/><path d="M1720 960 L1800 960 L1800 880"/></svg></div>')
    if v == 2:
        s, out = i * 7919 + 11, []
        for _ in range(16):
            s = (s * 1103515245 + 12345) & 0x7FFFFFFF
            x = 5 + (s >> 7) % 90
            s = (s * 1103515245 + 12345) & 0x7FFFFFFF
            y = 30 + (s >> 7) % 60
            s = (s * 1103515245 + 12345) & 0x7FFFFFFF
            r = 3 + (s >> 9) % 6
            out.append(f'<i class="mg-mote" style="left:{x}%;top:{y}%;width:{r}px;height:{r}px"></i>')
        return '<div class="mg mg-v2">' + "".join(out) + '</div>'
    return '<div class="mg mg-v3"><div class="mg-leak"></div></div>'


def icon_stage(url, i):
    """3D icon on an orbit: rotating rings, travelling lights, breathing glow."""
    return ('<div class="icon-stage"><div class="icon-glow"></div>'
            '<svg class="orb" viewBox="-360 -360 720 720">'
            '<g class="orb-a"><ellipse rx="330" ry="110"/><circle cx="330" cy="0" r="7"/></g>'
            '<g class="orb-b"><ellipse class="b" rx="290" ry="150" transform="rotate(-24)"/>'
            '<circle class="am" cx="-290" cy="0" r="6" transform="rotate(-24)"/></g></svg>'
            '<div class="icon-shadow"></div>'
            f'<img class="icon3d" src="{url}" alt=""></div>')


# ── scene builders ──────────────────────────────────────────────────────────
def src(key):
    """Asset URL. Keyed figures carry a whole URL; the originals are CDN names."""
    v = IMG[key]
    return v if v.startswith(("http", "assets/")) else CDN + v


_ROT = {}
_USED = []
_KEYS = []


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
    _USED.append(opts[n % len(opts)])
    return opts[n % len(opts)]


def background(i, kind, arg, section):
    """Return (css_class, inner_html). Photos own their own plate."""
    if kind == "B":
        key = pick(arg.partition("|")[0], i)
        return "bg-photo", (f'<img id="ph{i:03d}" src="{src(key)}" alt="">'
                            f'<div class="tint"></div>')
    if kind == "H":
        return "bg-ember", ""
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
        _, _, tag = arg.partition("|")
        if not tag:
            return photo_mg(i)
        warm = tag.startswith("!")
        return (f'<div class="ph-tag{" am" if warm else ""} bt-pop" data-l="0" data-o="0.35">'
                f'{esc(tag.lstrip("!"))}</div>')
    if kind == "S":
        a, b = arg.split("|")
        return kit2.split_hook(src(a), src(b))
    if kind == "F":
        mode, _, hot = arg.partition(":")
        return kit2.funnel(mode, int(hot) if hot else -1)
    if kind == "V":
        return kit2.dots_compare()
    if kind == "L":
        return kit2.anx_line()
    if kind == "X":
        return kit2.chat(arg["msgs"], phone=not arg.get("bg"), title=arg.get("title", "소개팅 상대"),
                         photo=src(pick(arg["bg"], i)) if arg.get("bg") else None)
    if kind == "R":
        cur, _, mode = str(arg).partition(":")
        title = {"intro": "오늘의 7단계", "walk": "정리 · 7단계"}.get(mode, "지금까지")
        return kit2.tracker(int(cur), mode == "intro", title, walk=mode == "walk")
    if kind == "Z":
        return g_bars(*arg)
    if kind == "W":
        title, items, muted, mark = arg
        return g_rows(title, items, muted=muted, mark=mark)
    if kind == "U":
        return g_chips(*arg)
    if kind == "A":
        return kit2.cta()
    if kind == "J":
        return kit2.journey()
    if kind == "D":
        return kit2.link(arg)
    if kind == "Y":
        return kit2.contrast(*arg)
    if kind == "Q":
        return kit2.checklist(*arg)
    if kind == "C":
        who, _, _bg = arg.partition("@")
        names = who.split("+")
        ring = ('<svg class="cut-ring" viewBox="-450 -450 900 900"><circle class="r3" r="430"/>'
                '<circle class="r1" r="360"/><circle class="r2" r="300"/></svg>')
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
                     f'style="height:{int(700*sc)}px"></div>')
        return ring + "".join(h)
    if kind == "I":
        key, _, badge = arg.partition("|")
        h = [f'<div class="stage">{icon_stage(src(pick(key, i)), i)}']
        if badge:
            h.append(f'<div class="hl md bt" data-l="0" data-o=".3" data-k="{esc(badge)}" '
                     f'style="margin-top:26px">{esc(badge)}</div>')
        h.append("</div>")
        return "".join(h)
    if kind == "N":
        return (f'<div class="diag"><div class="scrim wide"></div>'
                f'{FIGS[NEON_FIG[arg]]() if NEON_FIG[arg] != "qmarks" else fig_qmarks(i)}</div>')
    if kind == "P":
        mark, _, txt = arg.partition("|")
        words = txt or line
        size = "xl" if len(words) <= 14 else ("lg" if len(words) <= 26 else "md")
        key = "pi_" + mark
        if key in IMG:
            return f'<div class="stage">{icon_stage(src(pick(key, i)), i)}</div>'
        return f'<div class="stage"><div class="pmark">{picto(mark, 300)}</div></div>'
    if kind == "T":
        txt = arg if arg else line
        parts = [p for p in txt.split("|") if p.strip()]
        size = "xl" if (len(parts) == 1 and len(parts[0]) <= 14) else "lg"
        h = ['<div class="stage"><div class="scrim wide"></div>']
        for k, p in enumerate(parts):
            h.append(f'<div class="hl {size} {"bt" if k == 0 else "bt-show"}" data-l="0" data-o="{k * .5:.2f}" '
                     f'data-k="{esc(p)}">{esc(p)}</div>')
        h.append('<div class="t-acc"></div></div>')
        return "".join(h)
    if kind == "K":
        arg, _, label = arg.partition("|")
        crossed = arg.endswith("x")
        who = arg[0]
        side = "right" if who == "m" else ("center" if label else "left")
        tag = label or ("남자" if who == "m" else ("여자" if who == "w" else "내담자"))
        strike = ('<svg class="strike" viewBox="0 0 100 100">'
                  '<line x1="10" y1="10" x2="90" y2="90"/><line x1="10" y1="90" x2="90" y2="10"/>'
                  '</svg>') if crossed else ""
        return (f'<div class="bub-row {side}"><div class="bub {who}">'
                f'<span class="who" data-layout-allow-overflow>{esc(tag)}</span>{esc(line)}{strike}</div></div>')
    if kind == "H":
        num, _, word = arg.partition("|")
        label = num[1:] if num.startswith("n") else (num.lstrip("0") or num)
        steps = ""
        if label.isdigit():
            n = int(label)
            steps = '<div class="chap-steps">' + "".join(
                f'<i class="{"on" if k + 1 == n else ("done" if k + 1 < n else "")}"></i>'
                for k in range(7)) + '</div>'
        return (f'<div class="stage"><div class="scrim"></div>'
                f'<div class="pearl-wrap"><svg class="chap-ring" viewBox="-100 -100 200 200">'
                f'<circle r="92"/></svg><div class="pearl">{esc(label)}</div></div>'
                f'<div class="chap-word">{esc(word)}</div><div class="chap-line"></div>{steps}</div>')
    if kind == "G":
        fn = GRAPHICS.get(arg)
        body = fn() if fn else ""
        if arg in ("g_loop", "g_loop_full"):
            return f'<div class="diag"><div class="scrim wide"></div>{body}</div>'
        return body
    return ""


# ── main ────────────────────────────────────────────────────────────────────
NOCAP = ("T", "H", "K")          # sentence already set large mid-frame


def _norm(t):
    import re
    return re.sub(r"[^0-9A-Za-z가-힣]", "", t)


def load_lines():
    """WAV-aligned sentence timings: [{text, s, e, ct[]}] + total seconds."""
    tl = json.load(open(os.path.join(PROJ, "timeline.json"), encoding="utf-8"))
    return tl["lines"], tl["total"]


_SPLITS = None


def cards_for(line):
    """Caption cards for one sentence, each timed off the WAV char clock.
    A project's captions.txt (one sentence per line, ' / ' between meaning
    units) wins over the width-based splitter."""
    global _SPLITS
    if _SPLITS is None:
        cp = os.path.join(PROJ, "captions.txt")
        _SPLITS = [l.rstrip("\n") for l in open(cp, encoding="utf-8")] if os.path.exists(cp) else []
    text = line["text"].strip()
    if text.endswith("."):
        text = text[:-1]
    idx = line.get("i")
    sp = _SPLITS[idx] if _SPLITS and idx is not None and idx < len(_SPLITS) else None
    if sp and _norm(sp.replace(" / ", "")) == _norm(text):
        cards = [c.strip() for c in sp.split(" / ")]
    else:
        cards = caption_cards(text)
    out, off = [], 0
    for c in cards:
        n = len(_norm(c))
        t = line["ct"][min(off, len(line["ct"]) - 1)] if line["ct"] else line["s"]
        out.append([c, t])
        off += n
    out[0][1] = line["s"]
    return out


def resolve_keys(body, S, lines):
    """data-k="words" -> data-t="<sec>": when those words are spoken in the WAV
    (char clock from timeline.json). Unmatched keys keep their beat timing."""
    import re
    import html as _h
    seg, clock = "", []
    for L in S["lines"]:
        n = _norm(lines[L]["text"])
        ct = lines[L]["ct"][:len(n)]
        seg += n
        clock += ct + [lines[L]["e"]] * (len(n) - len(ct))
    lo = 0
    while lo < len(clock) and clock[lo] < S["start"] - 0.05:
        lo += 1
    state = {"cur": lo}

    def find(raw):
        txt = _h.unescape(raw)
        words = [_norm(w) for w in re.split(r"\s+", txt) if len(_norm(w)) >= 2]
        tries = [_norm(txt)] + sorted(words, key=len, reverse=True)
        tries += [w[:k] for w in words for k in range(len(w) - 1, 1, -1)]
        for start in (state["cur"], lo):
            for t in tries:
                if len(t) < 2 and t != _norm(txt):
                    continue
                i = seg.find(t, start)
                if i >= 0:
                    state["cur"] = i + 1
                    return clock[i]
        return None

    def sub(m):
        t = find(m.group(1))
        _KEYS.append((m.group(1), t))
        return "" if t is None else f'data-t="{max(t - 0.22, S["start"]):.2f}"'
    return re.sub(r'data-k="([^"]*)"', sub, body)


def build_scenes(lines, total):
    """Expand the plan into scenes. Plan entries per sentence:
         (kind, arg)        one scene
         "="                extend the previous scene over this sentence
         [spec, spec]       split this sentence into two scenes at a card edge
    """
    assert len(PLAN) == len(lines), (len(PLAN), len(lines))
    starts = [l["s"] for l in lines] + [total]
    starts[0] = 0.0
    sc = []
    for li, (ent, ln) in enumerate(zip(PLAN, lines)):
        cards = cards_for(ln)
        if ent == "=":
            sc[-1]["lines"].append(li)
            sc[-1]["cards"].extend(cards)
            sc[-1]["lb"].append(ln["s"])
            sc[-1]["end"] = starts[li + 1]
            continue
        specs = ent if isinstance(ent, list) else [ent]
        if len(specs) == 2 and len(cards) >= 2:
            cut = (len(cards) + 1) // 2
            parts = [(specs[0], cards[:cut], starts[li]), (specs[1], cards[cut:], cards[cut][1])]
        else:
            parts = [(specs[0], cards, starts[li])]
        for k, (spec, cs, t0) in enumerate(parts):
            if sc:
                sc[-1]["end"] = t0
            sc.append({"kind": spec[0], "arg": spec[1], "start": t0, "end": starts[li + 1],
                       "lines": [li], "cards": cs, "lb": [t0], "text": ln["text"]})
    return sc


def main():
    audio = None
    if "--audio" in sys.argv:
        audio = sys.argv[sys.argv.index("--audio") + 1]
    lines, total = load_lines()
    scenes = build_scenes(lines, total)

    bg_html, fg_html, cap_html, anim, cap_t = [], [], [], [], []
    cap_n = 0
    for i, S in enumerate(scenes):
        kind, arg, t0 = S["kind"], S["arg"], S["start"]
        d = max(0.4, S["end"] - t0)
        fam, inner = background(i, kind, arg, i // 9)
        background.prev.append(fam)
        bg_html.append(
            f'<div class="clip" id="bgc{i:03d}" data-start="{t0:.2f}" '
            f'data-duration="{d:.2f}" data-track-index="0">'
            f'<div class="layer"><div class="bgmove {fam}" id="bgm{i:03d}" data-layout-allow-overflow>{inner}</div>'
            f'<div class="grain"></div><div class="vig"></div></div></div>')

        if kind == "X":                 # bubbles quote the sentence they play on
            def _q(t):
                t = t.strip().rstrip(".")
                return t.strip('"').strip("'").strip("\u201c\u201d")
            arg = dict(arg, msgs=[(m[0], m[1] if m[1] else _q(lines[S["lines"][m[2]]]["text"]))
                                  + tuple(m[2:]) for m in arg["msgs"]])
        body = content(i, kind, arg, S["text"].rstrip("."))
        body = resolve_keys(body, S, lines)
        if kind == "T":                 # the headline opens with its sentence
            import re as _re
            body = _re.sub(r'data-t="([0-9.]+)"', lambda m: f'data-t="{min(float(m.group(1)), t0 + 0.25):.2f}"',
                           body, count=1)
        if body:
            fg_html.append(
                f'<div class="clip" id="fg{i:03d}" data-start="{t0:.2f}" '
                f'data-duration="{d:.2f}" data-track-index="1"><div class="fgm">{body}</div></div>')
        anim.append({"i": i, "t": round(t0, 2), "d": round(d, 2), "k": kind,
                     "has": bool(body), "lb": [round(x, 2) for x in S["lb"]],
                     "cb": [round(c[1], 2) for c in S["cards"]]})

        # captions — skipped where the same words are already on screen
        if kind in NOCAP:
            continue
        hide = set()
        if kind == "X":
            hide = {S["lines"][m[2]] for m in S["arg"]["msgs"] if not m[1]}
        cs = S["cards"]
        for j, (c, ct) in enumerate(cs):
            li = max([L for L in S["lines"] if lines[L]["s"] <= ct + 0.01] or [S["lines"][0]])
            if li in hide:
                continue
            ct = max(ct - 0.10, S["start"], cap_t[-1] + 0.05 if cap_t else 0)
            nxt = cs[j + 1][1] - 0.10 if j + 1 < len(cs) else S["end"]
            end = min(nxt, lines[li]["e"] + 0.7, S["end"])
            if end - ct < 0.25:
                end = min(ct + 0.25, S["end"])
            cap_html.append(
                f'<div class="clip" id="cap{cap_n:03d}" data-start="{ct:.2f}" '
                f'data-duration="{end-ct:.2f}" data-track-index="2">'
                f'<div class="cap-wrap"><div class="cap-scrim" data-layout-allow-overflow></div>'
                f'<div class="cap">{esc(c)}</div></div></div>')
            cap_t.append(round(ct, 2))
            cap_n += 1

    css = open(os.path.join(HERE, "style.css"), encoding="utf-8").read()
    audio_tag = (f'\n  <audio id="vo" src="{audio}" data-start="0" data-duration="{total:.3f}" '
                 f'data-track-index="4" data-volume="1"></audio>' if audio else "")

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
    <div class="wm">이다사</div>
  </div>{audio_tag}
</div>
<script>
var tl = gsap.timeline({{ paused: true }});
function T(sel, from, to, at) {{
  if (!document.querySelector(sel)) return;
  tl.fromTo(sel, from, to, at);
}}
var SC = {json.dumps(anim, separators=(",", ":"))};
var CAPT = {json.dumps(cap_t, separators=(",", ":"))};

// plates drift for the whole scene so no frame is ever dead still
SC.forEach(function (s) {{
  var id = "#bgm" + String(s.i).padStart(3, "0");
  var dir = (s.i % 2) ? 1 : -1;
  tl.fromTo(id, {{ xPercent: 0 }},
            {{ xPercent: dir * 0.8, duration: s.d, ease: "sine.inOut" }}, s.t);
}});


// beat-driven elements: arrive on the narration line they belong to
SC.forEach(function (s) {{
  if (!s.has) return;
  var root = document.getElementById("fg" + String(s.i).padStart(3, "0"));
  root.querySelectorAll("[data-l], [data-c], [data-t]").forEach(function (el) {{
    var base = s.t;
    if (el.hasAttribute("data-c")) {{
      base = s.cb[Math.min(parseInt(el.getAttribute("data-c"), 10), s.cb.length - 1)];
    }} else if (el.hasAttribute("data-l")) {{
      base = s.lb[Math.min(parseInt(el.getAttribute("data-l"), 10), s.lb.length - 1)];
    }}
    var at = base + parseFloat(el.getAttribute("data-o") || "0") + 0.06;
    if (el.hasAttribute("data-t")) at = parseFloat(el.getAttribute("data-t")) + parseFloat(el.getAttribute("data-o2") || "0");
    else if (el.hasAttribute("data-o2") && el.closest("[data-t]"))
      at = parseFloat(el.closest("[data-t]").getAttribute("data-t")) + parseFloat(el.getAttribute("data-o2"));
    if (el.hasAttribute("data-x")) {{
      var xi = parseInt(el.getAttribute("data-x"), 10);
      if (xi < s.lb.length) tl.to(el, {{ opacity: 0, duration: 0.3, ease: "power1.in" }}, s.lb[xi] - 0.05);
    }}
    var c = el.classList;
    if (c.contains("bt-grow")) {{
      tl.fromTo(el, {{ scaleX: 0 }}, {{ scaleX: 1, duration: 0.95, ease: "expo.out" }}, at + 0.12);
    }} else if (c.contains("bt-draw")) {{
      var len = el.getTotalLength ? el.getTotalLength() : 600;
      tl.fromTo(el, {{ strokeDasharray: len, strokeDashoffset: len }},
                {{ strokeDashoffset: 0, duration: 0.9, ease: "power2.inOut" }}, at);
    }} else if (c.contains("bt-show")) {{
      tl.fromTo(el, {{ display: "none", opacity: 0, y: 26 }},
                {{ display: "flex", opacity: 1, y: 0, duration: 0.28, ease: "power2.out" }}, at);
    }} else if (c.contains("bt-pop")) {{
      tl.fromTo(el, {{ opacity: 0, y: 16 }},
                {{ opacity: 1, y: 0, duration: 0.32, ease: "power2.out" }}, at);
    }} else {{
      tl.fromTo(el, {{ opacity: 0, y: 22 }},
                {{ opacity: 1, y: 0, duration: 0.32, ease: "power3.out" }}, at);
    }}
  }});
}});

// content entrances for the classic kinds, one recipe per kind
SC.forEach(function (s) {{
  if (!s.has) return;
  var f = "#fg" + String(s.i).padStart(3, "0"), t = s.t + 0.08;
  var dur = Math.min(0.62, Math.max(0.34, s.d * 0.34));
  if (s.k === "T") {{
  }} else if (s.k === "K") {{
    T(f + " .bub", {{ opacity: 0, yPercent: 10 }},
              {{ opacity: 1, yPercent: 0, duration: dur, ease: "power2.out" }}, t);
    T(f + " .who", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.3, ease: "power1.out" }}, t + 0.14);
  }} else if (s.k === "H") {{
    T(f + " .chap-kick", {{ opacity: 0, letterSpacing: "0.6em" }},
              {{ opacity: 1, letterSpacing: "0.3em", duration: 0.7, ease: "power2.out" }}, t);
    T(f + " .pearl", {{ opacity: 0, y: 20 }},
              {{ opacity: 1, y: 0, duration: 0.5, ease: "power2.out" }}, t + 0.05);
    T(f + " .chap-word", {{ yPercent: 50, opacity: 0 }},
              {{ yPercent: 0, opacity: 1, duration: 0.55, ease: "power3.out" }}, t + 0.18);
    T(f + " .chap-steps i", {{ scaleX: 0 }},
              {{ scaleX: 1, duration: 0.4, ease: "power2.out", stagger: 0.05 }}, t + 0.3);
  }} else if (s.k === "C") {{
    T(f + " .cut", {{ yPercent: 8, opacity: 0 }},
              {{ yPercent: 0, opacity: 1, duration: dur, ease: "power2.out", stagger: 0.12 }}, t);
  }} else if (s.k === "I" && !document.querySelector(f + " .icon-stage")) {{
    T(f + " .icon3d", {{ opacity: 0, y: 24 }},
              {{ opacity: 1, y: 0, duration: dur, ease: "power2.out" }}, t);
    var fl = Math.max(0, Math.floor((s.d - dur - 0.2) / 1.6) - 1);
    if (fl > 0 && document.querySelector(f + " .icon3d")) tl.to(f + " .icon3d", {{ yPercent: -2.6, rotation: 2.2,
                duration: 0.8, ease: "sine.inOut", yoyo: true, repeat: fl }}, t + dur + 0.1);
  }} else if (s.k === "N") {{
    T(f + " svg", {{ opacity: 0 }},
              {{ opacity: 1, duration: dur, ease: "power2.out" }}, t);
    T(f + " .fg-draw, " + f + " .fg-draw2", {{ strokeDasharray: 2400, strokeDashoffset: 2400 }},
              {{ strokeDashoffset: 0, duration: Math.min(1.6, s.d * 0.6), ease: "power2.inOut" }}, t + 0.1);
  }} else if (s.k === "P") {{
    T(f + " .pmark", {{ opacity: 0, y: 20 }},
              {{ opacity: 1, y: 0, duration: 0.5, ease: "power2.out" }}, t);
    var pf = Math.max(0, Math.floor((s.d - 0.8) / 1.8) - 1);
    if (pf > 0 && document.querySelector(f + " .pmark")) tl.to(f + " .pmark", {{ y: -10, duration: 0.9,
                ease: "sine.inOut", yoyo: true, repeat: pf }}, t + 0.6);
  }} else if (s.k === "G") {{
    T(f + " .gtitle:not(.bt)", {{ yPercent: 40, opacity: 0 }},
              {{ yPercent: 0, opacity: 1, duration: 0.45, ease: "power3.out" }}, t);
    T(f + " .row:not(.bt), " + f + " .chip:not(.bt), " + f + " .bars > div:not(.bt), " + f + " .stk",
              {{ yPercent: 36, opacity: 0 }},
              {{ yPercent: 0, opacity: 1, duration: 0.46, ease: "power3.out", stagger: 0.14 }}, t + 0.14);
    T(f + " .bar-fill:not(.bt-grow)", {{ scaleX: 0 }},
              {{ scaleX: 1, duration: 0.9, ease: "expo.out", stagger: 0.16 }}, t + 0.3);
    T(f + " .hl, " + f + " .sub, " + f + " .gapline",
              {{ opacity: 0, yPercent: 26 }},
              {{ opacity: 1, yPercent: 0, duration: 0.46, ease: "power2.out", stagger: 0.08 }}, t + 0.1);
  }} else if (s.k === "D") {{
    // semantic: the connection actually holds, breaks, restores or stretches
    var L = f + " .lk-l", R = f + " .lk-r", A = f + " .lk-node.a", B = f + " .lk-node.b";
    T(A + ", " + B, {{ opacity: 0, y: 16 }}, {{ opacity: 1, y: 0, duration: 0.5, ease: "power2.out", stagger: 0.1 }}, t);
    T(L + ", " + R, {{ strokeDasharray: 400, strokeDashoffset: 400 }}, {{ strokeDashoffset: 0, duration: 0.6, ease: "power2.out" }}, t + 0.3);
    var root = document.querySelector(f + " .lnk");
    if (root && root.classList.contains("break")) {{
      tl.to(L, {{ x: -70, rotation: -8, transformOrigin: "0% 50%", stroke: "#F0538F", duration: 0.5, ease: "power2.in" }}, t + 1.2);
      tl.to(R, {{ x: 70, rotation: 8, transformOrigin: "100% 50%", stroke: "#F0538F", duration: 0.5, ease: "power2.in" }}, t + 1.2);
      tl.to(B, {{ x: 60, opacity: 0.45, duration: 0.8, ease: "power2.out" }}, t + 1.3);
    }} else if (root && root.classList.contains("far")) {{
      tl.to(A, {{ x: -120, duration: Math.max(1, s.d - 1), ease: "sine.inOut" }}, t + 0.8);
      tl.to(B, {{ x: 120, duration: Math.max(1, s.d - 1), ease: "sine.inOut" }}, t + 0.8);
      tl.to(L + ", " + R, {{ opacity: 0.25, duration: 1.2 }}, t + 1.2);
    }} else if (root && root.classList.contains("restore")) {{
      tl.fromTo(L, {{ x: -70, rotation: -8, transformOrigin: "0% 50%" }}, {{ x: 0, rotation: 0, duration: 0.7, ease: "back.out(1.3)" }}, t + 1.0);
      tl.fromTo(R, {{ x: 70, rotation: 8, transformOrigin: "100% 50%" }}, {{ x: 0, rotation: 0, duration: 0.7, ease: "back.out(1.3)" }}, t + 1.0);
    }} else {{
      tl.to(L + ", " + R, {{ strokeWidth: 11, duration: 0.6, yoyo: true, repeat: 1, ease: "sine.inOut" }}, t + 1.2);
    }}
  }} else if (s.k === "L") {{
    var n = Math.max(1, Math.round(s.d / 2.5));
    T(f + " .clock-h", {{ rotation: 0, svgOrigin: "0 0" }},
              {{ rotation: 360 * 2, svgOrigin: "0 0", duration: s.d - 0.3, ease: "none" }}, t);
  }}
}});

// motion graphics: every image element keeps moving — never by zooming
SC.forEach(function (s) {{
  var f = "#fg" + String(s.i).padStart(3, "0"), t = s.t;
  var root = document.querySelector(f);
  if (!root) return;
  var D = Math.max(1, s.d);
  if (root.querySelector(".mg-v0")) {{
    var img0 = document.querySelector("#ph" + String(s.i).padStart(3, "0"));
    if (img0 && s.i > 0) tl.fromTo(img0, {{ clipPath: "inset(0 100% 0 0)" }}, {{ clipPath: "inset(0 0% 0 0)", duration: 0.7, ease: "power3.inOut" }}, t);
    tl.fromTo(f + " .mg-sweep", {{ xPercent: -120 }}, {{ xPercent: 330, duration: Math.min(2.4, D), ease: "power1.inOut" }}, t + 0.5);
  }}
  if (root.querySelector(".mg-v1")) {{
    root.querySelectorAll(".mg-frame path").forEach(function (p, k) {{
      tl.fromTo(p, {{ strokeDasharray: 170, strokeDashoffset: 170 }}, {{ strokeDashoffset: 0, duration: 0.6, ease: "power2.out" }}, t + 0.15 + k * 0.08);
    }});
    tl.fromTo(f + " .mg-frame", {{ x: 0 }}, {{ x: 18, duration: D, ease: "sine.inOut" }}, t);
  }}
  if (root.querySelector(".mg-v2")) {{
    root.querySelectorAll(".mg-mote").forEach(function (m, k) {{
      tl.fromTo(m, {{ y: 40, opacity: 0 }}, {{ y: -120 - (k % 5) * 30, opacity: 0.9, duration: D * 0.5, ease: "sine.out", yoyo: true, repeat: 1 }}, t + (k % 6) * 0.15);
    }});
  }}
  if (root.querySelector(".mg-v3")) {{
    tl.fromTo(f + " .mg-leak", {{ xPercent: -80, opacity: 0 }}, {{ xPercent: 90, opacity: 1, duration: D, ease: "sine.inOut" }}, t);
    var img3 = document.querySelector("#ph" + String(s.i).padStart(3, "0"));
    if (img3) tl.fromTo(img3, {{ clipPath: "inset(0 0 100% 0)" }}, {{ clipPath: "inset(0 0 0% 0)", duration: 0.65, ease: "power3.inOut" }}, t);
  }}
  if (root.querySelector(".icon-stage")) {{
    tl.fromTo(f + " .orb-a", {{ rotation: 0, svgOrigin: "0 0" }}, {{ rotation: 360, svgOrigin: "0 0", duration: Math.max(D, 6), ease: "none" }}, t);
    tl.fromTo(f + " .orb-b", {{ rotation: 0, svgOrigin: "0 0" }}, {{ rotation: -300, svgOrigin: "0 0", duration: Math.max(D, 6), ease: "none" }}, t);
    tl.fromTo(f + " .orb", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.6 }}, t + 0.1);
    tl.fromTo(f + " .icon-glow", {{ opacity: 0.4 }}, {{ opacity: 1, duration: 1.2, ease: "sine.inOut", yoyo: true, repeat: Math.max(1, Math.floor(D / 1.2)) }}, t);
    tl.fromTo(f + " .icon-stage .icon3d", {{ opacity: 0, y: 40, rotation: -4 }}, {{ opacity: 1, y: 0, rotation: 0, duration: 0.55, ease: "power3.out" }}, t);
    var nf = Math.max(1, Math.floor((D - 0.6) / 1.4));
    tl.to(f + " .icon-stage .icon3d", {{ y: -16, rotation: 2, duration: 1.4, ease: "sine.inOut", yoyo: true, repeat: nf }}, t + 0.6);
    tl.to(f + " .icon-shadow", {{ x: 12, opacity: 0.55, duration: 1.4, ease: "sine.inOut", yoyo: true, repeat: nf }}, t + 0.6);
  }}
  if (root.querySelector(".cut-ring")) {{
    tl.fromTo(f + " .cut-ring .r1", {{ rotation: 0, svgOrigin: "0 0" }}, {{ rotation: 120, svgOrigin: "0 0", duration: D, ease: "none" }}, t);
    tl.fromTo(f + " .cut-ring .r2", {{ rotation: 0, svgOrigin: "0 0" }}, {{ rotation: -90, svgOrigin: "0 0", duration: D, ease: "none" }}, t);
    tl.fromTo(f + " .cut-ring", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.5 }}, t);
    tl.fromTo(f + " .cut img", {{ clipPath: "inset(100% 0 0 0)" }}, {{ clipPath: "inset(0% 0 0 0)", duration: 0.6, ease: "power3.out" }}, t);
    tl.fromTo(f + " .cut", {{ x: 0 }}, {{ x: (s.i % 2 ? 16 : -16), duration: D, ease: "sine.inOut" }}, t);
  }}
  if (root.querySelector(".t-acc")) {{
    tl.fromTo(f + " .t-acc", {{ scaleX: 0 }}, {{ scaleX: 1, duration: 0.6, ease: "power3.out" }}, t + 0.3);
  }}
  if (root.querySelector(".chap-ring")) {{
    tl.fromTo(f + " .chap-ring circle", {{ strokeDasharray: 580, strokeDashoffset: 580 }}, {{ strokeDashoffset: 0, duration: 0.9, ease: "power2.inOut" }}, t + 0.1);
    tl.fromTo(f + " .chap-line", {{ scaleX: 0 }}, {{ scaleX: 1, duration: 0.8, ease: "power3.out" }}, t + 0.3);
  }}
  if (root.querySelector(".talk-photo img")) {{
    tl.fromTo(f + " .talk-photo img", {{ xPercent: -2 }}, {{ xPercent: 2, duration: D, ease: "sine.inOut" }}, t);
  }}
}});

// captions: one line, fading up at each card's own start
CAPT.forEach(function (ct, c) {{
  var cid = "#cap" + String(c).padStart(3, "0") + " .cap";
  tl.fromTo(cid, {{ opacity: 0, yPercent: 22 }},
            {{ opacity: 1, yPercent: 0, duration: 0.2, ease: "power2.out" }}, ct);
}});

window.__timelines["main"] = tl;
</script>
</body>
</html>
"""
    open(OUT, "w", encoding="utf-8").write(doc)
    print(f"wrote {OUT}")
    print(f"  duration {total:.2f}s · scenes {len(scenes)} · caption cards {cap_n}")
    from collections import Counter
    print("  kinds:", dict(Counter(S["kind"] for S in scenes)))
    print("  bg families:", dict(Counter(background.prev[2:])))
    use = Counter(v for v in _USED)
    print("  asset uses >2:", {k: v for k, v in use.items() if v > 2})
    miss = [k for k, t in _KEYS if t is None]
    print(f"  text synced to speech: {len(_KEYS) - len(miss)}/{len(_KEYS)}; beat-timed: {miss}")
    longest = sorted(((S["end"] - S["start"], i) for i, S in enumerate(scenes)), reverse=True)[:6]
    print("  longest scenes:", [(round(a, 1), i) for a, i in longest])


if __name__ == "__main__":
    main()
