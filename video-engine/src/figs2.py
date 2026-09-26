# -*- coding: utf-8 -*-
"""Beat-aware figures and scene bodies added for multi-line scene groups.

A scene group spans several narration lines. Any element can carry:
  data-b="k"      appear when line k of the group starts
  data-bo="k"     fade out at line k
  data-bs="k"     strike-through line that draws at line k (and dims its row)
  data-bd="k"     SVG stroke that draws itself at line k
  data-tw="k"     typewriter reveal at line k      data-te="k+0.9" erase
  data-gy="0:.8,1:.2"  vertical fill that moves to each level on its beat
  data-rot="0:30,2:60" rotation (deg) keyed to beats
Beat k is resolved to an absolute time in emit.py, so motion lands on the
word that motivates it instead of a generic entrance.
"""
import html


def esc(s):
    return html.escape(s, quote=True)


def B(k):
    return f' data-b="{k}"'


# ── chat thread ────────────────────────────────────────────────────────────
def thread(msgs, title="", tag=None, tagcls=""):
    """msgs: (beat, side, text[, extra]) — side me/her/think/time/sys.

    Space for every message is laid out up front so later bubbles never push
    earlier ones around; they only fade in on their own line.
    """
    h = ['<div class="stage"><div class="phone">']
    h.append('<div class="ph-head"><i class="ph-dot"></i>'
             f'<span>{esc(title)}</span></div><div class="ph-body">')
    for m in msgs:
        b, side, txt = m[0], m[1], m[2]
        extra = m[3] if len(m) > 3 else ""
        if side == "time":
            h.append(f'<div class="ph-time"{B(b)}>{esc(txt)}</div>')
            continue
        if side == "think":
            st = f'<i class="strk" data-bs="{extra}"></i>' if extra != "" else ""
            h.append(f'<div class="msg think"{B(b)}><div class="bb">{esc(txt)}{st}</div></div>')
            continue
        unread = '<span class="unread">1</span>' if extra == "1" else ""
        hot = " hot" if extra == "hot" else ""
        h.append(f'<div class="msg {side}{hot}"{B(b)}>{unread}<div class="bb">{esc(txt)}</div></div>')
    h.append('</div></div>')
    if tag:
        h.append(f'<div class="th-tag {tagcls}"{B(tag[0])}>{esc(tag[1])}</div>')
    h.append('</div>')
    return "".join(h)


# ── typography with beats and strikes ─────────────────────────────────────
def typo(parts, size=None):
    """parts: '@k' prefix = beat, '~' prefix = dim + strike on next beat,
    '^' prefix = amber accent, '*' = small kicker line."""
    h = ['<div class="stage"><div class="scrim wide"></div>']
    for p in parts:
        b = 0
        if p.startswith("@"):
            b, p = int(p[1]), p[2:]
        cls = "hl " + (size or ("xl" if len(p) <= 12 else ("lg" if len(p) <= 20 else "md")))
        strike = ""
        if p.startswith("~"):
            p = p[1:]
            cls += " dimmed"
            strike = f'<i class="strk" data-bs="{b + 1}"></i>'
        if p.startswith("^"):
            p, cls = p[1:], cls + " accent"
        if p.startswith("*"):
            p, cls = p[1:], "kick"
        h.append(f'<div class="{cls} tline"{B(b)}><span class="tw">{esc(p)}{strike}</span></div>')
    h.append("</div>")
    return "".join(h)


def tags_html(tags):
    """Thought chips floating over a photo or a cutout."""
    pos = ["t1", "t2", "t3", "t4"]
    return "".join(f'<div class="ftag {pos[i % 4]}"{B(b)}>{esc(t)}</div>'
                   for i, (b, t) in enumerate(tags))


