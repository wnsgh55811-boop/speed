# -*- coding: utf-8 -*-
"""Emit the HyperFrames composition for the 이다사 explainer.

Data in:  chunks.json (251 narration lines), plan.py (per-line scene spec),
          timings.txt (line start/end on the 1.2x master), style.css
Data out: ../index.html  — one root, one paused GSAP timeline, four tracks.

Review notes this build is written to satisfy:
  · captions are ALWAYS one line — measured here and pre-split, then pinned
    with `white-space:nowrap` so nothing can wrap at runtime
  · captions are white with a thin dark stroke behind the glyph
  · eight background families in rotation, never the same one three in a row
  · every wording block sits on a soft scrim so it never sinks into the plate
"""
import html
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from plan import PLAN                                    # noqa: E402
from PIL import ImageFont, ImageDraw, Image              # noqa: E402

W, H, FPS = 1920, 1080, 30
CAP_PX, CAP_MAX = 44, 1720
CDN = "https://d8j0ntlcm91z4.cloudfront.net/user_36TmLGicluGODkcYejmrwLWoKV7/"

# ── assets still sourced from the existing library (photos, cutouts, icons) ──
IMG = {
    "man_anx_1": "hf_20260919_150249_cd53c03a-b5d9-45a0-a3c2-ee29af265975.png",
    "man_anx_2": "hf_20260919_150249_ca824452-f7e3-4121-b73d-40d76561824e.png",
    "man_anx_3": "hf_20260919_151231_07d20b97-81d6-49ab-9f05-3c0b9cd5c593.png",
    "man_calm_1": "hf_20260919_150249_6de87b05-88db-4809-8be0-6def38e1e740.png",
    "man_calm_2": "hf_20260919_150249_420e758f-c732-4ae8-bd6f-e879f96a5e31.png",
    "man_calm_3": "hf_20260919_151232_8080bd32-9233-4c44-8103-85562f87dbe3.png",
    "man_think_1": "hf_20260919_150249_fe1e5693-59c6-4073-98c6-34969481085e.png",
    "man_think_2": "hf_20260919_151231_9ef0649d-ab5b-4a96-ac96-5a059076191a.png",
    "man_blur_1": "hf_20260919_150401_42c819e9-deea-488d-8fff-9c26be67c05e.png",
    "woman_a_1": "hf_20260919_150250_5990577d-da93-407e-afd8-cd846025e0cf.png",
    "woman_a_2": "hf_20260919_151232_840ec21e-8988-4261-9f79-c2fb58b114fa.png",
    "woman_b_1": "hf_20260919_150249_089b5b06-e5da-468d-9f2b-424de1cbf11d.png",
    "woman_b_2": "hf_20260919_151231_dc2c1cf1-0703-4d5d-9bca-f2a9f7b1025f.png",
    "ico_bubble_1": "hf_20260919_150401_c5d52053-e2bd-46ea-bc1a-34a3f2c08ca5.png",
    "ico_clock_1": "hf_20260919_150401_224491d1-8b14-4346-a9cf-7d47abf79488.png",
    "ico_glass_1": "hf_20260919_150401_0132827d-32e6-46ee-bf44-ea2aa6fa79a6.png",
    "ico_question_1": "hf_20260919_150401_8b00f700-9e09-439b-9349-20e44e9fec04.png",
    "ico_shoe_1": "hf_20260919_150725_3952f845-0d05-47fe-a7fd-37b01c4fe727.png",
    "ico_question_x_1": "hf_20260919_150726_0d922159-eaa8-4f30-8f25-e98348f64f8b.png",
    "br_cafe_two_1": "hf_20260919_150455_d80b901e-88f5-4d28-b8eb-6dac4028b719.png",
    "br_cafe_two_2": "hf_20260919_150726_c57cae7d-ea4a-4b8d-9d34-ef799d51af8f.png",
    "br_friends_1": "hf_20260919_150455_ea2b7058-4f8d-488a-a5d3-00d84ccc9d42.png",
    "br_phone_1": "hf_20260919_150455_afaf3360-4b62-4539-8a7c-855e164cee7d.png",
    "br_silence_table_1": "hf_20260919_150455_42528e16-9f2b-4188-ba7e-26a151f5802b.png",
    "br_silence_table_2": "hf_20260919_150725_11e9de28-391b-4182-808e-05197c64d1c6.png",
    "br_listen_1": "hf_20260919_150455_8ba469e7-6261-4f0b-aff6-9afdb0511fe4.png",
    "br_listen_2": "hf_20260919_150725_8394df35-628e-4a63-a8a1-7ded06f838e5.png",
    "br_counsel_1": "hf_20260919_150455_334a652b-a84b-42d0-8619-24d493e02ff5.png",
    "br_counsel_2": "hf_20260919_150725_7b1fa783-9f41-466f-a766-9c6823428651.png",
    "br_empty_chair_1": "hf_20260919_150455_295029c3-0dbb-44e2-9691-aa32435c7dcb.png",
    "br_bench_1": "hf_20260919_150455_9d84089a-1655-4aca-a2a9-d70e4bbc0206.png",
    "br_bench_2": "hf_20260919_150725_892f5427-0695-40f8-9236-db2a0284db5d.png",
    "br_running_1": "hf_20260919_150455_a335d8af-e590-4c96-9c98-9c769537ead8.png",
    "br_coffee_1": "hf_20260919_150455_3ac53c0f-058b-48e6-bc5c-4a6f3bbf525d.png",
    "br_mirror_1": "hf_20260919_150454_078d1108-2867-4f86-8bff-9048702aa86c.png",
    "br_street_1": "hf_20260919_150725_2754bc1b-d5f5-46a0-baef-cfcefcba89c2.png",
    # widened pools so no single still carries more than two scenes
    "man_anx_4": "hf_20260920_015819_5cdb1819-6174-4c48-9875-065810181dd1.png",
    "man_anx_5": "hf_20260920_015824_5412fd90-9b2e-48ff-aa04-32dc5087e276.png",
    "man_anx_6": "hf_20260920_015829_96a39513-e0e3-4c74-b06b-eef739b81bce.png",
    "man_anx_7": "hf_20260920_015835_4ac10782-f15a-40d9-8d13-4e428b374dac.png",
    "man_calm_4": "hf_20260920_015840_c4a3eb84-4353-4641-b3c4-2f538b8b420c.png",
    "man_calm_5": "hf_20260920_015845_9efdd36e-295f-4f3b-8853-5ff9a7789a3d.png",
    "woman_b_3": "hf_20260920_015851_9a359522-55fd-4498-9187-26da7b850f69.png",
    "woman_b_4": "hf_20260920_015856_465e34de-c515-4465-b2fa-2588b820dea2.png",
    "woman_a_3": "hf_20260920_015901_e9ee8918-080c-4f70-98e1-a473aec5699a.png",
}
# ── keyed figures ───────────────────────────────────────────────────────────
# The stills shipped opaque: every person and icon was an un-keyed rectangle
# sitting on the plate, which is why they read as dark boxes. These are the
# same frames cut out and, for the people, rebuilt as torn-paper cards.
KEYED = {
    "man_anx_1": "https://d2ol7oe51mr4n9.cloudfront.net/user_36TmLGicluGODkcYejmrwLWoKV7/32150598-ba63-47e2-a7f2-0cd0ac39ee44.png",
    "man_anx_2": "https://d2ol7oe51mr4n9.cloudfront.net/user_36TmLGicluGODkcYejmrwLWoKV7/613ad7a0-22a5-49fa-8dfc-e63ac40b9b55.png",
    "man_anx_3": "https://d2ol7oe51mr4n9.cloudfront.net/user_36TmLGicluGODkcYejmrwLWoKV7/24437ef0-f737-4184-8f4f-e72a99d34ab4.png",
    "man_anx_4": "https://d2ol7oe51mr4n9.cloudfront.net/user_36TmLGicluGODkcYejmrwLWoKV7/d93e8cb1-15b7-40a9-adae-bc5d294f6d7b.png",
    "man_anx_5": "https://d2ol7oe51mr4n9.cloudfront.net/user_36TmLGicluGODkcYejmrwLWoKV7/02aed6dc-5615-4fd3-b0f3-a4efa733d15a.png",
    "man_anx_6": "https://d2ol7oe51mr4n9.cloudfront.net/user_36TmLGicluGODkcYejmrwLWoKV7/6e3ea0e7-0a92-4598-a472-945169617595.png",
    "man_anx_7": "https://d2ol7oe51mr4n9.cloudfront.net/user_36TmLGicluGODkcYejmrwLWoKV7/243f5439-b64b-45da-b3c3-da119212121c.png",
    "man_calm_1": "https://d2ol7oe51mr4n9.cloudfront.net/user_36TmLGicluGODkcYejmrwLWoKV7/83f70de3-dea0-4c27-b758-11d60c452cbf.png",
    "man_calm_2": "https://d2ol7oe51mr4n9.cloudfront.net/user_36TmLGicluGODkcYejmrwLWoKV7/3855860b-37ef-4426-9c4f-b4a3d55b4293.png",
    "man_calm_3": "https://d2ol7oe51mr4n9.cloudfront.net/user_36TmLGicluGODkcYejmrwLWoKV7/88767897-55bf-46cb-a39d-dbbb94995008.png",
    "man_calm_4": "https://d2ol7oe51mr4n9.cloudfront.net/user_36TmLGicluGODkcYejmrwLWoKV7/e166ccb7-12a5-45a3-acf9-7c376f8eeeaa.png",
    "man_calm_5": "https://d2ol7oe51mr4n9.cloudfront.net/user_36TmLGicluGODkcYejmrwLWoKV7/4a1b7cb7-e8c4-4d39-80f8-841f95e48ea2.png",
    "man_think_1": "https://d2ol7oe51mr4n9.cloudfront.net/user_36TmLGicluGODkcYejmrwLWoKV7/f59f98bc-d3d3-4ff0-9f0a-15e8478f261a.png",
    "man_think_2": "https://d2ol7oe51mr4n9.cloudfront.net/user_36TmLGicluGODkcYejmrwLWoKV7/8b28bd06-74a6-4b8c-ada6-87efcc91fe49.png",
    "man_blur_1": "https://d2ol7oe51mr4n9.cloudfront.net/user_36TmLGicluGODkcYejmrwLWoKV7/9f4d80f6-581b-4404-879d-344f38fe5428.png",
    "woman_a_1": "https://d2ol7oe51mr4n9.cloudfront.net/user_36TmLGicluGODkcYejmrwLWoKV7/dd14294c-823d-40b8-826c-707724a8819b.png",
    "woman_a_2": "https://d2ol7oe51mr4n9.cloudfront.net/user_36TmLGicluGODkcYejmrwLWoKV7/dcdba5b4-34ae-40de-aa86-db104bd166ab.png",
    "woman_a_3": "https://d2ol7oe51mr4n9.cloudfront.net/user_36TmLGicluGODkcYejmrwLWoKV7/21463608-5ec2-4158-8924-9da213afad22.png",
    "woman_b_1": "https://d2ol7oe51mr4n9.cloudfront.net/user_36TmLGicluGODkcYejmrwLWoKV7/750f91fc-4ab5-4c37-acdd-8d11a77e1471.png",
    "woman_b_2": "https://d2ol7oe51mr4n9.cloudfront.net/user_36TmLGicluGODkcYejmrwLWoKV7/ba05bdb2-747f-4ae2-9d20-ccfccc1a3cce.png",
    "woman_b_3": "https://d2ol7oe51mr4n9.cloudfront.net/user_36TmLGicluGODkcYejmrwLWoKV7/5aeebf54-a7ad-42e7-94f8-4aba1344336f.png",
    "woman_b_4": "https://d2ol7oe51mr4n9.cloudfront.net/user_36TmLGicluGODkcYejmrwLWoKV7/1cfd3344-4cba-4ad8-b253-5f665c8c5ce5.png",
    "ico_bubble_1": "https://d2ol7oe51mr4n9.cloudfront.net/user_36TmLGicluGODkcYejmrwLWoKV7/6603859e-fd99-4853-b078-0fb3c31b7f3d.png",
    "ico_clock_1": "https://d2ol7oe51mr4n9.cloudfront.net/user_36TmLGicluGODkcYejmrwLWoKV7/7894457f-6b28-4883-a72f-8adb6cd177d7.png",
    "ico_glass_1": "https://d2ol7oe51mr4n9.cloudfront.net/user_36TmLGicluGODkcYejmrwLWoKV7/a4bdcbeb-1e3a-4798-bb95-cad65c952fe9.png",
    "ico_question_1": "https://d2ol7oe51mr4n9.cloudfront.net/user_36TmLGicluGODkcYejmrwLWoKV7/5e571fe6-86ce-4992-8ebe-76eb186d6db9.png",
    "ico_shoe_1": "https://d2ol7oe51mr4n9.cloudfront.net/user_36TmLGicluGODkcYejmrwLWoKV7/ab6835ee-d253-4536-866d-f16a5251bcc7.png",
}
IMG.update(KEYED)

