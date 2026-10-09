import json,re,sys
sys.path.insert(0,'/tmp/claude-0/-home-user-speed/0d948206-c1a3-547f-9fa6-f85521be224c/scratchpad/scripts')
from lib import *
FA=json.load(open(f'{S}/w/fa_raw.json'))
_T0=[0.0]
def _set(t): _T0[0]=t
def ST(prefix,after=None):
    if after is None: after=_T0[0]
    for st,en,t,ws in FA:
        if st>=after-0.05 and t.startswith(prefix): return st
    for st,en,t,ws in FA:
        if st>=after-0.05 and prefix in t:
            i=t.index(prefix); 
            for w,a,b in ws:
                pass
            # time of first word overlapping prefix
            pos=0
            for w,a,b in ws:
                j=t.find(w,pos)
                if j+len(w)>i: print('  [ST contains]',prefix,'->',t,a); return a
                pos=j+len(w)
            return st
    raise Exception('ST notfound '+prefix)
def WT(word,after=None):
    if after is None: after=_T0[0]
    for st,en,t,ws in FA:
        for w,a,b in ws:
            if a>=after-0.05 and word in w: return a
    raise Exception('WT notfound '+word)
END=round(FA[-1][1]+1.6,3)
SC=[];CH=[]
def scene(t0,t1,items,bg=None,xf=True):
    d=dict(t0=round(t0,3),t1=round(t1,3),items=items,xf=xf)
    if bg: d['bg']=bg
    SC.append(d)
def R(t,t0): return round(t-t0,3)
# ---------- backgrounds
NAVYBG='radial-gradient(120% 95% at 50% 35%,#223660 0%,#14213f 55%,#0a1226 100%)'
CREAMBG='radial-gradient(110% 80% at 50% 20%,#fbf7ef 0%,#f3ece0 60%,#ebe2d2 100%)'
def grain(): return html('',0,0,1920,1080,anim='none',cls='grain')
def orbs(dark=True):
    if dark: return [html('',-200,-260,900,900,anim='none',cls='orb',css='background:rgba(201,162,74,.22)',drift=[160,90]),
                     html('',1200,420,1000,1000,anim='none',cls='orb',css='background:rgba(76,116,210,.30)',drift=[-170,-70])]
    return [html('',-160,-300,900,900,anim='none',cls='orb',css='background:rgba(226,194,122,.35)',drift=[150,80]),
            html('',1250,500,900,900,anim='none',cls='orb',css='background:rgba(244,190,160,.35)',drift=[-140,-60])]
def navy(): return orbs(True)
def cream(): return orbs(False)
def dust(n=14,seed=1,col='#e2c27a',area=(80,120,1760,760)):
    import random; r=random.Random(seed); out=[]
    for k in range(n):
        s=r.choice([5,6,8,10]); x=area[0]+r.random()*area[2]; y=area[1]+r.random()*area[3]
        out.append(html('',x,y,s,s,anim='fade',at=r.random()*0.8,dur=1.2,cls='dot',css=f'background:{col};opacity:.6;box-shadow:0 0 12px {col}',drift=[r.uniform(-40,40),r.uniform(-70,-20)]))
    return out
# ---------- primitives
def ill(name): return img(f'il/{name}.jpg',0,0,1920,1080,anim='none')
def shade(kind):
    g={'l':'linear-gradient(90deg,rgba(10,18,38,.88) 0%,rgba(10,18,38,.6) 38%,rgba(10,18,38,0) 66%)',
       'r':'linear-gradient(270deg,rgba(10,18,38,.88) 0%,rgba(10,18,38,.6) 38%,rgba(10,18,38,0) 66%)',
       'b':'linear-gradient(180deg,rgba(10,18,38,0) 35%,rgba(10,18,38,.82) 100%)',
       't':'linear-gradient(0deg,rgba(10,18,38,0) 40%,rgba(10,18,38,.8) 100%)',
       'all':'rgba(10,18,38,.55)'}[kind]
    return html('',0,0,1920,1080,anim='none',css=f'background:{g}')
def H(h,x,y,w,size,at,align='left',dark=False,st=.03,**k):
    cls='h sp'+(' dk' if dark else '')
    return html(f'<div class="{cls}" style="font-size:{size}px;text-align:{align}">{h}</div>',x,y,w,None,at=at,anim='none',chars=dict(at=at,st=st),**k)
def P(h,x,y,w,size,at,align='left',color='#c9d2e6',weight=500,anim='up',**k):
    return html(f'<div style="font-size:{size}px;font-weight:{weight};color:{color};text-align:{align};line-height:1.4;letter-spacing:-.02em">{h}</div>',x,y,w,None,at=at,anim=anim,**k)
def KICK(t,x,y,at,w=1000,align='left',color=None):
    c=' c' if align=='center' else ''
    col=f'color:{color};' if color else ''
    return html(f'<div style="text-align:{align}"><span class="kick{c}" style="{col}">{t}</span></div>',x,y,w,None,at=at,anim='fade',dur=.8)
def PILL(t,ic,x,y,at,c='w',anim='pop',size=None,**k):
    i=IC(ic) if ic else ''
    fs=f'font-size:{size}px' if size else ''
    return html(f'<div class="pill {c}" style="{fs}">{i}<span>{t}</span></div>',x,y,None,None,at=at,anim=anim,**k)
def IBOX(name,x,y,size,at,bg='#14213f',color='#e2c27a',anim='pop',ring=True,**k):
    USED_ICONS.add(name)
    sh='box-shadow:0 0 0 12px rgba(201,162,74,.16),0 24px 50px rgba(0,0,0,.3);' if ring else 'box-shadow:0 20px 40px rgba(0,0,0,.25);'
    return html(f'<div class="ibox" style="width:{size}px;height:{size}px;background:{bg};color:{color};{sh}"><i class="ic" data-ic="{name}" style="width:50%;height:50%"></i></div>',x,y,size,size,at=at,anim=anim,**k)
def STK(t,cls=''): return f'<span class="st">{t}<b class="stl {cls}"></b></span>'
def SPR(name,x,y,w,at,anim='pop',float_=14,**k):
    return img(f'il/{name}.png',x,y,w,None,at=at,anim=anim,float=float_,**k)
def FRAME(name,x,y,w,h,at,anim='rise',**k):
    return html(f'<div class="frame" style="width:{w}px;height:{h}px"><img src="il/{name}.jpg"></div>',x,y,w,h,at=at,anim=anim,**k)
def STAMP(x,y,size,at,ok=False):
    n='check' if ok else 'x'; USED_ICONS.add(n)
    bg='#c9a24a' if ok else '#e0524a'; c='#14213f' if ok else '#fff'
    return html(f'<div class="ibox" style="width:{size}px;height:{size}px;background:{bg};color:{c};box-shadow:0 12px 30px rgba(0,0,0,.25)"><i class="ic" data-ic="{n}" style="width:58%;height:58%"></i></div>',x,y,size,size,at=at,anim='pop')
# ---------- slide scenes with spotlight
GLOW='drop-shadow(0px 0px 26px rgba(201,162,74,0.9)) drop-shadow(0px 18px 26px rgba(20,33,63,0.22))'
NOGLOW='drop-shadow(0px 0px 0px rgba(201,162,74,0)) drop-shadow(0px 0px 0px rgba(20,33,63,0))'
def slide(n,t0,t1,rev,spot=(),extra=(),xf=True,dim=True,nodim=()):
    """rev: list of (key, abs_time or None(=already visible), anim). spot: list of (abs_time, key|list|None)"""
    items=[img(f'assets/p{n:02d}.jpg',anim='none')]
    rt={}
    for key,t,an in rev:
        if t is None: it=crop(n,key,0,anim='none'); rt[key]=t0-1
        else: it=crop(n,key,R(t,t0),anim=an,dur=.7); rt[key]=t
        it['origin']='50% 50%'; it['tw']=[]
        items.append(it)
    keys=[r[0] for r in rev]
    sp=sorted(spot,key=lambda s:s[0])
    for it,key in zip(items[1:],keys):
        state='n'
        for T,act in sp:
            acts=[] if act is None else (act if isinstance(act,list) else [act])
            if 'title' in acts: acts=acts
            new='a' if key in acts else ('d' if acts and dim and key!='t' and key not in nodim else 'n')
            if key=='t': new='n'
            if new==state: continue
            at=max(T,rt[key]+0.75)
            if at>=t1: continue
            p={'a':dict(y=-10,scale=1.04,opacity=1),'d':dict(y=0,scale=1,opacity=.4),'n':dict(y=0,scale=1,opacity=1)}[new]
            it['tw'].append(dict(at=R(at,t0),p=p,dur=.5))
            state=new
    items+=list(extra)
    scene(t0,t1,items,xf=xf)
