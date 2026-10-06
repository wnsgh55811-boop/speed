// Timeline for scenes.py compositions. Expects SC (scene meta) and CAPN.
var tl = gsap.timeline({ paused: true });
var XF = 0;     // scenes no longer overlap (see scenes.py XF)
function pad(n) { return String(n).padStart(3, "0"); }

// plates drift so no frame is ever dead still
SC.forEach(function (s, i) {
  var dir = (i % 2) ? 1 : -1;
  tl.fromTo("#bm" + s.id, { scale: s.ph ? 1.06 : 1.0, xPercent: 0 },
    { scale: s.ph ? 1.0 : 1.045, xPercent: dir * 0.9, duration: s.d, ease: "sine.inOut" }, s.t);
  // content breathes a touch over the scene
  tl.fromTo("#fi" + s.id, { scale: 1 }, { scale: 1.018, duration: s.d, ease: "none" }, s.t);
  // quick, clean hand-off: the old content clears in 0.12s, the new one is up in 0.2s
  if (s.fin) tl.fromTo("#fi" + s.id, { opacity: 0 }, { opacity: 1, duration: 0.2, ease: "power1.out" }, s.t);
  if (!s.last && s.d > 0.6) tl.to("#fi" + s.id, { opacity: 0, duration: 0.12, ease: "power1.in" }, s.t + s.d - 0.12);
});

// the cold open hits on frame 0: no fade from black, a fast push-in instead
if (SC.length && SC[0].first) tl.fromTo("#bm" + SC[0].id, { scale: 1.16 }, { scale: 1.04, duration: 1.2, ease: "expo.out" }, 0);

// Long, soft-landing entrances: nothing snaps, nothing bounces past its mark.
var FX = {
  up:    [{ opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: 0.6, ease: "power3.out" }],
  rise:  [{ opacity: 0, yPercent: 30 }, { opacity: 1, yPercent: 0, duration: 0.6, ease: "power3.out" }],
  left:  [{ opacity: 0, x: -48 }, { opacity: 1, x: 0, duration: 0.6, ease: "power3.out" }],
  fade:  [{ opacity: 0 }, { opacity: 1, duration: 0.45, ease: "power1.out" }],
  pop:   [{ opacity: 0, scale: 0.88 }, { opacity: 1, scale: 1, duration: 0.6, ease: "power3.out" }],
  msg:   [{ opacity: 0, y: 28, scale: 0.96 }, { opacity: 1, y: 0, scale: 1, duration: 0.55, ease: "power3.out" }],
  slam:  [{ opacity: 0, scale: 1.12, y: 18 }, { opacity: 1, scale: 1, y: 0, duration: 0.7, ease: "expo.out" }],
  stamp: [{ opacity: 0, scale: 1.6, rotation: -14 }, { opacity: 1, scale: 1, rotation: -8, duration: 0.5, ease: "power3.out" }],
  strike:[{ scaleX: 0 }, { scaleX: 1, duration: 0.6, ease: "power2.inOut" }],
  dim:   [{ opacity: 0 }, { opacity: 1, duration: 0.5, ease: "power1.out" }],
  grow:  [{ scaleY: 0 }, { scaleY: 1, duration: 0.9, ease: "power3.out" }],
  slideL:[{ xPercent: -100 }, { xPercent: 0, duration: 0.8, ease: "power3.out" }],
  slideR:[{ xPercent: 100 }, { xPercent: 0, duration: 0.8, ease: "power3.out" }],
  mark:  [{ scaleX: 0 }, { scaleX: 1, duration: 0.7, ease: "power2.inOut" }],
  mask:  [{ yPercent: 110 }, { yPercent: 0, duration: 0.7, ease: "power3.out" }],
  inL:   [{ opacity: 0, x: -160 }, { opacity: 1, x: 0, duration: 0.7, ease: "power3.out" }],
  inR:   [{ opacity: 0, x: 160 }, { opacity: 1, x: 0, duration: 0.7, ease: "power3.out" }]
};

// Lines draw from their root to their tip. Lengths are measured, not assumed:
// a pathLength + CSS dash combination silently skipped the animation before,
// so the strokes just popped in.
function drawPath(el, t, dur) {
  el.removeAttribute("pathLength");
  var L = el.getTotalLength();
  el.style.strokeDasharray = "";
  el.setAttribute("stroke-dasharray", L + " " + L);
  tl.fromTo(el, { attr: { "stroke-dashoffset": L } }, { attr: { "stroke-dashoffset": 0 }, duration: dur, ease: "power1.inOut" }, t);
  return L;
}


