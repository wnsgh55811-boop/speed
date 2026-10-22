import re, json, sys
MAX=25
END=re.compile(r'[.?!…]["”’\']*$|[.?!][)」]*$')
def score_split(left, right):
    # left ends with token before space, right starts with next token
    lw=left.split(' ')[-1]; rw=right.split(' ')[0]
    if re.search(r'[.?!…][\"”’\']?$', lw) and not re.search(r'[“"‘\']$', lw): s=100
    elif lw.endswith(',') or lw.endswith(',”') or lw.endswith(",'") : s=80
    elif re.search(r'[”"\'’]$', lw): s=70
    elif re.search(r'(고|서|면|데|지만|니까|는데|도|며|게|듯|처럼|으로|에서|때|때는|면서|어서|아서|해서|하고|라고|다고|이라|라는|하는데|하더라도|보다|에게|한테|까지|부터|라서)$', lw): s=50
    elif re.search(r'(을|를|이|가|은|는|에|와|과|의|로)$', lw): s=35
    else: s=20
    # modifier-noun penalty: adnominal endings
    if re.search(r'(한|는|던|할|될|된|운|른|은|런|떤|의|ㄴ|갈|일|운|쁜|은|든|늘|난|던|른)$', lw) and not re.search(r'[,.?!]$', lw) and s<70:
        s-=25
    if re.search(r'^["“‘\']', rw): s+=15
    return s
def split(text):
    text=text.strip()
    if len(text)<=MAX: return [text]
    sp=[i for i,c in enumerate(text) if c==' ']
    best=None
    for i in sp:
        L,R=text[:i],text[i+1:]
        if len(L)<3 or len(R)<3: continue
        s=score_split(L,R)
        # balance: prefer each side fitting; mild preference for balanced unless strong boundary
        over=max(0,len(L)-MAX)
        bal=-abs(len(L)-len(R))*0.6 if s<100 else -abs(len(L)-len(R))*0.25
        sc=s+bal-over*4
        if len(L)<=MAX: sc+=10
        if min(len(L),len(R))<7: sc-=25
        if best is None or sc>best[0]: best=(sc,i)
    if best is None: return [text]
    i=best[1]
    return split(text[:i])+split(text[i+1:])
def chunks_for_para(t):
    # first sentence split
    parts=re.split(r'(?<=[.?!…])(?:["”’\'])?\s+(?=\S)', t)
    # re.split lost quote char; do manual
    out=[]; buf=''
    i=0; sents=[]; start=0
    for m in re.finditer(r'[.?!…]+["”’\']?(\s+)', t):
        end=m.start(1)
        seg=t[start:end]
        # don't split if inside an open quote (unbalanced)
        sents.append(seg); start=m.end(1)
    sents.append(t[start:])
    # merge pieces that are inside quotes when merged fits
    merged=[]
    for s in sents:
        if merged:
            prev=merged[-1]
            opens=prev.count('“')+prev.count('"')%2 - prev.count('”')
            q1=prev.count("'")%2==1 or prev.count('‘')>prev.count('’')
            q2=prev.count('"')%2==1 or prev.count('“')>prev.count('”')
            if (q1 or q2) and len(prev)+1+len(s)<=MAX:
                merged[-1]=prev+' '+s; continue
        merged.append(s)
    res=[]
    for s in merged:
        res+=split(s)
    return res
if __name__=='__main__':
    secs=json.load(open(sys.argv[1]))
    for si,s in enumerate(secs,1):
        for p in s['paras']:
            if 'text' in p:
                p['chunks']=chunks_for_para(p['text'])
    json.dump(secs,open(sys.argv[2],'w'),ensure_ascii=False,indent=1)
    for si,s in enumerate(secs,1):
        print(f'== {si}')
        for p in s['paras']:
            for c in p.get('chunks',[p.get('marker')]):
                print(f'{len(c):2d} {c}')
