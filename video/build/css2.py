# -*- coding: utf-8 -*-
FONTS="".join(
 f'@font-face{{font-family:Pretendard;src:url(assets/fonts/Pretendard-{n}.otf)format("opentype");'
 f'font-weight:{w};font-display:block}}'
 for n,w in [("Regular",400),("Medium",500),("SemiBold",600),("Bold",700),("ExtraBold",800),("Black",900)])

# backgrounds: charcoal base + a directional bloom, rotated so no family repeats 3x
BG={
 "charcoal":("#0b0c0e","radial-gradient(120% 92% at 50% 20%, rgba(150,162,178,.15), rgba(0,0,0,0) 62%)"),
 "blue":    ("#090d13","radial-gradient(112% 88% at 28% 26%, rgba(62,128,205,.28), rgba(0,0,0,0) 60%)"),
 "ember":   ("#110b0a","radial-gradient(116% 90% at 72% 26%, rgba(199,88,58,.26), rgba(0,0,0,0) 62%)"),
 "teal":    ("#07100f","radial-gradient(114% 88% at 32% 70%, rgba(48,160,158,.26), rgba(0,0,0,0) 60%)"),
 "violet":  ("#0c0a13","radial-gradient(114% 88% at 68% 68%, rgba(122,88,200,.26), rgba(0,0,0,0) 60%)"),
 "slate":   ("#0a0e0e","radial-gradient(118% 92% at 50% 78%, rgba(92,126,118,.22), rgba(0,0,0,0) 62%)"),
 "photo":   ("#08090a","radial-gradient(120% 92% at 50% 45%, rgba(120,124,132,.10), rgba(0,0,0,0) 66%)"),
}
CY="#4FC3E8"; AM="#E8C46A"; PK="#EF5F8C"; GR="#59C2A0"

