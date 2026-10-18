# 이다사 VOD 2강 — PPT + FishAudio 강의 영상

- `이다사_VOD_2강.mp4` — 완성본 (1920×1080, 30fps, H.264 CRF 12, AAC 320k 48kHz, 11:25)
- `timeline.md` — 슬라이드별 시작/종료, FishAudio·영상 사용 여부
- `2강_자막.srt` — 번인된 자막과 동일한 타이밍의 SRT
- `subs.txt` — 최종 스크립트를 의미 단위(25자 이내)로 끊은 자막 원본. `/` 가 줄 구분
- `chunks.json`, `render_plan.json` — 자막 조각별 음성 정렬 결과와 프레임 단위 렌더 계획

## 파이프라인 (`pipeline/`)

1. PPT → PDF(LibreOffice, 맑은 고딕 → Noto Sans KR 대체) → 슬라이드 PNG
2. `parse.py` 스크립트 → 슬라이드별 문장, `checksubs.py` 자막 조각이 원문과 글자 단위로 같은지·25자 이내인지 검사
3. `asr.py` (faster-whisper medium) 단어 타임스탬프 → `timeline.py` 글자 단위 정렬 → `refine.py` 무음 구간으로 경계 보정
4. `render_prep.py` 슬라이드+자막 합성(Noto Sans KR Medium 54px, 검정 60% 박스 y=971~1048) → `encode.py` 프레임 직접 파이프 인코딩
5. `fullqa.py` 전 프레임을 계획과 대조
