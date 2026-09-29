import numpy as np, json, wave, sys
SR=44100; rng=np.random.default_rng(3)
def env(n,a=.005,d=.2):
    t=np.arange(n)/SR; return np.minimum(1,t/a)*np.exp(-t/d)
def noise(n): return rng.standard_normal(n)
def lp(x,k):  # simple one-pole lowpass, k in (0,1)
    y=np.zeros_like(x); acc=0
    for i,v in enumerate(x): acc+=k*(v-acc); y[i]=acc
    return y
def sweep(f0,f1,dur):
    n=int(SR*dur); f=np.linspace(f0,f1,n); return np.sin(2*np.pi*np.cumsum(f)/SR)
def S(type):
    if type=='whoosh':
        n=int(SR*.38); x=noise(n); k=np.linspace(.02,.25,n)
        y=np.zeros(n); acc=0
        for i in range(n): acc+=k[i]*(x[i]-acc); y[i]=acc
        e=np.sin(np.linspace(0,np.pi,n))**2; return y*e*1.6
    if type=='pop':
        return sweep(500,1100,.07)*env(int(SR*.07),.002,.025)*.8
    if type=='send':
        return sweep(700,1300,.06)*env(int(SR*.06),.002,.02)*.6
    if type=='click':
        n=int(SR*.03); return noise(n)*env(n,.0005,.006)*.8
    if type=='tick':
        n=int(SR*.08); return (np.sin(2*np.pi*1900*np.arange(n)/SR)*env(n,.001,.018)+noise(n)*env(n,.0005,.004)*.3)*.7
    if type=='stamp':
        n=int(SR*.22); t=np.arange(n)/SR
        return (np.sin(2*np.pi*(110-60*t)*t)*env(n,.002,.07)*1.1 + lp(noise(n),.3)*env(n,.001,.03)*.9)
    if type=='thud':
        n=int(SR*.4); t=np.arange(n)/SR
        return np.sin(2*np.pi*(80-40*t)*t)*env(n,.003,.12)*1.3 + lp(noise(n),.15)*env(n,.001,.05)
    if type=='hit':
        n=int(SR*.6); t=np.arange(n)/SR
        return np.sin(2*np.pi*(70-30*t)*t)*env(n,.002,.18)*1.2 + lp(noise(n),.4)*env(n,.001,.06)*.8 + S('whoosh')[:n].__array__().resize(n) if False else np.sin(2*np.pi*(70-30*t)*t)*env(n,.002,.18)*1.2 + lp(noise(n),.4)*env(n,.001,.06)*.8
    if type=='crunch':
        n=int(SR*.5); y=np.zeros(n)
        for k,st in enumerate([0,.16,.32]):
            m=int(SR*.09); i=int(SR*st); b=lp(noise(m),.5)*env(m,.001,.025)*(1-.15*k); y[i:i+m]+=b[:max(0,min(m,n-i))]
        return y*1.2
    if type=='buzz':
        n=int(SR*.35); t=np.arange(n)/SR; g=((t%.18)<.12).astype(float)
        return np.sign(np.sin(2*np.pi*150*t))*lp(g,.05)*.12 + np.sin(2*np.pi*150*t)*g*.25
    if type=='ding':
        n=int(SR*.7); t=np.arange(n)/SR
        return (np.sin(2*np.pi*1318.5*t)*env(n,.002,.25)+.6*np.sin(2*np.pi*1760*t)*np.where(t>.09,env(n,.002,.3)[np.maximum(0,(np.arange(n)-int(.09*SR)))],0))*.45
    if type=='freeze':
        n=int(SR*.5); t=np.arange(n)/SR; f=np.maximum(40,220*(1-t*1.9))
        return np.sin(2*np.pi*np.cumsum(f)/SR)*env(n,.002,.3)*.7 + noise(n)*env(n,.0005,.01)*.6
    if type=='chime':
        n=int(SR*1.4); t=np.arange(n)/SR; y=np.zeros(n)
        for f,d,a in [(784,0,.5),(988,.06,.4),(1175,.12,.35),(1568,.18,.2)]:
            i=int(d*SR); m=n-i; tt=np.arange(m)/SR; y[i:]+=a*np.sin(2*np.pi*f*tt)*np.minimum(1,tt/.004)*np.exp(-tt/.45)
        return y*.6
    raise ValueError(type)
cues=json.load(open('sfx.json')); dur=float(sys.argv[1])
# keep SFX sparse: only hook, reversals, message arrivals, key reveals
DROP={2.20,10.32,11.64,12.08,15.16,16.04,22.00,28.64,29.28,29.72,32.08,37.44,43.68,46.68,49.88,50.12,52.16,54.56,64.36,67.26}
cues=[c for c in cues if round(c['t'],2) not in DROP]
out=np.zeros(int(SR*(dur+2)))
for c in cues:
    x=S(c['type'])*c['vol']; i=int(c['t']*SR); out[i:i+len(x)]+=x[:len(out)-i]
out*=0.22  # SFX sit well under the voice
print('peak',np.abs(out).max(), 'n',len(cues))
out=np.clip(out,-1,1)[:int(SR*dur)]
w=wave.open('sfx.wav','wb'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((out*32767).astype(np.int16).tobytes()); w.close()
