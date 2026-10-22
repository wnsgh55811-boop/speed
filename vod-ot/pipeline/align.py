import json,sys,re,difflib
import numpy as np
sys.path.insert(0,sys.argv[1]); from chunks import SLIDES
W=sys.argv[2]
asr=json.load(open(f"{W}/asr.json"))
norm=lambda s: re.sub(r"[^0-9A-Za-z가-힣]","",s)
# char stream with times from ASR words
ac=[];at=[]
for sg in asr:
    for s,e,w in sg["words"]:
        n=norm(w)
        for i,ch in enumerate(n):
            ac.append(ch); at.append((s+(e-s)*i/len(n), s+(e-s)*(i+1)/len(n)))
# script char stream with chunk ids
sc=[];sid=[];chunks=[]
for k in sorted(SLIDES):
    for pi,p in enumerate(SLIDES[k]):
        for c in p:
            for ch in norm(c): sc.append(ch); sid.append(len(chunks))
            chunks.append({"slide":k,"para":pi,"text":c})
sm=difflib.SequenceMatcher(None,sc,ac,autojunk=False)
m={}
for a,b,n in sm.get_matching_blocks():
    for i in range(n): m[a+i]=b+i
print("matched chars %d/%d"%(len(m),len(sc)))
for ci,c in enumerate(chunks):
    idx=[i for i in range(len(sc)) if sid[i]==ci]
    mi=[i for i in idx if i in m]
    c["t0"]=at[m[mi[0]]][0]; c["t1"]=at[m[mi[-1]]][1]
    c["cov"]=len(mi)/len(idx)
segs=json.load(open(f"{W}/speechsegs.json"))
dur=len(np.fromfile(f"{W}/v16.f32",dtype=np.float32))/16000
on=np.array([x[0] for x in segs]); off=np.array([x[1] for x in segs])
# anchors: whisper chunk start near a real onset -> real onset ; chunk end near a real offset -> real offset
anc=[]
w0=np.array([c["t0"] for c in chunks]); w1=np.array([c["t1"] for c in chunks])
for x in on:   # each real onset snaps only its closest chunk start
    j=int(np.argmin(abs(w0-x)))
    if abs(w0[j]-x)<0.7 and "on" not in chunks[j]: chunks[j]["on"]=float(x); anc.append((w0[j],x)); chunks[j]["snap0"]=True
for x in off:
    j=int(np.argmin(abs(w1-x)))
    if abs(w1[j]-x)<0.7 and "off" not in chunks[j]: chunks[j]["off"]=float(x); anc.append((w1[j],x)); chunks[j]["snap1"]=True
anc=sorted(dict(anc).items()); ax=np.array([x for x,_ in anc]); ay=np.array([y for _,y in anc])
fix=lambda t: float(np.interp(t,ax,ay-ax)+t)
for c in chunks:
    c["w0"],c["w1"]=c["t0"],c["t1"]
    c["t0"]=fix(c["t0"]); c["t1"]=fix(c["t1"])
    if "on" in c: c["t0"]=c["on"]
    if "off" in c: c["t1"]=c["off"]
# each real speech segment must be covered: report segments with no chunk start inside
for a0,a1 in segs:
    if not any(a0-0.05<=c["t0"]<a1 for c in chunks): print("WARN segment without chunk start",a0,a1)
cuts=[0.0]
for k in range(2,8):
    prev=[c for c in chunks if c["slide"]==k-1][-1]; nxt=[c for c in chunks if c["slide"]==k][0]
    cut=min(prev["t1"]+0.1,(prev["t1"]+nxt["t0"])/2); cut=round(cut*30)/30
    assert prev["t1"]<=cut<nxt["t0"]
    cuts.append(cut); print(f"slide {k-1}->{k}: sentence ends {prev['t1']:.2f} | cut {cut:.3f} | next sentence starts {nxt['t0']:.2f}")
cuts.append(round(dur*30)/30)
for i,c in enumerate(chunks):
    c["s"]=c["t0"]
    if i+1<len(chunks):
        nx=chunks[i+1]["t0"]; c["e"]=nx if nx-c["t1"]<0.8 else c["t1"]+0.3
    else: c["e"]=min(c["t1"]+0.6,dur)
    c["e"]=min(c["e"],cuts[c["slide"]]); c["s"]=max(c["s"],cuts[c["slide"]-1])
    c["s"]=round(c["s"]*30)/30; c["e"]=round(c["e"]*30)/30
low=[c for c in chunks if c["cov"]<0.6]
print("low-coverage chunks:",[(c["text"],round(c["cov"],2)) for c in low])
json.dump({"cuts":cuts,"chunks":chunks,"dur":dur},open(f"{W}/timeline.json","w"),ensure_ascii=False,indent=1)
