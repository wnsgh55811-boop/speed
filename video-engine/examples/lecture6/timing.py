import json, wave, numpy as np
W='work/'
d=json.load(open(W+'align.json')); m={int(k):v for k,v in d['m'].items()}; owner=d['owner']; at=d['at']; chunks=d['chunks']
secs=json.load(open(W+'chunks.json'))
for k,c in enumerate(chunks): c['s']=None; c['e']=None
for i,k in enumerate(owner):
    if i in m:
        t0,t1=at[m[i]]
        c=chunks[k]
        if c['s'] is None: c['s']=t0
        c['e']=t1
for k,c in enumerate(chunks):
    assert c['s'] is not None, c
# energy
w=wave.open(W+'a16.wav'); x=np.frombuffer(w.readframes(w.getnframes()),dtype=np.int16).astype(np.float32)/32768
hop=160; n=len(x)//hop
rms=np.sqrt(np.mean(x[:n*hop].reshape(n,hop)**2,axis=1)); db=20*np.log10(rms+1e-9)
thr=np.percentile(db,10)+12
sil=db<thr
# silence intervals >=80ms
iv=[]; i=0
while i<n:
    if sil[i]:
        j=i
        while j<n and sil[j]: j+=1
        if j-i>=8: iv.append((i/100,j/100))
        i=j
    else: i+=1
print('thr',thr,'silences',len(iv))
json.dump({'chunks':chunks,'sil':iv,'dur':len(x)/16000},open(W+'timing.json','w'),ensure_ascii=False)
# report slide boundaries
prev=None
for k,c in enumerate(chunks):
    if prev is not None and c['sec']!=chunks[prev]['sec']:
        e=chunks[prev]['e']; s=c['s']
        g=[v for v in iv if v[1]>e-0.3 and v[0]<s+0.3]
        print(f"slide {c['sec']+1}: prev end {e:.2f} next start {s:.2f} sil {[(round(a,2),round(b,2)) for a,b in g]}")
    prev=k
# big gaps anywhere
for a,b in iv:
    if b-a>1.2: print('long silence',a,b)
