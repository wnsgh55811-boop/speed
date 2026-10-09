(function(){
const D=window.SPEC, stage=document.getElementById('stage');
const tl=gsap.timeline({paused:true});
const XF=0.2;
function el(tag,cls,parent){const e=document.createElement(tag);if(cls)e.className=cls;(parent||stage).appendChild(e);return e;}
function place(e,it){const s=e.style;
  if(it.x!=null)s.left=it.x+'px'; if(it.y!=null)s.top=it.y+'px';
  if(it.w!=null)s.width=it.w+'px'; if(it.h!=null)s.height=it.h+'px';
  if(it.css)e.setAttribute('style',(e.getAttribute('style')||'')+';'+it.css);
  if(it.cls)e.className+=' '+it.cls;}
const E3='power3.out', E4='expo.out';
const ANIM={
 fade:[{opacity:0},{opacity:1,ease:'power2.out'}],
 up:[{opacity:0,y:60},{opacity:1,y:0,ease:E4}],
 down:[{opacity:0,y:-60},{opacity:1,y:0,ease:E4}],
 left:[{opacity:0,x:-110},{opacity:1,x:0,ease:E4}],
 right:[{opacity:0,x:110},{opacity:1,x:0,ease:E4}],
 pop:[{opacity:0,scale:.6},{opacity:1,scale:1,ease:'back.out(1.7)'}],
 rise:[{opacity:0,y:40,scale:.94,filter:'blur(10px)'},{opacity:1,y:0,scale:1,filter:'blur(0px)',ease:E4}],
 blur:[{opacity:0,filter:'blur(22px)'},{opacity:1,filter:'blur(0px)',ease:'power2.out'}],
 wipe:[{clipPath:'inset(0% 100% 0% 0%)'},{clipPath:'inset(0% 0% 0% 0%)',ease:'power3.inOut'}],
 wipel:[{clipPath:'inset(0% 0% 0% 100%)'},{clipPath:'inset(0% 0% 0% 0%)',ease:'power3.inOut'}],
 wipev:[{clipPath:'inset(100% 0% 0% 0%)'},{clipPath:'inset(0% 0% 0% 0%)',ease:'power3.inOut'}],
 iris:[{clipPath:'circle(0% at 50% 50%)'},{clipPath:'circle(75% at 50% 50%)',ease:'power3.inOut'}],
 grow:[{scaleX:0},{scaleX:1,ease:'power3.inOut'}],
 drop:[{opacity:0,y:-140,rotation:-6},{opacity:1,y:0,rotation:0,ease:'bounce.out'}],
 none:null,
};
function run(target,a,at,d){ if(a&&ANIM[a]) tl.fromTo(target,ANIM[a][0],Object.assign({duration:d},ANIM[a][1]),at); }
function anim(e,it,base){
  const a=it.anim||'fade', at=base+(it.at||0), d=it.dur||(a.startsWith('wipe')||a==='iris'||a==='grow'?0.75:0.7);
  run(e,a,at,d);
  if(it.chars){ const c=it.chars; const chs=e.querySelectorAll('.ch');
    tl.fromTo(chs,{opacity:0,y:c.y==null?46:c.y,filter:'blur(8px)'},{opacity:1,y:0,filter:'blur(0px)',duration:c.dur||.55,ease:E4,stagger:c.st||.028},base+(c.at==null?(it.at||0):c.at)); }
  if(it.sub) for(const s of it.sub){ const tg=e.querySelectorAll(s.sel); if(!tg.length) continue;
    if(s.anim) { if(s.stagger){ tl.fromTo(tg,ANIM[s.anim][0],Object.assign({duration:s.dur||.6,stagger:s.stagger},ANIM[s.anim][1]),base+s.at);} else run(tg,s.anim,base+s.at,s.dur||.6); }
    if(s.p) tl.to(tg,Object.assign({duration:s.dur||.5,ease:s.ease||'power2.inOut'},s.p),base+s.at); }
  if(it.type){ const full=it.type, span=e.querySelector('.typed')||e; const p={n:0}; span.textContent='';
    tl.to(p,{n:full.length,duration:it.typedur||full.length*0.07,ease:'none',onUpdate:()=>{span.textContent=full.slice(0,Math.round(p.n));}},at+(it.typedelay||0)); }
  if(it.count){ const c=it.count,span=e.querySelector('.num')||e,p={v:c[0]};
    const fmt=v=>c[2]?v.toFixed(c[2]):Math.round(v).toLocaleString('ko-KR'); span.textContent=fmt(c[0]);
    tl.to(p,{v:c[1],duration:c[3]||1.4,ease:'power2.out',onUpdate:()=>{span.textContent=fmt(p.v);}},base+(c[4]!=null?c[4]:(it.at||0))); }
  if(it.pulse) for(const pt of it.pulse) tl.fromTo(e,{scale:1},{scale:1.06,duration:.22,yoyo:true,repeat:1,ease:'power1.inOut'},base+pt);
  if(it.float){tl.fromTo(e,{y:0},{y:-it.float,duration:it._sd,ease:'sine.inOut'},base);}
  if(it.spin){tl.fromTo(e,{rotation:0},{rotation:it.spin,duration:it._sd,ease:'none'},base);}
  if(it.drift){const d2=it.drift; tl.fromTo(e,{x:0,y:0},{x:d2[0],y:d2[1],duration:it._sd,ease:'sine.inOut'},base);}
  if(it.tw) for(const w of it.tw) tl.to(e,Object.assign({duration:w.dur||.5,ease:w.ease||'power2.inOut'},w.p),base+w.at);
  if(it.out){const o=it.out; const oa=o.anim||'fade';
    const to=oa==='down'?{opacity:0,y:40}:oa==='up'?{opacity:0,y:-40}:oa==='shrink'?{opacity:0,scale:.7}:oa==='blur'?{opacity:0,filter:'blur(16px)'}:{opacity:0};
    tl.to(e,Object.assign({duration:o.dur||.4,ease:'power2.in'},to),base+o.at);}
}
function splitChars(root){
  root.querySelectorAll('.sp').forEach(sp=>{
    const walk=n=>{ if(n.nodeType===3){ const f=document.createDocumentFragment();
        for(const ch of n.textContent){ if(ch===' '){f.appendChild(document.createTextNode(' '));continue;}
          const s=document.createElement('span'); s.className='ch'; s.textContent=ch; f.appendChild(s);} n.replaceWith(f);}
      else if(n.nodeType===1 && !n.classList.contains('stl')) [...n.childNodes].forEach(walk); };
    [...sp.childNodes].forEach(walk);});
}
function build(it,parent,base,sd){
  it._sd=sd; let e;
  if(it.k==='img'){e=el('img','it',parent);e.src=it.src;}
  else {e=el('div','it',parent);e.innerHTML=it.html||'';}
  e.querySelectorAll('[data-ic]').forEach(x=>{x.innerHTML=window.ICONS[x.dataset.ic]||'';});
  splitChars(e);
  place(e,it);
  if(it.origin) e.style.transformOrigin=it.origin;
  if(it.items){for(const c of it.items) build(c,e,base,sd);}
  anim(e,it,base);
  return e;
}
D.scenes.forEach((sc,i)=>{
  const s=el('div','scene'); s.style.zIndex=i+1;
  if(sc.bg) s.style.background=sc.bg;
  const sd=sc.t1-sc.t0+XF;
  for(const it of sc.items) build(it,s,sc.t0,sd);
  tl.set(s,{autoAlpha:0},0);
  if(sc.xf===false) tl.set(s,{autoAlpha:1},sc.t0); else tl.fromTo(s,{autoAlpha:0},{autoAlpha:1,duration:XF,ease:'none'},sc.t0);
  tl.set(s,{autoAlpha:0},sc.t1+XF+0.05);
});
const sub=document.getElementById('sub'), subt=document.getElementById('subt'), chap=document.getElementById('chap');
tl.to({},{duration:D.duration},0);
window.__seek=function(t){tl.time(t,false);
  let cur='';for(const s of D.subs){if(t>=s[0]&&t<s[1]){cur=s[2];break;}}
  if(subt.textContent!==cur) subt.textContent=cur;
  sub.style.visibility=cur?'visible':'hidden';
  let c=null;for(const x of D.chapters){if(t>=x[0])c=x;}
  if(c){ if(chap.dataset.k!==String(c[0])){chap.dataset.k=String(c[0]);chap.innerHTML='<b>'+c[1]+'</b><span>'+c[2]+'</span>';}
    const a=Math.min(1,(t-c[0])/0.5); chap.style.opacity=c[3]===false?0:a; chap.style.transform='translateX('+((1-a)*-16)+'px)';}
};
window.__ready=Promise.all([document.fonts.ready,...[...document.images].map(i=>i.decode().catch(()=>{}))]);
})();
