// Measure every candidate subtitle string at the real subtitle style, in real Chromium,
// with the real Pretendard font. Output feeds the build-time one-line guarantee.
const { chromium } = require('playwright');
const fs = require('fs');
(async () => {
  const cand = JSON.parse(fs.readFileSync('sub_candidates.json', 'utf8'));
  const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
  const css = fs.readFileSync('../assets/fonts/Pretendard-SemiBold.otf');
  await page.setContent(`<!doctype html><html><head><style>
    @font-face{font-family:Pretendard;src:url(data:font/otf;base64,${css.toString('base64')})format("opentype");font-weight:600}
    body{margin:0}
    #m{position:absolute;visibility:hidden;white-space:nowrap;font-family:Pretendard,sans-serif;
       font-size:44px;font-weight:600;letter-spacing:-.01em;-webkit-text-stroke:5px #000;paint-order:stroke fill}
  </style></head><body><span id="m"></span></body></html>`);
  await page.evaluate(() => document.fonts.ready);
  const widths = await page.evaluate((list) => {
    const m = document.getElementById('m'); const out = {};
    for (const s of list) { m.textContent = s; out[s] = m.getBoundingClientRect().width; }
    return out;
  }, cand);
  fs.writeFileSync('sub_widths.json', JSON.stringify(widths));
  console.log('measured', Object.keys(widths).length, 'strings');
  await browser.close();
})();
