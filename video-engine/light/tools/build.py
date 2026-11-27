"""타임라인 + HTML 생성.  usage: python3 build.py <ep_dir>
ep_dir 에 script.txt, words.json, audio/voice.mp3, plan.py 가 있어야 한다.
결과: ep_dir/build/index.html, timeline.json, chapters.txt
"""
import sys, os, json, importlib.util, math, shutil
sys.path.insert(0, os.path.dirname(__file__))
from align import parse_script, screens, char_times, rms_track, build_lines, time_at
import components as C
from align import _quotes

ep = os.path.abspath(sys.argv[1])
C.BASE = os.path.join(ep, 'build')
spec = importlib.util.spec_from_file_location('plan', os.path.join(ep, 'plan.py'))
plan = importlib.util.module_from_spec(spec)
spec.loader.exec_module(plan)

text, chapters, paras = parse_script(os.path.join(ep, 'script.txt'))
scr = screens(text, paras, getattr(plan, 'OVERRIDES', ()))
full, sidx, diffs = char_times(text, json.load(open(os.path.join(ep, 'words.json'))))
voiced, onsets, dur = rms_track(os.path.join(ep, 'audio/voice.mp3'))
lines = build_lines(text, scr, full, voiced, onsets)


class Ctx:
    def __init__(self, pos, t0):
        self.pos, self.t0 = pos, t0

    def t(self, phrase, after=None):
        phrase = phrase.replace('“', '"').replace('”', '"')
        start = self.pos if after is None else text.find(after, self.pos)
        i = text.find(phrase, start)
        if i < 0 or i - self.pos > 900:
            raise SystemExit(f'reveal phrase not found: {phrase!r} after {text[self.pos:self.pos + 30]!r}')
        return max(self.t0, time_at(full, text, i) - 0.05)


def line_of(pos):
    for l in lines:
        if l['pos'] <= pos < l['end']:
            return l
    raise SystemExit(f'no line at {pos}')


# ---- 장면 시간
scenes, cursor = [], 0
for anchor, fn in plan.SCENES:
    anchor = anchor.replace('“', '"').replace('”', '"')
    p = text.find(anchor, cursor)
    if p < 0:
        raise SystemExit(f'anchor not found: {anchor!r}')
    l = line_of(p)
    if p - l['pos'] > 2:
        print(f'WARN anchor {anchor!r} is mid-line: {l["text"]!r}')
    cursor = p + 1
    scenes.append({'anchor': anchor, 'fn': fn, 'line': l['i'], 't0': l['show'] if scenes else 0.0,
                   'ch': l['ch'], 'card': isinstance(fn, tuple) and fn[0] == 'card'})

# 챕터 카드가 1초 미만이면 다음 장면을 한 줄 뒤로
for k, s in enumerate(scenes[:-1]):
    nxt = scenes[k + 1]
    if s['card'] and nxt['t0'] - s['t0'] < 1.0:
        li = nxt['line'] + 1
        nxt['line'] = li
        nxt['t0'] = lines[li]['show']
        print(f'card {s["anchor"]!r} extended to line {li}')
# 챕터가 바뀌는 장면은 이전 줄 자막이 내려가는 순간 바로 시작 (말 사이 공백에 화면이 붕 뜨지 않게)
for k, s in enumerate(scenes[1:], 1):
    if s['ch'] != scenes[k - 1]['ch'] and s['line'] > 0:
        s['t0'] = min(s['t0'], lines[s['line'] - 1]['hide'])
for k, s in enumerate(scenes):
    s['t1'] =scenes[k + 1]['t0'] if k + 1 < len(scenes) else dur + 1
    s['pos'] = lines[s['line']]['pos']

# ---- HTML
chap_titles = {c['n']: c['title'] for c in chapters if c['n'] > 0}
nch = max(chap_titles)
secs = []
for k, s in enumerate(scenes):
    if s['card']:
        body = C.card(s['fn'][1], _quotes(chap_titles[s['fn'][1]]))
    else:
        body = s['fn'](Ctx(s['pos'], s['t0']))
    hdr = 0 if (s['card'] or s['ch'] == 0) else s['ch']
    secs.append(f'<section class="scene" data-t0="{s["t0"]:.3f}" data-t1="{s["t1"]:.3f}" data-ch="{hdr}">{body}</section>')

tl = {'dur': dur, 'nch': nch,
      'titles': {n: _quotes(t) for n, t in chap_titles.items()},
      'labels': {n: ('OUTRO' if n == nch and 'OUTRO' in getattr(plan, 'FLAGS', ()) else f'CHAPTER {n}') for n in chap_titles},
      'lines': [{k: l[k] for k in ('text', 'show', 'hide', 'hl')} for l in lines]}

out = os.path.join(ep, 'build')
os.makedirs(out, exist_ok=True)
shutil.copy(os.path.join(os.path.dirname(__file__), 'style.css'), os.path.join(out, 'style.css'))
tpl = open(os.path.join(os.path.dirname(__file__), 'template.html'), encoding='utf-8').read()
open(os.path.join(out, 'index.html'), 'w', encoding='utf-8').write(
    tpl.replace('/*TL*/', 'const TL=' + json.dumps(tl, ensure_ascii=False) + ';').replace('<!--SCENES-->', '\n'.join(secs)))
json.dump({'scenes': [{k: v for k, v in s.items() if k != 'fn'} for s in scenes], **tl},
          open(os.path.join(out, 'timeline.json'), 'w'), ensure_ascii=False, indent=1)

# ---- 챕터 타임스탬프 (화면 기준: 카드 시작 시점)
def mmss(t):
    t = int(t)
    return f'{t // 60}:{t % 60:02d}'


ts = ['0:00 ' + getattr(plan, 'OPEN_TITLE', '오프닝')]
seen = set()
for s in scenes:
    if s['ch'] > 0 and s['ch'] not in seen:
        seen.add(s['ch'])
        lab = chap_titles[s['ch']]
        ts.append(f'{mmss(s["t0"])} {lab}')
open(os.path.join(ep, 'build', 'chapters.txt'), 'w').write('\n'.join(ts) + '\n')
print('\n'.join(ts))
print(f'{len(scenes)} scenes ({sum(s["card"] for s in scenes)} cards), {len(lines)} lines, dur {dur:.2f}s')
