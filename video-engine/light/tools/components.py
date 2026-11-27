"""장면 컴포넌트. 각 함수는 HTML 문자열을 돌려준다.

등장 시점 속성 (Ctx 에서 만든다)
  data-on=t      t 전에는 흐리게(.18) / class="hide" 면 안 보이게
  data-a0/a1     [a0,a1) 동안 class 'act' (현재 항목 강조)
  data-off=t     t 이후 사라짐
  data-grow=t    막대: t 부터 0.9초 동안 --w 까지 자람
"""
import html as _h, os
BASE = "."

E = _h.escape


def attr(on=None, a0=None, a1=None, off=None, grow=None):
    s = ''
    if on is not None:
        s += f' data-on="{on:.3f}"'
    if a0 is not None:
        s += f' data-a0="{a0:.3f}" data-a1="{(a1 if a1 is not None else 1e9):.3f}"'
    if off is not None:
        s += f' data-off="{off:.3f}"'
    if grow is not None:
        s += f' data-grow="{grow:.3f}"'
    return s


def sec(title):
    return f'<div class="sec"><i></i>{title}</div>'


def wrap(inner, title=None, cls=''):
    return f'<div class="stage {cls}">{sec(title) if title else ""}{inner}</div>'


# ---------------------------------------------------------------- 큰 문구
def big(t1, t2=None, on2=None, sub=None, t2cls=''):
    h = f'<div class="big">{t1}</div>'
    if t2:
        h += f'<div class="t2 {t2cls}"{attr(on=on2)}>{t2}</div>'
    if sub:
        h += f'<div class="bsub">{sub}</div>'
    return wrap(h, cls='center')


# ---------------------------------------------------------------- 비교
def vs(left, right, sym='≠', on_r=None, title=None, dark='r'):
    """left/right: (label, emoji, text)"""
    def card(d, k, on=None):
        lab, emo, txt = d
        lg = ' long' if len(txt.replace('<br>', '')) > 16 else ''
        return (f'<div class="c vsc {"k" if k else ""}{lg}"{attr(on=on)}><div class="lab">{lab}</div>'
                f'<div class="emo">{emo}</div><div class="txt">{txt}</div></div>')
    h = (f'<div class="row">{card(left, dark == "l")}<div class="sym">{sym}</div>'
         f'{card(right, dark == "r", on_r)}</div>')
    return wrap(h, title)


# ---------------------------------------------------------------- 카드 여러 장
def cards(items, title=None, sep='', note=None, note_on=None, w=360):
    """items: (emoji, text, on, dark, sub)"""
    parts = []
    for k, it in enumerate(items):
        emo, txt, on, dark, sub = (list(it) + [None] * 5)[:5]
        if k and sep:
            parts.append(f'<div class="arrow">{sep}</div>')
        parts.append(f'<div class="c tile {"k" if dark else ""}" style="width:{w}px"{attr(on=on)}>'
                     f'<div class="emo m">{emo}</div><div class="txt">{txt}</div>'
                     f'{f"<div class=tsub>{sub}</div>" if sub else ""}</div>')
    h = f'<div class="row">{"".join(parts)}</div>'
    if note:
        h += f'<div class="memo"{attr(on=note_on)}>{note}</div>'
    return wrap(h, title)


# ---------------------------------------------------------------- 목록
def lst(items, title='오늘 다룰 내용'):
    """items: (text, on, a0, a1)"""
    rows = []
    for k, it in enumerate(items):
        txt, on, a0, a1 = (list(it) + [None] * 4)[:4]
        rows.append(f'<div class="li"{attr(on=on, a0=a0, a1=a1)}><b>{k + 1}</b><span>{txt}</span></div>')
    return wrap(f'<div class="list">{"".join(rows)}</div>', title)


# ---------------------------------------------------------------- 네 칸
STAGES = [('호기심', '🧐'), ('호감', '😊'), ('불안', '😟'), ('확신', '👍')]


