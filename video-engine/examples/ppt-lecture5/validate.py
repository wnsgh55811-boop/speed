import json,re,sys
sents=json.load(open(sys.argv[1]))
chunks={}; cur=None
for l in open(sys.argv[2],encoding='utf-8'):
    l=l.rstrip('\n')
    if l.startswith('# '): cur=int(l[2:]); chunks[cur]=[]; continue
    if l: chunks[cur].append(l)
norm=lambda s: re.sub(r'\s+','',s)
extra={'+먼저 앱만 쓰는 사람입니다.':'앱만 쓰는 사람입니다.','+이번에는 매주 러닝크루에 나가는 사람입니다.':'매주 러닝크루에 나가는 사람입니다.'}
ok=True
def disp(c): return re.sub(r'[.,]$','',c)
for s in sents:
    a=norm(''.join(x for x in s['sents']))
    b=norm(''.join(extra.get(c,c.lstrip('!')) for c in chunks[s['slide']]))
    if a!=b:
        ok=False; print('MISMATCH slide',s['slide'])
        for i,(x,y) in enumerate(zip(a,b)):
            if x!=y: print(a[i-10:i+20]); print(b[i-10:i+20]); break
    for c in chunks[s['slide']]:
        if c.startswith('!') or c=='[PAUSE]': continue
        d=disp(c.lstrip('+'))
        if len(d)>25: ok=False; print('TOO LONG',len(d),d)
print('OK' if ok else 'FAIL', sum(len(v) for v in chunks.values()))