def chap(t,num,label): CH.append([round(t-0.1,3),f'{num:02d}',label])
# ---------- phone & zoom mocks
def zoomwin(x,y,at,w=1520,switch=(),name2='수강생',extra=''):
    h=round(w*630/1920)
    USED_ICONS.update(['mic','video','monitor-up','circle-dot','phone-off'])
    imgs=''.join(f'<img class="z z{k}" src="il/zoom{k}.jpg" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;{"" if k==1 else "opacity:0"}">' for k in (1,2,3))
    hh=f'''<div style="width:{w}px;border-radius:26px;overflow:hidden;background:#1b1f27;box-shadow:0 40px 100px rgba(0,0,0,.45);border:1px solid rgba(255,255,255,.08)">
<div style="height:58px;display:flex;align-items:center;padding:0 22px;gap:10px;color:#cfd5e2;font-size:22px;font-weight:600">
<span style="width:14px;height:14px;border-radius:50%;background:#ff5f57"></span><span style="width:14px;height:14px;border-radius:50%;background:#febc2e"></span><span style="width:14px;height:14px;border-radius:50%;background:#28c840"></span>
<span style="margin-left:18px">1:1 화상 코칭 세션</span>
<span style="margin-left:auto;display:flex;align-items:center;gap:10px;background:rgba(224,82,74,.15);color:#ff7b72;padding:6px 14px;border-radius:999px"><span class="recdot" style="width:12px;height:12px;border-radius:50%;background:#ff5f57"></span>REC</span></div>
<div style="position:relative;height:{h}px">{imgs}
<span style="position:absolute;left:18px;bottom:16px;background:rgba(0,0,0,.55);color:#fff;font-size:22px;font-weight:600;padding:6px 14px;border-radius:10px">메릭 코치</span>
<span style="position:absolute;left:{w//2+18}px;bottom:16px;background:rgba(0,0,0,.55);color:#fff;font-size:22px;font-weight:600;padding:6px 14px;border-radius:10px">{name2}</span>{extra}</div>
<div style="height:70px;display:flex;align-items:center;justify-content:center;gap:28px;color:#cfd5e2">
{''.join(f'<span style="width:48px;height:48px;border-radius:50%;background:#2a2f3a;display:flex;align-items:center;justify-content:center"><i class="ic" data-ic="{n}" style="width:24px;height:24px"></i></span>' for n in ('mic','video','monitor-up','circle-dot'))}
<span style="width:84px;height:48px;border-radius:24px;background:#e0524a;display:flex;align-items:center;justify-content:center;color:#fff"><i class="ic" data-ic="phone-off" style="width:24px;height:24px"></i></span></div></div>'''
    sub=[dict(sel=f'.z{k}',anim='fade',at=a,dur=.35) for k,a in switch]
    return html(hh,x,y,w,None,at=at,anim='rise',sub=sub), h
def search_box(x,y,w,txt,at,typedur=1.0,minh=0,strike_at=None):
    USED_ICONS.update(['search','history'])
    h=f'''<div style="width:{w}px;background:#fff;border-radius:30px;box-shadow:0 40px 90px rgba(0,0,0,.4);padding:34px 40px 26px;box-sizing:border-box;min-height:{minh}px">
 <div style="display:flex;align-items:center;gap:22px;font-size:46px;color:#14213f;font-weight:600;border-bottom:2px solid #eef0f4;padding-bottom:24px">
  <i class="ic" data-ic="search" style="width:50px;height:50px;color:#14213f"></i><span class="st"><span class="typed"></span><b class="stl gold"></b></span><span style="display:inline-block;width:3px;height:48px;background:#c9a24a;margin-left:-12px"></span>
  <span style="margin-left:auto;width:74px;height:74px;border-radius:50%;background:#c9a24a;display:flex;align-items:center;justify-content:center;color:#14213f"><i class="ic" data-ic="search" style="width:36px;height:36px"></i></span></div></div>'''
    sub=[dict(sel='.stl',anim='wipe',at=strike_at-0+0,dur=.5)] if strike_at is not None else []
    return html(h,x,y,w,None,at=at,anim='rise',type=txt,typedur=typedur,typedelay=0.3,sub=sub)
def srows(x,y,w,rows,ats,hl=0):
    out=[]
    for k,(r,a) in enumerate(zip(rows,ats)):
        bg='background:#f6ead0;' if k==hl else ''
        out.append(html(f'<div style="{bg}border-radius:16px;display:flex;align-items:center;gap:20px;font-size:36px;color:{"#14213f" if k==hl else "#6b7184"};padding:16px 22px;font-weight:{700 if k==hl else 500}"><i class="ic" data-ic="history" style="width:34px;height:34px;color:#a2a8b6"></i>{r}</div>',x,y+k*84,w,None,at=a,anim='left',dur=.5))
    return out
# ====================================================== S1 OPENING
B=[ST('소개팅 대화'),ST('이 얘기를'),ST('그리고 요즘도'),ST('이다사 부트캠프는'),ST('많은 분들을'),ST('요즘'),ST('이 부트캠프를 한'),ST('12주 동안 익히는'),
   ST('전체 흐름'),ST('부트캠프 과정의'),ST('그리고 한 단계는'),ST('또한 1:1'),ST("그리고 '좀"),ST('정리하면'),ST('한번 생각해보세요'),ST('부트캠프는 크게'),
   ST('가격은'),ST('아뇨'),ST('쉽게 말하면'),ST('대신 솔직하게'),ST('아마 지금쯤'),ST('1:1 태도 진단을'),ST('더 이상')]
B=[0.0]+[round(b-0.12,3) for b in B[1:]]
NAMES=['오프닝','신뢰','수강생 후기','프로그램 소개','멘트가 아니라 태도','외운 멘트의 한계','하이에나에서 사자로','사자의 태도 12가지','진단 + 6단계','90분 진단',
       '2주 사이클','1:1 코칭 6회','0·6·12주 비교','12주 뒤 마스터','무조건 1:1','두 구간','가격','1년 상담과 비교','태도 트레이너','신청하지 마세요','걱정하지 마세요','90분 진단부터','마무리']
pass
def cut(prefix,after=0): return round(ST(prefix,after)-0.1,3)
T=[]
# 1a search
t0,t1=0.0,cut('아마 없으실'); _set(t0)
rows=['여자 번호 따는 법','소개팅 대화 주제 추천','애프터 신청 멘트','카톡 답장 잘하는 법']
scene(t0,t1,[ill('a01'),shade('all'),search_box(470,150,980,'소개팅 대화 주제',0.0,typedur=0.9,minh=590),
   html('<div style="font-size:26px;color:#9aa0b0;font-weight:600;letter-spacing:.1em">최근 검색어</div>',532,328,400,None,at=0.7),
   *srows(510,374,900,rows,[R(WT('여자'),t0)-0.2,1.5,1.75,2.0]),
   grain()],xf=False)
# 1b
t0,t1=t1,cut('대화는 잘'); _set(t0)
scene(t0,t1,[*cream(),SPR('s24',230,200,560,0.1,anim='drop',dur=.9),
   KICK('THE PROBLEM',920,300,0.1),H(f'처음부터<br><span class="g">멘트</span>가 문제가<br>아니었습니다',920,350,900,96,R(WT('처음부터'),t0),dark=True),grain()],bg=CREAMBG)
# 1c kakao
t0,t1=t1,cut('그러면 또'); _set(t0)
USED_ICONS.update(['chevron-left'])
phone=f'''<div style="width:560px;height:800px;border-radius:60px;background:#b9cfe2;border:14px solid #0f1628;box-shadow:0 40px 90px rgba(0,0,0,.5);overflow:hidden">
<div style="height:100px;background:#adc4d9;display:flex;align-items:center;padding:0 30px;font-size:30px;font-weight:700;color:#14213f;gap:14px"><i class="ic" data-ic="chevron-left" style="width:34px;height:34px"></i>지난주 소개팅 그분</div></div>'''
def bub(t,me,y,at,meta=''):
    st='background:#fee500;border-top-right-radius:8px' if me else 'background:#fff;border-top-left-radius:8px'
    j='flex-end' if me else 'flex-start'
    m=f'<span style="font-size:22px;color:#33475e;white-space:nowrap">{meta}</span>'
    inner=(m+f'<div style="{st};color:#191919;font-size:30px;font-weight:600;padding:16px 24px;border-radius:26px;white-space:nowrap">{t}</div>') if me else (f'<div style="{st};color:#191919;font-size:30px;font-weight:600;padding:16px 24px;border-radius:26px;white-space:nowrap">{t}</div>'+m)
    return html(f'<div style="display:flex;justify-content:{j};align-items:flex-end;gap:10px">{inner}</div>',190,y,500,None,at=at,anim='up',dur=.45)
