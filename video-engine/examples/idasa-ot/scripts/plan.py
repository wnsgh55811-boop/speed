import json,re,sys
sys.path.insert(0,'/tmp/claude-0/-home-user-speed/0d948206-c1a3-547f-9fa6-f85521be224c/scratchpad/scripts')
from lib import *
asr=json.load(open(f'{S}/w/asr.json'))
WS=[(w0,w1,w.strip()) for s in asr for w0,w1,w in s['words']]
CH=[];CT=[]
for w0,w1,w in WS:
    for j,c in enumerate(w): CH.append(c); CT.append(w0+(w1-w0)*j/max(1,len(w)))
CHS=''.join(CH)
def W(s,after=0):
    s=s.replace(' ','')
    for m in re.finditer(re.escape(s),CHS):
        if CT[m.start()]>=after-0.05: return round(CT[m.start()],3)
    raise Exception('notfound '+s)
END=565.63+1.6
SC=[]
def scene(t0,t1,items,bg=None,cam=None,xf=True):
    d=dict(t0=t0,t1=t1,items=items,xf=xf)
    if bg: d['bg']=bg
    if cam: d['cam']=cam
    SC.append(d)
NAVY='radial-gradient(120% 90% at 50% 40%,#24385f 0%,#14213f 55%,#0a1226 100%)'
LIGHT='radial-gradient(90% 60% at 50% 0%,#f6efe0 0%,rgba(246,239,224,0) 60%),linear-gradient(180deg,#f5f6fa,#e6eaf3)'
def R(t,t0): return round(t-t0,3)
def plate(n): return img(f'assets/p{n:02d}.jpg',anim='none')
def photo(i,kb=(1.04,1.14,0,0,0,0),**k): return img(f'img/i{i:02d}.jpg',-96,-54,2112,1188,anim='none',kb=list(kb),**k)
def ov(cls): return html('',0,0,1920,1080,anim='none',cls=cls)
def T(h,x,y,w,at,size=84,anim='up',color='#fff',align='left',weight=700,**k):
    return html(f'<div style="font-size:{size}px;font-weight:{weight};color:{color};text-align:{align};line-height:1.2">{h}</div>',x,y,w,None,at=at,anim=anim,**k)
def kick(t,x,y,at,align='left',w=900,color='#e2c27a'):
    return html(f'<div class="kicker" style="text-align:{align};color:{color}">{t}</div>',x,y,w,None,at=at,anim='fade')
def chip(t,ic,x,y,at,cls='',anim='pop',**k):
    i=IC(ic) if ic else ''
    return html(f'<div class="chip {cls}">{i}<span>{t}</span></div>',x,y,None,None,at=at,anim=anim,**k)
def bigicon(name,x,y,size,at,bg='#14213f',color='#e2c27a',anim='pop',ring=True,**k):
    USED_ICONS.add(name)
    b=f'box-shadow:0 0 0 10px rgba(201,162,74,.18),0 20px 50px rgba(0,0,0,.35);' if ring else ''
    return html(f'<div class="circ" style="width:{size}px;height:{size}px;background:{bg};color:{color};{b}"><i class="ic" data-ic="{name}" style="width:52%;height:52%"></i></div>',x,y,size,size,at=at,anim=anim,**k)
def strike(x,y,w,at,color='#e0524a',h=8):
    return html(f'<div style="width:100%;height:{h}px;background:{color};border-radius:4px;box-shadow:0 2px 10px rgba(0,0,0,.3)"></div>',x,y,w,h,at=at,anim='wipe',dur=.45)
def xstamp(x,y,size,at):
    USED_ICONS.add('x')
    return html(f'<div class="circ" style="width:{size}px;height:{size}px;background:#e0524a;color:#fff;box-shadow:0 10px 30px rgba(224,82,74,.5)"><i class="ic" data-ic="x" style="width:60%;height:60%"></i></div>',x,y,size,size,at=at,anim='pop')
def okstamp(x,y,size,at):
    USED_ICONS.add('check')
    return html(f'<div class="circ" style="width:{size}px;height:{size}px;background:#c9a24a;color:#14213f;box-shadow:0 10px 30px rgba(201,162,74,.5)"><i class="ic" data-ic="check" style="width:60%;height:60%"></i></div>',x,y,size,size,at=at,anim='pop')
def fz(n,key,z): x,y,w,h=rect(n,key); return focus(x+w/2,y+h/2,z)
def camk(t,f,d=1.1): f=dict(f); f['t']=t; f['d']=d; return f
FULL=dict(s=1,x=0,y=0)
def drift(t0,t1,z=1.05): return [dict(s=1,x=0,y=0),dict(t=0,d=t1-t0+0.3,e='sine.inOut',**focus(960,500,z))]
def search_box(x,y,w,txt,at,typedur=1.0,items=None,struck=False,minh=0):
    USED_ICONS.add('search'); USED_ICONS.add('history')
    h=f'''<div style="width:{w}px;background:#fff;border-radius:28px;box-shadow:0 30px 80px rgba(0,0,0,.45);padding:34px 40px 26px;box-sizing:border-box;min-height:{minh}px">
 <div style="display:flex;align-items:center;gap:22px;font-size:46px;color:#1b2236;font-weight:500;border-bottom:2px solid #eceef3;padding-bottom:24px">
  <i class="ic" data-ic="search" style="width:50px;height:50px;color:#1b2236"></i><span class="typed"></span><span class="caret" style="display:inline-block;width:3px;height:48px;background:#c9a24a"></span>
  <span style="margin-left:auto;width:72px;height:72px;border-radius:50%;background:#c9a24a;display:flex;align-items:center;justify-content:center;color:#14213f"><i class="ic" data-ic="search" style="width:36px;height:36px"></i></span></div>'''
    h+='<div class="list" style="padding-top:12px"></div></div>'
    return html(h,x,y,w,None,at=at,anim='up',type=txt,typedur=typedur,typedelay=0.25)
def search_items(x,y,w,rows,ats,hl=0):
    out=[]
    for k,(r,a) in enumerate(zip(rows,ats)):
        bg='background:#f3e7c4;' if k==hl else ''
        out.append(html(f'<div style="{bg}border-radius:14px;display:flex;align-items:center;gap:20px;font-size:36px;color:{"#1b2236" if k==hl else "#6b7184"};padding:16px 22px;font-weight:{600 if k==hl else 400}"><i class="ic" data-ic="history" style="width:36px;height:36px;color:#9aa0b0"></i>{r}</div>',x,y+k*84,w,None,at=a,anim='left',dur=.45))
    return out
