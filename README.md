# MODERN RELATION UX

연애가 반복해서 막히는 이유를 생활환경, 관계패턴, 연락·갈등 반응, 애착반응, 감정·컨디션(우울·불안·강박·ADHD·불면·공황 가능성), 기존 진단·약복용 영향까지 함께 분석하는 자기이해용 관계 진단 서비스입니다.

본 서비스는 의료기관의 진단을 대체하지 않으며, 자기보고 기반의 관계·심리 패턴 분석을 제공합니다.

## 스택

- Vite + React + TypeScript
- Tailwind CSS v4
- react-router-dom, framer-motion

## 개발

```bash
npm install
npm run dev
```

## 구조

- `src/data` — 질문 문항, 정신건강 스크리닝 문항, 진단/약복용 문항, 결과 유형 12종 정의
- `src/lib/engine.ts` — 단계 흐름 생성 + 점수 산출 + 결과 유형 매칭 알고리즘
- `src/lib/store.tsx` — 진단 답변 상태 관리(세션 저장)
- `src/pages` — Landing / Consent / Test / Result / Guide / Scenario / Expert
- `src/components` — 단계별 질문 렌더러, 진행바, 레이아웃

## 안전 설계

자해·위기 위험 문항(`crisisCheck`)에서 위험도가 높게 감지되면 결과 리포트 대신 안전 안내(109 · 1577-0199 · 119)를 우선 표시합니다.
