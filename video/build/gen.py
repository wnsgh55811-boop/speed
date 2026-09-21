# -*- coding: utf-8 -*-
import json, os, re, sys, html as H
from gen_css import CSS, BG
from gen_svg import TORN_FILTER
import gen_scenes

FPS = 30
W, Hh = 1920, 1080
SUB_MAX_W = 1560          # px; subtitle must fit on ONE line inside this
TAIL = 0.34               # visual hold after a scene's narration ends
LEAD = 0.16               # silence before a scene's narration starts

def syl(s):               # Korean syllable-ish weight for proportional splitting
    return sum(1.0 if '가' <= c <= '힣' else (0.5 if c.strip() else 0.25) for c in s)

def est_dur(text):        # fallback only; replaced by measured mp3 durations
    return round(syl(text)/5.6 + 0.62, 3)

def load(p, d=None):
    return json.load(open(p)) if os.path.exists(p) else d

def build_timing(S):
    durs = load('durations.json', {}) or {}
    bounds = load('cue_bounds.json', {}) or {}
    t = 0.0
    for i, sc in enumerate(S):
        full = ' '.join(sc['cues'])
        d = durs.get(str(i))
        sc['_measured'] = d is not None
        d = float(d) if d is not None else est_dur(full)
        sc['_audio'] = d
        sc['_start'] = round(t, 3)
        sc['_dur'] = round(LEAD + d + TAIL, 3)
        # per-cue windows, proportional by syllable weight inside the measured clip
        b = bounds.get(str(i))
        if b and len(b) == len(sc['cues']) - 1:
            # real speech gaps: cue k runs from one detected pause to the next
            edges = [0.0] + list(b) + [d]
            sc['_aligned'] = True
        else:
            ws = [syl(c) for c in sc['cues']]; tot = sum(ws) or 1.0
            edges, acc = [0.0], 0.0
            for w in ws:
                acc += d * (w/tot); edges.append(acc)
            sc['_aligned'] = False
        sc['_cues'] = []
        for k, c in enumerate(sc['cues']):
            st = t + LEAD + edges[k]
            sc['_cues'].append({'text': c, 'start': round(st, 3),
                                'dur': round(edges[k+1] - edges[k], 3)})
        t += sc['_dur']
    return round(t, 3)

def sub_lines(S, widths):
    """Split each cue into ONE-LINE subtitle segments using measured pixel widths."""
    out = []
    for sc in S:
        # rule 3: if the centre type is the same sentence, drop the subtitle
        v = sc['vis']
        centre = {str(v.get(k, '')).replace('\n', ' ') for k in ('big', 'target', 'center')}
        for cu in sc['_cues']:
            txt = cu['text']
            if txt.strip() in centre:
                continue
            parts = split_fit(txt, widths)
            n = len(parts)
            for j, p in enumerate(parts):
                out.append({'t': round(cu['start'] + cu['dur']*j/n, 3),
                            'd': round(cu['dur']/n, 3), 'text': p})
    return out

def split_fit(txt, widths):
    if widths.get(txt, 0) <= SUB_MAX_W:
        return [txt]
    words = txt.split(' ')
    if len(words) == 1:
        return [txt]
    # greedy pack using measured width of each candidate line
    lines, cur = [], ''
    for w in words:
        cand = (cur + ' ' + w).strip()
        if cur and widths.get(cand, 10**9) > SUB_MAX_W:
            lines.append(cur); cur = w
        else:
            cur = cand
    if cur: lines.append(cur)
    return lines

def bg_html(fam):
    base, bloom = BG[fam]
    return (f'<div class="bg"><div class="base" style="background:{base}"></div>'
            f'<div class="bloom" style="background:{bloom}"></div></div>')