# ── rows / chips with beats ────────────────────────────────────────────────
def rows(title, items, strike_at=None, numbered=False, title_b=0):
    """items: (beat, text[, 'dim'|'hot'])."""
    h = ['<div class="stage"><div class="scrim wide"></div>']
    if title:
        h.append(f'<div class="hl md gtitle"{B(title_b)}>{esc(title)}</div>')
    h.append('<div class="rows" style="margin-top:46px">')
    for n, it in enumerate(items):
        b, t = it[0], it[1]
        tone = it[2] if len(it) > 2 else ""
        mark = (f'<b class="num">{n + 1}</b>' if numbered else '<i class="tick"></i>')
        st = f'<i class="strk" data-bs="{strike_at}"></i>' if strike_at is not None else ""
        h.append(f'<div class="row {tone}"{B(b)}>{mark}<span class="tw">{esc(t)}{st}</span></div>')
    h.append("</div></div>")
    return "".join(h)


def mapping(title, pairs):
    """(beat, left, right): left → right, the arrow drawing on its beat."""
    h = ['<div class="stage"><div class="scrim wide"></div>']
    if title:
        h.append(f'<div class="hl md gtitle"{B(0)}>{esc(title)}</div>')
    h.append('<div class="maprows">')
    for b, l, r in pairs:
        h.append(f'<div class="maprow"{B(b)}><span class="ml">{esc(l)}</span>'
                 '<svg width="150" height="40" viewBox="0 0 150 40"><path class="edge-hot" '
                 f'data-bd="{b}" d="M6 20 L128 20 M112 8 L132 20 L112 32"/></svg>'
                 f'<span class="mr">{esc(r)}</span></div>')
    h.append('</div></div>')
    return "".join(h)


def twobranch(title, left, right, bl=1, br=2, hot=None):
    lcls = "bl hotside" if hot == "l" else "bl"
    rcls = "bl hotside" if hot == "r" else "bl"
    return ("".join([
        '<div class="stage"><div class="scrim wide"></div>',
        f'<div class="hl md gtitle"{B(0)}>{esc(title)}</div>',
        '<svg width="1300" height="200" viewBox="0 0 1300 200" style="margin-top:22px">',
        f'<path class="edge glow" data-bd="{bl}" d="M650 10 L650 80 L300 80 L300 170"/>',
        f'<path class="edge glow" data-bd="{br}" d="M650 10 L650 80 L1000 80 L1000 170"/>',
        '</svg>',
        '<div class="branches">',
        f'<div class="{lcls}"{B(bl)}>{esc(left)}</div>',
        f'<div class="{rcls}"{B(br)}>{esc(right)}</div>',
        '</div></div>']))


# ── semantic figures ───────────────────────────────────────────────────────
def trio(items):
    """(beat, picto_svg, label) cards side by side."""
    h = ['<div class="stage"><div class="scrim wide"></div><div class="trio">']
    for b, svg, lab in items:
        h.append(f'<div class="trio-card"{B(b)}><div class="pmark">{svg}</div>'
                 f'<div class="trio-lab">{esc(lab)}</div></div>')
    h.append("</div></div>")
    return "".join(h)


def typing(first, second, erase_at=0.95):
    """A message typed, wiped, and typed again — 쓰고 지우고 다시 씁니다."""
    return ('<div class="stage"><div class="scrim"></div>'
            '<div class="inputbox"><div class="ib-lines">'
            f'<span class="ib-t" data-tw="0" data-te="0+{erase_at}">{esc(first)}</span>'
            f'<span class="ib-t" data-tw="1">{esc(second)}</span>'
            '</div>'
            '<div class="ib-send">전송</div></div>'
            '<div class="sub" data-b="1" style="margin-top:40px">한 문장을 몇 번씩</div></div>')


