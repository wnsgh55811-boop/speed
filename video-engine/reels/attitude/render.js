// node render.js <startFrame> <endFrame(excl)> <out.mp4>
const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const { spawn } = require('child_process');
(async () => {
  const [a, b, out] = [parseInt(process.argv[2]), parseInt(process.argv[3]), process.argv[4]];
  const br = await chromium.launch();
  const p = await br.newPage({ viewport: { width: 1080, height: 1920 } });
  const errs = []; p.on('pageerror', e => errs.push(String(e)));
  await p.goto('http://localhost:8123/index.html');
  await p.waitForFunction(() => window.READY === true, null, { timeout: 60000 });
  if (process.env.DUMP_SFX) require('fs').writeFileSync('sfx.json', JSON.stringify(await p.evaluate(() => window.SFX)));
  const ff = spawn('ffmpeg', ['-loglevel', 'error', '-y', '-f', 'image2pipe', '-framerate', '30', '-c:v', 'mjpeg', '-i', '-',
    '-c:v', 'libx264', '-preset', 'medium', '-crf', '14', '-pix_fmt', 'yuv420p', '-r', '30', out], { stdio: ['pipe', 'inherit', 'inherit'] });
  const t0 = Date.now();
  for (let f = a; f < b; f++) {
    await p.evaluate(t => window.seek(t), f / 30);
    const buf = await p.screenshot({ type: 'jpeg', quality: 95 });
    if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
    if ((f - a) % 150 === 0) console.log(`[${a}-${b}] frame ${f} ${((Date.now() - t0) / 1000).toFixed(1)}s`);
  }
  ff.stdin.end(); await new Promise(r => ff.on('close', r));
  if (errs.length) console.log('ERR', errs.slice(0, 5));
  await br.close();
})();
