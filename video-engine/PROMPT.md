# VIDEO ENGINE MASTER RULES

## 0. Core Goal
`speed/video-engine/`의 기존 구조와 컴포넌트를 최대한 재사용한다.
목표는 좋은 코드가 아니라 **전문 편집자가 만든 것처럼 보이는 좋은 영상**이다.

- 16:9 / 1920×1080 / 30fps / 1080p
- 체감 속도 약 1.2×
- HyperFrames 기반 로컬 CLI 렌더
- 이미지·음성 생성은 Higgsfield
- 기존 엔진을 불필요하게 새로 작성하거나 갈아엎지 않는다.
- 대본의 의미와 논리는 임의로 축약·삭제하지 않는다.
- 시각화 시 대사를 그대로 복붙하지 말고 핵심 의미를 재해석한다.

---

## 1. Brand Visual System
기본 무드는 **dark charcoal + subtle film grain + premium editorial**.

주요 시각 언어:
1. Cinematic B-roll / human photography
2. Cutout person / object
3. Premium pictogram / 2D icon / 3D icon
4. Editorial / conceptual illustration
5. Infographic / graph / diagram / flow
6. Chat UI
7. Big typography
8. Symbolic visual metaphor

### 색상 역할
- Cyan / Blue: 개념, 분석, 구조, 정상 방향
- Warm Brown / Amber: 감정, 긴장, 문제 제기, 챕터
- Yellow: 실제 대화, 인용
- White: 핵심 결론
- Red: 오류·부정 상태에만 제한적으로

같은 영상 안에서 color / material / lighting / stroke / grain / motion speed를 통일해
서로 다른 asset도 하나의 브랜드 시스템처럼 보여야 한다.

---

## 2. Visual Variety
한 종류의 화면만 반복하지 않는다.

가능하면 2~3개 scene마다 시각 표현 방식을 바꾼다.
예:
human photo → pictogram → infographic → B-roll → 3D icon → typography → diagram

단, 다양함을 위해 랜덤하게 넣지 않는다.
항상 narration의 의미에 맞는 format을 선택한다.

선택 우선순위:
- 감정/표정/관계 분위기 → cinematic human photo
- 논리/구조/비교 → infographic / graph / diagram
- 추상 개념 → premium pictogram / 3D symbolic icon
- 실제 상황 → B-roll
- 실제 대화 → chat UI
- 핵심 주장 → typography
- 비유/관계 변화 → symbolic visual metaphor

같은 이미지·같은 누끼·같은 도식은 최대 2회.
같은 배경 3연속 금지.

---

## 3. Premium Asset Rules
### Pictogram / 2D icon
- clean geometry
- controlled stroke width
- subtle depth
- restrained cyan highlight
- minimal shadow / glow
- strong silhouette
- premium editorial 느낌

금지:
- Material Icon 느낌
- Windows 기본 아이콘 느낌
- 무료 PPT 아이콘팩
- corporate clip-art
- 지나치게 귀여운 cartoon

### 3D icon
목표: **premium editorial 3D object / luxury UI icon**

- soft studio lighting
- matte ivory / graphite / muted blue / cyan / warm amber
- subtle AO / contact shadow
- controlled reflection
- realistic but slightly stylized
- childish toy / clay / emoji / candy / game asset 금지
- 영상 전체에서 재질과 광원 방향 통일

### Illustration
- editorial / magazine / conceptual psychology illustration
- restrained palette
- subtle grain
- mature composition
- generic corporate illustration, anime, cute cartoon, 과도한 gradient 금지

### Human Photo
- cinematic lifestyle photography
- 자연스러운 표정·피부·손·자세
- context에 맞는 한국/동아시아 성인 우선
- stock-photo 느낌과 인공적인 AI 미남·미녀 반복 금지
- wide / medium / OTS / hand detail / phone close-up / side profile / silhouette 등 구도 다양화

---

## 4. Background & Brightness
다크 무드는 **배경으로** 만든다.
사진 자체를 검게 죽이지 않는다.

- 얼굴과 핵심 오브젝트는 모바일에서도 명확히 보여야 함
- overlay 중첩, 과도한 vignette, opacity 저하 금지
- 필요하면 exposure / midtone / face brightness 보정
- 텍스트 위에는 필요 시 subtle scrim
- 배경 텍스트 대비는 WCAG AA 이상 확보

