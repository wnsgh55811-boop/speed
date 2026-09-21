import re
# -*- coding: utf-8 -*-
import html as H
from css2 import CY, AM, PK, GR
e = lambda s: H.escape(str(s))
nl = lambda s: e(s).replace("\n", "<br>")      # centre display type only, never body copy

def xmark(size=66, color=PK, sw=9):
    return (f'<svg viewBox="0 0 64 64" width="{size}" height="{size}" style="display:block;color:{color}">'
            f'<path d="M16 16l32 32M48 16L16 48" fill="none" stroke="currentColor" '
            f'stroke-width="{sw}" stroke-linecap="round"/></svg>')

def tick(size=34, color=GR, sw=7):
    """a tick that actually sits in the middle of its box"""
    return (f'<svg viewBox="0 0 32 32" width="{size}" height="{size}" style="display:block;color:{color}">'
            f'<circle cx="16" cy="16" r="13.5" fill="none" stroke="currentColor" stroke-width="2.6" '
            f'opacity=".85"/><path d="M10 16.4l4 4 8-8.4" fill="none" stroke="currentColor" '
            f'stroke-width="{sw*0.42}" stroke-linecap="round" stroke-linejoin="round"/></svg>')

def art(v, size=210):
    if not v.get("img"): return ""
    return (f'<div class="hero-ic"><img class="i3d" src="assets/img/{v["img"]}.png" '
            f'width="{size}" height="{size}" alt=""></div>')

def _dots(val, color):
    on = max(1, min(5, round(val/20)))
    return (f'<div class="dots" style="color:{color}">' +
            "".join(f'<i class="dot{" on" if i<on else ""}"></i>' for i in range(5)) + '</div>')
_ticks = lambda n=10: '<div class="ticks">' + '<i class="tick"></i>'*n + '</div>'

def _adv(t, px):
    """approx Pretendard ExtraBold advance, letter-spacing -.03em"""
    u = sum(0.95 if ord(c) > 0x1100 else (0.28 if c == ' ' else 0.52) for c in t)
    return u * px * 0.97

def one(t, px, box=1480):
    """centre hero copy is always a single line: never wraps, never breaks"""
    t = str(t).replace("\n", " ").strip()
    t = re.sub(r"\s+", " ", t)
    while _adv(t, px) > box and px > 46:
        px -= 2
    return e(t), px

def r_hero(v):
    sup = f'<div class="kicker">{e(v["sup"])}</div>' if v.get("sup") else ""
    sub2 = f'<div class="h-sm muted">{e(v["sub2"])}</div>' if v.get("sub2") else ""
    cls = "h-lg" if v.get("small") else "h-xl"
    txt, px = one(v["big"], 92 if v.get("small") else 126, 1560)
    return f'{sup}<div class="{cls}" style="font-size:{px}px">{txt}</div>{sub2}'

def r_hero3d(v):
    sup = f'<div class="kicker">{e(v["sup"])}</div>' if v.get("sup") else ""
    rest = {k: x for k, x in v.items() if k != "sup"}
    return sup + art(v, 240 if v.get("small") else 290) + r_hero(rest)

def r_quote(v):
    txt, px = one(v["big"], 92, 1400)
    return f'<div class="qmark">&ldquo;</div><div class="h-lg" style="font-size:{px}px">{txt}</div>'

def r_chapter(v):
    return f'<div class="chapnum">{e(v["num"])}</div><div class="h-lg">{e(v["big"])}</div>'

def r_cta(v):
    return (f'<div class="h-lg" style="color:{AM}">{e(v["big"])}</div>'
            f'<div class="h-sm muted">{e(v["sub2"])}</div>')

def r_strike(v):
    col = AM if v.get("soft") else PK
    return (art(v, 170) +
            f'<div class="strikewrap"><div class="h-lg">{e(v["target"])}</div>'
            f'<div class="strikeline" style="background:{col}"></div></div>'
            f'<div class="h-sm muted">{e(v["note"])}</div>')

