// Motion for the composition — one paused GSAP timeline, seeked by HyperFrames.
// Structure per scene: entrance → settle → subtle drift → beat accents → exit.
var full = gsap.timeline({ paused: true });

function Q(sel) { return document.querySelectorAll(sel); }
function T(sel, from, to, at) {
  if (!document.querySelector(sel)) return;
  full.fromTo(sel, from, to, at);
}
function beatAt(s, spec) {
  // "k" or "k+0.9": line k of the group, optionally offset in seconds
  var p = String(spec).split("+"), k = parseInt(p[0], 10), off = p[1] ? parseFloat(p[1]) : 0;
  k = Math.max(0, Math.min(k, s.b.length - 1));
  return s.t + s.b[k] + off;
}
function lenOf(el) {
  try { return el.getTotalLength(); } catch (e) { return 1200; }
}

// plates drift so no frame is ever dead still (Ken Burns on photos too)
SC.forEach(function (s) {
  var id = "#bgm" + String(s.i).padStart(3, "0");
  var dir = (s.i % 2) ? 1 : -1;
  full.fromTo(id, { scale: 1.0, xPercent: 0 },
    { scale: 1.05, xPercent: dir * 1.1, duration: Math.max(1, s.d), ease: "sine.inOut" }, s.t);
});

