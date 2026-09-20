# -*- coding: utf-8 -*-
"""Download every narration clip recorded in audio_ledger.json into assets/audio/."""
import json, os, subprocess, sys
led = json.load(open('audio_ledger.json'))
os.makedirs('../assets/audio', exist_ok=True)
missing = []
for k, v in sorted(led.items(), key=lambda x: int(x[0])):
    out = f'../assets/audio/s{int(k):03d}.mp3'
    if os.path.exists(out) and os.path.getsize(out) > 0:
        continue
    r = subprocess.run(['curl', '-fsSL', '--retry', '4', '--retry-delay', '2',
                        '-o', out, v['url']])
    if r.returncode != 0:
        missing.append(k); os.path.exists(out) and os.remove(out)
print('downloaded:', len(led) - len(missing), 'failed:', missing)
sys.exit(1 if missing else 0)
