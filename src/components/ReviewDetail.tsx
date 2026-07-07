import { reviewCategoryLabel } from "@/lib/reviewCategories";

export type ReviewDetailData = {
  category: string;
  nickname: string;
  ageGroup?: string | null;
  situationTag?: string | null;
  title: string;
  beforeContent: string;
  hardestPart: string;
  helpfulPart: string;
  afterContent: string;
  messageToOthers?: string | null;
  createdAt: string | Date;
};

function Block({ label, content }: { label: string; content: string }) {
  return (
    <div className="flex flex-col gap-2">
      <h3 className="text-sm font-semibold tracking-wide text-burgundy-700">
        {label}
      </h3>
      <p className="leading-relaxed whitespace-pre-line text-navy-800">{content}</p>
    </div>
  );
}

export function ReviewDetail({ review }: { review: ReviewDetailData }) {
  const date = new Date(review.createdAt);

  return (
    <div className="flex flex-col gap-8">
      <div className="flex flex-col gap-3">
        <span className="w-fit rounded-full bg-navy-900 px-3 py-1 text-xs font-medium text-ivory-50">
          {reviewCategoryLabel(review.category)}
        </span>
        <h1 className="font-serif-kr text-2xl leading-snug font-medium text-navy-900 sm:text-3xl">
          {review.title}
        </h1>
        <p className="text-sm text-warmgray-500">
          {[review.nickname, review.ageGroup, review.situationTag]
            .filter(Boolean)
            .join(" · ")}{" "}
          · {date.toLocaleDateString("ko-KR")}
        </p>
      </div>

      <div className="flex flex-col gap-6 rounded-sm border border-warmgray-200 bg-white p-6 sm:p-8">
        <Block label="상담 전 어떤 상황이었나요?" content={review.beforeContent} />
        <Block label="가장 힘들었던 부분은 무엇이었나요?" content={review.hardestPart} />
        <Block
          label="상담에서 가장 도움 됐던 부분은 무엇인가요?"
          content={review.helpfulPart}
        />
        <Block
          label="상담 후 생각이나 행동이 어떻게 달라졌나요?"
          content={review.afterContent}
        />
        {review.messageToOthers && (
          <Block
            label="비슷한 상황의 사람에게 해주고 싶은 말"
            content={review.messageToOthers}
          />
        )}
      </div>
    </div>
  );
}
