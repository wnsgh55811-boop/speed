import sys, json
from faster_whisper import WhisperModel
model_name, wav, out = sys.argv[1], sys.argv[2], sys.argv[3]
m = WhisperModel(model_name, device="cpu", compute_type="int8")
import wave, numpy as np
w_=wave.open(wav); audio=np.frombuffer(w_.readframes(w_.getnframes()),dtype=np.int16).astype(np.float32)/32768
segs, info = m.transcribe(audio, language="ko", word_timestamps=True, vad_filter=False, beam_size=5, condition_on_previous_text=False)
res=[]
for s in segs:
    res.append({"start":s.start,"end":s.end,"text":s.text,"words":[{"s":w.start,"e":w.end,"w":w.word} for w in s.words]})
    print(f"{s.start:8.2f} {s.end:8.2f} {s.text}", flush=True)
json.dump(res, open(out,"w"), ensure_ascii=False)
