import re,json,sys
txt=open(sys.argv[1],encoding='utf-8').read()
slides=[];cur=None
for line in txt.splitlines():
    l=line.strip()
    if l.startswith('## '):
        cur={'title':l[3:],'paras':[]};slides.append(cur);continue
    if not l or l.startswith('#') or l.startswith('--') : continue
    if re.fullmatch(r'\[.*\]',l): cur['paras'].append({'direction':l});continue
    cur['paras'].append({'text':l})
json.dump(slides,open('slides.json','w'),ensure_ascii=False,indent=1)
for i,s in enumerate(slides,1): print(i,s['title'],len(s['paras']))
