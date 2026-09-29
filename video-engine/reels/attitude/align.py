import json, re, difflib
toks=json.load(open("tokens.json"))
# keep middle-of-overlap tokens
chars=[]  # (char, time)
keep=[]
for ts,tok,w0 in toks:
    lo = w0+1 if w0>0 else 0; hi = w0+11
    if lo<=ts<hi: keep.append((ts,tok))
keep.sort()
for i,(ts,tok) in enumerate(keep):
    tok=re.sub(r'[^가-힣a-zA-Z0-9]','',tok.replace('▁',''))
    nxt = keep[i+1][0] if i+1<len(keep) else ts+0.2
    dur=min(nxt-ts,0.25)
    for j,c in enumerate(tok): chars.append((c, ts+dur*j/max(1,len(tok))))
asr=''.join(c for c,_ in chars)
lines=open("script.txt").read().split('\n')
blocks=[];cur=[]
for l in lines:
    if l.strip(): cur.append(l.strip())
    else:
        if cur: blocks.append(cur); cur=[]
if cur: blocks.append(cur)
flat=[]; spans=[]
for bi,b in enumerate(blocks):
    for li,l in enumerate(b):
        c=re.sub(r'[^가-힣a-zA-Z0-9]','',l)
        spans.append((bi,li,l,len(flat),len(flat)+len(c)))
        flat.extend(c)
sc=''.join(flat)
sm=difflib.SequenceMatcher(None, sc, asr, autojunk=False)
m=[None]*len(sc)
for a,b,n in sm.get_matching_blocks():
    for k in range(n): m[a+k]=chars[b+k][1]
# interpolate
known=[i for i,v in enumerate(m) if v is not None]
import bisect
for i in range(len(m)):
    if m[i] is None:
        p=bisect.bisect_left(known,i)
        L=known[p-1] if p>0 else None; R=known[p] if p<len(known) else None
        if L is None: m[i]=m[R]
        elif R is None: m[i]=m[L]+0.12*(i-L)
        else: m[i]=m[L]+(m[R]-m[L])*(i-L)/(R-L)
out=[]
for bi,li,l,s,e in spans:
    out.append(dict(b=bi,l=li,text=l,start=round(m[s],2),last=round(m[e-1],2)))
for i,o in enumerate(out):
    o['end']=round(min(out[i+1]['start'] if i+1<len(out) else 67.9, o['last']+0.35),2)
json.dump(out,open("lines.json","w"),ensure_ascii=False,indent=0)
for o in out: print(f"{o['b']:2d} {o['start']:6.2f} {o['end']:6.2f}  {o['text']}")
print(sm.ratio())
