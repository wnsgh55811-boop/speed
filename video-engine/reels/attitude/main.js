// ================= core =================
const DUR = 67.94, FPS = 30;
const stage = document.getElementById('stage');
const tl = gsap.timeline({paused: true});
const procs = [];
const SFX = [];
const T = i => LINES[i].s;
const sfx = (t, type, vol = 1) => SFX.push({t, type, vol});

function h(html){ const t=document.createElement('template'); t.innerHTML=html.trim(); return t.content.firstElementChild; }
function add(p, html, x, y, css){
  const e = typeof html==='string' ? h(html) : html; p.appendChild(e);
  if (x!=null){ e.style.position='absolute'; e.style.left=x+'px'; e.style.top=y+'px'; gsap.set(e,{xPercent:-50,yPercent:-50}); }
  if (css) Object.assign(e.style, css);
  return e;
}
function scene(t0, t1, bg){
  const s = h('<div class="scene"><div class="abs drift" style="inset:0"><div class="abs shk" style="inset:0"><div class="cam"></div><div class="abs ui" style="inset:0"></div></div></div></div>');
  s.style.background = bg; stage.insertBefore(s, document.getElementById('caps'));
  tl.set(s, {visibility:'visible'}, t0); tl.set(s, {visibility:'hidden'}, t1);
  s.cam = s.querySelector('.cam'); s.ui = s.querySelector('.ui'); s.shk = s.querySelector('.shk'); s.t0=t0; s.t1=t1;
  tl.fromTo(s.querySelector('.drift'), {scale:1}, {scale:1.025, duration:t1-t0, ease:'none'}, t0);
  return s;
}
// motions
const pop = (e,t,o={}) => (tl.fromTo(e,{scale:o.from??.3,autoAlpha:0,rotation:o.r0??(o.r??0)},{scale:o.to??1,autoAlpha:1,rotation:o.r??0,duration:o.d??.42,ease:o.ease??'back.out(2.2)'},t), e);
const rise = (e,t,o={}) => (tl.fromTo(e,{y:o.dy??90,autoAlpha:0},{y:0,autoAlpha:1,duration:o.d??.5,ease:o.ease??'power3.out'},t), e);
const slide = (e,t,dx,o={}) => (tl.fromTo(e,{x:dx,autoAlpha:0,rotation:o.r0??0},{x:0,autoAlpha:1,rotation:o.r??0,duration:o.d??.5,ease:o.ease??'power4.out'},t), e);
const fade = (e,t,d=.3) => (tl.fromTo(e,{autoAlpha:0},{autoAlpha:1,duration:d,ease:'power1.out'},t), e);
const out = (e,t,o={}) => tl.to(e,{autoAlpha:0,scale:o.s??.85,y:o.y??0,duration:o.d??.22,ease:'power2.in'},t);
function stamp(e,t,o={}){ tl.fromTo(e,{scale:o.from??2.6,autoAlpha:0,rotation:o.r??-10},{scale:1,autoAlpha:1,rotation:o.r??-10,duration:.18,ease:'power4.in'},t); return e; }
function shake(s,t,a=16){ const k=s.shk; [[a,0],[-a*.8,a*.3],[a*.5,-a*.3],[-a*.3,0],[0,0]].forEach(([x,y],i)=>tl.to(k,{x,y,duration:.045,ease:'none'},t+i*.045)); }
function focus(s,t,px,py,k,d=.5,ease='power3.inOut'){ tl.to(s.cam,{x:-k*(px-540),y:-k*(py-806),scale:k,duration:d,ease},t); }
function flash(t,a=.85,color='#fff'){ const f=document.getElementById('flash'); tl.set(f,{opacity:a,backgroundColor:color},t); tl.to(f,{opacity:0,duration:.28,ease:'power2.out'},t+.03); }
function draw(path,t,d=.5,ease='power2.inOut'){ const L=path.getTotalLength(); gsap.set(path,{strokeDasharray:L,strokeDashoffset:L}); tl.to(path,{strokeDashoffset:0,duration:d,ease},t); }
function expr(w,t,spec){ for(const k in spec){ tl.set(w.querySelectorAll(`[data-k="${k}"]`),{opacity:0},t); tl.set(w.querySelectorAll(`[data-k="${k}"][data-v="${spec[k]}"]`),{opacity:1},t);} }
function talk(w,t0,t1,base='smile'){ let k=0; for(let t=t0;t<t1-.05;t+=.11,k++) expr(w,t,{mo:k%2?base:'open'}); expr(w,t1,{mo:base}); }
function jitter(el, t0, t1, amp=6, spd=1.3){ procs.push(t=>{ if(t<t0||t>t1) return; const u=t*spd; gsap.set(el,{x:Math.sin(u*2.1)*amp+Math.sin(u*5.3)*amp*.4, y:Math.cos(u*1.7)*amp+Math.sin(u*4.1)*amp*.3, rotation:Math.sin(u*1.3)*.4}); }); }
const K = (txt,size,color='var(--dg)',w=900) => `<div class="k" style="font-size:${size}px;color:${color};font-weight:${w}">${txt}</div>`;
const svgBox = (svg,w) => `<div style="width:${w}px">${svg}</div>`;
const leafDeco = (p,x,y,r,sz,op=.5) => { const e=add(p,svgBox(ART.icon('leaf',{fill:'#C2E3B6',stroke:'#9CCB8E',w:4}),sz),x,y); gsap.set(e,{rotation:r,opacity:op}); return e; };
function counter(el,t0,t1,a,b,fmt=v=>Math.round(v)+'%'){ procs.push(t=>{ const u=Math.min(1,Math.max(0,(t-t0)/(t1-t0))); const e=u<.5?2*u*u:1-Math.pow(-2*u+2,2)/2; el.textContent=fmt(a+(b-a)*e); }); }

