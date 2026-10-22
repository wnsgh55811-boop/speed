import json,re,sys,difflib,wave
import numpy as np
W=sys.argv[1]; asr=json.load(open(W+'/asr.json'))
# ASR char stream
keep=lambda ch: re.match(r'[0-9A-Za-z가-힣]',ch) is not None
ac=[];at=[]   # chars, (wordstart, wordend, wordidx)
words=[w for s in asr for w in s['words']]
for wi,w in enumerate(words):
    cs=[c for c in w['w'] if keep(c)]
    for c in cs: ac.append(c.lower()); at.append(wi)
# chunks
chunks=[]; cur=None
for l in open(W+'/chunks.txt',encoding='utf-8'):
    l=l.rstrip('\n')
    if l.startswith('# '): cur=int(l[2:]); continue
    if not l: continue
    chunks.append({'slide':cur,'raw':l})
sc=[];sown=[]
for ci,c in enumerate(chunks):
    if c['raw'].startswith('!') or c['raw']=='[PAUSE]': continue
    for ch in c['raw'].lstrip('+'):
        if keep(ch): sc.append(ch.lower()); sown.append(ci)
sm=difflib.SequenceMatcher(None,sc,ac,autojunk=False)
m=[None]*len(sc)
for a,b,n in sm.get_matching_blocks():
    for k in range(n): m[a+k]=b+k
matched=sum(x is not None for x in m); print('matched',matched,'/',len(sc),'asr',len(ac))
# per chunk: first/last matched asr word
for ci,c in enumerate(chunks):
    idx=[i for i,o in enumerate(sown) if o==ci]
    if not idx: continue
    mm=[m[i] for i in idx if m[i] is not None]
    c['cov']=len(mm)/len(idx)
    c['w0']=at[mm[0]]; c['w1']=at[mm[-1]]
    c['t0']=words[c['w0']]['s']; c['t1']=words[c['w1']]['e']
# energy envelope
wf=wave.open(W+'/voice16k.wav'); x=np.frombuffer(wf.readframes(wf.getnframes()),dtype=np.int16).astype(np.float32)
hop=160; n=len(x)//hop
rms=np.sqrt((x[:n*hop].reshape(n,hop)**2).mean(1)+1e-9); db=20*np.log10(rms/32768)
thr=np.percentile(db,99)-38
sil=db<thr
def silent_run(a,b):
    """longest silent run in [a,b] seconds -> (start,end) or None"""
    i0=max(0,int(a*100)); i1=min(n,int(b*100))
    best=None;k=i0
    while k<i1:
        if sil[k]:
            j=k
            while j<i1 and sil[j]: j+=1
            if best is None or j-k>best[1]-best[0]: best=(k,j)
            k=j
        else: k+=1
    return None if best is None else (best[0]/100,best[1]/100)
spoken=[c for c in chunks if 't0' in c]
for a,b in zip(spoken,spoken[1:]):
    lo=min(a['t1'],b['t0'])-0.35; hi=max(a['t1'],b['t0'])+0.35
    r=silent_run(lo,hi)
    if r and r[1]-r[0]>=0.06:
        a['e']=r[0]; b['s']=r[1]
    else:
        mid=(a['t1']+b['t0'])/2; a['e']=mid; b['s']=mid
spoken[0]['s']=silent_run(0,spoken[0]['t0']+0.3)[1] if sil[0] else 0.0
r=silent_run(spoken[-1]['t1']-0.3,n/100); spoken[-1]['e']=r[0] if r else spoken[-1]['t1']
json.dump(chunks,open(W+'/aligned.json','w'),ensure_ascii=False,indent=0)
for c in chunks:
    if 't0' in c:
        flag='' if c['cov']>0.7 else '  <<LOWCOV'
        print(f"{c['slide']:2d} {c['s']:7.2f} {c['e']:7.2f} cov={c['cov']:.2f} {c['raw']}{flag}")
    else: print(f"{c['slide']:2d}    ----    ---- {c['raw']}")
