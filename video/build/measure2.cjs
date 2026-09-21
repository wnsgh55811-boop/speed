const { chromium } = require('playwright'); const fs = require('fs');
(async () => {
  const texts = JSON.parse(fs.readFileSync('sub_texts.json','utf8'));
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  const p = await b.newPage({ viewport: { width: 1920, height: 1080 } });
  const f = fs.readFileSync('../assets/fonts/Pretendard-SemiBold.otf');
  await p.setContent(`<style>
    @font-face{font-family:Pretendard;src:url(data:font/otf;base64,${f.toString('base64')})format("opentype");font-weight:600}
    #m{position:absolute;visibility:hidden;white-space:nowrap;font-family:Pretendard,sans-serif;
       font-size:43px;font-weight:600;letter-spacing:-.01em;-webkit-text-stroke:5px #000;paint-order:stroke fill}
  </style><span id="m"></span>`);
  await p.evaluate(() => document.fonts.ready);
  const w = await p.evaluate(list => { const m=document.getElementById('m'); const o={};
    for (const s of list){ m.textContent=s; o[s]=m.getBoundingClientRect().width; } return o; }, texts);
  fs.writeFileSync('sub_widths2.json', JSON.stringify(w));
  const over = Object.entries(w).filter(([,v])=>v>1560);
  console.log('measured', Object.keys(w).length, '| over 1560px:', over.length);
  over.slice(0,6).forEach(([t,v])=>console.log('  ', Math.round(v), t));
  await b.close();
})();