SC.forEach(function (s) {
  if (!s.has) return;
  var f = "#fg" + String(s.i).padStart(3, "0"), t = s.t + 0.06;
  var dur = Math.min(0.6, Math.max(0.32, s.d * 0.3));
  var root = document.querySelector(f);

  // micro-motion on the whole content layer: slow push + tiny drift
  full.fromTo(f + " .fgm", { scale: 1.0, y: 6 },
    { scale: 1.028, y: -8, duration: Math.max(1, s.d), ease: "sine.inOut" }, s.t);

  // entrances by kind
  if (s.k === "T") {
    // lines are revealed by their beats below
  } else if (s.k === "K") {
    T(f + " .bub", { scale: 0.94, opacity: 0, yPercent: 8 },
      { scale: 1, opacity: 1, yPercent: 0, duration: dur, ease: "back.out(1.4)" }, t);
  } else if (s.k === "H") {
    T(f + " .pearl", { scale: 0.3, opacity: 0 },
      { scale: 1, opacity: 1, duration: 0.6, ease: "back.out(1.6)" }, t);
    T(f + " .chap-word", { yPercent: 50, opacity: 0 },
      { yPercent: 0, opacity: 1, duration: 0.55, ease: "power3.out" }, t + 0.18);
  } else if (s.k === "C") {
    T(f + " .cut", { yPercent: 6, opacity: 0 },
      { yPercent: 0, opacity: 1, duration: dur, ease: "power2.out", stagger: 0.12 }, t);
    T(f + " .cut img", { x: -10 }, { x: 10, duration: Math.max(1, s.d), ease: "sine.inOut" }, t);
  } else if (s.k === "I") {
    T(f + " .icon3d", { scale: 0.86, opacity: 0, y: 30 },
      { scale: 1, opacity: 1, y: 0, duration: dur + 0.1, ease: "back.out(1.3)" }, t);
    // settle, then float — or ride, if this icon is a roller coaster
    var ride = s.fx === "coaster";
    var n = Math.max(1, Math.floor((s.d - 0.8) / (ride ? 0.9 : 1.6)));
    if (document.querySelector(f + " .icwrap"))
      full.to(f + " .icwrap", { y: ride ? -34 : -14, rotation: ride ? 3 : 1.2, duration: ride ? 0.45 : 0.8,
        ease: "sine.inOut", yoyo: true, repeat: n * 2 - 1 }, t + dur + 0.05);
  } else if (s.k === "P") {
    T(f + " .pmark", { opacity: 0, scale: 0.84 },
      { opacity: 1, scale: 1, duration: 0.5, ease: "back.out(1.5)" }, t);
    T(f + " .hl", { opacity: 0, yPercent: 26 },
      { opacity: 1, yPercent: 0, duration: 0.46, ease: "power2.out" }, t + 0.12);
  } else if (s.k === "M") {
    T(f + " .phone", { opacity: 0, y: 40, scale: 0.97 },
      { opacity: 1, y: 0, scale: 1, duration: 0.5, ease: "power3.out" }, t);
  } else if (s.k === "B") {
    // photo plate only; overlays ride beats
  } else {
    T(f + " .gtitle", { yPercent: 40, opacity: 0 },
      { yPercent: 0, opacity: 1, duration: 0.45, ease: "power3.out" }, t);
    T(f + " .diag svg, " + f + " .stage > svg", { opacity: 0, scale: 0.96 },
      { opacity: 1, scale: 1, duration: dur, ease: "power2.out" }, t);
    T(f + " .row:not([data-b]), " + f + " .chip, " + f + " .bars > div, " + f + " .stk",
      { yPercent: 36, opacity: 0 },
      { yPercent: 0, opacity: 1, duration: 0.46, ease: "power3.out", stagger: 0.08 }, t + 0.14);
    T(f + " .bar-fill", { scaleX: 0 },
      { scaleX: 1, duration: 0.8, ease: "expo.out", stagger: 0.1 }, t + 0.3);
    T(f + " .pmark", { opacity: 0, scale: 0.84 },
      { opacity: 1, scale: 1, duration: 0.52, ease: "back.out(1.6)" }, t + 0.06);
    T(f + " .sub:not([data-b]), " + f + " .gapline",
      { opacity: 0, yPercent: 26 },
      { opacity: 1, yPercent: 0, duration: 0.46, ease: "power2.out", stagger: 0.08 }, t + 0.1);
  }
  if (!root) return;

  // legacy figure hooks: strokes draw, end dots pop, gauges fill
  root.querySelectorAll(".fg-draw, .fg-draw2").forEach(function (el, n) {
    var L = lenOf(el);
    full.fromTo(el, { strokeDasharray: L, strokeDashoffset: L },
      { strokeDashoffset: 0, duration: Math.min(1.4, s.d * 0.6), ease: "power2.inOut" }, t + 0.15 + n * 0.25);
  });
  root.querySelectorAll(".fg-pop").forEach(function (el) {
    full.fromTo(el, { scale: 0, transformOrigin: "50% 50%" },
      { scale: 1, duration: 0.4, ease: "back.out(2)" }, t + Math.min(1.5, s.d * 0.6));
  });
  root.querySelectorAll(".fg-fill").forEach(function (el) {
    full.fromTo(el, { scaleY: 0, transformOrigin: "50% 100%" },
      { scaleY: 1, duration: 1.0, ease: "power2.out" }, t + 0.2);
  });

  // ── beat system ───────────────────────────────────────────────────────
  root.querySelectorAll("[data-b]").forEach(function (el) {
    var at = beatAt(s, el.getAttribute("data-b")) + (el.getAttribute("data-b") === "0" ? 0.08 : 0);
    var isSvg = el instanceof SVGElement;
    full.fromTo(el, isSvg ? { opacity: 0 } : { opacity: 0, y: 22 },
      isSvg ? { opacity: 1, duration: 0.4, ease: "power2.out" }
            : { opacity: 1, y: 0, duration: 0.42, ease: "power3.out" }, at);
  });
  root.querySelectorAll("[data-bo]").forEach(function (el) {
    full.to(el, { opacity: 0, duration: 0.3, ease: "power1.in" }, beatAt(s, el.getAttribute("data-bo")));
  });
  root.querySelectorAll("[data-bu]").forEach(function (el) {
    full.to(el, { y: -150, scale: 0.9, opacity: 0.35, duration: 0.6, ease: "power2.inOut" },
      beatAt(s, el.getAttribute("data-bu")));
  });
  root.querySelectorAll("[data-bs]").forEach(function (el) {
    var at = beatAt(s, el.getAttribute("data-bs"));
    full.fromTo(el, { scaleX: 0 }, { scaleX: 1, duration: 0.35, ease: "power2.out" }, at);
    var host = el.closest(".tline, .row, .msg");
    if (host) full.to(host, { opacity: 0.5, duration: 0.3 }, at + 0.1);
  });
  root.querySelectorAll("[data-bd]").forEach(function (el) {
    var L = lenOf(el);
    full.fromTo(el, { strokeDasharray: L, strokeDashoffset: L },
      { strokeDashoffset: 0, duration: 0.9, ease: "power2.inOut" }, beatAt(s, el.getAttribute("data-bd")) + 0.05);
  });
  root.querySelectorAll("[data-tw]").forEach(function (el) {
    var n = Math.max(4, el.textContent.length);
    full.fromTo(el, { clipPath: "inset(0 100% 0 0)" },
      { clipPath: "inset(0 0% 0 0)", duration: Math.min(0.9, n * 0.06), ease: "steps(" + n + ")" },
      beatAt(s, el.getAttribute("data-tw")) + 0.05);
    if (el.hasAttribute("data-te"))
      full.to(el, { clipPath: "inset(0 100% 0 0)", duration: 0.3, ease: "steps(" + n + ")" },
        beatAt(s, el.getAttribute("data-te")));
  });
  root.querySelectorAll("[data-gy]").forEach(function (el) {
    gsap.set(el, { transformOrigin: "50% 100%", scaleY: 0.08 });
    el.getAttribute("data-gy").split(",").forEach(function (kv) {
      var p = kv.split(":");
      full.to(el, { scaleY: parseFloat(p[1]), duration: 0.8, ease: "power2.inOut" }, beatAt(s, p[0]) + 0.1);
    });
  });
  root.querySelectorAll("[data-rot]").forEach(function (el) {
    el.getAttribute("data-rot").split(",").forEach(function (kv) {
      var p = kv.split(":");
      full.to(el, { rotation: parseFloat(p[1]), duration: 0.9, ease: "power2.inOut",
        svgOrigin: "500 330" }, beatAt(s, p[0]) + 0.1);
    });
  });
  root.querySelectorAll("[data-spin]").forEach(function (el) {
    full.fromTo(el, { rotation: 0, svgOrigin: "500 330" },
      { rotation: 720, svgOrigin: "500 330", duration: s.d, ease: "none" }, s.t);
  });
  root.querySelectorAll("[data-rip]").forEach(function (el) {
    var k = parseInt(el.getAttribute("data-rip"), 10);
    var reps = Math.max(0, Math.floor((s.d - 0.2) / 1.5) - 1);
    full.fromTo(el, { scale: 0.7, opacity: 0.8, transformOrigin: "50% 50%" },
      { scale: 1.9, opacity: 0, duration: 1.5, ease: "power1.out", repeat: reps }, s.t + 0.2 + k * 0.5);
  });
  root.querySelectorAll("[data-join]").forEach(function (el) {
    full.fromTo(el, { x: 260 }, { x: 0, duration: 1.1, ease: "power3.inOut" }, beatAt(s, el.getAttribute("data-join")) + 0.1);
  });
  root.querySelectorAll("[data-warn]").forEach(function (el) {
    full.to(el, { borderColor: "rgba(216,179,104,.95)", boxShadow: "0 0 40px rgba(216,179,104,.35)",
      duration: 0.5 }, beatAt(s, el.getAttribute("data-warn")));
  });
  root.querySelectorAll(".fs-her").forEach(function (el) {
    full.to(el, { flexGrow: 0.0001, width: 0, padding: 0, borderWidth: 0, marginLeft: -14, duration: 0.8,
      ease: "power2.inOut" }, beatAt(s, 6));
  });
  root.querySelectorAll(".sep-l, .sep-r").forEach(function (el) {
    var dir = el.classList.contains("sep-l") ? -60 : 60;
    full.to(el, { x: dir, duration: 0.9, ease: "power2.out" }, beatAt(s, 6) + 0.1);
  });
  root.querySelectorAll(".dragger, .dragged").forEach(function (el) {
    full.fromTo(el, { x: 0 }, { x: -70, duration: s.d, ease: "sine.inOut" }, s.t);
  });
  root.querySelectorAll(".caret").forEach(function (el) {
    var reps = Math.max(1, Math.floor(s.d / 0.5));
    full.fromTo(el, { opacity: 1 }, { opacity: 0, duration: 0.25, ease: "steps(1)", yoyo: true, repeat: reps }, s.t);
  });
  root.querySelectorAll(".cta-ar").forEach(function (el) {
    var reps = Math.max(1, Math.floor(s.d / 0.8) - 1);
    full.fromTo(el, { y: -6 }, { y: 10, duration: 0.4, ease: "sine.inOut", yoyo: true, repeat: reps }, s.t + 1);
  });
  root.querySelectorAll(".stamp").forEach(function (el) {
    var at = beatAt(s, el.getAttribute("data-b"));
    full.fromTo(el, { scale: 1.6, rotation: -14 }, { scale: 1, rotation: -8, duration: 0.35, ease: "power3.out" }, at);
  });
  root.querySelectorAll(".kk").forEach(function (el) {
    full.fromTo(el, { scale: 0.7, opacity: 0, transformOrigin: "50% 60%" },
      { scale: 1, opacity: 1, duration: 0.5, ease: "back.out(1.6)" }, s.t + 0.05);
    full.to(el, { scale: 1.12, duration: Math.max(0.6, s.d - 0.6), ease: "sine.inOut" }, s.t + 0.6);
  });
});

// captions: one line, fading up at each card's own start
CAPT.forEach(function (ct, c) {
  var cid = "#cap" + String(c).padStart(3, "0") + " .cap";
  T(cid, { opacity: 0, yPercent: 22 }, { opacity: 1, yPercent: 0, duration: 0.2, ease: "power2.out" }, ct);
});

// the composition timeline: the full film, or a slice of it for a segment render
var tl = gsap.timeline({ paused: true });
if (WIN[0] > 0 || WIN[1] < full.duration() - 0.001) {
  tl.add(full.tweenFromTo(WIN[0], WIN[1], { ease: "none", duration: WIN[1] - WIN[0] }), 0);
} else {
  full.paused(false);
  tl.add(full, 0);
}
window.__timelines = window.__timelines || {};
window.__timelines["main"] = tl;
