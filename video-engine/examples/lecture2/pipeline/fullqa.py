import json,subprocess,numpy as np
from PIL import Image
p=json.load(open('render_plan.json'))
segs=[]
for line in open('concat.txt'):
    if line.startswith('file'): cur=line.split("'")[1]
    if line.startswith('duration'): segs.append(cur)
W,H=384,216
thumb={}
def th(path):
    if path not in thumb: thumb[path]=np.asarray(Image.open(path).convert('L').resize((W,H),Image.BILINEAR),dtype=np.float32)
    return thumb[path]
exp=[]
for (a,b,n,t),path in zip(p['segs'],segs): exp+= [path]*(b-a)
proc=subprocess.Popen(['ffmpeg','-v','error','-i','out.mp4','-vf',f'scale={W}:{H}:flags=bilinear,format=gray','-f','rawvideo','-'],stdout=subprocess.PIPE)
i=0;worst=0;bad=[]
while True:
    buf=proc.stdout.read(W*H)
    if len(buf)<W*H: break
    fr=np.frombuffer(buf,np.uint8).astype(np.float32).reshape(H,W)
    e=exp[i] if i<len(exp) else exp[-1]
    mae=np.abs(fr-th(e)).mean()
    if mae>3: bad.append((i,round(float(mae),2)))
    worst=max(worst,mae); i+=1
print('frames',i,'expected',len(exp),'worst MAE',worst,'bad',len(bad),bad[:20])