def r_photo(v):
    if v.get("seq"):
        # one continuous shot; the lines take the centre in turn
        out = []
        for i, t in enumerate(v["seq"]):
            txt, px = one(t, 92, 1500)
            out.append(f'<div class="seqline h-lg" style="font-size:{px}px"{_at(v,i)}>{txt}</div>')
        return f'<div class="seq">{"".join(out)}</div>'
    if not v.get("center"):
        return ""
    txt, px = one(v["center"], 92, 1500)
    return f'<div class="h-lg" style="font-size:{px}px">{txt}</div>'

def r_portrait(v):
    w = v.get("w", 460)
    cls = "pcard fade" if v.get("fade") else "pcard"
    cap = f'<div class="h-sm">{e(v["label"])}</div>' if v.get("label") else ""
    return (f'<div class="{cls}"><img class="paper" src="assets/img/{v["img"]}.png" '
            f'width="{w}" height="{round(w * 1.252)}" alt=""></div>{cap}')

def r_chips(v):
    cells = "".join(f'<div class="chip{" on" if v.get("on") and t in v["on"] else ""}"{_at(v,i)}>{e(t)}</div>'
                    for i, t in enumerate(v["items"]))
    return f'<div class="h-md">{e(v["title"])}</div><div class="chips">{cells}</div>'

def _at(v, i):
    ts = v.get('_at') or []
    return f' data-at="{ts[i]}"' if i < len(ts) else ''

def r_list(v):
    marks = {"dot":'<span class="mkdot"></span>', "q":'<span class="mkq">?</span>',
             "minus":'<span class="mkm"></span>', "plus":'<span class="mkp"></span>',
             "check":tick(40), "loop":'<span class="mkm"></span>',
             "pause":'<span class="mkm"></span>'}
    mk = marks.get(v.get("mark","dot"), marks["dot"])
    rows = "".join(f'<div class="row"{_at(v,i)}><span class="mk">{mk}</span><span>{e(t)}</span></div>'
                   for i, t in enumerate(v["items"]))
    return f'<div class="h-md">{e(v["title"])}</div><div class="rows">{rows}</div>'

def r_steps(v):
    rows = "".join(f'<div class="row"{_at(v,i)}><span class="stepn">{i+1}</span><span>{e(t)}</span></div>'
                   for i, t in enumerate(v["items"]))
    return f'<div class="h-md">{e(v["title"])}</div><div class="rows">{rows}</div>'

def r_bubbles(v):
    tone = v.get("tone","say"); out = []
    for i, t in enumerate(v["items"]):
        c = {"say":"say","her":"her","thought":"thought"}.get(tone,"say")
        if tone == "mix": c = "say" if i % 2 == 0 else "her"
        d = " dense" if v.get("dense") else ""
        k = " crossed" if v.get("crossed") else ""
        big = ' style="font-size:52px"' if v.get("bigbub") else ""
        out.append(f'<div class="bub {c}{d}{k}"{_at(v,i)}{big}>{e(t)}</div>')
    head = ""
    if v.get("title"):
        cls = "h-md" if v.get("loud") else "kicker"
        col = f' style="color:{PK}"' if v.get("loud") else ""
        head = f'<div class="{cls}"{col}>{e(v["title"])}</div>'
    body = f'{head}<div class="bubs">{"".join(out)}</div>'
    if v.get("portrait"):
        w = v.get("pw", 300)
        gap = " tight" if v.get("tight") else ""
        return (f'<div class="side{gap}"><div class="pcard"><img class="paper sideimg" '
                f'style="width:{w}px;height:{round(w * 1.267)}px" '
                f'src="assets/img/{v["portrait"]}.png" alt=""></div>'
                f'<div style="display:flex;flex-direction:column;gap:18px;align-items:center">'
                f'{body}</div></div>')
    return body

def r_bars(v):
    pal = {"pink":PK,"amber":AM,"cyan":CY}
    rows = ""
    for lab, val, c in v["rows"]:
        col = pal.get(c, PK)
        rows += (f'<div class="barrow"><div class="barhead"><div class="barlab">{e(lab)}</div>'
                 f'{_dots(val,col)}</div><div class="track">{_ticks()}'
                 f'<div class="fill" data-w="{val}" style="background:linear-gradient(90deg,{col}cc,{col})">'
                 f'</div></div></div>')
    return (f'<div class="h-md">{e(v["title"])}</div><div class="bars">{rows}'
            f'<div class="axis"><span>{e(v["lo"])}</span><span>{e(v["hi"])}</span></div></div>')

