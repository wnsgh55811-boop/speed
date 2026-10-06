// Timeline for scenes.py compositions. Expects SC (scene meta) and CAPN.
var tl = gsap.timeline({ paused: true });
function pad(n) { return String(n).padStart(3, "0"); }

// plates drift so no frame is ever dead still; scenes hand over with a
// crossfade — the outgoing clip runs on `x` seconds under the incoming one
SC.forEach(function (s, i) {
  var dir = (i % 2) ? 1 : -1, span = s.d + s.x;
  tl.fromTo("#bm" + s.id, { scale: s.ph ? 1.06 : 1.0, xPercent: 0 },
    { scale: s.ph ? 1.0 : 1.045, xPercent: dir * 0.9, duration: span, ease: "sine.inOut" }, s.t);
  // content breathes a touch over the scene
  tl.fromTo("#fi" + s.id, { scale: 1 }, { scale: 1.018, duration: span, ease: "sine.inOut" }, s.t);
  if (!s.first && i > 0) {
    var xin = SC[i - 1].x || 0.4;
    tl.fromTo("#bg" + s.id, { opacity: 0 }, { opacity: 1, duration: xin, ease: "sine.inOut" }, s.t);
    tl.fromTo("#fi" + s.id, { opacity: 0 }, { opacity: 1, duration: xin, ease: "sine.inOut" }, s.t);
  }
  if (s.x > 0)
    tl.to("#fi" + s.id, { opacity: 0, duration: s.x * 0.9, ease: "sine.inOut" }, s.t + s.d);
});

// the cold open is live on frame 0: a slow push-in, no fade from black
if (SC.length && SC[0].first) tl.fromTo("#bm" + SC[0].id, { scale: 1.12 }, { scale: 1.03, duration: 2.6, ease: "power2.out" }, 0);

// entrances: soft ease-outs, no overshoot, long enough to read as motion
var FX = {
  up:    [{ opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.75, ease: "power2.out" }],
  rise:  [{ opacity: 0, y: 36 }, { opacity: 1, y: 0, duration: 0.8, ease: "power3.out" }],
  left:  [{ opacity: 0, x: -34 }, { opacity: 1, x: 0, duration: 0.7, ease: "power2.out" }],
  fade:  [{ opacity: 0 }, { opacity: 1, duration: 0.6, ease: "sine.inOut" }],
  pop:   [{ opacity: 0, scale: 0.9 }, { opacity: 1, scale: 1, duration: 0.75, ease: "power3.out" }],
  msg:   [{ opacity: 0, y: 22, scale: 0.97 }, { opacity: 1, y: 0, scale: 1, duration: 0.6, ease: "power3.out" }],
  slam:  [{ opacity: 0, scale: 1.2 }, { opacity: 1, scale: 1, duration: 0.6, ease: "power3.out" }],
  stamp: [{ opacity: 0, scale: 1.8, rotation: -14 }, { opacity: 1, scale: 1, rotation: -8, duration: 0.5, ease: "power3.in" }],
  strike:[{ scaleX: 0 }, { scaleX: 1, duration: 0.6, ease: "power2.inOut" }],
  draw:  [{ strokeDashoffset: 1 }, { strokeDashoffset: 0, duration: 1.2, ease: "power2.inOut" }],
  dim:   [{ opacity: 0 }, { opacity: 1, duration: 0.6, ease: "sine.inOut" }],
  grow:  [{ scaleY: 0 }, { scaleY: 1, duration: 0.9, ease: "power3.out" }],
  type:  [{ clipPath: "inset(0 100% 0 0)" }, { clipPath: "inset(0 0% 0 0)", duration: 1.0, ease: "steps(14)" }]
};

