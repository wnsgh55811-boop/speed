# -*- coding: utf-8 -*-
"""Real mp3 durations -> durations.json, plus sentence boundaries via silencedetect
so per-cue subtitle windows land on actual speech gaps instead of a proportional guess."""
import json, os, re, subprocess
S = json.load(open('scenes.json'))
durs, bounds = {}, {}
for i, sc in enumerate(S):
    p = f'../assets/audio/s{i:03d}.mp3'
    if not os.path.exists(p): continue
    d = float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration',
                              '-of','csv=p=0',p],capture_output=True,text=True).stdout.strip())
    durs[str(i)] = round(d, 3)
    if len(sc['cues']) > 1:
        r = subprocess.run(['ffmpeg','-v','info','-i',p,'-af',
                            'silencedetect=noise=-32dB:d=0.16','-f','null','-'],
                           capture_output=True, text=True).stderr
        starts = [float(m) for m in re.findall(r'silence_start: ([\d.]+)', r)]
        ends   = [float(m) for m in re.findall(r'silence_end: ([\d.]+)', r)]
        gaps = sorted(zip(starts, ends), key=lambda g: g[1]-g[0], reverse=True)
        need = len(sc['cues']) - 1
        picked = sorted((s+e)/2 for s, e in gaps[:need])
        if len(picked) == need:
            bounds[str(i)] = [round(x, 3) for x in picked]
json.dump(durs, open('durations.json','w'), indent=1)
json.dump(bounds, open('cue_bounds.json','w'), indent=1)
tot = sum(durs.values())
print(f'measured {len(durs)} clips, speech total {tot:.1f}s ({tot/60:.2f}min), '
      f'aligned boundaries for {len(bounds)} multi-cue scenes')