---

## 5. Hook & Structure
### 첫 3초
대본의 가장 강한 결론 / 역설 / 문제 제기를 1~3초 안에 보여준다.
배경 설명부터 길게 시작하지 않는다.

### 첫 10초
다음 3개가 최소 1회 들어가야 한다.
- 문제 제기
- 시청자 자기대입
- 영상에서 얻을 가치 암시

### Chapter
5분 이상 영상이면 큰 내용 전환에 chapter break를 사용한다.
1~2초 내외, warm brown / dark amber 계열 가능.

### Ending
마지막에는 전체 내용을 압축하는 **Final Takeaway**를 반드시 둔다.
그 뒤 7~10초 정도의 자연스러운 CTA를 넣는다.

기본 CTA:
소개팅이나 썸탈 때마다
"좋은 사람이지만 남자로는 안 느껴져요"
이런 말을 듣고 있다면
설명란에 있는 비공개 특강을 먼저 확인해보세요.

대본에 별도 CTA가 있으면 그 CTA 우선.

---

## 6. Scene Rhythm & Motion
의미 있는 시각 변화는 일반적으로 **2~4초마다 1회 이상**.

단순 컷 전환만으로 처리하지 않는다.
각 scene 내부에도 subtle micro-motion을 넣는다.

가능:
- slow zoom 100%→102~104%
- ±10~30px camera drift
- parallax
- floating
- light / glow breathing
- gradient shift
- line movement
- shadow movement
- icon micro rotation

기본 motion 구조:
**등장 → settle → subtle motion → 강조 → 퇴장**

linear 반복 금지.
ease-out / ease-in-out / subtle spring / tiny overshoot / mask reveal / line draw 등을 사용.

과장된 bounce / TikTok식 pop 금지.

---

## 7. Semantic Motion
Generic motion보다 **말의 의미를 움직임으로 표현하는 semantic motion**을 우선한다.

예:
- 불안이 올라간다 → graph line 상승
- 생각이 갈라진다 → line 실제 분기
- 대화가 끊긴다 → connection 끊김
- 다시 이어진다 → connection 복구
- 거리가 멀어진다 → 두 인물 간격 증가
- 관계가 깊어진다 → gauge / depth 증가
- 3초 기다린다 → 실제 timer / 초침
- 마음이 닫힌다 → shape / door가 실제로 닫힘

---

## 8. Infographic / Graph
인포그래픽은 장식이 아니라 **내용을 구조화해서 이해시키는 역할**을 해야 한다.

그래프에는 필요에 따라:
- axis
- tick / scale
- 기준점
- level dot
- low / medium / high
- 얕음 / 보통 / 깊음
- 1~5 단계
등을 넣어 "정도"가 읽히게 한다.

그래프는 완성된 상태로 한 번에 나오지 말고
축 → 기준 → 데이터 draw → 핵심 highlight 순으로 애니메이션한다.

Line graph는 path draw.
Bar는 0에서 실제 value까지 grow.

---

## 9. Typography
중앙 타이포는 대사를 그대로 복붙하지 말고
**핵심 의미를 짧게 압축**해서 보여준다.

큰 타이포는 반전 / 결론 / 챕터 핵심 / 기억할 문장에만 사용.
너무 자주 사용하지 않는다.

우측 상단에는 레퍼런스 영상과 같은 크기의 `이다사` 텍스트를 영상 처음부터 끝까지 고정.

---

## 10. Subtitle
절대 규칙:
- 항상 한 줄
- `white-space: nowrap`
- 순백 + 얇은 검정 stroke
- `paint-order: stroke fill`
- 모바일에서도 즉시 읽힐 크기
- bottom safe margin 100~130px 이상
- 긴 문장은 폰트 축소보다 자연스러운 호흡 단위로 분할

중앙 타이포와 하단 자막이 완전히 같은 문장이면 하단 자막 제거.
중앙 타이포가 요약 문구라면 자막 유지 가능.
둘이 겹치면 안 된다.

---

## 11. Cutout / Layout
모든 누끼는 실제 transparency를 확보한다.

인물 누끼:
- 단순 스티커 outline 금지
- torn-paper editorial edge
- 필요 시 subtle cyan glow / contact shadow