document.querySelectorAll("[data-at]").forEach(function (el) {
  var t = parseFloat(el.getAttribute("data-at"));
  var fx = el.getAttribute("data-fx");
  var sel = "#" + el.id;
  if (fx === "meter") {
    var a = parseFloat(el.getAttribute("data-from")), b = parseFloat(el.getAttribute("data-to"));
    tl.fromTo(sel, { xPercent: (a - 1) * 100 }, { xPercent: (b - 1) * 100, duration: 1.3, ease: "power2.inOut" }, t);
    var th = el.getAttribute("data-then");
    if (th !== null) tl.to(sel, { xPercent: (parseFloat(th) - 1) * 100, duration: 0.9, ease: "power3.inOut" },
      parseFloat(el.getAttribute("data-then-at")));
  } else if (fx === "timer") {
    // the ring empties over the real number of seconds while the digit counts up
    var secs = parseFloat(el.getAttribute("data-secs")), num = el.querySelector(".t-num"), oc = { v: 0 };
    tl.fromTo(el, { opacity: 0, scale: 0.9 }, { opacity: 1, scale: 1, duration: 0.4, ease: "power3.out" }, t - 0.35);
    tl.fromTo(sel + " .t-ring", { strokeDashoffset: 0 }, { strokeDashoffset: 1, duration: secs, ease: "none" }, t);
    tl.fromTo(oc, { v: 0 }, { v: secs, duration: secs, ease: "none",
      onUpdate: function () { num.innerHTML = oc.v.toFixed(1) + "<small>초</small>"; } }, t);
    tl.fromTo(sel + " svg", { scale: 1 }, { scale: 1.04, duration: 0.5, ease: "sine.inOut", yoyo: true,
      repeat: Math.max(1, Math.round(secs * 2) - 1) }, t);
  } else if (fx === "flash") {
    tl.fromTo(sel, { opacity: 0 }, { opacity: 0.94, duration: 0.3, ease: "power2.in" }, t);
    tl.to(sel, { opacity: 0.0, duration: 0.8, ease: "power2.inOut" }, t + 0.9);
  } else if (fx === "knob") {
    var p = parseFloat(el.getAttribute("data-pos"));
    tl.fromTo(sel, { x: 0 }, { x: (p - 0.5) * 640, duration: 1.1, ease: "power2.inOut" }, t);
  } else if (fx === "gap") {
    var g0 = parseFloat(el.getAttribute("data-from")), g1 = parseFloat(el.getAttribute("data-to"));
    var dx = (g0 - g1) / 2;
    tl.fromTo(sel + " .dp:not(.her)", { x: 0 }, { x: dx, duration: 1.6, ease: "power2.inOut" }, t);
    tl.fromTo(sel + " .dp.her", { x: 0 }, { x: -dx, duration: 1.6, ease: "power2.inOut" }, t);
    tl.fromTo(sel + " .dline", { scaleX: 1 }, { scaleX: Math.max(0.02, g1 / g0), duration: 1.6, ease: "power2.inOut" }, t);
  } else if (fx === "tilt") {
    tl.fromTo(sel + " .beam", { rotation: 0 }, { rotation: -9, duration: 1.0, ease: "power2.inOut" }, t);
    var lv = el.getAttribute("data-level-at");
    if (lv) tl.to(sel + " .beam", { rotation: 0, duration: 1.0, ease: "power2.inOut" }, parseFloat(lv));
  } else if (fx === "count") {
    var o = { v: 0 }, n = parseInt(el.getAttribute("data-count"), 10);
    tl.fromTo(el, { opacity: 0 }, { opacity: 1, duration: 0.2 }, t);
    tl.to(o, { v: n, duration: 1.1, ease: "power1.out",
      onUpdate: function () { el.textContent = Math.round(o.v) + "개"; } }, t);
  } else if (FX[fx]) {
    tl.fromTo(sel, FX[fx][0], FX[fx][1], t);
  }
  // checklist rows tick their box a beat after they land
  if (el.classList.contains("chk"))
    tl.fromTo(sel + " .tickpath", { strokeDashoffset: 1 }, { strokeDashoffset: 0, duration: 0.35, ease: "power2.out" }, t + 0.25);
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
  var maxR = 0, last = null;
  steps.forEach(function (st, n) {
    maxR = Math.max(maxR, st.r);
    var dx = (W - maxR) / 2;
    if (n === 0) tl.set("#" + row.id, { x: dx }, 0);
    else if (dx !== last) tl.to("#" + row.id, { x: dx, duration: 0.8, ease: "power2.inOut" }, st.t - 0.75);
    last = dx;
  });
});

// a ringing alarm: a short, damped rattle that repeats while the scene holds
document.querySelectorAll("[data-shake-at]").forEach(function (el, i) {
  var clip = el.closest(".clip"), s = parseFloat(clip.getAttribute("data-start")),
      d = parseFloat(clip.getAttribute("data-duration")), t = parseFloat(el.getAttribute("data-shake-at"));
  var img = el.querySelector("img"); img.id = img.id || "sk" + i;
  for (var k = 0; t + k * 1.1 < s + d - 0.4; k++)
    tl.fromTo("#" + img.id, { rotation: 0 }, { keyframes: [{ rotation: -9, duration: 0.07 }, { rotation: 8, duration: 0.08 },
      { rotation: -6, duration: 0.08 }, { rotation: 4, duration: 0.09 }, { rotation: 0, duration: 0.12 }],
      ease: "sine.inOut", transformOrigin: "50% 12%" }, t + k * 1.1);
});
// paper cutouts lean in a few pixels over the scene, never fully still
document.querySelectorAll(".p-fig").forEach(function (el, i) {
  var clip = el.closest(".clip"), s = parseFloat(clip.getAttribute("data-start")),
      d = parseFloat(clip.getAttribute("data-duration"));
  var img = el.querySelector("img"); img.id = img.id || "pf" + i;
  tl.fromTo("#" + img.id, { x: 0, rotation: 0 }, { x: (i % 2 ? -18 : 18), rotation: (i % 2 ? -0.8 : 0.8), duration: d, ease: "sine.inOut" }, s);
});
// photo-quote bubbles and chips drift up a touch while they hold
document.querySelectorAll(".ph-msg, .ph-chip, .rad-chip").forEach(function (el, i) {
  var clip = el.closest(".clip"), s = parseFloat(clip.getAttribute("data-start")),
      d = parseFloat(clip.getAttribute("data-duration"));
  var w = document.createElement("div"); w.className = "drift"; w.id = "dr" + i;
  el.parentNode.insertBefore(w, el); w.appendChild(el);
  if (el.classList.contains("rad-chip")) { w.style.position = "absolute"; w.style.inset = "0"; }
  tl.fromTo("#" + w.id, { y: 0 }, { y: -12, duration: d, ease: "sine.inOut" }, s);
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

// captions: one line, fading up at each card's start
for (var c = 0; c < CAPN; c++) {
  var cel = document.getElementById("cap" + pad(c));
  if (cel.getAttribute("data-cont")) continue;   // carried over a part cut: already showing
  tl.fromTo("#cap" + pad(c) + " .cap", { opacity: 0, yPercent: 16 },
    { opacity: 1, yPercent: 0, duration: 0.24, ease: "power2.out" }, parseFloat(cel.getAttribute("data-start")));
}

window.__timelines = window.__timelines || {};
window.__timelines["main"] = tl;
