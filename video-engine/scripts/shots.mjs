// Frame capture for QA.  usage: node scripts/shots.mjs <out-dir> <t> [t ...]
//
// Drives the composition's own paused GSAP timeline the same way the renderer
// does — seek, then show only the clips live at that time — so a capture here
// is the frame that will be rendered, not an approximation.
import { chromium } from 'playwright';
import { mkdirSync } from 'fs';
import { resolve } from 'path';

const [out, ...ts] = process.argv.slice(2);
mkdirSync(out, { recursive: true });

const browser = await chromium.launch({
  executablePath: process.env.PW_CHROME || undefined,
  args: ['--force-color-profile=srgb', '--font-render-hinting=none'],
});
const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
page.on('console', m => { if (m.type() === 'error') console.log('  [console]', m.text()); });
// 'load' would wait on the narration wav too, which is 160MB; the stills
// only need the images decoded.
await page.goto('file://' + resolve('index.html'), { waitUntil: 'domcontentloaded' });
await page.waitForFunction(
  () => [...document.images].every(i => i.complete),
  null, { timeout: 180000 });
await page.evaluate(() => document.fonts.ready);

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

for (const t of ts) {
  await page.evaluate(x => window.__seek(x), Number(t));
  await page.waitForTimeout(90);
  await page.screenshot({ path: `${out}/t${String(t).padStart(7, '0')}.png` });
  console.log('captured', t);
}
await browser.close();
