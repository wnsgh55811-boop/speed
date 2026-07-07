import type { Metadata } from "next";
import { Container } from "@/components/Container";
import { SectionHeading } from "@/components/SectionHeading";
import { Button } from "@/components/Button";
import { ReviewCard } from "@/components/ReviewCard";
import { prisma } from "@/lib/prisma";

export const metadata: Metadata = {
  title: "가격 안내",
  description: "러브백 1:1 상담 프로그램 가격 안내.",
};

const plans = [
  {
    program: "DATING",
    title: "연애/썸 관계 진단 상담",
    audience: "현재 연애 중이거나 썸 단계에서 관계 흐름이 불안한 분",
    items: [
      "현재 관계 흐름 분석",
      "상대 심리 분석",
      "내 대화/태도 패턴 진단",
      "앞으로의 접근 전략 제시",
      "연락/만남/표현 방식 가이드",
    ],
    duration: "60분",
    reviewCategory: "DATING",
  },
  {
    program: "REUNION",
    title: "재회 전략 상담",
    audience: "이별 후 재회를 원하지만 연락 타이밍과 방향을 모르는 분",
    items: [
      "이별 원인 분석",
      "상대의 현재 심리 상태 분석",
      "재회 가능성 판단",
      "연락 타이밍 및 메시지 방향",
      "재회 과정에서 하지 말아야 할 행동 정리",
      "상황별 대응 전략",
    ],
    duration: "60분",
    reviewCategory: "REUNION",
    featured: true,
  },
  {
    program: "PREMIUM",
    title: "프리미엄 관계 분석 상담",
    audience: "단순 답변이 아니라 내 연애 패턴 자체를 깊게 바꾸고 싶은 분",
    items: [
      "전체 연애 패턴 분석",
      "애착 유형 기반 관계 진단",
      "반복되는 관계 문제 구조화",
      "상대 선택 기준 정리",
      "장기적인 관계 개선 전략",
      "상담 후 실행 가이드 제공",
    ],
    duration: "90분",
    reviewCategory: "PATTERN",
  },
];

export default async function PricingPage() {
  const reviews = await Promise.all(
    plans.map((p) =>
      prisma.review.findFirst({
        where: { status: "APPROVED", category: p.reviewCategory as never },
        orderBy: { createdAt: "desc" },
      }),
    ),
  );

  return (
    <div>
      <section className="border-b border-warmgray-200 bg-navy-950 py-16 text-ivory-50 sm:py-20">
        <Container className="flex flex-col items-center gap-4 text-center">
          <span className="text-xs font-semibold tracking-[0.2em] text-ivory-100/70 uppercase">
            Pricing
          </span>
          <h1 className="font-serif-kr max-w-2xl text-3xl leading-snug font-medium sm:text-4xl">
            러브백 상담 프로그램 가격
          </h1>
          <p className="max-w-xl text-ivory-100/75">
            상담 특성상 정가는 프로그램 진행 전 안내드리며, 아래는 표준 구성
            기준 가격입니다.
          </p>
        </Container>
      </section>

      <section className="bg-ivory-50 py-20">
        <Container className="flex flex-col gap-16">
          {plans.map((plan, i) => (
            <div key={plan.program} className="flex flex-col gap-8">
              <div
                className={`grid gap-8 rounded-sm border p-8 md:grid-cols-[1.3fr_1fr] ${
                  plan.featured
                    ? "border-burgundy-600 bg-white shadow-lg"
                    : "border-warmgray-200 bg-white"
                }`}
              >
                <div className="flex flex-col gap-4">
                  {plan.featured && (
                    <span className="w-fit rounded-full bg-burgundy-700 px-3 py-1 text-xs font-medium text-ivory-50">
                      가장 많이 찾는 상담
                    </span>
                  )}
                  <h2 className="font-serif-kr text-2xl font-medium text-navy-900">
                    {plan.title}
                  </h2>
                  <p className="text-sm text-warmgray-500">
                    추천 대상 · {plan.audience}
                  </p>
                  <ul className="space-y-2 text-navy-800">
                    {plan.items.map((item) => (
                      <li key={item}>· {item}</li>
                    ))}
                  </ul>
                </div>
                <div className="flex flex-col justify-between gap-6 rounded-sm bg-beige-100 p-6">
                  <div>
                    <p className="text-sm text-warmgray-600">진행 시간</p>
                    <p className="mb-4 text-xl font-medium text-navy-900">
                      {plan.duration}
                    </p>
                    <p className="text-sm text-warmgray-600">상담 비용</p>
                    <p className="font-serif-kr text-3xl font-medium text-navy-900">
                      상담 신청 시 안내
                    </p>
                  </div>
                  <Button href={`/apply?program=${plan.program}`} className="w-full">
                    {plan.title.replace(" 상담", "")} 상담 신청하기
                  </Button>
                </div>
              </div>

              {reviews[i] && (
                <div className="max-w-md">
                  <ReviewCard
                    id={reviews[i]!.id}
                    category={reviews[i]!.category}
                    title={reviews[i]!.title}
                    helpfulPart={reviews[i]!.helpfulPart}
                    ageGroup={reviews[i]!.ageGroup}
                    situationTag={reviews[i]!.situationTag}
                  />
                </div>
              )}
            </div>
          ))}
        </Container>
      </section>

      <section className="bg-beige-100 py-20">
        <Container className="flex flex-col items-center gap-6 text-center">
          <SectionHeading
            title="어떤 상담이 맞을지 잘 모르겠다면"
            description="신청서에 현재 상황을 적어주시면, 상담 전 코치가 적합한 프로그램을 안내해드립니다."
          />
          <Button href="/apply?program=UNSURE" size="lg">
            상담 상품 추천받기
          </Button>
        </Container>
      </section>
    </div>
  );
}
