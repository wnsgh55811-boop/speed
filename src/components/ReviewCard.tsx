import Link from "next/link";
import { reviewCategoryLabel } from "@/lib/reviewCategories";

export function ReviewCard({
  id,
  category,
  title,
  helpfulPart,
  ageGroup,
  situationTag,
}: {
  id: string;
  category: string;
  title: string;
  helpfulPart: string;
  ageGroup?: string | null;
  situationTag?: string | null;
}) {
  return (
    <Link
      href={`/reviews/${id}`}
      className="flex h-full flex-col gap-4 rounded-sm border border-warmgray-300/60 bg-beige-100 p-6 transition-shadow hover:shadow-md"
    >
      <span className="w-fit rounded-full bg-navy-900 px-3 py-1 text-xs font-medium text-ivory-50">
        {reviewCategoryLabel(category)}
      </span>
      <p className="font-serif-kr text-lg leading-snug text-navy-900">
        “{title}”
      </p>
      <p className="line-clamp-3 flex-1 text-sm leading-relaxed text-warmgray-600">
        {helpfulPart}
      </p>
      <div className="flex items-center justify-between text-xs text-warmgray-500">
        <span>
          {[ageGroup, situationTag].filter(Boolean).join(" · ") || "러브백 상담 후기"}
        </span>
        <span className="font-medium text-burgundy-700">후기 전체 보기 →</span>
      </div>
    </Link>
  );
}
