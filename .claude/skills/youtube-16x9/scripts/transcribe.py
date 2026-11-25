"""Word timestamps with faster-whisper.
usage: $REELKIT_HOME/venv/bin/python -I transcribe.py <audio> <words.json> [script.txt] [model]
The script text (first ~800 chars) is passed as initial_prompt so names/terms are recognised.
Only the TIMING is used later; subtitle text always comes from the script."""
import sys, json, subprocess, tempfile, wave, re
import numpy as np
from faster_whisper import WhisperModel

src, out = sys.argv[1], sys.argv[2]
prompt = None
if len(sys.argv) > 3 and sys.argv[3]:
    txt = open(sys.argv[3], encoding="utf-8").read()
    txt = re.sub(r"^#.*$", "", txt, flags=re.M).replace("**", "")
    prompt = " ".join(txt.split())[:800]
model = sys.argv[4] if len(sys.argv) > 4 else "large-v3-turbo"

tmp = tempfile.mktemp(suffix=".wav")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-ac", "1", "-ar", "16000", "-c:a", "pcm_s16le", tmp], check=True)
w = wave.open(tmp)
a = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768  # numpy input avoids a PyAV bug
segs, _ = WhisperModel(model, device="cpu", compute_type="int8").transcribe(
    a, language="ko", word_timestamps=True, beam_size=5, initial_prompt=prompt)
words = []
for s in segs:
    print(f"[{s.start:7.2f}-{s.end:7.2f}] {s.text}")
    words += [[round(x.start, 2), round(x.end, 2), x.word.strip()] for x in s.words]
json.dump(words, open(out, "w"), ensure_ascii=False)