def twophones():
    ph = []
    for x, lab in ((330, "친구"), (970, "그녀")):
        ph.append(f'<g><rect x="{x-150}" y="40" width="300" height="520" rx="42" '
                  'fill="rgba(255,255,255,.05)" stroke="#5AD8F7" stroke-width="4"/>'
                  f'<rect x="{x-110}" y="130" width="170" height="54" rx="27" fill="rgba(255,255,255,.22)"/>'
                  f'<rect x="{x-60}" y="210" width="170" height="54" rx="27" fill="#FAE34E" opacity=".85"/>'
                  f'<rect x="{x-110}" y="290" width="130" height="54" rx="27" fill="rgba(255,255,255,.22)"/>'
                  f'<text class="dlabel" x="{x}" y="640" text-anchor="middle">{lab}</text></g>')
    return ('<div class="diag"><div class="scrim wide"></div>'
            '<svg width="1300" height="680" viewBox="0 0 1300 680">' + "".join(ph) +
            '<text data-b="0" x="650" y="340" text-anchor="middle" font-size="130" '
            'font-weight="800" fill="#F4F3EF" font-family="Pretendard">=</text>'
            '<text data-b="1" class="dlabel-dim" x="650" y="440" text-anchor="middle">같은 도구</text>'
            '</svg></div>')


def twinrise():
    """Expectation climbs, anxiety climbs right behind it."""
    ax = ('<path class="edge" d="M150 520 L1350 520" opacity=".6"/>'
          '<path class="edge" d="M150 520 L150 80" opacity=".6"/>')
    ticks = "".join(f'<path class="edge" d="M138 {y} L162 {y}" opacity=".6"/>'
                    f'<text class="axl" x="120" y="{y+12}" text-anchor="end">{t}</text>'
                    for y, t in ((460, "낮음"), (300, "보통"), (140, "높음")))
    exp = "M150 470 C 420 460, 640 360, 860 250 S 1180 130, 1300 110"
    anx = "M150 505 C 460 500, 700 430, 920 330 S 1200 200, 1300 180"
    return ('<div class="diag"><div class="scrim wide"></div>'
            '<svg width="1500" height="600" viewBox="0 0 1500 600">' + ax + ticks +
            f'<path class="edge-hot glow" data-bd="0" d="{exp}"/>'
            f'<path class="edge-warm" data-bd="1" d="{anx}"/>'
            '<text class="dlabel" data-b="0" x="1320" y="100">기대</text>'
            '<text class="dlabel warm" data-b="1" x="1320" y="200">불안</text>'
            '<g data-b="2"><rect x="230" y="70" width="420" height="64" rx="32" class="qchip"/>'
            '<text class="qtx" x="440" y="113" text-anchor="middle">재미없다고 느끼면?</text></g>'
            '<g data-b="3"><rect x="230" y="160" width="420" height="64" rx="32" class="qchip"/>'
            '<text class="qtx" x="440" y="203" text-anchor="middle">답장 끊기면?</text></g>'
            '</svg></div>')


def bigkk():
    rip = "".join(f'<circle class="rip" data-rip="{k}" cx="700" cy="300" r="170" '
                  'fill="none" stroke="#D8B368" stroke-width="3"/>' for k in range(3))
    return ('<div class="diag"><div class="scrim wide"></div>'
            '<svg width="1400" height="620" viewBox="0 0 1400 620">' + rip +
            '<text class="kk" x="700" y="390" text-anchor="middle">ㅋㅋ</text>'
            '<g data-b="1" class="qs">'
            '<text x="330" y="190" class="qm2">?</text><text x="1040" y="230" class="qm2">?</text>'
            '<text x="420" y="520" class="qm2">?</text><text x="990" y="500" class="qm2">?</text>'
            '</g></svg>'
            '<div class="sub" data-b="1" style="position:absolute;bottom:250px">단 두 글자</div></div>')


def flatline():
    d = ("M100 300 L300 300 L330 170 L360 420 L390 300 L560 300 L585 215 L610 380 "
         "L635 300 L800 300 L820 262 L840 336 L860 300 L1340 300")
    return ('<div class="diag"><div class="scrim wide"></div>'
            '<svg width="1440" height="560" viewBox="0 0 1440 560">'
            '<path class="edge" d="M100 300 L1340 300" opacity=".25"/>'
            f'<path class="edge-hot glow" data-bd="0" d="{d}"/>'
            '<circle class="node-warm" data-b="1" cx="1340" cy="300" r="14"/>'
            '<text class="dlabel" x="100" y="120">대화의 재미</text>'
            '<text class="dlabel-dim" data-b="1" x="1340" y="390" text-anchor="end">계속되지만, 평평하다</text>'
            '</svg></div>')


