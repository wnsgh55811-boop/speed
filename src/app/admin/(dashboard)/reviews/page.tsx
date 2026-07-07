import Link from "next/link";
import { clsx } from "clsx";
import { prisma } from "@/lib/prisma";
import { reviewCategoryLabel } from "@/lib/reviewCategories";
import { updateReviewStatus } from "../../actions";

const statusLabel: Record<string, string> = {
  PENDING: "승인 대기",
  APPROVED: "게시 중",
  HIDDEN: "비공개",
};

export default async function AdminReviewsPage({
  searchParams,
}: {
  searchParams: Promise<{ status?: string }>;
}) {
  const { status } = await searchParams;
  const activeStatus = status ?? "PENDING";

  const reviews = await prisma.review.findMany({
    where: { status: activeStatus as never },
    orderBy: { createdAt: "desc" },
  });

  return (
    <div className="flex flex-col gap-6">
      <h1 className="font-serif-kr text-2xl font-medium text-navy-900">후기 관리</h1>

      <div className="flex gap-2">
        {["PENDING", "APPROVED", "HIDDEN"].map((s) => (
          <Link
            key={s}
            href={`/admin/reviews?status=${s}`}
            className={clsx(
              "rounded-full border px-4 py-1.5 text-sm",
              activeStatus === s
                ? "border-navy-900 bg-navy-900 text-ivory-50"
                : "border-warmgray-300 text-navy-800",
            )}
          >
            {statusLabel[s]}
          </Link>
        ))}
      </div>

      <div className="flex flex-col gap-4">
        {reviews.length === 0 && (
          <p className="py-10 text-center text-warmgray-500">
            해당하는 후기가 없습니다.
          </p>
        )}
        {reviews.map((r) => (
          <div key={r.id} className="rounded-sm border border-warmgray-200 bg-white p-5">
            <div className="mb-2 flex flex-wrap items-center gap-2 text-xs text-warmgray-500">
              <span className="rounded-full bg-beige-200 px-2 py-0.5 text-navy-800">
                {reviewCategoryLabel(r.category)}
              </span>
              {r.isSecret && (
                <span className="rounded-full bg-navy-900 px-2 py-0.5 text-ivory-50">
                  비밀글
                </span>
              )}
              <span>{r.nickname}</span>
              <span>{new Date(r.createdAt).toLocaleString("ko-KR")}</span>
            </div>
            <p className="mb-1 font-medium text-navy-900">{r.title}</p>
            <p className="mb-4 line-clamp-2 text-sm text-warmgray-600">
              {r.helpfulPart}
            </p>
            <div className="flex gap-2">
              {activeStatus !== "APPROVED" && (
                <form action={updateReviewStatus.bind(null, r.id, "APPROVED")}>
                  <button className="rounded-sm bg-navy-900 px-4 py-1.5 text-sm text-ivory-50 hover:bg-navy-800">
                    승인
                  </button>
                </form>
              )}
              {activeStatus !== "HIDDEN" && (
                <form action={updateReviewStatus.bind(null, r.id, "HIDDEN")}>
                  <button className="rounded-sm border border-warmgray-300 px-4 py-1.5 text-sm text-navy-800 hover:border-navy-700">
                    비공개 처리
                  </button>
                </form>
              )}
              {activeStatus !== "PENDING" && (
                <form action={updateReviewStatus.bind(null, r.id, "PENDING")}>
                  <button className="rounded-sm border border-warmgray-300 px-4 py-1.5 text-sm text-navy-800 hover:border-navy-700">
                    대기 상태로
                  </button>
                </form>
              )}
              {activeStatus === "APPROVED" && (
                <Link
                  href={`/reviews/${r.id}`}
                  target="_blank"
                  className="rounded-sm border border-warmgray-300 px-4 py-1.5 text-sm text-navy-800 hover:border-navy-700"
                >
                  미리보기
                </Link>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