scene(t0,t1,[ill('a02'),shade('l'),html(phone,160,130,560,800,at=0.05,anim='left',dur=.6),
   bub('오늘 정말 즐거웠어요 :)',True,270,0.35,'<b style="color:#d4a000">1</b> 오후 10:12'),
   bub('네 저두요 ㅎㅎ',False,370,R(WT('두'),t0),'다음 날 오후'),
   bub('이번 주말에 시간 괜찮으세요?',True,470,R(WT('두'),t0)+0.7,'<b style="color:#d4a000">1</b>'),
   html('<div style="font-size:24px;font-weight:600;color:#33475e;background:rgba(255,255,255,.6);border-radius:20px;padding:8px 22px">3일째 읽지 않음</div>',330,580,300,None,at=R(WT('카톡'),t0),anim='pop'),
   grain()])
# 1d search again + strike
t0,t1=t1,cut('오늘은 왜'); _set(t0)
scene(t0,t1,[*navy(),html('<div style="font-size:28px;color:#9aa7c4;font-weight:600;letter-spacing:.08em">그리고 또 검색…</div>',470,240,800,None,at=0.05),
   search_box(470,300,980,'애프터 신청 멘트',0.0,typedur=0.7,strike_at=R(WT('끝까지'),t0)),
   H('이 영상 끝까지 보시면<br><span class="g">그 검색은 이제 그만</span>',0,560,1920,84,R(WT('끝까지'),t0),align='center'),grain()],bg=NAVYBG)
# 1e title
t0,t1=t1,B[1]; _set(t0)
scene(t0,t1,[*navy(),*dust(16,2),
   H('왜 매번 <span class="g">흐지부지</span> 끝날까?',0,250,1920,80,0.05,align='center',out=dict(at=R(ST('그리고 이다사'),t0)-0.3,anim='up')),
   KICK('IDASA BOOTCAMP',0,330,R(ST('그리고 이다사'),t0),align='center',w=1920),
   H('이다사 <span class="g">12주</span> 부트캠프',0,390,1920,132,R(ST('그리고 이다사'),t0)+0.1,align='center',st=.05),
   html('<div style="width:100%;height:4px;background:linear-gradient(90deg,transparent,#c9a24a,transparent)"></div>',560,580,800,4,at=R(ST('그리고 이다사'),t0)+0.7,anim='grow'),
   grain()],bg=NAVYBG)
# ====================================================== S2
t0,t1=B[1],cut('그냥 이야기만'); _set(t0)
slide(2,t0,t1,[('t',t0+0.1,'up'),('photo',WT('안녕하세요')-0.2,'pop'),('name',WT('메릭입니다'),'up'),('num',WT('500명이'),'pop'),('pill',WT('1:1로',WT('500명이')),'up')],
      spot=[(WT('500명이')+0.2,'num'),(WT('1:1로',WT('500명이'))+0.3,['num','pill'])])
t0,t1=t1,cut('그러다 보니'); _set(t0)
zw,zh=zoomwin(200,190,0.1,switch=[(2,R(ST('실제로 대화를'),t0)),(3,R(ST('한 장면씩'),t0))])
scene(t0,t1,[*navy(),H('듣고 끝나는 상담이 <span class="g">아닙니다</span>',0,80,1920,64,0.05,align='center'),zw,
   grain()],bg=NAVYBG)
t0,t1=t1,B[2]; _set(t0)
chart='''<svg width="1200" height="380" viewBox="0 0 1200 380"><defs><linearGradient id="g1" x1="0" x2="1"><stop offset="0" stop-color="#8ea2cc"/><stop offset="1" stop-color="#e2c27a"/></linearGradient></defs>
<line x1="0" y1="320" x2="1200" y2="320" stroke="rgba(255,255,255,.18)" stroke-width="2" stroke-dasharray="6 10"/>
<polyline fill="none" stroke="url(#g1)" stroke-width="8" stroke-linecap="round" stroke-linejoin="round" points="0,170 130,150 240,178 360,140 470,162 560,136 650,152 720,300 790,312 880,212 990,190 1100,175 1200,160"/></svg>'''
scene(t0,t1,[*navy(),KICK('500명을 직접 보며',0,140,0.05,align='center',w=1920),
   H('남자가 <span class="g">무너지는 순간</span>이 보입니다',0,200,1920,76,0.1,align='center'),
   html(chart,360,420,1200,380,at=0.3,anim='wipe',dur=1.6),
   html('<div style="width:48px;height:48px;border-radius:50%;background:#e0524a;box-shadow:0 0 0 14px rgba(224,82,74,.22),0 0 30px #e0524a"></div>',360+760-24,420+310-24,48,48,at=1.6,anim='pop'),
   PILL('무너지는 순간','circle-alert',990,800,1.8,c='n'),grain()],bg=NAVYBG)
# ====================================================== S3
t0,t1=B[2],cut('또 한 분은'); _set(t0)
slide(3,t0,t1,[('r1',t0+0.1,'pop'),('r2',t0+0.3,'pop'),('r3',t0+0.5,'pop'),('r4',t0+0.7,'pop')],
      spot=[(ST('한 분은'),'r1'),(ST('카톡만'),'r2')])
t0,t1=t1,cut('그분이 그러시더라고요'); _set(t0)
scene(t0,t1,[ill('a04'),grain()])
t0,t1=t1,cut('그리고 이분은'); _set(t0)
USED_ICONS.add('quote')
scene(t0,t1,[*cream(),html('<div style="color:#c9a24a;width:120px;height:120px"><i class="ic" data-ic="quote" style="width:120px;height:120px"></i></div>',900,150,120,120,at=0.05,anim='pop'),
   H('“제가 말을 못 하는 사람인 줄 알았는데,',0,330,1920,64,R(ST('제가 말을'),t0),align='center',dark=True,st=.02),
   H('<span class="g">전달해본 연습</span>이 부족했던 거였어요.”',0,430,1920,64,R(ST('전달해본'),t0),align='center',dark=True,st=.02),
   P('— 2차 애프터에서 손을 잡은 수강생',0,580,1920,32,R(ST('전달해본'),t0)+0.6,align='center',color='#8a8270'),grain()],bg=CREAMBG)
t0,t1=t1,cut('이분들은 멘트를'); _set(t0)
scene(t0,t1,[ill('a05'),grain()])
t0,t1=t1,B[3]; _set(t0)
thumbs=[crop(3,k,0,anim='none') for k in ('r1','r2','r3','r4')]
th=[]
for j,k in enumerate(('r1','r2','r3','r4')):
    x,y,w,h=rect(3,k); s=300/w
    th.append(img(f'assets/c03_{k}.png',230+j*370,640,300,round(h*s),at=R(ST('정말 아무것도'),t0)+j*0.12,anim='up',css=f'border-radius:14px;transform:rotate({[-4,3,-2,4][j]}deg)'))
scene(t0,t1,[*navy(),H(STK('멘트를 외운 게')+' 아닙니다',0,170,1920,80,0.05,align='center',sub=[dict(sel='.stl',anim='wipe',at=R(WT('아닙니다'),t0)+0.2,dur=.5)]),
   H('<span class="g">태도</span>가 바뀐 겁니다',0,300,1920,124,R(ST('태도가 바뀐'),t0),align='center',st=.05),*th,grain()],bg=NAVYBG)
# ====================================================== S4
t0,t1=B[3],cut('먼저 진단'); _set(t0)
def stat(x,y,big,small,at,count=None,gold=False):
    cls='gcard' if gold else 'glass'
    col='#14213f' if gold else '#fff'
    num=f'<span class="num">{big}</span>' if count else big
    return html(f'<div class="{cls}" style="width:420px;height:230px;display:flex;flex-direction:column;align-items:center;justify-content:center;color:{col}"><div style="font-size:84px;font-weight:800;letter-spacing:-.03em">{num}</div><div style="font-size:30px;font-weight:600;opacity:.8;margin-top:4px">{small}</div></div>',x,y,420,230,at=at,anim='rise',count=count)
scene(t0,t1,[*navy(),KICK('THE PROGRAM',0,170,0.05,align='center',w=1920),H('이다사 부트캠프',0,220,1920,110,0.1,align='center',st=.05),
   stat(270,480,'500명+','만나 온 남성분들',R(WT('500명'),t0),count=None),stat(750,480,'1:1','쌓아 온 방법 그대로',R(ST('쌓은 방법'),t0)),
   stat(1230,480,'1:1 훈련','과정',R(WT('훈련'),t0),gold=True),grain()],bg=NAVYBG)
