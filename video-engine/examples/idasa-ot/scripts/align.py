import json,re,sys,difflib
S=sys.argv[1]
txt=open(f'{S}/w/script.txt',encoding='utf-8').read()
secs=re.split(r'=+\n\[(\d+)\][^\n]*\n=+\n',txt)
sections=[]
for k in range(1,len(secs),2):
    n=int(secs[k]); body=secs[k+1]
    lines=body.split('대본:',1)[1].strip().split('\n')
    sents=[]
    for ln in lines:
        ln=ln.strip()
        if not ln: continue
        # split into sentences keeping punctuation
        parts=re.findall(r'[^.?!]+[.?!]?["”]?\s*',ln)
        buf=''
        for p in parts:
            p=p.strip()
            if not p: continue
            # merge quote fragments
            if buf and (buf.count('"')%2==1):
                buf+=' '+p; continue
            if buf: sents.append(buf)
            buf=p
        if buf: sents.append(buf)
    sections.append((n,sents))
asr=json.load(open(f'{S}/w/asr.json'))
# asr char stream
ac=[];at=[]
for s in asr:
    for w0,w1,w in s['words']:
        cs=[c for c in w if re.match(r'[가-힣A-Za-z0-9]',c)]
        for j,c in enumerate(cs):
            ac.append(c); at.append((w0+(w1-w0)*j/len(cs), w0+(w1-w0)*(j+1)/len(cs)))
# script char stream
sc=[];own=[]
allsent=[]
for n,ss in sections:
    for s in ss:
        idx=len(allsent); allsent.append({'sec':n,'text':s})
        for ci,c in enumerate(s):
            if re.match(r'[가-힣A-Za-z0-9]',c): sc.append(c); own.append((idx,ci))
sm=difflib.SequenceMatcher(None,sc,ac,autojunk=False)
tm=[None]*len(sc)
for a,b,size in sm.get_matching_blocks():
    for j in range(size): tm[a+j]=at[b+j]
# interpolate
known=[i for i,v in enumerate(tm) if v]
import bisect
for i in range(len(tm)):
    if tm[i] is None:
        k=bisect.bisect(known,i)
        L=known[k-1] if k>0 else None; Rr=known[k] if k<len(known) else None
        if L is None: tm[i]=tm[Rr]
        elif Rr is None: tm[i]=tm[L]
        else:
            f=(i-L)/(Rr-L); t=tm[L][1]+(tm[Rr][0]-tm[L][1])*f; tm[i]=(t,t)
print('matched',len(known),'/',len(sc))
chars={}
for i,(si,ci) in enumerate(own): chars.setdefault(si,[]).append((ci,tm[i][0],tm[i][1]))
for si,s in enumerate(allsent):
    cs=chars[si]; s['start']=cs[0][1]; s['end']=cs[-1][2]; s['chars']=cs
json.dump(allsent,open(f'{S}/w/sents.json','w'),ensure_ascii=False)
for s in allsent: print(f"[{s['sec']:2d}] {s['start']:7.2f}-{s['end']:7.2f} {s['text']}")