// ================= build =================
async function build(){
await document.fonts.load('900 40px P'); await document.fonts.load('700 40px P'); await document.fonts.load('800 40px P'); await document.fonts.load('600 40px P'); await document.fonts.load('700 40px Gaegu','가나다');
await document.fonts.ready;

// ---------- A. HOOK 0 → 2.76 : 매력 게이지가 깎인다 ----------
{ const s=scene(0,T(5),'radial-gradient(circle at 50% 38%,#FFFFFF 0%,#F0F6EB 55%,#E1EDD9 100%)'), c=s.cam;
  leafDeco(c,110,1250,-30,200,.45); leafDeco(c,980,420,140,150,.4);
  const hw=add(c,'<div style="width:560px;height:520px;position:relative"></div>',540,760);
  hw.innerHTML=ART.heartMeter();
  const pct=add(hw,`<div class="k" style="font-size:132px;color:#fff">100%</div>`,280,250);
  const lab=add(c,`<div class="tag" style="font-size:44px;padding:16px 36px">${ART.icon('heart',{size:46,fill:'#FF8C8C',stroke:'#fff',w:8})} 내 매력</div>`,540,420);
  tl.fromTo(hw,{scale:.82},{scale:1,duration:.45,ease:'back.out(2.5)'},0); pop(lab,T(1),{from:.5});
  const svg=hw.querySelector('svg'), liq=svg.querySelector('.liq'), wave=svg.querySelector('.wave');
  procs.push(t=>{ gsap.set(wave,{x:-((t*160)%135)}); });
  // bites
  const bites=[[468,120,70],[520,250,62],[70,140,58]];
  const NS='http://www.w3.org/2000/svg', defs=svg.querySelector('defs'), mk=document.createElementNS(NS,'mask'); mk.setAttribute('id','bm');
  const mr=document.createElementNS(NS,'rect'); mr.setAttribute('x',-50);mr.setAttribute('y',-50);mr.setAttribute('width',700);mr.setAttribute('height',700);mr.setAttribute('fill','#fff'); mk.appendChild(mr); defs.appendChild(mk);
  const grp=document.createElementNS(NS,'g'); grp.setAttribute('mask','url(#bm)'); [...svg.children].filter(e=>e!==defs).forEach(e=>grp.appendChild(e)); svg.appendChild(grp);
  bites.forEach(([x,y,r],i)=>{ const b=document.createElementNS(NS,'circle'); b.setAttribute('cx',x);b.setAttribute('cy',y);b.setAttribute('r',0);b.setAttribute('fill','#000'); mk.appendChild(b); tl.to(b,{attr:{r},duration:.12,ease:'power4.out'},T(2)+.02+i*.16); });
  for(let i=0;i<10;i++){ const cr=add(c,`<div style="width:${10+i%3*6}px;height:${10+i%3*6}px;border-radius:4px;background:${i%2?'#15402A':'#3E9B5B'}"></div>`,540+200*Math.cos(i),640+120*Math.sin(i*1.7));
    tl.fromTo(cr,{autoAlpha:0,x:0,y:0},{autoAlpha:1,x:(i%2?1:-1)*(80+i*18),y:-60+i*22,rotation:i*40,duration:.5,ease:'power2.out'},T(2)+.05+(i%3)*.15); tl.to(cr,{autoAlpha:0,y:'+=160',duration:.4},T(2)+.6); }
  tl.to(liq,{attr:{y:330},duration:.62,ease:'power2.in'},T(2)); tl.to(wave,{y:290,duration:.62,ease:'power2.in'},T(2));
  tl.to([liq,wave],{fill:'#E4574C',duration:.4},T(2)+.2);
  counter(pct,T(2),T(2)+.62,100,23); tl.to(pct,{scale:.8,duration:.3},T(2)+.3);
  shake(s,T(2)+.02,10); sfx(T(2),'crunch',.9); sfx(0,'whoosh',.5);
  // → card
  tl.to(hw,{scale:.46,y:-250,duration:.45,ease:'power3.inOut'},T(3)); tl.to(lab,{autoAlpha:0,y:-40,duration:.25},T(3));
  const card=add(c,`<div class="card" style="width:820px;height:360px;display:flex;align-items:center;gap:44px;padding:0 56px">
     <div style="flex:none;width:190px;height:190px;border-radius:50%;background:var(--dg);border:12px solid #E3A33B;display:flex;align-items:center;justify-content:center;color:#fff;font-weight:900;font-size:120px">1</div>
     <div style="flex:1"><div style="font-weight:800;font-size:40px;color:#8C988F;letter-spacing:-.02em;white-space:nowrap">매력 깎아먹는 행동</div>
     <div class="red1" style="margin-top:22px;height:44px;width:430px;border-radius:12px;background:#D7E3D1"></div>
     <div class="red2" style="margin-top:16px;height:44px;width:300px;border-radius:12px;background:#D7E3D1"></div></div></div>`,540,1040);
  rise(card,T(3),{dy:260,d:.5});
  const q=add(c,`<div style="width:130px;height:130px;border-radius:50%;background:#E4574C;color:#fff;font-weight:900;font-size:92px;display:flex;align-items:center;justify-content:center;box-shadow:0 10px 30px rgba(228,87,76,.4)">?</div>`,880,860);
  pop(q,T(4),{r0:-60,r:12}); sfx(T(4),'pop',.6);
  procs.push(t=>{ if(t<T(4)) return; const u=(t*3)%1; card.querySelectorAll('.red1,.red2').forEach(r=>r.style.background=`linear-gradient(90deg,#D7E3D1 ${u*100-30}%,#F2F7EF ${u*100}%,#D7E3D1 ${u*100+30}%)`); });
  const one=add(c,`<div class="tag red" style="font-size:40px">딱 하나</div>`,540,1290); pop(one,T(4)+.12);
}

// ---------- B. 흔한 착각 2.76 → 5.32 ----------
{ const s=scene(T(5),T(11),'#EEF5EA'), c=s.cam;
  c.style.backgroundImage='radial-gradient(#CFE3C7 3px,transparent 3px)'; c.style.backgroundSize='54px 54px';
  const q=add(c,`<div class="tag light" style="font-size:40px">이게 문제일까?</div>`,540,390); pop(q,T(5),{from:.6});
  const mk=(icon,label)=>`<div class="card" style="width:600px;height:250px;display:flex;align-items:center;gap:34px;padding:0 48px">${ART.icon(icon,{size:150})}<div class="k" style="font-size:78px">${label}</div></div>`;
  const c1=add(c,mk('speech','말주변'),420,700), c2=add(c,mk('laugh','유머 감각'),640,1030);
  slide(c1,T(5),-900,{r0:-12,r:-4}); slide(c2,T(8),900,{r0:12,r:3});
  const x1=add(c,svgBox(ART.xmark(210),210),700,690), x2=add(c,svgBox(ART.xmark(210),210),900,1020);
  stamp(x1,T(7)); stamp(x2,T(10)); sfx(T(7),'stamp',.8); sfx(T(10),'stamp',.8); shake(s,T(7)+.18,10); shake(s,T(10)+.18,10);
  tl.to(c1,{opacity:.45,filter:'grayscale(1)',duration:.25},T(7)+.18); tl.to(c2,{opacity:.45,filter:'grayscale(1)',duration:.25},T(10)+.18);
  tl.to([c1,c2,x1,x2],{scale:.9,duration:.5,ease:'power2.in'},T(10)+.35);
}

// ---------- C. 진짜 원인 (PATTERN INTERRUPT) 5.32 → 8.12 ----------
{ const s=scene(T(11),T(16),'radial-gradient(circle at 50% 45%,#1E5638 0%,#15402A 60%,#0F2F1F 100%)'), c=s.cam;
  flash(T(11),.9); sfx(T(11),'hit',1);
  const tag=add(c,`<div class="tag green" style="font-size:44px">진짜 원인</div>`,540,380); stamp(tag,T(11),{r:0,from:1.8});
  const d1=add(c,svgBox(ART.dial('#A6E6A0'),330),300,800), d2=add(c,svgBox(ART.dial('#FFD27A'),330),770,800);
  pop(d1,T(11)+.1,{from:.5}); pop(d2,T(11)+.2,{from:.5});
  const l1=add(c,K('상대 반응',50,'#fff',800),300,1010), l2=add(c,K('내 태도',50,'#fff',800),770,1010);
  rise(l1,T(11)+.15,{dy:30}); rise(l2,T(11)+.25,{dy:30});
  const f1=add(c,svgBox(ART.icon('smile',{fill:'#DDEFD5',stroke:'#15402A'}),110),300,590), f2=add(c,svgBox(ART.icon('face',{fill:'#DDEFD5',stroke:'#15402A'}),110),300,590);
  pop(f1,T(11)+.1); tl.set(f2,{autoAlpha:0},0); tl.to(f1,{autoAlpha:0,duration:.1},T(12)); tl.to(f2,{autoAlpha:1,duration:.1},T(12));
  const n1=d1.querySelector('.needle'), n2=d2.querySelector('.needle');
  tl.to(n1,{rotation:14,duration:.45,ease:'power2.out'},T(12));
  const sl=add(c,`<div class="tag" style="background:#A6E6A0;color:#15402A;font-size:36px">살짝</div>`,420,640); pop(sl,T(12)+.1);
  const arr=add(c,`<svg width="140" height="60" viewBox="0 0 140 60"><path d="M6 30 H120 M96 8 L124 30 L96 52" stroke="#fff" stroke-opacity=".7" stroke-width="10" stroke-linecap="round" stroke-linejoin="round" fill="none"/></svg>`,535,800);
  fade(arr,T(12)+.3);
  tl.to(d2,{scale:1.1,duration:.3,ease:'back.out(3)'},T(13));
  [[-100,.12],[110,.14],[-70,.12],[95,.14],[-40,.1],[80,.18]].forEach(([r,d],i,a)=>{ const st=T(14)+a.slice(0,i).reduce((s,x)=>s+x[1],0); tl.to(n2,{rotation:r,duration:d,ease:'power2.inOut'},st); });
  sfx(T(14),'whoosh',.7);
  const hk=add(c,`<div class="tag red" style="font-size:40px">확!</div>`,880,620); pop(hk,T(14)+.1,{r:10});
  const msg=add(c,K('반응 따라 <span style="color:#FFD27A">태도가 통째로</span> 바뀐다',62,'#fff'),540,1210); rise(msg,T(15),{dy:40});
  shake(s,T(14)+.1,8);
}

// ---------- D. 예시① 표정이 굳자 해명 8.12 → 13.96 ----------
function cafe(c){
  add(c,'<div style="width:300px;height:640px;border-radius:150px 150px 20px 20px;background:rgba(255,255,255,.7)"></div>',230,560);
  add(c,'<div style="width:300px;height:640px;border-radius:150px 150px 20px 20px;background:rgba(255,255,255,.7)"></div>',850,560);
  leafDeco(c,140,820,-20,170,.7); leafDeco(c,960,780,200,150,.7);
  const man=add(c,svgBox(ART.man(),420),300,900), wom=add(c,svgBox(ART.woman(),420),780,900);
  const table=add(c,`<div style="width:1160px;height:420px;background:linear-gradient(#E6D3B2 0 26px,#D6BF98 26px)"></div>`,540,1330);
  const cup=`<svg viewBox="0 0 120 110" width="120"><path d="M14 20 H96 L88 100 Q86 108 78 108 H32 Q24 108 22 100Z" fill="#fff" stroke="#15402A" stroke-width="6"/><path d="M96 36 Q118 36 116 58 Q114 76 92 76" stroke="#15402A" stroke-width="6" fill="none"/><rect x="26" y="50" width="62" height="18" fill="#C2E3B6"/></svg>`;
  const c1=add(c,cup,420,1085), c2=add(c,cup,680,1085);
  return {man,wom,table,cups:[c1,c2]};
}
{ const s=scene(T(16),T(26),'linear-gradient(#F7F3EA,#EFE6D5)'), c=s.cam, u=s.ui;
  const {man,wom,table,cups}=cafe(c);
  gsap.set(s.cam,{scale:1.14,x:0,y:-1.14*(900-806)});
  rise(table,T(16),{dy:200}); slide(man,T(16),-600); slide(wom,T(16)+.08,600); cups.forEach((e,i)=>pop(e,T(16)+.15+i*.05));
  const tag=add(u,`<div class="tag light">${ART.icon('people',{size:46})} 예시 ① 소개팅</div>`,540,370); pop(tag,T(16),{from:.6});
  // talk
  talk(man,T(17),T(18)-.05,'smile');
  const sq=add(c,`<div class="bub tl" style="position:absolute;padding:26px 34px"><svg width="170" height="60" viewBox="0 0 170 60"><path d="M6 18 Q26 4 46 18 T86 18 T126 18 T166 18 M6 46 Q26 32 46 46 T86 46" stroke="#8C988F" stroke-width="8" fill="none" stroke-linecap="round"/></svg></div>`,420,580);
  pop(sq,T(17),{from:.4}); out(sq,T(18)+.2);
  // push to woman, freeze
  focus(s,T(18),780,840,1.55,.45);
  expr(wom,T(19),{br:'f',mo:'flat',bl:'0'});
  tl.to(c,{filter:'saturate(.25)',duration:.08},T(19)); tl.to(c,{filter:'saturate(1)',duration:.25},T(20)-.1);
  const fr=add(u,`<div class="chip" style="font-size:44px"><span style="display:inline-flex;gap:8px"><i style="display:block;width:12px;height:40px;background:#15402A;border-radius:3px"></i><i style="display:block;width:12px;height:40px;background:#15402A;border-radius:3px"></i></span> 표정 굳음</div>`,540,1240);
  stamp(fr,T(19),{r:-4,from:1.8}); sfx(T(19),'tick',.8); out(fr,T(20));
  // whip to man
  focus(s,T(20),390,820,1.4,.28,'power4.inOut'); sfx(T(20),'whoosh',.45);
  expr(man,T(20)+.1,{br:'w',ey:'w',mo:'wob',sw:'1'});
  const ex=add(c,`<div class="k" style="font-size:120px;color:#E4574C">!</div>`,300,590); pop(ex,T(20)+.12,{r0:-30,r:8});
  tl.to(man.querySelector('.drop'),{y:14,duration:.3,repeat:9,yoyo:true,ease:'sine.inOut'},T(20)+.1);
  // quote bubbles (caption hidden)
  const q=['아 근데 제가','그런 의미로','말한 건 아니고…'];
  const bb=q.map((txt,i)=>add(u,`<div class="bub tl" style="font-size:52px">${txt}</div>`,700+i*20,470+i*140));
  bb.forEach((b,i)=>{ pop(b,T(21+i),{from:.4,r0:-6,r:i%2?2:-2}); sfx(T(21+i),'pop',.5); });
  talk(man,T(21),T(24),'wob');
  focus(s,T(22),370,810,1.5,.5,'power2.out'); focus(s,T(23),350,800,1.6,.5,'power2.out');
  // explanation explosion
  focus(s,T(24),540,806,1,.4);
  tl.to(bb,{scale:.6,y:-80,autoAlpha:0,duration:.3,ease:'power2.in'},T(24));
  const more=[['그러니까…',260,500,-6],['제 말은…',780,470,5],['오해하실까 봐…',420,620,4],['아니 그게…',800,600,-4],['혹시 기분…',560,500,2]];
  more.forEach(([txt,x,y,r],i)=>{ const b=add(u,`<div class="bub" style="font-size:38px;padding:18px 26px">${txt}</div>`,x,y); pop(b,T(24)+.06+i*.09,{from:.3,r}); });
  expr(wom,T(24),{ey:'h',br:'f',mo:'flat'});
  const on=add(u,`<div class="tag" style="font-size:44px;background:#fff;color:#15402A;box-shadow:0 10px 30px rgba(0,0,0,.15)"><span class="dot"></span> 해명 모드 ON</div>`,540,1240);
  stamp(on,T(25),{r:0,from:1.8}); sfx(T(25),'stamp',.6);
  procs.push(t=>{ if(t>T(25)) on.querySelector('.dot').style.opacity = (Math.floor(t*4)%2)?.3:1; });
  talk(man,T(24),T(26),'wob');
}

// ---------- E. 예시② 농담에 안 웃음 13.96 → 18.28 ----------
{ const s=scene(T(26),T(34),'radial-gradient(circle at 34% 45%,#FFFFFF 0%,#E9F4E3 40%,#D3E9CB 100%)'), c=s.cam, u=s.ui;
  const tag=add(u,`<div class="tag light">${ART.icon('laugh',{size:46})} 예시 ② 농담</div>`,540,370); pop(tag,T(26),{from:.6}); tl.to(tag,{autoAlpha:0,duration:.15},T(33)-.1);
  const man=add(c,svgBox(ART.man({shirt:'#2D7B48'}),490),330,1030); rise(man,T(26),{dy:300});
  talk(man,T(26),T(27),'smile');
  const joke=add(c,`<div class="bub tl" style="display:flex;align-items:center;gap:18px;padding:22px 34px">${ART.icon('laugh',{size:84})}<svg width="150" height="50" viewBox="0 0 150 50"><path d="M6 14 H144 M6 38 H100" stroke="#C2CCC5" stroke-width="12" stroke-linecap="round"/></svg>${ART.icon('spark',{size:56,fill:'#FFD27A'})}</div>`,420,580);
  pop(joke,T(26)+.05,{from:.4,r:-3});
  // laugh meter
  const mt=add(u,`<div style="width:190px;height:600px;position:relative">
     <div style="position:absolute;left:0;right:0;top:-70px;text-align:center;font-weight:800;font-size:38px;color:#15402A;white-space:nowrap">웃음 게이지</div>
     <div style="position:absolute;left:45px;width:100px;top:0;bottom:0;border-radius:50px;background:#fff;border:8px solid #15402A;overflow:hidden"><div class="lf" style="position:absolute;left:0;right:0;bottom:0;height:0%;background:#3E9B5B"></div></div>
     <div style="position:absolute;left:-60px;top:40px;font-weight:800;font-size:30px;color:#8C988F;line-height:180px;text-align:right;width:90px">ㅋㅋㅋ<br>ㅋㅋ<br>ㅋ</div></div>`,830,900);
  pop(mt,T(27),{from:.6});
  const lf=mt.querySelector('.lf');
  tl.to(lf,{height:'14%',duration:.25,ease:'power2.out'},T(27)+.2); tl.to(lf,{height:'0%',duration:.3,ease:'power2.in'},T(27)+.45);
  const zero=add(u,`<div class="tag red" style="font-size:52px">0</div>`,830,1250); stamp(zero,T(28),{r:0,from:2}); sfx(T(28),'tick',.6);
  const dots=add(u,`<div class="bub tr" style="font-size:60px;letter-spacing:.1em;color:#8C988F;padding:10px 40px 30px">……</div>`,630,760); pop(dots,T(28)+.08);
  // awkward
  expr(man,T(29),{br:'w',ey:'w',mo:'wob',sw:'1',bl:'1'}); focus(s,T(29),420,880,1.12,.45);
  tl.to(man.querySelector('.drop'),{y:14,duration:.3,repeat:7,yoyo:true,ease:'sine.inOut'},T(29));
  // joke cracks & falls
  tl.to(joke,{rotation:-24,y:520,x:-80,autoAlpha:0,duration:.7,ease:'power2.in'},T(30));
  const aw=add(u,`<div class="bub tl" style="font-size:54px">아 좀 재미없었죠?</div>`,520,520); pop(aw,T(30),{from:.4,r:-2}); sfx(T(30),'pop',.5);
  talk(man,T(30),T(31),'wob'); out(dots,T(30));
  // undo
  const un=add(u,`<div class="chip" style="font-size:42px;gap:16px">${ART.icon('undo',{size:56})} 되돌리기</div>`,760,1180); pop(un,T(31),{from:.5});
  const cur=add(u,svgBox(ART.icon('cursor',{size:90}),90),1000,1400); tl.fromTo(cur,{autoAlpha:0},{autoAlpha:1,x:-150,y:-160,duration:.3,ease:'power2.out'},T(31)+.05);
  tl.to(un,{scale:.9,duration:.06},T(32)); tl.to(un,{scale:1,duration:.12},T(32)+.06); sfx(T(32),'click',.7);
  tl.to(un,{backgroundColor:'#15402A',color:'#fff',duration:.1},T(32));
  tl.to(aw,{scale:.7,y:-60,autoAlpha:.5,duration:.3},T(32)+.05);
  const sp=add(u,`<div class="tag" style="font-size:42px;gap:18px"><svg width="44" height="44" viewBox="0 0 44 44" class="spin"><circle cx="22" cy="22" r="16" stroke="#fff" stroke-opacity=".3" stroke-width="6" fill="none"/><path d="M22 6 A16 16 0 0 1 38 22" stroke="#A6E6A0" stroke-width="6" fill="none" stroke-linecap="round"/></svg> 말 수습 중…</div>`,540,400);
  pop(sp,T(33),{from:.5});
  procs.push(t=>{ sp.querySelector('.spin').style.transform=`rotate(${t*540}deg)`; });
}

// ---------- F. 시네마틱 인서트: 테이블 위 폰 18.28 → 19.36 ----------
{ const s=scene(T(34),T(36),'#2A3A2E'), c=s.cam;
  const bok=add(c,'<div class="abs" style="inset:-80px;filter:blur(26px)"></div>');
  [['#F6D58A',180,300,160],['#9CCB8E',860,260,220],['#FFF1C9',620,520,120],['#E3A33B',300,640,140],['#C2E3B6',980,720,180],['#FFF7E0',120,900,110],['#F6D58A',760,120,90]].forEach(([col,x,y,r])=>add(bok,`<div style="width:${r*2}px;height:${r*2}px;border-radius:50%;background:${col};opacity:.55"></div>`,x,y));
  add(c,'<div class="abs" style="left:-200px;right:-200px;top:980px;height:1400px;background:linear-gradient(#8C6A48,#5E4630);transform:perspective(900px) rotateX(58deg);transform-origin:50% 0"></div>');
  const ph=add(c,`<div style="width:360px;height:740px;border-radius:52px;background:#0E1A14;padding:14px;box-shadow:30px 40px 60px rgba(0,0,0,.5)"><div class="scr" style="width:100%;height:100%;border-radius:40px;background:#111;position:relative;overflow:hidden">
    <div class="nt" style="position:absolute;left:16px;right:16px;top:60px;border-radius:26px;background:rgba(255,255,255,.92);padding:18px 20px;display:flex;gap:14px;align-items:center;opacity:0">
    <div style="width:56px;height:56px;border-radius:16px;background:#FEE34E"></div><div><div style="font-weight:800;font-size:26px">지은</div><div style="font-size:24px;color:#555">새 메시지</div></div></div></div></div>`,560,1180);
  gsap.set(ph,{rotationX:34,rotationZ:-10,transformPerspective:1600,scale:1.15});
  const cup=add(c,'<div style="width:220px;height:260px;border-radius:24px 24px 60px 60px;background:linear-gradient(90deg,#EDE6DA,#FFFFFF 40%,#D8CFC2);filter:blur(5px)"></div>',230,1010);
  const scr=ph.querySelector('.scr'), nt=ph.querySelector('.nt');
  tl.fromTo(c,{filter:'blur(14px)'},{filter:'blur(0px)',duration:.4,ease:'power2.out'},T(34));
  tl.fromTo(s.cam,{scale:1.0},{scale:1.1,duration:.9,ease:'none'},T(34));
  tl.to(scr,{background:'#DCEBDD',duration:.15},T(35)); tl.to(nt,{opacity:1,y:10,duration:.2},T(35)); sfx(T(35),'buzz',.6);
  const glow=add(c,'<div style="width:700px;height:700px;border-radius:50%;background:radial-gradient(rgba(220,255,220,.45),transparent 65%)"></div>',560,1180); fade(glow,T(35),.2);
  tl.to(s.cam,{scale:2.8,y:-900,duration:.25,ease:'power3.in'},T(36)-.25); flash(T(36)-.04,.9);
  jitter(s.querySelector('.drift'),T(34),T(36),5);
  add(s.ui,'<div class="abs" style="inset:0;background:radial-gradient(circle at 50% 50%,transparent 55%,rgba(0,0,0,.45))"></div>');
}

// ---------- chat helpers ----------
function chat(p,x,y,w,hh,msgs){
  const ph=add(p,`<div class="phone" style="width:${w}px;height:${hh}px"><div class="screen">
     <div class="chatbar"><span style="font-weight:400;font-size:52px;margin-right:4px">‹</span><div class="av"><div style="position:absolute;left:-6px;top:-4px;width:80px">${ART.woman()}</div></div>지은</div>
     <div class="box" style="position:absolute;left:0;right:0;top:0;padding:170px 30px 0;display:flex;flex-direction:column;gap:22px"></div></div></div>`,x,y);
  const box=ph.querySelector('.box');
  const els=msgs.map(m=>{ const e = m.div ? h(`<div style="align-self:center;background:rgba(21,64,42,.14);color:#2c4034;font-size:28px;font-weight:700;padding:10px 26px;border-radius:999px">${m.div}</div>`)
     : h(`<div class="m ${m.me?'me':''}"><div class="b">${m.text}</div><div class="meta">${m.one?'<span class="one">1</span><br>':''}${m.time||''}</div></div>`); box.appendChild(e); return e; });
  return {ph,box,els,H:hh-36};
}
const chatY=(c,i)=>{ const e=c.els[i]; return c.H-44-(e.offsetTop+e.offsetHeight); };
function chatNext(c,i,t){ const e=c.els[i]; tl.to(c.box,{y:chatY(c,i),duration:.32,ease:'power3.out'},t);
  tl.fromTo(e,{scale:.5,autoAlpha:0,transformOrigin:e.classList.contains('me')?'100% 100%':'0% 100%'},{scale:1,autoAlpha:1,duration:.34,ease:'back.out(2)'},t); }

// ---------- G. 카톡: 답장 짧아짐 → 과한 친절 19.36 → 21.36 ----------
{ const s=scene(T(36),T(39),'linear-gradient(160deg,#F4F7EF,#DDEFD5)'), c=s.cam, u=s.ui;
  leafDeco(c,90,1300,-20,180,.6);
  const ch=chat(c,540,830,720,1060,[
    {text:'혹시 전시 좋아하세요? 이번 주말에 괜찮은 거 있어서요',time:'오후 1:12'},
    {me:1,text:'오 완전 좋아요!! 같이 가요 ㅎㅎ',time:'오후 1:20'},
    {text:'오늘 전시 진짜 좋았어요!! 사진 정리해서 보내드릴게요 ㅎㅎ',time:'오후 6:02'},
    {me:1,text:'저도 너무 즐거웠어요 ㅎㅎ 조심히 들어가세요!',time:'오후 6:05'},
    {text:'ㅇㅇ',time:'오후 7:40'},
    {me:1,text:'헉 많이 피곤하시죠?? 😢 오늘 푹 쉬시고 따뜻한 거 꼭 챙겨 드세요!! 🙏✨',time:'오후 7:41'}]);
  gsap.set(ch.box,{y:chatY(ch,3)}); gsap.set(ch.els.slice(4),{autoAlpha:0});
  tl.fromTo(ch.ph,{scale:1.25,autoAlpha:0},{scale:1,autoAlpha:1,duration:.35,ease:'power3.out'},T(36));
  chatNext(ch,4,T(36)+.05); sfx(T(36),'ding',.7);
  const note=add(u,`<div class="chip" style="font-size:40px;background:#15402A;color:#fff">← 답장 길이 ↓</div>`,500,1262); pop(note,T(36)+.35,{r:-4});
  const typ=add(ch.ph.querySelector('.screen'),`<div class="typing" style="position:absolute;right:30px;bottom:44px;background:#FEE34E;border-radius:30px"><i></i><i></i><i></i></div>`);
  pop(typ,T(37),{from:.5}); tl.to(typ,{autoAlpha:0,duration:.05},T(38));
  procs.push(t=>{ typ.querySelectorAll('i').forEach((d,k)=>d.style.transform=`translateY(${Math.sin(t*14-k)*6}px)`); });
  chatNext(ch,5,T(38)); sfx(T(38),'send',.6);
  const st=add(u,`<div class="tag" style="font-size:46px;background:#E4574C;gap:12px">${ART.icon('heart',{size:52,fill:'#fff',stroke:'#fff',w:4})} 친절 +200%</div>`,700,560);
  pop(st,T(38)+.3,{r0:-20,r:6}); tl.to(note,{autoAlpha:0,duration:.2},T(38));
}

// ---------- H. 시네마틱 인서트: 밤, 답장 기다림 21.36 → 22.00 ----------
{ const s=scene(T(39),T(40),'linear-gradient(#0C1720,#1A2A33)'), c=s.cam;
  add(c,'<div style="width:360px;height:520px;border-radius:18px;background:linear-gradient(#1E3B4F,#12263A);border:10px solid #0A141B"></div>',760,560);
  add(c,'<div style="width:90px;height:90px;border-radius:50%;background:#F4EFD8;box-shadow:0 0 60px rgba(244,239,216,.5)"></div>',820,460);
  const clk=add(c,`<svg viewBox="0 0 200 200" width="200"><circle cx="100" cy="100" r="88" fill="#1B2C36" stroke="#6E8794" stroke-width="10"/><g class="hh"><path d="M100 100 V52" stroke="#E6EEF2" stroke-width="10" stroke-linecap="round"/></g><g class="mh"><path d="M100 100 V30" stroke="#A6E6A0" stroke-width="7" stroke-linecap="round"/></g><circle cx="100" cy="100" r="9" fill="#E6EEF2"/></svg>`,250,470);
  procs.push(t=>{ if(t<T(39)-.1||t>T(40)+.1) return; const u=(t-T(39)); clk.querySelector('.mh').setAttribute('transform',`rotate(${u*1400} 100 100)`); clk.querySelector('.hh').setAttribute('transform',`rotate(${u*1400/12+120} 100 100)`); });
  add(c,'<div style="width:1200px;height:520px;border-radius:40px;background:#223441"></div>',540,1420);
  const m=add(c,svgBox(ART.man({shirt:'#2A4A3A'}),520),520,1030); gsap.set(m,{filter:'brightness(.42) saturate(.6)'});
  expr(m,0,{ey:'w',br:'w',mo:'flat'});
  add(c,'<div style="width:620px;height:620px;border-radius:50%;background:radial-gradient(rgba(170,220,255,.55),transparent 62%);mix-blend-mode:screen"></div>',520,960);
  const phn=add(c,'<div style="width:120px;height:210px;border-radius:22px;background:#0B1116;border:6px solid #222;box-shadow:0 0 50px 12px rgba(170,220,255,.55)"><div style="margin:10px;height:170px;border-radius:12px;background:#CFE6F5"></div></div>',520,1240);
  const one=add(c,`<div style="width:74px;height:74px;border-radius:50%;background:#FEE34E;color:#15402A;font-weight:900;font-size:48px;display:flex;align-items:center;justify-content:center">1</div>`,600,1120);
  pop(one,T(39)+.1); fade(c,T(39),.15);
  const tx=add(c,`<div class="hand" style="font-size:78px;color:#E6EEF2;font-weight:700;white-space:nowrap">…2시간째</div>`,300,720); fade(tx,T(39)+.12,.2);
  jitter(s.querySelector('.drift'),T(39),T(40),5,1.6);
  add(s.ui,'<div class="abs" style="inset:0;background:radial-gradient(circle at 50% 55%,transparent 50%,rgba(0,0,0,.55))"></div>');
}

// ---------- I. 카톡: 늦은 답장 → 새 화제 투척 22.00 → 23.48 ----------
{ const s=scene(T(40),T(42),'#E6F2E0'), c=s.cam, u=s.ui;
  const ch=chat(c,540,770,680,940,[
    {text:'ㅇㅇ',time:'오후 7:40'},
    {me:1,text:'헉 많이 피곤하시죠?? 😢 오늘 푹 쉬시고 따뜻한 거 꼭 챙겨 드세요!! 🙏✨',time:'오후 7:41'},
    {div:'읽고 2시간째 답 없음'},
    {me:1,text:'아 맞다! 혹시 그 영화 보셨어요? 🎬',time:'오후 9:47',one:1},
    {me:1,text:'아니면 요즘 빠진 거 있으세요?? ㅎㅎ',time:'오후 9:48',one:1}]);
  gsap.set(ch.box,{y:chatY(ch,2)}); gsap.set(ch.els.slice(3),{autoAlpha:0});
  tl.fromTo(ch.ph,{rotation:-4,scale:1.08},{rotation:-2,scale:1.12,duration:1.5,ease:'none'},T(40));
  chatNext(ch,3,T(40)); chatNext(ch,4,T(41)); sfx(T(40),'send',.5); sfx(T(41),'send',.5);
  const throwIcon=(ic,t,x1,y1)=>{ const e=add(u,svgBox(ART.icon(ic,{size:150,fill:'#FFD27A'}),150),120,1300); tl.fromTo(e,{autoAlpha:0,x:0,y:0,rotation:-30},{autoAlpha:1,duration:.1},t); tl.to(e,{x:x1-120,duration:.55,ease:'power1.out'},t); tl.to(e,{y:y1-1300,duration:.55,ease:'back.out(1.4)'},t); tl.to(e,{rotation:340,duration:.55,ease:'power1.out'},t); return e; };
  throwIcon('film',T(40)+.05,860,470); throwIcon('food',T(41)+.05,200,470);
  const cnt=add(u,`<div class="tag" style="font-size:46px;background:#15402A">새 화제 <span class="n" style="color:#FFD27A">+1</span></div>`,540,1310); pop(cnt,T(40)+.2);
  tl.set(cnt.querySelector('.n'),{textContent:'+2'},T(41)+.2); tl.fromTo(cnt,{scale:1.2},{scale:1,duration:.3,ease:'back.out(3)',immediateRender:false},T(41)+.2);
}

// ---------- J. 흔한 해석: 배려 23.48 → 24.92 ----------
{ const s=scene(T(42),T(44),'radial-gradient(circle at 50% 40%,#FFFFFF,#E4F1DD)'), c=s.cam;
  const crowd=[]; for(let i=0;i<7;i++){ const e=add(c,svgBox(ART.person(i%2?'#9CCB8E':'#3E9B5B'),96),150+i*130,1130); crowd.push(e); rise(e,T(42)+i*.05,{dy:120}); }
  const hs=crowd.map((e,i)=>{ const b=add(c,svgBox(ART.icon('heart',{size:56,fill:'#FF9C9C',stroke:'#15402A',w:8}),56),150+i*130,990); pop(b,T(43)+.05+i*.04); return b; });
  const lbl=add(c,`<div class="tag light" style="font-size:40px">대부분의 생각</div>`,540,400); pop(lbl,T(42),{from:.6});
  const big=add(c,K('배려',230),540,700); const hi=add(c,svgBox(ART.icon('heart',{size:120,fill:'#C2E3B6'}),120),540,500);
  pop(big,T(43),{from:.5,ease:'back.out(1.8)'}); pop(hi,T(43)+.1);
  tl.fromTo(big,{textShadow:'0 0 0 rgba(62,155,91,0)'},{textShadow:'0 0 60px rgba(62,155,91,.45)',duration:.5,immediateRender:false},T(43)+.2);
}

// ---------- K. 반전: 배려 ✕ → 미움받을 가능성을 못 견딤 24.92 → 28.32 ----------
{ const s=scene(T(44),T(48),'radial-gradient(circle at 50% 40%,#FFFFFF,#E4F1DD)'), c=s.cam, u=s.ui;
  const frozen=add(c,'<div class="abs" style="inset:0"></div>');
  for(let i=0;i<7;i++){ add(frozen,svgBox(ART.person(i%2?'#9CCB8E':'#3E9B5B'),96),150+i*130,1130); add(frozen,svgBox(ART.icon('heart',{size:56,fill:'#FF9C9C',stroke:'#15402A',w:8}),56),150+i*130,990); }
  add(frozen,svgBox(ART.icon('heart',{size:120,fill:'#C2E3B6'}),120),540,500);
  add(frozen,K('배려',230),540,700);
  const stk=add(frozen,'<svg width="560" height="60" viewBox="0 0 560 60"><path d="M10 34 L550 26" stroke="#E4574C" stroke-width="22" stroke-linecap="round"/></svg>',540,700);
  tl.set(frozen,{filter:'grayscale(1) contrast(1.1)'},T(44)); draw(stk.querySelector('path'),T(44)+.02,.22,'power4.out');
  flash(T(44),.5); sfx(T(44),'freeze',1); shake(s,T(44),14);
  const tagF=add(u,`<div class="tag red" style="font-size:40px">그런데 본질은?</div>`,540,400); stamp(tagF,T(44)+.1,{r:-3,from:1.8});
  // circular wipe to deep green
  const dg=add(c,'<div class="abs" style="inset:0;background:radial-gradient(circle at 50% 45%,#1E5638,#15402A 60%,#0F2F1F)"></div>');
  tl.fromTo(dg,{clipPath:'circle(0px at 540px 700px)'},{clipPath:'circle(1400px at 540px 700px)',duration:.3,ease:'power3.in'},T(44)+.22);
  // magnifier reveal
  const base=add(c,K('배려',230,'rgba(255,255,255,.28)'),540,700);
  const strk2=add(c,'<div style="width:540px;height:20px;border-radius:10px;background:rgba(228,87,76,.6)"></div>',540,705);
  const rev=add(c,'<div class="abs" style="inset:0"></div>'); add(rev,K('불안',230,'#FFD27A'),540,700);
  tl.set([base,strk2,rev],{autoAlpha:0},0); tl.set([base,strk2,rev],{autoAlpha:1},T(44)+.5);
  tl.fromTo(rev,{clipPath:'circle(150px at -200px 700px)'},{clipPath:'circle(150px at 540px 700px)',duration:.4,ease:'power3.out',immediateRender:false},T(44)+.5);
  const lens=add(c,`<svg viewBox="0 0 400 400" width="400"><circle cx="160" cy="160" r="150" fill="none" stroke="#fff" stroke-width="18"/><path d="M270 270 L380 380" stroke="#fff" stroke-width="36" stroke-linecap="round"/></svg>`,-200+120,700+120);
  tl.set(lens,{autoAlpha:0},0); tl.set(lens,{autoAlpha:1},T(44)+.5);
  tl.fromTo(lens,{x:0},{x:740,duration:.4,ease:'power3.out',immediateRender:false},T(44)+.5);
  sfx(T(44)+.5,'whoosh',.5);
  tl.to(rev,{clipPath:'circle(900px at 540px 700px)',duration:.2,ease:'power2.in'},T(44)+.92); tl.to(lens,{autoAlpha:0,scale:1.4,duration:.2},T(44)+.92);
  tl.to([base,strk2],{autoAlpha:0,duration:.1},T(45)); tl.to(tagF,{autoAlpha:0,duration:.2},T(45));
  // move "불안" up, show infographic
  tl.to(rev,{y:-330,scale:.55,duration:.4,ease:'power3.inOut'},T(45)+.2);
  const tt=add(c,K('나를 <span style="color:#FFD27A">싫어할</span> 가능성',66,'#fff',800),540,760); rise(tt,T(45)+.25,{dy:40});
  const bar=add(c,`<div style="width:820px;height:96px;border-radius:48px;background:rgba(255,255,255,.12);border:4px solid rgba(255,255,255,.3);position:relative;overflow:hidden"><div class="bf" style="position:absolute;left:0;top:0;bottom:0;width:0;background:#E4574C;border-radius:48px"></div></div>`,540,900);
  fade(bar,T(45)+.3);
  tl.to(bar.querySelector('.bf'),{width:'5%',duration:.35,ease:'back.out(3)'},T(46));
  const p1=add(c,`<div class="tag red" style="font-size:44px">단 1%</div>`,170,790); pop(p1,T(46)+.1,{r:-6});
  // weight drops on the man
  const man=add(c,svgBox(ART.person('#DDEFD5'),140),540,1210); rise(man,T(46)+.2,{dy:60});
  const wt=add(c,`<div style="width:300px;height:200px;border-radius:30px 30px 20px 20px;background:#E4574C;color:#fff;font-weight:900;font-size:100px;display:flex;align-items:center;justify-content:center;box-shadow:0 20px 40px rgba(0,0,0,.35)">1%</div>`,540,1010);
  tl.fromTo(wt,{y:-700,autoAlpha:0},{y:0,autoAlpha:1,duration:.3,ease:'power4.in'},T(47));
  tl.to(man,{scaleY:.62,scaleX:1.25,transformOrigin:'50% 100%',y:30,duration:.12,ease:'power2.out'},T(47)+.3);
  shake(s,T(47)+.3,18); sfx(T(47)+.3,'thud',1);
  tl.to([tt,bar,p1],{autoAlpha:.25,duration:.3},T(47));
  const cant=add(c,`<div class="tag" style="font-size:52px;background:#fff;color:#E4574C">못 견딤</div>`,540,1290); stamp(cant,T(47)+.42,{r:-4,from:1.8});
}

// ---------- L. 심리: 신호 감시 → 나 계속 수정 28.32 → 32.60 ----------
{ const s=scene(T(48),T(55),'#F4F7EF'), c=s.cam, u=s.ui;
  const rings=[]; for(let i=0;i<4;i++) rings.push(add(c,`<div style="width:300px;height:300px;border-radius:50%;border:4px solid #C2E3B6"></div>`,540,820));
  procs.push(t=>{ rings.forEach((r,i)=>{ const u=((t-T(48))*.55+i/4)%1; gsap.set(r,{scale:.6+u*3.2,opacity:(1-u)*.9}); }); });
  const man=add(c,svgBox(ART.man(),330),540,880); pop(man,T(48),{from:.6});
  expr(man,T(48),{br:'w',ey:'w',mo:'flat'});
  const pup=man.querySelector('.pup');
  const lines=add(c,'<svg class="abs" style="left:0;top:0" width="1080" height="1920"><path d="M540 760 L250 540" /><path d="M540 760 L830 540"/><path d="M540 1000 L540 1150"/></svg>');
  gsap.set(lines,{xPercent:0,yPercent:0}); lines.querySelectorAll('path').forEach(p=>{p.setAttribute('stroke','#3E9B5B');p.setAttribute('stroke-width','6');p.setAttribute('fill','none');p.setAttribute('stroke-dasharray','14 14');});
  const cards=[['face','표정',250,540,T(49),-60,-40],['tone','말투',830,540,T(50),60,-40],['reply','답장',540,1270,T(51),0,50]].map(([ic,lb,x,y,t,px,py],i)=>{
    const e=add(c,`<div class="card" style="width:250px;height:250px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:10px;border-radius:44px">${ART.icon(ic,{size:120})}<div class="k" style="font-size:48px">${lb}</div></div>`,x,y);
    pop(e,t,{from:.3}); tl.fromTo(lines.querySelectorAll('path')[i],{opacity:0},{opacity:1,duration:.2},t); sfx(t,'pop',.35);
    tl.to(pup,{x:px/6,y:py/8,duration:.15},t); return e; });
  procs.push(t=>{ lines.querySelectorAll('path').forEach(p=>p.setAttribute('stroke-dashoffset',-t*60)); });
  // alerts
  cards.forEach((e,i)=>{ const b=add(e,`<div style="position:absolute;right:-14px;top:-14px;width:64px;height:64px;border-radius:50%;background:#E4574C;color:#fff;font-weight:900;font-size:44px;display:flex;align-items:center;justify-content:center">!</div>`); pop(b,T(52)+i*.07,{from:.2});
    tl.to(e,{rotation:i%2?4:-4,duration:.08,repeat:5,yoyo:true},T(52)+i*.05); });
  expr(man,T(52),{sw:'1',mo:'wob'}); tl.to(pup,{x:-8,duration:.1,repeat:6,yoyo:true},T(52));
  // doc versions
  tl.to([man,...cards,lines,...rings],{autoAlpha:0,scale:.6,duration:.3,ease:'power2.in'},T(53)-.05);
  const doc=add(c,`<div style="position:relative;width:420px">${ART.icon('doc',{size:420})}<svg class="abs" style="left:0;top:0" width="420" height="420" viewBox="0 0 120 120"><path class="r1" d="M38 52 H84" stroke="#E4574C" stroke-width="4"/><path class="r2" d="M38 70 H84" stroke="#E4574C" stroke-width="4"/><path class="r3" d="M38 88 H68" stroke="#E4574C" stroke-width="4"/></svg></div>`,540,780);
  pop(doc,T(53),{from:.5});
  ['.r1','.r2','.r3'].forEach((q,i)=>draw(doc.querySelector(q),T(53)+.3+i*.25,.2));
  const names=['나.hwp','나_수정.hwp','나_최종.hwp','나_진짜최종.hwp','나_진짜최종(7).hwp'];
  const fn=add(c,`<div class="chip" style="font-size:50px;font-family:P;min-width:420px;justify-content:center">나.hwp</div>`,540,1100); pop(fn,T(53)+.05,{from:.6});
  names.forEach((n,i)=>{ if(i) { tl.set(fn,{textContent:n},T(53)+i*.26); tl.fromTo(fn,{y:-18},{y:0,duration:.15,immediateRender:false},T(53)+i*.26); } });
  const badge=add(c,`<div style="width:130px;height:130px;border-radius:50%;background:#E4574C;color:#fff;font-weight:900;font-size:40px;line-height:1.05;display:flex;flex-direction:column;align-items:center;justify-content:center"><span style="font-size:26px">수정</span>7회</div>`,760,580);
  stamp(badge,T(54),{r:10,from:2}); sfx(T(54),'stamp',.5);
}

// ---------- M. 하이에나의 태도 32.60 → 37.44 ----------
{ const s=scene(T(55),T(65),'#EFE6D3'), c=s.cam, u=s.ui;
  c.style.backgroundImage='repeating-linear-gradient(135deg,rgba(185,154,112,.08) 0 30px,transparent 30px 60px)';
  tl.fromTo(s,{clipPath:'inset(100% 0 0 0)'},{clipPath:'inset(0% 0 0 0)',duration:.3,ease:'power3.out'},T(55));
  const row=['face','tone','reply'].map((ic,i)=>{ const e=add(c,svgBox(ART.icon(ic,{size:120,fill:'#E9D8B8',stroke:'#6E5237'}),120),360+i*180,450); pop(e,T(56)+i*.07,{from:.3}); return e; });
  const br=add(c,'<svg width="560" height="60" viewBox="0 0 560 60"><path d="M10 10 Q10 40 60 40 H240 Q280 40 280 58 Q280 40 320 40 H500 Q550 40 550 10" stroke="#6E5237" stroke-width="7" fill="none" stroke-linecap="round"/></svg>',540,550);
  draw(br.querySelector('path'),T(56)+.2,.3);
  const hy=add(c,svgBox(ART.hyena(),480),540,900);
  tl.fromTo(hy,{y:700,autoAlpha:0},{y:0,autoAlpha:1,duration:.5,ease:'back.out(1.6)'},T(57)); sfx(T(57),'whoosh',.6);
  const pup=hy.querySelector('.pup');
  tl.fromTo(pup,{x:-12},{x:12,duration:.16,repeat:26,yoyo:true,ease:'sine.inOut'},T(57)+.3);
  tl.to(hy.querySelectorAll('.drop,.drop2'),{y:12,duration:.25,repeat:18,yoyo:true,ease:'sine.inOut'},T(57));
  const np=add(c,`<div class="tag" style="font-size:56px;background:#6E5237;padding:18px 44px">하이에나의 태도</div>`,540,1240);
  stamp(np,T(57)+.15,{r:-3,from:1.8});
  tl.to([...row,br],{autoAlpha:0,y:-40,duration:.25},T(57)+.4);
  // simplify
  tl.to(hy,{scale:.72,y:30,duration:.4,ease:'power3.inOut'},T(59));
  tl.to(np,{scale:.62,x:-280,y:-890,duration:.4,ease:'power3.inOut'},T(59));
  const ch1=add(c,`<div class="chip" style="font-size:50px">${ART.icon('people',{size:70})} 맞춰주기</div>`,540,1240); pop(ch1,T(60)+.1,{from:.5});
  const xx=add(c,svgBox(ART.xmark(130),130),760,1235); stamp(xx,T(62)); sfx(T(62),'stamp',.6);
  tl.to(ch1,{opacity:.4,filter:'grayscale(1)',duration:.2},T(62)+.15);
  tl.to([ch1,xx],{autoAlpha:0,x:-200,duration:.25,ease:'power2.in'},T(63));
  // puppet controller
  const ctl=add(c,`<svg viewBox="0 0 460 150" width="460"><rect x="20" y="50" width="420" height="40" rx="20" fill="#6E5237"/><rect x="210" y="0" width="40" height="150" rx="20" fill="#6E5237"/><circle cx="230" cy="70" r="46" fill="#fff" stroke="#6E5237" stroke-width="8"/><circle cx="214" cy="62" r="6" fill="#15402A"/><circle cx="246" cy="62" r="6" fill="#15402A"/><path d="M212 88 H248" stroke="#15402A" stroke-width="6" stroke-linecap="round"/></svg>`,540,470);
  const strs=add(c,'<svg class="abs" style="left:0;top:0" width="1080" height="1920"><path d="M330 480 L420 760"/><path d="M750 480 L660 760"/><path d="M540 520 L540 700"/></svg>');
  gsap.set(strs,{xPercent:0,yPercent:0}); strs.querySelectorAll('path').forEach(p=>{p.setAttribute('stroke','#6E5237');p.setAttribute('stroke-width','4');p.setAttribute('fill','none');});
  tl.fromTo(ctl,{y:-500,autoAlpha:0},{y:0,autoAlpha:1,duration:.35,ease:'back.out(1.5)'},T(63)); tl.fromTo(strs,{autoAlpha:0},{autoAlpha:1,duration:.1},T(63)+.3);
  const clab=add(c,`<div class="tag light" style="font-size:36px">상대 반응</div>`,540,340); pop(clab,T(63)+.2);
  const sw=[[-14,-70],[12,60],[-10,-50],[9,40]];
  sw.forEach(([r,x],i)=>{ const t=T(64)+i*.16; tl.to([ctl,strs],{rotation:r,x:x*.5,transformOrigin:'540px 470px',duration:.16,ease:'sine.inOut'},t); tl.to(hy,{x,rotation:r*.6,duration:.18,ease:'sine.inOut'},t+.03); });
  const ch2=add(c,`<div class="tag red" style="font-size:52px;padding:18px 40px">끌려다님</div>`,540,1250); stamp(ch2,T(64),{r:-3,from:1.8});
}

// ---------- N. 사자의 태도 37.44 → 39.64 ----------
{ const s=scene(T(65),T(68),'#EFE6D3'), c=s.cam, u=s.ui;
  const left=add(c,'<div class="abs" style="left:0;top:0;bottom:0;width:540px;background:#EFE6D3;overflow:hidden"></div>'); gsap.set(left,{xPercent:0,yPercent:0});
  const hyS=add(left,svgBox(ART.hyena(),300),270,860);
  const right=add(c,'<div class="abs" style="right:0;top:0;bottom:0;width:540px;background:radial-gradient(circle at 50% 45%,#F7FBF3,#D8ECCF);overflow:hidden"></div>'); gsap.set(right,{xPercent:0,yPercent:0});
  tl.fromTo(right,{width:0},{width:540,duration:.3,ease:'power3.out'},T(65));
  const vs=add(c,`<div style="width:120px;height:120px;border-radius:50%;background:#15402A;color:#fff;font-weight:900;font-size:50px;display:flex;align-items:center;justify-content:center">VS</div>`,540,860); pop(vs,T(65)+.1);
  const lion=add(c,svgBox(ART.lion(),300),810,860); slide(lion,T(65),400);
  sfx(T(65),'whoosh',.5);
  tl.to(right,{width:1080,duration:.4,ease:'power3.inOut'},T(66)); tl.to([left,vs],{autoAlpha:0,duration:.2},T(66)+.1);
  tl.to(lion,{x:-270,scale:1.6,duration:.4,ease:'power3.inOut'},T(66)); sfx(T(66),'chime',.7);
  tl.fromTo(lion,{y:0},{y:-8,duration:1,repeat:1,yoyo:true,ease:'sine.inOut',immediateRender:false},T(66)+.4);
  const np=add(c,`<div class="tag" style="font-size:56px;background:#2D7B48;padding:18px 44px">사자의 태도</div>`,540,1250); stamp(np,T(66)+.15,{r:0,from:1.8});
  const glow=add(c,'<div style="width:760px;height:760px;border-radius:50%;background:radial-gradient(rgba(255,210,122,.45),transparent 62%)"></div>',540,860); fade(glow,T(66)+.2,.4);
  lion.parentNode.appendChild(lion);
  // not ignoring reactions
  expr(lion,T(67),{ey:'o'});
  const e1=add(c,svgBox(ART.icon('eye',{size:130}),130),200,520), e2=add(c,svgBox(ART.icon('ear',{size:130}),130),880,520);
  pop(e1,T(67)); pop(e2,T(67)+.08);
  const ok=add(c,`<div class="chip" style="font-size:46px">${ART.icon('check',{size:56})} 반응은 본다</div>`,540,390); pop(ok,T(67)+.2,{from:.5});
}

// ---------- O. 선을 넘으면 사과 39.64 → 41.24 ----------
{ const s=scene(T(68),T(71),'#F4F7EF'), c=s.cam, u=s.ui;
  const badge=add(u,`<div class="tag light" style="font-size:36px;gap:10px"><span style="width:60px;display:block">${ART.lion()}</span> 사자의 태도</div>`,540,380); pop(badge,T(68),{from:.6});
  add(c,'<div style="width:1000px;height:10px;border-radius:5px;background:#15402A"></div>',540,1110);
  const ln=add(c,'<svg width="30" height="480" viewBox="0 0 30 480"><path d="M15 0 V480" stroke="#E3A33B" stroke-width="12" stroke-dasharray="30 22" stroke-linecap="round"/></svg>',660,870);
  const ll=add(c,`<div class="tag" style="font-size:40px;background:#E3A33B">선</div>`,660,590);
  tl.fromTo(ln,{scaleY:0,transformOrigin:'50% 100%'},{scaleY:1,duration:.3,ease:'power3.out'},T(68)); pop(ll,T(68)+.2);
  const p=add(c,svgBox(ART.person('#3E9B5B'),130),300,1005);
  tl.fromTo(p,{x:-400},{x:180,duration:.4,ease:'power2.out'},T(68));
  procs.push(t=>{ if(t>T(68)&&t<T(70)) gsap.set(p,{y:-Math.abs(Math.sin(t*16))*14}); });
  tl.to(p,{x:470,duration:.35,ease:'power2.inOut'},T(69));
  tl.to(ln.querySelector('path'),{attr:{stroke:'#E4574C'},duration:.1},T(69)+.25); tl.to(ll,{backgroundColor:'#E4574C',duration:.1},T(69)+.25);
  const warn=add(c,`<div class="k" style="font-size:110px;color:#E4574C">!</div>`,780,760); pop(warn,T(69)+.28,{r:10}); sfx(T(69)+.28,'tick',.6);
  tl.to(p,{x:260,duration:.3,ease:'power2.out'},T(70));
  tl.to(p,{rotation:24,transformOrigin:'50% 100%',duration:.2,ease:'power2.out'},T(70)+.3);
  tl.to(ln.querySelector('path'),{attr:{stroke:'#E3A33B'},duration:.2},T(70)); tl.to(ll,{backgroundColor:'#E3A33B',duration:.2},T(70)); out(warn,T(70));
  const sor=add(c,`<div class="bub tl" style="font-size:52px">미안해요</div>`,500,780); pop(sor,T(70)+.3,{from:.4});
  const ck=add(c,`<div class="chip" style="font-size:46px">${ART.icon('check',{size:56})} 사과</div>`,540,1250); pop(ck,T(70)+.35,{from:.5});
}

// ---------- P. 기준은 유지 41.24 → 44.84 ----------
{ const s=scene(T(71),T(75),'linear-gradient(#EEF6E9,#DCEDD3)'), c=s.cam, u=s.ui;
  add(c,'<div style="width:1200px;height:500px;border-radius:50% 50% 0 0;background:#C2E3B6"></div>',540,1400);
  const fc=add(c,`<div style="position:relative;width:240px;height:240px;border-radius:50%;background:#fff;box-shadow:0 12px 30px rgba(21,64,42,.15);overflow:hidden"><div style="position:absolute;left:-40px;top:0;width:320px">${ART.woman()}</div></div>`,800,520);
  expr(fc,0,{br:'f',mo:'flat',bl:'0'});
  pop(fc,T(71),{from:.4});
  const fl=add(c,`<div class="tag light" style="font-size:34px">잠깐 굳은 표정</div>`,800,690); pop(fl,T(71)+.15);
  const gust=add(c,'<svg class="abs" style="left:0;top:0" width="1080" height="1920"><path d="M660 560 Q560 520 470 580 T260 600"/><path d="M660 640 Q560 610 470 670 T240 700"/><path d="M650 720 Q560 700 470 750 T280 790"/></svg>');
  gsap.set(gust,{xPercent:0,yPercent:0}); gust.querySelectorAll('path').forEach(p=>{p.setAttribute('stroke','#9CCB8E');p.setAttribute('stroke-width','10');p.setAttribute('fill','none');p.setAttribute('stroke-linecap','round');p.setAttribute('stroke-dasharray','120 60');});
  tl.fromTo(gust,{autoAlpha:0},{autoAlpha:1,duration:.2},T(72));
  procs.push(t=>{ gust.querySelectorAll('path').forEach((p,i)=>p.setAttribute('stroke-dashoffset',t*(420+i*60))); });
  const fg=add(c,svgBox(ART.flag(),300),330,960);
  tl.fromTo(fg,{y:-900,autoAlpha:0},{y:0,autoAlpha:1,duration:.3,ease:'power4.in'},T(73)); shake(s,T(73)+.3,14); sfx(T(73)+.3,'thud',.9);
  const cloth=fg.querySelector('.cloth');
  procs.push(t=>{ const a=t>T(74)?16:10, ph=t*9; let d=`M76 44 `; for(let k=1;k<=4;k++){const x=76+k*53.5; d+=`Q${x-26} ${44+Math.sin(ph+k)*a} ${x} ${44+Math.sin(ph+k+.8)*a*.6} `;} d+=`V${170+Math.sin(ph+5)*a*.6} `; for(let k=3;k>=0;k--){const x=76+k*53.5; d+=`Q${x+26} ${170+Math.sin(ph+k+1)*a} ${x} ${170+Math.sin(ph+k+.4)*a*.6} `;} cloth.setAttribute('d',d+'Z'); });
  const fx=add(fg,`<div class="k" style="font-size:44px;color:#fff">내 기준</div>`,190,110);
  const op=add(c,`<div class="bub tl" style="font-size:44px;background:#15402A;color:#fff">내 의견</div>`,640,930); pop(op,T(73)+.35,{from:.4,r:-3});
  const keep=add(c,`<div class="chip" style="font-size:50px">${ART.icon('check',{size:60})} 그대로 유지</div>`,540,1250); stamp(keep,T(74),{r:0,from:1.7}); sfx(T(74),'stamp',.6);
  tl.to(fg.querySelector('.base'),{attr:{fill:'#3E9B5B'},duration:.2},T(74));
  const xr=add(c,`<div class="tag light" style="font-size:36px;color:#8C988F;text-decoration:line-through;text-decoration-color:#E4574C;text-decoration-thickness:5px">철회</div>`,640,1060); pop(xr,T(74)+.1,{r:-4});
}

// ---------- Q. 사자의 한마디 44.84 → 47.76 ----------
{ const s=scene(T(75),T(81),'linear-gradient(#F7F3EA,#EFE6D5)'), c=s.cam, u=s.ui;
  const {man,wom,table,cups}=cafe(c);
  expr(man,0,{mo:'calm',br:'n'}); expr(wom,0,{br:'f',mo:'flat',bl:'0'});
  const pin=add(man,`<div style="position:absolute;left:250px;top:430px;width:70px">${ART.lion()}</div>`);
  tl.fromTo(s.cam,{scale:1.18,x:60,y:-60},{scale:1.1,x:44,y:-44,duration:.9,ease:'power1.out'},T(75));
  const bub=add(u,`<div class="bub tl" style="font-size:54px;line-height:1.35;padding:30px 44px;white-space:nowrap"><div class="q1">"저는 이렇게 생각하는데</div><div class="q2">다르게 볼 수도 있겠네요"</div></div>`,540,470);
  pop(bub,T(75),{from:.5}); gsap.set(bub.querySelector('.q2'),{opacity:0}); tl.to(bub.querySelector('.q2'),{opacity:1,duration:.25},T(77));
  talk(man,T(75),T(79),'calm');
  expr(wom,T(77),{br:'u',mo:'o',bl:'1'}); expr(wom,T(78)+.35,{br:'n',mo:'smile'});
  tl.to(s.cam,{scale:1.45,x:-1.45*(780-540)+0,y:-1.45*(860-806),duration:.4,ease:'power3.inOut'},T(77)-.05);
  tl.to(bub,{scale:.8,y:-40,duration:.4,ease:'power3.inOut'},T(77)-.05);
  tl.to(s.cam,{scale:1.08,x:40,y:-40,duration:.4,ease:'power3.inOut'},T(79)-.15); tl.to(bub,{scale:1,y:0,duration:.4},T(79)-.15);
  const chA=add(u,`<div class="chip" style="font-size:44px">${ART.icon('check',{size:52})} 내 생각</div>`,330,1250), chB=add(u,`<div class="chip" style="font-size:44px">${ART.icon('check',{size:52})} 상대 존중</div>`,760,1250);
  pop(chA,T(79),{from:.4}); pop(chB,T(79)+.12,{from:.4}); sfx(T(79),'pop',.5);
  const ln=add(u,`<div class="tag green" style="font-size:36px;gap:10px"><span style="width:52px;display:block">${ART.lion()}</span> 사자의 대화</div>`,540,300); pop(ln,T(75)+.1,{from:.6});
}

// ---------- R. 이 차이 47.76 → 48.68 ----------
{ const s=scene(T(81),T(83),'#fff'), c=s.cam;
  const L=add(c,'<div class="abs" style="left:0;top:0;bottom:0;width:540px;background:#EFE6D3"></div>'), R=add(c,'<div class="abs" style="right:0;top:0;bottom:0;width:540px;background:#D8ECCF"></div>');
  gsap.set([L,R],{xPercent:0,yPercent:0});
  tl.fromTo(L,{x:-540},{x:0,duration:.25,ease:'power3.out'},T(81)); tl.fromTo(R,{x:540},{x:0,duration:.25,ease:'power3.out'},T(81));
  const hy=add(c,svgBox(ART.hyena(),360),270,830), li=add(c,svgBox(ART.lion(),360),810,830);
  slide(hy,T(81),-400); slide(li,T(81),400); sfx(T(81),'whoosh',.6);
  const l1=add(c,K('반응에 끌려다님',46,'#6E5237',800),270,1080), l2=add(c,K('반응을 보되 중심',46,'#15402A',800),810,1080);
  rise(l1,T(81)+.15,{dy:30}); rise(l2,T(81)+.2,{dy:30});
  const ne=add(c,`<div style="width:170px;height:170px;border-radius:50%;background:#15402A;color:#fff;font-weight:900;font-size:110px;display:flex;align-items:center;justify-content:center;box-shadow:0 12px 30px rgba(0,0,0,.25)">≠</div>`,540,830);
  stamp(ne,T(82),{r:0,from:2.2}); tl.to(s.cam,{scale:1.08,duration:.4,ease:'power2.out'},T(82));
  const tg=add(c,`<div class="tag" style="font-size:44px">이 차이</div>`,540,420); pop(tg,T(81)+.1);
}

// ---------- S1. 필터 48.68 → 50.92 ----------
{ const s=scene(T(83),T(87),'#F4F7EF'), c=s.cam, u=s.ui;
  const words=[['내 취향',330,470],['내 의견',750,470],['농담',330,640],['솔직한 생각',750,640]];
  const ws=words.map(([w,x,y],i)=>{ const e=add(c,`<div class="bub" style="font-size:48px;background:#fff">${w}</div>`,x,y); pop(e,T(83)+i*.07,{from:.4,r:i%2?3:-3}); return e; });
  const flt=add(c,`<div style="width:900px;height:120px;border-radius:30px;background:repeating-linear-gradient(90deg,#15402A 0 16px,transparent 16px 34px),#DDEFD5;border:8px solid #15402A;display:flex;align-items:center;justify-content:center"><div style="background:#15402A;color:#fff;font-weight:800;font-size:40px;padding:10px 30px;border-radius:999px;white-space:nowrap">싫어할까 봐 필터</div></div>`,540,880);
  rise(flt,T(84),{dy:60});
  ws.forEach((e,i)=>{ const t=T(85)+i*.12; tl.to(e,{y:'+=' + (i<2?300:150),duration:.2,ease:'power2.in'},t); tl.to(e,{autoAlpha:0,scale:.3,duration:.18},t+.2);
    const xm=add(c,svgBox(ART.xmark(90),90),words[i][1],860); pop(xm,t+.2,{from:.2}); tl.to(xm,{autoAlpha:0,duration:.2},t+.5); });
  sfx(T(85)+.2,'tick',.4); sfx(T(85)+.44,'tick',.4);
  const outb=add(c,`<div class="bub" style="font-size:46px;color:#8C988F;background:#EEF1EC">네 ㅎㅎ 좋아요</div>`,540,1110);
  tl.fromTo(outb,{y:-120,autoAlpha:0},{y:0,autoAlpha:1,duration:.35,ease:'bounce.out'},T(86)+.2);
  const lab=add(c,`<div class="tag light" style="font-size:34px;color:#8C988F">무난한 말만 남음</div>`,540,1240); pop(lab,T(86)+.45,{from:.5});
}

// ---------- S2. 실수 ↓ 50.92 → 52.16 ----------
{ const s=scene(T(87),T(90),'#F4F7EF'), c=s.cam;
  c.style.backgroundImage='linear-gradient(#E3EEDD 2px,transparent 2px),linear-gradient(90deg,#E3EEDD 2px,transparent 2px)'; c.style.backgroundSize='90px 90px';
  const ch=add(c,`<svg viewBox="0 0 800 560" width="800"><path d="M60 20 V500 H780" stroke="#15402A" stroke-width="8" fill="none" stroke-linecap="round"/>
     <path class="ln" d="M80 80 C260 90 360 260 470 330 S680 450 760 470" stroke="#3E9B5B" stroke-width="16" fill="none" stroke-linecap="round"/>
     <circle class="pt" cx="760" cy="470" r="22" fill="#3E9B5B"/></svg>`,540,800);
  fade(ch,T(87),.2); draw(ch.querySelector('.ln'),T(87)+.05,.6,'power2.inOut'); pop(ch.querySelector('.pt'),T(87)+.6);
  const yl=add(c,K('실수 가능성',54,'#15402A',800),330,450); rise(yl,T(87),{dy:30});
  const ok=add(c,`<div class="chip" style="font-size:52px">${ART.icon('check',{size:60})} 실수 ↓</div>`,700,1180); stamp(ok,T(89),{r:0,from:1.8});
  const hmm=add(c,`<div class="tag light" style="font-size:34px;color:#8C988F">안전하긴 한데…</div>`,760,640); pop(hmm,T(89)+.2);
}

// ---------- S3. 내가 사라진다 52.16 → 54.56 ----------
{ const s=scene(T(90),T(94),'radial-gradient(circle at 50% 45%,#FFFFFF,#E4F1DD)'), c=s.cam, u=s.ui;
  const tg=add(c,`<div class="tag" style="font-size:44px">대신</div>`,540,380); stamp(tg,T(90),{r:0,from:1.8}); sfx(T(90),'whoosh',.4);
  const man=add(c,svgBox(ART.man(),440),540,930); pop(man,T(90)+.05,{from:.6});
  const ghost=add(c,`<svg viewBox="0 0 100 160" width="300"><circle cx="50" cy="30" r="24" fill="none" stroke="#8C988F" stroke-width="3" stroke-dasharray="7 6"/><path d="M12 160 V104 Q12 64 50 64 Q88 64 88 104 V160" fill="none" stroke="#8C988F" stroke-width="3" stroke-dasharray="7 6"/></svg>`,540,960);
  tl.set(ghost,{autoAlpha:0},0);
  const nm=add(c,`<div class="tag green" style="font-size:44px">나</div>`,540,600); pop(nm,T(91),{from:.5});
  const traits=[['취향',240,760,'spark'],['생각',840,760,'speech'],['유머',250,1110,'laugh'],['기준',830,1110,'leaf']];
  const tr=traits.map(([w,x,y,ic],i)=>{ const e=add(c,`<div class="chip" style="font-size:42px;gap:10px">${ART.icon(ic,{size:54})} ${w}</div>`,x,y); pop(e,T(92)+i*.08,{from:.4}); return e; });
  tr.forEach((e,i)=>tl.to(e,{autoAlpha:0,y:-40,filter:'blur(8px)',duration:.35},T(93)+i*.15));
  tl.to(man,{opacity:.08,filter:'grayscale(1) blur(3px)',duration:.9,ease:'power1.inOut'},T(93)+.1);
  tl.to(ghost,{autoAlpha:1,duration:.5},T(93)+.4);
  tl.to(nm,{backgroundColor:'#8C988F',duration:.4},T(93)+.3); tl.set(nm,{textContent:'나 = ?'},T(93)+.6);
  const qs=[[400,760],[690,820],[560,700]].map(([x,y],i)=>{ const q=add(c,K('?',100,'#8C988F'),x,y); pop(q,T(93)+.6+i*.1,{r:i%2?12:-12}); return q; });
}

// ---------- T. 셀프 체크 54.56 → 58.32 ----------
{ const s=scene(T(94),T(100),'linear-gradient(160deg,#E4F1DD,#C9E5BE)'), c=s.cam, u=s.ui;
  const card=add(c,`<div class="card" style="width:860px;height:820px;padding:56px 56px;display:flex;flex-direction:column;gap:34px">
     <div style="display:flex;align-items:center;gap:20px">${ART.icon('clip',{size:90})}<div class="k" style="font-size:60px;text-align:left">셀프 체크</div></div>
     <div style="font-weight:700;font-size:44px;color:#8C988F;margin-top:-10px">지금 나는?</div>
     <div class="oA" style="display:flex;align-items:center;gap:24px;padding:26px 34px;border-radius:30px;background:#EAF5E4;border:5px solid #C2E3B6"><div style="width:110px;flex:none">${ART.lion()}</div><div class="k" style="font-size:52px;text-align:left">반응을 <span style="color:#2D7B48">보고</span> 있다</div></div>
     <div class="or" style="align-self:center;font-weight:900;font-size:40px;color:#8C988F">아니면</div>
     <div class="oB" style="display:flex;align-items:center;gap:24px;padding:26px 34px;border-radius:30px;background:#F6EFE3;border:5px solid #E3D3B6"><div style="width:110px;flex:none">${ART.hyena()}</div><div class="k" style="font-size:52px;text-align:left;color:#6E5237">반응에 <span style="color:#C05A2E">끌려</span>다닌다</div></div></div>`,540,820);
  rise(card,T(94),{dy:300,d:.5}); sfx(T(94),'whoosh',.4);
  const A=card.querySelector('.oA'), O=card.querySelector('.or'), B=card.querySelector('.oB');
  [[540,845],[540,1115]].forEach(([x,y],i)=>{ const ph=add(c,`<div style="width:748px;height:150px;border-radius:30px;border:5px dashed #C9D6C4"></div>`,x,y); card.parentNode.insertBefore(ph,card.nextSibling); fade(ph,T(94)+.3,.2); tl.to(ph,{autoAlpha:0,duration:.1},i?T(98):T(95)); });
  slide(A,T(95),-500); fade(O,T(97),.2); tl.fromTo(O,{scale:1.8},{scale:1,duration:.3,ease:'back.out(3)',immediateRender:false},T(97)); slide(B,T(98),500);
  gsap.set([A,B],{xPercent:0,yPercent:0});
  const cur=add(u,svgBox(ART.icon('cursor',{size:100}),100),900,1500);
  tl.fromTo(cur,{autoAlpha:0},{autoAlpha:1,x:-200,y:-770,duration:.5,ease:'power2.inOut'},T(95)+.4);
  tl.to(A,{scale:1.03,borderColor:'#3E9B5B',duration:.2},T(95)+.8); tl.to(A,{scale:1,borderColor:'#C2E3B6',duration:.2},T(98)+.1);
  tl.to(cur,{y:-500,duration:.45,ease:'power2.inOut'},T(98)+.3); tl.to(B,{scale:1.03,borderColor:'#C05A2E',duration:.2},T(98)+.7);
  tl.to(cur,{y:-770,duration:.35,ease:'power2.inOut'},T(99)+.25); tl.to(cur,{y:-500,duration:.3,ease:'power2.inOut'},T(99)+.6);
}

// ---------- U. 결론①: 멘트 ✕ 58.32 → 60.16 ----------
{ const s=scene(T(100),T(103),'#F4F7EF'), c=s.cam, u=s.ui;
  const a=add(c,K('결국 연애에서',54,'#8C988F',800),540,400), b=add(c,K('중요한 건',100),540,500);
  rise(a,T(100),{dy:40}); rise(b,T(101),{dy:50});
  const titles=['카톡 멘트 100선','첫 만남 오프닝 멘트','애프터 신청 멘트'];
  const cards=titles.map((tt,i)=>{ const e=add(c,`<div class="card" style="width:460px;height:300px;padding:34px;display:flex;flex-direction:column;justify-content:space-between;border:6px solid #15402A">${ART.icon('book',{size:90})}<div class="k" style="font-size:46px;text-align:left;white-space:normal">${tt}</div></div>`,540,900);
     tl.fromTo(e,{autoAlpha:0,rotation:0,y:200},{autoAlpha:1,rotation:(i-1)*14,x:(i-1)*190,y:(i===1?-20:20),duration:.35,ease:'back.out(1.6)'},T(102)+i*.06); return e; });
  const xm=add(c,svgBox(ART.xmark(360),360),540,900); stamp(xm,T(102)+.3); sfx(T(102)+.3,'stamp',1); shake(s,T(102)+.48,16);
  const nt=add(c,`<div class="tag red" style="font-size:48px">멘트 ✕</div>`,540,1230); stamp(nt,T(102)+.36,{r:-4,from:1.8});
}

// ---------- V. 결론②: 흔들려도 유지 60.16 → 62.56 ----------
{ const s=scene(T(103),T(108),'radial-gradient(circle at 50% 50%,#1E5638,#15402A 60%,#0F2F1F)'), c=s.cam, u=s.ui;
  const l1=add(c,K('상대 반응',52,'#A6E6A0',800),230,480), l2=add(c,K('내 태도',52,'#FFD27A',800),210,900);
  const sv=add(c,'<svg class="abs" style="left:0;top:0" width="1080" height="1920"><path class="w" stroke="#A6E6A0" stroke-width="12" fill="none" stroke-linecap="round"/><path class="s" d="M80 1020 H1000" stroke="#FFD27A" stroke-width="14" fill="none" stroke-linecap="round"/><circle class="d" cx="80" cy="1020" r="26" fill="#FFD27A"/></svg>');
  gsap.set(sv,{xPercent:0,yPercent:0});
  const w=sv.querySelector('.w');
  procs.push(t=>{ if(t<T(103)-.1||t>T(108)+.1) return; const amp=t<T(104)?50:115; const u=Math.min(1,(t-T(103))/.35); let d=''; for(let x=80;x<=1000;x+=10){ const y=640+Math.sin(x*.018+t*9)*amp*Math.sin(x*.004+t*1.3)*u; d+=(x===80?'M':'L')+x+' '+y.toFixed(1)+' ';} w.setAttribute('d',d); });
  rise(l1,T(103),{dy:30}); tl.fromTo(w,{autoAlpha:0},{autoAlpha:1,duration:.2},T(103));
  const shk=add(c,`<div class="tag red" style="font-size:36px">흔들흔들</div>`,860,480); pop(shk,T(104),{r:8});
  rise(l2,T(105),{dy:30}); draw(sv.querySelector('.s'),T(105),.5,'power2.out');
  tl.fromTo(sv.querySelector('.d'),{attr:{cx:80}},{attr:{cx:1000},duration:1.4,ease:'none'},T(105));
  const lv=add(c,svgBox(ART.icon('level',{size:260,fill:'#FFD27A',stroke:'#fff'}),260),540,1220); pop(lv,T(107)-.1,{from:.4});
  const keep=add(c,K('유지',120,'#fff'),540,1220); gsap.set(keep,{autoAlpha:0});
  tl.to(lv,{autoAlpha:0,scale:.6,duration:.2},T(107)+.35); pop(keep,T(107)+.4,{from:.6});
  tl.fromTo(keep,{textShadow:'0 0 0 rgba(255,210,122,0)'},{textShadow:'0 0 50px rgba(255,210,122,.8)',duration:.4,immediateRender:false},T(107)+.5);
}

// ---------- W. 핵심 메시지 → header ----------
const HD = document.getElementById('hdrL');
const hdr = add(HD, `<div style="text-align:center;white-space:nowrap"><div class="h1 k" style="font-size:112px">태도를 바꾸면</div><div class="h2 k" style="font-size:124px;color:#2D7B48;position:relative;display:inline-block">연애가 쉬워진다<svg class="ul abs" style="left:0;bottom:-26px" width="100%" height="40" viewBox="0 0 600 40" preserveAspectRatio="none"><path d="M10 26 Q300 6 590 22" stroke="#E3A33B" stroke-width="14" fill="none" stroke-linecap="round"/></svg></div></div>`, 540, 820);
{ const s=scene(T(108),T(111),'radial-gradient(circle at 50% 45%,#FFFFFF,#E4F1DD)'), c=s.cam;
  flash(T(108),.8); sfx(T(108),'chime',1);
  leafDeco(c,170,560,-30,160,.6); leafDeco(c,920,1130,150,180,.6);
  const h1=hdr.querySelector('.h1'), h2=hdr.querySelector('.h2');
  tl.set(hdr,{autoAlpha:0},0); tl.set(hdr,{autoAlpha:1},T(108));
  tl.fromTo(h1,{y:60,autoAlpha:0},{y:0,autoAlpha:1,duration:.35,ease:'power3.out'},T(108));
  tl.fromTo(h2,{scale:.6,autoAlpha:0},{scale:1,autoAlpha:1,duration:.45,ease:'back.out(2)'},T(108)+.35);
  draw(hdr.querySelector('.ul path'),T(108)+.7,.35);
  const lf=add(c,svgBox(ART.icon('leaf',{size:120}),120),540,560); pop(lf,T(108)+.1,{r0:-90,r:0});
  // move to header
  tl.to(hdr,{top:330,scale:.42,duration:.5,ease:'power3.inOut'},T(111)-.15);
}

// ---------- X. 좋은 사람 vs 이성 63.76 → 66.40 ----------
{ const s=scene(T(111),T(115),'#F4F7EF'), c=s.cam, u=s.ui;
  const L=add(c,`<div class="card" style="width:400px;height:560px;padding:40px 30px;display:flex;flex-direction:column;align-items:center;gap:22px;background:#ECEEEA;box-shadow:none;border:4px solid #D4D9D2">
     ${ART.icon('smile',{size:140,fill:'#fff',stroke:'#8C988F'})}<div class="k" style="font-size:54px;color:#6F7A72">좋은 사람</div>
     <div class="bub tl" style="position:relative;font-size:32px;color:#6F7A72;padding:16px 24px">좋은 분 같아요 ㅎㅎ</div>
     <div class="tag" style="background:#8C988F;font-size:34px;margin-top:auto">여기서 끝</div></div>`,300,880);
  const R=add(c,`<div class="card" style="width:400px;height:560px;padding:40px 30px;display:flex;flex-direction:column;align-items:center;gap:22px;background:#15402A">
     <div style="position:relative">${ART.icon('heart',{size:140,fill:'#FF8C8C',stroke:'#fff'})}<div style="position:absolute;right:-30px;top:-20px">${ART.icon('spark',{size:60,fill:'#FFD27A',stroke:'#fff',w:5})}</div></div><div class="k" style="font-size:54px;color:#fff">이성적 끌림</div>
     <div class="bub tr" style="position:relative;font-size:32px;padding:16px 24px">다음엔 언제 봐요?</div>
     <div class="tag" style="background:#E3A33B;font-size:34px;margin-top:auto">관계 시작</div></div>`,780,880);
  slide(L,T(111),-600,{r0:-10,r:-3}); slide(R,T(112),600,{r0:10,r:3}); sfx(T(112),'pop',.5);
  const mid=add(c,`<div style="width:190px;height:190px;border-radius:50%;background:#E3A33B;color:#fff;font-weight:900;font-size:62px;display:flex;align-items:center;justify-content:center;box-shadow:0 14px 34px rgba(227,163,59,.45);border:10px solid #fff">태도</div>`,540,880);
  stamp(mid,T(113),{r:0,from:2}); sfx(T(113),'stamp',.6);
  const q=add(c,`<div class="chip" style="font-size:46px">차이는 <span style="color:#2D7B48">태도</span>에서</div>`,540,1260); pop(q,T(114),{from:.5});
  tl.to(mid,{scale:1.15,duration:.2,ease:'power2.out'},T(114)); tl.to(mid,{scale:1,duration:.3,ease:'power2.inOut'},T(114)+.2);
}

// ---------- Y. CTA 66.40 → end ----------
{ const s=scene(T(115),DUR+1,'radial-gradient(circle at 50% 40%,#1E5638,#15402A 60%,#0F2F1F)'), c=s.cam, u=s.ui;
  tl.to(hdr.querySelectorAll('.k'),{color:'#fff',duration:.2},T(115)); tl.to(hdr.querySelector('.h2'),{color:'#A6E6A0',duration:.2},T(115));
  leafDeco(c,130,1280,-20,200,.18); leafDeco(c,960,560,150,170,.18);
  const logo=add(c,`<div style="display:flex;align-items:center;gap:16px;color:#fff;font-weight:800;font-size:44px;white-space:nowrap">${ART.icon('leaf',{size:70,fill:'#A6E6A0',stroke:'#fff'})} 이다사 부트캠프</div>`,540,620);
  rise(logo,T(115),{dy:40});
  const ttl=add(c,K('비공개 특강',140,'#fff'),540,790); pop(ttl,T(115)+.1,{from:.7,ease:'power3.out'});
  const sub=add(c,`<div style="text-align:center;color:rgba(255,255,255,.8);font-weight:600;font-size:42px;line-height:1.4;white-space:nowrap">'좋은 사람'과 '이성'을 가르는<br><b style="color:#FFD27A">태도의 차이</b></div>`,540,960);
  rise(sub,T(116),{dy:30});
  const btn=add(c,`<div style="display:flex;align-items:center;gap:18px;padding:30px 54px;border-radius:999px;background:#fff;color:#15402A;font-weight:900;font-size:50px;white-space:nowrap">프로필 링크에서 확인 <svg width="44" height="44" viewBox="0 0 44 44"><path d="M10 34 L34 10 M14 10 H34 V30" stroke="#15402A" stroke-width="7" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg></div>`,540,1150);
  pop(btn,T(117)-.1,{from:.6,ease:'back.out(1.6)'}); sfx(T(117)-.1,'pop',.5);
  tl.fromTo(btn,{boxShadow:'0 0 0 0 rgba(166,230,160,.6)'},{boxShadow:'0 0 0 26px rgba(166,230,160,0)',duration:.8,repeat:1,ease:'power1.out',immediateRender:false},T(117)+.2);
}

// ---------- captions ----------
const HIDE = new Set([21,22,23,30,75,76,77,78]);
const caps = document.getElementById('caps');
LINES.forEach((l,i)=>{
  if (HIDE.has(i)) return; if (i===0) l={...l,s:0};
  const nextStart = i+1<LINES.length ? LINES[i+1].s : DUR+1;
  const end = HIDE.has(i+1) ? l.e : nextStart;
  const txt = l.t.replace(/[“”"]/g,'').replace(/태도/g,'<b>태도</b>');
  const e = add(caps, `<div class="cap"><span>${txt}</span></div>`); gsap.set(e,{xPercent:-50,yPercent:0});
  tl.set(e,{visibility:'visible'},l.s); tl.set(e,{visibility:'hidden'},end);
  tl.fromTo(e.firstChild,{y:12,scale:.94,opacity:.4},{y:0,scale:1,opacity:1,duration:.12,ease:'power2.out'},l.s);
});

// ---------- grain ----------
{ const cv=document.createElement('canvas'); cv.width=cv.height=256; const g=cv.getContext('2d'); const im=g.createImageData(256,256);
  let sd=7; const rnd=()=>{sd=(sd*16807)%2147483647; return sd/2147483647;};
  for(let i=0;i<im.data.length;i+=4){ const v=Math.floor(rnd()*255); im.data[i]=im.data[i+1]=im.data[i+2]=v; im.data[i+3]=255; }
  g.putImageData(im,0,0); const gr=document.getElementById('grain'); gr.style.backgroundImage=`url(${cv.toDataURL()})`;
  procs.push(t=>{ const f=Math.round(t*FPS); gr.style.backgroundPosition=`${(f*73)%256}px ${(f*151)%256}px`; });
}

tl.set({}, {}, DUR);
window.SFX = SFX;
window.seek = (t) => { t=Math.max(t,0.0005); tl.seek(t, false); procs.forEach(p=>p(t)); };
const qs = new URLSearchParams(location.search);
window.seek(parseFloat(qs.get('t')||'0'));
window.READY = true;
}
build();
