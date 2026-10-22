import json,sys,math
sys.path.insert(0,sys.argv[1]); from chunks import SLIDES
W=sys.argv[2]; FPS=30
fw=json.load(open(f"{W}/fa_words.json")); segs=json.load(open(f"{W}/speechsegs.json"))
import numpy as np
dur=len(np.fromfile(f"{W}/v16.f32",dtype=np.float32))/16000
chunks=[]
for k in sorted(SLIDES):
    for pi,p in enumerate(SLIDES[k]):
        for c in p: chunks.append({"slide":k,"para":pi,"text":c})
for i,c in enumerate(chunks):
    ws=[w for w in fw if w["chunk"]==i]
    c["t0"]=ws[0]["t0"]; c["t1"]=ws[-1]["t1"]
# slide cut: 0.1s after the slide's last word, always before the next slide's first word
cuts=[0.0]
for k in range(2,8):
    prev=[c for c in chunks if c["slide"]==k-1][-1]; nxt=[c for c in chunks if c["slide"]==k][0]
    cut=round(min(prev["t1"]+0.1,(prev["t1"]+nxt["t0"])/2)*FPS)/FPS
    assert prev["t1"]<=cut<nxt["t0"]; cuts.append(cut)
cuts.append(round(dur*FPS)/FPS)
for i,c in enumerate(chunks):
    s=math.floor(c["t0"]*FPS)/FPS                       # appears on/just before the first syllable
    if i+1<len(chunks):
        nx=math.floor(chunks[i+1]["t0"]*FPS)/FPS
        e=nx if chunks[i+1]["t0"]-c["t1"]<0.8 else math.ceil((c["t1"]+0.3)*FPS)/FPS
    else: e=math.ceil(min(c["t1"]+0.6,dur)*FPS)/FPS
    c["s"]=max(s,cuts[c["slide"]-1]); c["e"]=min(e,cuts[c["slide"]])
json.dump({"cuts":cuts,"chunks":chunks,"dur":dur},open(f"{W}/timeline.json","w"),ensure_ascii=False,indent=1)
for k in range(1,7): print(f"cut {k}->{k+1} at {cuts[k]:.3f}")