t0,t1=t1,cut('PDF 하나'); _set(t0)
slide(4,t0,t1,[('t',t0+0.05,'up'),('a',t0+0.15,'pop'),('ar1',ST('12주 동안')-0.3,'left'),('b',ST('12주 동안'),'pop'),('ar2',ST('그리고 부트캠프를')-0.3,'left'),('c',ST('그리고 부트캠프를'),'pop')],
      spot=[(t0+0.4,'a'),(ST('12주 동안'),'b'),(ST('그리고 부트캠프를'),'c')])
t0,t1=t1,B[4]; _set(t0)
def pcard(i,x,label,sub,at,dark):
    cls='ncard' if dark else 'wcard'
    flt='' if dark else 'filter:grayscale(.65) brightness(.95);'
    return html(f'''<div class="{cls}" style="width:700px;height:600px;overflow:hidden">
<img src="il/{i}.jpg" style="width:700px;height:394px;object-fit:cover;display:block;{flt}">
<div style="padding:30px 38px"><div style="font-size:44px;font-weight:800;letter-spacing:-.03em">{label}</div><div style="font-size:30px;opacity:.65;margin-top:8px;font-weight:500">{sub}</div></div></div>''',x,190,700,600,at=at,anim='rise')
scene(t0,t1,[*cream(),pcard('a26',200,'PDF + 영상 강의','받고, 보고, 끝',0.1,False),STAMP(810,140,120,0.9),
   pcard('a13',1020,'직접 해보고 같이 고친다','이다사 부트캠프',R(ST('직접 해보고'),t0),True),STAMP(1630,140,120,R(ST('직접 해보고'),t0)+0.5,ok=True),grain()],bg=CREAMBG)
# ====================================================== S5
t0,t1=B[4],cut('멘트 100개를'); _set(t0)
scene(t0,t1,[*navy(),KICK('500명을 만나며 확실히 알게 된 한 가지',0,240,0.1,align='center',w=1920),
   H(STK('멘트를 더 외울 게 아니라'),0,330,1920,72,R(ST('연애가 어려울수록'),t0),align='center',sub=[dict(sel='.stl',anim='wipe',at=R(WT('아니라'),t0)+0.25,dur=.5)]),
   H('<span class="g">태도</span>를 바꿔야 합니다',0,460,1920,124,R(WT('태도를'),t0),align='center',st=.05),grain()],bg=NAVYBG)
t0,t1=t1,cut('그런데 태도는'); _set(t0)
fl=[('“주말에 뭐 하세요?”',1180,140),('멘트 #27',1500,260),('“취미가 뭐예요?”',1250,380),('멘트 #64',140,170),('“MBTI가 뭐예요?”',120,330),('멘트 #100',1480,520),('“오늘 날씨 좋네요”',160,520)]
items=[ill('a03'),html('',0,0,1920,1080,anim='none',css='background:rgba(10,18,38,.2)'),shade('b')]
for k,(tx,x,y) in enumerate(fl):
    items.append(html(f'<div class="pill w" style="font-size:28px;padding:12px 22px">{tx}</div>',x,y+60,None,None,at=0.3+k*0.22,anim='pop',float=10,
                      out=dict(at=R(WT('사라집니다'),t0)+k*0.07,anim='blur',dur=.5)))
items+=[H('긴장하는 순간 <span class="g">전부 사라집니다</span>',0,800,1920,70,R(WT('사라집니다'),t0),align='center'),grain()]
scene(t0,t1,items)
t0,t1=t1,B[5]; _set(t0)
slide(5,t0,t1,[('t',t0+0.05,'up'),('a',t0+0.15,'left'),('lt',t0+0.55,'pop'),('b',t0+0.75,'right')],
      spot=[(ST('한 번 몸에'),'b'),(ST('그래서 멘트'),['a','b']),(WT('익히는'),'b')])
# ====================================================== S6
t0,t1=B[5],cut('그런데 상대가'); _set(t0)
USED_ICONS.update(['play','heart'])
feed=['이 멘트만 쓰면 된다','카톡은 이렇게 보내라','여자가 반하는 말투 5가지','소개팅 필승 대화 주제','밀당 고수의 카톡법','애프터 100% 받는 멘트']
cards=''.join(f'<div style="display:flex;gap:18px;align-items:center;background:#fff;border-radius:22px;padding:16px;margin-bottom:16px;box-shadow:0 8px 20px rgba(0,0,0,.06)"><div style="width:150px;height:96px;border-radius:14px;background:linear-gradient(135deg,{c1},{c2});display:flex;align-items:center;justify-content:center;color:#fff"><i class="ic" data-ic="play" style="width:40px;height:40px"></i></div><div style="font-size:28px;font-weight:700;color:#14213f;line-height:1.3">{t}</div></div>' for t,(c1,c2) in zip(feed*2,[('#24385f','#c9a24a'),('#e0524a','#f0a07a'),('#5470c6','#8ea2cc'),('#c9a24a','#e2c27a'),('#14213f','#5470c6'),('#e07b5a','#c9a24a')]*2))
phone2=f'<div style="width:620px;height:860px;border-radius:64px;background:#eef1f6;border:14px solid #0f1628;box-shadow:0 40px 90px rgba(0,0,0,.5);overflow:hidden;position:relative"><div class="feed" style="position:absolute;left:24px;right:24px;top:30px">{cards}</div></div>'
scene(t0,t1,[*navy(),html(phone2,1120,110,620,860,at=0.05,anim='up',sub=[dict(sel='.feed',p=dict(y=-560),at=0.6,dur=R(ST('그런데 상대가'),t0)-0.6,ease='sine.inOut')]),
   KICK('요즘 넘쳐나는 것',160,300,0.1),H("<span class='g'>'이 멘트만 쓰면 된다'</span>",160,350,900,70,0.15,st=.025),
   H("'카톡은 이렇게 보내라'",160,450,900,70,R(WT('카톡은'),t0),st=.025),
   grain()],bg=NAVYBG)
t0,t1=t1,cut('상대가 바뀌어도'); _set(t0)
slide(6,t0,t1,[('t',t0+0.05,'up'),('a',t0+0.15,'up'),('b',ST('픽업이나')-0.1,'up'),('c',ST('유튜브 꿀팁')-0.1,'up')],
      spot=[(t0+0.6,'a'),(ST('픽업이나'),'b'),(ST('유튜브 꿀팁'),'c')])
t0,t1=t1,B[6]; _set(t0)
scene(t0,t1,[ill('a06'),shade('l'),KICK('끝까지 남는 건 딱 하나',140,330,0.1),
   H('긴장한 순간에도<br><span class="g">무너지지 않는 내 태도</span>',140,390,1000,88,R(ST('긴장한 순간에도'),t0)),grain()])
# ====================================================== S7
t0,t1=B[6],cut('하이에나는 상대'); _set(t0)
slide(7,t0,t1,[('t',t0+0.05,'up'),('a',WT('하이에나의')-0.1,'left'),('ar',WT('사자의')-0.3,'pop'),('b',WT('사자의'),'right')],spot=[(WT('사자의')+0.2,'b')])
t0,t1=t1,cut('사자는 자기'); _set(t0)
gauge='''<svg width="420" height="250" viewBox="0 0 420 250"><path d="M30 220 A180 180 0 0 1 390 220" fill="none" stroke="rgba(255,255,255,.14)" stroke-width="26" stroke-linecap="round"/>
<path d="M30 220 A180 180 0 0 1 210 40" fill="none" stroke="#7bc79a" stroke-width="26" stroke-linecap="round" opacity=".85"/><path d="M210 40 A180 180 0 0 1 390 220" fill="none" stroke="#e0524a" stroke-width="26" stroke-linecap="round" opacity=".85"/>
<text x="40" y="250" fill="#9aa7c4" font-size="24" font-family="P" font-weight="700">안심</text><text x="330" y="250" fill="#9aa7c4" font-size="24" font-family="P" font-weight="700">불안</text></svg>'''
needle='<div style="width:10px;height:160px;border-radius:5px;background:#fff;box-shadow:0 0 12px rgba(255,255,255,.6)"></div>'
scene(t0,t1,[img('img/i07.jpg',0,0,1920,1080,anim='none',css='object-fit:cover'),shade('r'),
   KICK('HYENA',1000,170,0.1),H('상대 반응을<br><span class="g">먹고 산다</span>',1000,220,800,92,0.15),
   html(gauge,1000,560,420,250,at=0.5,anim='fade'),
   html(needle,1000+205,560+60,10,160,at=0.5,anim='fade',origin='50% 100%',css='transform:rotate(0deg)',
        tw=[dict(at=0.6,p=dict(rotation=0),dur=.1),dict(at=R(WT('웃으면'),t0),p=dict(rotation=-62),dur=.6,ease='back.out(2)'),dict(at=R(WT('굳어도'),t0),p=dict(rotation=64),dur=.6,ease='back.out(2)')]),
   PILL('웃으면 → 안심','smile',1480,600,R(WT('웃으면'),t0),c='t',size=28),PILL('굳으면 → 불안','frown',1480,690,R(WT('굳어도'),t0),c='t',size=28),
   PILL('점수 따려고 애씀','circle-alert',1480,780,R(WT('점수를'),t0),c='g',size=28),grain()])
