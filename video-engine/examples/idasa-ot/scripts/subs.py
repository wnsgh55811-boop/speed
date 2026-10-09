import json,re,sys
S='/tmp/claude-0/-home-user-speed/0d948206-c1a3-547f-9fa6-f85521be224c/scratchpad'
asr=json.load(open(f'{S}/w/asr.json'))
R=[('소비팅','소개팅'),('여자번호','여자 번호'),('1대1 태도진단','1:1 태도 진단'),('1대1','1:1'),('1대2','1:1'),('이 다섯 부트캠프는','이다사 부트캠프는'),('많이 되었던','많이 데였던'),('진단해서','진단에서'),
('상대방에','상대 반응에'),('자가제는','작아지는'),('따르고','따려고'),('몸에 뺀','몸에 밴'),('하이엔아이','하이에나의'),('코칭해서','코칭에서'),('한 두 시간','1~2시간'),('들이니까','드리니까'),
('다넘코','단언코'),('한 라인','핫라인'),('프로포즈','프러포즈'),('12주 차의','12주 차에'),('TOP3','TOP 3'),('뜯어 고칩니다','뜯어고칩니다'),('알 거 같은데','알 것 같은데'),('흐지부지 돼요','흐지부지돼요'),
('태도로 바꾸는 겁니다','태도를 바꾸는 겁니다'),('카페 값','카페값'),('4가지를','네 가지를'),('4번이면','네 번이면'),('앞에 4단계에서','앞의 네 단계에서'),('뒤에 2단계에서','뒤의 두 단계에서'),
('만원','만 원'),('말을 못하는','말을 못 하는'),('남아있습니다','남아 있습니다'),('만나왔습니다','만나 왔습니다'),('피드백해드렸습니다','피드백해 드렸습니다'),('해봅니다','해 봅니다'),('가르쳐드립니다','가르쳐 드립니다'),('안내해드립니다','안내해 드립니다'),
('저는 원래 말주변이 없는데요? 괜찮습니다','"저는 원래 말주변이 없는데요." 괜찮습니다.'),('나이가 좀 많은데 될까요?','"나이가 좀 많은데 될까요?"'),('연애 경험이 거의 없어요','"연애 경험이 거의 없어요."'),
('시간이 별로 없어요.','"시간이 별로 없어요."'),('좀 비싼데 싶으셨나요','\'좀 비싼데?\' 싶으셨나요'),('심사받는 자리로','\'심사받는 자리\'로'),('좀 나아진 것 같다는','\'좀 나아진 것 같다\'는'),
('이 멘트만 쓰면 된다',"'이 멘트만 쓰면 된다'"),('카톡은 이렇게 보내라',"'카톡은 이렇게 보내라'"),('한방에 먹히는 멘트만',"'한 방에 먹히는 멘트'만"),('6주 차','6주차'),('12주 차','12주차'),
('SOS 핫라인, 새 강의','SOS 핫라인, 새 강의'),('보장을 받고','보장받고'),('2주씩 6단계로','2주씩 여섯 단계로')]
def fix(t):
    t=t.strip()
    for a,b in R: t=t.replace(a,b)
    return t
