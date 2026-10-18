import sys, json, subprocess, numpy as np
from faster_whisper import WhisperModel
m = WhisperModel("deepdml/faster-whisper-large-v3-turbo-ct2", device="cpu", compute_type="int8", cpu_threads=4)
raw=subprocess.run(["ffmpeg","-v","error","-i",sys.argv[1],"-ac","1","-ar","16000","-f","f32le","-"],capture_output=True).stdout
audio=np.frombuffer(raw,dtype=np.float32).copy()
segs, info = m.transcribe(audio, language="ko", word_timestamps=True, vad_filter=False, beam_size=5, condition_on_previous_text=False)
out=[]
for s in segs:
    out.append({"start":s.start,"end":s.end,"text":s.text,"words":[{"s":w.start,"e":w.end,"w":w.word} for w in s.words]})
    print(f"{s.start:7.2f} {s.end:7.2f} {s.text}", flush=True)
json.dump(out, open(sys.argv[2],"w"), ensure_ascii=False, indent=1)
