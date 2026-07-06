import type { CrisisCheckStep, MentalHealthDomain, ScaleQuestionnaireStep, SingleChoiceStep } from "./types";

export const mentalHealthIntro = {
  title: "감정과 컨디션에 대한 질문",
  body: [
    "이제 관계에 영향을 줄 수 있는 감정·컨디션 질문이 나옵니다.",
    "이 질문은 병명을 확정하기 위한 것이 아니라, 연락, 약속, 감정표현, 갈등반응에 영향을 주는 심리적 요인을 확인하기 위한 것입니다.",
    "답변이 불편한 문항은 건너뛸 수 있습니다.",
  ],
  cta: "다음",
};

export const quickScreenStep: SingleChoiceStep = {
  kind: "single",
  id: "quickScreen",
  section: "감정·컨디션 스크리닝",
  question: "최근 2주 기준, 가장 가까운 상태는?",
  options: [
    { label: "기분이 자주 가라앉고 의욕이 줄었다", value: "depression" },
    { label: "걱정이 많고 긴장이 잘 풀리지 않는다", value: "anxiety" },
    { label: "특정 생각이나 행동을 반복하지 않으면 불안하다", value: "ocd" },
    { label: "집중이 어렵고 일을 자주 미루거나 놓친다", value: "adhd" },
    { label: "잠들기 어렵거나 자주 깨고 피곤하다", value: "insomnia" },
    { label: "갑자기 심장이 뛰고 숨이 막히는 공포감이 온다", value: "panic" },
    { label: "특별히 해당 없음", value: "none" },
  ],
};

