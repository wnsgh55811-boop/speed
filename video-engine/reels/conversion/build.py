# -*- coding: utf-8 -*-
"""9:16 reel — "마케팅의 핵심은 전환" (28.8s narration, 내-목소리-v4 / Seed Audio 1.0).

Writes index.html next to this file: one root composition, ten scenes, one
paused GSAP timeline. Captions are measured with the real font here and the
build fails if any would need a second line.
"""
import html
import os

from PIL import ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 1080, 1920
TOTAL = 29.2                      # 28.8s narration + short hold on the end card
CAP_PX, CAP_MAX = 54, 940

# ── scenes: (id, start, end, background family) ─────────────────────────────
# bg rotation a b c a d b c a b d — never the same family three in a row
SCENES = [
    ("s1", 0.00, 2.55, "a"), ("s2", 2.55, 6.15, "b"), ("s3", 6.15, 9.05, "c"),
    ("s4", 9.05, 10.80, "a"), ("s5", 10.80, 14.60, "d"), ("s6", 14.60, 16.85, "b"),
    ("s7", 16.85, 18.55, "c"), ("s8", 18.55, 20.60, "a"), ("s9", 20.60, 25.15, "b"),
    ("s10", 25.15, TOTAL, "d"),
]

# ── captions: (start, end, text) — synced to the narration's pauses ─────────
# The last line is dropped: the end card shows the same sentence in the centre.
CAPS = [
    (0.31, 1.20, "마케팅, 아직도"), (1.20, 2.45, "조회수로 평가하세요?"),
    (2.60, 3.50, "만 명이 봐도,"), (3.59, 4.62, "아무도 사지 않으면"),
    (4.73, 6.10, "매출은 0원입니다"),
    (6.23, 6.98, "마케팅의 핵심은"), (6.98, 7.85, "노출이 아니라"),
    (8.02, 8.95, "전환입니다"),
    (9.17, 10.70, "전환은 세 단계로 일어납니다"),
    (10.86, 11.80, "멈추게 하고,"), (11.90, 12.80, "믿게 하고,"),
    (12.89, 14.50, "움직이게 하는 것"),
    (14.85, 15.55, "첫 3초에"), (15.55, 16.80, "고객의 문제를 정확히 짚고"),
    (17.05, 18.50, "후기와 숫자로 신뢰를 쌓고"),
    (18.67, 19.45, "지금 해야 할"), (19.45, 20.55, "단 하나의 행동을 보여주세요"),
    (20.72, 21.80, "전환율이 1%에서"), (21.80, 22.78, "2%가 되면,"),
    (22.84, 23.92, "광고비는 그대로인데"), (24.00, 25.10, "매출은 두 배입니다"),
    (25.28, 26.10, "많이 보이는 것보다"), (26.10, 27.30, "한 명을 움직이는 것"),
]

font = ImageFont.truetype(os.path.join(HERE, "assets/fonts/Pretendard-Bold.otf"), CAP_PX)
for _, _, t in CAPS:
    w = font.getlength(t)
    assert w <= CAP_MAX, f"caption would wrap ({w:.0f}px): {t}"

# ── pictograms (stroke style, currentColor) ─────────────────────────────────
def svg(body, vb="0 0 64 64", cls="pic"):
    return (f'<svg class="{cls}" viewBox="{vb}" fill="none" stroke="currentColor" '
            f'stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round">{body}</svg>')

EYE = svg('<path d="M4 32 C14 16 50 16 60 32 C50 48 14 48 4 32Z"/><circle cx="32" cy="32" r="9"/>'
          '<circle cx="32" cy="32" r="3" fill="currentColor"/>')
PERSON = svg('<circle cx="32" cy="20" r="9" fill="currentColor" stroke="none"/>'
             '<path d="M14 56 C14 40 50 40 50 56Z" fill="currentColor" stroke="none"/>', cls="pp")
CART = svg('<path d="M6 10h8l7 30h30l6-22H17"/><circle cx="25" cy="51" r="4"/><circle cx="47" cy="51" r="4"/>')
HAND = svg('<path d="M22 34V14a4 4 0 0 1 8 0v16M30 28V10a4 4 0 0 1 8 0v20M38 28V14a4 4 0 0 1 8 0v22'
           'c0 12-7 20-17 20-7 0-11-4-15-10l-6-10a4 4 0 0 1 7-4l5 6"/>')
SHIELD = svg('<path d="M32 6 52 14v16c0 14-9 23-20 28C21 53 12 44 12 30V14Z"/><path d="m23 32 6 6 13-14"/>')
CURSOR = svg('<path d="M14 8 48 30 33 34 42 52 35 55 26 37 16 47Z" fill="currentColor"/>')
STAR = ('<svg class="star" viewBox="0 0 64 64"><path d="M32 5l8.3 17 18.7 2.7-13.5 13.2 3.2 18.6'
        'L32 47.7 15.3 56.5l3.2-18.6L5 24.7 23.7 22Z"/></svg>')
ARROW = svg('<path d="M32 10v44M16 38l16 16 16-16"/>', cls="arrow")
CLOCK = svg('<circle cx="32" cy="34" r="22"/><path d="M32 22v12l8 6M26 6h12"/>')

# ── scene bodies ────────────────────────────────────────────────────────────
people = "".join(f'<span class="pcell" data-i="{i}">{PERSON}</span>' for i in range(30))
dots = "".join(f'<i class="dot{" hero" if i == 33 else ""}"></i>' for i in range(60))
ticks = "".join(
    f'<i class="tick" style="transform:rotate({i * 30}deg) translateY(-205px)"></i>' for i in range(12))