# ======================= S1 OPENING
t=0
sb=search_box(470,150,980,'소개팅 대화 주제',0.0,typedur=1.1,minh=580)
rows=['여자 번호 따는 법','소개팅 대화 주제 추천','애프터 신청 멘트','카톡 답장 잘하는 법']
scene(0,7.30,[sb]+search_items(510,370,900,rows,[1.0,1.35,1.7,2.05])+[
    html('',0,0,1920,1080,anim='none',cls='vig'),
    kick('최근 검색어',532,322,0.8,w=400,color='#9aa0b0'),
],bg=NAVY,cam=[dict(s=1,x=0,y=0),dict(t=0,d=7.5,e='sine.inOut',**focus(960,470,1.08))],xf=False)
# B 7.3 - 11.1 crumpled scripts
t0,t1=7.30,11.10
scene(t0,t1,[photo(18,(1.12,1.0,0,0,0,0)),ov('shade-l'),
    kick('THE PROBLEM',150,330,0.1),
    T('처음부터<br><span class="g">멘트</span>가 문제가<br>아니었습니다',150,390,1100,R(8.62,t0),size=96),
    ])
# C 11.1-15.76 waiting for reply + kakao mock
t0,t1=11.10,15.76
USED_ICONS.update(['chevron-left','menu'])
phone=f'''<div style="width:560px;height:820px;border-radius:56px;background:#b2c7da;border:14px solid #10172a;box-shadow:0 40px 90px rgba(0,0,0,.55);overflow:hidden;position:relative">
<div style="height:96px;background:#a9bfd3;display:flex;align-items:center;padding:0 28px;font-size:30px;font-weight:600;color:#1b2236;gap:14px"><i class="ic" data-ic="chevron-left" style="width:34px;height:34px"></i>지난주 소개팅 그분</div></div>'''
def bub(t,side,y,at,meta=''):
    if side=='me':
        return html(f'<div style="display:flex;justify-content:flex-end;align-items:flex-end;gap:10px"><span style="font-size:22px;color:#3b4a5e">{meta}</span><div class="bubble me" style="position:relative;font-size:30px;padding:16px 22px">{t}</div></div>',1235,y,500,None,at=at,anim='up',dur=.4)
    return html(f'<div style="display:flex;align-items:flex-end;gap:10px"><div class="bubble you" style="position:relative;font-size:30px;padding:16px 22px">{t}</div><span style="font-size:22px;color:#3b4a5e">{meta}</span></div>',1235,y,500,None,at=at,anim='up',dur=.4)
scene(t0,t1,[photo(2,(1.06,1.16,0,0,-4,0)),ov('vig'),
    html(phone,1205,120,560,820,at=0.05,anim='right',dur=.5),
    bub('오늘 정말 즐거웠어요 :)','me',260,0.4,'<b style="color:#e0a400">1</b> 오후 10:12'),
    bub('네 저두요 ㅎㅎ','you',360,R(12.1,t0),'오전 9:40'),
    bub('이번 주말에 시간 괜찮으세요?','me',460,R(13.0,t0),'<b style="color:#e0a400">1</b> 오전 9:52'),
    html('<div style="font-size:24px;color:#2c3a50;background:rgba(255,255,255,.55);border-radius:20px;padding:8px 20px">… 3일째 읽지 않음</div>',1340,570,360,None,at=R(14.3,t0),anim='fade'),
    chip('두 번째 만남 ✕','calendar-x',150,780,R(12.4,t0),cls='navy'),
    chip('답장은 점점 늦어지고','clock',150,880,R(14.1,t0)),
])
# D 15.76-20.68 search again -> strike
t0,t1=15.76,20.68
sb2=search_box(470,330,980,'애프터 신청 멘트',0.0,typedur=0.9)
scene(t0,t1,[sb2, html('',0,0,1920,1080,anim='none',cls='vig'),
    kick('그리고 또 검색…',470,250,0.05,w=900,color='#9aa0b0'),
    strike(570,384,420,R(17.6,t0),color='#c9a24a',h=6),
    T('이 영상 끝까지 보시면<br><span class="g">그 검색은 이제 그만</span>',0,600,1920,R(17.9,t0),size=72,align='center'),
],bg=NAVY,cam=[dict(s=1,x=0,y=0),dict(t=1.6,d=3,e='sine.inOut',**focus(960,560,1.04))])
# E 20.68-26.52 title
t0,t1=20.68,26.52
scene(t0,t1,[
    T('왜 매번 <span class="g">흐지부지</span> 끝날까?',0,230,1920,0.1,size=80,align='center',out=dict(at=1.6)),
    kick('IDASA BOOTCAMP',0,330,R(22.3,t0),align='center',w=1920),
    T('이다사 <span class="g">12주</span> 부트캠프',0,390,1920,R(22.4,t0),size=120,align='center',anim='blur',dur=.9),
    html('<div style="width:100%;height:4px;background:linear-gradient(90deg,transparent,#c9a24a,transparent)"></div>',560,560,800,4,at=R(23.0,t0),anim='wipe'),
    T('무엇이 문제이고, 무엇을 바꾸는지',0,600,1920,R(23.4,t0),size=46,align='center',weight=500,color='#c9d2e6'),
],bg=NAVY,cam=drift(t0,t1,1.05))
# ======================= S2
t0,t1=26.52,34.62
scene(t0,t1,[plate(2),crop(2,'t',0.05),crop(2,'photo',R(28.46,t0),anim='zoom'),crop(2,'name',R(28.9,t0),anim='fade'),
    crop(2,'num',R(30.82,t0),anim='pop',pulse=[R(31.8,t0)]),crop(2,'pill',R(33.4,t0),anim='up')],
    cam=[dict(s=1,x=0,y=0),camk(R(30.9,t0),focus(1150,520,1.22),1.2),camk(R(33.6,t0),FULL,1.0)])
t0,t1=34.62,43.60
scene(t0,t1,[photo(3,(1.04,1.14,0,0,-3,-2)),ov('shade-b'),
    kick('1:1 녹화 피드백',140,520,0.1),
    T('듣고 끝나는 상담이 아닙니다',140,570,1300,0.2,size=70),
    html('<div style="display:flex;align-items:center;gap:14px;font-size:34px;font-weight:700;color:#fff"><span style="width:22px;height:22px;border-radius:50%;background:#e0524a;box-shadow:0 0 18px #e0524a"></span>REC</div>',1640,120,200,None,at=R(37.2,t0)),
    chip('말투','message-circle',140,700,R(38.9,t0)),chip('표정','smile',420,700,R(39.5,t0)),chip('시선','eye',700,700,R(40.1,t0)),
    html('<div style="height:10px;border-radius:5px;background:rgba(255,255,255,.25);overflow:hidden"><div style="width:100%;height:100%;background:#c9a24a"></div></div>',140,830,1640,10,at=R(41.04,t0),anim='wipe',dur=2.4),
    kick('한 장면씩 다시 보기',140,852,R(41.2,t0),w=700,color='#fff'),
])
t0,t1=43.60,48.46
chart='''<svg width="1100" height="360" viewBox="0 0 1100 360"><defs><linearGradient id="g1" x1="0" x2="1"><stop offset="0" stop-color="#7f93bd"/><stop offset="1" stop-color="#c9a24a"/></linearGradient></defs>
<line x1="0" y1="300" x2="1100" y2="300" stroke="rgba(255,255,255,.25)" stroke-width="2"/>
<polyline fill="none" stroke="url(#g1)" stroke-width="7" stroke-linecap="round" stroke-linejoin="round" points="0,170 120,150 220,175 330,140 430,160 520,135 600,150 660,290 720,300 800,210 900,190 1000,175 1100,160"/></svg>'''
scene(t0,t1,[kick('500명의 데이터',0,150,0.05,align='center',w=1920),
    T('남자가 <span class="g">무너지는 순간</span>이 보입니다',0,200,1920,0.15,size=76,align='center'),
    html(chart,410,400,1100,360,at=0.4,anim='wipe',dur=1.6),
    html('<div style="width:44px;height:44px;border-radius:50%;background:#e0524a;box-shadow:0 0 0 12px rgba(224,82,74,.25)"></div>',410+700-22,400+300-22,44,44,at=2.0,anim='pop'),
    html('<div class="chip" style="background:#e0524a;border-color:#e0524a">무너지는 순간</div>',1000,780,None,None,at=2.2,anim='pop'),
],bg=NAVY,cam=drift(t0,t1,1.04))
# ======================= S3 reviews
t0,t1=48.46,67.28
scene(t0,t1,[plate(3),crop(3,'r1',0.1,anim='pop'),crop(3,'r2',0.35,anim='pop'),crop(3,'r3',0.6,anim='pop'),crop(3,'r4',0.85,anim='pop'),
    ],cam=[dict(s=1,x=0,y=0),camk(R(52.0,t0),fz(3,'r1',1.6),1.3),camk(R(56.0,t0),focus(610,330,1.6),3.0),camk(R(62.04,t0),fz(3,'r2',1.6),1.2)])
