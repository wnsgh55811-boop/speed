# -*- coding: utf-8 -*-
"""Download every image in image_ledger.json. Portraits/3D icons keep alpha (.png);
photographs are written as .jpg because they are used as full-bleed backgrounds."""
import json, os, subprocess, sys
led = json.load(open('image_ledger.json'))
os.makedirs('../assets/img', exist_ok=True)
bad = []
for name, v in led.items():
    if name.startswith('_'): continue
    ext = 'jpg' if v['kind'] == 'photo' else 'png'
    out = f'../assets/img/{name}.{ext}'
    tmp = f'/tmp/{name}.src'
    if subprocess.run(['curl','-fsSL','--retry','4','--retry-delay','2','-o',tmp,v['url']]).returncode:
        bad.append(name); continue
    if ext == 'jpg':
        subprocess.run(['ffmpeg','-v','error','-i',tmp,'-vf','scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080',
                        '-q:v','3','-y',out], check=True)
    else:
        subprocess.run(['ffmpeg','-v','error','-i',tmp,'-y',out], check=True)
    os.remove(tmp)
print('images ok:', sum(1 for k in led if not k.startswith('_')) - len(bad), 'failed:', bad)
sys.exit(1 if bad else 0)
