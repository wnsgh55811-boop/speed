window.__timelines = window.__timelines || {};
var tl = gsap.timeline({ paused: true });
var E = "power3.out", LIME = "#C8FF3D";
function up(sel, t, o) {
  tl.fromTo(sel, { opacity: 0, y: 46 },
    Object.assign({ opacity: 1, y: 0, duration: 0.45, ease: E }, o || {}), t);
}
function pop(sel, t, o) {
  tl.fromTo(sel, { opacity: 0, scale: 0.6 },
    Object.assign({ opacity: 1, scale: 1, duration: 0.5, ease: "back.out(1.8)" }, o || {}), t);
}

// every scene: soft fade + slight push-in of the whole stage
Object.keys(SCENES).forEach(function (id) {
  var t = SCENES[id];
  tl.fromTo("#" + id + " .stage", { opacity: 0, scale: 1.04 },
            { opacity: 1, scale: 1, duration: 0.35, ease: E }, t);
});

// s1 hook — views stack up, then the question lands
up("#s1 .kicker", 0.05);
pop("#s1 .eyewrap", 0.15);
up("#s1 .views", 0.35);
tl.fromTo("#s1 .spark i", { scaleY: 0 }, { scaleY: 1, duration: 0.5, ease: E, stagger: 0.06 }, 0.5);
up("#s1 .s1hl", 1.25);
tl.fromTo("#s1 .s1hl em", { rotation: -25, scale: 0.4 }, { rotation: 0, scale: 1, duration: 0.5, ease: "back.out(3)" }, 1.45);

// s2 — a crowd watched, nobody bought, revenue zero
up("#s2 .label", 2.6);
tl.fromTo("#s2 .pcell", { opacity: 0, scale: 0.3 },
          { opacity: 1, scale: 1, duration: 0.3, ease: "back.out(2)", stagger: { each: 0.018, from: "random" } }, 2.65);
up("#s2 .cartrow", 3.62);
tl.to("#s2 .pcell", { opacity: 0.22, duration: 0.4 }, 3.62);
tl.fromTo("#s2 .zero", { opacity: 0, scale: 1.8, rotation: -8 },
          { opacity: 1, scale: 1, rotation: -4, duration: 0.35, ease: "power4.in" }, 4.75);
tl.fromTo("#s2 .stage", { x: 0 }, { x: 14, duration: 0.05, repeat: 5, yoyo: true, ease: "none" }, 5.1);

// s3 — exposure struck out, conversion takes the frame
up("#s3 .label", 6.25);
up("#s3 .w-dim", 6.4);
tl.fromTo("#s3 .strike", { scaleX: 0 }, { scaleX: 1, duration: 0.35, ease: "power2.inOut" }, 7.05);
up("#s3 .arrow", 7.5);
tl.fromTo("#s3 .w-hot", { opacity: 0, scale: 0.5 }, { opacity: 1, scale: 1, duration: 0.6, ease: "back.out(2)" }, 8.0);

// s4 — funnel builds top-down, a drop falls through
up("#s4 .label", 9.1);
tl.fromTo("#s4 .tier", { opacity: 0, scaleX: 0.4 }, { opacity: 1, scaleX: 1, duration: 0.4, ease: E, stagger: 0.22 }, 9.2);
tl.fromTo("#s4 .drop", { opacity: 0, y: -520 }, { opacity: 1, y: 0, duration: 0.6, ease: "bounce.out" }, 10.0);

// s5 — the three verbs light up on the beat
tl.fromTo("#s5 .step", { y: 46 }, { y: 0, duration: 0.3, ease: E, stagger: 0.04 }, 10.8);
[11.0, 11.95, 12.95].forEach(function (t, i) {
  var s = "#sp" + i;
  tl.to(s, { opacity: 1, duration: 0.2 }, t);
  tl.to(s + " .ic", { backgroundColor: LIME, borderColor: LIME, color: "#111", duration: 0.25 }, t);
  tl.fromTo(s + " .ic", { scale: 0.8 }, { scale: 1, duration: 0.45, ease: "back.out(3)" }, t);
});

