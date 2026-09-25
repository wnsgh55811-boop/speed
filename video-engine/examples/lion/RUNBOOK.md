# 하이에나 vs 사자 — 남은 단계

화면 쪽 작업은 끝났다: 씬 78개, 자막 171개, 에셋 키잉·밝기 보정, 프레임 QA 1차.
나레이션이 없어서 멈춰 있다 (Higgsfield 잔액 0.77 크레딧).

## 1. 나레이션 (크레딧 약 7~9 필요)

`chunks.json` 의 3건을 그대로 생성 (문장 끝에서 자른 1100~1300자 테이크).

- 모델: `text2speech_v2`, variant `elevenlabs`
- 보이스: `내-목소리-v4` (element `c02aabbb-e76a-4b36-98a4-28e2fdd5e8d2`)
- 속도 파라미터 없음 → 1.2×는 `mkaudio_v2.py` 에서 **한 번만** (`plan.SPEED`)

## 2. 정렬 → 타이밍 커밋

```
sandbox_job.sh voice <branch> lion "<mp3 url 3개, 콤마>"
```
로그의 `===TIMINGS===` / `===SPANS===` 를 `timings.txt` / `spans.json` 으로 저장·커밋.
그 뒤 로컬에서 `emit_v2.py` → 스냅샷으로 자막 싱크·클립 길이(≤5초 경고) 재확인.

## 3. 세그먼트 렌더 (샌드박스 작업 수명 ~15분)

길이를 약 85초씩 나눠 `seg` 잡을 따로 돌린다. 경계는 정수 초로.
```
sandbox_job.sh seg <branch> lion 0 85 <PUT url>
sandbox_job.sh seg <branch> lion 85 170 <PUT url>   ...
```

## 4. 최종

```
sandbox_job.sh final <branch> lion "<mp3 3개>" "<세그먼트 url들>" <PUT master> <PUT light>
```
오디오 합치기 + pause 삽입 + SFX 믹스(−14.5 LUFS / −1.5 dBTP) → 세그먼트 concat →
MASTER (원본 품질) / LIGHT (~96MB, faststart H.264).
