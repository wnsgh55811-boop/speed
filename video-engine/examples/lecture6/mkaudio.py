import wave, numpy as np, json
S='./'
w=wave.open(S+'dl2/6강 최종 음성.wav'); sr=w.getframerate(); x=np.frombuffer(w.readframes(w.getnframes()),dtype=np.int16)
tl=json.load(open(S+'work2/timeline.json'))
z=np.zeros(int(2.0*sr),dtype=np.int16); parts=[]; prev=0
for p in [int(round(i['at']*sr)) for i in tl['inserts']]: parts+=[x[prev:p],z]; prev=p
parts.append(x[prev:]); y=np.concatenate(parts)
o=wave.open(S+'build2/narration.wav','wb'); o.setnchannels(1); o.setsampwidth(2); o.setframerate(sr); o.writeframes(y.tobytes()); o.close()
print(len(y)/sr, tl['total'])
