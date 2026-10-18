"""Build the output timeline (slides, narration pieces, clips, subtitles) from aligned.json."""
import json,sys
S=sys.argv[1]; W=S+"/work"
D=json.load(open(W+"/aligned.json")); ch=D["chunks"]; AUD=D["audlen"]
CLIPDUR={"H":11.566667,"L":10.466667}
FPS=30
q=lambda t: round(t*FPS)/FPS
TAIL,LEAD=0.30,0.12   # breath kept around a narration cut at slide 11

# narration pieces: split fish audio only at the two video cues on slide 11
pieces=[]; cur0=0.0; plan=[]
for i,c in enumerate(ch):
    if c["text"].startswith("@"):
        prev=ch[i-1]; nxt=ch[i+1]
        mid=(prev["e"]+nxt["s"])/2; cut_a=min(prev["e"]+TAIL,mid); cut_b=max(nxt["s"]-LEAD,mid)
        pieces.append(("fish",cur0,cut_a)); pieces.append(("clip",c["text"][-1]))
        cur0=cut_b
pieces.append(("fish",cur0,AUD))
# map: fish time -> output time
segs=[]; t=0.0
for p in pieces:
    if p[0]=="fish":
        d=q(p[2]-p[1]); segs.append({"kind":"fish","src0":p[1],"src1":p[1]+d,"out0":t,"out1":t+d}); t+=d
    else:
        d=q(CLIPDUR[p[1]]); segs.append({"kind":"clip","clip":p[1],"out0":t,"out1":t+d}); t+=d
TOTAL=t
def out(ft):
    for s in segs:
        if s["kind"]=="fish" and s["src0"]-1e-6<=ft<=s["src1"]+1e-6: return s["out0"]+ft-s["src0"]
    raise ValueError(ft)
sp=[c for c in ch if "s" in c]
# slide boundaries: middle of the pause between last chunk of slide k and first of k+1
slides={}
for p,n in zip(sp,sp[1:]):
    if p["slide"]!=n["slide"]:
        slides[n["slide"]]=q(out((p["e"]+n["s"])/2))
slides[1]=0.0
ks=sorted(slides); bounds=[(k,slides[k],slides[ks[i+1]] if i+1<len(ks) else TOTAL) for i,k in enumerate(ks)]
# subtitles
subs=[]
for i,c in enumerate(sp):
    s=out(c["s"])-0.05; e=out(c["e"])+0.20
    if i+1<len(sp):
        ns=out(sp[i+1]["s"])-0.05
        same_piece=any(g["kind"]=="fish" and g["src0"]<=c["e"] and sp[i+1]["s"]<=g["src1"] for g in segs)
        if ns-e<0.6 and same_piece: e=ns
        e=min(e,ns)
    sl=[b for b in bounds if b[0]==c["slide"]][0]
    s=max(s,sl[1])
    piece=[g for g in segs if g["kind"]=="fish" and g["src0"]-1e-6<=c["s"]<=g["src1"]][0]
    e=min(e,sl[2],piece["out1"])
    subs.append({"slide":c["slide"],"s":q(s),"e":q(e),"text":c["text"]})
CS=json.load(open(W+"/clipsubs.json"))
for g in segs:
    if g["kind"]=="clip":
        for a,b,t in CS[g["clip"]]:
            subs.append({"slide":11,"s":q(g["out0"]+a),"e":q(min(g["out0"]+b,g["out1"])),"text":t,"clip":g["clip"]})
subs.sort(key=lambda z:z["s"])
json.dump({"total":TOTAL,"segs":segs,"slides":bounds,"subs":subs},open(W+"/timeline.json","w"),ensure_ascii=False,indent=1)
print("TOTAL %.2f"%TOTAL)
for s in segs: print(s)
for k,a,b in bounds: print("slide %2d  %7.2f - %7.2f  (%5.2fs)"%(k,a,b,b-a))
