# -*- coding: utf-8 -*-
"""Key every figure out and give the people a hand-torn paper edge.

Run this over the raw generated stills BEFORE they go into the composition.
Generated portraits usually ship opaque, so on screen they read as dark
rectangles sitting on the plate. This keys them with rembg, then builds a
torn-paper card: dilate, blur into a wide ramp, push two octaves of noise
through it, and only then hard-threshold — so the white border wanders like a
real tear instead of reading as a die-cut sticker.

    pip install rembg onnxruntime pillow numpy
    python3 paper.py              # reads urls.json, writes out/

urls.json maps {asset_key: cdn_basename}. Icons (keys starting "ico_") are
keyed and trimmed only — no paper card.
"""
import json
import os

import numpy as np
from PIL import Image, ImageFilter
from rembg import new_session, remove

PAPER = (240, 238, 232)
SESS = new_session("u2net")


def _octave(shape, blur, seed):
    rng = np.random.default_rng(seed)
    n = rng.normal(0, 1, shape)
    n = (n - n.min()) / (np.ptp(n) + 1e-6)
    n = np.asarray(Image.fromarray((n * 255).astype(np.uint8))
                   .filter(ImageFilter.GaussianBlur(blur))).astype(np.float32) / 255.0
    n = n - n.mean()
    return n / (np.abs(n).max() + 1e-6)


def ragged_mask(alpha, grow=15, jitter=6.5, seed=0):
    m = alpha.filter(ImageFilter.MaxFilter(3))
    for _ in range(max(1, grow // 2)):
        m = m.filter(ImageFilter.MaxFilter(3))
    m = m.filter(ImageFilter.GaussianBlur(max(3.0, grow * 0.85)))
    a = np.asarray(m).astype(np.float32) / 255.0
    a = a + _octave(a.shape, max(5.0, grow * 0.9), seed) * (0.42 * jitter / 10.0) \
          + _octave(a.shape, 1.6, seed + 977) * (0.16 * jitter / 10.0)
    return Image.fromarray(((a > 0.5) * 255).astype(np.uint8)) \
                .filter(ImageFilter.GaussianBlur(0.7))


def grain(img, amount=5, seed=0):
    rng = np.random.default_rng(seed)
    a = np.asarray(img.convert("RGB")).astype(np.int16)
    n = rng.normal(0, amount, a.shape[:2])[:, :, None]
    return Image.fromarray(np.clip(a + n, 0, 255).astype(np.uint8)).convert("RGBA")


def key(im):
    """Return an RGBA cutout, trusting an alpha channel that is already real."""
    if im.mode in ("RGBA", "LA"):
        a = im.convert("RGBA").getchannel("A")
        if np.asarray(a).min() == 0:
            return im.convert("RGBA")
    return remove(im.convert("RGB"), session=SESS).convert("RGBA")


def trim(im):
    bb = im.getchannel("A").getbbox()
    return im.crop(bb) if bb else im


def paper_card(im, seed, height=1500):
    sub = trim(im)
    s = height / sub.size[1]
    sub = sub.resize((max(1, int(sub.size[0] * s)), height), Image.LANCZOS)
    a = sub.getchannel("A")

    pad = 46
    size = (sub.size[0] + pad * 2, sub.size[1] + pad * 2)
    am = Image.new("L", size, 0)
    am.paste(a, (pad, pad))
    tear = ragged_mask(am, seed=seed)

    paper = grain(Image.new("RGBA", size, PAPER + (255,)), 5, seed)
    paper.putalpha(tear)

    shadow = Image.new("RGBA", size, (0, 0, 0, 0))
    shadow.paste((0, 0, 0, 150), (0, 0), tear)
    shadow = shadow.filter(ImageFilter.GaussianBlur(16))

    out = Image.new("RGBA", size, (0, 0, 0, 0))
    out.alpha_composite(shadow, (0, 7))
    out.alpha_composite(paper)
    out.alpha_composite(sub, (pad, pad))
    return out


if __name__ == "__main__":
    urls = json.load(open("urls.json"))
    os.makedirs("out", exist_ok=True)
    for n, k in enumerate(sorted(urls)):
        dst = f"out/{k}.png"
        if os.path.exists(dst):
            continue
        im = key(Image.open(f"{k}.png"))
        im = trim(im) if k.startswith("ico_") else paper_card(im, seed=n * 37 + 11)
        im.save(dst)
        print(f"{k:16s} -> {im.size}", flush=True)
    print("PAPER DONE")
