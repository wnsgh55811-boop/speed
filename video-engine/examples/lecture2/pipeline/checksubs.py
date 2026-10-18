import json
sl=json.load(open('slides.json'))
src=[[p.get('text',p.get('direction')) for p in s['paras']] for s in sl]
mine=[];cur=None
for l in open('subs.txt',encoding='utf-8'):
    l=l.rstrip('\n')
    if l.startswith('## '): cur=[];mine.append(cur);continue
    if l.strip(): cur.append(l)
assert len(mine)==len(src),(len(mine),len(src))
bad=0
for i,(a,b) in enumerate(zip(src,mine),1):
    assert len(a)==len(b),(i,len(a),len(b))
    for x,y in zip(a,b):
        if x.startswith('['): continue
        parts=[p.strip() for p in y.split(' / ')]
        if ' '.join(parts)!=x: print('MISMATCH',i,'\n ',x,'\n ',' '.join(parts)); bad+=1
        for p in parts:
            if len(p)>25: print('LONG',i,len(p),p); bad+=1
print('bad',bad)
