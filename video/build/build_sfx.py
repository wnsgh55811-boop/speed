# -*- coding: utf-8 -*-
"""Synthesize the handful of effect cues. Kept 14-20 dB under the narration
peak so they mark a motion beat without competing with the voice."""
import subprocess
SPECS = {
 'sfx_thump': ('sine=frequency=68:duration=0.45',
               'afade=t=out:st=0.05:d=0.40:curve=exp,volume=-4dB'),
 'sfx_tick':  ('sine=frequency=1150:duration=0.13',
               'afade=t=out:st=0.008:d=0.122:curve=exp,lowpass=f=4000,volume=-10dB'),
 'sfx_riser': ('anoisesrc=d=0.7:c=pink:a=0.9',
               'highpass=f=200,lowpass=f=2600,afade=t=in:st=0:d=0.55:curve=exp,'
               'afade=t=out:st=0.55:d=0.15,volume=-12dB'),
}
for name, (src, af) in SPECS.items():
    subprocess.run(['ffmpeg', '-v', 'error', '-f', 'lavfi', '-i', src, '-af', af,
                    '-ar', '48000', '-b:a', '96k', '-y',
                    f'../assets/audio/{name}.mp3'], check=True)
    print('built', name)