t0,t1=t1,cut('여자 앞에서'); _set(t0)
scene(t0,t1,[img('img/i08.jpg',0,0,1920,1080,anim='none',css='object-fit:cover'),shade('r'),
   KICK('LION',1160,200,0.1),H('<span class="g">자기 기준</span>으로<br>움직인다',1160,250,700,96,0.15),
   PILL('흔들리지 않는다','anchor',1160,560,R(WT('흔들리지'),t0),c='t'),PILL('원하는 걸 말한다','message-square-heart',1160,670,R(WT('원하는'),t0),c='t'),
   PILL('먼저 제안한다','arrow-right',1160,780,R(WT('먼저'),t0),c='g'),grain()])
t0,t1=t1,cut('그리고 솔직히'); _set(t0)
scene(t0,t1,[*cream(),H('여자 앞에서 <span class="g">작아지는 이유</span>',0,90,1920,64,0.05,align='center',dark=True),
   html(f'<div class="pill w" style="font-size:34px">{IC("circle-alert")}<span>{STK("자신감이 없어서?")}</span></div>',0,200,1920,None,at=0.5,anim='pop',css='display:flex;justify-content:center',sub=[dict(sel='.stl',anim='wipe',at=R(WT('아닙니다'),t0),dur=.45)]),
   SPR('s23',680,290,560,R(ST('만남을'),t0)-0.2,anim='rise',float_=6),
   H("만남을 <span class='g'>'심사받는 자리'</span>로 생각하기 때문",0,840,1920,56,R(ST('만남을'),t0)+0.3,align='center',dark=True,st=.02),grain()],bg=CREAMBG)
t0,t1=t1,B[7]; _set(t0)
scene(t0,t1,[*navy(),IBOX('magnet',820,120,280,0.1),
   html('<div style="width:280px;height:280px;border-radius:50%;border:12px solid #e0524a;box-sizing:border-box;position:relative"><div style="position:absolute;left:50%;top:50%;width:300px;height:12px;margin-left:-150px;margin-top:-6px;background:#e0524a;border-radius:6px;transform:rotate(-45deg)"></div></div>',820,120,280,280,at=0.6,anim='pop'),
   P('점수 따려고 애쓰는 사람에게는',0,470,1920,56,0.3,align='center',weight=600),
   H('<span class="g">그 누구도 끌리지 않습니다</span>',0,560,1920,100,R(WT('누구도'),t0),align='center',st=.04),grain()],bg=NAVYBG)
# ====================================================== S8
t0,t1=B[7],cut('첫 번째는'); _set(t0)
br='''<svg width="900" height="200" viewBox="0 0 900 200"><path d="M450 0 C450 90 120 90 120 190" fill="none" stroke="#c9a24a" stroke-width="5" stroke-linecap="round"/><path d="M450 0 L450 190" fill="none" stroke="#c9a24a" stroke-width="5" stroke-linecap="round"/><path d="M450 0 C450 90 780 90 780 190" fill="none" stroke="#c9a24a" stroke-width="5" stroke-linecap="round"/></svg>'''
scene(t0,t1,[*navy(),KICK("THE LION'S 12",0,120,0.05,align='center',w=1920),
   html('<div style="font-size:250px;font-weight:800;color:#e2c27a;text-align:center;line-height:1;letter-spacing:-.04em"><span class="num">0</span></div>',0,160,1920,None,at=0.1,anim='rise',count=[0,12,0,1.1]),
   H('사자의 태도 12가지',0,430,1920,72,0.4,align='center'),
   html(br,510,560,900,200,at=R(ST('크게 세 갈래'),t0),anim='wipev',dur=.7),
   *[IBOX(n,510+x-50,750,100,R(ST('크게 세 갈래'),t0)+0.5+j*0.12,ring=False) for j,(n,x) in enumerate((('anchor',120),('compass',450),('magnet',780)))],grain()],bg=NAVYBG)
t0,t1=t1,cut('몸에 밴'); _set(t0)
slide(8,t0,t1,[('t',t0,'fade'),('a',t0+0.1,'up'),('b',ST('두 번째는')-0.1,'up'),('c',ST('세 번째는')-0.1,'up')],
      spot=[(t0+0.5,'a'),(ST('두 번째는'),'b'),(ST('세 번째는'),'c')])
