import json,sys
from faster_whisper import WhisperModel
m=WhisperModel(sys.argv[3] if len(sys.argv)>3 else "medium",device="cpu",compute_type="int8",cpu_threads=4)
import subprocess,numpy as np
aud=np.frombuffer(subprocess.run(["ffmpeg","-v","error","-i",sys.argv[1],"-f","f32le","-ac","1","-ar","16000","-"],capture_output=True).stdout,np.float32)
segs,info=m.transcribe(aud,language="ko",word_timestamps=True,beam_size=5,vad_filter=False,condition_on_previous_text=False)
out=[]
for s in segs:
    out.append({"start":s.start,"end":s.end,"text":s.text,"words":[[w.start,w.end,w.word] for w in s.words]})
    print(f"{s.start:7.2f} {s.end:7.2f} {s.text}",flush=True)
json.dump(out,open(sys.argv[2],"w"),ensure_ascii=False)
