import sys, subprocess, numpy as np
from faster_whisper import WhisperModel
m = WhisperModel(sys.argv[1], device="cpu", compute_type="int8", cpu_threads=4)
for rng in sys.argv[3:]:
    a,b=map(float,rng.split('-'))
    raw=subprocess.run(["ffmpeg","-v","error","-ss",str(a),"-t",str(b-a),"-i",sys.argv[2],"-ac","1","-ar","16000","-f","f32le","-"],capture_output=True).stdout
    audio=np.frombuffer(raw,dtype=np.float32).copy()
    segs,_=m.transcribe(audio,language="ko",beam_size=5,word_timestamps=True)
    print(rng, ' | '.join(f"{w.word}@{a+w.start:.2f}-{a+w.end:.2f}" for s in segs for w in s.words), flush=True)
