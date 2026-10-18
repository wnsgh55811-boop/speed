import json,sys,subprocess,numpy as np
from faster_whisper import WhisperModel
m=WhisperModel(sys.argv[3] if len(sys.argv)>3 else "small",device="cpu",compute_type="int8",cpu_threads=4)
segs,info=m.transcribe(np.frombuffer(subprocess.run(['ffmpeg','-v','error','-i',sys.argv[1],'-ac','1','-ar','16000','-f','s16le','-'],capture_output=True).stdout,np.int16).astype(np.float32)/32768,language="ko",word_timestamps=True,beam_size=5,vad_filter=False,condition_on_previous_text=True)
out=[]
for s in segs:
    out.append({"s":s.start,"e":s.end,"t":s.text,"w":[[w.start,w.end,w.word,w.probability] for w in s.words]})
    print(f"{s.start:.2f}-{s.end:.2f} {s.text}",flush=True)
json.dump(out,open(sys.argv[2],"w"),ensure_ascii=False)
