// Layout assertions against the real DOM.  usage: node scripts/check.mjs
import { chromium } from 'playwright';
import { resolve } from 'path';

const browser = await chromium.launch({
  executablePath: process.env.PW_CHROME || undefined,
});
const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
await page.goto('file://' + resolve('index.html'), { waitUntil: 'load' });
await page.evaluate(() => document.fonts.ready);

// settle the timeline first: measuring at tween-start would report the
// caption mid-rise rather than where it comes to rest
await page.evaluate(() => {
  window.__timelines.main.time(0);
  for (const c of document.querySelectorAll('.cap')) c.style.transform = 'none';
});
const r = await page.evaluate(() => {
  const out = { caps: 0, wide: [], lines2: [], lowCap: null, highCap: null,
                stageOut: [], bubOut: [], wm: null };
  for (const el of document.querySelectorAll('.clip')) el.hidden = false;
  const caps = [...document.querySelectorAll('.cap')];
  out.caps = caps.length;
  for (const c of caps) {
    const b = c.getBoundingClientRect();
    if (b.width > 1720) out.wide.push([c.textContent.slice(0, 30), Math.round(b.width)]);
    // one line == height within a single line-box
    if (b.height > 70) out.lines2.push([c.textContent.slice(0, 30), Math.round(b.height)]);
    out.lowCap = Math.max(out.lowCap ?? 0, Math.round(1080 - b.bottom));
    out.highCap = Math.min(out.highCap ?? 9999, Math.round(1080 - b.bottom));
  }
  for (const s of document.querySelectorAll('.stage .hl, .chap-word, .vflow, .bars, .rows, .chips')) {
    const b = s.getBoundingClientRect();
    if (b.left < 60 || b.right > 1860 || b.top < 40 || b.bottom > 960)
      out.stageOut.push([s.className, Math.round(b.left), Math.round(b.top),
                         Math.round(b.right), Math.round(b.bottom)]);
  }
  for (const s of document.querySelectorAll('.bub-stack .bub')) {
    const b = s.getBoundingClientRect();
    if (b.left < 40 || b.right > 1880 || b.bottom > 930)
      out.bubOut.push([s.textContent.slice(0, 24), Math.round(b.left),
                       Math.round(b.right), Math.round(b.bottom)]);
  }
  const w = document.querySelector('.wm').getBoundingClientRect();
  out.wm = [Math.round(w.left), Math.round(w.top), Math.round(w.width), Math.round(w.height)];
  const st = getComputedStyle(document.querySelector('.cap'));
  out.white = [st.whiteSpace, st.color, st.fontSize, st.webkitTextStrokeWidth, st.paintOrder];
  return out;
});
console.log('caption cards        ', r.caps);
console.log('captions over 1720px ', r.wide.length, r.wide.slice(0, 5));
console.log('captions wrapping    ', r.lines2.length, r.lines2.slice(0, 5));
console.log('caption bottom margin', r.highCap, '-', r.lowCap, 'px');
console.log('caption style        ', r.white);
console.log('centre blocks outside safe area', r.stageOut.length, r.stageOut.slice(0, 6));
console.log('bubbles outside safe area      ', r.bubOut.length, r.bubOut.slice(0, 6));
console.log('watermark [x,y,w,h]  ', r.wm);
await browser.close();
