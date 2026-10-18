# Build the master timeline from aligned chunks.
# usage: timeline.py align.json sil_fine.txt narr_dur video_before_dur video_after_dur out.json
import sys, json, numpy as np
X = np.load(sys.argv[7]); XSR = 44100
items = json.load(open(sys.argv[1]))
sil = [tuple(map(float, l.split()[:2])) for l in open(sys.argv[2])]
NARR_DUR = float(sys.argv[3])
VDUR = {'BEFORE': float(sys.argv[4]), 'AFTER': float(sys.argv[5])}
OUT = sys.argv[6]
SNAP = 0.35

def snap_end(t):
    c = [a for a, b in sil if abs(a - t) <= SNAP]
    return min(c, key=lambda a: abs(a - t)) if c else t

def snap_start(t):
    c = [b for a, b in sil if abs(b - t) <= SNAP]
    return min(c, key=lambda b: abs(b - t)) if c else t

# group chunks into sentences (lines), keep markers in order
seq = []
for it in items:
    if 'marker' in it:
        seq.append({'marker': it['marker'], 'slide': it['slide']})
        continue
    if it['ci'] == 0:
        seq.append({'slide': it['slide'], 'chunks': []})
    seq[-1]['chunks'].append(it)
sents = [s for s in seq if 'chunks' in s]
# sentence boundaries: longest pause between the two sentences' word timings
sents[0]['s'] = snap_start(sents[0]['chunks'][0]['s'])
sents[-1]['e'] = snap_end(sents[-1]['chunks'][-1]['e'])
FALLBACK = []
for a, b in zip(sents, sents[1:]):
    ra, rb = a['chunks'][-1]['e'], b['chunks'][0]['s']
    lo, hi = min(ra, rb) - 0.45, max(ra, rb) + 0.45
    c = [(x, y) for x, y in sil if x >= lo and y <= hi]
    if c:
        x, y = max(c, key=lambda p: p[1] - p[0])
        a['e'], b['s'] = x, y
    else:
        # TTS ran the sentences together: cut at the energy minimum between them
        lo2, hi2 = min(ra, rb) - 0.3, max(ra, rb) + 0.3
        best = min((float(np.sqrt(np.mean(X[int(t * XSR) - 441:int(t * XSR) + 441] ** 2))), t)
                   for t in np.arange(lo2, hi2, 0.005))[1]
        a['e'] = b['s'] = round(best, 3)
        FALLBACK.append((a['chunks'][-1]['text'], b['chunks'][0]['text'], ra, rb))
for s in sents:
    for a, b in zip(s['chunks'], s['chunks'][1:]):
        t = b['s']
        c = [(x, y) for x, y in sil if x >= a['s'] and y <= b['e'] and abs((x + y) / 2 - t) <= SNAP]
        b['cs'] = (min(c, key=lambda p: abs((p[0] + p[1]) / 2 - t))[1] if c else t)
    s['chunks'][0]['cs'] = s['s']
    for i, c in enumerate(s['chunks']):
        c['ce'] = s['chunks'][i + 1]['cs'] if i + 1 < len(s['chunks']) else s['e']
for a, b in zip(sents, sents[1:]):
    assert b['s'] >= a['e'] - 1e-6
print('fallback boundaries:', len(FALLBACK))
for f in FALLBACK: print('  ', f)

# narration cut points: midpoint of the natural gap around a marker
segs = []      # output audio/visual segments: dict(kind, src_s, src_e) in narration time or video
cur = 0.0
marker_cuts = []
for i, s in enumerate(seq):
    if 'marker' in s:
        prev = next(x for x in reversed(seq[:i]) if 'chunks' in x)
        nxt = next(x for x in seq[i + 1:] if 'chunks' in x)
        mid = (prev['e'] + nxt['s']) / 2
        marker_cuts.append((mid, s['marker'], prev['e'], nxt['s']))
tl = []        # (out_start, out_end, kind, arg, src_start)
t_out = 0.0
pos = 0.0
for mid, mk, pe, ns in marker_cuts:
    tl.append((t_out, t_out + (mid - pos), 'narr', None, pos)); t_out += mid - pos; pos = mid
    if mk[0] == '@PAUSE':
        need = float(mk[1]) - (ns - pe)       # total pause = script value
        if need > 0:
            tl.append((t_out, t_out + need, 'silence', None, None)); t_out += need
    elif mk[0] == '@VIDEO':
        # video starts right after the natural trailing pause of the sentence; trim the halves so
        # the gap on each side equals the narrator's own half-pause
        d = VDUR[mk[1]]
        tl.append((t_out, t_out + d, 'video', mk[1], 0.0)); t_out += d
tl.append((t_out, t_out + (NARR_DUR - pos), 'narr', None, pos)); t_out += NARR_DUR - pos

def n2o(t):
    for a, b, k, arg, src in tl:
        if k == 'narr' and src - 1e-6 <= t <= src + (b - a) + 1e-6:
            return a + (t - src)
    raise ValueError(t)

for s in sents:
    s['os'], s['oe'] = n2o(s['s']), n2o(s['e'])
    for c in s['chunks']:
        c['os'], c['oe'] = n2o(c['cs']), n2o(c['ce'])

# slide changes: after the last sentence of slide N ends, before the first of slide N+1 starts
nslides = max(s['slide'] for s in seq)
slide_start = {1: 0.0}
for n in range(2, nslides + 1):
    last = [s for s in sents if s['slide'] == n - 1][-1]
    first = [s for s in sents if s['slide'] == n][0]
    a, b = last['oe'], first['os']
    slide_start[n] = min(a + 0.15, (a + b) / 2)
total = t_out
slides = [{'n': n, 'start': slide_start[n], 'end': slide_start.get(n + 1, total)} for n in range(1, nslides + 1)]

# subtitle events: chunk shown from its start until the next chunk starts (bridging short pauses),
# never across a slide change or into a video
cuts = sorted([x['start'] for x in slides[1:]] + [a for a, b, k, *_ in tl if k == 'video'])
subs = []
allc = [c for s in sents for c in s['chunks']]
for i, c in enumerate(allc):
    st = c['os']; en = c['oe']
    if i + 1 < len(allc):
        nx = allc[i + 1]['os']
        en = nx if nx - en < 0.8 else en + 0.25
    else:
        en = min(en + 0.5, total)
    nxtcut = min([x for x in cuts if x > st + 1e-6], default=total)
    en = min(en, nxtcut)
    subs.append({'s': round(st, 3), 'e': round(en, 3), 'text': c['text'], 'slide': c['slide']})
json.dump({'total': total, 'timeline': tl, 'slides': slides, 'subs': subs,
           'sents': [{'slide': s['slide'], 's': s['os'], 'e': s['oe'], 'text': ' '.join(c['text'] for c in s['chunks'])} for s in sents]},
          open(OUT, 'w'), ensure_ascii=False, indent=1)
print('total', round(total, 3))
for x in tl: print('TL', [round(v, 3) if isinstance(v, float) else v for v in x])