def steps(cur=None, quote=None, q_on=None, name_on=None, done=(), dim=(), stop=None, stop_txt='',
          stop_on=None, title=None, hidden=False, gap=None, gap_on=None, fills=None, empty=None,
          act_on=None, empty_txt='비어 있음'):
    """cur: 현재 칸(0-3, 검정). done: 지난 칸(흰색). dim: 흐린 칸. stop: 주황 '멈춤' 칸.
    hidden: 이름 대신 '?'. gap: (k) k 와 k+1 사이 빨간 끊김. fills: 칸별 아래 문구 [(txt,on)]"""
    cs = []
    for k, (nm, emo) in enumerate(STAGES):
        cls = 'c st'
        if k == cur:
            cls += ' k'
        if k in dim:
            cls += ' dimc'
        if k == stop:
            cls += ' stop'
        if k == empty:
            cls += ' empty'
        a = attr(on=None)
        if act_on and k == cur:
            a = attr(a0=act_on)
            cls = cls.replace(' k', ' actk')
        nm_ = '?' if hidden else nm
        inner = f'<div class="num">{k + 1}</div><div class="emo m">{"❔" if hidden else emo}</div>'
        inner += f'<div class="nm"{attr(on=name_on) if (k == cur and name_on) else ""}>{nm_}</div>'
        if k == cur and quote:
            inner += f'<div class="q"{attr(on=q_on)}>{quote}</div>'
        if fills:
            ft, fo = fills[k]
            inner += f'<div class="fill"{attr(on=fo)}>{ft}</div>'
        if k == stop:
            inner += f'<div class="tag or"{attr(on=stop_on)}>{stop_txt}</div>'
        if k == empty:
            inner += f'<div class="tag gy">{empty_txt}</div>'
        cs.append(f'<div class="{cls}"{a}>{inner}</div>')
        if k < 3:
            if gap == k:
                cs.append(f'<div class="arrow gap"{attr(on=gap_on)}><span>✕</span><em>끊김</em></div>')
            else:
                cs.append('<div class="arrow">→</div>')
    return wrap(f'<div class="row steps">{"".join(cs)}</div>', title)


# ---------------------------------------------------------------- 사람 점
def dots(n, hi, hi_on=None, title=None, cols=10, label=None, label_on=None, hi_cls='g', rest_cls='x',
         emoji=False):
    ds = ''
    for k in range(n):
        c = hi_cls if k < hi else rest_cls
        ds += f'<i class="{c}">{"👤" if emoji else ""}</i>'
    h = (f'<div class="dots {"big" if n <= 10 else ""}" style="--cols:{cols}">'
         f'<div class="pre">{"".join("<i></i>" for _ in range(n))}</div>'
         f'<div class="post hide"{attr(on=hi_on)}>{ds}</div></div>')
    if label:
        h += f'<div class="memo"{attr(on=label_on)}>{label}</div>'
    return wrap(h, title)


# ---------------------------------------------------------------- 막대
def bars(rows, title=None, note=None, note_on=None, unit_w=1000):
    """rows: (label, value_text, pct, color, on)"""
    rs = ''
    for lab, val, pct, col, on in rows:
        rs += (f'<div class="br"><div class="bl">{lab}</div><div class="bt">'
               f'<div class="bf {col}" style="--w:{pct}%"{attr(grow=on)}></div></div>'
               f'<div class="bv {col}"{attr(on=on)}>{val}</div></div>')
    h = f'<div class="c bars">{rs}</div>'
    if note:
        h += f'<div class="memo"{attr(on=note_on)}>{note}</div>'
    return wrap(h, title)


# ---------------------------------------------------------------- 밈
def meme(src, caption):
    from PIL import Image
    w, h = Image.open(os.path.join(BASE, src)).size
    k = min(1100 / w, 520 / h)
    return wrap(f'<div class="mcap">‘{caption}’</div><img class="meme" src="{src}" '
                f'style="width:{w * k:.0f}px;height:{h * k:.0f}px">', cls='center')


# ---------------------------------------------------------------- 표
def table(head, rows, title=None):
    """rows: [(label, (txt,on,win), (txt,on,win))]"""
    h = '<div class="c tbl"><div class="tr th"><div></div>' + ''.join(f'<div>{x}</div>' for x in head) + '</div>'
    for lab, *cells in rows:
        h += f'<div class="tr"><div class="tl">{lab}</div>'
        for txt, on, win in cells:
            h += f'<div class="{"win" if win else ""}"{attr(on=on)}>{txt}</div>'
        h += '</div>'
    return wrap(h + '</div>', title)


