// Does each scene actually move?  usage: node scripts/motion.mjs <n>
//
// The checklist asks for start/middle/end frames of representative scenes and
// calls a scene broken if the three are near-identical. Doing that by eye over
// 308 scenes is not practical, so this samples each scene at 15%/50%/85% and
// reports the mean absolute pixel difference between the three.
import { chromium } from 'playwright';
import { readFileSync } from 'fs';
import { resolve } from 'path';

const html = readFileSync('index.html', 'utf8');
const clips = [...html.matchAll(/id="fg(\d{3})" data-start="([\d.]+)" data-duration="([\d.]+)"/g)]
  .map(m => ({ i: +m[1], s: +m[2], d: +m[3] }));

const browser = await chromium.launch({
  executablePath: process.env.PW_CHROME || undefined,
});
const page = await browser.newPage({ viewport: { width: 640, height: 360 } });
// 'load' would wait on the narration wav too, which is 160MB; the stills
// only need the images decoded.
await page.goto('file://' + resolve('index.html'), { waitUntil: 'domcontentloaded' });
await page.waitForFunction(
  () => [...document.images].every(i => i.complete),
  null, { timeout: 180000 });
await page.evaluate(() => {
  const root = document.getElementById('root');
  window.__clips = [...root.querySelectorAll('.clip')].map(el => {
    const s = parseFloat(el.getAttribute('data-start')) || 0;
    return { el, s, e: s + (parseFloat(el.getAttribute('data-duration')) || 0) };
  });
  window.__seek = t => {
    window.__timelines.main.time(t);
    for (const c of window.__clips) c.el.hidden = !(t >= c.s && t < c.e);
  };
});

const step = Math.max(1, Math.floor(clips.length / (Number(process.argv[2]) || 40)));
const flat = [];
for (let k = 0; k < clips.length; k += step) {
  const c = clips[k];
  const shots = [];
  for (const f of [0.15, 0.5, 0.85]) {
    await page.evaluate(x => window.__seek(x), c.s + c.d * f);
    await page.waitForTimeout(60);
    shots.push(await page.screenshot({ type: 'png' }));
  }
  // compare decoded bytes via a canvas in-page would be heavier; PNG byte
  // length differences are a crude but sufficient liveness signal, so compare
  // pixels properly instead
  const diffs = await page.evaluate(async bufs => {
    const load = b => new Promise(r => {
      const img = new Image();
      img.onload = () => r(img);
      img.src = 'data:image/png;base64,' + b;
    });
    const imgs = await Promise.all(bufs.map(load));
    const cv = document.createElement('canvas');
    cv.width = 640; cv.height = 360;
    const cx = cv.getContext('2d');
    const data = imgs.map(im => { cx.drawImage(im, 0, 0); return cx.getImageData(0, 0, 640, 360).data; });
    const md = (a, b) => {
      let t = 0;
      for (let i = 0; i < a.length; i += 4) t += Math.abs(a[i] - b[i]);
      return t / (a.length / 4);
    };
    return [md(data[0], data[1]), md(data[1], data[2]), md(data[0], data[2])];
  }, shots.map(b => b.toString('base64')));
  flat.push({ i: c.i, d: c.d, max: Math.max(...diffs) });
}
flat.sort((a, b) => a.max - b.max);
console.log('scenes sampled:', flat.length);
console.log('quietest 12 (mean abs pixel delta across start/mid/end):');
for (const f of flat.slice(0, 12)) console.log(`  fg${String(f.i).padStart(3,'0')}  dur ${f.d.toFixed(1)}s  delta ${f.max.toFixed(2)}`);
const dead = flat.filter(f => f.max < 0.5);
console.log(`scenes below 0.5 delta (would read as frozen): ${dead.length}`);
await browser.close();
