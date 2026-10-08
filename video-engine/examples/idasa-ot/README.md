# 이다사 12주 부트캠프 OT 영상

PPT PNG 23장 + OT 나레이션(9:25)으로 만든 1920×1080 / 30fps / H.264 + AAC 영상의 소스.
HyperFrames 대신 자체 경량 렌더러(HTML + GSAP 타임라인 → Playwright 프레임 캡처 → ffmpeg)를 썼다.

## 파이프라인

```
narr.wav ──asr.py (faster-whisper medium, 단어 타임스탬프)──> asr.json
script.txt + asr.json ──align.py──> sents.json        (대본 문장별 시작/끝)
asr.json ──subs.py──> engine/subs.json                 (실제 발화 기준 자막, 한 줄 27자 이하, 의미 단위 분할)
slides/*.png ──crops.py (regions.py 영역)──> 빈 배경 plate + 요소별 크롭  (순차 등장 애니메이션용)
plan.py ──> engine/index.html                          (71개 씬: 슬라이드 빌드·카메라 포커스·실사 컷어웨이·인포그래픽)
render.py ×4 병렬 ──> seg_*.mp4 ──concat + AAC 320k──> 최종 MP4
```

- 자막: 하단 고정, 흰 글씨 + 검정 60% 배경, 한 줄.
- 나레이션이 대본과 다른 구간(예: 가격 파트, 과제-코칭 조건 문장)은 **음성 기준**으로 자막 처리.
- 실사 이미지 18장은 Higgsfield (GPT Image 2.5, 2K) 생성 — 용량 때문에 레포에는 미포함.
- 화면 전환: 0.2초 디졸브.
