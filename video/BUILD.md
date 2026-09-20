# 소개팅 첫 1분 — 16:9 explainer (HyperFrames)

## 상태 (2026-09-20)
- 대본 → 106 scenes / 233 cues (원본 대본과 1:1 검증 완료)
- 자막: 빌드 시점 Pretendard 실측 → 전부 1줄 보장 (초과 0건, 최대 1558px / 1560px)
- 컴포지션: `index.html` (build/gen.py 로 생성) — `npx hyperframes check` 통과 (0 error / 0 info)
- 나레이션 106개 전부 생성 완료 → audio_ledger.json
- 이미지 12개 생성 완료 (인물 4 / 사진 4 / 3D 아이콘 4), 인물·아이콘 8개 누끼 완료 → image_ledger.json
- 실제 프레임 캡처로 눈으로 확인한 항목:
  ① 자막 1줄 유지 (전 구간 초과 0건, 최대 1558px / 1560px)
  ② 누끼 + 종이 찢은 테두리 + 가로·세로 중앙 정렬
  ③ 막대그래프가 실제로 그려짐 (채움 + 등급 점 + 눈금 + 축 라벨)
- 나레이션: Higgsfield Seed Audio 1.0, voice `내-목소리-v4`
  (element / c02aabbb-e76a-4b36-98a4-28e2fdd5e8d2), speech_rate=18 (≈1.2x),
  mp3 / 24kHz / pitch 0 / loudness 0

## 남은 작업 (Higgsfield CDN 허용 필요)
이 세션의 네트워크 정책이 아래 호스트를 막고 있어서 에셋을 내려받지 못함:
  cdn.higgsfield.ai, d8j0ntlcm91z4.cloudfront.net,
  d2ol7oe51mr4n9.cloudfront.net, d1xarpci4ikg0w.cloudfront.net

허용되면:
  1) `python3 build/fetch_assets.py`   # ledger 의 URL 로 mp3 전부 다운로드
  2) `python3 build/measure_audio.py`  # 실제 길이 → durations.json (+문장 경계 silencedetect)
  3) `cd build && python3 gen.py`      # 실측 길이로 타이밍 재생성
  4) `npx hyperframes check && npx hyperframes render --quality delivery -o out/final.mp4`

## 재생성
```
cd build && python3 gen.py        # index.html 재생성
node measure.cjs                  # 자막 폭 재측정 (문구 바뀌면 필수)
```