// s6 — three-second ring fills while "3" holds
up("#s6 .label", 14.65);
pop("#s6 .sec", 14.8);
tl.fromTo("#s6 .tick", { opacity: 0 }, { opacity: 1, duration: 0.2, stagger: 0.02 }, 14.7);
tl.to("#s6 .tick", { backgroundColor: LIME, duration: 0.12, stagger: 0.1 }, 14.9);
up("#s6 .sub", 15.6);

// s7 — score, stars fill one by one, a real quote
up("#s7 .label", 16.9);
pop("#s7 .score", 17.0);
tl.fromTo("#s7 .sw", { opacity: 0, scale: 0, rotation: -60 },
          { opacity: 1, scale: 1, rotation: 0, duration: 0.35, ease: "back.out(2.5)", stagger: 0.09 }, 17.25);
up("#s7 .bubble", 17.7);
up("#s7 .meta", 17.95);

// s8 — one button, a cursor taps it
up("#s8 .label", 18.6);
pop("#s8 .cta", 18.75);
tl.fromTo("#s8 .cursor", { opacity: 0, x: 220, y: 260 }, { opacity: 1, x: 0, y: 0, duration: 0.6, ease: E }, 19.2);
tl.to("#s8 .cta", { scale: 0.93, duration: 0.1, yoyo: true, repeat: 1 }, 19.85);
tl.to("#s8 .cursor", { scale: 0.85, duration: 0.1, yoyo: true, repeat: 1 }, 19.85);
tl.fromTo("#s8 .ripple", { scale: 0, opacity: 0.8 }, { scale: 9, opacity: 0, duration: 0.6, ease: "power2.out" }, 19.9);
up("#s8 .sub", 20.0);

// s9 — same budget, bars 1% vs 2%, revenue doubles
up("#s9 .label", 20.65);
tl.fromTo("#s9 .grid i, #s9 .yaxis span", { opacity: 0 }, { opacity: 1, duration: 0.3, stagger: 0.04 }, 20.7);
up("#s9 .c1 .xl", 20.8);
tl.fromTo("#s9 .c1 .bar i", { scaleY: 0 }, { scaleY: 1, duration: 0.7, ease: E }, 20.9);
up("#s9 .c1 .val", 21.4);
up("#s9 .c2 .xl", 21.8);
tl.fromTo("#s9 .c2 .bar i", { scaleY: 0 }, { scaleY: 1, duration: 0.9, ease: E }, 21.9);
up("#s9 .c2 .val", 22.6);
up("#s9 .budget", 22.9);
pop("#s9 .double", 24.0);

// s10 — a crowd of dots, one lights up, it becomes the full stop
tl.fromTo("#s10 .dot", { opacity: 0, scale: 0 },
          { opacity: 1, scale: 1, duration: 0.3, ease: "back.out(2)", stagger: { each: 0.008, from: "center" } }, 25.25);
tl.fromTo("#s10 .hero", { scale: 1 }, { scale: 1.6, duration: 0.5, ease: "back.out(3)" }, 26.15);
tl.to("#s10 .dot:not(.hero)", { opacity: 0.08, duration: 0.5 }, 26.15);
up("#s10 .one", 26.3);
tl.to("#s10 .dots, #s10 .one", { opacity: 0, duration: 0.3 }, 27.2);
up("#s10 .end small", 27.45);
tl.fromTo("#s10 .end", { opacity: 0 }, { opacity: 1, duration: 0.01 }, 27.45);
tl.fromTo("#s10 .end", { scale: 0.85 }, { scale: 1, duration: 0.6, ease: "back.out(2)" }, 27.6);
pop("#s10 .period", 28.1, { ease: "back.out(4)" });

// captions fade up on their own starts
CAPS.forEach(function (t, i) {
  var id = "#cap" + String(i).padStart(2, "0") + " .cap";
  tl.fromTo(id, { opacity: 0, y: 18 }, { opacity: 1, y: 0, duration: 0.18, ease: "power2.out" }, t);
});

window.__timelines["main"] = tl;
