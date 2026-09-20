# -*- coding: utf-8 -*-
# Inline SVG pictograms. Stroke-based => inherently cut out, no background plate.
_S = 'fill="none" stroke="currentColor" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"'
ICONS = {
"stopwatch": f'<circle cx="32" cy="36" r="22" {_S}/><path d="M32 24v12l8 5M24 8h16M32 8v6" {_S}/>',
"play":      f'<circle cx="32" cy="32" r="24" {_S}/><path d="M27 22l16 10-16 10z" {_S}/>',
"brain":     f'<path d="M30 12a10 10 0 00-10 10 8 8 0 00-4 14 10 10 0 0010 12h8V12z" {_S}/><path d="M34 12a10 10 0 0110 10 8 8 0 014 14 10 10 0 01-10 12h-8V12z" {_S}/><path d="M24 24h4M24 34h4M40 24h-4M40 34h-4" {_S}/>',
"spark":     f'<path d="M32 8l5 15 15 5-15 5-5 15-5-15-15-5 15-5z" {_S}/>',
"eye":       f'<path d="M6 32s10-15 26-15 26 15 26 15-10 15-26 15S6 32 6 32z" {_S}/><circle cx="32" cy="32" r="7" {_S}/>',
"radar":     f'<circle cx="32" cy="32" r="24" {_S}/><circle cx="32" cy="32" r="14" {_S}/><circle cx="32" cy="32" r="4" {_S}/><path d="M32 32l17-11" {_S}/>',
"loop":      f'<path d="M14 26a18 18 0 0131-8M50 38a18 18 0 01-31 8" {_S}/><path d="M44 12v8h-8M20 52v-8h8" {_S}/>',
"check":     f'<circle cx="32" cy="32" r="24" {_S}/><path d="M21 33l8 8 15-16" {_S}/>',
"heart":     f'<path d="M32 51S12 39 12 26a10 10 0 0120-4 10 10 0 0120 4c0 13-20 25-20 25z" {_S}/>',
"hands":     f'<path d="M10 34l10-10 12 8 12-8 10 10-14 16H24z" {_S}/>',
"fork":      f'<path d="M32 8v20M32 28L16 44v12M32 28l16 16v12" {_S}/>',
"mirror":    f'<ellipse cx="32" cy="26" rx="16" ry="20" {_S}/><path d="M32 46v10M22 56h20" {_S}/>',
"shirt":     f'<path d="M24 10l8 6 8-6 14 8-6 10-4-2v26H20V26l-4 2-6-10z" {_S}/>',
"hair":      f'<path d="M16 34a16 16 0 0132 0v14H16z" {_S}/><path d="M16 34c0-12 6-20 16-20s16 8 16 20" {_S}/>',
"ruler":     f'<path d="M12 44h40M12 20h40M16 20v24M48 20v24" {_S}/><path d="M22 26v12M32 26v12M42 26v12" {_S}/>',
"wave":      f'<path d="M8 32h6l4-12 6 26 6-34 6 42 6-30 4 8h10" {_S}/>',
"feather":   f'<path d="M48 14C34 14 18 28 18 44l-6 6M18 44l24-24M22 40h14" {_S}/>',
"switch":    f'<rect x="10" y="22" width="44" height="20" rx="10" {_S}/><circle cx="42" cy="32" r="7" {_S}/>',
"split":     f'<path d="M32 10v14M32 24L16 40v14M32 24l16 16v14" {_S}/>',
"handshake": f'<path d="M8 30l10-8 8 6 8-6 8 6 10-6 4 8-14 18-8-6-8 6-8-6z" {_S}/>',
"doc":       f'<path d="M18 8h20l10 10v38H18z" {_S}/><path d="M38 8v10h10M26 30h14M26 40h14" {_S}/>',
"tie":       f'<path d="M26 8h12l-4 10 6 22-8 14-8-14 6-22z" {_S}/>',
"seat":      f'<path d="M16 42V22a6 6 0 016-6h20a6 6 0 016 6v20M12 42h40v8H12zM20 50v6M44 50v6" {_S}/>',
"megaphone": f'<path d="M12 26v12l28 12V14zM40 22a10 10 0 010 20M12 38l4 14h8l-3-14" {_S}/>',
"question":  f'<circle cx="32" cy="32" r="24" {_S}/><path d="M25 25a7 7 0 0113 3c0 5-6 5-6 10" {_S}/><circle cx="32" cy="46" r="2.6" fill="currentColor"/>',
"pause":     f'<circle cx="32" cy="32" r="24" {_S}/><path d="M26 23v18M38 23v18" {_S}/>',
"three":     f'<circle cx="32" cy="32" r="24" {_S}/><path d="M25 23h13l-7 9a7 7 0 11-6 9" {_S}/>',
"fear":      f'<circle cx="32" cy="32" r="24" {_S}/><path d="M23 27h5M36 27h5M24 44c4-5 12-5 16 0" {_S}/>',
"repair":    f'<path d="M42 14a10 10 0 00-13 13L14 42l8 8 15-15a10 10 0 0013-13l-7 7-6-6z" {_S}/>',
"mask":      f'<path d="M10 24c8-4 36-4 44 0 0 16-8 26-22 26S10 40 10 24z" {_S}/><path d="M22 32h6M36 32h6" {_S}/>',
"info":      f'<circle cx="32" cy="32" r="24" {_S}/><path d="M32 30v14" {_S}/><circle cx="32" cy="22" r="2.6" fill="currentColor"/>',
"info2":     f'<rect x="12" y="14" width="40" height="36" rx="6" {_S}/><path d="M22 26h20M22 36h12" {_S}/>',
"match":     f'<path d="M20 32a12 12 0 1112 12M44 32a12 12 0 11-12-12" {_S}/>',
"signal":    f'<path d="M14 44V32M24 44V24M34 44V16M44 44V26M54 44V20" {_S}/>',
"mute":      f'<path d="M12 26v12h8l10 8V18l-10 8z" {_S}/><path d="M40 26l12 12M52 26L40 38" {_S}/>',
}
def icon(name, size=112, color="#e9ecf1", sw=None):
    body = ICONS.get(name, ICONS["check"])
    if sw: body = body.replace('stroke-width="5"', f'stroke-width="{sw}"')
    return (f'<svg class="ic" viewBox="0 0 64 64" width="{size}" height="{size}" '
            f'style="color:{color};display:block;overflow:visible">{body}</svg>')

