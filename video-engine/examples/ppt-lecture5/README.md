# PPT 강의 VOD — 5강 (사람을 만나는 환경 설계)

PPT 슬라이드 + FishAudio 나레이션 + 하단 고정 자막 → 1920×1080 30fps H.264 MP4.

| 단계 | 파일 | 내용 |
|---|---|---|
| 1 | `lo_export.py` | LibreOffice UNO로 PPTX → PDF. 한글·영문 사이 자동 띄어쓰기(ParaIsCharacterDistance) 끔. `맑은 고딕`은 fontconfig로 Noto Sans KR 대체 |
| 2 | `asr.py` | faster-whisper(large-v3-turbo) 단어 타임스탬프 |
| 3 | `parse.py` | 최종 스크립트 → 슬라이드별 문장 |
| 4 | `chunks.txt` | 수작업 자막 분할(의미 단위, 25자 이내). `+`=녹음에만 있는 단어, `!`=녹음에 없는 문장, `[PAUSE]`=스크립트의 쉼 |
| 5 | `validate.py` | 자막 합치면 스크립트 원문과 글자 단위로 같은지, 25자 이내인지 검사 |
| 6 | `align.py` | 스크립트↔ASR 글자 정렬 후 오디오 무음 구간으로 경계 보정 |
| 7 | `build.py` | 타임라인(슬라이드 전환=문장 끝 무음), 자막 프레임 합성, ffmpeg concat 리스트 |

렌더:
```
ffmpeg -f concat -safe 0 -i concat.txt -i audio_final.wav -vf fps=30,format=yuv420p \
  -c:v libx264 -preset slow -crf 14 -tune stillimage -c:a aac -b:a 320k -ar 48000 -ac 2 -movflags +faststart out.mp4
```
