# -*- coding: utf-8 -*-
"""Second scene kit: beat-driven infographics, chat UI, split hook, tracker.

Every element that should arrive on a narration beat carries
  data-l="k"   → the k-th narration line inside the scene's span
  data-o="s"   → optional extra offset in seconds
plus one effect class the timeline knows:
  bt       fade + rise            bt-pop   scale in
  bt-grow  bar 0 → value          bt-draw  SVG path draw
  bt-show  chat bubble (display + rise, pushes older messages up)
  bt-hot   switch to the highlighted state at that beat
Static scenes simply omit data-l and get the shared entrance.
"""
import html

esc = lambda s: html.escape(s, quote=True)


def _b(l, o=0.0, x=None):
    return (f' data-l="{l}"' + (f' data-o="{o:.2f}"' if o else "")
            + (f' data-x="{x}"' if x is not None else ""))


def _k(text):
    """sync key: the element lands when these words are actually spoken"""
    return f' data-k="{esc(text)}"'


def _c(c, o=0.0):
    """beat on a caption card instead of a sentence"""
    return f' data-c="{c}"' + (f' data-o="{o:.2f}"' if o else "")


# ── 1. split hook: two outcomes of the same date ───────────────────────────
def split_hook(left_img, right_img):
    bub = ('<svg width="34" height="34" viewBox="0 0 34 34"><path d="M5 7h24a3 3 0 0 1 3 3v12a3 3 0 0 1-3 3H14l-7 6v-6H5'
           'a3 3 0 0 1-3-3V10a3 3 0 0 1 3-3z" fill="currentColor"/></svg>')
    return f"""<div class="split">
  <div class="pane l bt-pop"{_b(0)}><img src="{left_img}" alt=""><div class="pane-tint"></div>
    <div class="pane-tag cy">여자가 먼저 연락</div>
    <div class="notif bt-pop"{_b(0, 1.15)}><span class="ni">{bub}</span><span>오늘 너무 즐거웠어요!</span></div></div>
  <div class="pane r bt-pop"{_b(0, .18)}><img src="{right_img}" alt=""><div class="pane-tint"></div>
    <div class="pane-tag am">애프터에서 끊김</div>
    <div class="notif dead bt-pop"{_b(0, 2.05)}><span class="ni">{bub}</span><span>읽음 · 답장 없음</span></div></div>
  <div class="split-mid bt"{_b(0, .3)}>같은 소개팅, <b>다른 결말</b></div>
</div>"""


# ── 2. conversion funnel ───────────────────────────────────────────────────
FUNNEL = [("첫인상", 100), ("대화", 72), ("호감 형성", 48), ("애프터", 26), ("관계 발전", 12)]
BREAK_NOTE = {0: "관심을 못 얻음", 1: "카톡에서 식음", 2: "매력이 안 전달됨", 3: "제안을 못 함", 4: ""}


def funnel(mode="all", hot=-1):
    """mode build: rows arrive one by one on line 1 (the list sentence).
    hot=k: stage k is where it breaks — later stages go dark."""
    h = ['<div class="stage"><div class="scrim wide"></div><div class="fun">',
         '<div class="fun-title bt"' + _b(0) + '>연애의 <b>전환 구조</b></div>']
    walk = mode == "walk"
    for k, (lab, v) in enumerate(FUNNEL):
        if walk:
            tag = _b(0, 0.1 + k * 0.1)
            hl = (f'<i class="fun-hl bt"{_b(k, .05, k + 1 if k < 3 else None)}></i>'
                  if k < 4 else "")
            h.append(f'<div class="fun-row"{tag}>{hl}<span class="fun-num">{k+1}</span>'
                     f'<span class="fun-lab">{esc(lab)}</span>'
                     f'<div class="fun-track"><i class="fun-fill bt-grow"{tag} style="width:{v}%"></i>'
                     + "".join(f'<span class="ftick" style="left:{q}%"></span>' for q in (25, 50, 75))
                     + f'</div><span class="fun-val">{v}%</span></div>')
            continue
        if mode == "build":
            tag = _b(1, k * 0.62) + _k(lab)
        else:
            tag = _b(0, 0.15 + k * 0.12)
        cls = "fun-row bt"
        if hot >= 0 and k > hot:
            cls += " after"
        if k == hot:
            cls += " hot"
        h.append(f'<div class="{cls}"{tag}><span class="fun-num">{k+1}</span>'
                 f'<span class="fun-lab">{esc(lab)}</span>'
                 f'<div class="fun-track"><i class="fun-fill bt-grow"{tag}'
                 f' style="width:{v}%"></i>'
                 + "".join(f'<span class="ftick" style="left:{q}%"></span>' for q in (25, 50, 75))
                 + f'</div><span class="fun-val">{v}%</span></div>')
        if k == hot and BREAK_NOTE.get(k):
            h.append(f'<div class="fun-break bt-pop"{_b(0, .75)}><i></i>{esc(BREAK_NOTE[k])}</div>')
    h.append('<div class="fun-axis"><span>다음 단계로 이어진 비율</span><span>0 · 25 · 50 · 75 · 100%</span></div>')
    if walk:
        h.append('<div class="fun-notes">' + "".join(
            f'<div class="fun-break bt-pop"{_b(k, .35, k + 1 if k < 3 else None)}><i></i>'
            f'{k+1}단계 · {esc(BREAK_NOTE[k])}</div>' for k in range(4)) + '</div>')
    h.append('</div></div>')
    return "".join(h)


