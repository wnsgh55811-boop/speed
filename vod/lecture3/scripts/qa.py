import json, subprocess, numpy as np, sys
from PIL import Image
S=sys.argv[1]; O=S+'/out/lecture3.mp4'
T=json.load(open('timeline.json')); VS=json.load(open('vsubs.json'))
def frame(t):
    raw=subprocess.run(['ffmpeg','-v','error','-ss',f'{t:.3f}','-i',O,'-frames:v','1','-f','rawvideo','-pix_fmt','rgb24','-'],capture_output=True).stdout
    return np.frombuffer(raw,np.uint8).reshape(1080,1920,3).astype(np.float32)
slides=[np.array(Image.open(f'{S}/render/s{n:02d}.png').convert('RGB')).astype(np.float32) for n in range(1,23)]
def psnr(a,b): 
    m=np.mean((a-b)**2); return 99 if m==0 else 10*np.log10(255**2/m)
err=0
# 1) slide identity at start+0.2, mid, end-0.2 (top 960 rows, away from subtitles and video boxes)
for s in T['slides']:
    for t in (s['start']+0.2, (s['start']+s['end'])/2, s['end']-0.2):
        f=frame(t)
        if s['n']==16: f[434:942,163:1767]=slides[15][434:942,163:1767]
        sc=[psnr(f[:960],sl[:960]) for sl in slides]
        best=int(np.argmax(sc))+1
        if best!=s['n'] or sc[best-1]<40: err+=1; print('SLIDE MISMATCH',s['n'],round(t,2),best,round(sc[best-1],1))
print('slide check done')
# 2) every sentence inside its slide window
for x in T['sents']:
    sl=T['slides'][x['slide']-1]
    if not (sl['start']-1e-6<=x['s'] and x['e']<=sl['end']+1e-6): err+=1; print('SENT OUTSIDE SLIDE',x)
# 3) subtitles within slide windows, no overlaps, length<=25
subs=sorted(T['subs'],key=lambda s:s['s'])
for a in subs:
    sl=T['slides'][a['slide']-1]
    if a['s']<sl['start']-1e-6 or a['e']>sl['end']+1e-6: err+=1; print('SUB CROSSES SLIDE',a)
    if len(a['text'])>25: err+=1; print('LONG',a)
for a,b in zip(subs,subs[1:]):
    if a['e']>b['s']+1e-6: err+=1; print('OVERLAP',a,b)
# 4) subtitle band vs slide content: the band rows 971..1048 under each slide's widest subtitle must be blank background
sys.path.insert(0,S+'/scripts'); from subimg import render
for n in range(1,23):
    texts=[s['text'] for s in subs if s['slide']==n]
    if n==16: texts+= [v['text'] for k in VS for v in VS[k]]
    xs=[]; 
    for t in texts:
        im,x,y=render(t,S+'/fonts/NotoSansKR-500.ttf'); xs.append((x,x+im.size[0]))
    x0=min(a for a,b in xs); x1=max(b for a,b in xs)
    band=slides[n-1][965:1054, x0:x1]
    var=band.reshape(-1,3).std(0).max()
    if var>2: err+=1; print('PPT CONTENT UNDER SUBTITLE BAND slide',n,var)
# 5) subtitle box geometry from actual frames
for a in subs[::25]:
    f=frame((a['s']+a['e'])/2)
    col=f[:,960]
    dark=[y for y in range(900,1080) if col[y].mean()<140]
    print('sub box rows', min(dark), max(dark), a['text'])
print('ERRORS',err)