document.querySelectorAll("[data-at]").forEach(function (el) {
  var t = parseFloat(el.getAttribute("data-at"));
  var fx = el.getAttribute("data-fx");
  var sel = "#" + el.id;
  if (fx === "draw") {
    var dur = parseFloat(el.getAttribute("data-dur")) || 1.5;
    var L = drawPath(el, t, dur);
    // chart lines carry a glowing tip that rides the end of the stroke
    if (el.classList.contains("sline")) {
      var tip = document.createElementNS("http://www.w3.org/2000/svg", "circle");
      tip.setAttribute("r", "11"); tip.setAttribute("class", "stip " + (el.getAttribute("class") || ""));
      el.parentNode.appendChild(tip);
      var p0 = el.getPointAtLength(0); tip.setAttribute("cx", p0.x); tip.setAttribute("cy", p0.y);
      tl.fromTo(tip, { opacity: 0 }, { opacity: 1, duration: 0.2 }, t);
      var o2 = { u: 0 };
      tl.to(o2, { u: 1, duration: dur, ease: "power1.inOut", onUpdate: function () {
        var p = el.getPointAtLength(L * o2.u); tip.setAttribute("cx", p.x); tip.setAttribute("cy", p.y); } }, t);
    }
  } else if (fx === "ring") {
    var C = parseFloat(el.getAttribute("data-c"));
    var r0 = parseFloat(el.getAttribute("data-from")), r1 = parseFloat(el.getAttribute("data-to"));
    tl.fromTo(el, { attr: { "stroke-dashoffset": C * (1 - r0) } }, { attr: { "stroke-dashoffset": C * (1 - r1) }, duration: 1.8, ease: "power2.inOut" }, t);
  } else if (fx === "meter") {
    var a = parseFloat(el.getAttribute("data-from")), b = parseFloat(el.getAttribute("data-to"));
    tl.fromTo(sel, { xPercent: (a - 1) * 100 }, { xPercent: (b - 1) * 100, duration: 1.7, ease: "power2.inOut" }, t);
  } else if (fx === "knob") {
    var p = parseFloat(el.getAttribute("data-pos"));
    tl.fromTo(sel, { x: 0 }, { x: (p - 0.5) * 640, duration: 1.3, ease: "power2.inOut" }, t);
  } else if (fx === "gap") {
    var g0 = parseFloat(el.getAttribute("data-from")), g1 = parseFloat(el.getAttribute("data-to"));
    var dx = (g0 - g1) / 2;
    tl.fromTo(sel + " .dp:not(.her)", { x: 0 }, { x: dx, duration: 1.6, ease: "power2.inOut" }, t);
    tl.fromTo(sel + " .dp.her", { x: 0 }, { x: -dx, duration: 1.6, ease: "power2.inOut" }, t);
    tl.fromTo(sel + " .dline", { scaleX: 1 }, { scaleX: Math.max(0.02, g1 / g0), duration: 1.6, ease: "power2.inOut" }, t);
  } else if (fx === "tilt") {
    tl.fromTo(sel + " .beam", { rotation: 0 }, { rotation: -9, duration: 1.5, ease: "sine.inOut" }, t);
    var lv = el.getAttribute("data-level-at");
    if (lv) tl.to(sel + " .beam", { rotation: 0, duration: 1.5, ease: "sine.inOut" }, parseFloat(lv));
  } else if (fx === "count") {
    var o = { v: 0 }, n = parseInt(el.getAttribute("data-count"), 10);
    tl.fromTo(el, { opacity: 0 }, { opacity: 1, duration: 0.5, ease: "sine.inOut" }, t);
    tl.to(o, { v: n, duration: 1.1, ease: "power1.out",
      onUpdate: function () { el.textContent = Math.round(o.v) + "개"; } }, t);
  } else if (FX[fx]) {
    tl.fromTo(sel, FX[fx][0], FX[fx][1], t);
  }
  // checklist rows tick their box a beat after they land
  if (el.classList.contains("chk")) drawPath(el.querySelector(".tickpath"), t + 0.25, 0.45);
  if (el.hasAttribute("data-out-at"))
    tl.to(sel, { opacity: 0, scale: 0.6, duration: 0.4, ease: "power2.in" }, parseFloat(el.getAttribute("data-out-at")));
  if (el.hasAttribute("data-shrink-at"))
    tl.to(sel, { scale: 0.72, opacity: 0.4, duration: 0.6, ease: "power2.inOut" }, parseFloat(el.getAttribute("data-shrink-at")));
});

