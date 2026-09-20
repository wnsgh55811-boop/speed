/* Single paused, seek-safe GSAP timeline. No clocks, no Math.random, no infinite repeats.
   Clip visibility is owned by the framework: we only animate CHILDREN of .clip. */
(function () {
  const TL = gsap.timeline({ paused: true });
  const meta = window.__HF_TIMING || [];
  const q = (sel, root) => Array.from((root || document).querySelectorAll(sel));

  /* film grain: deterministic stepped drift (finite repeat, seek-safe) */
  const grain = document.getElementById('grain');
  if (grain) {
    const steps = [[0,0],[-14,9],[7,-12],[-5,15],[12,4],[-10,-8]];
    steps.forEach((p, i) => TL.set(grain, { x: p[0], y: p[1] }, i * 0.1));
    const dur = Number(document.getElementById('root').dataset.duration) || 60;
    for (let t = 0.6; t < dur; t += 0.1) {
      const p = steps[Math.floor(t * 10) % steps.length];
      TL.set(grain, { x: p[0], y: p[1] }, t);
    }
  }

  /* subtitles: quick, clean in/out. Hard-killed at the clip edge by the framework. */
  q('#subs .sub').forEach((el) => {
    const s = Number(el.dataset.start), d = Number(el.dataset.duration);
    TL.fromTo(el, { opacity: 0, y: 10 }, { opacity: 1, y: 0, duration: 0.16, ease: 'power2.out' }, s);
    TL.to(el, { opacity: 0, duration: 0.14, ease: 'power2.in' }, s + Math.max(0.3, d - 0.14));
  });

  /* per-scene choreography, driven off each scene clip's own window */
  meta.forEach((m) => {
    const sc = document.getElementById('sc' + m.i);
    if (!sc) return;
    const st = m.start, inAt = st + 0.02;
    const stage = sc.querySelector('.stage');

    /* background bloom breathes very slightly so static frames never feel dead */
    const bloom = sc.querySelector('.bloom');
    if (bloom) TL.fromTo(bloom, { scale: 1.0, opacity: .86 },
      { scale: 1.06, opacity: 1, duration: Math.max(1, m.dur), ease: 'sine.inOut' }, st);

    /* stage lift-in */
    if (stage) {
      TL.fromTo(stage, { opacity: 0, y: 26 },
        { opacity: 1, y: 0, duration: 0.42, ease: 'power3.out' }, inAt);
      TL.to(stage, { opacity: 0, duration: 0.26, ease: 'power2.in' },
        st + Math.max(0.5, m.dur - 0.26));
    }

    /* photo slow push (Ken Burns) on the inner layer, never the timed clip */
    const photo = sc.querySelector('.photo');
    if (photo) TL.fromTo(photo, { scale: 1.04 }, { scale: 1.12, duration: m.dur, ease: 'none' }, st);

    /* staggered reveals */
    const rows = q('.rows .row', sc);
    rows.forEach((r, k) => TL.fromTo(r, { opacity: 0, x: -22 },
      { opacity: 1, x: 0, duration: 0.34, ease: 'power2.out' }, inAt + 0.26 + k * 0.30));

    const bubs = q('.bub', sc);
    bubs.forEach((b, k) => TL.fromTo(b, { opacity: 0, y: 18, scale: .97 },
      { opacity: 1, y: 0, scale: 1, duration: 0.34, ease: 'back.out(1.5)' }, inAt + 0.24 + k * 0.42));

    const cells = q('.icell', sc);
    cells.forEach((c, k) => TL.fromTo(c, { opacity: 0, y: 20 },
      { opacity: 1, y: 0, duration: 0.36, ease: 'power2.out' }, inAt + 0.26 + k * 0.22));

    /* BAR / METER / GAUGE fills: width driven from data-w (percent). Block-level + sized. */
    q('.fill,.meterf,.gfill', sc).forEach((f, k) => {
      const w = Number(f.dataset.w || 0);
      TL.fromTo(f, { width: '0%' },
        { width: w + '%', duration: 0.72, ease: 'power3.out' }, inAt + 0.40 + k * 0.18);
    });
    q('.gknob', sc).forEach((f) => {
      const w = Number(f.dataset.w || 0);
      const track = f.parentElement.getBoundingClientRect().width || 1180;
      TL.fromTo(f, { x: 0, yPercent: -50, xPercent: -50 },
        { x: track * w / 100, duration: 0.72, ease: 'power3.out' }, inAt + 0.40);
    });
    q('.dot.on', sc).forEach((d, k) => TL.fromTo(d, { scale: 0 },
      { scale: 1, duration: 0.20, ease: 'back.out(2)' }, inAt + 0.62 + k * 0.07));

    /* strike-through draws across its own word only */
    q('.strikeline', sc).forEach((l) => TL.fromTo(l, { scaleX: 0 },
      { scaleX: 1, duration: 0.34, ease: 'power2.inOut' }, inAt + 0.50));
    q('.xmark,.bubx,.xmark-s', sc).forEach((x, k) => TL.fromTo(x, { opacity: 0, scale: .5, rotate: -18 },
      { opacity: 1, scale: 1, rotate: 0, duration: 0.28, ease: 'back.out(2)' }, inAt + 0.76 + k * 0.16));

    /* grow-dot magnitude */
    q('.gsmall,.gbig', sc).forEach((g, k) => TL.fromTo(g, { scale: 0 },
      { scale: 1, duration: 0.44, ease: 'back.out(1.4)' }, inAt + 0.34 + k * 0.26));

    /* scale beam tips */
    q('.beam', sc).forEach((b) => TL.fromTo(b, { rotate: 0 },
      { rotate: -7, duration: 0.70, ease: 'power2.out' }, inAt + 0.40));

    /* mutual arrows */
    q('.ar', sc).forEach((a, k) => TL.fromTo(a, { scaleX: 0, transformOrigin: k ? '100% 50%' : '0% 50%' },
      { scaleX: 1, duration: 0.40, ease: 'power2.out' }, inAt + 0.40 + k * 0.14));

    /* ring pulse on hero */
    q('.ring', sc).forEach((r) => TL.fromTo(r, { scale: .82, opacity: 0 },
      { scale: 1.06, opacity: 1, duration: 0.9, ease: 'power2.out' }, inAt + 0.10));

    /* portrait paper card settle */
    q('.pcard', sc).forEach((p) => TL.fromTo(p, { opacity: 0, scale: .94, rotate: -1.2 },
      { opacity: 1, scale: 1, rotate: 0, duration: 0.55, ease: 'power3.out' }, inAt + 0.14));

    /* chapter number */
    q('.chapnum', sc).forEach((c) => TL.fromTo(c, { opacity: 0, y: -18 },
      { opacity: 1, y: 0, duration: 0.5, ease: 'power3.out' }, inAt + 0.06));
  });

  window.__timelines['main'] = TL;
  TL.seek(0);
})();
