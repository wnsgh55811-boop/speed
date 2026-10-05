// Frame renderer: node render.js <outdir|-> <fps> [start] [end] [--snap t1,t2,...]
// Seeks the GSAP timeline per frame and pipes JPEG screenshots to stdout (or writes snapshots).
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
(async () => {
  const args = process.argv.slice(2);
  const root = path.resolve(process.env.ROOT || __dirname);
  const exe = process.env.CHROME || undefined;
  const b = await chromium.launch({ executablePath: exe, args: ['--disable-gpu', '--force-color-profile=srgb', '--font-render-hinting=none'] });
  const p = await b.newPage({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
  await p.goto('file://' + root + '/index.html?render=1');
  await p.waitForFunction('window.READY === true', null, { timeout: 120000 });
  const dur = await p.evaluate('window.DURATION');
  const snapIdx = args.indexOf('--snap');
  if (args[0] === 'info') { console.log(JSON.stringify({ dur, caps: await p.evaluate('window.CAPTIONS.length') })); await b.close(); return; }
  if (snapIdx >= 0) {
    const ts = args[snapIdx + 1].split(',').map(Number);
    fs.mkdirSync(args[0], { recursive: true });
    for (const t of ts) { await p.evaluate((t) => window.seek(t), t); await p.screenshot({ path: path.join(args[0], `t${String(t.toFixed(1)).padStart(6, '0')}.jpg`), type: 'jpeg', quality: 80 }); }
    await b.close(); return;
  }
  const fps = Number(args[1] || 30);
  const N = Math.ceil(dur * fps);
  const s = Number(args[2] || 0), e = Math.min(Number(args[3] || N), N);
  for (let f = s; f < e; f++) {
    await p.evaluate((t) => window.seek(t), f / fps);
    const buf = await p.screenshot({ type: 'jpeg', quality: Number(process.env.Q || 94) });
    if (!process.stdout.write(buf)) await new Promise((r) => process.stdout.once('drain', r));
    if (f % 300 === 0) process.stderr.write(`[${s}-${e}] ${f}\n`);
  }
  await b.close();
})();