t0,t1=67.28,72.10
scene(t0,t1,[photo(4,(1.12,1.02,0,0,0,0)),ov('shade-b'),
    chip('2차 애프터','calendar-check',140,760,0.3),chip('산책하다 손을 잡았어요','heart-handshake',460,760,R(69.0,t0),cls='gold')])
t0,t1=72.10,76.10
scene(t0,t1,[plate(3),crop(3,'r1',0,anim='none'),crop(3,'r2',0,anim='none'),crop(3,'r3',0,anim='none'),crop(3,'r4',0,anim='none')],
    cam=[focus(614,760,1.0),camk(0,focus(614,745,1.8),0.6)],xf=True)
t0,t1=76.10,82.26
scene(t0,t1,[photo(5,(1.03,1.13,0,0,0,-2)),ov('shade-b'),
    chip('프러포즈 · 승낙','gem',140,770,R(77.9,t0),cls='gold'),
    T('“정말 많이 데였던 분”',140,640,1200,R(79.8,t0),size=62,weight=600)])
t0,t1=82.26,88.34
scene(t0,t1,[
    T('멘트를 외운 게 아닙니다',0,330,1920,0.05,size=88,align='center',color='#9aa7c4'),
    strike(525,382,870,0.9,h=7),
    T('<span class="g">태도</span>가 바뀐 겁니다',0,470,1920,R(84.18,t0),size=120,align='center',anim='zoom'),
    T('아무것도 안 바뀌었다면, 이런 후기는 없었겠죠',0,680,1920,R(85.4,t0),size=44,align='center',weight=500,color='#c9d2e6'),
],bg=NAVY,cam=drift(t0,t1,1.05))
# ======================= S4
t0,t1=88.34,95.14
scene(t0,t1,[
    kick('THE PROGRAM',0,250,0.05,align='center',w=1920),
    T('이다사 부트캠프',0,300,1920,0.1,size=110,align='center',anim='blur',dur=.8),
    html('<div style="display:flex;gap:40px;justify-content:center"></div>',0,0,10,10,anim='none'),
    chip('500명+ 1:1 경험','users',560,520,R(89.8,t0)),
    chip('그대로 담은 방법','book-open',1000,520,R(92.4,t0)),
    T('<span class="g">1:1 훈련 과정</span>',0,660,1920,R(93.4,t0),size=76,align='center',anim='up'),
],bg=NAVY,cam=drift(t0,t1,1.04))
t0,t1=95.14,107.80
scene(t0,t1,[plate(4),crop(4,'t',0.05),crop(4,'a',0.2,anim='pop'),crop(4,'ar1',R(97.6,t0),anim='left'),crop(4,'b',R(98.1,t0),anim='pop',pulse=[R(100.2,t0)]),
    crop(4,'ar2',R(103.6,t0),anim='left'),crop(4,'c',R(104.0,t0),anim='pop',pulse=[R(105.8,t0)])],
    cam=[focus(960,520,1.15),camk(R(97.8,t0),focus(960,520,1.1),1.0),camk(R(103.6,t0),FULL,1.0)])
t0,t1=107.80,113.36
def pcard(i,x,label,sub,at,dark):
    bg='#14213f' if dark else '#fff'; col='#fff' if dark else '#1b2236'
    return html(f'''<div style="width:700px;height:560px;border-radius:26px;background:{bg};box-shadow:0 30px 70px rgba(20,33,63,.25);overflow:hidden">
<img src="img/i{i:02d}.jpg" style="width:700px;height:394px;object-fit:cover;{'filter:grayscale(.7) brightness(.9)' if not dark else ''}">
<div style="padding:26px 34px;color:{col}"><div style="font-size:42px;font-weight:700">{label}</div><div style="font-size:28px;opacity:.7;margin-top:6px">{sub}</div></div></div>''',x,170,700,560,at=at,anim='up')
scene(t0,t1,[pcard(11,190,'PDF + 영상 강의','받고, 보고, 끝',0.1,False),xstamp(800,120,110,0.8),
    pcard(10,1030,'직접 해보고 같이 고친다','이다사 부트캠프',R(110.66,t0),True),okstamp(1640,120,110,R(111.2,t0))],bg=LIGHT)
# ======================= S5
t0,t1=113.36,120.12
scene(t0,t1,[kick('500명을 만나며 알게 된 한 가지',0,280,0.1,align='center',w=1920),
    T('멘트를 더 외울 게 아니라',0,360,1920,R(116.12,t0),size=80,align='center',color='#c9d2e6'),
    T('<span class="g">태도</span>를 바꿔야 합니다',0,490,1920,R(118.2,t0),size=118,align='center',anim='zoom'),
],bg=NAVY,cam=drift(t0,t1,1.05))
t0,t1=120.12,127.22
fl=[('“주말에 뭐 하세요?”',300,190),('멘트 #27',1320,170),('“취미가 뭐예요?”',1180,330),('멘트 #64',230,420),('“MBTI가…”',1430,500),('멘트 #100',420,620),('“오늘 날씨…”',1250,700)]
items=[photo(6,(1.0,1.12,0,0,0,0)),ov('vig')]
for k,(tx,x,y) in enumerate(fl):
    items.append(html(f'<div class="chip" style="font-size:30px">{tx}</div>',x,y,None,None,at=0.2+k*0.25,anim='pop',out=dict(at=R(123.7,t0)+k*0.08,dur=.5),float=12))
