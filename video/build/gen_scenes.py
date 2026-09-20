# -*- coding: utf-8 -*-
from gen_svg import icon, xmark
import html as H
def e(s): return H.escape(str(s))
def nl(s): return e(s).replace("\n", "<br>")   # only used in centre display type, never body copy

def _dots(v, color):
    on = max(1, min(5, round(v/20)))
    return ('<div class="dots" style="color:%s">' % color +
            "".join('<i class="dot%s"></i>' % (" on" if i < on else "") for i in range(5)) + "</div>")
def _ticks(n=10):
    return '<div class="ticks">' + '<i class="tick"></i>'*n + '</div>'

def r_hero(v):
    ic = f'<div class="hero-ic">{icon(v.get("icon","check"), 128)}</div>' if v.get("icon") else ""
    sup = f'<div class="kicker">{e(v["sup"])}</div>' if v.get("sup") else ""
    cls = "h-lg" if v.get("small") else "h-xl"
    sub2 = f'<div class="h-sm muted">{e(v["sub2"])}</div>' if v.get("sub2") else ""
    ring = '<div class="ring"></div>' if v.get("ring") else ""
    return f'{ic}{ring}{sup}<div class="{cls}">{nl(v["big"])}</div>{sub2}'

def r_quote(v):
    return (f'<div class="qmark">&ldquo;</div>'
            f'<div class="h-lg" style="max-width:1400px">{nl(v["big"])}</div>')

def r_chapter(v):
    return (f'<div class="chapnum">{e(v["num"])}</div>'
            f'<div class="h-lg">{e(v["big"])}</div>')

def r_cta(v):
    return (f'{icon("play",120,"#e8b46a")}<div class="h-lg accent">{e(v["big"])}</div>'
            f'<div class="h-sm muted">{e(v["sub2"])}</div>')

def r_strike(v):
    col = "#e8b46a" if v.get("soft") else "#ef5f8c"
    return (f'<div class="strikewrap"><div class="h-lg">{e(v["target"])}</div>'
            f'<div class="strikeline" style="background:{col}"></div>'
            f'<div class="xmark">{xmark(72,col)}</div></div>'
            f'<div class="h-sm muted">{e(v["note"])}</div>')

def r_gauge(v):
    return (f'<div class="h-md">{e(v["title"])}</div>'
            f'<div class="gauge"><div class="gtrack"><div class="gfill" data-w="{v["value"]}"></div>'
            f'{"".join(["<div class=gscale>"]+["<i></i>"]*10+["</div>"])}'
            f'<div class="gknob" data-w="{v["value"]}"></div></div>'
            f'<div class="axis"><span>{e(v["lo"])}</span><span>{e(v["hi"])}</span></div></div>'
            + (f'<div class="h-sm muted">{e(v["caption"])}</div>' if v.get("caption") else ""))

def r_bars(v):
    rows = ""
    pal = {"pink":"#ef5f8c","amber":"#e8b46a","teal":"#59c2a0"}
    for lab, val, c in v["rows"]:
        col = pal.get(c, "#ef5f8c")
        rows += (f'<div class="barrow"><div class="barhead"><div class="barlab">{e(lab)}</div>'
                 f'{_dots(val, col)}</div>'
                 f'<div class="track">{_ticks()}<div class="fill" data-w="{val}" '
                 f'style="background:linear-gradient(90deg,{col}cc,{col})"></div></div></div>')
    return (f'<div class="h-md">{e(v["title"])}</div><div class="bars">{rows}'
            f'<div class="axis"><span>{e(v["lo"])}</span><span>{e(v["hi"])}</span></div></div>')

def r_compare(v):
    (lt, ls, lv), (rt, rs, rv) = v["left"], v["right"]
    lc = "#8d96a3" if v.get("neutral") else "#ef5f8c"
    rc = "#59c2a0" if not v.get("neutral") else "#e8b46a"
    def col(t, s, val, c):
        return (f'<div class="col"><div class="colt">{e(t)}</div>'
                + (f'<div class="cols">{e(s)}</div>' if s else "")
                + f'<div class="meter"><div class="meterf" data-w="{val}" style="background:{c}"></div></div>'
                + _dots(val, c) + '</div>')
    return (f'<div class="h-md">{e(v["title"])}</div><div class="cmp">'
            + col(lt, ls, lv, lc) + '<div class="divider"></div>' + col(rt, rs, rv, rc) + '</div>')

def r_split(v):
    ax = f'<div class="xmark-s">{xmark(56)}</div>' if v.get("cross_a") else ""
    bx = f'<div class="xmark-s">{xmark(56)}</div>' if v.get("cross_b") else ""
    bpick = ' style="color:#59c2a0"' if v.get("pick_b") else ""
    return (f'<div class="h-md">{e(v["title"])}</div><div class="cmp">'
            f'<div class="col"><div class="colt muted">{e(v["a"])}</div>{ax}</div>'
            f'<div class="divider"></div>'
            f'<div class="col"><div class="colt"{bpick}>{e(v["b"])}</div>{bx}</div></div>')

