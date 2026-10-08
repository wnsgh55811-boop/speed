import json,os,re
S='/tmp/claude-0/-home-user-speed/0d948206-c1a3-547f-9fa6-f85521be224c/scratchpad'
CR=json.load(open(f'{S}/eng/crops.json'))
ICONDIR=f'{S}/eng/node_modules/lucide-static/icons'
USED_ICONS=set()
def icon_svg(name,sw=1.75):
    USED_ICONS.add(name)
    return f'<span data-ic="{name}"></span>'
def icons_js():
    d={}
    for n in USED_ICONS:
        s=open(f'{ICONDIR}/{n}.svg').read()
        s=re.sub(r'<!--.*?-->','',s,flags=re.S).strip()
        s=re.sub(r'width="24"','width="100%"',s); s=re.sub(r'height="24"','height="100%"',s)
        s=s.replace('stroke-width="2"','stroke-width="1.75"')
        d[n]=s
    return 'window.ICONS='+json.dumps(d)+';'
def IC(name): 
    USED_ICONS.add(name); return f'<i class="ic" data-ic="{name}"></i>'
# ---- item helpers
def img(src,x=0,y=0,w=1920,h=1080,at=0,anim='fade',**k):
    d=dict(k='img',src=src,x=x,y=y,w=w,h=h,at=at,anim=anim); d.update(k); return d
def html(h,x,y,w=None,hh=None,at=0,anim='fade',**k):
    d=dict(k='html',html=h,x=x,y=y,w=w,h=hh,at=at,anim=anim); d.update(k); return d
def icon(name,x,y,size,color='#c9a24a',at=0,anim='pop',**k):
    USED_ICONS.add(name)
    d=dict(k='icon',name=name,x=x,y=y,w=size,h=size,at=at,anim=anim,css=f'color:{color}'); d.update(k); return d
def crop(n,key,at,anim='up',**k):
    x,y,w,h=CR[str(n)][key]
    d=dict(k='img',src=f'assets/c{n:02d}_{key}.png',x=x,y=y,w=w,h=h,at=at,anim=anim); d.update(k); return d
def rect(n,key):
    x,y,w,h=CR[str(n)][key]; return x,y,w,h
def focus(cx,cy,z):
    x=960-cx*z; y=480-cy*z
    x=min(0,max(1920-1920*z,x)); y=min(0,max(1080-1080*z,y))
    return dict(s=z,x=x,y=y)
