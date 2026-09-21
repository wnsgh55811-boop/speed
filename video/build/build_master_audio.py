# -*- coding: utf-8 -*-
"""Pre-build the entire soundtrack as one file BEFORE rendering.

The composition references a single assets/audio/master.mp3. Building it up
front keeps the render lean (one audio element instead of 114) and lets the
soundtrack be checked on its own. Narration clips never overlap, so each is
written at its exact cue offset into a silent timeline; the effect cues are
summed on top with headroom.
"""
import json, subprocess, array, re, os
SR = 48000
LEAD = 0.16
T = json.load(open('timing.json'))
tl, total = T['timing'], T['total']
n = int(round(total * SR))
buf = array.array('h', bytes(2 * n))

def decode(p):
    r = subprocess.run(['ffmpeg', '-v', 'error', '-i', p, '-f', 's16le',
                        '-ac', '1', '-ar', str(SR), '-'], capture_output=True)
    return array.array('h', r.stdout)

for s in tl:
    pcm = decode(f'../assets/audio/s{s["i"]:03d}.mp3')
    off = int(round((s['start'] + LEAD) * SR))
    end = min(off + len(pcm), n)
    buf[off:end] = pcm[:end - off]

html = open('../index.html').read()
for f, t in re.findall(r'src="assets/audio/(sfx_[a-z]+\.mp3)" data-start="([0-9.]+)"', html):
    if not os.path.exists(f'../assets/audio/{f}'):
        continue
    pcm = decode(f'../assets/audio/{f}')
    off = int(round(float(t) * SR)); end = min(off + len(pcm), n)
    for i in range(end - off):
        v = buf[off + i] + int(pcm[i] * 0.9)
        buf[off + i] = 32767 if v > 32767 else (-32768 if v < -32768 else v)

open('/tmp/master.raw', 'wb').write(buf.tobytes())
subprocess.run(['ffmpeg', '-v', 'error', '-f', 's16le', '-ar', str(SR), '-ac', '1',
                '-i', '/tmp/master.raw', '-c:a', 'libmp3lame', '-b:a', '128k',
                '-y', '/tmp/master_untrimmed.mp3'], check=True)
# trim the encoder's tail padding so the track matches the composition exactly
subprocess.run(['ffmpeg', '-v', 'error', '-i', '/tmp/master_untrimmed.mp3',
                '-t', str(total), '-c', 'copy', '-y',
                '../assets/audio/master.mp3'], check=True)
d = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
                    '-of', 'csv=p=0', '../assets/audio/master.mp3'],
                   capture_output=True, text=True).stdout.strip()
print(f'master.mp3 {float(d):.3f}s vs composition {total}s')
