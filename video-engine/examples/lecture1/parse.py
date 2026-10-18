import re,sys,json
S=sys.argv[1]
def script():
    txt=open(S+"/dl/1강/이다사_VOD_1강_최종스크립트.txt",encoding="utf-8").read()
    slides={}
    cur=None
    for ln in txt.splitlines():
        m=re.match(r"## 슬라이드 (\d+)",ln)
        if m: cur=int(m.group(1)); slides[cur]=[]; continue
        if cur is None: continue
        s=ln.strip()
        if not s or s.startswith("[") or s.startswith("영상 끝나자마자"): continue
        slides[cur].append(s)
    return slides
def subs():
    out={}; cur=None
    for ln in open(S+"/work/subs.txt",encoding="utf-8"):
        ln=ln.rstrip("\n")
        if ln.startswith("#"): cur=int(ln[1:]); out[cur]=[]; continue
        if ln: out[cur].append(ln)
    return out
norm=lambda t: re.sub(r"\s+","",t)
if __name__=="__main__":
    sc,sb=script(),subs()
    ok=True
    for k in sc:
        a=norm(" ".join(sc[k])); b=norm(" ".join(x for x in sb[k] if not x.startswith("@")))
        # the trailing '/' in slide 14 is a script marker, not narration
        a=a.replace("때문이다/","때문이다")
        if a!=b:
            ok=False; i=next(i for i in range(min(len(a),len(b))) if a[i]!=b[i]) if any(a[i]!=b[i] for i in range(min(len(a),len(b)))) else min(len(a),len(b))
            print("MISMATCH slide",k,"\n S:",a[max(0,i-20):i+20],"\n B:",b[max(0,i-20):i+20])
        for x in sb[k]:
            if len(x)>25: print("LONG",k,len(x),x)
    # whitespace check: space positions should match the script too
    for k in sc:
        a=" ".join(sc[k]).replace("때문이다/","때문이다"); b=" ".join(x for x in sb[k] if not x.startswith("@"))
        if re.sub(r"\s+"," ",a)!=re.sub(r"\s+"," ",b): print("SPACE diff slide",k)
    print("TEXT OK" if ok else "TEXT FAIL", sum(len(v) for v in sb.values()),"chunks")