# A project may add its own stills, cutouts and icons; the shared library above
# stays the same from film to film.
try:
    from plan import IMG_EXTRA as _IE                      # noqa: E402
    IMG.update(_IE)
except ImportError:
    pass

ALIAS = {
    "man_anx": ["man_anx_1", "man_anx_4", "man_anx_2", "man_anx_5",
                "man_anx_3", "man_anx_6", "man_anx_7"],
    "man_calm": ["man_calm_1", "man_calm_4", "man_calm_2", "man_calm_5",
                 "man_calm_3"],
    "man_think": ["man_think_1", "man_think_2"],
    "man_blur": ["man_blur_1"],
    "woman_a": ["woman_a_1", "woman_a_3", "woman_a_2"],
    "woman_b": ["woman_b_1", "woman_b_3", "woman_b_2", "woman_b_4"],
    "ico_bubble": ["ico_bubble_1"], "ico_clock": ["ico_clock_1"],
    "ico_glass": ["ico_glass_1"], "ico_question": ["ico_question_1"],
    "ico_shoe": ["ico_shoe_1"], "ico_question_x": ["ico_question_x_1"],
    "br_cafe_two": ["br_cafe_two_1", "br_cafe_two_2"],
    "br_friends": ["br_friends_1"], "br_phone": ["br_phone_1"],
    "br_silence_table": ["br_silence_table_1", "br_silence_table_2"],
    "br_listen": ["br_listen_1", "br_listen_2"],
    "br_counsel": ["br_counsel_1", "br_counsel_2"],
    "br_empty_chair": ["br_empty_chair_1"],
    "br_bench": ["br_bench_1", "br_bench_2"],
    "br_running": ["br_running_1"], "br_coffee": ["br_coffee_1"],
    "br_mirror": ["br_mirror_1"], "br_street": ["br_street_1"],
}
try:
    from plan import ALIAS_EXTRA as _AE                    # noqa: E402
    ALIAS.update(_AE)
