import re, json, sys
txt=open(sys.argv[1],encoding='utf-8').read()
secs=[]
for block in re.split(r'\n## ', txt)[1:]:
    lines=block.split('\n')
    title=lines[0]
    body=[l.strip() for l in lines[1:]]
    paras=[]
    for l in body:
        if not l or l=='---' or l.startswith('#'): continue
        if l in ('[2초 쉼]','[BEFORE]','[AFTER]'):
            paras.append(l); continue
        paras.append(l)
    secs.append({"title":title,"paras":paras})
# merge quote lines in sec 22
out=[]
for i,s in enumerate(secs,1):
    sents=[]
    buf=None
    for p in s['paras']:
        if p in ('[BEFORE]','[AFTER]'): continue
        if p=='[2초 쉼]': sents.append('[PAUSE]'); continue
        if p.startswith('“') and not p.endswith('”'): buf=p; continue
        if buf is not None:
            sents.append(buf+'\n'+p); buf=None; continue
        # sentence split: end punct followed by space, not inside quotes
        parts=[]; cur=''; q=0
        for k,ch in enumerate(p):
            cur+=ch
            if ch in '"“': q^=1 if ch=='"' else 0
            if ch=='“': q=1
            if ch=='”': q=0
            nxt=p[k+1] if k+1<len(p) else ' '
            if ch in '.?!' and nxt==' ' and q==0:
                parts.append(cur.strip()); cur=''
        if cur.strip(): parts.append(cur.strip())
        sents+=parts
    out.append({"slide":i,"title":s['title'],"sents":sents})
json.dump(out,open(sys.argv[2],'w'),ensure_ascii=False,indent=1)
for o in out:
    print('##',o['slide'],o['title'])
    for x in o['sents']: print('   ',x.replace('\n','/'))