items.append(T('긴장하면 <span class="g">다 사라집니다</span>',0,840,1920,R(124.0,t0),size=68,align='center'))
scene(t0,t1,items)
t0,t1=127.22,137.70
scene(t0,t1,[plate(5),crop(5,'t',0.05),crop(5,'a',0.15,anim='left'),crop(5,'lt',0.6,anim='pop'),crop(5,'b',R(128.74,t0),anim='right',pulse=[R(130.6,t0),R(134.8,t0)])],
    cam=[dict(s=1,x=0,y=0),camk(R(129.5,t0),fz(5,'b',1.3),1.2),camk(R(132.68,t0),FULL,1.2)])
# ======================= S6
t0,t1=137.70,142.54
scene(t0,t1,[photo(1,(1.02,1.12,0,0,2,0)),ov('shade-r'),
    chip("'이 멘트만 쓰면 된다'",'circle-play',1080,300,0.2),chip("'카톡은 이렇게 보내라'",'message-circle',1130,420,R(139.42,t0)),
    chip('연애 강의 · 영상 · 꿀팁','monitor-play',1100,540,R(140.6,t0),cls='gold')])
t0,t1=142.54,155.46
scene(t0,t1,[plate(6),crop(6,'t',0.05),crop(6,'a',0.15,anim='up'),crop(6,'b',R(146.1,t0),anim='up'),crop(6,'c',R(151.1,t0),anim='up')],
    cam=[dict(s=1,x=0,y=0),camk(0.6,fz(6,'a',1.45),1.0),camk(R(146.1,t0),fz(6,'b',1.45),1.0),camk(R(151.1,t0),fz(6,'c',1.45),1.0),camk(R(154.6,t0),FULL,0.8)])
t0,t1=155.46,162.10
scene(t0,t1,[photo(9,(1.12,1.02,0,0,0,0)),ov('shade-l'),
    kick('끝까지 남는 건 딱 하나',140,360,0.1),
    T('긴장한 순간에도<br><span class="g">무너지지 않는 내 태도</span>',140,420,1100,R(159.22,t0),size=88)])
# ======================= S7
t0,t1=162.10,166.84
scene(t0,t1,[plate(7),crop(7,'t',0.05),crop(7,'a',0.4,anim='left'),crop(7,'ar',R(164.0,t0),anim='pop'),crop(7,'b',R(164.4,t0),anim='right',pulse=[R(165.8,t0)])])
t0,t1=166.84,173.20
scene(t0,t1,[photo(7,(1.0,1.12,0,0,3,0)),ov('shade-r'),
    kick('HYENA',1080,250,0.05),T('상대 반응을<br>먹고 산다',1080,300,800,0.1,size=96),
    chip('상대가 웃으면 → 안심','smile',1080,600,R(168.86,t0)),
    chip('표정이 굳으면 → 불안','frown',1080,710,R(170.5,t0)),
    chip('점수 따려고 애쓴다','circle-alert',1080,820,R(172.0,t0),cls='navy')])
t0,t1=173.20,179.00
scene(t0,t1,[photo(8,(1.12,1.0,0,0,0,0)),ov('shade-l'),
    kick('LION',140,250,0.05),T('<span class="g">자기 기준</span>으로<br>움직인다',140,300,900,0.1,size=96),
    chip('흔들리지 않는다','anchor',140,600,R(175.56,t0)),chip('원하는 걸 말한다','message-square-heart',140,710,R(176.9,t0)),
    chip('먼저 제안한다','arrow-right',140,820,R(178.0,t0),cls='gold')])
t0,t1=179.00,184.66
judge=lambda x,sc,at: html(f'<div style="width:150px;height:110px;border-radius:16px;background:#fff;color:#14213f;font-size:56px;font-weight:800;display:flex;align-items:center;justify-content:center;box-shadow:0 14px 30px rgba(0,0,0,.35)">{sc}</div>',x,340,150,110,at=at,anim='down')
scene(t0,t1,[T('여자 앞에서 작아지는 이유',0,120,1920,0.05,size=62,align='center',weight=600,color='#c9d2e6'),
    chip('자신감 부족?','circle-alert',815,210,0.4),strike(815,244,290,R(181.3,t0)),
    bigicon('user',860,520,200,R(182.04,t0),bg='#24385f',color='#c9d2e6',ring=False),
    judge(560,'6.5',R(182.3,t0)),judge(885,'7.0',R(182.5,t0)),judge(1210,'5.5',R(182.7,t0)),
    T("만남을 <span class='g'>'심사받는 자리'</span>로 생각하기 때문",0,770,1920,R(182.6,t0),size=58,align='center')],bg=NAVY)
t0,t1=184.66,189.10
scene(t0,t1,[bigicon('magnet',860,220,200,0.1),xstamp(1010,210,80,0.6),
    T('점수 따려고 애쓰는 사람에게는',0,500,1920,0.3,size=60,align='center',weight=600,color='#c9d2e6'),
    T('<span class="g">아무도 끌리지 않습니다</span>',0,590,1920,R(186.6,t0),size=96,align='center',anim='zoom')],bg=NAVY,cam=drift(t0,t1,1.04))
# ======================= S8
t0,t1=189.10,193.20
items=[kick("THE LION'S 12",0,220,0.05,align='center',w=1920),
    html('<div style="font-size:260px;font-weight:800;color:#e2c27a;text-align:center;line-height:1"><span class="num">0</span></div>',0,270,1920,None,at=0.1,anim='zoom',count=[0,12,0,1.2]),
    T('사자의 태도 12가지',0,560,1920,0.4,size=78,align='center'),
    T('세 갈래로 익힙니다',0,680,1920,R(191.8,t0),size=52,align='center',weight=500,color='#c9d2e6')]
scene(t0,t1,items,bg=NAVY)
t0,t1=193.20,206.98
scene(t0,t1,[plate(8),crop(8,'t',0,anim='fade'),crop(8,'a',0.1,anim='up'),crop(8,'b',R(197.68,t0),anim='up'),crop(8,'c',R(202.58,t0),anim='up')],
    cam=[fz(8,'a',1.4),camk(R(197.4,t0),fz(8,'b',1.4),1.0),camk(R(202.3,t0),fz(8,'c',1.4),1.0),camk(R(205.8,t0),FULL,1.0)])
