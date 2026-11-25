"""Resolve a scene plan into timeline.json for the page template.
usage: python3 -I build_timeline.py <chunks.json> <scenes.py> <timeline.json> [memes_dir]

scenes.py defines:
  SCENES = [ (anchor, scene_dict), ... ]   # in order; a scene starts when the first chunk at/after the
                                            # previous scene whose text STARTS WITH anchor begins
  TITLE  = {"t1": "...", "t2": "...", "end": "@anchor"}   # optional opening title caption
Inside scene dicts any string "@text" becomes the start time of the first chunk (from this scene on)
starting with text. Matching ignores spaces/quotes/punctuation. Use ["@text", n] style only via
the helper nth("@text", n) when the same line repeats inside one scene's range.
Helpers available in scenes.py: meme, text, icons, kakao, card, cta (9:16 dark), and the generic
dict builders big, vs, chap for the 16:9 template (see SKILL.md)."""
import json, re, sys, os
from PIL import Image

cp, scp, outp = sys.argv[1:4]
MEMES = sys.argv[4] if len(sys.argv) > 4 else os.path.join(os.path.dirname(os.path.abspath(scp)), "memes")
D = json.load(open(cp)); CH = D["chunks"]
norm = lambda s: re.sub(r"[\s\"'“”‘’.,?!·…~]", "", s)
NC = [norm(c["t"]) for c in CH]

def find(anchor, frm, n=1):
    a = norm(anchor)
    for i in range(frm, len(CH)):
        if NC[i].startswith(a):
            n -= 1
            if n == 0: return i
    raise SystemExit(f"anchor not found after chunk {frm}: {anchor!r}")

# ---- helpers for scenes.py
MAXW, MAXH = 820, 540          # 9:16 default; 16:9 scenes.py sets MAXW, MAXH = 1100, 540
def meme(img, cap="", ov=None):
    w, h = Image.open(os.path.join(MEMES, img + ".jpg")).size
    k = min(G["MAXW"] / w, G["MAXH"] / h)
    d = {"type": "meme", "img": img, "cap": cap, "w": round(w * k), "h": round(h * k)}
    if ov: d["ov"] = ov        # [[x%, y%, w%, "text<br>text", fontpx], ...] text drawn on the image
    return d
def text(): return {"type": "text"}
def icons(*ev): return {"type": "icons", "ev": list(ev)}       # (at|None, "w"/"m", text|None|"", append0/1, mood)
def kakao(*ev): return {"type": "kakao", "ev": list(ev)}       # (at|None, "in"/"out", text)
def card(emoji, cap, bg=("#3a2a4a", "#151020")): return {"type": "card", "emoji": emoji, "cap": cap, "bg": list(bg)}
def cta(pill=None, sub=None):
    d = {"type": "cta"}
    if pill is not None: d["pill"] = pill
    if sub is not None: d["sub"] = sub                            # "" hides the line under the pill
    return d
def big(t, t2=None, at2=None, s=None): return {"type": "big", "t": t, "t2": t2, "at2": at2, "s": s}
def vs(a, b, ata=None, atb=None, mid=None, title=None, hotb=True):
    return {"type": "vs", "a": a, "b": b, "ata": ata, "atb": atb, "mid": mid, "title": title, "hotb": hotb}
def chap(n, t): return {"type": "chapter", "n": n, "t": t}
class nth:                                                       # nth("@그런데", 2)
    def __init__(self, a, n): self.a, self.n = a, n

G = dict(meme=meme, text=text, icons=icons, kakao=kakao, card=card, cta=cta, big=big, vs=vs, chap=chap, nth=nth,
         MAXW=MAXW, MAXH=MAXH)
exec(open(scp, encoding="utf-8").read(), G)

def resolve(x, base):
    if isinstance(x, nth): return CH[find(x.a.lstrip("@"), base, x.n)]["s"]
    if isinstance(x, str) and x.startswith("@"): return CH[find(x[1:], base)]["s"]
    if isinstance(x, (list, tuple)): return [resolve(v, base) for v in x]
    if isinstance(x, dict): return {k: resolve(v, base) for k, v in x.items()}
    return x

cur, scenes = 0, []
for item in G["SCENES"]:
    anchor, d = item[0], item[1]
    n = item[2] if len(item) > 2 else 1
    i = find(anchor, cur, n); cur = i
    sc = resolve(d, i); sc["start"] = 0.0 if not scenes else CH[i]["s"]
    if "ev" in sc:  # None in events = scene start
        sc["ev"] = [[sc["start"] if e[0] is None else max(e[0], sc["start"])] + list(e[1:]) for e in sc["ev"]]
    scenes.append(sc)
out = {"dur": D["dur"], "chunks": CH, "scenes": scenes,
       "chapters": [{"n": c["ch"]["n"], "t": c["ch"]["t"], "s": c["s"]} for c in CH if c.get("ch")]}
if G.get("TITLE"): out["title"] = resolve(G["TITLE"], 0)
json.dump(out, open(outp, "w"), ensure_ascii=False)
print(len(scenes), "scenes")
for a, b in zip(scenes, scenes[1:]):
    if b["start"] - a["start"] < 1.0: print(f"  short scene {a['type']} @{a['start']:.2f} ({b['start'] - a['start']:.2f}s)")