# ---------------------------------------------------------------- 답글 스레드
def thread(q, answers, title=None):
    """answers: (who, text, on, kind)  kind: None|'bad'|'good'|'badx' """
    h = f'<div class="c thr"><div class="qb"><i class="av a1"></i><span>{q}</span></div>'
    for who, txt, on, kind in answers:
        mark = {'badx': '<em class="mk x">✕</em>', 'good': '<em class="mk o">○</em>'}.get(kind, '')
        h += (f'<div class="ab {kind or ""}"{attr(on=on)}><i class="av">{who}</i>'
              f'<span>{txt}</span>{mark}</div>')
    return wrap(h + '</div>', title)


# ---------------------------------------------------------------- 체크리스트
def check(rows, title=None, result=None, result_on=None, w=1100):
    """rows: (text, check_on)"""
    h = f'<div class="c chk" style="width:{w}px">'
    for txt, on in rows:
        mark = f'<b{attr(on=on)} class="hide">✓</b>' if on is not None else ''
        h += f'<div class="cr"><span class="box">{mark}</span>{txt}</div>'
    if result:
        h += f'<div class="res"{attr(on=result_on)}>→ {result}</div>'
    return wrap(h + '</div>', title)


# ---------------------------------------------------------------- 캡션 BEFORE/AFTER
def caption(tag, lines, title='소개 문구', w=1200):
    """tag: BEFORE|AFTER ; lines: (text, on, orange)"""
    cls = 'bf' if tag == 'BEFORE' else 'af'
    h = f'<div class="c cap" style="width:{w}px"><div class="ch"><span class="pill {cls}">{tag}</span>{title}</div>'
    for txt, on, o in lines:
        h += f'<div class="cl {"o" if o else ""}"{attr(on=on)}>{txt}</div>'
    return h + '</div>'


def capwrap(inner, title=None):
    return wrap(f'<div class="col">{inner}</div>', title)


# ---------------------------------------------------------------- 고정 댓글
def pinned(on_txt=None, chk_on=None, pill_on=None, pill_off=None):
    boxes = ''.join(f'<i>✓</i>' for _ in range(5))
    h = (f'<div class="c pin"><div class="pt">📌 고정됨</div><div class="pr"><i class="av a2"></i>'
         f'<div class="pb"><div class="bar g1"></div><div class="ptx"{attr(on=on_txt)}>'
         f'🎓 23분 고객전환 마스터클래스<br><span>▶ 체크 5개로 막힌 칸 찾기</span><u>링크 열기</u></div></div></div>'
         f'<div class="five"{attr(on=chk_on)}>{boxes}<span>체크 5개 → 막힌 칸이 보임</span></div></div>'
         f'<div class="pinpill hide"{attr(on=pill_on, off=pill_off)}>고정댓글 확인 ↓</div>')
    return wrap(h, cls='center')


# ---------------------------------------------------------------- 장바구니 UI
def cart(on_stamp):
    items = [('🧥', '울 블렌드 코트', '129,000원'), ('👟', '러닝화', '89,000원'), ('🎧', '무선 이어폰', '159,000원'),
             ('🕯️', '향초 세트', '32,000원')]
    rows = ''.join(f'<div class="ci"><span class="ce">{e}</span><span class="cn">{n}</span><span class="cp">{p}</span></div>'
                   for e, n, p in items)
    h = (f'<div class="c cartui"><div class="ct">🛒 장바구니 <b>4</b></div>{rows}'
         f'<div class="ctot"><span>총 결제 금액</span><b>409,000원</b></div>'
         f'<div class="pay">결제하기<em class="stamp hide"{attr(on=on_stamp)}>결제 안 함</em></div></div>')
    return wrap(h, cls='center')


