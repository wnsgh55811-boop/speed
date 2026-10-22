import json, subprocess, numpy as np
from PIL import Image
S='./'
segs=json.load(open(S+'work/segments.json'))
# decode full video at low res grayscale to check every frame's segment identity
W,H=480,270
p=subprocess.Popen(['ffmpeg','-v','error','-i',S+'build/6강_분리의태도_VOD.mp4','-vf',f'scale={W}:{H}','-f','rawvideo','-pix_fmt','gray','-'],stdout=subprocess.PIPE)
ref={}
def r(path):
    if path not in ref: ref[path]=np.asarray(Image.open(path).convert('L').resize((W,H),Image.BILINEAR)).astype(np.float32)
    return ref[path]
fi=0; bad=0; si=0; worst=0
while True:
    b=p.stdout.read(W*H)
    if len(b)<W*H: break
    while si<len(segs)-1 and fi>=segs[si][3]: si+=1
    f=np.frombuffer(b,np.uint8).astype(np.float32)
    g=f.reshape(H,W)
    err=np.abs(g-r(segs[si][0])).mean()
    worst=max(worst,err)
    others=[np.abs(g-r(segs[j][0])).mean() for j in (si-1,si+1) if 0<=j<len(segs) and segs[j][0]!=segs[si][0]]
    if others and min(others)<=err:
        bad+=1
        if bad<10: print('mismatch frame',fi,'expected seg',si,segs[si][4],segs[si][5],'err',err)
    fi+=1
print('frames',fi,'bad',bad,'worst mean abs err',worst)
