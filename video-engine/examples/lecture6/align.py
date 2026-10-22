import json, re, difflib, wave, numpy as np
W='work/'
secs=json.load(open(W+'chunks.json')); asr=json.load(open(W+'asr.json'))
keep=lambda c: bool(re.match(r'[가-힣0-9A-Za-z]',c))
# script chars
sc=[]; owner=[]
chunks=[]
for si,s in enumerate(secs):
    for pi,p in enumerate(s['paras']):
        for ci,c in enumerate(p.get('chunks',[])):
            k=len(chunks); chunks.append({'sec':si,'para':pi,'text':c})
            for ch in c:
                if keep(ch): sc.append(ch); owner.append(k)
# asr chars
ac=[]; at=[]
for seg in asr:
    for w in seg['words']:
        cs=[ch for ch in w['w'] if keep(ch)]
        n=len(cs)
        for i,ch in enumerate(cs):
            ac.append(ch); at.append((w['s']+(w['e']-w['s'])*i/max(n,1), w['s']+(w['e']-w['s'])*(i+1)/max(n,1)))
A=''.join(sc); B=''.join(ac)
print(len(A),len(B))
sm=difflib.SequenceMatcher(None,A,B,autojunk=False)
ops=sm.get_opcodes()
m={}
for tag,i1,i2,j1,j2 in ops:
    if tag=='equal':
        for k in range(i2-i1): m[i1+k]=j1+k
    elif tag!='equal' and tag!='insert':
        pass
    if tag in('replace','insert','delete') and max(i2-i1,j2-j1)>=1:
        print(f'{tag:7s} S[{A[i1:i2]}]  A[{B[j1:j2]}] t={at[j1][0] if j1<len(at) else -1:.1f}')
json.dump({'m':m,'owner':owner,'at':at,'chunks':chunks},open(W+'align.json','w'),ensure_ascii=False)
