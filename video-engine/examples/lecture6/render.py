import json, subprocess, numpy as np
from PIL import Image
S='./'
segs=json.load(open(S+'work/segments.json'))
cmd=['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s','1920x1080','-r','30','-i','-','-i',S+'build/narration.wav',
 '-map','0:v','-map','1:a','-c:v','libx264','-preset','slow','-crf','10','-tune','stillimage','-pix_fmt','yuv420p','-profile:v','high','-g','60',
 '-color_primaries','bt709','-color_trc','bt709','-colorspace','bt709','-vf','scale=out_color_matrix=bt709:flags=accurate_rnd+full_chroma_int',
 '-c:a','aac','-b:a','320k','-ar','48000','-ac','2','-movflags','+faststart',S+'build/6강_분리의태도_VOD.mp4']
p=subprocess.Popen(cmd,stdin=subprocess.PIPE)
n=0
for path,d,a,b,sl,tx in segs:
    buf=np.asarray(Image.open(path).convert('RGB')).tobytes()
    for _ in range(b-a): p.stdin.write(buf); n+=1
p.stdin.close(); p.wait(); print('frames',n,'rc',p.returncode)
