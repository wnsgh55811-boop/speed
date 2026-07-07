import type { Metadata } from "next";
import Link from "next/link";
import { Lock } from "lucide-react";
import { Container } from "@/components/Container";
import { SectionHeading } from "@/components/SectionHeading";
import { Button } from "@/components/Button";
import { ReviewCard } from "@/components/ReviewCard";
import { reviewCategories, reviewCategoryLabel } from "@/lib/reviewCategories";
import { prisma } from "@/lib/prisma";
import { clsx } from "clsx";

export const metadata: Metadata = {
  title: "상담 후기",
  description: "러브백 관계 연구소 실제 상담 후기 게시판.",
};

export default async function ReviewsPage({
  searchParams,
}: {
  searchParams: Promise<{ category?: string }>;
}) {
  const { category } = await searchParams;

  const reviews = await prisma.review.findMany({
    where: {
      status: "APPROVED",
      ...(category ? { category: category as never } : {}),
    },
    orderBy: { createdAt: "desc" },
  });

  return (
    <div>
      <section className="border-b border-warmgray-200 bg-navy-950 py-16 text-ivory-50 sm:py-20">
        <Container className="flex flex-col items-center gap-4 text-center">
          <span className="text-xs font-semibold tracking-[0.2em] text-ivory-100/70 uppercase">
            Reviews
          </span>
          <h1 className="font-serif-kr max-w-2xl text-3xl leading-snug font-medium sm:text-4xl">
            상담 후기
          </h1>
          <p className="max-w-xl text-ivory-100/75">
            나와 비슷한 상황의 사람들이 상담을 통해 무엇을 얻었는지 확인해보세요.
          </p>
          <Button href="/reviews/write" variant="kakao" size="sm">
            내 후기 남기기
          </Button>
        </Container>
      </section>

      <section className="bg-ivory-50 py-14">
        <Container className="flex flex-col gap-10">
          <div className="flex flex-wrap gap-2">
            <Link
              href="/reviews"
              className={clsx(
                "rounded-full border px-4 py-1.5 text-sm transition-colors",
                !category
                  ? "border-navy-900 bg-navy-900 text-ivory-50"
                  : "border-warmgray-300 text-navy-800 hover:border-navy-700",
              )}
            >
              전체
            </Link>
            {reviewCategories.map((c) => (
              <Link
                key={c.value}
                href={`/reviews?category=${c.value}`}
                className={clsx(
                  "rounded-full border px-4 py-1.5 text-sm transition-colors",
                  category === c.value
                    ? "border-navy-900 bg-navy-900 text-ivory-50"
                    : "border-warmgray-300 text-navy-800 hover:border-navy-700",
                )}
              >
                {c.label}
              </Link>
            ))}
          </div>

          {reviews.length === 0 ? (
            <p className="py-16 text-center text-warmgray-500">
              {category
                ? `"${reviewCategoryLabel(category)}" 카테고리의 후기가 아직 없습니다.`
                : "등록된 후기가 아직 없습니다."}
            </p>
          ) : (
            <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
              {reviews.map((r) =>
                r.isSecret ? (
                  <Link
                    key={r.id}
                    href={`/reviews/${r.id}`}
                    className="flex h-full flex-col gap-4 rounded-sm border border-warmgray-300/60 bg-beige-100 p-6 transition-shadow hover:shadow-md"
                  >
                    <span className="w-fit rounded-full bg-navy-900 px-3 py-1 text-xs font-medium text-ivory-50">
                      {reviewCategoryLabel(r.category)}
                    </span>
                    <p className="flex flex-1 items-center gap-2 font-serif-kr text-lg text-warmgray-500">
                      <Lock size={16} /> 비밀글입니다
                    </p>
                    <span className="text-xs font-medium text-burgundy-700">
                      비밀번호 확인 후 보기 →
                    </span>
                  </Link>
                ) : (
                  <ReviewCard
                    key={r.id}
                    id={r.id}
                    category={r.category}
                    title={r.title}
                    helpfulPart={r.helpfulPart}
                    ageGroup={r.ageGroup}
                    situationTag={r.situationTag}
                  />
                ),
              )}
            </div>
          )}
        </Container>
      </section>

      <section className="bg-navy-900 py-16 text-ivory-50">
        <Container className="flex flex-col items-center gap-6 text-center">
          <SectionHeading
            title="지금 이 상황, 나만 겪는 게 아닙니다"
            description="비슷한 상황의 후기를 더 보고 싶다면, 1:1 상담으로 내 상황도 정리해보세요."
            light
          />
          <Button href="/apply" size="lg">
            상담 신청하기
          </Button>
        </Container>
      </section>
    </div>
  );
}