def mirror():
    """Her reaction drives my state — two linked gauges."""
    def gauge(x, lab, gy, fillcls):
        return (f'<rect x="{x}" y="80" width="150" height="400" rx="75" '
                'fill="rgba(255,255,255,.06)" stroke="rgba(255,255,255,.25)" stroke-width="3"/>'
                f'<rect class="{fillcls}" data-gy="{gy}" x="{x+8}" y="88" width="134" height="384" rx="67"/>'
                f'<text class="dlabel" x="{x+75}" y="560" text-anchor="middle">{lab}</text>')
    return ('<div class="diag"><div class="scrim wide"></div>'
            '<svg width="1300" height="620" viewBox="0 0 1300 620">'
            + gauge(220, "상대 반응", "0:.86,1:.22", "gfill")
            + '<path class="edge-hot glow" data-bd="0" d="M420 280 L840 280 M810 250 L845 280 L810 310"/>'
            + gauge(930, "내 편안함", "0:.8,1:.2", "gfill")
            + '<text class="dlabel" data-b="0" data-bo="1" x="1110" y="300">편안</text>'
            '<text class="dlabel warm" data-b="1" x="1110" y="300">불안</text>'
            '</svg></div>')


def escalate():
    steps = [(1, "질문 하나 더"), (2, "말 한 번 더"), (3, "좋아할 만한 답 찾기")]
    h = ['<div class="stage"><div class="scrim wide"></div>',
         f'<div class="hl md gtitle"{B(0)}>불안을 없애려고</div><div class="stairs">']
    for n, (b, t) in enumerate(steps):
        h.append(f'<div class="stair s{n}"{B(b)}>{esc(t)}</div>')
    h.append('</div></div>')
    return "".join(h)


def reveal(front, back):
    return ('<div class="stage"><div class="scrim wide"></div><div class="reveal">'
            f'<div class="rv back" data-b="2"><span class="rvk">실제로는</span>{esc(back)}</div>'
            f'<div class="rv front" data-b="0" data-bu="1"><span class="rvk">겉으로는</span>{esc(front)}</div>'
            '</div></div>')


def separate():
    return ('<div class="diag"><div class="scrim wide"></div>'
            '<svg width="1500" height="560" viewBox="0 0 1500 560">'
            '<g class="sep-l"><circle cx="360" cy="260" r="120" class="ring"/>'
            '<text class="dlabel" x="360" y="276" text-anchor="middle">내 표현</text></g>'
            '<g class="sep-r"><circle cx="1140" cy="260" r="120" class="ring warmring"/>'
            '<text class="dlabel" x="1140" y="276" text-anchor="middle">상대 반응</text></g>'
            '<path class="edge-hot glow" data-bd="1" data-bo="6" d="M485 260 L1015 260"/>'
            '<g data-b="2" data-bo="6"><rect x="600" y="160" width="300" height="64" rx="32" class="qchip"/>'
            '<text class="qtx" x="750" y="203" text-anchor="middle">반드시 좋아야?</text></g>'
            '<path class="edge" data-b="6" d="M485 260 L690 260" stroke-dasharray="14 16"/>'
            '<path class="edge" data-b="6" d="M810 260 L1015 260" stroke-dasharray="14 16"/>'
            '<text class="dlabel" data-b="6" x="750" y="420" text-anchor="middle">분리할 수 있다</text>'
            '</svg></div>')


def interview():
    h = ['<div class="stage"><div class="scrim wide"></div><div class="iv">',
         '<div class="iv-head"><span>나</span><span>상대</span></div>']
    for b in (0, 1, 2):
        h.append(f'<div class="iv-row"{B(b)}><span class="q">질문 ?</span>'
                 '<i class="iv-ar">&rarr;</i><span class="a">대답</span></div>')
    h.append('<div class="stamp" data-b="4">인터뷰</div></div></div>')
    return "".join(h)


