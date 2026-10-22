# 6강 「분리의 태도」 VOD (PPT + FishAudio)

PPT를 넘기며 말하는 강의 영상 파이프라인. 결과 영상(mp4)은 용량 때문에 레포에 넣지 않는다.

1. `fixexport.py` — LibreOffice로 PPTX→PDF (한글·문장부호 사이 자동 간격 끔, 표 셀 포함). 맑은 고딕 → Noto Sans CJK KR 대체
2. `pdftoppm -scale-to-x 1920 -scale-to-y 1080` — 슬라이드 PNG
3. `parse.py` → `apply_ov.py`(`chunk.py` + `overrides.txt`) — 대본을 25자 이내 의미 단위 자막으로 분할
4. `asr.py` (faster-whisper turbo, 단어 타임스탬프) → `align.py` (대본 글자↔음성 글자 정렬) → `timing.py` (무음 구간)
5. `build.py` — 슬라이드 전환(문장 사이 무음 중간), [멈춤]/[2초 쉼]에 2초 정지 삽입, 자막 프레임 합성
6. `render.py` — 프레임 단위 raw 파이프 → H.264 CRF10 / AAC 320k
7. `qa2.py` — 전 프레임을 계획된 슬라이드+자막 이미지와 대조

결과: `timeline.md`, `6강_자막.srt`

## v2 (6강 최종 음성)
- 음성을 `6강 최종 음성.wav`로 교체해 재정렬·재렌더 (`mkaudio.py`로 [멈춤]/[2초 쉼] 2초 삽입)
- `slide17_fixed.xml`: 요일 라벨을 막대마다 개별 텍스트상자(가운데 정렬)로 분리
- `slide18_fixed.xml`: '‘나’'를 한 런으로 합쳐 공백 없이 중앙 정렬
- 대본 오타 '있씁니다' → 자막에서 '있습니다'
