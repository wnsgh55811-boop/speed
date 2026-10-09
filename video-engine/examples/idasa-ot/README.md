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

## v2 (수정본)

- 자막 싱크: faster-whisper 단어 타임스탬프 → **MMS 강제 정렬**(torchaudio `MMS_FA` + uroman, 섹션 단위 무음 절단)로 교체 (`fa.py` → `fa_raw.json`).
  자막 시작이 실제 발화 시작과 ±0.04초 이내 (VAD 대조, `vad.py`).
- 카메라 줌 인/아웃 전면 제거. 강조는 해당 요소 살짝 띄우기 + 나머지 흐리게.
- 실사 이미지 → 둥근 플랫 일러스트 (Higgsfield GPT Image 2.5, 첫 장을 레퍼런스로 그림체·캐릭터 통일). 투명 스티커 5종.
- 코칭 장면은 실제 줌 코칭 캡처를 화상회의 창 목업에 넣어 사용.
- 취소선은 텍스트 폭에 맞춰 그려지는 인라인 요소(`.st/.stl`).
- 글자 단위 등장 모션, 챕터 태그, 배경 오브·그레인.
- 장면 플랜: `scripts/plan2.py` (모든 연출 타이밍을 정렬된 단어 시간으로 지정).