// Rows that reveal left → right (chips, cards, A → B): the row slides so the
// part already on screen stays optically centred, instead of hugging the left
// while the later items are still invisible.
document.querySelectorAll(".flow, .cards, .morph").forEach(function (row, i) {
  var kids = Array.prototype.filter.call(row.children, function (el) { return el.hasAttribute("data-at"); });
  if (kids.length < 2) return;
  row.id = row.id || "rw" + i;
  var W = row.offsetWidth, steps = [];
  kids.forEach(function (el) {
    steps.push({ t: parseFloat(el.getAttribute("data-at")), r: el.offsetLeft + el.offsetWidth });
  });
  steps.sort(function (a, b) { return a.t - b.t; });
  // items that arrive together (a card and its "vs") make ONE glide — two
  // overlapping tweens on the same x fight each other and the row stalls
  var merged = [];
  steps.forEach(function (st) {
    var m = merged[merged.length - 1];
    if (m && st.t - m.t < 0.05) m.r = Math.max(m.r, st.r); else merged.push({ t: st.t, r: st.r });
  });
  steps = merged;
  var maxR = 0, last = null;
  steps.forEach(function (st, n) {
    maxR = Math.max(maxR, st.r);
    var dx = (W - maxR) / 2;
    if (n === 0) tl.set("#" + row.id, { x: dx }, 0);
    // finish the slide before the new item lands, so nothing pokes past the frame
    // glide while the new item eases in, so the row and the reveal move as one
    else if (dx !== last) tl.to("#" + row.id, { x: dx, duration: 0.9, ease: "power2.inOut" }, Math.max(0, st.t - 0.65));
    last = dx;
  });
});

// generic mover: data-path = [[t, x, y], ...]; first entry sets, the rest glide in
document.querySelectorAll("[data-path]").forEach(function (el, i) {
  var pts = JSON.parse(el.getAttribute("data-path"));
  el.id = el.id || "mv" + i;
  tl.set("#" + el.id, { x: pts[0][1], y: pts[0][2] }, 0);
  for (var k = 1; k < pts.length; k++)
    tl.to("#" + el.id, { x: pts[k][1], y: pts[k][2], duration: 0.8, ease: "power2.inOut" }, Math.max(pts[0][0], pts[k][0] - 0.8));
});

// micro-motion that keeps long holds alive
document.querySelectorAll(".floaty").forEach(function (el, i) {
  var clip = el.closest(".clip"), s = parseFloat(clip.getAttribute("data-start")),
      d = parseFloat(clip.getAttribute("data-duration"));
  var reps = Math.max(0, Math.floor(d / 1.8) - 1);
  if (!el.id) el.id = "fl" + i;
  if (reps) tl.fromTo("#" + el.id, { y: 0 }, { y: -14, duration: 0.9, ease: "sine.inOut", yoyo: true, repeat: reps }, s + 0.6);
});
document.querySelectorAll(".orb").forEach(function (el, i) {
  var clip = el.closest(".clip"), s = parseFloat(clip.getAttribute("data-start")),
      d = parseFloat(clip.getAttribute("data-duration"));
  el.id = el.id || "orb" + i;
  var o = { a: 0 };
  tl.to(o, { a: Math.PI * 2 * Math.max(1, Math.round(d / 2.6)), duration: d, ease: "none",
    onUpdate: function () { el.setAttribute("cx", 300 + 290 * Math.cos(o.a)); el.setAttribute("cy", 110 + 70 * Math.sin(o.a)); } }, s);
});
document.querySelectorAll(".think-bub .tdot").forEach(function (el, i) {
  el.id = el.id || "td" + i;
  tl.fromTo("#" + el.id, { opacity: 0.25, y: 0 }, { opacity: 1, y: -8, duration: 0.3, ease: "sine.inOut",
    yoyo: true, repeat: 7 }, 0.15 + (i % 3) * 0.14);
});
document.querySelectorAll(".chat-dot").forEach(function (el, i) {
  var clip = el.closest(".clip"), s = parseFloat(clip.getAttribute("data-start")),
      d = parseFloat(clip.getAttribute("data-duration"));
  el.id = el.id || "cd" + i;
  var reps = Math.max(1, Math.floor(d / 1.2));
  var w = parseFloat(el.closest(".dist").getAttribute("data-gap")) || 600;
  tl.fromTo("#" + el.id, { x: 0, opacity: 0 }, { x: w, opacity: 1, duration: 1.2, ease: "none",
    repeat: reps, yoyo: true }, s + 0.4 + (i % 5) * 0.22);
});

// captions: no entrance, no exit — the text simply changes on its cue

window.__timelines = window.__timelines || {};
window.__timelines["main"] = tl;
