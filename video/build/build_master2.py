# -*- coding: utf-8 -*-
"""Pre-build the whole soundtrack before rendering: narration blocks placed at
their exact offsets plus a few effect cues, as one master.mp3."""
import json, subprocess, array, os
SR = 48000
cues = json.load(open('cues.json'))
blocks = json.load(open('blocks2.json'))
total, GAP = cues['total'], cues['gap']
n = int(round(total * SR))
buf = array.array('h', bytes(2 * n))

def decode(p):
    r = subprocess.run(['ffmpeg','-v','error','-i',p,'-f','s16le','-ac','1','-ar',str(SR),'-'],
                       capture_output=True)
    return array.array('h', r.stdout)

t = 0.0
for bi in range(len(blocks)):
    p = f'../assets/audio/b{bi:02d}.mp3'
    pcm = decode(p)
    off = int(round(t * SR)); end = min(off + len(pcm), n)
    buf[off:end] = pcm[:end - off]
    dur = float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration',
          '-of','csv=p=0',p], capture_output=True, text=True).stdout)
    t += dur + GAP

# a handful of quiet cues on motion beats only
timing = json.load(open('timing2.json'))['timing']
picks = [(0,'thump'),(len(timing)//4,'tick'),(len(timing)//2,'tick'),
         (len(timing)*3//4,'riser'),(len(timing)-1,'thump')]
for idx, name in picks:
    f = f'../assets/audio/sfx_{name}.mp3'
    if not os.path.exists(f) or idx >= len(timing): continue
    pcm = decode(f)
    off = int(round((timing[idx]['start'] + 0.05) * SR)); end = min(off + len(pcm), n)
    for i in range(end - off):
        v = buf[off+i] + int(pcm[i] * 0.85)
        buf[off+i] = 32767 if v > 32767 else (-32768 if v < -32768 else v)

open('/tmp/m.raw','wb').write(buf.tobytes())
subprocess.run(['ffmpeg','-v','error','-f','s16le','-ar',str(SR),'-ac','1','-i','/tmp/m.raw',
                '-c:a','libmp3lame','-b:a','128k','-y','/tmp/m.mp3'], check=True)
subprocess.run(['ffmpeg','-v','error','-i','/tmp/m.mp3','-t',str(total),'-c','copy','-y',
                '../assets/audio/master.mp3'], check=True)
d = subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',
                    '../assets/audio/master.mp3'], capture_output=True, text=True).stdout.strip()
print(f'master.mp3 {float(d):.3f}s vs composition {total}s')
