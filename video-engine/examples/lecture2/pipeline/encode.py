import json,subprocess,numpy as np
from PIL import Image
p=json.load(open('render_plan.json'))
segs=[]
for line in open('concat.txt'):
    if line.startswith('file'): cur=line.split("'")[1]
    if line.startswith('duration'): segs.append(cur)
cmd=['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s','1920x1080','-r','30','-i','-','-i','narr.wav',
 '-map','0:v','-map','1:a','-c:v','libx264','-preset','slow','-crf','12','-tune','stillimage','-pix_fmt','yuv420p',
 '-profile:v','high','-level','4.1','-x264-params','keyint=60','-colorspace','bt709','-color_primaries','bt709','-color_trc','bt709',
 '-c:a','aac','-b:a','320k','-ar','48000','-ac','2','-movflags','+faststart','out.mp4']
pr=subprocess.Popen(cmd,stdin=subprocess.PIPE)
for (a,b,n,t),path in zip(p['segs'],segs):
    raw=np.asarray(Image.open(path).convert('RGB')).tobytes()
    for _ in range(b-a): pr.stdin.write(raw)
pr.stdin.close(); print('rc',pr.wait())
