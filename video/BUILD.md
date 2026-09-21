# 소개팅 첫 1분 — 16:9 explainer (HyperFrames)

1920×1080 / 30fps / 9.81분. 다크 차콜 + 필름 그레인, 나레이션 + 한 줄 자막.

## 파이프라인

```
cd build
python3 fetch_assets.py        # 나레이션 106개 (audio_ledger.json 의 URL)
python3 fetch_images.py        # 이미지 12개 (image_ledger.json)
python3 measure_audio.py       # 실제 mp3 길이 → durations.json
                               # + silencedetect 로 문장 경계 → cue_bounds.json
python3 gen.py                 # index.html 생성 (실측 타이밍)
python3 build_sfx.py           # 효과음 3종 합성
python3 build_master_audio.py  # 사운드트랙 전체를 master.mp3 하나로 미리 완성
HF_NO_AUDIO=1 python3 gen.py   # 렌더용: 오디오 없는 컴포지션
cd .. && npx hyperframes render --quality delivery --workers 4 -o out/video.mp4
ffmpeg -i out/video.mp4 -i assets/audio/master.mp3 -c:v copy -c:a aac \
       -map 0:v:0 -map 1:a:0 -shortest -movflags +faststart out/final.mp4
```

자막 문구를 바꾸면 `node measure.cjs` 로 폭을 다시 재야 한 줄 보장이 유지된다.

## 설계상 정해둔 것

- **자막 한 줄**: 빌드 시점에 Chromium 에서 실제 Pretendard 로 폭을 재서 미리 분할한다
  (`measure.cjs` → `sub_widths.json`). 233개 전부 1560px 예산 안, 최대 1558px.
  순백 + 얇은 검정 획(`paint-order: stroke fill`), `white-space: nowrap` 고정.
- **자막 싱크**: 여러 문장이 든 씬은 `silencedetect` 가 찾은 실제 묵음 위치로 끊는다.
  검출된 묵음 개수가 문장 수와 안 맞을 때만 음절 가중 비례 분할로 폴백.
- **그래프**: 길이만 그리지 않는다. 등급 점 5개, 눈금, 축 라벨(적음/많음)을 같이 그려서
  "얼마나"가 읽히게 한다. 막대·미터·게이지는 전부 block+flex — `<i>` 인라인은 width 가
  안 먹어서 통째로 안 그려진다.
- **오디오는 렌더 전에 완성**: 컴포지션이 참조하는 오디오가 없으면 렌더가 바로 실패한다.
  `build_master_audio.py` 가 나레이션을 각 큐 시각에 얹고 효과음을 섞어 master.mp3 를
  만든 뒤, 인코더 꼬리 패딩을 잘라 컴포지션 길이와 정확히 맞춘다.
- **렌더는 비디오만**: 114개 오디오 엘리먼트를 넣으면 워커마다 디코드하다 브라우저가
  떨어진다. 그림만 렌더하고 완성된 master.mp3 를 ffmpeg 로 먹싱한다.

## 에셋

- 나레이션: Higgsfield Seed Audio 1.0, voice `내-목소리-v4`
  (element / `c02aabbb-e76a-4b36-98a4-28e2fdd5e8d2`), `speech_rate=18`(≈1.2배),
  mp3 / 24kHz / pitch 0 / loudness 0. 후처리에서 배속을 다시 걸지 않는다.
  ※ "표현 강도"는 Seed Audio API 에 없는 파라미터라 적용하지 못함.
- 이미지 12장: 흑백 인물 4 / 씬 사진 4 / 3D 아이콘 4. 인물·아이콘 8장은 누끼 처리.
  같은 이미지는 전체에서 최대 2회까지만 사용.
- job id 는 두 ledger 에 기록되어 있어 재생성 없이 복구된다.
