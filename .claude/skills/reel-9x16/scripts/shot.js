// Render a standalone HTML page (thumbnail) to PNG.
// usage: node shot.js <page.html> <out.png> <W> <H>
const {chromium}=require('playwright'); const path=require('path');
const [html,out,W,H]=process.argv.slice(2);
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:+W,height:+H}});
await p.goto('file://'+path.resolve(html));
await p.evaluate(async()=>{for(const f of ['500 10px GA1','700 10px GA1','900 10px GA1','10px Pen','10px Emo'])
  await document.fonts.load(f,'가✅').catch(()=>{});await document.fonts.ready;
  await Promise.all([...document.images].map(i=>i.decode().catch(()=>{})))});
await p.screenshot({path:out});await b.close();})();