# X mark used for strike-throughs (kept modest, never spanning the frame)
def xmark(size=72, color="#ef5f8c", sw=9):
    return (f'<svg viewBox="0 0 64 64" width="{size}" height="{size}" style="display:block;color:{color}">'
            f'<path d="M16 16l32 32M48 16L16 48" fill="none" stroke="currentColor" '
            f'stroke-width="{sw}" stroke-linecap="round"/></svg>')

# Torn-paper edge, exactly the requested chain:
# dilate -> wide blur -> 2-octave noise -> hard threshold => irregular, non-sticker edge.
TORN_FILTER = """
<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>
  <filter id="torn" x="-22%" y="-22%" width="144%" height="144%" color-interpolation-filters="sRGB">
    <feMorphology in="SourceAlpha" operator="dilate" radius="13" result="fat"/>
    <feGaussianBlur in="fat" stdDeviation="11" result="soft"/>
    <feTurbulence type="fractalNoise" baseFrequency="0.018" numOctaves="2" seed="7" result="noise"/>
    <feDisplacementMap in="soft" in2="noise" scale="64" xChannelSelector="R" yChannelSelector="G" result="wob"/>
    <feComponentTransfer in="wob" result="paper">
      <feFuncA type="discrete" tableValues="0 0 0 0 0 0 1 1 1 1"/>
    </feComponentTransfer>
    <feFlood flood-color="#f4f2ec" result="white"/>
    <feComposite in="white" in2="paper" operator="in" result="sheet"/>
    <feMerge><feMergeNode in="sheet"/><feMergeNode in="SourceGraphic"/></feMerge>
  </filter>
</defs></svg>
"""
