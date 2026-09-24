# VIDEO ENGINE QA CHECKLIST

이 파일은 Preview 이후 최종 렌더 전에 사용한다.
코드만 보고 체크하지 말고 실제 프레임/영상으로 확인한다.

---

## A. HOOK
- [ ] 첫 1~3초 안에 문제/역설/핵심 결론이 보이는가
- [ ] 첫 10초 안에 시청자가 자기 이야기라고 느낄 장면이 있는가
- [ ] 첫 10초 안에 이 영상을 계속 볼 이유가 드러나는가

---

## B. SUBTITLE
- [ ] 모든 자막이 한 줄인가
- [ ] `white-space: nowrap`이 실제로 적용됐는가
- [ ] 하단 safe margin 100~130px 이상인가
- [ ] 모바일에서 읽을 크기인가
- [ ] 긴 자막 때문에 폰트가 과도하게 작아지지 않았는가
- [ ] 중앙 타이포와 동일 문장이 중복되지 않는가
- [ ] 중앙 타이포와 자막이 겹치지 않는가
- [ ] 순백 + 얇은 검정 stroke가 정상 렌더되는가

---

## C. LAYOUT
- [ ] 주요 요소가 중앙 safe area 안에 있는가
- [ ] visual mass가 한쪽으로 무너지지 않는가
- [ ] 인물 머리/손/중요 오브젝트가 잘리지 않는가
- [ ] icon shadow/glow까지 프레임 안에 있는가
- [ ] 우측 상단 `이다사` 표시가 정상인가

---

## D. IMAGE / CUTOUT
- [ ] 인물·오브젝트 배경이 실제 제거됐는가
- [ ] 검은 사각형/원본 배경이 남아 있지 않은가
- [ ] torn-paper edge가 자연스러운가
- [ ] 단순 스티커 outline처럼 보이지 않는가
- [ ] 인물이 너무 어둡지 않은가
- [ ] 얼굴과 핵심 오브젝트가 모바일에서도 보이는가
- [ ] 같은 이미지/누끼를 3회 이상 사용하지 않았는가

---

## E. VISUAL VARIETY
- [ ] 같은 visual type이 3 scene 이상 연속되지 않는가
- [ ] B-roll / human photo / pictogram / 3D icon / illustration / infographic / typography가 의미에 맞게 교차되는가
- [ ] 다양하지만 하나의 브랜드처럼 보이는가
- [ ] cheap stock / PPT / Canva / cartoon 느낌 asset이 없는가
- [ ] 3D icon의 재질과 광원이 통일됐는가
- [ ] 인물 사진의 스타일이 서로 지나치게 이질적이지 않은가

---

## F. MOTION
- [ ] 평균 2~4초마다 의미 있는 시각 변화가 있는가
- [ ] 정적인 scene에도 micro-motion이 있는가
- [ ] 대표 scene 시작/중간/끝 프레임이 실제로 변화하는가
- [ ] linear animation만 반복되지 않는가
- [ ] 과도한 bounce/pop이 없는가
- [ ] narration 의미와 motion이 연결되는가

대표 scene은 최소 3프레임 캡처:
- start
- middle
- end

세 프레임이 거의 같으면 수정.

---

## G. GRAPH / INFOGRAPHIC
- [ ] graph/bar/line이 실제로 렌더되는가
- [ ] `<i>` inline bug 등으로 사라진 요소가 없는가
- [ ] axis / scale / label / level 등 정도가 읽히는가
- [ ] 모바일에서 글자가 너무 작지 않은가
- [ ] graph가 0→value 또는 path draw 방식으로 실제 애니메이션되는가
- [ ] 핵심 구간이 highlight되는가

---

## H. CHAT / QUOTE
- [ ] 말풍선에 실제 발언 내용이 있는가
- [ ] 화자 이름만 있는 빈 말풍선이 없는가
- [ ] chat UI가 전체 브랜드 톤과 맞는가
- [ ] message motion과 click SFX가 정확히 sync되는가

---

## I. AUDIO
- [ ] 나레이션이 끊기지 않는가
- [ ] 문단 간 음색/볼륨 jump가 없는가
- [ ] 모든 pause가 똑같은 길이로 반복되지 않는가
- [ ] 핵심 문장에 필요한 호흡이 있는가
- [ ] 효과음이 목소리를 가리지 않는가
- [ ] 불필요한 효과음이 남발되지 않았는가
- [ ] Integrated loudness가 약 -14~-15 LUFS인가
- [ ] True Peak가 약 -1 dBTP 이하인가
- [ ] 나레이션과 자막 timing이 맞는가

---

## J. ENDING / CTA
- [ ] Final Takeaway가 기억에 남는 한 문장인가
- [ ] 단순 요약문이 아니라 영상의 핵심 생각을 남기는가
- [ ] CTA가 7~10초 내외로 자연스러운가
- [ ] CTA가 영상 여운을 깨지 않는가
- [ ] CTA에서 다음 행동이 명확한가

---

## K. REPRESENTATIVE FRAME CAPTURE
반드시 실제 캡처 확인:
- [ ] 첫 3초
- [ ] 30초
- [ ] 1분
- [ ] 25%
- [ ] 50%
- [ ] 75%
- [ ] Final Takeaway
- [ ] CTA

각 프레임에서:
- [ ] 지나치게 어둡지 않은가
- [ ] 작은 글자가 없는가
- [ ] 이미지가 충분히 보이는가
- [ ] 화면 중심이 안정적인가
- [ ] 자막이 안전한가
- [ ] motion/graph가 실제로 렌더되는가

---

## L. OUTPUT
- [ ] MASTER MP4 존재
- [ ] LIGHT MP4 존재
- [ ] MASTER에 나레이션 포함
- [ ] LIGHT에 나레이션 포함
- [ ] LIGHT가 약 100MB 내외
- [ ] 브라우저에서 바로 재생 가능
- [ ] 링크에 로그인/권한승인/claim이 필요하지 않음
