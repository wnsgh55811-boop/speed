# -*- coding: utf-8 -*-
"""Build index.html from the whisper-aligned cue timings.

Subtitle windows come straight from the words the narration actually says, so
nothing here guesses at sync. Scene windows are derived from the cues they own.
"""
import json, os, sys, html as H
from css2 import CSS, BG
import render2

FPS, W, Hh = 30, 1920, 1080
SUB_MAX_W = 1560
LEAD, TAIL = 0.12, 0.10        # visual lead-in / hold; deliberately small

def main():
    cues   = json.load(open('cues.json'))
    scenes = json.load(open('scenes2.json'))
    total  = cues['total']
    by_beat = {}
    for c in cues['cues']:
        by_beat.setdefault(c['beat'], []).append(c)

    # ---- scene windows from the cues each scene owns ----
    for i, s in enumerate(scenes):
        own = [c for b in range(s['a'], s['b']+1) for c in by_beat.get(b, [])]
        s['_cues'] = own
        s['_start'] = round(max(0.0, min(c['t'] for c in own) - LEAD), 3)
        s['_end']   = round(max(c['e'] for c in own) + TAIL, 3)
    scenes.sort(key=lambda s: s['_start'])
    for i in range(len(scenes)-1):                     # butt scenes together, no dead air
        scenes[i]['_end'] = max(scenes[i]['_end'], scenes[i+1]['_start'])
        scenes[i]['_dur'] = round(scenes[i+1]['_start'] - scenes[i]['_start'], 3)
    scenes[-1]['_dur'] = round(total - scenes[-1]['_start'], 3)

    # ---- subtitles: drop a line the centre type already says ----
    widths = json.load(open('sub_widths2.json')) if os.path.exists('sub_widths2.json') else {}
    subs = []
    for s in scenes:
        v = s['vis']
        centre = {str(v.get(k,'')).replace('\n',' ').strip() for k in ('big','center','target')}
        for c in s['_cues']:
            if c['text'].strip() in centre:
                continue
            subs.append({'t': c['t'], 'd': round(max(0.45, c['e']-c['t']), 3), 'text': c['text']})
    over = [x for x in subs if widths.get(x['text'], 0) > SUB_MAX_W]

    # ---- markup ----
    scene_html = []
    for i, s in enumerate(scenes):
        base, bloom = BG[s['bg']]
        v = s['vis']
        photo = ''
        if v['kind'] == 'photo':
            photo = (f'<div class="photo" style="background-image:url(assets/img/{v["img"]}.jpg)"></div>'
                     f'<div class="scrim"></div>')
        scene_html.append(
            f'<div class="scene clip" id="sc{i}" data-start="{s["_start"]}" '
            f'data-duration="{s["_dur"]}" data-track-index="1">'
            f'<div class="bg"><i style="background:{base}"></i><i style="background:{bloom}"></i></div>'
            f'{photo}<div class="vig"></div><div class="stage" id="st{i}">{render2.render(v)}</div></div>')

    sub_html = "".join(
        f'<div class="sub clip" data-start="{x["t"]}" data-duration="{x["d"]}" '
        f'data-track-index="2">{H.escape(x["text"])}</div>' for x in subs)

    audio_html = ('<audio id="vo" src="assets/audio/master.mp3" data-start="0" data-track-index="3"></audio>'
                  if os.path.exists('../assets/audio/master.mp3') and not os.environ.get('HF_NO_AUDIO') else '')

    grain = ("<div class=\"grain\" id=\"grain\" style=\"background-image:url(&quot;data:image/svg+xml,"
             "%3Csvg xmlns='http://www.w3.org/2000/svg' width='320' height='320'%3E%3Cfilter id='n'%3E"
             "%3CfeTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='2' seed='11'/%3E"
             "%3C/filter%3E%3Crect width='320' height='320' filter='url(%23n)' opacity='0.5'/%3E"
             "%3C/svg%3E&quot;)\"></div>")

    torn = """<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>
 <filter id="torn" x="-22%" y="-22%" width="144%" height="144%" color-interpolation-filters="sRGB">
  <feMorphology in="SourceAlpha" operator="dilate" radius="12" result="fat"/>
  <feGaussianBlur in="fat" stdDeviation="10" result="soft"/>
  <feTurbulence type="fractalNoise" baseFrequency="0.018" numOctaves="2" seed="7" result="noise"/>
  <feDisplacementMap in="soft" in2="noise" scale="60" xChannelSelector="R" yChannelSelector="G" result="wob"/>
  <feComponentTransfer in="wob" result="paper">
   <feFuncA type="discrete" tableValues="0 0 0 0 0 0 1 1 1 1"/></feComponentTransfer>
  <feFlood flood-color="#f5f3ed" result="white"/>
  <feComposite in="white" in2="paper" operator="in" result="sheet"/>
  <feMerge><feMergeNode in="sheet"/><feMergeNode in="SourceGraphic"/></feMerge>
 </filter></defs></svg>"""

    timing = json.dumps([{'i': i, 'start': s['_start'], 'dur': s['_dur'], 'kind': s['vis']['kind']}
                         for i, s in enumerate(scenes)], ensure_ascii=False)
    anim = open('../assets/anim2.js').read()

    html = f"""<!doctype html>
<html lang="ko"><head><meta charset="UTF-8"/>
<meta name="viewport" content="width=1920, height=1080"/>
<script src="assets/gsap.min.js"></script>
<style>{CSS}</style></head>
<body>
{torn}
<div id="root" data-composition-id="main" data-start="0" data-duration="{total}"
     data-width="{W}" data-height="{Hh}" data-fps="{FPS}">
{"".join(scene_html)}
<div id="subs">{sub_html}</div>
<div id="mark">이다사</div>
{grain}
{audio_html}
</div>
<script>window.__HF_TIMING={timing};</script>
<script>{anim}</script>
</body></html>"""
    open('../index.html','w').write(html)
    json.dump({'total': total, 'scenes': len(scenes), 'subs': len(subs),
               'timing': [{'i':i,'start':s['_start'],'dur':s['_dur'],'key':f"{s['a']}-{s['b']}"}
                          for i,s in enumerate(scenes)]}, open('timing2.json','w'), indent=1)
    json.dump([x['text'] for x in subs], open('sub_texts.json','w'), ensure_ascii=False)
    print(f"total={total:.2f}s ({total/60:.2f}min) scenes={len(scenes)} subs={len(subs)} "
          f"over-one-line={len(over) if widths else 'unmeasured'}")
    if widths and over:
        for x in over[:5]: print('  OVER:', widths.get(x['text']), x['text'])

if __name__ == '__main__':
    main()
