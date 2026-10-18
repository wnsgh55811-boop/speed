"""Align subtitle chunks (subs.txt) to the FishAudio narration via Whisper word times,
refine boundaries on real pauses, and build the full lecture timeline."""
import json,re,sys,wave,difflib
import numpy as np
sys.path.insert(0,sys.argv[1]+"/work")
from parse import subs
S=sys.argv[1]; W=S+"/work"
WAV=S+"/dl/1강/1강 음성.wav"
CLIP={"H":(S+"/dl/1강/1강 하이에나의 태도.mp4",11.566667),"L":(S+"/dl/1강/1강 사자의 태도.mp4",10.466667)}
FPS=30
keep=lambda t: re.sub(r"[^0-9A-Za-z가-힣]","",t).lower()

# ---- ASR chars with times
asr=json.load(open(W+"/asr.json"))
ac=[]
for s in asr:
    for st,en,w,p in s["w"]:
        k=keep(w)
        for j,c in enumerate(k):
            ac.append((c,st+(en-st)*j/len(k),st+(en-st)*(j+1)/len(k)))
# ---- script chars per chunk
sb=subs(); chunks=[]
for sl in sorted(sb):
    for x in sb[sl]:
        chunks.append({"slide":sl,"text":x})
sc=[];own=[]
for ci,c in enumerate(chunks):
    if c["text"].startswith("@"): continue
    for ch in keep(c["text"]): sc.append(ch); own.append(ci)
sm=difflib.SequenceMatcher(None,"".join(sc),"".join(a[0] for a in ac),autojunk=False)
anc={}
for a,b,n in sm.get_matching_blocks():
    for k in range(n): anc[a+k]=(ac[b+k][1],ac[b+k][2])
print("matched %d/%d script chars"%(len(anc),len(sc)))
ai=sorted(anc)
def tstart(i):
    if i in anc: return anc[i][0]
    lo=max([k for k in ai if k<i],default=None); hi=min([k for k in ai if k>i],default=None)
    if lo is None: return anc[hi][0]
    if hi is None: return anc[lo][1]
    return anc[lo][1]+(anc[hi][0]-anc[lo][1])*(i-lo)/(hi-lo)
def tend(i):
    if i in anc: return anc[i][1]
    return tstart(i)
pos=0
for ci,c in enumerate(chunks):
    if c["text"].startswith("@"): continue
    n=len(keep(c["text"])); c["a0"]=tstart(pos); c["a1"]=tend(pos+n-1)
    c["matched"]=sum(1 for k in range(pos,pos+n) if k in anc)/n; pos+=n

# ---- energy envelope (10 ms)
w=wave.open(WAV); sr=w.getframerate(); x=np.frombuffer(w.readframes(w.getnframes()),np.int16).astype(np.float32)/32768
AUDLEN=len(x)/sr
hop=sr//100; nf=len(x)//hop
db=20*np.log10(np.sqrt((x[:nf*hop].reshape(nf,hop)**2).mean(1))+1e-9)
THR=-45.0
quiet=db<THR
def runs(t0,t1,minlen=0.06):
    a=max(0,int(t0*100)); b=min(nf,int(t1*100)); out=[]; i=a
    while i<b:
        if quiet[i]:
            j=i
            while j<b and quiet[j]: j+=1
            if (j-i)/100>=minlen: out.append((i/100,j/100))
            i=j
        else: i+=1
    return out
def onset(t): # first loud frame at/after t
    i=int(t*100)
    while i<nf and quiet[i]: i+=1
    return i/100
def offset(t): # last loud frame end at/before t
    i=int(t*100)-1
    while i>0 and quiet[i]: i-=1
    return (i+1)/100

speech=[c for c in chunks if "a0" in c]
speech[0]["s"]=onset(0)
for p,q in zip(speech,speech[1:]):
    lo=min(p["a1"],q["a0"])-0.35; hi=max(p["a1"],q["a0"])+0.35
    r=runs(lo,hi)
    if r:
        g=max(r,key=lambda z:z[1]-z[0]); p["e"]=g[0]; q["s"]=g[1]; p["gap"]=g[1]-g[0]
    else:
        m=(p["a1"]+q["a0"])/2; p["e"]=m; q["s"]=m; p["gap"]=0
speech[-1]["e"]=offset(AUDLEN)
json.dump({"chunks":chunks,"audlen":AUDLEN},open(W+"/aligned.json","w"),ensure_ascii=False,indent=0)
for c in chunks:
    if "s" in c: print("%2d %7.2f %7.2f gap=%.2f m=%.2f  %s"%(c["slide"],c["s"],c["e"],c.get("gap",0),c["matched"],c["text"]))
    else: print(c["slide"],c["text"])
