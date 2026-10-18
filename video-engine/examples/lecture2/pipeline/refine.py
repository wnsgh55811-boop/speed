import json,numpy as np,soundfile as sf
x,sr=sf.read('../drive/2강/2강 음성.wav',dtype='float32')
hop=int(sr*0.01)
rms=np.sqrt(np.convolve(x**2,np.ones(hop)/hop,'same')[::hop])
db=20*np.log10(rms+1e-9)
ch=json.load(open('chunks_raw.json'))
def quiet_run(a,b,thr):
    i0,i1=max(0,int(a*100)),min(len(db),int(b*100))
    seg=db[i0:i1]<thr
    best=(0,None,None);k=0
    while k<len(seg):
        if seg[k]:
            j=k
            while j<len(seg) and seg[j]: j+=1
            if j-k>best[0]: best=(j-k,(i0+k)/100,(i0+j)/100)
            k=j
        else: k+=1
    return best
# boundary between chunk i-1 and i
for i in range(1,len(ch)):
    p,c=ch[i-1],ch[i]
    a=min(p['e2'],c['s2'])-0.30; b=max(p['e2'],c['s2'])+0.30
    for thr in (-45,-40,-35,-30):
        n,qs,qe=quiet_run(a,b,thr)
        if n>=5: break
    c['gap']=(qs,qe,thr) if n>=5 else None
    if n>=5:
        p['e3']=qs; c['s3']=qe
    else:
        m=(p['e2']+c['s2'])/2; p['e3']=m; c['s3']=m
ch[0]['s3']=0.0; ch[-1]['e3']=min(len(x)/sr, ch[-1]['e2']+0.3)
bad=[(i,c['text'],c['gap']) for i,c in enumerate(ch[1:],1) if c['sent_start'] and (c['gap'] is None or c['gap'][2]>-40)]
print('sentence starts without clear pause:',len(bad))
for b in bad: print(' ',b)
json.dump(ch,open('chunks.json','w'),ensure_ascii=False,indent=0)
