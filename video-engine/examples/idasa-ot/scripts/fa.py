import json,re,torch,torchaudio,subprocess,numpy as np,uroman as ur
S='/tmp/claude-0/-home-user-speed/0d948206-c1a3-547f-9fa6-f85521be224c/scratchpad'
subs=json.load(open(f'{S}/eng/subs.json')); asr=json.load(open(f'{S}/w/asr.json'))
U=ur.Uroman()
SP=[('1:1','일대일'),('1~2시간','한두 시간'),('500명','오백명'),('12가지','열두 가지'),('3가지','세 가지'),('4가지','네 가지'),('TOP 3','탑 쓰리'),('VOD','브이오디'),('PDF','피디에프'),('SOS','에스오에스'),('VAT','브이에이티'),
('6번','여섯 번'),('4번','네 번'),('100개','백 개'),('6분의 1','육분의 일')]
DIG='영일이삼사오육칠팔구'
def sino(n):
    n=int(n)
    if n==0: return '영'
    out=''
    for unit,name in ((10000,'만'),(1000,'천'),(100,'백'),(10,'십')):
        q=n//unit
        if q: out+=('' if q==1 and unit!=10000 else sino(q) if unit==10000 else DIG[q])+name; n%=unit
    if n: out+=DIG[n]
    return out
def spoken(t):
    for a,b in SP: t=t.replace(a,b)
    t=re.sub(r'\d+',lambda m:sino(m.group()),t)
    return t
def words_of(t,src=None):
    ws=[];hs=[]
    for orig in t.split():
        sp=spoken(orig)
        for w in re.findall(r'[가-힣A-Za-z]+',sp):
            r=''.join(c for c in U.romanize_string(w).lower() if c in DICT)
            if r: ws.append(r); hs.append(orig)
    if src is not None: src.extend(hs)
    return ws
bundle=torchaudio.pipelines.MMS_FA
DICT=bundle.get_dict()
model=bundle.get_model(with_star=False); model.eval()
tok=bundle.get_tokenizer(); aligner=bundle.get_aligner()
a=np.frombuffer(subprocess.run(['ffmpeg','-v','error','-i',f'{S}/w/narr.wav','-f','f32le','-ac','1','-ar','16000','-'],capture_output=True).stdout,np.float32).copy()
SR=16000; TOT=len(a)/SR
gaps=json.load(open(f'{S}/w/gaps.json'))
SEC=[0,26.52,48.46,88.34,113.36,137.70,162.10,189.10,215.12,237.66,253.38,269.40,288.40,303.34,329.92,353.18,404.88,424.96,443.88,470.56,494.52,530.04,551.16]
def cut(t):
    if t<=0: return 0.0
    g=min(gaps,key=lambda g:0 if g[0]<=t<=g[1] else min(abs(g[0]-t),abs(g[1]-t)))
    return (g[0]+g[1])/2
B=[cut(t) for t in SEC]+[TOT]
newt={};WORDS={}
for n in range(len(SEC)):
    w0,w1=B[n],B[n+1]
    ks=[k for k,s in enumerate(subs) if w0-0.3<=s[0]<w1-0.3 and (n==len(SEC)-1 or s[0]<SEC[n+1]-0.05)]
    ks=[k for k in ks if SEC[n]-0.05<=subs[k][0]]
    allw=[];own=[];hs=[]
    for k in ks:
        ws=words_of(subs[k][2],hs); own.append((len(allw),len(allw)+len(ws))); allw+=ws
    wav=torch.from_numpy(a[int(w0*SR):int(w1*SR)])[None]
    with torch.inference_mode():
        em,_=model(wav)
        sp=aligner(em[0],tok(allw))
    ratio=wav.shape[1]/em.shape[1]/SR
    for k,(i0,i1) in zip(ks,own):
        st=w0+sp[i0][0].start*ratio; en=w0+sp[i1-1][-1].end*ratio
        newt[k]=(round(st,3),round(en,3))
        wl=[]
        for j in range(i0,i1):
            ws_,we_=w0+sp[j][0].start*ratio,w0+sp[j][-1].end*ratio
            if wl and wl[-1][0]==hs[j]: wl[-1][2]=round(we_,3)
            else: wl.append([hs[j],round(ws_,3),round(we_,3)])
        WORDS[k]=wl
    print(n,round(w0,2),round(w1,2),len(ks),flush=True)
print('aligned',len(newt),'of',len(subs))
out=[]
for k,s in enumerate(subs):
    st,en=newt.get(k,(s[0],s[1]))
    out.append([st,en,s[2],WORDS.get(k,[])])
json.dump(out,open(f'{S}/w/fa_raw.json','w'),ensure_ascii=False)
d=[abs(out[k][0]-subs[k][0]) for k in range(len(subs))]
print('mean |shift| %.3f max %.3f'%(np.mean(d),np.max(d)))
for k in np.argsort(d)[-15:]: print(round(subs[k][0],2),'->',out[k][0],subs[k][2])
