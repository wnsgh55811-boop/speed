export type SignalKey =
  | "contactSensitivity"
  | "attachmentAnxiety"
  | "avoidance"
  | "envRestriction"
  | "familyInfluence"
  | "oppositeFriendConfusion"
  | "moodSwingRisk"
  | "depression"
  | "anxiety"
  | "ocd"
  | "adhd"
  | "insomnia"
  | "panic";

export interface ResultType {
  id: string;
  name: string;
  tagline: string;
  description: string;
  weights: Partial<Record<SignalKey, number>>;
  coreCauses: string[];
  goodMatch: string[];
  badMatch: string[];
  actionGuide: { label: string; text: string }[];
}

export const resultTypes: ResultType[] = [
  {
    id: "opportunity-scarce",
    name: "기회 부족형",
    tagline: "사람을 만날 환경 자체가 좁은 유형",
    description:
      "생활반경과 만남 경로가 좁아 연애가 시작될 기회 자체가 적은 상태입니다. 성격이나 매력의 문제가 아니라 구조적으로 사람을 만날 접점이 부족한 경우가 많습니다.",
    weights: { envRestriction: 0.7, avoidance: 0.3 },
    coreCauses: ["관계환경", "생활리듬", "경제/시간환경"],
    goodMatch: ["새로운 만남 경로를 함께 시도해보려는 사람", "여유 있는 페이스로 관계를 쌓는 사람"],
    badMatch: ["빠른 진전을 강하게 요구하는 사람", "약속을 자주 즉흥적으로 잡는 사람"],
    actionGuide: [
      { label: "환경 확장", text: "한 달에 새로운 사람을 만날 수 있는 접점을 1개만 늘려보세요. 동아리, 모임, 소개 요청 중 부담이 적은 것부터 시작합니다." },
      { label: "에너지 배분", text: "생활 리듬이 안정되는 요일을 정해 그 시간만큼은 만남에 열어두는 방식이 효과적입니다." },
    ],
  },
  {
    id: "overinterpret-contact",
    name: "연락 과해석형",
    tagline: "답장, 말투, SNS 반응을 빠르게 의미화하는 유형",
    description:
      "상대의 연락 속도나 말투 변화를 실제보다 더 크게 해석하는 경향이 있습니다. 확인받고 싶은 마음이 커서 연락 자체가 관계의 안정감을 좌우하게 됩니다.",
    weights: { contactSensitivity: 0.6, attachmentAnxiety: 0.4 },
    coreCauses: ["연락성향", "애착반응"],
    goodMatch: ["연락 패턴을 미리 설명해주는 사람", "일관된 리듬으로 답장하는 사람"],
    badMatch: ["답장을 자주 미루면서 설명하지 않는 사람", "연락에 무심한 태도를 보이는 사람"],
    actionGuide: [
      { label: "연락 가이드", text: "“바쁘면 나중에 답해도 괜찮아. 다만 오늘 안에만 짧게 말해주면 좋겠어.” 같은 문장으로 기준을 먼저 공유해보세요." },
      { label: "해석 늦추기", text: "답장이 늦을 때 바로 의미를 해석하지 않고 30분 정도 텀을 두는 연습이 도움이 됩니다." },
    ],
  },
  {
    id: "avoidant-distancer",
    name: "회피성 거리두기형",
    tagline: "가까워질수록 부담을 느끼고 연락이나 만남을 줄이는 유형",
    description:
      "관계가 안정될수록 오히려 혼자 있고 싶은 마음이 커지는 유형입니다. 감정이 없어서가 아니라 친밀감 자체가 부담으로 느껴지는 경우가 많습니다.",
    weights: { avoidance: 0.8, envRestriction: 0.2 },
    coreCauses: ["애착반응", "관계환경"],
    goodMatch: ["속도를 강요하지 않는 사람", "혼자만의 시간을 존중하는 사람"],
    badMatch: ["갈등이 생기면 잠수타는 사람", "거리를 둘 때마다 강하게 추궁하는 사람"],
    actionGuide: [
      { label: "컨디션 설명 가이드", text: "“내가 컨디션이 안 좋을 때 답장이 느려질 수 있는데, 마음이 식어서 그런 건 아니야.” 라고 미리 말해두면 오해를 줄일 수 있습니다." },
      { label: "작은 신호 남기기", text: "완전히 잠수타기 전에 짧게라도 상황을 알리는 습관을 만들어보세요." },
    ],
  },
  {
    id: "low-energy-depressive",
    name: "우울 저에너지형",
    tagline: "감정과 에너지가 떨어져 연락, 데이트, 관계 유지가 부담되는 유형",
    description:
      "기분과 에너지 저하가 연애 전반에 영향을 주는 유형입니다. 관심이 없는 것이 아니라 관계를 유지할 에너지 자체가 부족한 상태일 수 있습니다.",
    weights: { depression: 0.75, avoidance: 0.25 },
    coreCauses: ["감정/컨디션", "생활리듬"],
    goodMatch: ["재촉하지 않고 기다려주는 사람", "작은 반응에도 의미를 알아주는 사람"],
    badMatch: ["감정 기복을 공격적으로 받아들이는 사람", "무기력함을 애정 부족으로 단정하는 사람"],
    actionGuide: [
      { label: "컨디션 공유", text: "“요즘 기분이 가라앉아서 표현이 적을 수 있는데, 너 때문이 아니야.” 라고 먼저 설명해보세요." },
      { label: "작은 목표", text: "매일 연락하기보다 하루 한 번, 짧은 문장이라도 보내는 최소 목표를 세워보세요." },
    ],
  },
  {
    id: "anxious-reassurance",
    name: "불안 확인형",
    tagline: "상대의 마음을 확인받아야 안정되는 유형",
    description:
      "관계의 확신이 있어야 안정감을 느끼는 유형입니다. 확신이 부족하면 불안이 커지고, 반복적으로 마음을 확인하려는 행동으로 이어질 수 있습니다.",
    weights: { attachmentAnxiety: 0.65, anxiety: 0.35 },
    coreCauses: ["애착반응", "감정/컨디션"],
    goodMatch: ["애정 표현을 자주, 명확히 하는 사람", "갈등을 회피하지 않는 사람"],
    badMatch: ["애매한 태도를 유지하는 사람", "확인 요청을 집착으로 치부하는 사람"],
    actionGuide: [
      { label: "갈등 가이드", text: "“네가 잘못했다는 뜻은 아니고, 나는 이 상황에서 조금 불안해졌어.” 라는 문장으로 감정을 먼저 설명해보세요." },
      { label: "확인 텀 두기", text: "확인하고 싶은 마음이 들 때, 바로 연락하기 전에 스스로 이유를 적어보는 습관이 도움이 됩니다." },
    ],
  },
  {
    id: "adhd-execution",
    name: "ADHD 실행흔들림형",
    tagline: "마음은 있지만 답장, 약속, 일정관리에서 오해가 생기는 유형",
    description:
      "집중과 실행 조절이 흔들려 답장이나 약속을 놓치는 유형입니다. 관심이 없어서가 아니라 일정 관리 자체가 어려운 경우가 많습니다.",
    weights: { adhd: 0.8, moodSwingRisk: 0.2 },
    coreCauses: ["연락성향", "감정/컨디션"],
    goodMatch: ["일정을 함께 챙겨주는 사람", "놓친 것에 유연하게 반응하는 사람"],
    badMatch: ["사소한 실수를 애정 문제로 확대 해석하는 사람", "빡빡한 일정 관리를 강하게 요구하는 사람"],
    actionGuide: [
      { label: "구조 만들기", text: "중요한 약속은 캘린더 알림으로 이중 확인하는 습관을 만들어보세요." },
      { label: "미리 설명하기", text: "“나는 가끔 답장이나 약속을 깜빡할 수 있어. 놓치면 바로 말해줘.” 라고 미리 공유해두면 오해가 줄어듭니다." },
    ],
  },
  {
    id: "insomnia-sensitive",
    name: "불면 예민형",
    tagline: "수면 문제로 감정조절과 관계 지속력이 흔들리는 유형",
    description:
      "수면의 질이 떨어지면서 감정 기복, 피로, 예민함이 관계에 영향을 주는 유형입니다.",
    weights: { insomnia: 0.75, moodSwingRisk: 0.25 },
    coreCauses: ["감정/컨디션", "생활리듬"],
    goodMatch: ["컨디션 기복을 자연스럽게 받아들이는 사람", "늦은 답장에 유연한 사람"],
    badMatch: ["즉각적인 반응을 강하게 요구하는 사람", "피곤함을 무시하고 일정을 강행하는 사람"],
    actionGuide: [
      { label: "컨디션 설명 가이드", text: "“내가 컨디션이 안 좋을 때 답장이 느려질 수 있는데, 마음이 식어서 그런 건 아니야.”" },
      { label: "수면 루틴", text: "데이트 전날은 일정을 가볍게 조정해 수면 리듬을 지키는 것이 관계 지속에도 도움이 됩니다." },
    ],
  },
  {
    id: "panic-avoidant",
    name: "공황 회피형",
    tagline: "특정 장소, 상황, 이동, 데이트 환경이 부담이 되는 유형",
    description:
      "특정 장소나 갑작스러운 일정이 신체적 공포 반응을 일으켜 회피로 이어지는 유형입니다.",
    weights: { panic: 0.85, anxiety: 0.15 },
    coreCauses: ["감정/컨디션", "관계환경"],
    goodMatch: ["데이트 장소를 미리 조율해주는 사람", "갑작스러운 일정 변경에 유연한 사람"],
    badMatch: ["회피를 관심 부족으로 오해하는 사람", "즉흥적인 장거리 일정을 자주 잡는 사람"],
    actionGuide: [
      { label: "장소 조율", text: "데이트 장소와 이동 방식을 미리 상의하고, 부담되는 상황은 대안을 함께 정해두세요." },
      { label: "미리 알리기", text: "“특정 장소에서 긴장이 심해질 수 있어, 그럴 땐 잠깐 나갔다 올게.” 라고 미리 말해두면 서로 편해집니다." },
    ],
  },
  {
    id: "ocd-checking",
    name: "강박 확인형",
    tagline: "상대 마음, 말, 카톡, SNS를 반복 확인하는 유형",
    description:
      "확신이 들 때까지 반복적으로 확인하는 패턴이 관계에 영향을 주는 유형입니다.",
    weights: { ocd: 0.7, attachmentAnxiety: 0.3 },
    coreCauses: ["감정/컨디션", "연락성향"],
    goodMatch: ["같은 질문에도 안정적으로 답해주는 사람", "확인 행동을 비난하지 않는 사람"],
    badMatch: ["확인 자체를 집착으로 단정하는 사람", "모호한 답변을 반복하는 사람"],
    actionGuide: [
      { label: "확인 대체 행동", text: "확인하고 싶은 충동이 들 때 5분만 다른 행동으로 전환해보는 연습이 도움이 됩니다." },
      { label: "솔직한 공유", text: "“확실해질 때까지 물어보고 싶어지는 편이야” 라고 미리 알려두면 상대도 이해하기 쉬워집니다." },
    ],
  },
  {
    id: "family-security-seeker",
    name: "가족영향 안정추구형",
    tagline: "가족환경 때문에 안정적인 관계를 강하게 원하는 유형",
    description:
      "가족환경의 영향으로 갈등 없는, 예측 가능한 관계를 강하게 원하게 된 유형입니다. 작은 갈등에도 관계 자체를 의심하게 될 수 있습니다.",
    weights: { familyInfluence: 0.8, attachmentAnxiety: 0.2 },
    coreCauses: ["가족환경", "애착반응"],
    goodMatch: ["갈등을 자연스러운 과정으로 받아들이는 사람", "일관된 태도를 보이는 사람"],
    badMatch: ["감정 기복이 심하고 예측 불가능한 사람", "약속을 자주 어기는 사람"],
    actionGuide: [
      { label: "기대 조율", text: "완벽하게 갈등 없는 관계보다, 갈등을 잘 풀어가는 관계가 더 안정적이라는 것을 함께 확인해보세요." },
      { label: "가족 이야기 나누기", text: "부담되지 않는 선에서 가족환경이 연애관에 미친 영향을 상대에게 조금씩 공유해보세요." },
    ],
  },
  {
    id: "boundary-confusion",
    name: "이성친구 경계혼란형",
    tagline: "친구와 썸, 애인과 이성친구 기준이 불명확해 갈등이 생기는 유형",
    description:
      "이성친구 관계의 기준이 스스로도 애매해 관계 정의나 신뢰 문제로 갈등이 반복되는 유형입니다.",
    weights: { oppositeFriendConfusion: 0.85, attachmentAnxiety: 0.15 },
    coreCauses: ["관계환경", "신뢰 문제"],
    goodMatch: ["기준을 먼저 이야기하고 조율하려는 사람", "투명하게 관계를 공유하는 사람"],
    badMatch: ["기준 이야기를 회피하는 사람", "설명 없이 이성 관계를 유지하는 사람"],
    actionGuide: [
      { label: "기준 먼저 말하기", text: "이성친구에 대한 서로의 기준을 관계 초반에 구체적으로 이야기해보세요." },
      { label: "투명성", text: "애매한 상황일수록 먼저 설명하는 것이 신뢰를 쌓는 데 더 효과적입니다." },
    ],
  },
  {
    id: "mood-swing-highrisk",
    name: "감정기복 고위험형",
    tagline: "관계 초반 몰입과 후반 급격한 거리두기가 반복되는 유형",
    description:
      "감정 에너지의 급격한 상승과 하강이 반복되는 유형입니다. 관계 초반에는 강하게 몰입하지만 이후 급격히 가라앉거나 거리를 두게 될 수 있습니다.",
    weights: { moodSwingRisk: 0.75, attachmentAnxiety: 0.25 },
    coreCauses: ["감정/컨디션", "애착반응"],
    goodMatch: ["기복을 있는 그대로 받아들이는 사람", "일정한 거리에서 지켜봐주는 사람"],
    badMatch: ["기복에 똑같이 감정적으로 반응하는 사람", "고양된 감정을 이용하려는 사람"],
    actionGuide: [
      { label: "전문가 병행", text: "감정 에너지의 급격한 상승과 하강이 보고되었습니다. 일반적인 연애 코칭보다 전문가 상담이나 진료와 병행하는 것이 안전할 수 있습니다." },
      { label: "패턴 기록", text: "감정이 크게 올라가거나 내려가는 시점을 기록해두면 스스로 패턴을 알아차리는 데 도움이 됩니다." },
    ],
  },
];
