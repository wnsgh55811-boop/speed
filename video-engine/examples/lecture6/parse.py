import re, json, sys
src=sys.argv[1]
lines=open(src,encoding='utf-8').read().split('\n')
secs=[]; cur=None
for ln in lines:
    if ln.startswith('## '):
        cur={'title':ln[3:].strip(),'paras':[]}; secs.append(cur); continue
    if cur is None: continue
    t=ln.strip()
    if not t or t=='---': continue
    if re.fullmatch(r'\[[^\]]*\]',t): cur['paras'].append({'marker':t}); continue
    cur['paras'].append({'text':t})
json.dump(secs,open(sys.argv[2],'w'),ensure_ascii=False,indent=1)
print(len(secs))
for i,s in enumerate(secs,1):
    print(i,s['title'],[p.get('marker') for p in s['paras'] if 'marker' in p])
