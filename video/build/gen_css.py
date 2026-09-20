# -*- coding: utf-8 -*-
FONT_FACE = """
@font-face{font-family:Pretendard;src:url(assets/fonts/Pretendard-Regular.otf)format("opentype");font-weight:400;font-display:block}
@font-face{font-family:Pretendard;src:url(assets/fonts/Pretendard-Medium.otf)format("opentype");font-weight:500;font-display:block}
@font-face{font-family:Pretendard;src:url(assets/fonts/Pretendard-SemiBold.otf)format("opentype");font-weight:600;font-display:block}
@font-face{font-family:Pretendard;src:url(assets/fonts/Pretendard-Bold.otf)format("opentype");font-weight:700;font-display:block}
@font-face{font-family:Pretendard;src:url(assets/fonts/Pretendard-ExtraBold.otf)format("opentype");font-weight:800;font-display:block}
@font-face{font-family:Pretendard;src:url(assets/fonts/Pretendard-Black.otf)format("opentype");font-weight:900;font-display:block}
"""

# background families: base charcoal + a directional colour bloom. Rotated so no family repeats 3x.
BG = {
 "charcoal": ("#0c0d0f", "radial-gradient(120% 90% at 50% 18%, rgba(150,160,175,.16), rgba(0,0,0,0) 62%)"),
 "blue":     ("#0a0d12", "radial-gradient(110% 85% at 26% 24%, rgba(64,124,196,.26), rgba(0,0,0,0) 60%)"),
 "ember":    ("#100b0a", "radial-gradient(115% 88% at 74% 26%, rgba(196,86,58,.24), rgba(0,0,0,0) 62%)"),
 "teal":     ("#080f10", "radial-gradient(112% 86% at 32% 72%, rgba(46,150,148,.24), rgba(0,0,0,0) 60%)"),
 "violet":   ("#0c0a12", "radial-gradient(112% 86% at 68% 70%, rgba(124,86,196,.24), rgba(0,0,0,0) 60%)"),
 "slate":    ("#0b0e0d", "radial-gradient(118% 90% at 50% 80%, rgba(96,124,110,.20), rgba(0,0,0,0) 62%)"),
 "photo_cafe":("#0a0a0b","radial-gradient(120% 90% at 50% 40%, rgba(120,120,130,.12), rgba(0,0,0,0) 65%)"),
}