# ── 3. dot-matrix comparison: 10 dates/0 vs 3 dates/2 ──────────────────────
def dots_compare():
    def row(name, n, hit, l, rate, best):
        cells = "".join(
            f'<i class="dc{" on" if k < hit else ""} bt-pop"{_b(l, .35 + k * .09)}></i>' for k in range(n))
        return (f'<div class="dc-row bt"{_b(l)}><span class="dc-name">{name}</span>'
                f'<div class="dc-cells">{cells}</div>'
                f'<span class="dc-rate{" best" if best else ""} bt-pop"{_b(l, .4 + n * .09)}>{rate}</span></div>')
    return ('<div class="stage"><div class="scrim wide"></div><div class="dcmp">'
            '<div class="dc-legend bt"' + _b(0) + '><span><i class="dc"></i>소개팅</span>'
            '<span><i class="dc on"></i>두 번째 만남</span></div>'
            + row("남자 A", 10, 0, 0, "0%", False)
            + row("남자 B", 3, 2, 1, "67%", True)
            + '<div class="dc-win bt-pop"' + _b(3) + '>횟수보다 <b>이어지는 비율</b></div>'
            '</div></div>')


# ── 4. anxiety-over-time line graph with a running clock ───────────────────
def anx_line():
    X = [190, 470, 750, 1030]
    Y = [395, 330, 210, 95]
    segs = "".join(
        f'<path class="edge-hot glow bt-draw"{_b(k)} d="M{X[k]} {Y[k]} C {X[k]+120} {Y[k]}, '
        f'{X[k+1]-120} {Y[k+1]}, {X[k+1]} {Y[k+1]}"/>' for k in range(3))
    dots = "".join(f'<circle class="node glow bt-pop"{_b(max(k-1, 0), .7 if k else 0)} cx="{X[k]}" '
                   f'cy="{Y[k]}" r="{12 if k < 3 else 17}"/>' for k in range(4))
    xl = ["보냄", "1시간", "2시간", "지금"]
    xlab = "".join(f'<text class="dlabel-dim" x="{X[k]}" y="500" text-anchor="middle">{xl[k]}</text>'
                   for k in range(4))
    grid = "".join(f'<path class="edge" d="M150 {y} L1110 {y}" opacity=".28"/>' for y in (95, 245, 395))
    ylab = "".join(f'<text class="dlabel-dim" x="120" y="{y+14}" text-anchor="end">{t}</text>'
                   for y, t in ((95, "높음"), (245, "보통"), (395, "낮음")))
    return ('<div class="diag"><div class="scrim wide"></div><div class="anx">'
            '<div class="anx-title">답장을 기다리는 동안 <b>불안</b></div>'
            '<svg width="1240" height="540" viewBox="0 0 1240 540">'
            + grid + ylab + '<path class="edge" d="M150 420 L1110 420" opacity=".6"/>' + xlab + segs + dots
            + '<g transform="translate(1150 70)"><circle r="44" fill="rgba(90,216,247,.08)" stroke="#5AD8F7" stroke-width="4"/>'
            '<path class="clock-h" d="M0 0 L0 -30" stroke="#F4F3EF" stroke-width="5" stroke-linecap="round"/>'
            '<circle r="5" fill="#F4F3EF"/></g>'
            '</svg></div></div>')


# ── 5. chat / spoken-dialogue stack ────────────────────────────────────────
def chat(msgs, phone=True, title="소개팅 상대", photo=None):
    """msgs: list of (side, text, line_in_span). side w|m|t (t = inner thought)."""
    items = []
    for m in msgs:
        side, text, l = m[0], m[1], m[2]
        o = m[3] if len(m) > 3 else 0.0
        items.append(f'<div class="msg {side} bt-show"{_b(l, o)}{_k(text)}><div class="mb">{esc(text)}</div></div>')
    body = f'<div class="chat-body">{"".join(items)}</div>'
    if phone:
        return ('<div class="stage"><div class="phone bt-pop"' + _b(0) + '>'
                f'<div class="ph-head"><i class="ph-av"></i><span>{esc(title)}</span></div>{body}</div></div>')
    return (f'<div class="talk-wrap"><div class="talk-photo bt-pop"{_b(0)}><img src="{photo}" alt=""></div>'
            f'<div class="talk">{body}</div></div>')