export const domainDefinitions: Record<MentalHealthDomain, {
  label: string;
  title: string;
  intro: string;
  timeframe: string;
  items: string[];
  lightItemIdx: number[];
  scaleOptions: { label: string; score: number }[];
  levels: { max: number; label: string }[];
  analysis: (level: string) => string;
}> = {
  depression: {
    label: "우울 영역",
    title: "우울 영역 체크",
    intro: "기분과 의욕에 관한 질문입니다. 우울 가능성이 높으면 연락 에너지 저하, 데이트 회피, 자기비난, 이별 후 회복 지연 같은 패턴으로 나타날 수 있습니다.",
    timeframe: "최근 2주 동안",
    items: [
      "흥미나 즐거움이 줄었다",
      "기분이 가라앉거나 공허했다",
      "잠을 너무 못 자거나 너무 많이 잤다",
      "피로감이 컸다",
      "식욕이 줄거나 늘었다",
      "자신을 부정적으로 생각했다",
      "집중이 어려웠다",
      "행동이 느려지거나 초조했다",
      "사라지고 싶거나 죽고 싶다는 생각이 있었다",
    ],
    lightItemIdx: [0, 1],
    scaleOptions: [
      { label: "전혀 없음", score: 0 },
      { label: "며칠 있음", score: 1 },
      { label: "일주일 이상", score: 2 },
      { label: "거의 매일", score: 3 },
    ],
    levels: [
      { max: 4, label: "낮음" },
      { max: 9, label: "경미" },
      { max: 14, label: "중간" },
      { max: 19, label: "높음" },
      { max: Infinity, label: "매우 높음" },
    ],
    analysis: (level) =>
      level === "높음" || level === "매우 높음"
        ? "기분 저하가 높게 나타납니다. 이 경우 상대에게 마음이 식은 것이 아닌데도 연락을 미루거나 데이트를 피하게 될 수 있습니다. 이별 후 회복이 늦어지거나 상대 반응을 자기비난으로 해석할 가능성도 있습니다."
        : level === "중간"
        ? "기분 저하 신호가 일부 나타납니다. 컨디션이 낮은 날에는 연락과 데이트 에너지가 함께 떨어질 수 있습니다."
        : "기분·의욕 영역은 비교적 안정적으로 보입니다.",
  },
  anxiety: {
    label: "불안 영역",
    title: "불안 영역 체크",
    intro: "불안이 높으면 답장 지연을 거절로 해석하거나, 상대의 말투 변화에 과민해지고, 관계를 확인하려는 행동이 늘어날 수 있습니다.",
    timeframe: "최근 2주 동안",
    items: [
      "초조하거나 불안했다",
      "걱정을 멈추기 어려웠다",
      "여러 가지 일을 지나치게 걱정했다",
      "편히 쉬기 어려웠다",
      "가만히 있기 어려웠다",
      "쉽게 짜증이 났다",
      "나쁜 일이 생길 것 같은 두려움이 있었다",
    ],
    lightItemIdx: [0, 6],
    scaleOptions: [
      { label: "전혀 없음", score: 0 },
      { label: "며칠 있음", score: 1 },
      { label: "일주일 이상", score: 2 },
      { label: "거의 매일", score: 3 },
    ],
    levels: [
      { max: 4, label: "낮음" },
      { max: 9, label: "경미" },
      { max: 14, label: "중간" },
      { max: Infinity, label: "높음" },
    ],
    analysis: (level) =>
      level === "높음"
        ? "불안 영역이 높게 나타납니다. 연애에서는 상대의 답장 지연, 말투 변화, 약속 변경을 실제보다 부정적으로 해석할 가능성이 있습니다. 확인 연락이 늘어나거나, 반대로 상처받기 전에 먼저 거리를 두는 행동으로 나타날 수 있습니다."
        : level === "중간"
        ? "긴장·걱정이 관계에 영향을 줄 수 있는 수준입니다."
        : "불안 영역은 비교적 안정적으로 보입니다.",
  },
  ocd: {
    label: "강박 영역",
    title: "강박 영역 체크",
    intro: "강박이 높으면 특정 생각을 떨치기 어렵고, 확인 행동이 반복되거나, 관계에서 완벽한 확신을 요구할 수 있습니다.",
    timeframe: "최근 한 달 동안",
    items: [
      "원치 않는 생각이 반복적으로 떠올라 괴로웠다",
      "확인하지 않으면 불안해서 반복적으로 확인했다",
      "오염, 청결, 정리, 순서, 숫자 등에 과하게 신경 썼다",
      "상대의 말이나 행동을 반복해서 되짚었다",
      "확신이 들 때까지 질문하거나 확인하고 싶었다",
      "반복 행동 때문에 시간이 많이 소모됐다",
      "이런 생각이나 행동이 관계에 영향을 줬다",
    ],
    lightItemIdx: [1, 4],
    scaleOptions: [
      { label: "전혀 없음", score: 0 },
      { label: "가끔 있음", score: 1 },
      { label: "자주 있음", score: 2 },
      { label: "매우 자주 있음", score: 3 },
    ],
    levels: [
      { max: 5, label: "낮음" },
      { max: 10, label: "주의" },
      { max: 15, label: "높음" },
      { max: Infinity, label: "매우 높음" },
    ],
    analysis: (level) =>
      level === "높음" || level === "매우 높음"
        ? "강박적 확인 패턴이 높게 나타납니다. 연애에서는 상대의 마음을 확실히 알고 싶어 반복 질문을 하거나, 카톡과 SNS를 계속 확인하는 방식으로 나타날 수 있습니다. 관계가 불확실할수록 안심을 요구하는 행동이 늘어날 수 있습니다."
        : level === "주의"
        ? "확인 행동이 관계 안에서 가끔 반복될 수 있는 수준입니다."
        : "강박 영역은 비교적 안정적으로 보입니다.",
  },
  adhd: {
    label: "ADHD 영역",
    title: "집중·실행 영역 체크",
    intro: "이 영역이 높으면 답장을 까먹거나, 약속 시간을 놓치거나, 감정이 빠르게 올라오고, 관계 초반에는 몰입했다가 지속력이 떨어지는 패턴이 생길 수 있습니다.",
    timeframe: "최근 6개월 동안",
    items: [
      "해야 할 일을 시작하기 어렵다",
      "세부적인 일을 자주 놓친다",
      "집중이 오래 유지되지 않는다",
      "정리정돈이나 일정관리가 어렵다",
      "약속이나 답장을 잊는 일이 있다",
      "충동적으로 말하거나 행동한다",
      "감정이 빠르게 올라왔다가 식는다",
      "흥미 있는 것에는 과몰입하지만 아닌 것은 미룬다",
    ],
    lightItemIdx: [4, 2],
    scaleOptions: [
      { label: "거의 없음", score: 0 },
      { label: "가끔 있음", score: 1 },
      { label: "자주 있음", score: 2 },
      { label: "매우 자주 있음", score: 3 },
    ],
    levels: [
      { max: 7, label: "낮음" },
      { max: 13, label: "주의" },
      { max: 18, label: "높음" },
      { max: Infinity, label: "매우 높음" },
    ],
    analysis: (level) =>
      level === "높음" || level === "매우 높음"
        ? "집중·실행 조절 영역이 높게 나타납니다. 연애에서는 마음이 없어서가 아니라 답장이나 약속을 놓치는 방식으로 오해가 생길 수 있습니다. 초반에는 강하게 몰입하지만, 관계가 안정되면 자극이 줄어들어 상대가 관심이 식었다고 느낄 수 있습니다."
        : level === "주의"
        ? "일정·연락 관리가 가끔 흔들릴 수 있는 수준입니다."
        : "집중·실행 영역은 비교적 안정적으로 보입니다.",
  },
  insomnia: {
    label: "불면 영역",
    title: "수면 영역 체크",
    intro: "불면이 높으면 감정조절, 피로, 데이트 지속력, 예민함, 연락 패턴에 직접 영향을 줍니다.",
    timeframe: "최근 2주~1개월 동안",
    items: [
      "잠들기 어렵다",
      "자다가 자주 깬다",
      "너무 일찍 깨고 다시 잠들기 어렵다",
      "잠을 자도 개운하지 않다",
      "수면 문제 때문에 낮에 피곤하다",
      "수면 때문에 감정이 예민해졌다",
      "수면 문제로 약속이나 연락이 흔들렸다",
    ],
    lightItemIdx: [0, 4],
    scaleOptions: [
      { label: "전혀 없음", score: 0 },
      { label: "약간 있음", score: 1 },
      { label: "중간 정도", score: 2 },
      { label: "심함", score: 3 },
      { label: "매우 심함", score: 4 },
    ],
    levels: [
      { max: 7, label: "낮음" },
      { max: 14, label: "주의" },
      { max: 21, label: "높음" },
      { max: Infinity, label: "매우 높음" },
    ],
    analysis: (level) =>
      level === "높음" || level === "매우 높음"
        ? "수면 문제가 관계에 영향을 줄 가능성이 있습니다. 연락이 늦어지거나, 데이트 중 쉽게 지치거나, 작은 갈등에도 예민하게 반응할 수 있습니다."
        : level === "주의"
        ? "수면의 질이 컨디션에 영향을 줄 수 있는 수준입니다."
        : "수면 영역은 비교적 안정적으로 보입니다.",
  },
  panic: {
    label: "공황 영역",
    title: "공황 영역 체크",
    intro: "공황이 높으면 사람이 많은 장소, 지하철, 영화관, 술자리, 장거리 이동, 갑작스러운 데이트 일정에서 회피가 생길 수 있습니다.",
    timeframe: "최근 한 달 동안",
    items: [
      "갑자기 심장이 빠르게 뛰거나 숨이 막히는 느낌이 있었다",
      "죽을 것 같거나 통제력을 잃을 것 같은 공포를 느꼈다",
      "어지러움, 손발 저림, 가슴 답답함, 식은땀이 있었다",
      "다시 그 증상이 올까 봐 걱정했다",
      "특정 장소나 상황을 피하게 됐다",
      "데이트나 약속 중 증상이 올까 봐 부담을 느꼈다",
      "증상 때문에 이동, 외출, 사람 만남이 줄었다",
    ],
    lightItemIdx: [0, 4],
    scaleOptions: [
      { label: "없음", score: 0 },
      { label: "약하게 있음", score: 1 },
      { label: "중간 정도 있음", score: 2 },
      { label: "심하게 있음", score: 3 },
      { label: "매우 심함", score: 4 },
    ],
    levels: [
      { max: 5, label: "낮음" },
      { max: 10, label: "주의" },
      { max: 17, label: "높음" },
      { max: Infinity, label: "매우 높음" },
    ],
    analysis: (level) =>
      level === "높음" || level === "매우 높음"
        ? "공황 관련 반응이 높게 나타납니다. 연애에서는 특정 장소나 상황을 피하게 되면서 상대가 관심 부족이나 약속 회피로 오해할 수 있습니다. 데이트 장소 선택과 이동 방식, 갑작스러운 일정 변경에 대한 부담을 미리 조율하는 것이 중요합니다."
        : level === "주의"
        ? "특정 상황에서의 긴장이 데이트에 영향을 줄 수 있는 수준입니다."
        : "공황 영역은 비교적 안정적으로 보입니다.",
  },
};

