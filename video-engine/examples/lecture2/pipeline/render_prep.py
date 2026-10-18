import json,os
from PIL import Image,ImageDraw,ImageFont
FPS=30
ch=json.load(open('chunks.json'))
# --- 2-second pause from the script's "[2초 후]" direction ---
pi=[i for i,c in enumerate(ch) if c['pause2']][0]
gap=ch[pi]['s3']-ch[pi-1]['e3']
P=(ch[pi]['s3']+ch[pi-1]['e3'])/2; D=round((2.0-gap)*FPS)/FPS
mp=lambda t: t+D if t>=P else t
for c in ch: c['S']=mp(c['s3']); c['E']=mp(c['e3'])
AUDIO_LEN=683.2299+D
# --- slide transitions: right after the slide's last sentence ends ---
nslides=26
start={1:0.0}
for i in range(1,len(ch)):
    if ch[i]['slide']!=ch[i-1]['slide']:
        e=ch[i-1]['E']; s=ch[i]['S']
        start[ch[i]['slide']]=e+min(0.12,(s-e)/2)
END=ch[-1]['E']+0.5
END=max(END,AUDIO_LEN)
fr=lambda t:int(round(t*FPS))
# --- subtitle intervals ---
subs=[]
for i,c in enumerate(ch):
    s=c['S']; e=c['E']
    if i>0 and ch[i-1]['slide']!=c['slide']: s=start[c['slide']]
    if i+1<len(ch):
        n=ch[i+1]
        if n['slide']!=c['slide']: e=start[n['slide']]
        elif n['S']-e<0.7: e=n['S']
        else: e=e+0.25
    else: e=END
    subs.append((fr(s),fr(e),c['text'],c['slide']))
# --- states (frame-accurate) ---
events=sorted(set([0,fr(END)]+[fr(v) for v in start.values()]+[a for a,_,_,_ in subs]+[b for _,b,_,_ in subs]))
def slide_at(f):
    k=1
    for n,t in start.items():
        if fr(t)<=f: k=max(k,n)
    return k
def sub_at(f):
    for a,b,t,_ in subs:
        if a<=f<b: return t
    return None
font=ImageFont.truetype('/root/.fonts/NotoSansKR-Medium.otf',54)
os.makedirs('frames',exist_ok=True)
base={}
for n in range(1,nslides+1):
    base[n]=Image.open(f'slides/s-{n:02d}.png').convert('RGB').resize((1920,1080),Image.LANCZOS)
def compose(n,t):
    im=base[n].copy()
    if t:
        w=font.getlength(t); bw=int(round(w))+24
        x0=960-bw//2
        ov=Image.new('RGBA',im.size,(0,0,0,0)); d=ImageDraw.Draw(ov)
        d.rectangle([x0,971,x0+bw-1,1048],fill=(0,0,0,153))
        im=Image.alpha_composite(im.convert('RGBA'),ov)
        ImageDraw.Draw(im).text((960,1006),t,font=font,fill=(255,255,255),anchor='mm')
        im=im.convert('RGB')
    return im
cache={};lines=[];segs=[]
for a,b in zip(events,events[1:]):
    if b<=a: continue
    n=slide_at(a); t=sub_at(a); key=(n,t)
    if key not in cache:
        p=f'frames/f{len(cache):04d}.png'; compose(n,t).save(p); cache[key]=p
    segs.append((a,b,n,t,cache[key]))
with open('concat.txt','w') as f:
    for a,b,n,t,p in segs: f.write(f"file '{p}'\nduration {(b-a)/FPS:.6f}\n")
    f.write(f"file '{segs[-1][4]}'\n")
json.dump({'P':P,'D':D,'start':start,'END':END,'subs':subs,'segs':[s[:4] for s in segs],'total_frames':fr(END)},open('render_plan.json','w'),ensure_ascii=False,indent=0)
print('pause insert at',P,'dur',D,'END',END,'states',len(cache),'segs',len(segs))