t0,t1=206.98,215.12
items=[T('하이에나의 태도를 걷어내고, <span class="g">사자의 태도</span>로',0,110,1920,0.05,size=60,align='center',weight=600)]
for k in range(12):
    cx=460+(k%6)*170; cy=290+(k//6)*190
    at=0.6+k*0.28
    items.append(html(f'<div class="circ" style="width:140px;height:140px;background:#2a3a5e;color:#9aa7c4"><i class="ic" data-ic="dog" style="width:50%;height:50%"></i></div>',cx,cy,140,140,at=0.1+k*0.03,anim='pop',out=dict(at=at,anim='shrink',dur=.25)))
    items.append(html(f'<div class="circ" style="width:140px;height:140px;background:linear-gradient(135deg,#e2c27a,#b8892f);color:#14213f;box-shadow:0 10px 30px rgba(201,162,74,.4)"><i class="ic" data-ic="crown" style="width:50%;height:50%"></i></div>',cx,cy,140,140,at=at+0.2,anim='pop'))
USED_ICONS.update(['dog','crown'])
items.append(T('부트캠프 안에서 하나씩 <span class="g">몸으로</span> 익힙니다',0,720,1920,R(211.8,t0),size=56,align='center',weight=600))
scene(t0,t1,items,bg=NAVY)
# ======================= S9
t0,t1=215.12,237.66
nt=[W('진단으로',216),W('1단계',219),W('2단계',220),W('3단계',221),W('4단계',222),W('5단계',224),W('6단계',228)]
its=[plate(9),crop(9,'t',0.05)]
for k in range(7): its.append(crop(9,f'n{k}',R(nt[k],t0),anim='pop',pulse=[]))
its+= [crop(9,'m1',R(231.3,t0),anim='wipe'),crop(9,'m2',R(233.74,t0),anim='wipe')]
its.append(html('<div class="ring" style="width:100%;height:100%"></div>',230,270,880,330,at=R(231.4,t0),anim='fade',out=dict(at=R(233.6,t0))))
its.append(html('<div class="ring" style="width:100%;height:100%"></div>',1050,270,690,330,at=R(233.8,t0),anim='fade'))
scene(t0,t1,its,cam=[focus(960,420,1.18),camk(R(230.8,t0),focus(960,470,1.1),1.2)])
# ======================= S10
t0,t1=237.66,243.60
scene(t0,t1,[photo(10,(1.03,1.15,0,0,0,-2)),ov('shade-b'),
    chip('1:1 태도 진단 · 90분','stethoscope',140,160,0.2,cls='gold'),
    html('<div style="display:flex;align-items:center;gap:14px;font-size:34px;font-weight:700;color:#fff"><span style="width:22px;height:22px;border-radius:50%;background:#e0524a;box-shadow:0 0 18px #e0524a"></span>REC</div>',1640,160,200,None,at=R(240.6,t0)),
    T('실제 상황처럼 대화해 보기',140,760,1400,R(240.56,t0),size=70)])
t0,t1=243.60,253.38
scene(t0,t1,[plate(10),crop(10,'t',0.05),crop(10,'a',0.1,anim='up'),crop(10,'b',0.4,anim='up'),crop(10,'c',R(248.62,t0),anim='pop',pulse=[R(250.5,t0)])],
    cam=[fz(10,'b',1.35),camk(R(248.3,t0),fz(10,'c',1.35),1.0),camk(R(252.2,t0),FULL,1.0)])
# ======================= S11
t0,t1=253.38,269.40
scene(t0,t1,[plate(11),crop(11,'t',0.05),crop(11,'s0',R(256.8,t0),anim='pop'),crop(11,'ar0',R(258.4,t0),anim='left'),crop(11,'s1',R(258.62,t0),anim='pop'),
    crop(11,'ar1',R(260.4,t0),anim='left'),crop(11,'s2',R(260.62,t0),anim='pop'),crop(11,'ar2',R(264.6,t0),anim='left'),crop(11,'s3',R(264.82,t0),anim='pop'),
    crop(11,'pill',R(266.74,t0),anim='up',pulse=[R(267.8,t0)])],
    cam=[focus(960,470,1.12),camk(R(256.6,t0),fz(11,'s0',1.3),1.0),camk(R(258.5,t0),fz(11,'s1',1.3),0.9),camk(R(260.5,t0),fz(11,'s2',1.3),0.9),
         camk(R(264.6,t0),fz(11,'s3',1.3),0.9),camk(R(266.5,t0),FULL,1.0)])
# ======================= S12
t0,t1=269.40,276.60
its=[plate(12),crop(12,'t',0.05)]
for k in range(6): its.append(crop(12,f'w{k}',0.4+k*0.35,anim='pop'))
its+=[crop(12,'c0',R(275.22,t0),anim='up'),crop(12,'v0',R(275.8,t0),anim='fade')]
scene(t0,t1,its,cam=[focus(960,420,1.15),camk(R(274.8,t0),FULL,1.0)])
t0,t1=276.60,280.68
scene(t0,t1,[photo(3,(1.18,1.3,-3,0,-5,-2)),ov('vig'),
    html('<div style="width:100%;height:100%;border:6px solid #c9a24a;border-radius:20px;box-shadow:0 0 40px rgba(201,162,74,.7)"></div>',1150,250,420,300,at=0.3,anim='pop'),
    chip('핀포인트 피드백','target',140,760,0.2,cls='gold'),chip('모조리 뜯어고친다','repeat',540,760,R(278.4,t0))])
t0,t1=280.68,288.40
its=[plate(12),crop(12,'t',0,anim='none')]+[crop(12,f'w{k}',0,anim='none') for k in range(6)]+[crop(12,'c0',0,anim='none'),crop(12,'v0',0,anim='none'),crop(12,'c1',0,anim='none'),crop(12,'v1',0,anim='none'),crop(12,'v2',R(283.3,t0),anim='fade'),
    crop(12,'c2',0.1,anim='up',pulse=[R(281.6,t0)]),crop(12,'c3',R(283.56,t0),anim='up',pulse=[R(285.3,t0)])]
scene(t0,t1,its,cam=[focus(1150,680,1.3),camk(R(283.3,t0),focus(1350,680,1.3),1.0),camk(R(286.5,t0),FULL,1.2)])
# ======================= S13
t0,t1=288.40,291.98
scene(t0,t1,[T("'좀 나아진 것 같다'",0,330,1920,0.05,size=96,align='center',color='#9aa7c4'),strike(640,395,640,1.3),
    T('<span class="g">느낌</span>으로 판단하지 않습니다',0,520,1920,1.6,size=80,align='center')],bg=NAVY)
t0,t1=291.98,303.34
scene(t0,t1,[plate(13),crop(13,'t',0.05),crop(13,'a',0.2,anim='pop'),crop(13,'b',R(294.38,t0)+0.7,anim='pop'),crop(13,'c',R(296.04,t0)+0.3,anim='pop',pulse=[R(300.5,t0)]),
    html('<div style="display:flex;align-items:center;gap:12px;font-size:28px;font-weight:700;color:#14213f"><span style="width:18px;height:18px;border-radius:50%;background:#e0524a"></span>같은 조건 촬영</div>',820,820,320,None,at=R(298.5,t0),anim='up')],
    cam=[fz(13,'a',1.5),camk(R(294.38,t0),FULL,1.2)])
# ======================= S14
t0,t1=303.34,309.76
mil=[('stethoscope','진단',0.3),('dumbbell','12주 훈련',1.6),('message-square-heart','실제 만남',3.2),('heart','연애 시작',4.6)]
its=[kick('START TO FINISH',0,180,0.05,align='center',w=1920),T('진단부터 연애가 시작될 때까지',0,230,1920,0.1,size=70,align='center'),
    html('<div style="width:100%;height:6px;border-radius:3px;background:linear-gradient(90deg,#7f93bd,#c9a24a)"></div>',360,563,1200,6,at=0.3,anim='wipe',dur=4.4)]
for k,(ic,lb,a) in enumerate(mil):
    x=360+k*400-80
    its.append(bigicon(ic,x,486,160,a,bg='#14213f' if k<3 else '#c9a24a',color='#e2c27a' if k<3 else '#14213f'))
    its.append(T(lb,x-70,680,300,a+0.15,size=40,align='center',weight=600))
its.append(T('<span class="g">처음부터 끝까지</span> 같이 갑니다',0,800,1920,R(307.0,t0),size=54,align='center',weight=600))
scene(t0,t1,its,bg=NAVY)
t0,t1=309.76,320.80
scene(t0,t1,[plate(14),crop(14,'t',0.05),crop(14,'a',R(312.3,t0),anim='up'),crop(14,'b',R(313.84,t0),anim='up'),crop(14,'c',R(315.36,t0),anim='up',pulse=[R(316.8,t0)])],
    cam=[focus(960,540,1.08),camk(R(318.14,t0),FULL,1.5)])
t0,t1=320.80,329.92
rays='<div style="width:1400px;height:1400px;border-radius:50%;background:radial-gradient(circle,rgba(201,162,74,.35) 0%,rgba(201,162,74,0) 60%)"></div>'
scene(t0,t1,[html(rays,260,-160,1400,1400,at=0,anim='fade',dur=1.5),
    kick('자신 있게 말씀드립니다',0,220,0.1,align='center',w=1920),
    T('내 영상을 <span class="g">장면 단위</span>로 보며<br>태도 자체를 고쳐주는 1:1 훈련',0,290,1920,R(323.06,t0),size=74,align='center'),
    bigicon('award',860,560,200,R(327.6,t0),bg='linear-gradient(135deg,#e2c27a,#b8892f)',color='#14213f'),
    T('<span class="g">국내 유일</span>',0,790,1920,R(327.82,t0),size=80,align='center',anim='zoom')],bg=NAVY,cam=drift(t0,t1,1.05))
# ======================= S15
t0,t1=329.92,337.10
scene(t0,t1,[photo(13,(1.02,1.12,0,0,0,0)),html('',0,0,1920,1080,anim='none',css='background:rgba(8,14,30,.45)'),ov('vig'),
    T('강의만 들어서 연애가 된다면?',0,300,1920,R(330.98,t0),size=80,align='center'),
    T('<span class="g">현실은 그렇지 않습니다</span>',0,460,1920,R(335.54,t0),size=96,align='center',anim='zoom')])
t0,t1=337.10,353.18
scene(t0,t1,[plate(15),crop(15,'t',0.05),crop(15,'a',0.2,anim='left'),crop(15,'ar',R(345.6,t0),anim='pop'),crop(15,'b',R(345.78,t0),anim='right',pulse=[R(349.5,t0)])],
    cam=[fz(15,'a',1.4),camk(R(345.5,t0),fz(15,'b',1.4),1.1),camk(R(351.8,t0),FULL,1.1)])
# ======================= S16
t0,t1=353.18,362.50
scene(t0,t1,[plate(16),crop(16,'t',0.05),crop(16,'a',R(355.72,t0),anim='wipe'),crop(16,'i0',R(357.66,t0),anim='up'),crop(16,'i1',R(W('매일',357),t0),anim='up'),
    crop(16,'i4',R(W('실전',358),t0),anim='up'),crop(16,'i5',R(W('코칭6회',360),t0),anim='up')],
    cam=[focus(960,420,1.1),camk(R(355.5,t0),focus(580,540,1.55),1.2)])
t0,t1=362.50,368.78
ch='''<svg width="1200" height="460" viewBox="0 0 1200 460">
<line x1="60" y1="400" x2="1180" y2="400" stroke="rgba(255,255,255,.35)" stroke-width="2"/><line x1="60" y1="20" x2="60" y2="400" stroke="rgba(255,255,255,.35)" stroke-width="2"/>
<text x="1180" y="440" fill="#9aa7c4" font-size="26" text-anchor="end" font-family="P">시간</text><text x="40" y="30" fill="#9aa7c4" font-size="26" text-anchor="end" font-family="P">변화</text>
<polyline fill="none" stroke="#7f8aa3" stroke-width="7" stroke-linecap="round" stroke-dasharray="2 16" points="60,330 250,290 420,300 600,350 800,385 1150,395"/>
<polyline fill="none" stroke="#c9a24a" stroke-width="9" stroke-linecap="round" points="60,330 250,280 450,220 650,160 850,105 1150,60"/></svg>'''
scene(t0,t1,[T('집중하는 기간이 없으면?',0,110,1920,0.05,size=66,align='center'),
    html(ch,360,250,1200,460,at=0.3,anim='wipe',dur=2.2),
    html('<div class="chip" style="font-size:28px">혼자 · 흐지부지</div>',1340,640,None,None,at=1.2,anim='pop'),
    html('<div class="chip gold" style="font-size:28px">12주 집중</div>',1360,250,None,None,at=R(365.86,t0),anim='pop'),
    T('12주 안에 <span class="g">확실히</span> 바꿉니다',0,780,1920,R(366.4,t0),size=56,align='center',weight=600)],bg=NAVY)
t0,t1=368.78,374.12
scene(t0,t1,[plate(16),crop(16,'t',0,anim='none'),crop(16,'a',0,anim='none')]+[crop(16,f'i{k}',0,anim='none') for k in (0,1,4,5)]+[crop(16,'b',0.1,anim='wipe',pulse=[R(371.6,t0)])],
    cam=[focus(1340,540,1.55),camk(R(372.6,t0),focus(1340,500,1.35),1.2)])
t0,t1=374.12,382.04
mm=[('sparkles','썸이 생겼을 때',374.12),('heart','연애를 시작했을 때',375.6),('zap','같은 문제로 다툴 때',376.7),('gem','결혼을 고민할 때',378.3)]
its=[T('진짜 연애는 <span class="g">12주 뒤</span>부터',0,120,1920,0.05,size=66,align='center'),
     html('<div style="width:100%;height:4px;background:rgba(255,255,255,.25)"></div>',300,438,1320,4,at=0.1,anim='wipe',dur=4)]
for k,(ic,lb,a) in enumerate(mm):
    x=300+k*440-70
    its.append(bigicon(ic,x,370,140,R(a,t0),bg='#24385f',ring=False))
    its.append(T(lb,x-90,540,320,R(a,t0)+0.1,size=36,align='center',weight=600))
    its.append(html(f'<div class="circ" style="width:64px;height:64px;background:#c9a24a;color:#14213f"><i class="ic" data-ic="refresh-cw" style="width:55%;height:55%"></i></div>',x+38,620,64,64,at=R(379.72,t0)+k*0.15,anim='pop'))
USED_ICONS.add('refresh-cw')
its.append(T('그때마다 돌아와서 <span class="g">점검</span>',0,760,1920,R(379.9,t0),size=56,align='center',weight=600))
scene(t0,t1,its,bg=NAVY)
t0,t1=382.04,395.28
scene(t0,t1,[plate(16)]+[crop(16,k,0,anim='none') for k in ('t','a','b','i0','i1','i4','i5')]+[crop(16,'i2',R(386.96,t0),anim='pop',pulse=[R(388.5,t0)]),crop(16,'i3',R(390.5,t0),anim='pop',pulse=[R(392.4,t0)]),
     ],
    cam=[focus(1340,600,1.5),camk(R(386.6,t0),fz(16,'i2',1.9),1.0),camk(R(390.3,t0),fz(16,'i3',1.9),1.0),camk(R(394.0,t0),focus(1340,600,1.4),1.0)])
t0,t1=395.28,401.16
scene(t0,t1,[photo(14,(1.02,1.12,0,0,0,0)),ov('shade-b'),chip('프러포즈 기획','gem',140,780,0.3,cls='gold'),chip('결혼 준비 가이드','clipboard-check',520,780,R(397.94,t0))])
t0,t1=401.16,404.88
scene(t0,t1,[plate(16)]+[crop(16,k,0,anim='none') for k in ('t','a','b','i0','i1','i2','i3','i4','i5')]+[crop(16,'i6',0.1,anim='pop'),crop(16,'i7',0.3,anim='pop'),
    html('<div style="font-size:40px;font-weight:700;color:#14213f;text-align:center">썸에서 결혼까지, <span style="color:#b8892f">갈림길마다 옆에</span></div>',0,830,1920,None,at=R(401.4,t0),anim='up')],
    cam=[focus(960,560,1.12),camk(0.2,FULL,3.0)])
# ======================= S17
t0,t1=404.88,420.64
perks=[('life-buoy','SOS 핫라인'),('book-open','새 강의 무료'),('gem','프러포즈 기획'),('clipboard-check','결혼 준비 가이드')]
its=[plate(17),crop(17,'t',0.05),crop(17,'a',R(407.18,t0),anim='pop'),crop(17,'b',R(409.2,t0),anim='pop',pulse=[R(410.6,t0)]),
     html('<div class="chip gold" style="font-size:32px">+ 약 30만 원</div>',1240,240,None,None,at=R(413.0,t0),anim='pop')]
for k,(ic,lb) in enumerate(perks):
    its.append(html(f'<div class="chip navy" style="font-size:28px;padding:12px 22px">{IC(ic)}<span>{lb}</span></div>',230+k*370,890,None,None,at=R(415.3,t0)+k*0.45,anim='up'))
scene(t0,t1,its,cam=[focus(960,500,1.08),camk(R(407.0,t0),fz(17,'a',1.4),1.0),camk(R(409.0,t0),fz(17,'b',1.4),1.0),camk(R(413.0,t0),FULL,1.0)])
t0,t1=420.64,424.96
scene(t0,t1,[chip('둘 다 VAT 별도','file-text',780,240,0.1),T("혹시 지금 <span class='g'>'좀 비싼데?'</span>",0,430,1920,R(422.32,t0),size=100,align='center',anim='zoom'),
    T('싶으셨나요?',0,580,1920,R(423.8,t0),size=60,align='center',weight=500,color='#c9d2e6')],bg=NAVY)
# ======================= S18
t0,t1=424.96,430.28
scene(t0,t1,[T('아뇨, <span class="g">전혀 비싸지 않습니다</span>',0,350,1920,0.05,size=96,align='center',anim='zoom'),
    T('1:1로 꾸준히 도움받는 건 원래 비쌉니다',0,540,1920,R(426.36,t0),size=54,align='center',weight=500,color='#c9d2e6')],bg=NAVY)
t0,t1=430.28,437.34
calc=lambda x,y,lab,num,unit,at,gold=False: html(f'<div style="text-align:center;color:#fff"><div style="font-size:30px;opacity:.8;font-weight:600">{lab}</div><div style="font-size:{96 if gold else 80}px;font-weight:800;color:{"#e2c27a" if gold else "#fff"}"><span class="num">0</span>{unit}</div></div>',x,y,420,None,at=at,anim='up',count=[0,num,0,1.0])
scene(t0,t1,[photo(15,(1.02,1.1,0,0,0,0)),html('',0,0,1920,1080,anim='none',css='background:rgba(10,18,38,.62)'),
    kick('심리상담 1년 (가정)',0,170,0.1,align='center',w=1920),
    calc(130,330,'1회',18,'만 원',0.2),T('×',540,360,100,R(433.14,t0),size=80,align='center'),
    calc(620,330,'한 달 4회',72,'만 원',R(433.14,t0)),T('×',1030,360,100,R(435.0,t0),size=80,align='center'),
    calc(1110,330,'12개월',864,'만 원',R(435.0,t0),gold=True),
    T('1년이면 <span class="g">800만 원</span>이 넘습니다',0,640,1920,R(435.6,t0),size=60,align='center',weight=600)])
t0,t1=437.34,443.88
scene(t0,t1,[plate(18),crop(18,'t',0.05),crop(18,'l1',0.1,anim='fade'),crop(18,'b1',0.2,anim='wipe'),crop(18,'v1',0.9,anim='fade'),
    crop(18,'l2',0.3,anim='fade'),crop(18,'b2',0.5,anim='wipe'),crop(18,'v2',1.0,anim='pop',pulse=[R(440.6,t0)]),
    chip('1년이 아니라 평생','infinity',720,760,R(441.48,t0),cls='gold')],cam=[focus(960,470,1.08),camk(2.5,FULL,1.2)])
# ======================= S19
t0,t1=443.88,452.38
scene(t0,t1,[plate(19),crop(19,'t',0.05),crop(19,'big',0.9,anim='zoom',dur=.8),crop(19,'pill',R(447.88,t0),anim='up',pulse=[R(449.8,t0)])],
    cam=[focus(960,500,1.12),camk(R(447.6,t0),FULL,1.2)])
t0,t1=452.38,460.10
scene(t0,t1,[photo(9,(1.02,1.12,0,0,-3,0)),ov('shade-l'),
    T('12주가 끝나도<br><span class="g">트레이너는 그대로</span>',140,240,1000,0.1,size=80),
    chip('썸이 생길 때','sparkles',140,560,R(455.58,t0)),chip('연애를 시작할 때','heart',140,670,R(456.7,t0)),chip('다시 흔들릴 때','zap',140,780,R(457.9,t0),cls='gold')])
t0,t1=460.10,464.90
scene(t0,t1,[photo(16,(1.12,1.02,0,0,0,0)),html('',0,0,1920,1080,anim='none',css='background:rgba(10,18,38,.45)'),
    html('<div class="dcard" style="padding:34px 46px;width:560px"><div style="font-size:30px;opacity:.8">소개팅 1번</div><div style="font-size:54px;font-weight:800;margin-top:6px">밥값 + 카페값</div></div>',220,380,560,None,at=0.2,anim='left'),
    T('vs',880,420,160,1.0,size=80,align='center',color='#e2c27a'),
    html('<div class="dcard" style="padding:34px 46px;width:620px;background:#c9a24a;color:#14213f"><div style="font-size:30px;opacity:.8">월 10만 원대</div><div style="font-size:54px;font-weight:800;margin-top:6px">평생 태도 트레이너</div></div>',1080,380,620,None,at=1.4,anim='right'),
    T('남는 장사입니다',0,680,1920,R(462.6,t0),size=64,align='center')])
t0,t1=464.90,470.56
scene(t0,t1,[bigicon('repeat',860,170,200,0.1,bg='#24385f',color='#9aa7c4',ring=False),
    T('혼자 같은 실수를 반복하며 버리는 <span class="g">시간과 돈</span>',0,430,1920,0.3,size=58,align='center',weight=600),
    bigicon('trending-up',860,560,180,R(467.9,t0)),
    T('오히려 <span class="g">돈을 버는 선택</span>',0,780,1920,R(468.2,t0),size=80,align='center',anim='zoom')],bg=NAVY)
# ======================= S20
t0,t1=470.56,474.24
scene(t0,t1,[T('솔직하게 말씀드릴게요',0,300,1920,0.05,size=60,align='center',weight=500,color='#c9d2e6'),
    bigicon('ban',880,420,160,R(472.24,t0),bg='#e0524a',color='#fff',ring=False),
    T('이런 분은 <span class="g">신청하지 마세요</span>',0,640,1920,R(472.4,t0),size=92,align='center',anim='zoom')],bg=NAVY)
t0,t1=474.24,488.00
scene(t0,t1,[plate(20),crop(20,'t',0,anim='fade'),crop(20,'a',0.1,anim='up'),crop(20,'b',R(477.96,t0),anim='up'),crop(20,'c',R(483.42,t0),anim='up')],
    cam=[fz(20,'a',1.45),camk(R(477.7,t0),fz(20,'b',1.45),1.0),camk(R(483.2,t0),fz(20,'c',1.45),1.0),camk(R(487.0,t0),FULL,1.0)])
t0,t1=488.00,494.52
scene(t0,t1,[photo(12,(1.02,1.12,0,0,0,0)),ov('shade-r'),
    T('진심으로 변하고 싶은 분이라면',1000,330,820,0.2,size=56,weight=600,align='right'),
    T('<span class="g">끝까지<br>같이 가겠습니다</span>',1000,450,820,R(493.12,t0),size=100,align='right',anim='zoom')])
# ======================= S21
t0,t1=494.52,498.24
scene(t0,t1,[photo(17,(1.02,1.12,0,0,0,0)),ov('shade-r'),
    T('해보고는 싶은데…',1000,340,820,0.2,size=74,align='right'),
    T('이런 <span class="g">걱정</span>이 드시나요?',1000,460,820,1.5,size=74,align='right')])
t0,t1=498.24,520.34
scene(t0,t1,[plate(21),crop(21,'t',0,anim='fade'),crop(21,'a',0.1,anim='up'),crop(21,'b',R(505.4,t0),anim='up'),crop(21,'c',R(509.12,t0),anim='up'),crop(21,'d',R(516.82,t0),anim='up')],
    cam=[fz(21,'a',1.55),camk(R(505.1,t0),fz(21,'b',1.55),1.0),camk(R(508.9,t0),fz(21,'c',1.55),1.0),camk(R(516.6,t0),fz(21,'d',1.55),1.0)])
t0,t1=520.34,530.04
scene(t0,t1,[bigicon('clipboard-check',560,260,200,0.1),T('→',860,300,200,0.6,size=100,align='center',color='#e2c27a'),bigicon('users',1160,260,200,0.8),
    T('과제',560,490,200,0.2,size=40,align='center',weight=600),T('1:1 코칭',1110,490,300,0.9,size=40,align='center',weight=600),
    T('과제를 해야 <span class="g">코칭이 진행</span>됩니다',0,610,1920,R(523.26,t0),size=64,align='center'),
    chip('어렵지 않아요 · 주 1~2시간','smile',700,760,R(526.18,t0),cls='gold')],bg=NAVY,cam=drift(t0,t1,1.04))
# ======================= S22
t0,t1=530.04,546.54
scene(t0,t1,[plate(22),crop(22,'t',0.05),crop(22,'a',0.2,anim='pop'),crop(22,'ar1',R(533.4,t0),anim='left'),crop(22,'b',R(533.58,t0),anim='pop'),
    crop(22,'ar2',R(536.7,t0),anim='left'),crop(22,'c',R(536.88,t0),anim='pop'),crop(22,'pill',R(542.58,t0),anim='up',pulse=[R(544.6,t0)])],
    cam=[fz(22,'a',1.5),camk(R(533.3,t0),fz(22,'b',1.5),1.0),camk(R(536.6,t0),fz(22,'c',1.5),1.0),camk(R(542.2,t0),FULL,1.0)])
t0,t1=546.54,551.16
scene(t0,t1,[photo(4,(1.02,1.12,0,0,2,0)),ov('shade-b'),
    T('부담 갖지 마시고,<br><span class="g">평소 모습 그대로</span> 오세요',140,600,1300,0.2,size=76)])
# ======================= S23
t0,t1=551.16,558.40
scene(t0,t1,[plate(23),crop(23,'s',0.1,anim='down'),crop(23,'t1',R(555.6,t0),anim='up'),crop(23,'t2',R(556.4,t0),anim='blur',dur=.8)],
    cam=[focus(960,300,1.25),camk(R(555.4,t0),focus(960,400,1.08),1.4)])
t0,t1=558.40,561.90
scene(t0,t1,[photo(12,(1.12,1.0,0,0,0,0)),ov('shade-b'),T('있는 그대로의 내 모습으로,<br><span class="g">다음 만남</span>을 잡으러 가시죠',0,620,1920,0.2,size=70,align='center')])
t0,t1=561.90,END
scene(t0,t1,[plate(23),crop(23,'s',0,anim='none'),crop(23,'t1',0,anim='none'),crop(23,'t2',0,anim='none'),crop(23,'cta',0.15,anim='pop',pulse=[1.4,2.6])],
    cam=[focus(960,520,1.12),camk(0.2,FULL,2.0)])
# ---------- write
subs=json.load(open(f'{S}/eng/subs.json'))
subs=[[a,b,re.sub(r'[.,]$','',t)] for a,b,t in subs]
spec=dict(duration=END,scenes=SC,subs=subs)
for k in range(len(SC)-1):
    assert abs(SC[k]['t1']-SC[k+1]['t0'])<1e-6,(k,SC[k]['t1'],SC[k+1]['t0'])
htmls=f'''<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="style.css"></head><body>
<div id="stage"></div><div id="sub"><span id="subt"></span></div>
<script src="gsap.min.js"></script><script>{icons_js()}</script><script>window.SPEC={json.dumps(spec,ensure_ascii=False)};</script><script src="runtime.js"></script></body></html>'''
open(f'{S}/eng/index.html','w').write(htmls)
print('scenes',len(SC),'dur',END)
json.dump([round(x['t0']+0.75*(x['t1']-x['t0']),2) for x in SC],open(f'{S}/w/mids.json','w'))