t0,t1=t1,B[8]; _set(t0)
items=[*navy(),H('하이에나의 태도를 걷어내고, <span class="g">사자의 태도</span>로',0,110,1920,60,0.05,align='center',st=.02)]
USED_ICONS.update(['dog','crown'])
for k in range(12):
    cx=470+(k%6)*170; cy=290+(k//6)*190; at=0.7+k*0.26
    items.append(html('<div class="ibox" style="width:140px;height:140px;background:#2a3a5e;color:#9aa7c4"><i class="ic" data-ic="dog" style="width:50%;height:50%"></i></div>',cx,cy,140,140,at=0.1+k*0.03,anim='pop',out=dict(at=at,anim='shrink',dur=.22)))
    items.append(html('<div class="ibox" style="width:140px;height:140px;background:linear-gradient(135deg,#e2c27a,#b8892f);color:#14213f;box-shadow:0 10px 30px rgba(201,162,74,.4)"><i class="ic" data-ic="crown" style="width:50%;height:50%"></i></div>',cx,cy,140,140,at=at+0.18,anim='pop'))
items+=[H('부트캠프 안에서 하나씩 <span class="g">몸으로</span> 익힙니다',0,730,1920,56,R(ST('자세한 건'),t0),align='center',st=.02),grain()]
scene(t0,t1,items,bg=NAVYBG)
# ====================================================== S9
t0,t1=B[8],B[9]; _set(t0)
nt=[WT('진단으로'),WT('1단계'),WT('2단계'),WT('3단계'),WT('4단계'),WT('5단계'),WT('6단계')]
rev=[('t',t0+0.05,'up')]+[(f'n{k}',nt[k]-0.05,'pop') for k in range(7)]+[('m1',ST('앞의 네')+0.1,'wipe'),('m2',ST('뒤의 두')+0.1,'wipe')]
spot=[(nt[k]+0.05,f'n{k}') for k in range(7)]+[(ST('앞의 네'),['n0','n1','n2','n3','n4','m1']),(ST('뒤의 두'),['n5','n6','m2'])]
slide(9,t0,t1,rev,spot=spot)
# ====================================================== S10
t0,t1=B[9],cut('그리고 녹화된'); _set(t0)
scene(t0,t1,[ill('a13'),shade('b'),
   html('<div style="display:flex;align-items:center;gap:12px;font-size:30px;font-weight:800;color:#fff;background:rgba(224,82,74,.9);padding:10px 20px;border-radius:999px"><span style="width:16px;height:16px;border-radius:50%;background:#fff"></span>REC</div>',1640,120,200,None,at=R(ST('진단에서 실제'),t0),anim='pop',pulse=[R(ST('진단에서 실제'),t0)+1.0,R(ST('진단에서 실제'),t0)+2.0]),
   H('실제 상황처럼 <span class="g">대화해 보기</span>',140,800,1500,76,R(ST('진단에서 실제'),t0)),grain()])
t0,t1=t1,B[10]; _set(t0)
slide(10,t0,t1,[('t',t0+0.05,'up'),('a',t0+0.1,'up'),('b',t0+0.35,'up'),('c',ST('진단이 끝나면'),'pop')],spot=[(t0+0.9,'b'),(ST('진단이 끝나면')+0.2,'c')])
# ====================================================== S11
t0,t1=B[10],B[11]; _set(t0)
slide(11,t0,t1,[('t',t0+0.05,'up'),('s0',ST('강의를 통해'),'pop'),('ar0',ST('배운 걸')-0.2,'left'),('s1',ST('배운 걸'),'pop'),('ar1',ST('단계가 끝나면')-0.2,'left'),('s2',ST('단계가 끝나면'),'pop'),
            ('ar2',ST('그렇게 한')-0.2,'left'),('s3',ST('그렇게 한'),'pop'),('pill',ST('시간은'),'up')],
      spot=[(ST('강의를 통해')+0.2,'s0'),(ST('배운 걸')+0.2,'s1'),(ST('단계가 끝나면')+0.2,'s2'),(ST('그렇게 한')+0.2,'s3'),(ST('시간은')+0.2,'pill')])
# ====================================================== S12
t0,t1=B[11],cut('같이 롤플레잉'); _set(t0)
slide(12,t0,t1,[('t',t0+0.05,'up')]+[(f'w{k}',WT('6번')+k*0.18,'pop') for k in range(6)],spot=[(WT('90분'),['w0','w1','w2','w3','w4','w5'])])
t0,t1=t1,cut('그리고 같은 장면을'); _set(t0)
ret='<div class="ret" style="position:absolute;left:{}px;top:60px;width:300px;height:340px;border:6px solid #e2c27a;border-radius:24px;box-shadow:0 0 0 9999px rgba(0,0,0,0),0 0 40px rgba(201,162,74,.8);opacity:0"></div>'
zw,zh=zoomwin(200,150,0.05,extra=ret.format(760+220),name2='수강생 (롤플레잉)')
zw['sub']=zw.get('sub',[])+[dict(sel='.ret',anim='pop',at=R(WT('핀포인트로'),t0),dur=.5)]
scene(t0,t1,[*navy(),zw,grain()],bg=NAVYBG)
t0,t1=t1,B[12]; _set(t0)
slide(12,t0,t1,[('t',None,''),*[(f'w{k}',None,'') for k in range(6)],('c0',None,''),('v0',None,''),('c1',None,''),('v1',t0+0.1,'fade'),('c2',t0+0.1,'up'),('v2',ST('녹화본도')-0.2,'fade'),('c3',ST('녹화본도'),'up')],
      spot=[(t0+0.6,'c2'),(ST('녹화본도')+0.2,'c3')])
# ====================================================== S13
t0,t1=B[12],cut('시작하는 날'); _set(t0)
scene(t0,t1,[*navy(),H(STK("'좀 나아진 것 같다'"),0,330,1920,96,0.05,align='center',sub=[dict(sel='.stl',anim='wipe',at=R(WT('판단하지'),t0),dur=.5)]),
   H('<span class="g">느낌</span>으로 판단하지 않습니다',0,500,1920,76,R(WT('느낌만으로'),t0),align='center'),grain()],bg=NAVYBG)
t0,t1=t1,B[13]; _set(t0)
slide(13,t0,t1,[('t',t0+0.05,'up'),('a',t0+0.2,'pop'),('b',WT('6주차')-0.1,'pop'),('c',WT('12주차')-0.1,'pop')],
      spot=[(t0+0.6,'a'),(WT('6주차'),'b'),(WT('12주차'),'c'),(ST('세 영상을'),None)],
      extra=[PILL('같은 조건 · 나란히 비교','scale',0,820,R(ST('세 영상을'),ST('시작하는 날')-0.1) if False else 0,c='n',css='display:none')])
SC[-1]['items'].pop()
# ====================================================== S14
t0,t1=B[13],cut('12주 뒤에는'); _set(t0)
_a=WT('진단부터'); _b=max(WT('시작될')+0.3,_a+2.4); _d=(_b-_a)/3
mil=[('stethoscope','진단',_a),('dumbbell','12주 훈련',_a+_d),('message-square-heart','실제 만남',_a+2*_d),('heart','연애 시작',_b)]
its=[*navy(),KICK('START TO FINISH',0,170,0.05,align='center',w=1920),H('진단부터 연애가 시작될 때까지',0,220,1920,70,0.1,align='center'),
     html('<div style="width:100%;height:6px;border-radius:3px;background:linear-gradient(90deg,#8ea2cc,#c9a24a)"></div>',360,563,1200,6,at=R(mil[0][2],t0),anim='grow',dur=R(mil[3][2],mil[0][2])+0.3,origin='0% 50%')]
for k,(ic,lb,a) in enumerate(mil):
    x=360+k*400-80
    its.append(IBOX(ic,x,486,160,R(a,t0),bg='#14213f' if k<3 else 'linear-gradient(135deg,#e2c27a,#b8892f)',color='#e2c27a' if k<3 else '#14213f'))
    its.append(P(lb,x-70,680,300,40,R(a,t0)+0.15,align='center',color='#fff',weight=700))
its+=[H('<span class="g">처음부터 끝까지</span> 같이 갑니다',0,800,1920,56,R(WT('처음부터'),t0),align='center',st=.02),grain()]
scene(t0,t1,its,bg=NAVYBG)
t0,t1=t1,cut('그리고 이건'); _set(t0)
slide(14,t0,t1,[('t',t0+0.05,'up'),('a',WT('원하는')-0.1,'up'),('b',WT('호감을')-0.1,'up'),('c',WT('관계를')-0.1,'up')],
      spot=[(WT('원하는'),'a'),(WT('호감을'),'b'),(WT('관계를'),'c'),(ST('모든 강의와'),['a','b','c'])])
t0,t1=t1,B[14]; _set(t0)
rays='<div style="width:1400px;height:1400px;border-radius:50%;background:radial-gradient(circle,rgba(201,162,74,.32) 0%,rgba(201,162,74,0) 60%)"></div>'
scene(t0,t1,[*navy(),html(rays,260,-200,1400,1400,anim='fade',dur=1.5,spin=40),KICK('자신 있게 말씀드립니다',0,200,0.1,align='center',w=1920),
   H('내 영상을 <span class="g">장면 단위</span>로 보며<br>태도 자체를 고쳐주는 1:1 훈련',0,270,1920,72,R(ST('내 모습을'),t0),align='center',st=.02),
   IBOX('award',860,540,200,R(WT('단언코'),t0),bg='linear-gradient(135deg,#e2c27a,#b8892f)',color='#14213f'),
   H('<span class="g">국내 유일</span>',0,770,1920,84,R(WT('단언코'),t0)+0.2,align='center',st=.06),grain()],bg=NAVYBG)
# ====================================================== S15
t0,t1=B[14],cut('대부분의'); _set(t0)
scene(t0,t1,[ill('a07'),shade('all'),H('강의만 들어서 연애가 된다면?',0,320,1920,82,R(ST('강의를 듣기만'),t0),align='center'),
   H('<span class="g">현실은 그렇지 않습니다</span>',0,470,1920,100,R(ST('그런데 현실은'),t0),align='center',st=.04),grain()])
t0,t1=t1,B[15]; _set(t0)
slide(15,t0,t1,[('t',t0+0.05,'up'),('a',t0+0.15,'left'),('ar',ST('그래서 이다사')-0.2,'pop'),('b',ST('그래서 이다사'),'right')],
      spot=[(t0+0.6,'a'),(ST('그래서 이다사')+0.2,'b')])
# ====================================================== S16
t0,t1=B[15],cut('이렇게 집중하는'); _set(t0)
slide(16,t0,t1,[('t',t0+0.05,'up'),('a',ST('첫 번째는 12주'),'wipe'),('i0',WT('28편'),'up'),('i1',WT('매일'),'up'),('i4',WT('실전'),'up'),('i5',WT('코칭',WT('실전')),'up')],
      nodim=('a',),spot=[(WT('28편'),'i0'),(WT('매일'),'i1'),(WT('실전'),'i4'),(WT('코칭',WT('실전')),'i5'),(WT('바꿉니다',WT('실전')),None)])
t0,t1=t1,cut('두 번째는 수료'); _set(t0)
ch='''<svg width="1200" height="460" viewBox="0 0 1200 460">
<line x1="60" y1="400" x2="1180" y2="400" stroke="rgba(255,255,255,.3)" stroke-width="2"/><line x1="60" y1="20" x2="60" y2="400" stroke="rgba(255,255,255,.3)" stroke-width="2"/>
<text x="1180" y="440" fill="#9aa7c4" font-size="26" text-anchor="end" font-family="P">시간</text><text x="74" y="30" fill="#9aa7c4" font-size="26" font-family="P">변화</text>
<polyline fill="none" stroke="#7f8aa3" stroke-width="7" stroke-linecap="round" stroke-dasharray="2 16" points="60,330 250,290 420,300 600,350 800,385 1150,395"/>
<polyline fill="none" stroke="#e2c27a" stroke-width="9" stroke-linecap="round" points="60,330 250,280 450,220 650,160 850,105 1150,60"/></svg>'''
scene(t0,t1,[*navy(),H('집중하는 기간이 없으면?',0,100,1920,66,0.05,align='center'),html(ch,360,240,1200,460,at=0.3,anim='wipe',dur=2.0),
   PILL('혼자 · 흐지부지','frown',1300,640,R(WT('흐지부지'),t0),c='t',size=26),PILL('12주 집중','trending-up',1330,230,R(ST('그래서 12주'),t0),c='g',size=26),
   H('12주 안에 <span class="g">확실히</span> 바꿉니다',0,780,1920,56,R(ST('그래서 12주'),t0)+0.2,align='center',st=.02),grain()],bg=NAVYBG)
t0,t1=t1,cut('썸이 생겼을'); _set(t0)
LEFT=[('t',None,''),('a',None,''),('i0',None,''),('i1',None,''),('i4',None,''),('i5',None,'')]
slide(16,t0,t1,LEFT+[('b',t0+0.1,'wipel')],spot=[(t0+0.5,'b')])
t0,t1=t1,cut('평생 회원에게는'); _set(t0)
mm=[('sparkles','썸이 생겼을 때',WT('썸이')),('heart','연애를 시작했을 때',WT('연애를')),('zap','같은 문제로 다툴 때',WT('다툴')),('gem','결혼을 고민할 때',WT('결혼을'))]
its=[*navy(),H('진짜 연애는 <span class="g">12주 뒤</span>부터',0,110,1920,66,0.05,align='center'),
     html('<div style="width:100%;height:4px;border-radius:2px;background:rgba(255,255,255,.22)"></div>',300,438,1320,4,at=R(mm[0][2],t0),anim='grow',dur=R(mm[3][2],mm[0][2])+0.3,origin='0% 50%')]
USED_ICONS.add('refresh-cw')
for k,(ic,lb,a) in enumerate(mm):
    x=300+k*440-70
    its.append(IBOX(ic,x,370,140,R(a,t0),bg='#24385f',ring=False))
    its.append(P(lb,x-90,540,320,36,R(a,t0)+0.1,align='center',color='#fff',weight=700))
    its.append(html('<div class="ibox" style="width:64px;height:64px;background:#c9a24a;color:#14213f"><i class="ic" data-ic="refresh-cw" style="width:55%;height:55%"></i></div>',x+38,620,64,64,at=R(ST('그때마다'),t0)+k*0.12,anim='pop'))
its+=[H('그때마다 돌아와서 <span class="g">점검</span>',0,760,1920,56,R(ST('그때마다'),t0),align='center',st=.03),grain()]
scene(t0,t1,its,bg=NAVYBG)
t0,t1=t1,cut('결혼을 결심'); _set(t0)
ALL=LEFT+[('b',None,'')]
slide(16,t0,t1,ALL+[('i2',WT('SOS'),'pop'),('i3',ST('첫 연애'),'pop')],nodim=('a','b'),spot=[(t0+0.2,'b'),(WT('SOS'),'i2'),(ST('첫 연애'),'i3')])
t0,t1=t1,cut('썸에서 결혼까지'); _set(t0)
scene(t0,t1,[ill('a08'),shade('all'),H('<span class="g">프러포즈 기획</span>',0,330,1920,120,R(WT('프러포즈'),t0),align='center',st=.04),
   H('결혼 준비 가이드까지',0,500,1920,96,R(ST('결혼 준비하면서'),t0),align='center',st=.04),grain()])
t0,t1=t1,B[16]; _set(t0)
slide(16,t0,t1,ALL+[('i2',None,''),('i3',None,''),('i6',t0+0.1,'pop'),('i7',t0+0.3,'pop')],spot=[],
      extra=[H('썸에서 결혼까지, <span class="g">갈림길마다 옆에</span>',0,820,1920,48,0.5,align='center',dark=True,st=.02)])
# ====================================================== S17
t0,t1=B[16],cut('둘 다 VAT'); _set(t0)
perks=[('life-buoy','SOS 핫라인',WT('SOS')),('book-open','새 강의 무료',WT('새',WT('SOS'))),('gem','프러포즈 기획',WT('프러포즈')),('clipboard-check','결혼 준비 가이드',WT('결혼',WT('프러포즈')))]
ex=[]

slide(17,t0,t1,[('t',t0+0.05,'up'),('a',ST('12주 부트캠프는'),'pop'),('b',ST('평생 회원까지 더하면'),'pop')],
      spot=[(ST('12주 부트캠프는')+0.2,'a'),(ST('평생 회원까지 더하면')+0.2,'b')],extra=ex)
t0,t1=t1,B[17]; _set(t0)
scene(t0,t1,[*navy(),PILL('둘 다 VAT 별도','file-text',790,200,0.1,c='t'),IBOX('circle-help',880,330,160,R(WT('비싼데'),t0),ring=False,bg='#24385f'),
   H("혹시 지금 <span class='g'>'좀 비싼데?'</span>",0,540,1920,100,R(ST('혹시 지금'),t0),align='center',st=.04),grain()],bg=NAVYBG)
# ====================================================== S18
t0,t1=B[17],cut('심리 상담만'); _set(t0)
scene(t0,t1,[*navy(),H('아뇨, <span class="g">전혀 비싸지 않습니다</span>',0,340,1920,96,0.05,align='center',st=.04),
   P('1:1로 꾸준히 도움받는 건 원래 비용이 많이 듭니다',0,520,1920,46,R(ST('누군가에게'),t0),align='center'),grain()],bg=NAVYBG)
t0,t1=t1,cut('부트캠프에 평생'); _set(t0)
def crow(y,lab,val,at,unit='만 원',gold=False,op=''):
    c='#e2c27a' if gold else '#fff'
    return html(f'<div style="display:flex;align-items:baseline;justify-content:space-between;width:760px;border-bottom:1px solid rgba(255,255,255,.15);padding:18px 0"><span style="font-size:34px;color:#c9d2e6;font-weight:600">{op}{lab}</span><span style="font-size:{86 if gold else 64}px;font-weight:800;color:{c};letter-spacing:-.03em"><span class="num">0</span>{unit}</span></div>',1040,y,760,None,at=at,anim='up',count=[0,val,0,1.0])
scene(t0,t1,[*navy(),FRAME('a09',120,230,820,461,0.05),KICK('1:1 심리상담 (가정)',1040,200,0.1),
   crow(260,'1회',18,0.2),crow(400,'× 월 4회',72,R(WT('네'),t0)),crow(540,'× 12개월',864,R(WT('1년이면'),t0),gold=True),
   P('1년이면 <b style="color:#e2c27a">800만 원</b>이 넘습니다',1040,760,760,40,R(WT('800만'),t0),color='#fff',weight=600),grain()],bg=NAVYBG)
t0,t1=t1,B[18]; _set(t0)
slide(18,t0,t1,[('t',t0+0.05,'up'),('l1',t0+0.1,'fade'),('b1',t0+0.2,'wipe'),('v1',t0+0.8,'fade'),('l2',t0+0.4,'fade'),('b2',t0+0.6,'wipe'),('v2',t0+1.0,'pop')],
      spot=[(WT('6분의'),['b2','v2'])],dim=False)
# ====================================================== S19
t0,t1=B[18],cut('12주가 끝나도'); _set(t0)
slide(19,t0,t1,[('t',t0+0.05,'up'),('big',WT('10만'),'pop'),('pill',ST('상담 한 번'),'up')],spot=[(WT('10만')+0.3,'big'),(ST('상담 한 번')+0.2,'pill')],dim=False)
t0,t1=t1,cut('소개팅 한 번'); _set(t0)
scene(t0,t1,[*cream(),SPR('s25',120,250,880,0.05,anim='pop',float_=10),
   H('12주가 끝나도<br><span class="g">트레이너는 그대로</span>',1060,200,800,76,0.1,dark=True),
   PILL('썸이 생길 때','sparkles',1060,450,R(WT('썸이'),t0),c='w'),PILL('연애를 시작할 때','heart',1060,550,R(WT('연애를'),t0),c='w'),
   PILL('다시 흔들릴 때','zap',1060,650,R(WT('흔들릴'),t0),c='w'),PILL('언제든 점검','refresh-cw',1060,750,R(WT('언제든'),t0),c='g'),grain()],bg=CREAMBG)
t0,t1=t1,cut('혼자서 같은'); _set(t0)
scene(t0,t1,[ill('a10'),html('',0,0,1920,1080,anim='none',css='background:rgba(10,18,38,.5)'),
   html('<div class="ncard" style="padding:36px 48px;width:600px"><div style="font-size:30px;opacity:.75">소개팅 한 번</div><div style="font-size:56px;font-weight:800;margin-top:6px">밥값 + 카페값</div></div>',200,360,600,None,at=0.2,anim='left'),
   P('vs',860,410,200,80,0.8,align='center',color='#e2c27a',weight=800),
   html('<div class="gcard" style="padding:36px 48px;width:640px"><div style="font-size:30px;opacity:.75">월 10만 원대</div><div style="font-size:56px;font-weight:800;margin-top:6px">평생 태도 트레이너</div></div>',1080,360,640,None,at=1.2,anim='right'),
   H('<span class="g">남는 장사</span>입니다',0,700,1920,72,R(WT('남는'),t0),align='center'),grain()])
t0,t1=t1,B[19]; _set(t0)
scene(t0,t1,[*navy(),IBOX('repeat',860,150,200,0.1,bg='#24385f',color='#9aa7c4',ring=False),
   P('혼자 같은 실수를 반복하며 버리는 <b style="color:#fff">시간과 돈</b>',0,410,1920,52,0.3,align='center',weight=600),
   IBOX('trending-up',870,540,180,R(WT('오히려'),t0)),H('오히려 <span class="g">돈을 버는 선택</span>',0,770,1920,84,R(WT('오히려'),t0)+0.2,align='center',st=.04),grain()],bg=NAVYBG)
# ====================================================== S20
t0,t1=B[19],cut("'한 방에"); _set(t0)
scene(t0,t1,[*navy(),P('솔직하게 말씀드릴게요',0,290,1920,56,0.05,align='center'),IBOX('ban',880,400,160,R(ST('이런 분은'),t0),bg='#e0524a',color='#fff',ring=False),
   H('이런 분은 <span class="g">신청하지 마세요</span>',0,630,1920,92,R(ST('이런 분은'),t0)+0.1,align='center',st=.04),grain()],bg=NAVYBG)
t0,t1=t1,cut('반대로 나를'); _set(t0)
slide(20,t0,t1,[('t',t0,'fade'),('a',t0+0.1,'up'),('b',ST('2주에 과제'),'up'),('c',ST('특정 여성을'),'up')],spot=[(t0+0.5,'a'),(ST('2주에 과제'),'b'),(ST('특정 여성을'),'c')])
t0,t1=t1,B[20]; _set(t0)
scene(t0,t1,[ill('a12'),shade('r'),P('진심으로 표현하고, 행복한 연애를 위해<br>변하고 싶은 분이라면',900,340,920,48,0.2,align='right',color='#fff',weight=600),
   H('<span class="g">끝까지 같이 가겠습니다</span>',700,520,1120,92,R(ST('끝까지 같이'),t0),align='right',st=.04),grain()])
# ====================================================== S21
t0,t1=B[20],cut('"저는 원래'); _set(t0)
scene(t0,t1,[ill('a11'),shade('r'),H('해보고는 싶은데…',900,330,920,76,0.1,align='right'),H('이런 <span class="g">걱정</span> 드시나요?',900,450,920,76,R(ST('이런 걱정이'),t0),align='right'),grain()])
t0,t1=t1,cut('하지만 과제를'); _set(t0)
slide(21,t0,t1,[('t',t0,'fade'),('a',t0+0.1,'up'),('b',ST('"나이가'),'up'),('c',ST('"연애 경험'),'up'),('d',ST('"시간이'),'up')],
      spot=[(t0+0.5,'a'),(ST('"나이가'),'b'),(ST('"연애 경험'),'c'),(ST('"시간이'),'d')])
t0,t1=t1,B[21]; _set(t0)
scene(t0,t1,[*navy(),IBOX('clipboard-check',560,250,200,0.1),html(f'<div style="color:#e2c27a;width:90px;height:90px">{IC("arrow-right")}</div>',915,305,90,90,at=0.6,anim='left',css='font-size:90px'),IBOX('users',1160,250,200,0.8),
   P('과제',560,480,200,40,0.2,align='center',color='#fff',weight=700),P('1:1 코칭',1110,480,300,40,0.9,align='center',color='#fff',weight=700),
   H('과제를 해야 <span class="g">코칭이 진행</span>됩니다',0,600,1920,66,R(ST('과제를 반드시'),t0),align='center',st=.03),
   P('어렵지 않아요. 주 1~2시간이면 충분합니다',0,760,1920,44,R(ST('그렇다고 과제가'),t0),align='center'),grain()],bg=NAVYBG)
# ====================================================== S22
t0,t1=B[21],cut('그러니 부담'); _set(t0)
slide(22,t0,t1,[('t',t0+0.05,'up'),('a',t0+0.2,'pop'),('ar1',ST('먼저 고쳐야')-0.2,'left'),('b',ST('먼저 고쳐야'),'pop'),('ar2',ST('진단이 끝나고')-0.2,'left'),('c',ST('진단이 끝나고'),'pop'),('pill',ST('지금까지 이다사'),'up')],
      spot=[(t0+0.6,'a'),(ST('먼저 고쳐야')+0.2,'b'),(ST('진단이 끝나고')+0.2,'c'),(ST('지금까지 이다사')+0.2,'pill')])
t0,t1=t1,B[22]; _set(t0)
scene(t0,t1,[ill('a04'),shade('l'),H('부담 갖지 마시고,<br><span class="g">평소 모습 그대로</span> 오세요',140,380,1100,80,0.2),grain()])
# ====================================================== S23
USED_ICONS.update(['search','x'])
def endpage(t0,show_all,cta_at=None,t1_at=None,t2_at=None,s_at=0.1):
    sb=f'''<div style="display:flex;align-items:center;gap:20px;padding:20px 34px;border-radius:999px;background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.2);color:#c9d2e6;font-size:36px;font-weight:500;backdrop-filter:blur(8px)">
<i class="ic" data-ic="search" style="width:36px;height:36px"></i>{STK('소개팅 대화 주제','gold')}<i class="ic" data-ic="x" style="width:32px;height:32px;margin-left:40px;color:#e2c27a"></i></div>'''
    it=[*navy(),*dust(18,7),html(sb,0,170,1920,None,at=0 if show_all else s_at,anim='none' if show_all else 'down',css='display:flex;justify-content:center',
        sub=[dict(sel='.stl',anim='none' if show_all else 'wipe',at=(0 if show_all else s_at+0.6),dur=.5)] if not show_all else [])]
    if show_all:
        it[-1]['css']+=';'
        it[-1]['html']=it[-1]['html'].replace('class="stl gold"','class="stl gold" style="clip-path:inset(0% 0% 0% 0%)"')
    it.append(H('멘트 검색은',0,330,1920,96,0 if show_all else t1_at,align='center',st=.04) if not show_all else html('<div class="h" style="font-size:96px;text-align:center">멘트 검색은</div>',0,330,1920,None,anim='none'))
    it.append(H('<span class="g">이제 그만하셔도 됩니다</span>',0,460,1920,112,t2_at,align='center',st=.04) if not show_all else html('<div class="h" style="font-size:112px;text-align:center"><span class="g">이제 그만하셔도 됩니다</span></div>',0,460,1920,None,anim='none'))
    return it
t0,t1=B[22],cut('있는 그대로'); _set(t0)
scene(t0,t1,endpage(t0,False,t1_at=R(ST('이제는 멘트를'),t0),t2_at=R(WT('태도를',ST('이제는 멘트를')),t0))+[grain()],bg=NAVYBG)
t0,t1=t1,cut('지금 바로'); _set(t0)
scene(t0,t1,[ill('a12'),shade('b'),H('있는 그대로의 내 모습으로,<br><span class="g">다음 만남</span>을 잡으러 가시죠',0,640,1920,72,0.15,align='center',st=.02),grain()])
t0,t1=t1,END; _set(t0)
cta=html('<div class="ctab"><span class="shine"></span><span style="position:relative">90분 진단 신청하기</span></div>',0,700,1920,None,at=0.2,anim='pop',dur=.8,css='display:flex;justify-content:center',
         pulse=[R(WT('신청하세요'),t0)],sub=[dict(sel='.shine',p=dict(x=1100),at=0.9,dur=1.4,ease='power2.inOut'),dict(sel='.shine',p=dict(x=0),at=2.4,dur=0.01),dict(sel='.shine',p=dict(x=1100),at=2.5,dur=1.4,ease='power2.inOut')])
scene(t0,t1,endpage(t0,True)+[cta,grain()],bg=NAVYBG)
# ---------- subtitles
subs=[]
for k,(st,en,t,ws) in enumerate(FA):
    nxt=FA[k+1][0] if k+1<len(FA) else en+1
    s0=max(0,st-0.04)
    e=nxt-0.03 if nxt-en<0.6 else min(nxt-0.03,en+0.3)
    subs.append([round(s0,3),round(e,3),re.sub(r'[.,]$','',t)])
for k in range(len(SC)-1):
    assert abs(SC[k]['t1']-SC[k+1]['t0'])<1e-6,(k,SC[k]['t1'],SC[k+1]['t0'])
    assert SC[k]['t1']>SC[k]['t0'],(k,SC[k])
spec=dict(duration=END,scenes=SC,subs=subs,chapters=CH)
htmls=f'''<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="style.css"></head><body>
<div id="stage"></div><div id="chap"></div><div id="sub"><span id="subt"></span></div>
<script src="gsap.min.js"></script><script>{icons_js()}</script><script>window.SPEC={json.dumps(spec,ensure_ascii=False)};</script><script src="runtime.js"></script></body></html>'''
open(f'{S}/eng/index.html','w').write(htmls)
json.dump([round(x['t0']+0.8*(x['t1']-x['t0']),2) for x in SC],open(f'{S}/w/mids.json','w'))
print('scenes',len(SC),'dur',END)
