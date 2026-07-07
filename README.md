# 러브백 관계 연구소

연애·이별·재회 관계 코칭 상담 서비스 "러브백 관계 연구소"의 공식 웹사이트입니다.
Next.js(App Router) + TypeScript + Tailwind CSS + Prisma(SQLite)로 구현되었습니다.

## 포함된 기능

### 1차 (MVP)
- 메인 랜딩 페이지 (히어로, 공감 섹션, 브랜드 철학, 상담 분야, 상황별 추천, 후기 미리보기)
- 러브백 소개 (철학 + 코치 소개)
- 상담 프로그램 (6단계 상담 진행 방식, 3개 상담 분야)
- 가격 안내 (연애/재회/프리미엄 3개 상품)
- 상담 후기 게시판 (카테고리 필터, 비밀글, 후기 작성, 관리자 승인 노출)
- 블로그 칼럼 (연애/재회/카톡/관계심리 4개 카테고리, 20편)
- 상담 신청 (신청서 작성 → API 저장)
- FAQ
- 이용약관 / 개인정보처리방침 / 환불규정
- 모바일 하단 고정 CTA(카톡 문의 / 상담 신청)

### 2차 확장
- 무료 진단 체크리스트 4종 (자가진단 → 결과 → 추천 프로그램 CTA)
- 관리자 대시보드 (`/admin`, 비밀번호 로그인)
  - 후기 승인 / 비공개 처리
  - 상담 신청 상태 관리 및 메모

## 시작하기

```bash
npm install
cp .env.example .env   # ADMIN_PASSWORD, ADMIN_SESSION_SECRET 값을 변경하세요
npx prisma migrate dev
npm run db:seed        # 샘플 후기 데이터 시딩 (선택)
npm run dev
```

http://localhost:3000 에서 확인할 수 있습니다.

관리자 대시보드는 `/admin` (초기 비밀번호는 `.env`의 `ADMIN_PASSWORD` 값)에서 접속합니다.

## 운영 배포 전 확인 사항

- `ADMIN_PASSWORD`, `ADMIN_SESSION_SECRET`을 반드시 변경하세요.
- 결제 연동은 포함되어 있지 않습니다. 상담 신청은 신청서 접수까지만 처리되며,
  실제 결제는 카카오톡 채널 안내 또는 별도 PG 연동이 필요합니다.
- `site.kakaoChannelUrl`, `site.phone` 등 연락처 정보는 `src/lib/site.ts`에서 실제 값으로 교체하세요.
- 프로덕션에서는 SQLite 대신 PostgreSQL 등으로 `DATABASE_URL`과 Prisma datasource를 교체하는 것을 권장합니다.

## 기술 스택

- Next.js 16 (App Router, Turbopack)
- TypeScript
- Tailwind CSS v4
- Prisma + SQLite (better-sqlite3 driver adapter)
- Zod (입력 검증)
