# light — 밝은 미니멀 인포그래픽 영상 파이프라인

규칙은 `SPEC.md`. 영상 하나 = `epN/` 폴더 하나.

```
epN/script.txt     ## n | 챕터 제목  + 문단 (한 줄 = 한 문단, **강조**)
epN/audio/voice.mp3
epN/plan.py        장면 계획 (앵커 문구 → 컴포넌트, c.t('문구') = 등장 시점)
```

```bash
python3 tools/transcribe.py epN/audio/voice.mp3 epN/script.txt epN/words.json   # faster-whisper
python3 tools/build.py epN                                                     # 타임라인 + build/index.html
node tools/render.cjs epN/build snap /tmp/snap 12.3 45.6                       # 시점 확인
node tools/render.cjs epN/build frames epN/frames 30 4                         # 전체 프레임 (같은 상태는 하드링크)
ffmpeg -framerate 30 -i epN/frames/%06d.jpg -i epN/audio/voice.mp3 -map 0:v -map 1:a \
  -c:v libx264 -crf 20 -pix_fmt yuv420p -c:a aac -b:a 192k -shortest -movflags +faststart out.mp4
```

폰트: `fonts/GothicA1-{Medium,Bold,Black}.ttf` (Google Fonts, 커밋 안 함).
