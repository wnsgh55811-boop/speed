// Timeline for scenes.py compositions. Expects SC (scene meta) and CAPN.
var tl = gsap.timeline({ paused: true });
function pad(n) { return String(n).padStart(3, "0"); }

// plates drift so no frame is ever dead still
SC.forEach(function (s, i) {
  var dir = (i % 2) ? 1 : -1;
  tl.fromTo("#bm" + s.id, { scale: s.ph ? 1.06 : 1.0, xPercent: 0 },
    { scale: s.ph ? 1.0 : 1.045, xPercent: dir * 0.9, duration: s.d, ease: "sine.inOut" }, s.t);
  // content breathes a touch over the scene, then clears just before the cut
  tl.fromTo("#fi" + s.id, { scale: 1 }, { scale: 1.018, duration: s.d, ease: "none" }, s.t);
  if (!s.last && s.d > 0.8)
    tl.to("#fi" + s.id, { opacity: 0, duration: 0.16, ease: "power1.in" }, s.t + s.d - 0.16);
});

// the cold open hits on frame 0: no fade from black, a fast push-in instead
if (SC.length && SC[0].first) tl.fromTo("#bm" + SC[0].id, { scale: 1.16 }, { scale: 1.04, duration: 1.2, ease: "expo.out" }, 0);

var FX = {
  up:    [{ opacity: 0, y: 34 }, { opacity: 1, y: 0, duration: 0.5, ease: "power3.out" }],
  rise:  [{ opacity: 0, yPercent: 40 }, { opacity: 1, yPercent: 0, duration: 0.55, ease: "power3.out" }],
  left:  [{ opacity: 0, x: -40 }, { opacity: 1, x: 0, duration: 0.45, ease: "power3.out" }],
  fade:  [{ opacity: 0 }, { opacity: 1, duration: 0.4, ease: "power1.out" }],
  pop:   [{ opacity: 0, scale: 0.82 }, { opacity: 1, scale: 1, duration: 0.55, ease: "back.out(1.6)" }],
  msg:   [{ opacity: 0, y: 26, scale: 0.94 }, { opacity: 1, y: 0, scale: 1, duration: 0.42, ease: "back.out(1.5)" }],
  slam:  [{ opacity: 0, scale: 1.35 }, { opacity: 1, scale: 1, duration: 0.42, ease: "power4.out" }],
  stamp: [{ opacity: 0, scale: 2.2, rotation: -14 }, { opacity: 1, scale: 1, rotation: -8, duration: 0.38, ease: "power4.in" }],
  strike:[{ scaleX: 0 }, { scaleX: 1, duration: 0.35, ease: "power2.inOut" }],
  draw:  [{ strokeDashoffset: 1 }, { strokeDashoffset: 0, duration: 1.1, ease: "power2.inOut" }],
  dim:   [{ opacity: 0 }, { opacity: 1, duration: 0.4, ease: "power1.out" }]
};

document.querySelectorAll("[data-at]").forEach(function (el) {
  var t = parseFloat(el.getAttribute("data-at"));
  var fx = el.getAttribute("data-fx");
  var sel = "#" + el.id;
  if (fx === "meter") {
    var a = parseFloat(el.getAttribute("data-from")), b = parseFloat(el.getAttribute("data-to"));
    tl.fromTo(sel, { xPercent: (a - 1) * 100 }, { xPercent: (b - 1) * 100, duration: 1.3, ease: "power2.inOut" }, t);
  } else if (fx === "knob") {
    var p = parseFloat(el.getAttribute("data-pos"));
    tl.fromTo(sel, { x: 0 }, { x: (p - 0.5) * 640, duration: 0.9, ease: "power3.inOut" }, t);
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
  tl.fromTo("#cap" + pad(c) + " .cap", { opacity: 0, yPercent: 22 },
    { opacity: 1, yPercent: 0, duration: 0.18, ease: "power2.out" }, parseFloat(cel.getAttribute("data-start")));
}

window.__timelines = window.__timelines || {};
window.__timelines["main"] = tl;
