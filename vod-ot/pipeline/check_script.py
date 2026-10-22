import re,sys
sys.path.insert(0,sys.argv[2]); from chunks import SLIDES
txt=open(sys.argv[1],encoding="utf-8").read().splitlines()
paras={};cur=None
for l in txt:
    l=l.strip()
    m=re.match(r"슬라이드 (\d+)",l)
    if m: cur=int(m.group(1)); paras[cur]=[]; continue
    if not l or cur is None or re.match(r"\[\d",l): continue
    paras[cur].append(l)
ok=True
for k in sorted(paras):
    mine=[" ".join(p) for p in SLIDES[k]]
    if mine!=paras[k]:
        ok=False; print("MISMATCH slide",k)
        for a,b in zip(mine,paras[k]):
            if a!=b: print(" mine:",a,"\n  src:",b)
        print(len(mine),len(paras[k]))
for k,ps in SLIDES.items():
    for p in ps:
        for c in p:
            if len(c)>25: ok=False; print("TOO LONG",len(c),c)
print("all paragraphs match script verbatim:",ok, "| chunks:",sum(len(p) for ps in SLIDES.values() for p in ps), "| max len:",max(len(c) for ps in SLIDES.values() for p in ps for c in p))