# ── 6. seven-step tracker ──────────────────────────────────────────────────
STEPS = ["막히는 단계 확인", "첫인상 요소 점검", "취향과 기준 드러내기", "카톡보다 실제 만남",
         "침묵 두려워하지 않기", "연기 말고 표현", "행동을 구체적으로 복기"]


def tracker(cur=-1, intro=False, title="소개팅 7단계", walk=False):
    h = ['<div class="stage"><div class="scrim wide"></div><div class="trk">',
         f'<div class="trk-title">{esc(title)}</div>']
    for k, lab in enumerate(STEPS):
        st = "done" if (cur >= 0 and k < cur) else ("cur" if k == cur else "")
        tag = (_b(0, .2 + k * .32) + _k("일곱 가지") + f' data-o2="{k * .3:.2f}"') if intro else _b(0, .08 + k * .05)
        mark = "&#10003;" if st == "done" else str(k + 1)
        hl = (f'<i class="trk-hl bt"{_b(k + 1, 0, k + 2 if k < 6 else None)}></i>'
              f'<i class="trk-ok bt-pop"{_b(k + 2, 0)}>&#10003;</i>' if walk else "")
        h.append(f'<div class="trk-row {st} bt"{tag}>{hl}<span class="trk-n">{mark}</span>'
                 f'<span class="trk-lab">{esc(lab)}</span></div>')
    h.append('</div></div>')
    return "".join(h)


# ── 7. two-node connection: holds / breaks / restores / drifts ─────────────
def link(mode="break", a="나", b="상대"):
    if "|" in mode:
        mode, a, b = (mode.split("|") + ["나", "상대"])[:3]
    return (f'<div class="diag"><div class="scrim wide"></div><div class="lnk {mode}">'
            f'<div class="lk-node a"><i></i><span>{esc(a)}</span></div>'
            '<svg class="lk-svg" width="760" height="120" viewBox="0 0 760 120">'
            '<path class="lk-l edge-hot glow" d="M0 60 L380 60"/>'
            '<path class="lk-r edge-hot glow" d="M380 60 L760 60"/></svg>'
            f'<div class="lk-node b"><i></i><span>{esc(b)}</span></div>'
            '</div></div>')


# ── 8. two-column contrast card (before / after, A / B) ────────────────────
def contrast(title, left, right, lt="", rt="", lc="neg", rc="pos", gap=.5, rl=1, ro=0.0):
    """rl: line the right column lands on; ro: extra offset (one-line scenes)."""
    def col(items, cls, t, l, base):
        rows = "".join(f'<div class="cx-item bt"{_b(l, base + .3 + k * gap)}{_k(x)}>{esc(x)}</div>'
                       for k, x in enumerate(items))
        head = f'<div class="cx-head bt"{_b(l, base)}{_k(t)}>{esc(t)}</div>' if t else ""
        first = (t or items[0])
        return f'<div class="cx-col {cls} bt"{_b(l, base)}{_k(first)}>{head}{rows}</div>'
    return ('<div class="stage"><div class="scrim wide"></div>'
            + (f'<div class="hl md gtitle bt"{_b(0)}>{esc(title)}</div>' if title else "")
            + '<div class="cx">' + col(left, lc, lt, 0, 0.0) + '<div class="cx-vs bt"' + _b(rl, ro) + _k(rt or right[0]) + '>VS</div>'
            + col(right, rc, rt, rl, ro) + '</div></div>')


# ── 9. three-question checklist (self review) ──────────────────────────────
def checklist(items, title, mode="line"):
    def tag(k, extra=0.0):
        if mode == "card":
            return _c(k, .1 + extra)
        if mode == "stagger":
            return _b(0, .3 + k * .9 + extra)
        return _b(k, extra)
    rows = "".join(f'<div class="ck-row bt"{tag(k)}{_k(x)}><i class="ck-box"><b class="bt-pop"{tag(k, .45)}'
                   f' data-o2="0.45">&#10003;</b></i><span>{esc(x)}</span></div>' for k, x in enumerate(items))
    return (f'<div class="stage"><div class="scrim wide"></div><div class="ck">'
            f'<div class="ck-title">{esc(title)}</div>{rows}</div></div>')


# ── 10. CTA card: points at the description box ────────────────────────────
def cta():
    return ('<div class="stage"><div class="scrim wide"></div><div class="cta">'
            '<div class="cta-main bt"' + _b(0, .25) + _k("설명란의") + '>설명란의 <b>비공개 특강</b></div>'
            '<div class="cta-btn bt-pop"' + _b(0, .6) + _k("확인해") + '>확인해 보세요'
            '<svg width="40" height="40" viewBox="0 0 40 40"><path d="M20 6v24M9 20l11 11 11-11" '
            'stroke="currentColor" stroke-width="5" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>'
            '</div></div></div>')
