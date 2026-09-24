# video-engine

한국어 나레이션 설명 영상을 만드는 HyperFrames 엔진. "공백의 태도" (10:02, 251씬)
제작 과정에서 나온 코드를 다음 영상에 그대로 쓰려고 정리해 둔 것.

## 새 영상 만들 때

영상 하나당 새 채팅 하나. 대화가 길어지면 이전 프로젝트 기록이 매 턴 딸려가서
비싸지고, 이전 씬 플랜이 새 영상에 잘못 섞일 수도 있다.

새 채팅에서:

```
speed 레포의 video-engine/ 을 써서 영상 만들어줘.
PROMPT.md 규칙 그대로 따르고, 대본만 새 걸로 갈아끼워.
```

그리고 `PROMPT.md` 내용 + 레퍼런스 영상 + 대본을 붙여넣으면 된다.

## 구성

| 경로 | 내용 |
|---|---|
| `PROMPT.md` | 붙여넣기용 제작 프롬프트. 스타일·절대 규칙·전달 방식 |
| `src/emit.py` | 씬 빌더. 도식 40여 종, 픽토그램 24종, GSAP 모션 |
| `src/style.css` | 디자인 시스템. 배경 8종, 자막, 말풍선, 그래프, 누끼 |
| `src/build.py` | 자막 실측 분할, 에셋 라운드로빈 |
| `src/mkpreview.py` | 컴포지션 → 브라우저 프리뷰 빌더 |
| `scripts/paper.py` | 누끼 + 손으로 찢은 종이 테두리 처리 |
| `scripts/mkaudio.py` | 나레이션 조각 이어붙이기 → master.wav |
| `scripts/render.sh` | 샌드박스 1회성 렌더 (오디오 → 렌더 → 업로드) |
| `examples/idasa/` | "공백의 태도" 씬 플랜·대본·타이밍 (참고용) |

`src/` 는 프로젝트 무관하게 재사용, `examples/` 는 이번 영상 전용이다.
새 영상은 `examples/` 를 복사해서 `plan.py` 와 `chunks.json` 만 새로 쓴다.

## 파이프라인

```
대본 → 문장 분할 (chunks.json)
     → 힉스필드 TTS → 조각 오디오 → mkaudio.py → master.wav
     → 문장별 타이밍 (timings.txt)
     → 씬 플랜 (plan.py: 씬 종류 + 에셋)
     → emit.py → index.html (HyperFrames 컴포지션)
     → hyperframes check (린트 · 레이아웃 · 모션 · 대비)
     → hyperframes snapshot (프레임 눈으로 확인)
     → render.sh → MP4
```

## 씬 종류 (`plan.py`)

| 코드 | 내용 | arg |
|---|---|---|
| `B` | 사진 b-roll | 에셋 키 |
| `C` | 인물 누끼 합성 | `"cutout[+cutout]@bg"` |
| `N` | 선화 도식 | 도식 키 |
| `P` | 픽토그램 + 큰 문장 | `"마크명"` 또는 `"마크명\|문구"` |
| `I` | 3D 아이콘 | `"아이콘키\|뱃지"` |
| `T` | 키네틱 타이포 | 문구 (빈 값이면 대본 줄 사용) |
| `K` | 인용 말풍선 | `m` 남자 / `w` 여자 / `n` 내담자, 끝에 `x` = 취소선 |
| `H` | 챕터 헤더 | `"번호\|키워드"` |
| `G` | 인포그래픽 | 그래픽 id |

`T`·`H`·`P` 는 문장이 화면 중앙에 크게 뜨므로 하단 자막을 내보내지 않는다.

## 이번에 잡은 버그 (다시 밟지 말 것)

- **막대그래프가 안 그려짐** — `.bar-fill` 이 `<i>` 라 인라인이었고,
  인라인 요소에는 `width`/`height` 가 안 먹는다. `display:block` 필요.
- **인물이 바닥에 붙고 잘림** — 세로 중앙을 `transform` 으로 잡았는데
  GSAP 가 같은 요소에 `yPercent` 를 물려서 덮어썼다. 정렬은 박스 레이아웃으로.
- **인물이 검은 사각형으로 보임** — 생성된 스틸이 알파 없는 RGB 였다.
  합성 전에 `paper.py` 로 키잉 필요.
