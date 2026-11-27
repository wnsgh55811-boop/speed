"""음성 → 단어 타임스탬프 (faster-whisper large-v3-turbo). usage: transcribe.py audio script.txt out.json"""
import sys, json, re
from faster_whisper import WhisperModel
audio, script, out = sys.argv[1:4]
txt = open(script, encoding='utf-8').read()
body = ' '.join(l for l in txt.splitlines() if not l.startswith('##'))
prompt = re.sub(r'\*\*', '', body)[:200]
m = WhisperModel('large-v3-turbo', device='cpu', compute_type='int8', cpu_threads=4)
import subprocess, numpy as np
pcm = subprocess.run(['ffmpeg','-v','error','-i',audio,'-f','f32le','-ac','1','-ar','16000','-'],capture_output=True).stdout
arr = np.frombuffer(pcm, np.float32)
segs, info = m.transcribe(arr, language='ko', word_timestamps=True, beam_size=5,
                          initial_prompt=prompt, vad_filter=False)
words = []
for s in segs:
    for w in s.words:
        words.append({'w': w.word, 's': round(w.start, 3), 'e': round(w.end, 3)})
    print(f'{s.start:7.2f} {s.text}', flush=True)
json.dump(words, open(out, 'w'), ensure_ascii=False)
print('DONE', len(words))