def r_gauge(v):
    return (f'<div class="h-md">{e(v["title"])}</div><div class="gauge"><div class="gtrack">'
            f'<div class="gfill" data-w="{v["value"]}"></div>'
            f'<div class="gscale">{"<i></i>"*10}</div>'
            f'<div class="gknob" data-w="{v["value"]}"></div></div>'
            f'<div class="axis"><span>{e(v["lo"])}</span><span>{e(v["hi"])}</span></div></div>'
            + (f'<div class="h-sm muted">{e(v["caption"])}</div>' if v.get("caption") else ''))

def r_compare(v):
    (lt,ls,lv),(rt,rs,rv) = v["left"], v["right"]
    lc = "#8b95a3" if v.get("neutral") else PK
    rc = AM if v.get("neutral") else GR
    def col(t,s,val,c):
        return (f'<div class="col"><div class="colt">{e(t)}</div>'
                + (f'<div class="cols">{e(s)}</div>' if s else '')
                + f'<div class="meter"><div class="meterf" data-w="{val}" style="background:{c}"></div></div>'
                + _dots(val,c) + '</div>')
    return (f'<div class="h-md">{e(v["title"])}</div><div class="cmp">'
            + col(lt,ls,lv,lc) + '<div class="divider"></div>' + col(rt,rs,rv,rc) + '</div>')

def r_split(v):
    ac = " struck" if v.get("cross_a") else ""
    bc = " struck" if v.get("cross_b") else ""
    bs = f' style="color:{GR}"' if v.get("pick_b") else ""
    bm = f'<span class="pickdot">{tick(46, GR)}</span>' if v.get("pick_b") else ""
    return (f'<div class="h-md">{e(v["title"])}</div><div class="cmp">'
            f'<div class="col"><div class="colt muted{ac}">{e(v["a"])}</div></div>'
            f'<div class="divider"></div>'
            f'<div class="col"><div class="colt{bc}"{bs}>{e(v["b"])}</div>{bm}</div></div>')

def r_scale(v):
    return (art(v,150) + f'<div class="h-md">{e(v["title"])}</div>'
            f'<div class="scale"><div class="beam">'
            f'<div class="pan up"><span>{e(v["up"])}</span></div>'
            f'<div class="pan down"><span>{e(v["down"])}</span></div></div>'
            f'<div class="fulcrum"></div></div>')

def r_venn(v):
    return (f'<div class="h-md">{e(v["title"])}</div><div class="venn">'
            f'<div class="vc a"><span>{e(v["a"])}</span></div>'
            f'<div class="vc b"><span>{e(v["b"])}</span></div>'
            f'<div class="vmid">{nl(v["mid"])}</div></div>')

def r_mutual(v):
    return (f'<div class="h-md">{e(v["title"])}</div><div class="mutual">'
            f'<div class="mnode">{e(v["a"])}</div>'
            f'<div class="marrows"><span class="ar r"></span><span class="ar l"></span></div>'
            f'<div class="mnode">{e(v["b"])}</div></div>')

def r_beforeafter(v):
    return (f'<div class="h-md">{e(v["title"])}</div><div class="bubs">'
            f'<div class="bub say dense before crossed"{_at(v,0)}>{e(v["before"])}</div>'
            f'<div class="bub say dense after"{_at(v,1)}>{e(v["after"])}</div></div>')

def r_growdot(v):
    return (f'<div class="h-md">{e(v["title"])}</div><div class="grow">'
            f'<div class="gcell"><div class="gsmall"></div><div class="glab">{e(v["small_l"])}</div></div>'
            f'<div class="gcell"><div class="gbig"></div><div class="glab">{e(v["big_l"])}</div></div></div>')

R = dict(hero=r_hero, hero3d=r_hero3d, quote=r_quote, chapter=r_chapter, cta=r_cta,
         strike=r_strike, photo=r_photo, portrait=r_portrait, chips=r_chips, list=r_list,
         steps=r_steps, bubbles=r_bubbles, bars=r_bars, gauge=r_gauge, compare=r_compare,
         split=r_split, scale=r_scale, venn=r_venn, mutual=r_mutual,
         beforeafter=r_beforeafter, growdot=r_growdot)
render = lambda v: R[v["kind"]](v)
