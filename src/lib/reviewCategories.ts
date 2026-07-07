export const reviewCategories = [
  { value: "REUNION", label: "재회 상담 후기" },
  { value: "DATING", label: "연애 상담 후기" },
  { value: "SOME", label: "썸/소개팅 상담 후기" },
  { value: "CHAT_ANALYSIS", label: "카톡 분석 후기" },
  { value: "PATTERN", label: "관계 패턴 진단 후기" },
  { value: "LONGFORM", label: "장문 후기" },
  { value: "CHANGE", label: "상담 후 변화 후기" },
] as const;

export type ReviewCategoryValue = (typeof reviewCategories)[number]["value"];

export function reviewCategoryLabel(value: string) {
  return reviewCategories.find((c) => c.value === value)?.label ?? value;
}

export const programTypes = [
  { value: "DATING", label: "연애/썸 관계 진단 상담" },
  { value: "REUNION", label: "재회 전략 상담" },
  { value: "PREMIUM", label: "프리미엄 관계 분석 상담" },
  { value: "UNSURE", label: "아직 잘 모르겠어요 (상담 후 추천받고 싶어요)" },
] as const;

export function programLabel(value: string) {
  return programTypes.find((p) => p.value === value)?.label ?? value;
}