CSS = FONT_FACE + """
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1920px;height:1080px;overflow:hidden;background:#0a0a0b}
#root{width:100%;height:100%;position:relative;font-family:Pretendard,sans-serif;
  color:#f2f3f5;-webkit-font-smoothing:antialiased;overflow:hidden}

/* ---- background layers ---- */
.bg{position:absolute;inset:0;z-index:0}
.bg .base{position:absolute;inset:0}
.bg .bloom{position:absolute;inset:0}
.vig{position:absolute;inset:0;z-index:40;pointer-events:none;
  background:radial-gradient(130% 100% at 50% 50%, rgba(0,0,0,0) 46%, rgba(0,0,0,.62) 100%)}
/* deterministic film grain: fixed-seed turbulence tile, stepped offsets on the timeline */
.grain{position:absolute;inset:-80px;z-index:41;pointer-events:none;opacity:.14;mix-blend-mode:overlay;
  background-repeat:repeat;background-size:320px 320px;will-change:transform}

/* ---- stage: everything is centred both axes ---- */
.scene{position:absolute;inset:0;z-index:10;display:flex;align-items:center;justify-content:center}
.stage{width:1560px;height:720px;margin:0 auto;display:flex;flex-direction:column;
  align-items:center;justify-content:center;gap:34px;transform:translateY(-44px)}

/* ---- typography ---- */
.kicker{font-size:30px;font-weight:600;letter-spacing:.02em;color:#9aa3b0;text-transform:none}
.h-xl{font-size:132px;font-weight:800;letter-spacing:-.035em;line-height:1.08;text-align:center}
.h-lg{font-size:96px;font-weight:800;letter-spacing:-.03em;line-height:1.14;text-align:center}
.h-md{font-size:64px;font-weight:700;letter-spacing:-.02em;line-height:1.2;text-align:center}
.h-sm{font-size:46px;font-weight:600;letter-spacing:-.01em;line-height:1.3;text-align:center}
.muted{color:#98a1ad}
.accent{color:#e8b46a}
.pink{color:#ef5f8c}
.good{color:#59c2a0}

/* ---- subtitle: ALWAYS one line, white + thin black stroke ---- */
#subs{position:absolute;left:0;right:0;bottom:64px;z-index:60;height:64px;
  display:flex;align-items:center;justify-content:center;pointer-events:none}
.sub{position:absolute;white-space:nowrap;font-size:44px;font-weight:600;letter-spacing:-.01em;
  color:#ffffff;-webkit-text-stroke:5px rgba(0,0,0,.92);paint-order:stroke fill;
  text-shadow:0 2px 18px rgba(0,0,0,.55)}

/* ---- watermark ---- */
#mark{position:absolute;top:34px;right:44px;z-index:62;font-size:22px;font-weight:600;
  color:rgba(233,236,240,.40);letter-spacing:.02em}

/* ---- scrim for text over photography (WCAG AA) ---- */
.scrim{position:absolute;inset:0;z-index:5;
  background:linear-gradient(180deg,rgba(6,7,9,.58) 0%,rgba(6,7,9,.30) 38%,rgba(6,7,9,.72) 100%)}
.photo{position:absolute;inset:0;z-index:1;background-size:cover;background-position:center;
  filter:saturate(.72) contrast(1.02)}

/* ---- cutout media (no background plates) ---- */
.cut{display:block;object-fit:contain;filter:drop-shadow(0 26px 44px rgba(0,0,0,.55))}
.paper{display:block;object-fit:contain}

/* ---- list rows ---- */
.rows{display:flex;flex-direction:column;gap:26px;align-items:flex-start}
.row{display:flex;align-items:center;gap:26px;font-size:46px;font-weight:600;letter-spacing:-.01em}
.mk{flex:0 0 auto;width:34px;height:34px;display:flex;align-items:center;justify-content:center}

/* ---- bars: length + grade dots + ticks + axis labels ---- */
.bars{width:1260px;display:flex;flex-direction:column;gap:40px}
.barrow{display:flex;flex-direction:column;gap:14px}
.barhead{display:flex;align-items:center;justify-content:space-between}
.barlab{font-size:40px;font-weight:600}
.dots{display:flex;gap:10px}
.dot{width:16px;height:16px;border-radius:50%;background:rgba(255,255,255,.22)}
.dot.on{background:currentColor}
.track{position:relative;height:34px;border-radius:17px;background:rgba(255,255,255,.10);overflow:visible}
.fill{position:absolute;left:0;top:0;bottom:0;border-radius:17px}
.ticks{position:absolute;inset:0;display:flex}
.tick{flex:1;border-right:2px solid rgba(255,255,255,.14)}
.tick:last-child{border-right:none}
.axis{display:flex;justify-content:space-between;font-size:26px;color:#8d96a3;font-weight:500}

/* ---- gauge ---- */
.gauge{width:1180px;display:flex;flex-direction:column;gap:18px}
.gtrack{position:relative;height:30px;border-radius:15px;background:rgba(255,255,255,.10)}
.gfill{position:absolute;left:0;top:0;bottom:0;border-radius:15px;background:linear-gradient(90deg,#e8b46a,#ef5f8c)}
.gscale{position:absolute;inset:0;display:flex}
.gscale i{flex:1;border-right:2px solid rgba(255,255,255,.16);display:block}
.gscale i:last-child{border-right:none}
.gknob{position:absolute;top:50%;left:0;width:38px;height:38px;border-radius:50%;background:#fff;
  box-shadow:0 0 0 8px rgba(239,95,140,.22),0 10px 22px rgba(0,0,0,.5)}

/* ---- compare / split ---- */
.cmp{display:flex;gap:80px;align-items:stretch;justify-content:center;width:1420px}
.col{flex:1;display:flex;flex-direction:column;align-items:center;gap:22px;text-align:center}
.colt{font-size:48px;font-weight:700;letter-spacing:-.02em;line-height:1.24}
.cols{font-size:28px;color:#8d96a3;font-weight:500}
.meter{width:100%;height:22px;border-radius:11px;background:rgba(255,255,255,.10);position:relative}
.meterf{position:absolute;left:0;top:0;bottom:0;border-radius:11px}
.divider{width:2px;background:linear-gradient(180deg,rgba(255,255,255,0),rgba(255,255,255,.18),rgba(255,255,255,0))}

/* ---- bubbles ---- */
.bubs{display:flex;flex-direction:column;gap:22px;width:1280px}
.bub{max-width:1100px;padding:26px 38px;border-radius:30px;font-size:44px;font-weight:600;
  letter-spacing:-.01em;line-height:1.34;position:relative}
.bub.say{align-self:flex-start;background:rgba(236,240,246,.94);color:#14161a;border-bottom-left-radius:10px}
.bub.her{align-self:flex-end;background:rgba(72,84,104,.92);color:#f2f4f8;border-bottom-right-radius:10px}
.bub.thought{align-self:center;background:rgba(255,255,255,.08);color:#e9ecf1;
  border:2px dashed rgba(255,255,255,.26);border-radius:34px}
.bub.dense{font-size:38px;padding:20px 32px}
.bub .xout{position:absolute;inset:0;pointer-events:none}

/* ---- strike ---- */
.strikewrap{position:relative;display:inline-block;padding:10px 24px}
.strikeline{position:absolute;left:0;right:0;top:50%;height:8px;border-radius:4px;background:#ef5f8c;
  transform-origin:left center}
.xmark{position:absolute;right:-96px;top:50%;width:72px;height:72px;margin-top:-36px}

/* ---- chapter ---- */
.chapnum{font-size:180px;font-weight:900;letter-spacing:-.05em;color:rgba(255,255,255,.12);line-height:.9}
"""

