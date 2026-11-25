"""imgflip meme templates.
  python3 -I meme.py search <keyword> [keyword...]     -> lists "ID name" (template pages)
  python3 -I meme.py get <ID> <name> <memes_dir> [crop] -> memes_dir/<name>.jpg
crop: "x0,y0,x1,y1" pixels | "trim" (cut white margins) | "left" | "right" | "top" | "bottom"
Template image = https://i.imgflip.com/<base36(ID)>.jpg|png  (ID from /meme/<ID>/<name>)."""
import sys, re, io, os, urllib.request, urllib.parse
from PIL import Image
import numpy as np

UA = {"User-Agent": "Mozilla/5.0"}
def http(u): return urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=30).read()
def b36(n):
    s, a = "", "0123456789abcdefghijklmnopqrstuvwxyz"
    while n: s = a[n % 36] + s; n //= 36
    return s

cmd = sys.argv[1]
if cmd == "search":
    for kw in sys.argv[2:]:
        html = http("https://imgflip.com/memesearch?q=" + urllib.parse.quote_plus(kw)).decode("utf-8", "ignore")
        print("==", kw)
        for i, n in sorted(set(re.findall(r'href="/meme/(\d+)/([^"]+)"', html)))[:10]: print(" ", i, n)
elif cmd == "get":
    mid, name, out = sys.argv[2], sys.argv[3], sys.argv[4]
    crop = sys.argv[5] if len(sys.argv) > 5 else None
    data = None
    for ext in ("jpg", "png"):
        try: data = http(f"https://i.imgflip.com/{b36(int(mid))}.{ext}"); break
        except Exception: pass
    if not data: raise SystemExit("download failed")
    im = Image.open(io.BytesIO(data)).convert("RGBA")
    bg = Image.new("RGB", im.size, "white"); bg.paste(im, mask=im.split()[3]); im = bg
    W, H = im.size
    if crop == "trim":
        a = np.asarray(im).astype(int); nw = a.min(axis=2) < 235
        r = np.where(nw.mean(axis=1) > 0.02)[0]; c = np.where(nw.mean(axis=0) > 0.02)[0]
        im = im.crop((c[0], r[0], c[-1] + 1, r[-1] + 1))
    elif crop in ("left", "right", "top", "bottom"):
        im = im.crop({"left": (0, 0, W // 2, H), "right": (W // 2, 0, W, H), "top": (0, 0, W, H // 2), "bottom": (0, H // 2, W, H)}[crop])
    elif crop:
        im = im.crop(tuple(int(v) for v in crop.split(",")))
    os.makedirs(out, exist_ok=True); im.save(os.path.join(out, name + ".jpg"), quality=92)
    print(name, im.size)
