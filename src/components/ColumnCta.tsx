import { Button } from "./Button";

export function ColumnCta() {
  return (
    <div className="flex flex-col items-center gap-5 rounded-sm border border-warmgray-200 bg-beige-100 p-8 text-center">
      <p className="max-w-lg leading-relaxed text-navy-800">
        지금 이 글을 읽으며 “내 상황도 여기에 해당되는 것 같다”는 생각이
        들었다면, 혼자서 연락 타이밍만 고민하지 마세요.
      </p>
      <p className="max-w-lg leading-relaxed text-navy-800">
        관계는 상황마다 흐름이 다르고, 상대의 심리적 저항도 다릅니다. 러브백
        관계 연구소에서는 현재 관계의 흐름, 상대 심리, 내 행동 패턴을 함께
        분석해 지금 해야 할 선택을 정리해드립니다.
      </p>
      <Button href="/apply" size="lg">
        1:1 상담 신청하기
      </Button>
    </div>
  );
}
