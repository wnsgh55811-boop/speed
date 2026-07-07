import type { Metadata } from "next";
import { Suspense } from "react";
import { Container } from "@/components/Container";
import { Button } from "@/components/Button";
import { ApplyForm } from "@/components/ApplyForm";
import { site } from "@/lib/site";

export const metadata: Metadata = {
  title: "상담 신청",
  description: "러브백 1:1 상담 신청 페이지.",
};

const process = [
  "상담 상품 선택",
  "결제 진행",
  "상담 신청서 작성",
  "상담 일정 조율",
  "1:1 상담 진행",
  "상담 후 실행 방향 정리",
];

export default function ApplyPage() {
  return (
    <div>
      <section className="border-b border-warmgray-200 bg-navy-950 py-16 text-ivory-50 sm:py-20">
        <Container className="flex flex-col items-center gap-4 text-center">
          <span className="text-xs font-semibold tracking-[0.2em] text-ivory-100/70 uppercase">
            Apply
          </span>
          <h1 className="font-serif-kr max-w-2xl text-3xl leading-snug font-medium sm:text-4xl">
            러브백 1:1 상담 신청
          </h1>
          <p className="max-w-xl text-ivory-100/75">
            상담을 원하시는 분은 아래 내용을 확인한 후 신청해주세요. 신청서
            작성 후 코치가 확인하고 결제 및 일정 안내를 도와드립니다.
          </p>
        </Container>
      </section>

      <section className="bg-ivory-50 py-14">
        <Container>
          <div className="mb-14 grid gap-3 sm:grid-cols-3 lg:grid-cols-6">
            {process.map((p, i) => (
              <div
                key={p}
                className="flex flex-col gap-2 rounded-sm border border-warmgray-200 bg-white p-4 text-center"
              >
                <span className="font-serif-kr text-burgundy-600">{i + 1}</span>
                <span className="text-sm text-navy-800">{p}</span>
              </div>
            ))}
          </div>
        </Container>
      </section>

      <section className="bg-beige-100 pb-20">
        <Container className="max-w-2xl">
          <div className="rounded-sm border border-warmgray-300/60 bg-white p-6 sm:p-10">
            <Suspense>
              <ApplyForm />
            </Suspense>
          </div>

          <div className="mt-8 flex flex-col items-center gap-3 text-center">
            <p className="text-warmgray-600">
              신청서 작성이 어렵거나 먼저 문의하고 싶으시다면
            </p>
            <Button href={site.kakaoChannelUrl} target="_blank" variant="kakao">
              카카오톡으로 문의하기
            </Button>
          </div>
        </Container>
      </section>
    </div>
  );
}
