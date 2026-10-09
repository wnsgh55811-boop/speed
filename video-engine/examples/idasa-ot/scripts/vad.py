import numpy as np,subprocess,json,sys
S='/tmp/claude-0/-home-user-speed/0d948206-c1a3-547f-9fa6-f85521be224c/scratchpad'
a=np.frombuffer(subprocess.run(['ffmpeg','-v','error','-i',f'{S}/w/narr.wav','-f','f32le','-ac','1','-ar','16000','-'],capture_output=True).stdout,np.float32)
hop=160 # 10ms
n=len(a)//hop
e=np.sqrt((a[:n*hop].reshape(n,hop)**2).mean(1)+1e-12)
db=20*np.log10(e)
floor=np.percentile(db,10); peak=np.percentile(db,95)
th=floor+0.25*(peak-floor)
sp=db>th
print('floor',floor,'peak',peak,'th',th)
# gaps (silence runs >= 80ms)
gaps=[];i=0
while i<n:
    if not sp[i]:
        j=i
        while j<n and not sp[j]: j+=1
        if j-i>=8: gaps.append((i/100,j/100))
        i=j
    else: i+=1
json.dump(gaps,open(f'{S}/w/gaps.json','w'))
asr=json.load(open(f'{S}/w/asr.json'))
# for each asr seg start, nearest gap end (speech onset)
offs=[]
for s in asr[:200]:
    st=s['start']
    ons=[g[1] for g in gaps]
    k=min(ons,key=lambda o:abs(o-st))
    offs.append(k-st)
offs=np.array(offs)
print('onset - asr start: mean %.3f med %.3f  p10 %.3f p90 %.3f'%(offs.mean(),np.median(offs),np.percentile(offs,10),np.percentile(offs,90)))
print(len(gaps),'gaps; first 30:',[(round(a,2),round(b,2)) for a,b in gaps[:30]])
print([round(s['start'],2) for s in asr[:15]])
