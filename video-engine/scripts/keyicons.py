# -*- coding: utf-8 -*-
"""Key the 3D objects and pictograms of a project out of their plates.

    python3 keyicons.py <library.json url|path> <put-map.json> [--sheet]

Generated icons ship on an opaque studio plate, which reads as a dark box on
the composition. Two keys, picked per image:
  · dark-plate line pictograms  → luminance key, so the glow keeps its falloff
  · everything else             → rembg (isnet-general-use), then a soft edge
Each cutout is trimmed, padded to a square and uploaded to its presigned PUT.
"""
import io, json, os, subprocess, sys, urllib.request

import numpy as np
from PIL import Image, ImageFilter

OUT = "keyed"
os.makedirs(OUT, exist_ok=True)


def load(src):
    if src.startswith("http"):
        return json.loads(urllib.request.urlopen(src).read())
    return json.load(open(src))


def fetch(url):
    return Image.open(io.BytesIO(urllib.request.urlopen(url).read())).convert("RGB")


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
    puts = load(sys.argv[2]) if len(sys.argv) > 2 and os.path.exists(sys.argv[2]) else {}
    for k, url in sorted(lib.items()):
        if not k.startswith(("ico_", "pic_")):
            continue
        dst = f"{OUT}/{k}.png"
        if not os.path.exists(dst):
            im = fetch(url)
            lum, plate = plate_luma(im)
            how = "luma" if (k.startswith("pic_") and lum < 60) else "rembg"
            cut = luma_key(im, plate) if how == "luma" else rembg_key(im)
            square(cut).save(dst)
            print(f"{k:16s} {how} plate={lum:.0f}", flush=True)
        if k in puts:
            r = subprocess.run(["curl", "-sf", "-X", "PUT", "-H", "Content-Type: image/png",
                                "--data-binary", "@" + dst, puts[k], "-o", "/dev/null",
                                "-w", "%{http_code}"], capture_output=True, text=True)
            print(f"  PUT {k} {r.stdout}", flush=True)
    print("KEY DONE", flush=True)