CSS=FONTS+"""
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1920px;height:1080px;overflow:hidden;background:#08090a}
#root{width:100%;height:100%;position:relative;font-family:Pretendard,sans-serif;color:#f2f4f7;
 -webkit-font-smoothing:antialiased;overflow:hidden}
.bg{position:absolute;inset:0;z-index:0}
.bg i{position:absolute;inset:0;display:block}
.vig{position:absolute;inset:0;z-index:8;pointer-events:none;
 background:radial-gradient(134% 104% at 50% 50%, rgba(0,0,0,0) 56%, rgba(0,0,0,.50) 100%)}
.grain{position:absolute;inset:-80px;z-index:42;pointer-events:none;opacity:.13;mix-blend-mode:overlay;
 background-repeat:repeat;background-size:320px 320px;will-change:transform}
.scene{position:absolute;inset:0;z-index:10;display:flex;align-items:center;justify-content:center}
.stage{position:relative;z-index:12;width:1560px;min-height:640px;display:flex;flex-direction:column;align-items:center;
 justify-content:center;gap:32px;transform:translateY(-38px)}

/* photography: bright enough to read, one scrim only */
.photo.dim{filter:saturate(.62) contrast(1.03) brightness(.95)}
.scrim.heavy{background:linear-gradient(180deg,rgba(6,7,9,.66) 0%,rgba(6,7,9,.56) 45%,rgba(6,7,9,.78) 100%)}
.photo{position:absolute;inset:0;z-index:1;background-size:cover;background-position:center;
 filter:saturate(.78) contrast(1.04) brightness(1.06)}
.scrim{position:absolute;inset:0;z-index:5;
 background:linear-gradient(180deg,rgba(6,7,9,.52) 0%,rgba(6,7,9,.30) 42%,rgba(6,7,9,.74) 100%)}

/* typography */
.kicker{font-size:29px;font-weight:600;letter-spacing:.02em;color:#96a0ad}
.h-xl{font-size:126px;font-weight:800;letter-spacing:-.035em;line-height:1.1;text-align:center;white-space:nowrap}
.h-lg{font-size:92px;font-weight:800;letter-spacing:-.03em;line-height:1.16;text-align:center;white-space:nowrap}
.h-md{font-size:60px;font-weight:700;letter-spacing:-.02em;line-height:1.22;text-align:center}
.h-sm{font-size:44px;font-weight:600;letter-spacing:-.01em;line-height:1.32;text-align:center}
.muted{color:#939dab}

/* subtitle: one line, white + thin black stroke */
#subs{position:absolute;left:0;right:0;bottom:62px;z-index:60;height:62px;
 display:flex;align-items:center;justify-content:center;pointer-events:none}
.sub{position:absolute;white-space:nowrap;font-size:43px;font-weight:600;letter-spacing:-.01em;
 color:#fff;-webkit-text-stroke:5px rgba(0,0,0,.92);paint-order:stroke fill;
 text-shadow:0 2px 16px rgba(0,0,0,.5)}
#mark{position:absolute;top:32px;right:42px;z-index:62;font-size:21px;font-weight:600;
 color:rgba(236,239,243,.72)}

/* cut-out media */
.cut{display:block;object-fit:contain;filter:drop-shadow(0 26px 46px rgba(0,0,0,.6))}
.i3d{display:block;object-fit:contain;filter:drop-shadow(0 22px 42px rgba(0,0,0,.62))}
.pcard{filter:url(#torn) drop-shadow(0 30px 52px rgba(0,0,0,.62))}
.paper{display:block;object-fit:contain}

/* rows */
.rows{display:flex;flex-direction:column;gap:24px;align-items:flex-start}
.row{display:flex;align-items:center;gap:24px;font-size:44px;font-weight:600;letter-spacing:-.01em}
.mk{flex:0 0 auto;width:30px;display:flex;align-items:center;justify-content:center}
.mkdot{width:15px;height:15px;border-radius:50%;background:""" + CY + """;display:block}
.mkq{font-size:32px;font-weight:800;color:""" + CY + """}
.mkm{width:26px;height:6px;border-radius:3px;background:""" + PK + """;display:block}
.mkp{width:26px;height:26px;display:block;position:relative}
.mkp::before,.mkp::after{content:"";position:absolute;background:""" + GR + """;border-radius:3px}
.mkp::before{left:0;right:0;top:10px;height:6px}
.mkp::after{top:0;bottom:0;left:10px;width:6px}
.mkc{width:28px;height:28px;border-radius:50%;border:3px solid """ + GR + """;display:block;position:relative}
.mkc::after{content:"";position:absolute;left:6px;top:11px;width:11px;height:5px;
 border-left:4px solid """ + GR + """;border-bottom:4px solid """ + GR + """;transform:rotate(-45deg)}
.stepn{flex:0 0 auto;width:50px;height:50px;border-radius:50%;border:3px solid rgba(255,255,255,.3);
 display:flex;align-items:center;justify-content:center;font-size:26px;font-weight:700}

/* chips (reference motif) */
.chips{display:flex;gap:20px;flex-wrap:nowrap;justify-content:center}
.chip{padding:16px 34px;border-radius:999px;font-size:38px;font-weight:600;
 border:2px solid rgba(255,255,255,.22);background:rgba(255,255,255,.06);white-space:nowrap}
.chip.on{border-color:""" + AM + """;background:rgba(232,196,106,.16);color:#f3dfb0}

/* amber quote bubbles (reference motif) */
.bubs{display:flex;flex-direction:column;gap:20px;width:1240px}
.bwrap{position:relative;display:flex;flex-direction:column;gap:6px}
.btag{font-size:24px;font-weight:600;color:#8b95a3}
.bub{padding:24px 34px;border-radius:26px;font-size:42px;font-weight:600;line-height:1.34;
 position:relative;max-width:1100px}
.bub.say{align-self:flex-start;background:""" + AM + """;color:#1a1408;border-bottom-left-radius:8px}
.bub.her{align-self:flex-end;background:rgba(78,90,110,.94);color:#f2f4f8;border-bottom-right-radius:8px}
.bub.thought{align-self:center;background:rgba(255,255,255,.07);color:#e9ecf1;
 border:2px dashed rgba(255,255,255,.28);border-radius:32px}
.bub.dense{font-size:36px;padding:18px 28px}
.bubx{position:absolute;right:-28px;top:50%;margin-top:-24px}
.okdot{width:50px;height:50px;border-radius:50%;background:rgba(89,194,160,.16);
 border:3px solid """ + GR + """;position:relative}
.okdot::after{content:"";position:absolute;left:14px;top:22px;width:18px;height:8px;
 border-left:5px solid """ + GR + """;border-bottom:5px solid """ + GR + """;transform:rotate(-45deg)}
.side{display:flex;align-items:center;gap:56px;justify-content:center}
.side>*{flex:0 0 auto}
.side .bubs{width:860px}
.sideimg{width:300px;height:380px}

/* bars: length + grade dots + ticks + axis */
.bars{width:1240px;display:flex;flex-direction:column;gap:36px}
.barrow{display:flex;flex-direction:column;gap:12px}
.barhead{display:flex;align-items:center;justify-content:space-between}
.barlab{font-size:38px;font-weight:600}
.dots{display:flex;gap:9px}
.dot{width:15px;height:15px;border-radius:50%;background:rgba(255,255,255,.2);display:block}
.dot.on{background:currentColor}
.track{position:relative;height:30px;border-radius:15px;background:rgba(255,255,255,.09)}
.fill{position:absolute;left:0;top:0;bottom:0;border-radius:15px}
.ticks{position:absolute;inset:0;display:flex}
.tick{flex:1;border-right:2px solid rgba(255,255,255,.13);display:block}
.tick:last-child{border-right:none}
.axis{display:flex;justify-content:space-between;font-size:25px;color:#8b95a3;font-weight:500}

/* gauge */
.gauge{width:1160px;display:flex;flex-direction:column;gap:16px}
.gtrack{position:relative;height:28px;border-radius:14px;background:rgba(255,255,255,.09)}
.gfill{position:absolute;left:0;top:0;bottom:0;border-radius:14px;
 background:linear-gradient(90deg,""" + CY + """,""" + PK + """)}
.gscale{position:absolute;inset:0;display:flex}
.gscale i{flex:1;border-right:2px solid rgba(255,255,255,.15);display:block}
.gscale i:last-child{border-right:none}
.gknob{position:absolute;top:50%;left:0;width:36px;height:36px;border-radius:50%;background:#fff;
 box-shadow:0 0 0 8px rgba(239,95,140,.2),0 10px 22px rgba(0,0,0,.5)}

/* compare / split */
.cmp{display:flex;gap:72px;align-items:stretch;justify-content:center;width:1420px}
.col{flex:1;display:flex;flex-direction:column;align-items:center;gap:20px;text-align:center}
.colt{font-size:46px;font-weight:700;letter-spacing:-.02em;line-height:1.24}
.cols{font-size:26px;color:#8b95a3;font-weight:500}
.meter{width:100%;height:20px;border-radius:10px;background:rgba(255,255,255,.09);position:relative}
.meterf{position:absolute;left:0;top:0;bottom:0;border-radius:10px}
.divider{width:2px;background:linear-gradient(180deg,rgba(255,255,255,0),rgba(255,255,255,.18),rgba(255,255,255,0))}

/* strike */
.strikewrap{position:relative;display:inline-block;padding:8px 22px}
.strikeline{position:absolute;left:0;right:0;top:50%;height:8px;border-radius:4px;transform-origin:left center}
.xmark{position:absolute;right:-88px;top:50%;width:66px;height:66px;margin-top:-33px}
.xmark-s{margin-top:4px}

/* chapter / quote / cta */
.chapnum{font-size:170px;font-weight:900;letter-spacing:-.05em;color:rgba(255,255,255,.13);line-height:.9}
.qmark{font-size:140px;font-weight:900;line-height:.6;color:rgba(255,255,255,.16)}
.hero-ic{display:flex;align-items:center;justify-content:center}

/* scale */
.scale{position:relative;width:1140px;height:280px;display:flex;align-items:center;justify-content:center}
.beam{position:relative;width:980px;height:190px}
.beam::before{content:"";position:absolute;left:0;right:0;top:50%;height:7px;border-radius:4px;
 background:rgba(255,255,255,.32)}
.pan{position:absolute;top:50%;width:370px;padding:20px 24px;border-radius:20px;text-align:center;
 font-size:34px;font-weight:700;line-height:1.26}
.pan.up{left:0;margin-top:-132px;background:rgba(122,88,200,.22);border:2px solid rgba(160,130,230,.5)}
.pan.down{right:0;margin-top:18px;background:rgba(239,95,140,.18);border:2px solid rgba(239,95,140,.5)}
.fulcrum{position:absolute;bottom:14px;width:0;height:0;border-left:32px solid transparent;
 border-right:32px solid transparent;border-bottom:66px solid rgba(255,255,255,.2)}

/* venn / mutual / grow */
.venn{position:relative;width:1060px;height:400px;display:flex;align-items:center;justify-content:center}
.vc{position:absolute;width:420px;height:420px;border-radius:50%;display:flex;align-items:center;
 justify-content:center;font-size:42px;font-weight:700}
.vc.a{left:120px;border:3px solid rgba(79,195,232,.7);background:rgba(79,195,232,.10)}
.vc.a span{transform:translateX(-92px)}
.vc.b{right:120px;border:3px solid rgba(232,196,106,.7);background:rgba(232,196,106,.10)}
.vc.b span{transform:translateX(92px)}
.vmid{position:relative;z-index:3;width:320px;text-align:center;font-size:33px;font-weight:700;line-height:1.3}
.mutual{display:flex;align-items:center;justify-content:center;gap:52px}
.mnode{padding:26px 52px;border-radius:22px;font-size:46px;font-weight:700;
 border:2px solid rgba(255,255,255,.26);background:rgba(255,255,255,.06)}
.marrows{display:flex;flex-direction:column;gap:18px;width:190px}
.ar{display:block;height:5px;border-radius:3px;background:rgba(255,255,255,.5);position:relative}
.ar::after{content:"";position:absolute;top:50%;width:17px;height:17px;margin-top:-9px;
 border-top:5px solid rgba(255,255,255,.5);border-right:5px solid rgba(255,255,255,.5)}
.ar.r::after{right:0;transform:rotate(45deg)}
.ar.l::after{left:0;transform:rotate(-135deg)}
.grow{display:flex;gap:200px;align-items:center;justify-content:center}
.gcell{display:flex;flex-direction:column;align-items:center;gap:22px;width:320px}
.gsmall{width:68px;height:68px;border-radius:50%;background:rgba(139,149,163,.5);
 box-shadow:0 0 0 2px rgba(255,255,255,.18)}
.gbig{width:238px;height:238px;border-radius:50%;background:rgba(239,95,140,.28);
 box-shadow:0 0 0 2px rgba(239,95,140,.6)}
.glab{font-size:30px;font-weight:600;color:#c3cad4;text-align:center}
.bub.before{opacity:.5}
.bub.after{box-shadow:0 0 0 3px rgba(89,194,160,.55)}
"""