CSS += """
/* ---- hero bits ---- */
.hero-ic{color:#e9ecf1;opacity:.92}
.ring{position:absolute;width:420px;height:420px;border-radius:50%;
  border:2px solid rgba(255,255,255,.14);pointer-events:none}
.qmark{font-size:150px;font-weight:900;line-height:.6;color:rgba(255,255,255,.16)}

/* ---- list marks ---- */
.mkdot{width:16px;height:16px;border-radius:50%;background:#e8b46a;display:block}
.mkq{font-size:34px;font-weight:800;color:#6fa8dc}
.mkm{width:28px;height:6px;border-radius:3px;background:#ef5f8c;display:block}
.mkp{width:28px;height:28px;display:block;position:relative}
.mkp::before,.mkp::after{content:"";position:absolute;background:#59c2a0;border-radius:3px}
.mkp::before{left:0;right:0;top:11px;height:6px}
.mkp::after{top:0;bottom:0;left:11px;width:6px}
.stepn{flex:0 0 auto;width:52px;height:52px;border-radius:50%;border:3px solid rgba(255,255,255,.28);
  display:flex;align-items:center;justify-content:center;font-size:28px;font-weight:700;color:#e9ecf1}

/* ---- icon rows ---- */
.icons{display:flex;gap:110px;align-items:flex-start;justify-content:center}
.icons.grid4{gap:86px}
.icell{display:flex;flex-direction:column;align-items:center;gap:20px;color:#e9ecf1;width:230px}
.ilab{font-size:34px;font-weight:600;color:#c7cdd6;text-align:center;line-height:1.25}

/* ---- bubble extras ---- */
.bubx{position:absolute;right:-30px;top:50%;margin-top:-26px}
.okdot{width:54px;height:54px;border-radius:50%;background:rgba(89,194,160,.16);
  border:3px solid #59c2a0;position:relative}
.okdot::after{content:"";position:absolute;left:15px;top:24px;width:20px;height:9px;
  border-left:5px solid #59c2a0;border-bottom:5px solid #59c2a0;transform:rotate(-45deg)}
.bub.before{opacity:.55}
.bub.after{box-shadow:0 0 0 3px rgba(89,194,160,.55)}

/* ---- portrait paper card ---- */
.pcard{filter:url(#torn) drop-shadow(0 30px 50px rgba(0,0,0,.6))}
.xmark-s{margin-top:6px}

/* ---- balance scale ---- */
.scale{position:relative;width:1180px;height:300px;display:flex;align-items:center;justify-content:center}
.beam{position:relative;width:1000px;height:200px;transform:rotate(-7deg)}
.beam::before{content:"";position:absolute;left:0;right:0;top:50%;height:8px;border-radius:4px;
  background:rgba(255,255,255,.35)}
.pan{position:absolute;top:50%;width:380px;padding:22px 26px;border-radius:22px;text-align:center;
  font-size:36px;font-weight:700;line-height:1.28;transform:rotate(7deg)}
.pan.up{left:0;margin-top:-140px;background:rgba(124,86,196,.22);border:2px solid rgba(160,130,230,.5)}
.pan.down{right:0;margin-top:20px;background:rgba(239,95,140,.18);border:2px solid rgba(239,95,140,.5)}
.fulcrum{position:absolute;bottom:18px;width:0;height:0;border-left:34px solid transparent;
  border-right:34px solid transparent;border-bottom:70px solid rgba(255,255,255,.22)}

/* ---- venn ---- */
.venn{position:relative;width:1080px;height:420px;display:flex;align-items:center;justify-content:center}
.vc{position:absolute;width:440px;height:440px;border-radius:50%;display:flex;align-items:center;
  justify-content:center;font-size:44px;font-weight:700}
.vc.a{left:120px;border:3px solid rgba(110,168,220,.7);background:rgba(110,168,220,.10)}
.vc.a span{transform:translateX(-96px)}
.vc.b{right:120px;border:3px solid rgba(232,180,106,.7);background:rgba(232,180,106,.10)}
.vc.b span{transform:translateX(96px)}
.vmid{position:relative;z-index:3;width:330px;text-align:center;font-size:34px;font-weight:700;
  line-height:1.3;color:#fff}

/* ---- mutual ---- */
.mutual{display:flex;align-items:center;justify-content:center;gap:56px}
.mnode{padding:28px 56px;border-radius:24px;font-size:48px;font-weight:700;
  border:2px solid rgba(255,255,255,.26);background:rgba(255,255,255,.06)}
.mutual.glow .mnode{border-color:rgba(89,194,160,.7);box-shadow:0 0 34px rgba(89,194,160,.20)}
.marrows{display:flex;flex-direction:column;gap:20px;width:200px}
.ar{display:block;height:5px;border-radius:3px;background:rgba(255,255,255,.5);position:relative}
.ar::after{content:"";position:absolute;top:50%;width:18px;height:18px;margin-top:-9px;
  border-top:5px solid rgba(255,255,255,.5);border-right:5px solid rgba(255,255,255,.5)}
.ar.r::after{right:0;transform:rotate(45deg)}
.ar.l::after{left:0;transform:rotate(-135deg)}

/* ---- grow dots (size = magnitude, with scale ring) ---- */
.grow{display:flex;gap:220px;align-items:center;justify-content:center}
.gcell{display:flex;flex-direction:column;align-items:center;gap:26px;width:340px}
.gsmall{width:72px;height:72px;border-radius:50%;background:rgba(141,150,163,.5);
  box-shadow:0 0 0 2px rgba(255,255,255,.18)}
.gbig{width:248px;height:248px;border-radius:50%;background:rgba(239,95,140,.30);
  box-shadow:0 0 0 2px rgba(239,95,140,.6)}
.glab{font-size:32px;font-weight:600;color:#c7cdd6;text-align:center}

/* ---- path ---- */
.pathwrap{display:flex;gap:90px;align-items:center;justify-content:center}
.pnode{padding:30px 54px;border-radius:24px;font-size:46px;font-weight:700;
  border:2px solid rgba(255,255,255,.22)}
.pnode.dim{opacity:.42}
.pnode.pick{border-color:rgba(232,180,106,.8);background:rgba(232,180,106,.12);color:#f3d6a6}
"""
