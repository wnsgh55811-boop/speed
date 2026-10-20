"""timeline.json -> 프레임 정렬 구간 -> 슬라이드+자막 PNG -> concat -> MP4"""
import json, sys, os, subprocess
from PIL import Image, ImageDraw, ImageFont

W, AUDIO, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
FPS = 30
tl = json.load(open(f"{W}/timeline.json", encoding="utf-8"))
ch = tl["chunks"]; END = tl["audio_end"]
NS = 24

FONT = ImageFont.truetype("/root/.fonts/noto/NotoSansKR_500Medium.ttf", 38)
BOX_TOP, BOX_H, PAD = 971, 78, 12

def fr(t): return int(round(t * FPS))

# 슬라이드 전환 시각 = 해당 슬라이드 첫 조각의 t0 (= 앞 슬라이드 마지막 문장 뒤 무음 중앙)
first_of = {}
for c in ch:
    first_of.setdefault(c["slide"], c["t0"])
sw = [0.0] + [first_of[s] for s in range(2, NS + 1)]  # slide s starts at sw[s-1]
slide_at = lambda f: max(s for s in range(1, NS + 1) if fr(sw[s - 1]) <= f)

# 프레임별 상태 (slide, chunk idx or -1)
NF = fr(END)
state = [None] * NF
for f in range(NF):
    state[f] = [slide_at(f), -1]
for i, c in enumerate(ch):
    for f in range(fr(c["t0"]), min(fr(c["t1"]), NF)):
        state[f][1] = i
# 검증: 자막 조각의 슬라이드와 화면 슬라이드가 일치해야 함
bad = [(f, s, ch[k]["slide"]) for f, (s, k) in enumerate(state) if k >= 0 and ch[k]["slide"] != s]
assert not bad, bad[:5]

segs = []
for f, st in enumerate(state):
    if segs and segs[-1][2] == tuple(st): segs[-1][1] = f + 1
    else: segs.append([f, f + 1, tuple(st)])

os.makedirs(f"{W}/frames", exist_ok=True)
cache = {}
def img_for(s, k):
    key = (s, k)
    if key in cache: return cache[key]
    p = f"{W}/frames/s{s:02d}_{k:03d}.png"
    im = Image.open(f"{W}/slides2/s-{s:02d}.png").convert("RGBA")
    if k >= 0:
        txt = ch[k]["text"]
        tw = FONT.getlength(txt)
        bw = int(round(tw)) + 2 * PAD
        x0 = (1920 - bw) // 2
        ov = Image.new("RGBA", im.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(ov)
        d.rectangle([x0, BOX_TOP, x0 + bw - 1, BOX_TOP + BOX_H - 1], fill=(0, 0, 0, 153))
        d.text((960, BOX_TOP + BOX_H / 2), txt, font=FONT, fill=(255, 255, 255, 255), anchor="mm")
        im = Image.alpha_composite(im, ov)
    im.convert("RGB").save(p)
    cache[key] = p
    return p

with open(f"{W}/concat.txt", "w") as fh:
    for a, b, (s, k) in segs:
        fh.write(f"file '{img_for(s, k)}'\nduration {(b - a) / FPS:.6f}\n")
    fh.write(f"file '{img_for(*segs[-1][2])}'\n")
json.dump([[a, b, s, k] for a, b, (s, k) in segs], open(f"{W}/segs.json", "w"))
print("segments", len(segs), "frames", NF)

subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-stats",
    "-f", "concat", "-safe", "0", "-i", f"{W}/concat.txt", "-i", AUDIO,
    "-map", "0:v", "-map", "1:a", "-vf", f"fps={FPS},format=yuv420p", "-frames:v", str(NF),
    "-c:v", "libx264", "-preset", "slow", "-crf", "14", "-tune", "stillimage",
    "-profile:v", "high", "-x264-params", "keyint=60:min-keyint=1",
    "-maxrate", "20M", "-bufsize", "40M",
    "-c:a", "aac", "-b:a", "320k", "-ar", "48000", "-ac", "2",
    "-movflags", "+faststart", "-t", f"{NF / FPS:.6f}", OUT], check=True)
