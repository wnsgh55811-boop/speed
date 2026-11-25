// usage:
//   node render.js <workdir> <page.html> <timeline.json> <W> <H> test "1,4.5,10"   -> <workdir>/test/t_<t>.jpg
//   node render.js <workdir> <page.html> <timeline.json> <W> <H> full               -> <workdir>/frames/%05d.jpg (30fps)
//   node render.js <workdir> <page.html> <timeline.json> <W> <H> range ranges.json  -> re-render [[t0,t1],...] only
// Then: ffmpeg -framerate 30 -i frames/%05d.jpg -i in/voice.* -c:v libx264 -preset medium -crf 18|20 \
//         -pix_fmt yuv420p -c:a aac -b:a 192k -shortest -movflags +faststart out.mp4
const {chromium}=require('playwright'); const fs=require('fs'); const path=require('path');
const [dir,html,tlf,W,H,mode,arg]=process.argv.slice(2);
(async()=>{
  const b=await chromium.launch(); const p=await b.newPage({viewport:{width:+W,height:+H}});
  await p.goto('file://'+path.resolve(dir,html));
  const TL=JSON.parse(fs.readFileSync(path.resolve(dir,tlf),'utf8'));
  await p.evaluate(tl=>{window.TL=tl},TL);
  await p.evaluate(async()=>{for(const f of ['500 10px GA1','700 10px GA1','900 10px GA1','10px Pen','10px Emo'])
    await document.fonts.load(f,'가😊').catch(()=>{});await document.fonts.ready});
  const shot=async(t,file)=>{
    await p.evaluate(async t=>{renderAt(t);await Promise.all([...document.images].map(i=>i.decode().catch(()=>{})))},t);
    await p.screenshot({path:file,type:'jpeg',quality:93});
  };
  if(mode==='test'){ fs.mkdirSync(path.join(dir,'test'),{recursive:true});
    for(const t of arg.split(',').map(Number)) await shot(t,path.join(dir,'test',`t_${t}.jpg`)); }
  else { fs.mkdirSync(path.join(dir,'frames'),{recursive:true});
    const frames=[];
    if(mode==='range'){ for(const [a,z] of JSON.parse(fs.readFileSync(arg,'utf8'))) for(let i=Math.floor(a*30);i<=Math.ceil(z*30);i++) frames.push(i); }
    else { const n=Math.ceil(TL.dur*30); for(let i=0;i<n;i++) frames.push(i); }
    for(const [k,i] of frames.entries()){ await shot(i/30,path.join(dir,'frames',String(i).padStart(5,'0')+'.jpg'));
      if(k%300===0) console.log(k,'/',frames.length); } }
  await b.close();
})();
