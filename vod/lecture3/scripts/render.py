# Render final MP4 from timeline.json.
# usage: render.py timeline.json vsubs.json slides_dir narr.wav before.mp4 after.mp4 font.ttf out.mp4 [after_trim]
import sys, json, subprocess, numpy as np
from PIL import Image
sys.path.insert(0, __import__('os').path.dirname(__file__))
from subimg import render as subrender

T = json.load(open(sys.argv[1])); VS = json.load(open(sys.argv[2]))
SL, NARR, VB, VA, FONT, OUT = sys.argv[3:9]
FPS = 30; W, H = 1920, 1080; SR = 48000
BOX = {'BEFORE': (163, 434, 730, 508), 'AFTER': (1037, 434, 730, 489)}
SRC = {'BEFORE': VB, 'AFTER': VA}
total = T['total']; nfr = int(round(total * FPS))
tl = T['timeline']
vids = {a[3]: (a[0], a[1]) for a in tl if a[2] == 'video'}

# ---- subtitles: narration chunks + video dialogue (relative to clip start)
subs = list(T['subs'])
for name, lst in VS.items():
    st0, en0 = vids[name]
    for s in lst:
        subs.append({'s': st0 + s['s'], 'e': min(st0 + s['e'], en0), 'text': s['text'], 'slide': 16})
subs.sort(key=lambda s: s['s'])
for a, b in zip(subs, subs[1:]):
    assert a['e'] <= b['s'] + 1e-6, (a, b)

# ---- audio
def load(path, ss=None, dur=None):
    cmd = ['ffmpeg', '-v', 'error']
    if ss is not None: cmd += ['-ss', str(ss)]
    if dur is not None: cmd += ['-t', str(dur)]
    cmd += ['-i', path, '-vn', '-ac', '2', '-ar', str(SR), '-f', 'f32le', '-']
    return np.frombuffer(subprocess.run(cmd, capture_output=True, check=True).stdout, np.float32).reshape(-1, 2)
narr = load(NARR)
vgain = json.load(open(sys.argv[9])) if len(sys.argv) > 9 else {}
pieces = []; cursor = 0
for a, b, k, arg, src in tl:
    n = int(round(b * SR)) - int(round(a * SR))
    if k == 'narr':
        s0 = int(round(src * SR)); p = narr[s0:s0 + n]
    elif k == 'silence':
        p = np.zeros((n, 2), np.float32)
    else:
        p = load(SRC[arg], 0, b - a) * (10 ** (vgain.get(arg, 0) / 20))
    if len(p) < n: p = np.vstack([p, np.zeros((n - len(p), 2), np.float32)])
    p = p[:n].copy()
    if k == 'narr' and n > 960:      # 10 ms de-click ramps at every narration cut
        r = np.linspace(0, 1, 480, dtype=np.float32)[:, None]
        if a > 0: p[:480] *= r
        if b < total - 1e-6: p[-480:] *= r[::-1]
    pieces.append(p[:n])
aud = np.clip(np.vstack(pieces), -1, 1)
wav = OUT + '.wav'
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'f32le', '-ar', str(SR), '-ac', '2', '-i', '-', '-c:a', 'pcm_s24le', wav],
               input=aud.tobytes(), check=True)

# ---- video frames of the PPT clips (scaled into the PPT box, stretched exactly like PowerPoint)
vframes = {}
for name, (st0, en0) in vids.items():
    x, y, w, h = BOX[name]
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', SRC[name], '-t', str(en0 - st0), '-map', '0:v:0',
                          '-vf', f'fps={FPS},scale={w}:{h}:flags=lanczos', '-pix_fmt', 'rgb24', '-f', 'rawvideo', '-'],
                         capture_output=True, check=True).stdout
    vframes[name] = np.frombuffer(raw, np.uint8).reshape(-1, h, w, 3)
    print(name, 'frames', len(vframes[name]), 'needed', round((en0 - st0) * FPS, 2), flush=True)

slides = [np.array(Image.open(f'{SL}/s{n:02d}.png').convert('RGB')) for n in range(1, 23)]
sub_cache = {}
def sub_overlay(text):
    if text not in sub_cache:
        im, x, y = subrender(text, FONT)
        a = np.array(im).astype(np.float32)
        sub_cache[text] = (a[..., :3], a[..., 3:4] / 255.0, x, y)
    return sub_cache[text]

def slide_at(t):
    for s in T['slides']:
        if s['start'] <= t < s['end']: return s['n']
    return T['slides'][-1]['n']

enc = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                        '-i', wav, '-map', '0:v', '-map', '1:a',
                        '-vf', 'scale=out_color_matrix=bt709:out_range=tv:flags=accurate_rnd+full_chroma_int,format=yuv420p',
                        '-c:v', 'libx264', '-preset', 'slow', '-crf', '14', '-maxrate', '30M', '-bufsize', '60M',
                        '-profile:v', 'high', '-level', '4.2', '-g', '60',
                        '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709', '-color_range', 'tv',
                        '-c:a', 'aac', '-b:a', '320k', '-ar', str(SR), '-movflags', '+faststart', '-shortest', OUT],
                       stdin=subprocess.PIPE)
last_key = None; last_buf = None
si = 0
for f in range(nfr):
    t = (f + 0.5) / FPS          # sample the middle of each frame interval
    n = slide_at(t)
    vkey = []
    if n == 16:
        for name, (st0, en0) in vids.items():
            if t >= st0:
                vkey.append((name, min(int((t - st0) * FPS), len(vframes[name]) - 1)))
    sub = next((s['text'] for s in subs if s['s'] <= t < s['e']), None)
    key = (n, tuple(vkey), sub)
    if key != last_key:
        fr = slides[n - 1].copy()
        for name, idx in vkey:
            x, y, w, h = BOX[name]
            fr[y:y + h, x:x + w] = vframes[name][idx]
        if sub:
            rgb, al, x, y = sub_overlay(sub)
            h_, w_ = al.shape[:2]
            reg = fr[y:y + h_, x:x + w_].astype(np.float32)
            fr[y:y + h_, x:x + w_] = (rgb * al + reg * (1 - al) + 0.5).astype(np.uint8)
        last_buf = fr.tobytes(); last_key = key
    enc.stdin.write(last_buf)
    if f % 1800 == 0: print('frame', f, '/', nfr, flush=True)
enc.stdin.close(); enc.wait()
print('done', OUT, enc.returncode)
