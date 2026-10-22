import json, re, sys, os, subprocess
from PIL import Image, ImageDraw, ImageFont
W=sys.argv[1]; SL=sys.argv[2]; OUT=sys.argv[3]
FPS=30; PAUSE=2.0
ch=json.load(open(W+'/aligned.json'))
sp=[c for c in ch if 's' in c]
# pause insertion point
pi=[i for i,c in enumerate(ch) if c['raw']=='[PAUSE]'][0]
before=ch[pi-1]; after=ch[pi+1]
P=(before['e']+after['s'])/2
sh=lambda t: t+PAUSE if t>P else t
for c in sp: c['S']=sh(c['s']); c['E']=sh(c['e'])
fr=lambda t: int(round(t*FPS))
AUDIO_ORIG=742.09
total=fr(AUDIO_ORIG+PAUSE)
# slide starts
starts={1:0}
for k in range(1,24):
    a=[c for c in sp if c['slide']==k][-1]; b=[c for c in sp if c['slide']==k+1][0]
    starts[k+1]=fr(a['E']+min(0.1,(b['S']-a['E'])/2))
# subtitles
def disp(t):
    t=t.lstrip('+'); t=re.sub(r'\.(["”\'])$',r'\1',t); t=re.sub(r'[.,]$','',t); return t
subs=[]
for i,c in enumerate(sp):
    nxt=sp[i+1] if i+1<len(sp) else None
    if nxt is not None and (nxt['S']-c['E']<1.0 or c is before):
        end=nxt['S']
    else:
        end=c['E']+0.3
    subs.append({'f0':fr(c['S']),'f1':min(fr(end),total),'text':disp(c['raw']),'slide':c['slide']})
# timeline table
tl=[]
for k in range(1,25):
    f0=starts[k]; f1=starts[k+1] if k<24 else total
    tl.append({'slide':k,'start':f0/FPS,'end':f1/FPS,'fishaudio':True,'video':False,'video_audio':False,
               'n_subs':sum(1 for s in subs if s['slide']==k)})
json.dump({'pause_at_orig':P,'slides':tl,'subs':[dict(s,start=s['f0']/FPS,end=s['f1']/FPS) for s in subs]},open(W+'/timeline.json','w'),ensure_ascii=False,indent=1)
# events -> states
font=ImageFont.truetype('/root/.fonts/NotoSansKR-500.ttf',54)
# vertical centering reference: Hangul body
ref=font.getbbox('가나다한글',anchor='ls')  # (l,t,r,b) relative to baseline
BOX_T,BOX_H=971,78
base=BOX_T+(BOX_H-(ref[3]-ref[1]))/2-ref[1]
cuts=sorted(set([0,total]+[starts[k] for k in starts]+[s['f0'] for s in subs]+[s['f1'] for s in subs]))
slides={k:Image.open(f'{SL}/s-{k:02d}.png').convert('RGB') for k in range(1,25)}
os.makedirs(W+'/frames',exist_ok=True)
lines=[]; cache={}
for a,b in zip(cuts,cuts[1:]):
    if b<=a: continue
    k=max(kk for kk in starts if starts[kk]<=a)
    cur=[s for s in subs if s['f0']<=a<s['f1']]
    assert len(cur)<=1,(a,cur)
    txt=cur[0]['text'] if cur else ''
    key=(k,txt)
    if key not in cache:
        im=slides[k].copy().convert('RGBA')
        if txt:
            w=font.getlength(txt); bw=int(round(w+24)); x0=(1920-bw)//2
            ov=Image.new('RGBA',im.size,(0,0,0,0)); d=ImageDraw.Draw(ov)
            d.rectangle([x0,BOX_T,x0+bw-1,BOX_T+BOX_H-1],fill=(0,0,0,153))
            im=Image.alpha_composite(im,ov); d=ImageDraw.Draw(im)
            d.text((x0+12,base),txt,font=font,fill=(255,255,255,255),anchor='ls')
        p=f'{W}/frames/f{len(cache):04d}.png'; im.convert('RGB').save(p); cache[key]=p
    lines.append(f"file '{cache[key]}'\nduration {(b-a)/FPS:.6f}")
lines.append(f"file '{cache[key]}'")
open(W+'/concat.txt','w').write('\n'.join(lines)+'\n')
print('states',len(lines)-1,'unique frames',len(cache),'total',total/FPS,'pause_at',P)
