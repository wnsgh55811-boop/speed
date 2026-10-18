import re
def load_chunks(p):
    slides=[]; 
    for line in open(p,encoding='utf-8'):
        line=line.rstrip('\n')
        if not line.strip(): continue
        if line.startswith('## '): slides.append([]); continue
        if line.startswith('@'): slides[-1].append(line.split()); continue
        slides[-1].append([c.strip() for c in line.split(' / ')])
    return slides
def load_script(p):
    secs=[]; 
    for line in open(p,encoding='utf-8'):
        l=line.strip()
        if l.startswith('## '): secs.append([]); continue
        if not secs or not l or l=='---' or l.startswith('# '): continue
        if l.startswith('['): continue
        if l=='영상 재생 후 아래 대본 음성 재생': continue
        if l.startswith('---'): continue
        secs[-1].append(l)
    return [' '.join(s) for s in secs]