def main():
    S = json.load(open('scenes.json'))
    total = build_timing(S)

    # pass 1: emit every string that may need measuring
    cand = set()
    for sc in S:
        for cu in sc['_cues']:
            t = cu['text']; cand.add(t)
            ws = t.split(' ')
            for a in range(len(ws)):
                for b in range(a+1, len(ws)+1):
                    cand.add(' '.join(ws[a:b]))
    json.dump(sorted(cand), open('sub_candidates.json','w'), ensure_ascii=False)

    widths = load('sub_widths.json', {}) or {}
    if not widths:
        print('!! no sub_widths.json yet — run measure.js first', file=sys.stderr)
    subs = sub_lines(S, widths)

    # ---- scenes ----
    scene_html, prev = [], []
    for i, sc in enumerate(S):
        fam = sc['bg']
        prev.append(fam)
        body = gen_scenes.render(sc['vis'])
        photo = ''
        if sc['vis']['kind'] == 'photo':
            photo = (f'<div class="photo" style="background-image:url(assets/img/'
                     f'{sc["vis"]["img"]}.jpg)"></div><div class="scrim"></div>')
        scene_html.append(
            f'<div class="scene clip" id="sc{i}" data-start="{sc["_start"]}" '
            f'data-duration="{sc["_dur"]}" data-track-index="1">'
            f'{bg_html(fam)}{photo}<div class="stage" id="st{i}">{body}</div></div>')

    sub_html = "".join(
        f'<div class="sub clip" data-start="{s["t"]}" data-duration="{s["d"]}" '
        f'data-track-index="2">{H.escape(s["text"])}</div>' for s in subs)

    audio_html = "".join(
        f'<audio id="vo{i}" src="assets/audio/s{i:03d}.mp3" data-start="{sc["_start"]+LEAD}" '
        f'data-track-index="3"></audio>' for i, sc in enumerate(S)
        if os.path.exists(f'../assets/audio/s{i:03d}.mp3'))

    grain = ("<div class=\"grain\" id=\"grain\" style=\"background-image:url(&quot;data:image/svg+xml,"
             "%3Csvg xmlns='http://www.w3.org/2000/svg' width='320' height='320'%3E%3Cfilter id='n'%3E"
             "%3CfeTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='2' seed='11'/%3E"
             "%3C/filter%3E%3Crect width='320' height='320' filter='url(%23n)' opacity='0.5'/%3E"
             "%3C/svg%3E&quot;)\"></div>")

    anim_js = open('../assets/anim.js').read()
    timing_js = json.dumps([{'i': i, 'start': s['_start'], 'dur': s['_dur']}
                            for i, s in enumerate(S)], ensure_ascii=False)
    html = f"""<!doctype html>
<html lang="ko"><head><meta charset="UTF-8"/>
<meta name="viewport" content="width=1920, height=1080"/>
<script src="assets/gsap.min.js"></script>
<style>{CSS}</style></head>
<body>
{TORN_FILTER}
<div id="root" data-composition-id="main" data-start="0" data-duration="{total}"
     data-width="{W}" data-height="{Hh}" data-fps="{FPS}">
{"".join(scene_html)}
<div id="subs">{sub_html}</div>
<div id="mark">이다사</div>
<div class="vig"></div>
{grain}
{audio_html}
</div>
<script>window.__HF_TIMING={timing_js};</script>
<script>{anim_js}</script>
</body></html>"""
    open('../index.html','w').write(html)
    meta = {'total': total, 'scenes': len(S), 'subs': len(subs),
            'measured': sum(1 for s in S if s['_measured']),
            'aligned': sum(1 for s in S if s.get('_aligned')),
            'timing': [{'i': i, 'key': s['key'], 'start': s['_start'], 'dur': s['_dur'],
                        'audio': s['_audio']} for i, s in enumerate(S)]}
    json.dump(meta, open('timing.json','w'), ensure_ascii=False, indent=1)
    json.dump(subs, open('subs.json','w'), ensure_ascii=False, indent=1)
    print(f'total={total:.2f}s ({total/60:.2f}min) scenes={len(S)} subs={len(subs)} '
          f'measured={meta["measured"]}/{len(S)}')

if __name__ == '__main__':
    main()
