# Align subtitle chunks (script text) to FishAudio ASR word timings.
import sys, json, re, difflib
sys.path.insert(0, sys.argv[4])
from chunks import load_chunks
asr=json.load(open(sys.argv[1])); slides=load_chunks(sys.argv[2]); out=sys.argv[3]
KEEP=re.compile(r'[0-9A-Za-z가-힣○]')
# ASR char stream with times
ac=[]; at=[]
for s in asr:
    for w in s['words']:
        cs=[c for c in w['w'] if KEEP.match(c)]
        n=len(cs)
        for i,c in enumerate(cs):
            ac.append(c); at.append((w['s']+(w['e']-w['s'])*i/max(n,1), w['s']+(w['e']-w['s'])*(i+1)/max(n,1)))
# script char stream with chunk ids
sc=[]; sid=[]; items=[]
for si,sl in enumerate(slides):
    for li,line in enumerate(sl):
        if line[0].startswith('@'): items.append({'slide':si+1,'marker':line}); continue
        for ci,c in enumerate(line):
            k=len(items); items.append({'slide':si+1,'line':li,'ci':ci,'n':len(line),'text':c})
            for ch in c:
                if KEEP.match(ch): sc.append(ch); sid.append(k)
sm=difflib.SequenceMatcher(None, sc, ac, autojunk=False)
m={}
for a,b,n in sm.get_matching_blocks():
    for i in range(n): m[a+i]=b+i
ops=[o for o in sm.get_opcodes() if o[0]!='equal']
rep=[]
for tag,a1,a2,b1,b2 in ops:
    rep.append(f"{tag:8s} script[{''.join(sc[a1:a2])}] asr[{''.join(ac[b1:b2])}] t={at[b1][0] if b1<len(at) else -1:.2f}")
open(out+'.diff.txt','w').write('\n'.join(rep))
for k,it in enumerate(items):
    if 'marker' in it: continue
    idx=[i for i,s in enumerate(sid) if s==k]
    mi=[m[i] for i in idx if i in m]
    it['matched']=len(mi)/max(len(idx),1)
    if mi: it['s']=at[min(mi)][0]; it['e']=at[max(mi)][1]
json.dump(items,open(out,'w'),ensure_ascii=False,indent=1)
print('ops',len(ops)); print('\n'.join(r for r in rep if len(r)>0)[:6000])