except ImportError:
    pass

# neon diagrams are now drawn in SVG, so these map onto coded figures
NEON_FIG = {
    "neon_qmarks": "qmarks", "neon_loop": "loop4", "neon_branch": "branch",
    "neon_two_nodes": "twonodes", "neon_multitask": "panels",
    "neon_windows": "panels",
}
# figures added so no diagram carries more than two moments in the film
NEON_FIG.update({f"neon_{k}": k for k in (
    "surge", "meter", "repeatstrip", "dial", "bridge", "flow", "weave",
    "pendulum", "rally", "split", "twocheck", "cutoff", "tree", "fan",
    "lens", "queue", "countdown", "stretch", "elapsed", "plainchips",
    "asktoss", "askagain")})

# ── background rotation: eight families, never three alike in a row ─────────
FAMILIES = ["bg-canvas", "bg-ink", "bg-teal", "bg-grid",
            "bg-spot", "bg-ember", "bg-dust", "bg-canvas"]


def esc(s):
    return html.escape(s, quote=True)


_F = {}


def font(px, weight="SemiBold"):
    key = (px, weight)
    if key not in _F:
        _F[key] = ImageFont.truetype(
            os.path.join(HERE, "..", "assets", "fonts", f"Pretendard-{weight}.otf"), px)
    return _F[key]