def clock():
    ticks = "".join(
        f'<path d="M500 {130 if k % 3 else 116} L500 150" stroke="rgba(255,255,255,.45)" '
        f'stroke-width="{6 if k % 3 == 0 else 3}" transform="rotate({k*30} 500 330)"/>'
        for k in range(12))
    return ('<div class="diag"><div class="scrim wide"></div>'
            '<svg width="1400" height="660" viewBox="0 0 1400 660">'
            '<circle cx="500" cy="330" r="220" fill="rgba(255,255,255,.05)" '
            'stroke="#F4F3EF" stroke-width="6"/>' + ticks +
            '<path class="hand-h" data-rot="0:30,2:60" d="M500 330 L500 205" '
            'stroke="#F4F3EF" stroke-width="12" stroke-linecap="round" style="transform-origin:500px 330px"/>'
            '<path class="hand-m" data-spin="1" d="M500 330 L500 150" stroke="#5AD8F7" '
            'stroke-width="6" stroke-linecap="round" style="transform-origin:500px 330px"/>'
            '<circle cx="500" cy="330" r="14" fill="#F4F3EF"/>'
            '<text class="dlabel" data-b="0" data-bo="2" x="500" y="610" text-anchor="middle">1시간</text>'
            '<text class="dlabel warm" data-b="2" x="500" y="610" text-anchor="middle">2시간</text>'
            '<g transform="translate(860 250)"><rect width="380" height="96" rx="48" fill="#FAE34E"/>'
            '<text x="190" y="62" text-anchor="middle" font-size="40" font-weight="600" '
            'fill="#211F1D" font-family="Pretendard">보냈어요 :)</text>'
            '<text x="-34" y="76" font-size="34" font-weight="800" fill="#D8B368" '
            'font-family="Pretendard" text-anchor="middle">1</text></g>'
            '<text class="dlabel-dim" data-b="1" x="1050" y="420" text-anchor="middle">답장 없음</text>'
            '</svg></div>')


def converge():
    return ('<div class="diag"><div class="scrim wide"></div>'
            '<svg width="1560" height="600" viewBox="0 0 1560 600">'
            '<g data-b="0"><rect x="40" y="90" width="420" height="96" rx="48" class="srcbox"/>'
            '<text class="stx" x="250" y="150" text-anchor="middle">할 말이 생겨서</text></g>'
            '<g data-b="2"><rect x="40" y="410" width="420" height="96" rx="48" class="srcbox warmbox"/>'
            '<text class="stx" x="250" y="470" text-anchor="middle">불편함을 없애려고</text></g>'
            '<path class="edge-hot glow" data-bd="0" d="M460 138 C 760 138, 820 300, 1060 300"/>'
            '<path class="edge-warm" data-bd="2" d="M460 458 C 760 458, 820 300, 1060 300"/>'
            '<g data-b="4"><rect x="1070" y="252" width="440" height="96" rx="48" fill="#FAE34E"/>'
            '<text x="1290" y="313" text-anchor="middle" font-size="40" font-weight="600" '
            'fill="#211F1D" font-family="Pretendard">똑같은 카톡</text></g>'
            '<text class="dlabel" data-b="5" x="1290" y="440" text-anchor="middle">출발점이 다르다</text>'
            '</svg></div>')


def join():
    return ('<div class="diag"><div class="scrim wide"></div>'
            '<svg width="1400" height="600" viewBox="0 0 1400 600">'
            '<circle cx="560" cy="280" r="190" class="ring"/>'
            '<text class="dlabel" x="480" y="296" text-anchor="middle">나</text>'
            '<g class="joiner" data-join="0"><circle cx="840" cy="280" r="190" class="ring warmring"/>'
            '<text class="dlabel" x="920" y="296" text-anchor="middle">상대</text></g>'
            '<text class="dlabel-dim" data-b="1" x="700" y="296" text-anchor="middle">관계</text>'
            '<g data-b="2"><rect x="1080" y="70" width="220" height="70" rx="35" class="qchip"/>'
            '<text class="qtx" x="1190" y="117" text-anchor="middle">질문</text></g>'
            '<g data-b="3"><rect x="1080" y="250" width="220" height="70" rx="35" class="qchip"/>'
            '<text class="qtx" x="1190" y="297" text-anchor="middle">궁금함</text></g>'
            '<g data-b="4"><rect x="1080" y="430" width="220" height="70" rx="35" class="qchip"/>'
            '<text class="qtx" x="1190" y="477" text-anchor="middle">연락</text></g>'
            '</svg></div>')