export function buildScaleStep(domain: MentalHealthDomain, light: boolean): ScaleQuestionnaireStep {
  const def = domainDefinitions[domain];
  const items = light ? def.lightItemIdx.map((i) => def.items[i]) : def.items;
  return {
    kind: "scale",
    id: `scale_${domain}_${light ? "light" : "full"}`,
    section: light ? "감정·컨디션 간이 체크" : "감정·컨디션 세부 체크",
    domain,
    title: def.title,
    intro: def.intro,
    timeframe: def.timeframe,
    items,
    scaleOptions: def.scaleOptions,
    light,
  };
}

export const bipolarSignalStep: SingleChoiceStep = {
  kind: "single",
  id: "moodSwingSignal",
  section: "감정기복 신호",
  question: "과거에 아래 상태가 며칠 이상 지속된 적이 있나요? (가장 가까운 것 하나)",
  help: "감정 에너지의 급격한 상승·하강 신호를 가볍게 확인하는 질문입니다.",
  options: [
    { label: "잠을 적게 자도 피곤하지 않고 말이 평소보다 많아졌다", value: "고양감", tags: { moodSwingRisk: 60 } },
    { label: "생각이 너무 빠르게 이어지고 자신감이 지나치게 올라갔다", value: "생각 질주", tags: { moodSwingRisk: 60 } },
    { label: "돈, 관계, 일에서 충동적인 선택이 늘고 이후 크게 후회했다", value: "충동 후회", tags: { moodSwingRisk: 70 } },
    { label: "해당 없음", value: "없음" },
  ],
};

export const crisisStep: CrisisCheckStep = {
  kind: "crisis",
  id: "crisisCheck",
  section: "위기 위험 확인",
  question: "최근 스스로를 해치고 싶거나 사라지고 싶다는 생각이 있었나요?",
  options: [
    { label: "전혀 없음", value: "전혀 없음", risk: "none" },
    { label: "생각만 스친 적 있음", value: "생각만 스침", risk: "low" },
    { label: "반복적으로 생각함", value: "반복적으로 생각", risk: "mid" },
    { label: "방법을 생각해본 적 있음", value: "방법을 생각해봄", risk: "high" },
    { label: "구체적 계획이 있음", value: "구체적 계획", risk: "danger" },
    { label: "지금 위험함", value: "지금 위험함", risk: "danger" },
  ],
};