stars = "".join(f'<span class="sw" id="st{i}">{STAR}</span>' for i in range(5))

BODY = {
"s1": f"""
  <div class="kicker">MARKETING</div>
  <div class="eyewrap">{EYE}</div>
  <div class="views"><b>10,000</b><span>views</span></div>
  <div class="spark"><i></i><i></i><i></i><i></i><i></i><i></i><i></i></div>
  <div class="hl s1hl">조회수 = 성과<em>?</em></div>""",
"s2": f"""
  <div class="label">10,000명이 봤다</div>
  <div class="crowd">{people}</div>
  <div class="cartrow">{CART}<span>구매 <b>0</b>건</span></div>
  <div class="zero"><small>매출</small>₩0</div>""",
"s3": f"""
  <div class="label">마케팅의 핵심</div>
  <div class="word w-dim">노출<i class="strike"></i></div>
  {ARROW}
  <div class="word w-hot">전환</div>""",
"s4": """
  <div class="label">전환의 3단계</div>
  <div class="funnel">
    <div class="tier t1"><b>01</b>멈추게</div>
    <div class="tier t2"><b>02</b>믿게</div>
    <div class="tier t3"><b>03</b>움직이게</div>
  </div>
  <div class="drop"></div>""",
"s5": f"""
  <div class="steps">
    <div class="step" id="sp0"><span class="ic">{HAND}</span><div><small>STOP</small>멈추게</div></div>
    <div class="step" id="sp1"><span class="ic">{SHIELD}</span><div><small>TRUST</small>믿게</div></div>
    <div class="step" id="sp2"><span class="ic">{CURSOR}</span><div><small>ACTION</small>움직이게</div></div>
  </div>""",
"s6": f"""
  <div class="label"><b>STEP 1</b> 멈추게</div>
  <div class="ring">{ticks}<div class="sec"><b>3</b>초</div></div>
  <div class="sub">고객의 <em>문제</em>부터 짚어라</div>""",
"s7": f"""
  <div class="label"><b>STEP 2</b> 믿게</div>
  <div class="score"><b>4.9</b><span>/ 5.0</span></div>
  <div class="stars">{stars}</div>
  <div class="bubble">“상담 받고 진짜 달라졌어요”</div>
  <div class="meta">실제 후기 <b>1,280</b>건</div>""",
"s8": f"""
  <div class="label"><b>STEP 3</b> 움직이게</div>
  <div class="cta"><span class="ripple"></span>지금 신청하기 →</div>
  <div class="cursor">{CURSOR}</div>
  <div class="sub">버튼은 <em>단 하나</em></div>""",
"s9": """
  <div class="label">광고비는 그대로</div>
  <div class="chart">
    <div class="yaxis"><span>×2</span><span>×1.5</span><span>×1</span><span>×0.5</span><span>0</span></div>
    <div class="grid"><i></i><i></i><i></i><i></i><i></i></div>
    <div class="col c1"><div class="val">매출 ×1</div><div class="bar"><i></i></div><div class="xl">전환율 <b>1%</b></div></div>
    <div class="col c2"><div class="val">매출 ×2</div><div class="bar"><i></i></div><div class="xl">전환율 <b>2%</b></div></div>
    <div class="budget">광고비 <b>=</b> 동일</div>
  </div>
  <div class="double">매출 <em>2배</em></div>""",
"s10": f"""
  <div class="dots">{dots}</div>
  <div class="one">한 명을 움직여라</div>
  <div class="end"><small>그게,</small><span>마케팅<i class="period"></i></span></div>""",
}

# ── assemble ────────────────────────────────────────────────────────────────
scene_html = []
for sid, t0, t1, bg in SCENES:
    scene_html.append(
        f'<div class="clip scene bg-{bg}" id="{sid}" data-start="{t0:.2f}" '
        f'data-duration="{t1 - t0:.2f}" data-track-index="0">'
        f'<div class="stage">{BODY[sid]}\n  </div></div>')
cap_html = [
    f'<div class="clip capclip" id="cap{i:02d}" data-start="{a:.2f}" data-duration="{b - a:.2f}" '
    f'data-track-index="2"><div class="cap">{html.escape(t)}</div></div>'
    for i, (a, b, t) in enumerate(CAPS)]

css = open(os.path.join(HERE, "style.css"), encoding="utf-8").read()
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
     data-start="0" data-duration="{TOTAL}">
{chr(10).join(scene_html)}
  <div class="clip fx" id="fx" data-start="0" data-duration="{TOTAL}" data-track-index="1">
    <svg class="grain" width="100%" height="100%"><filter id="gn"><feTurbulence type="fractalNoise"
      baseFrequency=".85" numOctaves="2" stitchTiles="stitch"/><feColorMatrix type="saturate" values="0"/></filter>
      <rect width="100%" height="100%" filter="url(#gn)"/></svg>
    <div class="vignette"></div>
  </div>
{chr(10).join(cap_html)}
  <audio id="vo" src="assets/audio/narr.mp3" data-start="0" data-duration="28.8"></audio>
</div>
<script>
var CAPS = {[round(a, 2) for a, _, _ in CAPS]};
var SCENES = {{{", ".join(f'"{s}": {a}' for s, a, _, _ in SCENES)}}};
{js}
</script>
</body>
</html>
"""
open(os.path.join(HERE, "index.html"), "w", encoding="utf-8").write(doc)
print("wrote index.html,", len(SCENES), "scenes,", len(CAPS), "captions")