def fillspace():
    blocks = [(0, "질문"), (2, "대화 살리기"), (4, "더 많은 말")]
    h = ['<div class="stage"><div class="scrim wide"></div>',
         '<div class="fs-wrap"><div class="fs-box" data-warn="6">']
    for n, (b, t) in enumerate(blocks):
        h.append(f'<div class="fs-blk k{n}"{B(b)}>{esc(t)}</div>')
    h.append('<div class="fs-her">상대의 자리</div></div>'
             '<div class="fs-cap"><span>나</span><span>상대</span></div></div>'
             '<div class="sub" data-b="6" style="margin-top:34px">상대가 들어올 공간까지 채워버린다</div></div>')
    return "".join(h)


def drag():
    return ('<div class="diag"><div class="scrim wide"></div>'
            '<svg width="1500" height="560" viewBox="0 0 1500 560">'
            '<g class="dragger"><circle cx="330" cy="290" r="70" class="ring"/>'
            '<text class="dlabel" x="330" y="306" text-anchor="middle">나</text></g>'
            '<path class="edge-hot glow" data-bd="0" d="M400 290 C 640 250, 860 330, 1060 290"/>'
            '<g class="dragged"><circle cx="1130" cy="290" r="70" class="ring warmring" opacity=".55"/>'
            '<text class="dlabel-dim" x="1130" y="306" text-anchor="middle">관계</text></g>'
            '<path class="edge-hot" data-b="1" d="M250 430 L90 430 M130 400 L85 430 L130 460"/>'
            '<text class="dlabel" data-b="2" x="750" y="140" text-anchor="middle">혼자 끌고 온 관계</text>'
            '</svg></div>')


def sameroot():
    return ('<div class="diag"><div class="scrim wide"></div>'
            '<svg width="1400" height="620" viewBox="0 0 1400 620">'
            '<g><rect x="180" y="60" width="380" height="110" rx="24" class="srcbox"/>'
            '<text class="stx" x="370" y="128" text-anchor="middle">카톡</text></g>'
            '<g><rect x="840" y="60" width="380" height="110" rx="24" class="srcbox"/>'
            '<text class="stx" x="1030" y="128" text-anchor="middle">실제 만남</text></g>'
            '<path class="edge glow" data-bd="1" d="M370 170 C 370 300, 700 300, 700 410"/>'
            '<path class="edge glow" data-bd="1" d="M1030 170 C 1030 300, 700 300, 700 410"/>'
            '<g data-b="1"><rect x="400" y="410" width="600" height="120" rx="60" class="srcbox warmbox"/>'
            '<text class="dlabel" x="700" y="486" text-anchor="middle">같은 태도</text></g>'
            '</svg></div>')


def thoughts(items):
    h = ['<div class="stage"><div class="scrim wide"></div><div class="thts">']
    for n, (b, t) in enumerate(items):
        h.append(f'<div class="tht r{n % 3}"{B(b)}>{esc(t)}</div>')
    h.append("</div></div>")
    return "".join(h)


def cta():
    return ('<div class="stage"><div class="scrim wide"></div>'
            '<div class="cta" data-b="0"><div class="cta-k">더 자세한 이야기</div>'
            '<div class="cta-t">비공개 특강</div>'
            '<div class="cta-s">카톡·소개팅·썸에서 반복되는 태도</div></div>'
            '<div class="cta-btn" data-b="1">설명란에서 확인하기 <span class="cta-ar">&darr;</span></div>'
            '</div>')
