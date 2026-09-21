# -*- coding: utf-8 -*-
"""Build preview/comp.html from index.html.

The published artifact can't reach the local font files or the asset CDN, so
the preview swaps Pretendard for Noto Sans KR (served by Google Fonts, which
the artifact CSP allows) and appends the __hfPaint bridge the player chrome
in preview/index.html drives.
"""
import io
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")

src = io.open(os.path.join(ROOT, "index.html"), encoding="utf-8").read()
gsap = io.open(os.path.join(ROOT, "vendor", "gsap.min.js"), encoding="utf-8").read()

# 1. inline GSAP (the artifact has no local vendor directory)
src = re.sub(r'<script src="[^"]*gsap\.min\.js"></script>',
             lambda m: "<script>" + gsap + "</script>", src, count=1)

# 2. a web font the artifact can actually fetch
src = src.replace(
    "<head>",
    '<head>\n<link rel="preconnect" href="https://fonts.googleapis.com">\n'
    '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
    '<link href="https://fonts.googleapis.com/css2?'
    'family=Noto+Sans+KR:wght@400;500;600;700;800&display=swap" rel="stylesheet">',
    1)
src = re.sub(r'@font-face\s*\{[^}]*Pretendard[^}]*\}', "", src)
src = src.replace('--font:"Pretendard", sans-serif;',
                  '--font:"Noto Sans KR","Pretendard",sans-serif;')
src = src.replace('font-family="Pretendard"', 'font-family="Noto Sans KR"')

BRIDGE = """
<script>
(function () {
  var root = document.getElementById('root');
  var tl = window.__timelines.main;
  var clips = Array.prototype.map.call(root.querySelectorAll('.clip'), function (el) {
    var s = parseFloat(el.getAttribute('data-start')) || 0;
    return { el: el, s: s, e: s + (parseFloat(el.getAttribute('data-duration')) || 0) };
  });
  document.documentElement.style.background = '#000';
  window.__hfDuration = parseFloat(root.getAttribute('data-duration'));
  window.__hfPaint = function (t) {
    tl.time(t);
    for (var i = 0; i < clips.length; i++) {
      var c = clips[i], hide = !(t >= c.s && t < c.e);
      if (c.el.hidden !== hide) c.el.hidden = hide;
    }
  };
  window.__hfPaint(0);
  if (window.parent && window.parent.__hfReady) window.parent.__hfReady();
})();
</script>
</body>
</html>"""
src = re.sub(r"</body>\s*</html>\s*$", lambda m: BRIDGE, src)

out = os.path.join(ROOT, "preview", "comp.html")
io.open(out, "w", encoding="utf-8").write(src)
print("wrote", out, len(src), "bytes")
