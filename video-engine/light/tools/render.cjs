// usage:
//   node render.js <build_dir> snap <out_dir> t1 t2 ...      특정 시점 PNG
//   node render.js <build_dir> frames <out_dir> <fps> <workers>   전체 프레임 JPEG(q93)
// 같은 상태가 이어지는 프레임은 다시 찍지 않고 하드링크한다.
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
const [, , buildDir, mode, outDir, ...rest] = process.argv;
fs.mkdirSync(outDir, { recursive: true });
const url = 'file://' + path.resolve(buildDir, 'index.html');

async function page(browser) {
  const p = await browser.newPage({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
  await p.goto(url);
  await p.evaluate(() => Promise.all(['500','700','900'].map(w => document.fonts.load(w + ' 56px G', '가A1'))).then(() => document.fonts.ready));
  await p.waitForTimeout(300);
  return p;
}

(async () => {
  const browser = await chromium.launch();
  if (mode === 'snap') {
    const p = await page(browser);
    for (const t of rest) {
      await p.evaluate(t => renderAt(t), +t);
      await p.evaluate(() => new Promise(r => requestAnimationFrame(() => r())));
      await p.screenshot({ path: path.join(outDir, `t_${(+t).toFixed(2).padStart(7, '0')}.png`) });
    }
  } else {
    const fps = +rest[0], W = +rest[1];
    const dur = JSON.parse(fs.readFileSync(path.join(buildDir, 'timeline.json'))).dur;
    const N = Math.ceil(dur * fps);
    let shots = 0;
    const chunk = Math.ceil(N / W);
    await Promise.all([...Array(W).keys()].map(async w => {
      const p = await page(browser);
      let prevKey = null, prevFile = null;
      for (let i = w * chunk; i < Math.min(N, (w + 1) * chunk); i++) {
        const f = path.join(outDir, String(i).padStart(6, '0') + '.jpg');
        const key = await p.evaluate(t => renderAt(t), i / fps);
        if (key === prevKey) { try { fs.unlinkSync(f) } catch (e) {} fs.linkSync(prevFile, f); continue; }
        await p.evaluate(() => new Promise(r => requestAnimationFrame(() => r())));
        await p.screenshot({ path: f, type: 'jpeg', quality: 93 });
        prevKey = key; prevFile = f; shots++;
        if (shots % 200 === 0) console.log(`shots ${shots}, frame ${i}/${N}`);
      }
    }));
    console.log(`done: ${N} frames, ${shots} unique`);
  }
  await browser.close();
})();