def paybtn(mode, on=None):
    if mode == 'press':
        h = (f'<div class="c payui"><div class="ptot"><span>총 결제 금액</span><b>89,000원</b></div>'
             f'<div class="pay big">💳 결제하기</div><div class="ok hide"{attr(on=on)}>✓ 결제 완료</div></div>')
    else:
        h = (f'<div class="c payui"><div class="ptot"><span>총 결제 금액</span><b>89,000원</b></div>'
             f'<div class="pay big hover">💳 결제하기<span class="cursor">➤</span></div>'
             f'<div class="hold">⏸ 버튼 위에서 멈춤</div></div>')
    return wrap(h, cls='center')


# ---------------------------------------------------------------- 채널 첫 화면
def profile(on_bio=None, on_grid=None, title='들어온 사람이 보는 곳'):
    grid = ''.join(f'<i style="background:{c}"></i>' for c in
                   ['#E9E3D8', '#DCD5C8', '#EFE9DF', '#D9D2C4', '#E4DDD1', '#EDE7DC'])
    h = (f'<div class="c prof"><div class="ph"><i class="av big"></i><div><div class="bar g1 w300"></div>'
         f'<div class="pst"><span><b>128</b>게시물</span><span><b>5.2만</b>팔로워</span></div></div></div>'
         f'<div class="bio"{attr(on=on_bio)}><div class="bar g2 w560"></div><div class="bar g2 w420"></div><em>소개 문구</em></div>'
         f'<div class="pg"{attr(on=on_grid)}>{grid}</div></div>')
    return wrap(h, title)


# ---------------------------------------------------------------- 인사이트 캡처
def shot(src, stats, title=None):
    """stats: (label, value, on, orange)"""
    ss = ''.join(f'<div class="c stat {"k" if o else ""}"{attr(on=on)}><div class="lab">{l}</div><div class="val">{v}</div></div>'
                 for l, v, on, o in stats)
    h = f'<div class="row"><img class="phone" src="{src}"><div class="stats">{ss}</div></div>'
    return wrap(h, title)


def dash(srcs, total, on_total, title='다음 영상 예고 · 1월 24일 ~ 10월 21일'):
    ims = ''.join(f'<img class="dimg" src="{s}">' for s in srcs)
    h = (f'<div class="row dashes">{ims}</div>'
         f'<div class="t2 tot"{attr(on=on_total)}>9개월 합계 {total}회</div>')
    return wrap(h, title)


# ---------------------------------------------------------------- 칩
def chips(items, title=None):
    """items: (text, on)"""
    h = ''.join(f'<div class="chip"{attr(on=on)}>{t}<em>✕</em></div>' for t, on in items)
    return wrap(f'<div class="row chips">{h}</div>', title)


# ---------------------------------------------------------------- 질문 말풍선
def bubbles(items, title=None):
    """items: (emoji, text, on)"""
    h = ''.join(f'<div class="c bub"{attr(on=on)}><span class="emo s">{e}</span>{t}</div>' for e, t, on in items)
    return wrap(f'<div class="bubs">{h}</div>', title)


# ---------------------------------------------------------------- 주차
def weeks(on1, title='과정 보여주기 (예시)'):
    rows = [('1주 차', '지금 숫자 같이 보기 · 막힌 칸 찾기'), ('2주 차', ''), ('3주 차', ''), ('4주 차', '')]
    h = '<div class="c wk"><div class="wh">📅 4주 프로그램</div>'
    for k, (w, t) in enumerate(rows):
        if k == 0:
            h += f'<div class="wr on1"{attr(on=on1)}><b>{w}</b><span>{t}</span></div>'
        else:
            h += f'<div class="wr"><b>{w}</b><span class="bar g2 w420"></span></div>'
    return wrap(h + '</div>', title)


# ---------------------------------------------------------------- 엔딩
def end():
    return wrap('<div class="endp"><div class="pk">💬 궁금한 점은 댓글로</div>'
                '<div class="pr2">구독하고 다음 영상 보기</div></div>', cls='center')


# ---------------------------------------------------------------- 챕터 카드
def card(n, title):
    return (f'<div class="ccard"><div class="cblock"><div class="cl1"><i></i>CHAPTER<i></i></div>'
            f'<div class="cnum">{n:02d}</div><div class="cbar"></div><div class="ctitle">{title}</div></div></div>')
