// Read SFX cue times from the built composition, using the same beat math as
// the timeline, so every sound lands on the visual it belongs to.
//   node scripts/sfx_events.mjs > renders/sfx.json   (project served on :8765)
import puppeteer from "puppeteer-core";

const browser = await puppeteer.launch({
  executablePath: process.env.CHROME || "/opt/pw-browsers/chromium-1194/chrome-linux/chrome",
  args: ["--no-sandbox", "--disable-gpu"],
});
const page = await browser.newPage();
await page.evaluateOnNewDocument(() => { window.__timelines = {}; });
await page.goto("http://127.0.0.1:8765/index.html", { waitUntil: "domcontentloaded", timeout: 180000 });
const ev = await page.evaluate(() => {
  const SCx = JSON.parse(document.body.innerHTML.match(/var SC = (\[.*?\]);/)[1]);
  const out = [];
  const beat = (s, el) => {
    if (el.dataset.t) return parseFloat(el.dataset.t) + parseFloat(el.dataset.o2 || "0");
    const base = el.hasAttribute("data-c")
      ? s.cb[Math.min(+el.dataset.c, s.cb.length - 1)]
      : s.lb[Math.min(+el.dataset.l, s.lb.length - 1)];
    return base + parseFloat(el.dataset.o || "0") + 0.06;
  };
  for (const s of SCx) {
    const root = document.getElementById("fg" + String(s.i).padStart(3, "0"));
    if (s.k === "H") out.push([s.t + 0.1, "impact"]);
    if (s.k === "T") out.push([s.t + 0.08, "soft"]);
    if (s.k === "K") out.push([s.t + 0.1, "click"]);
    if (!root) continue;
    root.querySelectorAll(".bt-show").forEach((el) => out.push([beat(s, el), "click"]));
    root.querySelectorAll(".notif").forEach((el) => out.push([beat(s, el), "click"]));
    root.querySelectorAll(".bt-draw").forEach((el) => out.push([beat(s, el), "draw"]));
    root.querySelectorAll(".fun-hl, .trk-hl, .dc-rate, .fun-break").forEach((el) => out.push([beat(s, el), "tick"]));
    root.querySelectorAll(".cta-btn").forEach((el) => out.push([beat(s, el), "impact"]));
    if (s.k === "S") out.push([s.t + 0.05, "whoosh"]);
    if (s.k === "D" && root.querySelector(".lnk.break")) out.push([s.t + 1.25, "snap"]);
  }
  return out.sort((a, b) => a[0] - b[0]);
});
console.log(JSON.stringify(ev));
await browser.close();
