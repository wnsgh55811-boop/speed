import json,re,difflib
FPS=30
norm=lambda s:re.sub(r'[^0-9A-Za-z가-힣]','',s)
asr=json.load(open('asr.json'))
# whisper chars with times
A=[];AT=[]
for seg in asr:
    for ws,we,w in seg['words']:
        n=norm(w)
        for k,c in enumerate(n):
            A.append(c);AT.append((ws+(we-ws)*k/len(n),ws+(we-ws)*(k+1)/len(n)))
# script chunks
chunks=[];slide=0;pause_before_next=False
for l in open('subs.txt',encoding='utf-8'):
    l=l.rstrip('\n')
    if l.startswith('## '): slide=int(l[3:]);continue
    if not l.strip(): continue
    if l.strip()=='[2초 후]': pause_before_next=True;continue
    parts=[p.strip() for p in l.split(' / ')]
    for j,p in enumerate(parts):
        chunks.append({'slide':slide,'text':p,'sent_start':j==0,'pause2':pause_before_next and j==0})
    pause_before_next=False
S=[];SI=[]
for i,c in enumerate(chunks):
    for ch in norm(c['text']): S.append(ch);SI.append(i)
sm=difflib.SequenceMatcher(None,''.join(S),''.join(A),autojunk=False)
hit={}
for a,b,n in sm.get_matching_blocks():
    for k in range(n): hit.setdefault(SI[a+k],[]).append(AT[b+k])
print('match ratio',sum(n for *_,n in sm.get_matching_blocks())/len(S))
# silences
sil=[];s0=None
for l in open('sil.txt'):
    m=re.search(r'silence_start: ([\d.]+)',l)
    if m: s0=float(m.group(1))
    m=re.search(r'silence_end: ([\d.]+)',l)
    if m: sil.append((s0,float(m.group(1))))
for i,c in enumerate(chunks):
    h=hit[i]; c['s']=min(x[0] for x in h); c['e']=max(x[1] for x in h)
    c['cov']=len(h)/len(norm(c['text']))
# snap chunk starts/ends to silence edges when close
def snap_start(t):
    best=None
    for a,b in sil:
        if abs(b-t)<0.35 and (best is None or abs(b-t)<abs(best-t)): best=b
    return best if best is not None else t
def snap_end(t):
    best=None
    for a,b in sil:
        if abs(a-t)<0.35 and (best is None or abs(a-t)<abs(best-t)): best=a
    return best if best is not None else t
for c in chunks:
    c['s2']=snap_start(c['s']); c['e2']=snap_end(c['e'])
# enforce monotonic
for i in range(1,len(chunks)):
    if chunks[i]['s2']<chunks[i-1]['e2']-0.02:
        # whisper boundary inside continuous speech: split at the matched boundary
        m=(chunks[i-1]['e']+chunks[i]['s'])/2
        chunks[i-1]['e2']=min(chunks[i-1]['e2'],m); chunks[i]['s2']=max(chunks[i]['s2'],m)
AUDIO_END=683.23
json.dump(chunks,open('chunks_raw.json','w'),ensure_ascii=False,indent=0)
for i,c in enumerate(chunks):
    flag='' if c['cov']>0.7 else ' <-- LOW'
    print(f"{i:3d} s{c['slide']:2d} {c['s2']:7.2f} {c['e2']:7.2f} {c['cov']:.2f} {c['text']}{flag}")
