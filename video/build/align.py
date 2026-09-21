import json, os, sys, time
from faster_whisper import WhisperModel
os.makedirs('words', exist_ok=True)
m = WhisperModel("small", device="cpu", compute_type="int8",
                 download_root="/opt/whisper-models", cpu_threads=8)
for i in range(int(sys.argv[1]) if len(sys.argv)>1 else 12):
    out = f'words/b{i:02d}.json'
    if os.path.exists(out): continue
    segs, _ = m.transcribe(f'../assets/audio/b{i:02d}.mp3', language="ko",
                           word_timestamps=True, vad_filter=False, beam_size=1)
    w = [{'w': x.word.strip(), 's': round(x.start,3), 'e': round(x.end,3)}
         for s in segs for x in (s.words or [])]
    json.dump(w, open(out,'w'), ensure_ascii=False)
    print(f'b{i:02d}: {len(w)} words', flush=True)