- **사진이 안 보임** — `brightness(.40)` + 블러 + 진한 틴트, 어둡게 하는 처리가
  세 겹이었다. 하나만 걸 것.
- **에셋이 한 장만 반복됨** — `i % len(pool)` 이 회전처럼 보였지만 씬 인덱스가
  거의 같은 합동류라 한 변형만 뽑혔다. 별도 카운터로 라운드로빈.
- **나레이션 재생성 시 자막이 밀림** — 다시 합치면 1초쯤 짧아진다.
  `atempo` 로 원래 길이에 맞출 것 (0.2%, 안 들림).
- **렌더가 통째로 날아감** — 샌드박스는 호출 사이에 회수된다.
  렌더 도중 자리를 비우지 말 것.
- **오디오 누락으로 렌더 즉시 실패** — 컴포지션이 참조하는 오디오 파일은
  렌더 시작 전에 존재해야 한다. 병렬로 만들면 늦는다.


## 2세대: span 컴포저 (`src/compose.py`) — "하이에나와 사자"

짧은 호흡의 대본(492줄)은 한 줄 = 한 씬이면 너무 잘게 끊긴다. 그래서 씬 하나가
여러 줄에 걸치고, 씬 **안의 요소가 각자 자기 대사 줄에 맞춰** 등장한다
(말풍선은 그 말을 할 때, 막대는 그 단어가 나올 때, 토큰은 "넘겨준다"는 순간 이동).

```
대본(script.txt) → chunks.json (≈1,600자 × 5, 문장 끝에서 자름)
  → Higgsfield TTS (ElevenLabs, 내-목소리-v4) — 이미 빠른 템포라 1.2× 후처리 없음
  → scripts/align.py (샌드박스): 이어붙이기 · -14 LUFS · faster-whisper 줄 타이밍
  → timings.txt
  → plan.py (씬 = (시작 줄, 종류, 인자))  →  src/compose.py  →  build/index.html
  → scripts/snap.mjs 로 로컬 프레임 QA (CDN 이미지는 라벨 자리표시자로)
  → compose.py --seg a b  로 구간 분할 → scripts/render_seg.sh (샌드박스 렌더)
  → scripts/assemble.py : 구간 연결 + 나레이션 + 효과음 + 마스터링 + MASTER/LIGHT
```

씬 종류: `hook photo video typo chat quotes rows icon chapter cmp graph_reverse
graph_effort scale tokens iceberg timer share invest steps center eq cycle roots
flip check cta` — 모든 씬에 `nocap=[줄]`(중앙 타이포와 같은 말이면 자막 제거),
`head=(줄, 문구)`(도식이 시작되기 전 빈 화면을 막는 상단 제목)을 줄 수 있다.

### 이번에 잡은 버그 (다시 밟지 말 것)

- **사진·영상이 통째로 안 보임** — Ken Burns 래퍼 `.kb` 에 크기가 없었다. GSAP 가
  transform 을 거는 순간 높이 0 박스가 absolute 이미지의 기준이 된다.
  `.kb{position:absolute;inset:0}` 필수.
- **샌드박스 백그라운드 렌더가 5초 만에 취소** — `render_cancelled_parent_exited`.
  부모 프로세스 감시 때문. `HYPERFRAMES_RENDER_DETACHED=1` 로 실행.
- **영상 클립 프레임 멈춤 경고** — concat `-c copy` 로 만든 부메랑은 키프레임이 6.8초
  간격. `-g 30` 으로 재인코딩.
- **샌드박스 → 로컬로 파일을 못 가져옴** — 이 컨테이너는 Higgsfield CDN 이 막혀 있다.
  로컬 QA 는 자리표시자로, 이미지 밝기 QA 는 샌드박스에서 프레임 통계로 한다.
- **Whisper 타임스탬프가 균일 간격으로 무너지는 구간** — 청크 경계 무음으로 앵커를 잡고,
  같은 길이가 3줄 이상 반복되면 글자 수 비례 재배분 후 무음에 스냅(align 보정).

## 결과물 전달

Claude 아티팩트 페이지는 네트워크 정책상 이미지 CDN을 못 불러오는 환경이라
사진도 소리도 나오지 않는다. 완성본은 **MP4 링크**로 전달한다 (로그인 불필요).
