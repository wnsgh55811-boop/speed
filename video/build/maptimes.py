# -*- coding: utf-8 -*-
"""Map every subtitle line onto the words the narration actually says.

Script text and recognised words are both reduced to bare hangul/digits and
aligned with difflib, so a line's on-screen window is the real start of its
first word and the real end of its last. No proportional guessing.
"""
import json, re, difflib, subprocess

beats  = json.load(open('beats.json'))
blocks = json.load(open('blocks2.json'))
GAP, LEAD = 0.26, 0.10
strip = lambda s: re.sub(r'[^0-9가-힣]', '', s)

cues, words_abs, t = [], [], 0.0
for bi, blk in enumerate(blocks):
    words = json.load(open(f'words/b{bi:02d}.json'))
    dur = float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration',
          '-of','csv=p=0',f'../assets/audio/b{bi:02d}.mp3'],
          capture_output=True, text=True).stdout)

    units = [(bt, li, line) for bt in blk['beats'] for li, line in enumerate(beats[bt])]
    script_chars, owner = [], []
    for u_i, (_, _, line) in enumerate(units):
        for ch in strip(line):
            script_chars.append(ch); owner.append(u_i)
    heard_chars, heard_t = [], []
    for w in words:
        for ch in strip(w['w']):
            heard_chars.append(ch); heard_t.append((w['s'], w['e']))

    for w in words:
        words_abs.append({'w': w['w'], 's': round(t + w['s'], 3), 'e': round(t + w['e'], 3)})

    sm = difflib.SequenceMatcher(None, script_chars, heard_chars, autojunk=False)
    span = {}
    for a, b, n in sm.get_matching_blocks():
        for k in range(n):
            u = owner[a+k]; s, e = heard_t[b+k]
            if u not in span: span[u] = [s, e]
            else:
                span[u][0] = min(span[u][0], s); span[u][1] = max(span[u][1], e)

    last = 0.0
    for u_i, (bt, li, line) in enumerate(units):
        s, e = span.get(u_i, (last, last + 0.6))
        s = max(s, last); e = max(e, s + 0.35); last = e
        cues.append({'beat': bt, 'li': li, 'text': line,
                     't': round(t + s, 3), 'e': round(t + e, 3)})
    print(f'b{bi:02d} {dur:6.2f}s lines {len(units):3d} matched {len(span):3d}')
    t += dur + GAP

total = round(t - GAP + 0.6, 3)
json.dump({'cues': cues, 'total': total, 'gap': GAP, 'lead': LEAD},
          open('cues.json','w'), ensure_ascii=False)
json.dump(words_abs, open('words_abs.json','w'), ensure_ascii=False)
print(f'words {len(words_abs)}  lines {len(cues)}  video {total:.1f}s ({total/60:.2f} min)  '
      f'unmatched {sum(1 for c in cues if c["e"]-c["t"] <= 0.36)}')
