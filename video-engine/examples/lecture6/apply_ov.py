import json, re, sys
sys.path.insert(0, sys.argv[4]); from chunk import chunks_for_para
secs=json.load(open(sys.argv[1])); ovs=[l.rstrip('\n') for l in open(sys.argv[2],encoding='utf-8') if l.strip()]
used=set()
for s in secs:
    for p in s['paras']:
        if 'text' not in p: continue
        t=re.sub(r' {2,}',' ',p['text'])
        p['sub']=t
        auto=chunks_for_para(t)
        # boundaries from auto
        b=set(); pos=0
        for c in auto:
            i=t.index(c,pos); b.add(i); pos=i+len(c)
        b.add(len(t))
        for k,o in enumerate(ovs):
            parts=o.split(' | '); j=' '.join(parts)
            i=t.find(j)
            if i<0: continue
            used.add(k)
            b={x for x in b if not (i<x<i+len(j)) and not (i+len(j)<x<i+len(j)+1)}
            b.add(i); b.add(i+len(j)+ (1 if i+len(j)<len(t) else 0))
            q=i
            for pt in parts[:-1]:
                q+=len(pt)+1; b.add(q)
        bs=sorted(b|{0}); ch=[t[a:c].strip() for a,c in zip(bs,bs[1:]) if t[a:c].strip()]
        assert ' '.join(ch)==t, (ch,t)
        p['chunks']=ch
for k,o in enumerate(ovs):
    if k not in used: print('UNUSED',o)
json.dump(secs,open(sys.argv[3],'w'),ensure_ascii=False,indent=1)
n=0
for si,s in enumerate(secs,1):
    for p in s['paras']:
        for c in p.get('chunks',[]):
            n+=1
            if len(c)>25: print('LONG',si,c)
print('chunks',n)
