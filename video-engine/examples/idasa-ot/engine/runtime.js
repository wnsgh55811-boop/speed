(function(){
const D=window.SPEC, stage=document.getElementById('stage');
const tl=gsap.timeline({paused:true});
const XF=0.2;
function el(tag,cls,parent){const e=document.createElement(tag);if(cls)e.className=cls;(parent||stage).appendChild(e);return e;}
function place(e,it){const s=e.style;
  if(it.x!=null)s.left=it.x+'px'; if(it.y!=null)s.top=it.y+'px';
  if(it.w!=null)s.width=it.w+'px'; if(it.h!=null)s.height=it.h+'px';
  if(it.css)e.setAttribute('style',e.getAttribute('style')+';'+it.css);
  if(it.cls)e.className+=' '+it.cls;}
const ANIM={
 fade:[{opacity:0},{opacity:1,ease:'power2.out'}],
 up:[{opacity:0,y:50},{opacity:1,y:0,ease:'power3.out'}],
 down:[{opacity:0,y:-50},{opacity:1,y:0,ease:'power3.out'}],
 left:[{opacity:0,x:-90},{opacity:1,x:0,ease:'power3.out'}],
 right:[{opacity:0,x:90},{opacity:1,x:0,ease:'power3.out'}],
 pop:[{opacity:0,scale:.55},{opacity:1,scale:1,ease:'back.out(1.8)'}],
 zoom:[{opacity:0,scale:1.18},{opacity:1,scale:1,ease:'power3.out'}],
 wipe:[{clipPath:'inset(0% 100% 0% 0%)'},{clipPath:'inset(0% 0% 0% 0%)',ease:'power2.inOut'}],
 wipev:[{clipPath:'inset(100% 0% 0% 0%)'},{clipPath:'inset(0% 0% 0% 0%)',ease:'power2.inOut'}],
 blur:[{opacity:0,filter:'blur(18px)',scale:1.06},{opacity:1,filter:'blur(0px)',scale:1,ease:'power2.out'}],
 none:null,
};
function anim(e,it,base){
  const a=it.anim||'fade', at=base+(it.at||0), d=it.dur||(a==='wipe'||a==='wipev'?0.8:0.6);
  if(a!=='none'&&ANIM[a]) tl.fromTo(e,ANIM[a][0],Object.assign({duration:d},ANIM[a][1]),at);
  if(it.type){ // typing text
    const full=it.type, span=e.querySelector('.typed')||e; const p={n:0};
    span.textContent='';
    tl.to(p,{n:full.length,duration:it.typedur||full.length*0.07,ease:'none',onUpdate:()=>{span.textContent=full.slice(0,Math.round(p.n));}},at+(it.typedelay||0));
  }
  if(it.count){ const c=it.count,span=e.querySelector('.num')||e,p={v:c[0]};
    const fmt=v=>c[2]?v.toFixed(c[2]):Math.round(v).toLocaleString('ko-KR');
    span.textContent=fmt(c[0]);
    tl.to(p,{v:c[1],duration:c[3]||1.4,ease:'power2.out',onUpdate:()=>{span.textContent=fmt(p.v);}},at);
  }
  if(it.pulse) for(const pt of it.pulse) tl.fromTo(e,{scale:1},{scale:1.08,duration:.25,yoyo:true,repeat:1,ease:'power1.inOut'},base+pt);
  if(it.kb){const k=it.kb; tl.fromTo(e,{scale:k[0],xPercent:k[2]||0,yPercent:k[3]||0},{scale:k[1],xPercent:k[4]||0,yPercent:k[5]||0,duration:it._sd,ease:'none'},base);}
  if(it.float){tl.fromTo(e,{y:0},{y:-it.float,duration:it._sd,ease:'sine.inOut'},base);}
  if(it.out){const o=it.out; const oa=o.anim||'fade';
    const to=oa==='fade'?{opacity:0}:oa==='down'?{opacity:0,y:40}:oa==='up'?{opacity:0,y:-40}:oa==='shrink'?{opacity:0,scale:.8}:{opacity:0};
    tl.to(e,Object.assign({duration:o.dur||.4,ease:'power2.in'},to),base+o.at);}
  if(it.tw) for(const w of it.tw) tl.to(e,Object.assign({duration:w.dur||.5,ease:w.ease||'power2.inOut'},w.p),base+w.at);
}
function build(it,parent,base,sd){
  it._sd=sd; let e;
  if(it.k==='img'){e=el('img','it',parent);e.src=it.src;}
  else if(it.k==='icon'){e=el('div','it icon',parent);e.innerHTML=window.ICONS[it.name]||'';}
  else {e=el('div','it',parent);e.innerHTML=it.html||'';}
  e.querySelectorAll('[data-ic]').forEach(x=>{x.innerHTML=window.ICONS[x.dataset.ic]||'';});
  place(e,it);
  if(it.origin) e.style.transformOrigin=it.origin;
  if(it.items){for(const c of it.items) build(c,e,base,sd);}
  anim(e,it,base);
  return e;
}
D.scenes.forEach((sc,i)=>{
  const s=el('div','scene'); s.style.zIndex=i+1; s.id='sc'+i;
  if(sc.bg) s.style.background=sc.bg;
  const cam=el('div','cam',s);
  const sd=sc.t1-sc.t0+XF;
  for(const it of sc.items) build(it,cam,sc.t0,sd);
  // visibility
  tl.set(s,{autoAlpha:0},0);
  if(sc.xf===false) tl.set(s,{autoAlpha:1},sc.t0); else tl.fromTo(s,{autoAlpha:0},{autoAlpha:1,duration:XF,ease:'none'},sc.t0);
  tl.set(s,{autoAlpha:0},sc.t1+XF+0.05);
  if(sc.cam){ tl.set(cam,{scale:sc.cam[0].s||1,x:sc.cam[0].x||0,y:sc.cam[0].y||0},sc.t0);
    for(const c of sc.cam.slice(1)) tl.to(cam,{scale:c.s,x:c.x,y:c.y,duration:c.d||1.2,ease:c.e||'power2.inOut'},sc.t0+c.t);}
});
// subtitles
const sub=document.getElementById('sub'), subt=document.getElementById('subt');
const subs=D.subs;
tl.to({},{duration:D.duration},0);
window.__seek=function(t){tl.time(t,false);
  let cur='';for(const s of subs){if(t>=s[0]&&t<s[1]){cur=s[2];break;}}
  if(subt.textContent!==cur){subt.textContent=cur;}
  sub.style.visibility=cur?'visible':'hidden';
};
window.__ready=Promise.all([document.fonts.ready,...[...document.images].map(i=>i.decode().catch(()=>{}))]);
})();