MAX=27
OV=[
['소개팅 대화 주제, 여자 번호 따는 법','이런 거 검색해보신 적 있으시죠?'],
['많은 분들을 만나면서','확실하게 알게 된 게 하나 있습니다'],
['연애가 어려울수록 멘트를 더 외울 게 아니라','태도를 바꿔야 한다는 거예요'],
['멘트 100개를 외워도','마음에 드는 사람 앞에서 긴장하는 순간'],
['그래서 멘트 100개 외우는 것보다','태도 하나를 익히는 게'],
['맞춰주기만 하지 않고','관계를 같이 만들어가는 거고요.'],
['뒤의 두 단계에서','그걸 실제 만남과 연애에 적용해보는 거죠.'],
['그리고 같은 장면을','사자의 태도로 다시 해보는 거죠'],
['세 영상을 나란히 놓고 보면','내 태도가 어떻게 바뀌었는지','내 눈으로 바로 보입니다.'],
['정리하면 이다사 부트캠프는','진단부터 실제 연애가 시작될 때까지','처음부터 끝까지 같이 가는 과정입니다.'],
['내가 원하는 걸 말하고','대화로 호감을 쌓을 수 있게 되고'],
['대부분의 연애 강의는','영상을 보거나 단체로 듣고 끝납니다'],
['저에게 바로 피드백 받을 수 있는','1:1 SOS 핫라인,'],
['결혼 준비하면서','부딪히는 문제까지 가르쳐 드립니다.'],
['프러포즈 기획, 결혼 준비 가이드까지','평생 이어지는 거예요'],
['심리 상담만 해도','보통 한 번에 18만 원 정도 합니다'],
['쉽게 말하면 월 10만 원대로','평생 같이 갈 태도 트레이너를 두는 거예요.'],
['상담 한 번 비용보다 적은 돈으로','내 태도를 봐주고 고쳐주는 사람이 생기는 겁니다.'],
['혼자서 같은 실수를 반복하면서','버리는 시간과 돈을 생각하면','오히려 돈을 버는 쪽에 가깝습니다.'],
['2주에 과제 하나도 해볼 생각이 없는 분,','이건 듣기만 하는 강의가 아니라','직접 해보는 훈련입니다.'],
['특정 여성을 무조건 꼬실 수 있다는','보장받고 싶은 분,','저는 지킬 수 있는 것만 약속합니다.'],
['반대로 나를 진심으로 표현하고','정말 행복한 연애를 하고 싶어서','변하고 싶은 분이라면'],
['지금 만나는 사람이 없어도','모든 과제를 할 수 있게 만들어 뒀습니다'],
['1:1 태도 진단을 받으시면','내가 어디서 흔들리는지 직접 확인하고'],
['진단이 끝나고','제가 확실히 도와드릴 수 있겠다 싶고'],
['지금까지 이다사에서 연애에 성공하신 분들','모두 이 진단에서 시작하셨습니다.'],
['강의 제일 많이 들은 사람이','연애도 제일 잘해야겠죠'],
]
OVD={' '.join(x):x for x in OV}
def tat(seg,frac):
    words=seg['words'];tot=sum(len(w[2].strip()) for w in words); acc=0
    for w0,w1,w in words:
        acc+=len(w.strip())
        if acc/tot>=frac-1e-6: return w1
    return seg['end']
def split(seg):
    t=fix(seg['text'])
    if t in OVD:
        parts=OVD[t]; out=[]; pos=0; st=seg['start']
        for k,pp in enumerate(parts):
            pos+=len(pp)+(1 if k else 0)
            en=seg['end'] if k==len(parts)-1 else tat(seg,pos/len(t))
            out.append((st,en,pp)); st=en
        return out
    return split0(seg)
def split0(seg):
    t=fix(seg['text']); words=seg['words']
    if len(t)<=MAX: return [(seg['start'],seg['end'],t)]
    # candidate split points at spaces; prefer after comma
    best=None
    for m in re.finditer(r' ',t):
        i=m.start(); l,r=t[:i],t[i+1:]
        if len(l)>MAX+4 and len(r)>MAX+4: continue
        score=abs(len(l)-len(r))-(8 if l.endswith(',') else 0)
        if best is None or score<best[0]: best=(score,i)
    i=best[1]; frac=i/len(t)
    # time by asr char fraction
    tot=sum(len(w[2].strip()) for w in words); acc=0; ts=seg['end']
    for w0,w1,w in words:
        acc+=len(w.strip())
        if acc/tot>=frac: ts=w1; break
    a=dict(start=seg['start'],end=ts,text=t[:i],words=[w for w in words if w[1]<=ts+1e-3])
    b=dict(start=ts,end=seg['end'],text=t[i+1:],words=[w for w in words if w[1]>ts+1e-3])
    if not b['words']: b['words']=[[ts,seg['end'],t[i+1:]]]
    if not a['words']: a['words']=[[seg['start'],ts,t[:i]]]
    return split_raw(a)+split_raw(b)
def split_raw(seg):
    # seg text already fixed
    t=seg['text']
    if len(t)<=MAX: return [(seg['start'],seg['end'],t)]
    s2=dict(seg); 
    global fix
    f=fix; fix=lambda x:x.strip()
    r=split(s2); fix=f; return r
out=[];segi=[]
for si,s in enumerate(asr):
    r=split(s); out+=r; segi+=[si]*len(r)
# extend end to next start if gap small
res=[]
for k,(a,b,t) in enumerate(out):
    nxt=out[k+1][0] if k+1<len(out) else b+0.6
    e=nxt if nxt-b<0.7 else b+0.35
    res.append([round(a,3),round(e,3),t,segi[k]])
json.dump(res,open(f'{S}/eng/subs.json','w'),ensure_ascii=False)
for r in res: print(f'{r[0]:7.2f} {r[1]:7.2f} {len(r[2]):2d} {r[2]}')
