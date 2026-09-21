/* One paused, seek-safe GSAP timeline. Only children of .clip are animated;
   the framework owns clip visibility. No clocks, no randomness, finite repeats. */
(function () {
  const TL = gsap.timeline({ paused: true });
  const meta = window.__HF_TIMING || [];
  const q = (s, r) => Array.from((r || document).querySelectorAll(s));

  const grain = document.getElementById('grain');
  if (grain) {
    const steps = [[0,0],[-14,9],[7,-12],[-5,15],[12,4],[-10,-8]];
    const dur = Number(document.getElementById('root').dataset.duration) || 60;
    for (let t = 0; t < dur; t += 0.1) {
      const p = steps[Math.round(t * 10) % steps.length];
      TL.set(grain, { x: p[0], y: p[1] }, t);
    }
  }

  q('#subs .sub').forEach((el) => {
    const s = Number(el.dataset.start), d = Number(el.dataset.duration);
    TL.fromTo(el, { opacity: 0, y: 8 }, { opacity: 1, y: 0, duration: 0.14, ease: 'power2.out' }, s);
    TL.to(el, { opacity: 0, duration: 0.12, ease: 'power2.in' }, s + Math.max(0.26, d - 0.12));
  });

  meta.forEach((m) => {
    const sc = document.getElementById('sc' + m.i);
    if (!sc) return;
    const st = m.start, at = st + 0.02, stage = sc.querySelector('.stage');

    const bloom = sc.querySelector('.bg i:last-child');
    if (bloom) TL.fromTo(bloom, { scale: 1, opacity: .85 },
      { scale: 1.05, opacity: 1, duration: Math.max(1, m.dur), ease: 'sine.inOut' }, st);

    if (stage) {
      TL.fromTo(stage, { opacity: 0, y: 20 },
        { opacity: 1, y: 0, duration: 0.36, ease: 'power3.out' }, at);
      TL.to(stage, { opacity: 0, duration: 0.22, ease: 'power2.in' },
        st + Math.max(0.42, m.dur - 0.22));
    }

    const photo = sc.querySelector('.photo');
    if (photo) TL.fromTo(photo, { scale: 1.04 }, { scale: 1.11, duration: m.dur, ease: 'none' }, st);

    /* an element with data-at arrives on the word that says it */
    const when = (el, fallback) => {
      const v = el.dataset.at;
      return v === undefined ? fallback : Math.max(st, Number(v));
    };
    q('.rows .row', sc).forEach((r, k) => TL.fromTo(r, { opacity: 0, x: -18 },
      { opacity: 1, x: 0, duration: 0.3, ease: 'power2.out' }, when(r, at + 0.2 + k * 0.26)));
    q('.bub', sc).forEach((b, k) => TL.fromTo(b, { opacity: 0, y: 14, scale: .97 },
      { opacity: 1, y: 0, scale: 1, duration: 0.3, ease: 'back.out(1.5)' },
      when(b, at + 0.18 + k * 0.34)));
    /* a continuous shot whose centre line changes: each takes over from the last */
    const seq = q('.seqline', sc);
    seq.forEach((el, k) => {
      const t0 = when(el, at + 0.3 + k * 1.1);
      TL.fromTo(el, { opacity: 0, y: 16 },
        { opacity: 1, y: 0, duration: 0.34, ease: 'power2.out' }, t0);
      const nxt = seq[k + 1];
      if (nxt) TL.to(el, { opacity: 0, y: -14, duration: 0.26, ease: 'power2.in' },
                     when(nxt, at + 0.3 + (k + 1) * 1.1) - 0.1);
    });
    q('.chip', sc).forEach((c, k) => TL.fromTo(c, { opacity: 0, y: 14 },
      { opacity: 1, y: 0, duration: 0.28, ease: 'power2.out' }, when(c, at + 0.2 + k * 0.18)));

    /* bars, meters and gauges: width driven from data-w, block-level and sized */
    q('.fill,.meterf,.gfill', sc).forEach((f, k) => TL.fromTo(f, { width: '0%' },
      { width: Number(f.dataset.w || 0) + '%', duration: 0.66, ease: 'power3.out' }, at + 0.34 + k * 0.16));
    q('.gknob', sc).forEach((f) => {
      const w = Number(f.dataset.w || 0);
      const track = f.parentElement.getBoundingClientRect().width || 1160;
      TL.fromTo(f, { x: 0, xPercent: -50, yPercent: -50 },
        { x: track * w / 100, duration: 0.66, ease: 'power3.out' }, at + 0.34);
    });
    q('.dot.on', sc).forEach((d, k) => TL.fromTo(d, { scale: 0 },
      { scale: 1, duration: 0.18, ease: 'back.out(2)' }, at + 0.56 + k * 0.06));

    q('.strikeline', sc).forEach((l) => TL.fromTo(l, { scaleX: 0 },
      { scaleX: 1, duration: 0.3, ease: 'power2.inOut' }, at + 0.44));
    q('.xmark,.bubx,.xmark-s', sc).forEach((x, k) => TL.fromTo(x,
      { opacity: 0, scale: .5, rotate: -16 },
      { opacity: 1, scale: 1, rotate: 0, duration: 0.26, ease: 'back.out(2)' }, at + 0.66 + k * 0.14));

    q('.i3d', sc).forEach((g) => TL.fromTo(g, { opacity: 0, scale: .88, y: 12 },
      { opacity: 1, scale: 1, y: 0, duration: 0.5, ease: 'back.out(1.4)' }, at + 0.06));
    q('.pcard', sc).forEach((p) => TL.fromTo(p, { opacity: 0, scale: .95, rotate: -1 },
      { opacity: 1, scale: 1, rotate: 0, duration: 0.48, ease: 'power3.out' }, at + 0.1));
    q('.gsmall,.gbig', sc).forEach((g, k) => TL.fromTo(g, { scale: 0 },
      { scale: 1, duration: 0.4, ease: 'back.out(1.4)' }, at + 0.3 + k * 0.24));
    q('.beam', sc).forEach((b) => TL.fromTo(b, { rotate: 0 },
      { rotate: -7, duration: 0.62, ease: 'power2.out' }, at + 0.34));
    q('.ar', sc).forEach((a, k) => TL.fromTo(a,
      { scaleX: 0, transformOrigin: k ? '100% 50%' : '0% 50%' },
      { scaleX: 1, duration: 0.36, ease: 'power2.out' }, at + 0.34 + k * 0.12));
    q('.chapnum', sc).forEach((c) => TL.fromTo(c, { opacity: 0, y: -14 },
      { opacity: 1, y: 0, duration: 0.44, ease: 'power3.out' }, at + 0.04));
    q('.vc', sc).forEach((c, k) => TL.fromTo(c, { opacity: 0, scale: .9 },
      { opacity: 1, scale: 1, duration: 0.42, ease: 'power2.out' }, at + 0.2 + k * 0.16));
  });

  window.__timelines = window.__timelines || {};
  window.__timelines['main'] = TL;
  TL.seek(0);
})();
