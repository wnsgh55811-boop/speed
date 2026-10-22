import json, os, subprocess
from PIL import Image, ImageDraw, ImageFont
S='./'
W=S+'work/'; B=S+'build/'
FPS=30; PAUSE=2.0
t=json.load(open(W+'timing.json')); ch=t['chunks']; sil=t['sil']; DUR=t['dur']
secs=json.load(open(W+'chunks.json'))
def sil_between(e,s):
    g=[v for v in sil if v[1]>e-0.3 and v[0]<s+0.3]
    assert g,(e,s)
    a,b=max(g,key=lambda v:v[1]-v[0]); return a,b
# insertion points (markers)
inserts=[]
for k in range(len(ch)-1):
    c,n=ch[k],ch[k+1]
    if c['sec']==n['sec'] and n['para']-c['para']==2 and 'marker' in secs[c['sec']]['paras'][c['para']+1]:
        a,b=sil_between(c['e'],n['s']); inserts.append({'at':(a+b)/2,'marker':secs[c['sec']]['paras'][c['para']+1]['marker'],'after':k})
print('inserts',inserts)
def shift(x):
    return x+sum(PAUSE for i in inserts if x>i['at'])
fr=lambda x: int(round(x*FPS))
# slide cuts
cuts=[0.0]
for k in range(1,len(ch)):
    if ch[k]['sec']!=ch[k-1]['sec']:
        a,b=sil_between(ch[k-1]['e'],ch[k]['s']); cuts.append((a+b)/2)
assert len(cuts)==41
TOTAL=shift(DUR)
# subtitle starts
starts=[]
for k,c in enumerate(ch):
    s=c['s']
    if k==0 or ch[k-1]['sec']!=c['sec']:
        s=cuts[c['sec']]
    else:
        near=[v for v in sil if abs(v[1]-s)<=0.25]
        if near: s=min(near,key=lambda v:abs(v[1]-s))[1]-0.05
    starts.append(s)
ev=[]
for k,c in enumerate(ch):
    s=shift(starts[k]) if not (k==0 or ch[k-1]['sec']!=c['sec']) else shift(cuts[c['sec']]) if c['sec']>0 else 0.0
    if k==len(ch)-1: e=TOTAL
    elif ch[k+1]['sec']!=c['sec']: e=shift(cuts[c['sec']+1])
    elif any(i['after']==k for i in inserts): e=shift(c['e']+0.25)
    else: e=shift(starts[k+1])
    ev.append({'f0':fr(s),'f1':fr(e),'text':c['text'],'sec':c['sec']})
slides=[{'n':i+1,'f0':fr(shift(cuts[i])) if i else 0,'f1':fr(shift(cuts[i+1])) if i<40 else fr(TOTAL)} for i in range(41)]
for i in range(1,len(ev)): assert ev[i]['f0']>=ev[i-1]['f1'] and ev[i]['f1']>ev[i]['f0'], (ev[i-1],ev[i])
json.dump({'events':ev,'slides':slides,'inserts':[dict(i,at_new=shift(i['at'])) for i in inserts],'total':TOTAL,'cuts':cuts},open(W+'timeline.json','w'),ensure_ascii=False,indent=1)
# ---- subtitle rendering
font=ImageFont.truetype('/root/.fonts/NotoSansKR-VF.ttf',54); font.set_variation_by_axes([500])  # Noto Sans KR Medium
def compose(slide,text):
    im=Image.open(S+f'render/s-{slide:02d}.png').convert('RGBA')
    if text:
        w=font.getlength(text)
        bw=int(round(w))+24; x0=(1920-bw)//2
        ov=Image.new('RGBA',im.size,(0,0,0,0)); d=ImageDraw.Draw(ov)
        d.rectangle([x0,971,x0+bw-1,1048],fill=(0,0,0,153))
        im=Image.alpha_composite(im,ov); d=ImageDraw.Draw(im)
        d.text((x0+12, 1030),text,font=font,fill=(255,255,255,255),anchor='ls')
    return im.convert('RGB')
# segments
bounds=set([0,fr(TOTAL)])
for s in slides: bounds|={s['f0'],s['f1']}
for e in ev: bounds|={e['f0'],e['f1']}
bounds=sorted(bounds)
lines=[]; cache={}
for a,b in zip(bounds,bounds[1:]):
    sl=[s for s in slides if s['f0']<=a<s['f1']][0]['n']
    tx=[e['text'] for e in ev if e['f0']<=a<e['f1']]; tx=tx[0] if tx else ''
    key=(sl,tx)
    if key not in cache:
        p=B+f'frames/{len(cache):04d}.png'; compose(sl,tx).save(p,compress_level=1); cache[key]=p
    lines.append((cache[key],(b-a)/FPS,a,b,sl,tx))
with open(B+'list.txt','w') as f:
    for p,d,*_ in lines: f.write(f"file '{p}'\nduration {d:.6f}\n")
    f.write(f"file '{lines[-1][0]}'\n")
json.dump(lines,open(W+'segments.json','w'),ensure_ascii=False)
print('segments',len(lines),'images',len(cache),'total',TOTAL, 'frames',fr(TOTAL))
