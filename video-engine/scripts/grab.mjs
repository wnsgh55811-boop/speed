// Frame grabber for QA: seeks the paused GSAP timeline the same way the
// renderer does and screenshots real pixels.
//   node scripts/grab.mjs <outdir> t1,t2,...   (serve the project on :8765 first)
import puppeteer from "puppeteer-core";
import fs from "fs";

const [out, list] = process.argv.slice(2);
fs.mkdirSync(out, { recursive: true });
const browser = await puppeteer.launch({
  executablePath: process.env.CHROME || "/opt/pw-browsers/chromium-1194/chrome-linux/chrome",
  args: ["--no-sandbox", "--disable-gpu", "--autoplay-policy=no-user-gesture-required"],
});
const page = await browser.newPage();
await page.setViewport({ width: 1920, height: 1080 });
await page.evaluateOnNewDocument(() => { window.__timelines = {}; });
await page.goto("http://127.0.0.1:8765/index.html", { waitUntil: "networkidle0", timeout: 180000 });
await page.evaluate(() => document.fonts.ready);
for (const t of list.split(",").map(Number)) {
  await page.evaluate((t) => {
    window.__timelines.main.time(t);
    document.querySelectorAll("#root .clip").forEach((el) => {
      const s = parseFloat(el.dataset.start) || 0, d = parseFloat(el.dataset.duration) || 0;
      el.style.visibility = t >= s && t < s + d ? "visible" : "hidden";
    });
  }, t);
  await new Promise((r) => setTimeout(r, 120));
  await page.screenshot({ path: `${out}/t${t.toFixed(1).padStart(6, "0")}.png` });
}
await browser.close();
