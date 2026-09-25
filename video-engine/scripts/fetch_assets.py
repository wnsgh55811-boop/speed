# -*- coding: utf-8 -*-
"""Pull a project's generated assets into assets/lib and key the icons.

    python3 scripts/fetch_assets.py examples/<project>/library.json

library.json maps {key: url}. Photos, illustrations and clips are saved as-is
(assets/lib/<key>.<ext>); the composition references them by relative path so
a render never depends on the CDN mid-capture.

Generated icons (ico_*, pic_*) ship on an opaque studio plate, which reads as
a dark box on the composition. Two keys, picked per image:
  · dark-plate line pictograms  → luminance key, so the glow keeps its falloff
  · everything else             → rembg (isnet-general-use), then a soft edge
Each cutout is trimmed and padded to a square in assets/keyed/<key>.png.

Night-scene stills and clips come out of the generator with a median luma
of 20-40, which reads as a black box once the plate grade and caption scrim
sit on top. Anything with a median below LIFT_BELOW gets a midtone gamma so
its median lands near LIFT_TO — shadows stay dark, faces become visible.
"""
import io, json, math, os, subprocess, sys, urllib.request

import numpy as np
from PIL import Image, ImageFilter

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
LIB = os.path.join(ROOT, "assets", "lib")
OUT = os.path.join(ROOT, "assets", "keyed")
os.makedirs(LIB, exist_ok=True)
os.makedirs(OUT, exist_ok=True)


def load(src):
    if src.startswith("http"):
        return json.loads(urllib.request.urlopen(src).read())
    return json.load(open(src))


def download(url, dst):
    if not os.path.exists(dst) or os.path.getsize(dst) == 0:
        subprocess.run(["curl", "-fsSL", "--retry", "5", "-o", dst, url], check=True)
    return dst


def plate_luma(im):
    a = np.asarray(im).astype(np.float32)
    h, w = a.shape[:2]
    k = max(8, min(h, w) // 12)
    corners = np.concatenate([a[:k, :k].reshape(-1, 3), a[:k, -k:].reshape(-1, 3),
                              a[-k:, :k].reshape(-1, 3), a[-k:, -k:].reshape(-1, 3)])
    return corners.mean(), corners.mean(0)


def luma_key(im, plate):
    a = np.asarray(im).astype(np.float32)
    d = np.sqrt(((a - plate[None, None, :]) ** 2).sum(-1))
    alpha = np.clip((d - 10) / 90.0, 0, 1) ** 0.9
    rgb = np.clip((a - plate[None, None, :] * (1 - alpha[..., None])) /
                  np.maximum(alpha[..., None], 1e-3), 0, 255)
    return Image.fromarray(np.dstack([rgb, alpha * 255]).astype(np.uint8), "RGBA")


_S = None


def rembg_key(im):
    global _S
    from rembg import new_session, remove
    if _S is None:
        _S = new_session("isnet-general-use")
    out = remove(im, session=_S).convert("RGBA")
    a = out.getchannel("A").filter(ImageFilter.GaussianBlur(0.8))
    out.putalpha(a)
    return out


LIFT_BELOW, LIFT_TO = 60, 74


def lift_gamma(median):
    """Exponent that maps the median to LIFT_TO (1.0 = untouched)."""
    if median >= LIFT_BELOW:
        return 1.0
    return max(0.55, math.log(LIFT_TO / 255) / math.log(max(median, 8) / 255))


def lift_still(path):
    im = Image.open(path).convert("RGB")
    lum = np.asarray(im.convert("L").resize((480, 270))).astype(np.float32)
    g = lift_gamma(float(np.median(lum)))
    if g < 1.0:
        a = np.asarray(im).astype(np.float32) / 255.0
        Image.fromarray((np.power(a, g) * 255).clip(0, 255).astype(np.uint8)).save(path)
    return g


def lift_clip(path):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", "2", "-i", path, "-frames:v", "1",
                          "-vf", "scale=480:270,format=gray", "-f", "rawvideo", "-"],
                         capture_output=True).stdout
    g = lift_gamma(float(np.median(np.frombuffer(raw, np.uint8))))
    if g < 1.0:
        tmp = path + ".tmp.mp4"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", path, "-vf", f"eq=gamma={1 / g:.3f}",
                        "-c:v", "libx264", "-crf", "16", "-preset", "medium", "-pix_fmt", "yuv420p",
                        "-an", tmp], check=True)
        os.replace(tmp, path)
    return g


def square(im, pad=0.08, size=900):
    bb = im.getchannel("A").point(lambda v: 255 if v > 12 else 0).getbbox()
    if bb:
        im = im.crop(bb)
    s = int(max(im.size) * (1 + pad * 2))
    c = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    c.alpha_composite(im, ((s - im.size[0]) // 2, (s - im.size[1]) // 2))
    return c.resize((size, size), Image.LANCZOS)


if __name__ == "__main__":
    lib = load(sys.argv[1])
    for k, url in sorted(lib.items()):
        ext = url.rsplit(".", 1)[-1].lower()
        dst0 = f"{LIB}/{k}.{ext}"
        fresh = not os.path.exists(dst0)
        raw = download(url, dst0)
        if fresh and k.startswith(("ph_", "ill_")):
            print(f"{k:16s} lift gamma {lift_still(raw):.2f}", flush=True)
        if fresh and k.startswith("vid_"):
            print(f"{k:16s} lift gamma {lift_clip(raw):.2f}", flush=True)
        if not k.startswith(("ico_", "pic_")):
            continue
        dst = f"{OUT}/{k}.png"
        if os.path.exists(dst):
            continue
        im = Image.open(raw).convert("RGB")
        lum, plate = plate_luma(im)
        how = "luma" if (k.startswith("pic_") and lum < 60) else "rembg"
        cut = luma_key(im, plate) if how == "luma" else rembg_key(im)
        square(cut).save(dst)
        print(f"{k:16s} {how} plate={lum:.0f}", flush=True)
    print("FETCH DONE", flush=True)
