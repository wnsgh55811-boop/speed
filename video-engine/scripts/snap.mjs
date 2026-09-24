// Local frame QA: seek the paused GSAP timeline, show only the clips live at t,
// and screenshot. Mirrors what the HyperFrames runtime does per frame.
//   node snap.mjs <build/index.html> <outdir> t1 t2 ...   (or "grid:<s>:<e>:<n>")
import { chromium } from 'playwright';
import path from 'path'; import fs from 'fs';
const [,, html, out, ...ts] = process.argv;
fs.mkdirSync(out, { recursive: true });
let times = [];
for (const t of ts) {
  if (t.startsWith('grid:')) { const [, s, e, n] = t.split(':').map(Number);
    for (let i = 0; i < n; i++) times.push(+(s + (e - s) * i / Math.max(1, n - 1)).toFixed(2)); }
  else times.push(+t);
}
const b = await chromium.launch(process.env.CHROME ? { executablePath: process.env.CHROME } : {});
const p = await b.newPage({ viewport: { width: 1920, height: 1080 } });
p.on('pageerror', e => console.log('PAGEERR', e.message)); p.on('console', m => { if (m.type()==='error') console.log('CONSOLE', m.text()); });
await p.goto('file://' + path.resolve(html));
await p.waitForTimeout(1500); console.log('tl', await p.evaluate(() => !!(window.__timelines && window.__timelines.main)));
await p.evaluate(() => document.fonts.ready);
for (const t of times) {
  await p.evaluate((t) => {
    document.querySelectorAll('.clip').forEach(el => {
      const s = parseFloat(el.getAttribute('data-start')) || 0, d = parseFloat(el.getAttribute('data-duration')) || 0;
      el.style.visibility = (t >= s && t < s + d) ? 'visible' : 'hidden';
    });
    window.__timelines.main.time(t, false);
  }, t);
  await p.waitForTimeout(40);
  await p.screenshot({ path: `${out}/f_${String(t.toFixed(2)).padStart(7, '0')}.jpg`, type: 'jpeg', quality: 70 });
}
await b.close();
console.log('snapped', times.length);
