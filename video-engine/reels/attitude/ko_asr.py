import sherpa_onnx, wave, numpy as np, json
d="sherpa-onnx-zipformer-korean-2024-06-24/"
rec = sherpa_onnx.OfflineRecognizer.from_transducer(
    encoder=d+"encoder-epoch-99-avg-1.onnx", decoder=d+"decoder-epoch-99-avg-1.onnx",
    joiner=d+"joiner-epoch-99-avg-1.onnx", tokens=d+"tokens.txt", num_threads=4, decoding_method="greedy_search")
w=wave.open("a16.wav"); sr=w.getframerate(); x=np.frombuffer(w.readframes(w.getnframes()),dtype=np.int16).astype(np.float32)/32768
out=[]
# chunk into 12s windows with 1s overlap
step=10.0; win=12.0; t=0.0
while t < len(x)/sr:
    s=rec.create_stream(); seg=x[int(t*sr):int((t+win)*sr)]
    s.accept_waveform(sr, seg); rec.decode_stream(s)
    r=s.result
    for tok,ts in zip(r.tokens, r.timestamps):
        out.append([round(t+ts,3), tok, t])
    print(f"[{t:.0f}] {r.text}", flush=True)
    t+=step
json.dump(out, open("tokens.json","w"), ensure_ascii=False)
