import { notFound } from "next/navigation";
import { Container } from "@/components/Container";
import { Button } from "@/components/Button";
import { ReviewDetail } from "@/components/ReviewDetail";
import { PasswordGate } from "@/components/PasswordGate";
import { prisma } from "@/lib/prisma";

export default async function ReviewDetailPage({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id } = await params;
  const review = await prisma.review.findUnique({ where: { id } });

  if (!review || review.status !== "APPROVED") {
    notFound();
  }

  return (
    <div className="bg-ivory-50 py-16">
      <Container className="flex flex-col gap-10">
        {review.isSecret ? (
          <PasswordGate reviewId={review.id} />
        ) : (
          <ReviewDetail review={review} />
        )}

        <div className="flex flex-col items-center gap-4 border-t border-warmgray-200 pt-10 text-center">
          <p className="text-warmgray-600">
            지금 이 후기가 내 상황과 비슷하다고 느껴지신다면, 혼자 고민하지
            마세요.
          </p>
          <div className="flex gap-3">
            <Button href="/apply">1:1 상담 신청하기</Button>
            <Button href="/reviews" variant="secondary">
              다른 후기 보기
            </Button>
          </div>
        </div>
      </Container>
    </div>
  );
}
