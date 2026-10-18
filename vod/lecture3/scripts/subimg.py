# Subtitle overlay: Noto Sans KR Medium 54px, white, black 60% box, h=78 (y 971..1048), pad 12px L/R, centered.
from PIL import Image, ImageDraw, ImageFont
FONT=None
def font(path):
    global FONT
    if FONT is None: FONT=ImageFont.truetype(path,54)
    return FONT
TOP, BOT = 971, 1048          # inclusive rows -> 78px
def render(text, fontpath, W=1920):
    f=font(fontpath)
    l,t,r,b=f.getbbox(text)
    tw=int(round(f.getlength(text)))
    bw=tw+24; bh=BOT-TOP+1
    im=Image.new('RGBA',(bw,bh),(0,0,0,153))
    d=ImageDraw.Draw(im)
    # vertical centering on font em-box (ascent/descent) so baseline is constant for every line
    # centre the Hangul glyph box ('가' top..bottom) inside the 78px band; fixed baseline for all lines
    gl,gt,gr,gb=f.getbbox('가')
    y=round(bh/2-(gt+gb)/2)
    d.text((12,y),text,font=f,fill=(255,255,255,255))
    x=(W-bw)//2
    return im,x,TOP