def text_w(t, f):
    l, tp, r, b = ImageDraw.Draw(Image.new("L", (1, 1))).textbbox((0, 0), t, font=f)
    return r - l


def caption_cards(line):
    """Break one narration line into cards that each fit on a single line."""
    f = font(CAP_PX)
    if text_w(line, f) <= CAP_MAX:
        return [line]
    # prefer clause boundaries, then plain spaces
    parts, buf = [], ""
    tokens = re.split(r"(?<=[.?!,])\s+", line)
    flat = []
    for t in tokens:
        flat.extend([t] if text_w(t, f) <= CAP_MAX else t.split(" "))
    for tok in flat:
        trial = (buf + " " + tok).strip()
        if buf and text_w(trial, f) > CAP_MAX:
            parts.append(buf)
            buf = tok
        else:
            buf = trial
    if buf:
        parts.append(buf)
    # last resort: hard-cut anything still too wide
    out = []
    for p in parts:
        while text_w(p, f) > CAP_MAX and len(p) > 1:
            cut = len(p)
            while cut > 1 and text_w(p[:cut], f) > CAP_MAX:
                cut -= 1
            out.append(p[:cut])
            p = p[cut:].strip()
        if p:
            out.append(p)
    return out or [line]


def motes(seed, n=46):
    """Deterministic dust field for bg-dust."""
    s, out = seed * 7919 + 13, []
    for _ in range(n):
        s = (s * 1103515245 + 12345) & 0x7FFFFFFF
        x = (s >> 7) % 1000 / 10.0
        s = (s * 1103515245 + 12345) & 0x7FFFFFFF
        y = (s >> 7) % 1000 / 10.0
        s = (s * 1103515245 + 12345) & 0x7FFFFFFF
        r = 1.2 + (s >> 9) % 26 / 10.0
        s = (s * 1103515245 + 12345) & 0x7FFFFFFF
        o = 0.12 + (s >> 11) % 40 / 100.0
        out.append(f'<i class="mote" style="left:{x:.1f}%;top:{y:.1f}%;'
                   f'width:{r:.1f}px;height:{r:.1f}px;opacity:{o:.2f}"></i>')
    return "".join(out)
