import json,sys
from faster_whisper import WhisperModel
m=WhisperModel(sys.argv[2],device="cpu",compute_type="int8")
import soundfile as sf
aud,_=sf.read(sys.argv[1],dtype="float32")
segs,info=m.transcribe(aud,language="ko",word_timestamps=True,beam_size=5,vad_filter=False,condition_on_previous_text=False)
out=[]
for s in segs:
    out.append({"start":s.start,"end":s.end,"text":s.text,"words":[[w.start,w.end,w.word] for w in s.words]})
    print(f"{s.start:7.2f} {s.end:7.2f} {s.text}",flush=True)
json.dump(out,open(sys.argv[3],"w"),ensure_ascii=False)