def r_list(v):
    marks = {"dot":'<span class="mkdot"></span>', "q":'<span class="mkq">?</span>',
             "minus":'<span class="mkm"></span>', "plus":'<span class="mkp"></span>',
             "loop":icon("loop",30), "pause":icon("pause",30)}
    mk = marks.get(v.get("mark","dot"), marks["dot"])
    rows = "".join(f'<div class="row"><span class="mk">{mk}</span><span>{e(t)}</span></div>'
                   for t in v["items"])
    return f'<div class="h-md">{e(v["title"])}</div><div class="rows">{rows}</div>'

def r_steps(v):
    rows = "".join(f'<div class="row"><span class="stepn">{i+1}</span><span>{e(t)}</span></div>'
                   for i, t in enumerate(v["items"]))
    return f'<div class="h-md">{e(v["title"])}</div><div class="rows">{rows}</div>'

def r_icons(v):
    cells = "".join(f'<div class="icell">{icon(n,104)}<div class="ilab">{e(l)}</div></div>'
                    for n, l in v["items"])
    grid = " grid4" if v.get("grid4") else ""
    return f'<div class="h-md">{e(v["title"])}</div><div class="icons{grid}">{cells}</div>'

def r_bubbles(v):
    tone = v.get("tone","say")
    cls_map = {"say":"say","her":"her","thought":"thought","mix":"say"}
    out = []
    for i, t in enumerate(v["items"]):
        c = cls_map.get(tone,"say")
        if tone == "mix": c = "say" if i % 2 == 0 else "her"
        d = " dense" if v.get("dense") else ""
        x = f'<div class="bubx">{xmark(52)}</div>' if v.get("crossed") else ""
        out.append(f'<div class="bub {c}{d}">{e(t)}{x}</div>')
    tag = ""
    if v.get("ok"): tag = '<div class="okdot"></div>'
    return (f'<div class="kicker">{e(v["title"])}</div>'
            f'<div class="bubs">{"".join(out)}</div>{tag}')

def r_photo(v):
    return f'<div class="h-lg">{e(v["center"])}</div>'

def r_portrait(v):
    return (f'<div class="pcard"><img class="paper" src="assets/img/{v["img"]}.png" '
            f'width="620" height="620" alt=""></div>'
            f'<div class="h-sm">{e(v["label"])}</div>')

def r_scale(v):
    return (f'<div class="h-md">{e(v["title"])}</div>'
            f'<div class="scale"><div class="beam">'
            f'<div class="pan up"><span>{e(v["up"])}</span></div>'
            f'<div class="pan down"><span>{e(v["down"])}</span></div>'
            f'</div><div class="fulcrum"></div></div>')

def r_venn(v):
    return (f'<div class="h-md">{e(v["title"])}</div>'
            f'<div class="venn"><div class="vc a"><span>{e(v["a"])}</span></div>'
            f'<div class="vc b"><span>{e(v["b"])}</span></div>'
            f'<div class="vmid">{nl(v["mid"])}</div></div>')

def r_mutual(v):
    glow = " glow" if v.get("glow") else ""
    return (f'<div class="h-md">{e(v["title"])}</div>'
            f'<div class="mutual{glow}"><div class="mnode">{e(v["a"])}</div>'
            f'<div class="marrows"><span class="ar r"></span><span class="ar l"></span></div>'
            f'<div class="mnode">{e(v["b"])}</div></div>')

def r_beforeafter(v):
    return (f'<div class="h-md">{e(v["title"])}</div>'
            f'<div class="bubs"><div class="bub say dense before">{e(v["before"])}'
            f'<div class="bubx">{xmark(52)}</div></div>'
            f'<div class="bub say dense after">{e(v["after"])}</div></div>')

def r_growdot(v):
    return (f'<div class="h-md">{e(v["title"])}</div>'
            f'<div class="grow"><div class="gcell"><div class="gsmall"></div>'
            f'<div class="glab">{e(v["small_l"])}</div></div>'
            f'<div class="gcell"><div class="gbig"></div>'
            f'<div class="glab">{e(v["big_l"])}</div></div></div>')

def r_path(v):
    return (f'<div class="h-md">{e(v["title"])}</div>'
            f'<div class="pathwrap"><div class="pnode dim">{e(v["a"])}</div>'
            f'<div class="pnode pick">{e(v["b"])}</div></div>')

RENDER = dict(hero=r_hero, quote=r_quote, chapter=r_chapter, cta=r_cta, strike=r_strike,
              gauge=r_gauge, bars=r_bars, compare=r_compare, split=r_split, list=r_list,
              steps=r_steps, icons=r_icons, bubbles=r_bubbles, photo=r_photo,
              portrait=r_portrait, scale=r_scale, venn=r_venn, mutual=r_mutual,
              beforeafter=r_beforeafter, growdot=r_growdot, path=r_path)

def render(vis):
    return RENDER[vis["kind"]](vis)