모든 주요 요소는 1920×1080의 중앙 safe area 안에 배치.
visual mass도 중앙에서 안정적이어야 한다.
머리·손·중요 오브젝트·shadow가 프레임 밖으로 잘리지 않게 한다.

---

## 12. Chat / Quote UI
실제 대화 상황에만 사용.
실제 카톡 UI 복제보다는 영상 브랜드에 맞춘 stylized UI 사용.

인용 말풍선에는 화자 이름만 쓰지 말고
**실제 발언 내용**을 반드시 적는다.

Message 등장 시 subtle click / slide / bubble reveal 정도만 사용.

---

## 13. Voice
Higgsfield의 저장 보이스를 사용한다.

현재 기본:
- voice: `내-목소리-v4`
- model: 작업 시 지정된 모델
- pitch: 0
- volume: 100%
- MP3 / 24kHz
- 체감 속도 약 1.2×

TTS에서 이미 1.2×로 생성했으면 후처리에서 다시 1.2× 적용하지 않는다.

긴 대본은 문단 단위로 나눠 생성하되
음색·노이즈·호흡·볼륨 jump 없이 자연스럽게 이어 붙인다.

모든 문장을 같은 템포로 읽지 않는다.
핵심 문장 앞뒤에는 0.6~0.9초 등 의도적 pause를 줄 수 있다.
모든 pause 길이를 동일하게 만들지 않는다.

---

## 14. Sound
현재 기본은 **BGM 없음**.

SFX는 핵심 모션에만 최소 사용:
- subtle whoosh
- tiny UI click
- soft / low impact
- line draw
- muted transition
- tiny synth tick

과장된 pop, cartoon, TikTok식 효과음 난사 금지.

효과음은 반드시 시각 움직임과 sync:
message → click
line draw → draw sound
graph peak → tiny tick
핵심 문장 → low impact

---

## 15. Audio Mastering
- Integrated loudness: 약 -14~-15 LUFS
- True Peak: 약 -1 dBTP 이하
- voice가 항상 최우선
- 과도한 limiter / compression 금지

---

## 16. Render & Audio Safety
오디오는 렌더 시작 전에 반드시 완성하고 경로/존재 여부 확인.
컴포지션이 없는 오디오 asset을 참조하지 않게 한다.

나레이션 길이와 자막 timing을 맞춘다.
필요하면 `atempo`로 사람이 거의 느끼지 못하는 범위에서 미세 보정.

원격 sandbox 렌더라면 끝날 때까지 process를 확인하고
완료 후 output file 존재를 직접 검증한다.

---

## 17. Preview QA
최종 렌더 전 preview를 만들고
**코드가 아니라 실제 렌더 프레임으로 검수**한다.

반드시 눈으로 확인:
1. 자막이 전부 한 줄인가
2. 자막이 프레임 밖으로 나가지 않는가
3. 모바일에서 읽을 정도로 큰가
4. cutout / icon 배경이 실제 제거됐는가
5. 인물·아이콘이 중앙 safe area에 있는가
6. 이미지가 검게 죽지 않았는가
7. graph / bar / line이 실제 렌더되는가
8. graph의 정도가 읽히는가
9. motion이 실제로 작동하는가

대표 캡처:
- 첫 3초
- 30초
- 1분
- 25%
- 50%
- 75%
- Final Takeaway
- CTA

대표 scene은 시작 / 중간 / 종료 3프레임 이상 확인.
세 프레임이 거의 같으면 micro-motion이 부족한 것으로 보고 수정.

---

## 18. Output
최종 결과물:
### MASTER
- MP4
- 1920×1080
- 최고 품질
- 나레이션 포함

### LIGHT
- MP4
- 브라우저에서 바로 재생
- 약 100MB 내외
- 시각 품질 손실 최소화
- 나레이션 포함

최종 링크는 로그인 / 권한 승인 / claim 없이 바로 열 수 있어야 한다.

---

## 19. Execution Principles
- 기존 컴포넌트 재사용
- 이미 해결된 문제를 다시 조사하지 않기
- 중간에 사소한 질문 반복 금지
- 합리적 판단은 스스로 하고 끝까지 진행
- 오류 발생 시 원인 분석 → 수정 → 계속 진행
- 새 기능보다 최종 영상 완성도를 우선
- 토큰을 불필요하게 낭비하지 않는다.

**목표는 좋은 코드가 아니라 좋은 영상이다.**
