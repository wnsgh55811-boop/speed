import json,sys,re,torch,torchaudio,numpy as np,uroman
sys.path.insert(0,sys.argv[1]); from chunks import SLIDES
W=sys.argv[2]
SPOKEN={"VOD":"브이오디","VOD를":"브이오디를","VOD는":"브이오디는","12주":"십이주","12주는":"십이주는","12주차에":"십이주차에","12가지라고":"열두가지라고",
 "2주씩":"이주씩","6단계로":"육단계로","1단계에서":"일단계에서","2단계부터":"이단계부터","4단계까지":"사단계까지","5단계에서":"오단계에서",
 "6단계에서는":"육단계에서는","1:1로":"일대일로","2분짜리":"이분짜리","6주차와":"육주차와","1강에서":"일강에서","12주":"십이주"}
words=[]  # (chunk_idx, spoken)
ci=0
for k in sorted(SLIDES):
    for p in SLIDES[k]:
        for c in p:
            for w in c.split():
                w2=re.sub(r"[\"'“”‘’.,]","",w)
                sp=SPOKEN.get(w2,w2)
                assert not re.search(r"[0-9A-Za-z]",sp),w
                words.append((ci,sp))
            ci+=1
ur=uroman.Uroman()
bundle=torchaudio.pipelines.MMS_FA
model=bundle.get_model(with_star=False); dic=bundle.get_dict(star=None)
rom=[re.sub(r"[^a-z]","",ur.romanize_string(sp).lower()) for _,sp in words]
assert all(rom)
tokens=[dic[ch] for r in rom for ch in r]
wav=torch.from_numpy(np.fromfile(f"{W}/v16.f32",dtype=np.float32))[None]
with torch.inference_mode():
    em=[]
    step=16000*30
    for i in range(0,wav.shape[1],step):
        e,_=model(wav[:,i:i+step]); em.append(e)
    emission=torch.cat(em,1)
ratio=wav.shape[1]/emission.shape[1]/16000
al,sc=torchaudio.functional.forced_align(emission,torch.tensor([tokens],dtype=torch.int32),blank=0)
spans=torchaudio.functional.merge_tokens(al[0],sc[0].exp())
out=[];k=0
for (c,sp),r in zip(words,rom):
    s=spans[k:k+len(r)]; k+=len(r)
    out.append({"chunk":c,"word":sp,"t0":s[0].start*ratio,"t1":s[-1].end*ratio,"score":float(np.mean([x.score for x in s]))})
json.dump(out,open(f"{W}/fa_words.json","w"),ensure_ascii=False,indent=0)
for w in out: print(f"{w['t0']:7.2f} {w['t1']:7.2f} {w['score']:.2f} {w['chunk']:3d} {w['word']}")
