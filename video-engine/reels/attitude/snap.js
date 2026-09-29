const { chromium } = require('/opt/node22/lib/node_modules/playwright');
(async () => {
  const times = process.argv[2].split(',').map(Number);
  const outDir = process.argv[3] || 'snaps';
  require('fs').mkdirSync(outDir, {recursive:true});
  const b = await chromium.launch({args:['--disable-web-security']});
  const p = await b.newPage({viewport:{width:1080,height:1920}});
  const errs=[]; p.on('pageerror', e=>errs.push(String(e))); p.on('console', m=>{ if(m.type()==='error') errs.push(m.text()); });
  await p.goto('http://localhost:8123/index.html');
  await p.waitForFunction(()=>window.READY===true, null, {timeout:30000}).catch(e=>console.log('not ready', errs));
  for (const t of times) {
    await p.evaluate(t=>window.seek(t), t);
    await p.screenshot({path:`${outDir}/t${t.toFixed(2).padStart(6,'0')}.jpg`, type:'jpeg', quality:80});
  }
  if (errs.length) console.log('ERRORS', errs.slice(0,10));
  await b.close();
})();
