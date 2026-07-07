export type DiagnosisQuestion = {
  text: string;
};

export type ResultBand = {
  min: number;
  max: number;
  title: string;
  description: string;
  recommendedProgram: "DATING" | "REUNION" | "PREMIUM";
};

export type Diagnosis = {
  slug: string;
  title: string;
  description: string;
  questions: DiagnosisQuestion[];
  bands: ResultBand[];
};

export const diagnoses: Diagnosis[] = [
  {
    slug: "contact-possibility",
    title: "이별 후 연락 가능성 체크",
    description: "지금 연락을 시도해도 괜찮은 상황인지 가볍게 점검해보세요.",
    questions: [
      { text: "이별한 지 2주 이상 지났다." },
      { text: "이별 당시 서로 큰 소리를 내거나 감정적으로 격했다." },
      { text: "이별 후 상대에게 연락을 한 적이 없다." },
      { text: "상대가 나를 차단하거나 완전히 무반응 상태는 아니다." },
      { text: "이별 이후 내 감정이 어느 정도 진정된 상태다." },
      { text: "상대의 SNS 등에서 특별히 부정적인 신호가 보이지 않는다." },
      { text: "다시 연락할 명확한 이유나 계기가 있다." },
    ],
    bands: [
      {
        min: 0,
        max: 2,
        title: "지금은 연락보다 정리가 먼저인 시기입니다",
        description:
          "아직 감정이 정리되지 않았거나 이별 직후일 가능성이 높습니다. 지금 연락을 시도하면 오히려 상대의 심리적 저항을 키울 수 있습니다. 먼저 상황을 정리하는 것을 권합니다.",
        recommendedProgram: "REUNION",
      },
      {
        min: 3,
        max: 5,
        title: "조건부로 연락을 고려해볼 수 있는 상태입니다",
        description:
          "일부 조건은 갖춰졌지만, 연락 타이밍과 메시지 방향에 따라 결과가 크게 달라질 수 있는 상태입니다. 구체적인 전략 없이 접근하는 것은 위험합니다.",
        recommendedProgram: "REUNION",
      },
      {
        min: 6,
        max: 7,
        title: "연락을 시도해볼 수 있는 조건에 가깝습니다",
        description:
          "여러 조건이 갖춰진 상태입니다. 다만 '가능하다'는 것과 '어떻게 해야 하는가'는 다른 문제입니다. 메시지 방향과 타이밍을 구체적으로 설계해보세요.",
        recommendedProgram: "REUNION",
      },
    ],
  },
  {
    slug: "cooling-signs",
    title: "상대가 식었을 때 나타나는 신호 체크",
    description: "지금 느끼는 불안이 실제 신호인지 확인해보세요.",
    questions: [
      { text: "연락 빈도와 속도가 눈에 띄게 줄었다." },
      { text: "대화 내용이 감정 공유보다 단순 정보 전달 위주로 바뀌었다." },
      { text: "만나는 약속을 상대가 먼저 잡지 않는다." },
      { text: "갈등 상황에서 예전만큼 적극적으로 풀려고 하지 않는다." },
      { text: "미래에 대한 이야기를 꺼리거나 얼버무린다." },
      { text: "스킨십이나 애정 표현이 눈에 띄게 줄었다." },
      { text: "내가 먼저 연락하거나 만나자고 하는 경우가 대부분이다." },
    ],
    bands: [
      {
        min: 0,
        max: 2,
        title: "아직 뚜렷한 신호로 보기는 이릅니다",
        description:
          "일시적인 변화일 가능성이 있습니다. 다만 계속 신경 쓰인다면 관계 흐름을 한 번 점검해보는 것도 도움이 됩니다.",
        recommendedProgram: "DATING",
      },
      {
        min: 3,
        max: 5,
        title: "관계 흐름 점검이 필요한 시점입니다",
        description:
          "몇 가지 신호가 겹쳐 나타나고 있습니다. 감정적으로 대응하기 전에, 정확히 어느 지점에서 흐름이 바뀌었는지 짚어보는 것이 중요합니다.",
        recommendedProgram: "DATING",
      },
      {
        min: 6,
        max: 7,
        title: "구체적인 진단과 전략이 필요합니다",
        description:
          "여러 신호가 동시에 나타나고 있는 상태입니다. 지금 어떤 태도를 취하느냐에 따라 관계의 방향이 크게 달라질 수 있으니, 빠른 진단을 권합니다.",
        recommendedProgram: "DATING",
      },
    ],
  },
  {
    slug: "reunion-risk-actions",
    title: "재회 가능성을 낮추는 행동 체크리스트",
    description: "혹시 나도 모르게 재회 가능성을 낮추는 행동을 하고 있지 않은지 확인해보세요.",
    questions: [
      { text: "이별 후 감정적인 상태에서 연락한 적이 있다." },
      { text: "SNS에 상대가 볼 만한 의미심장한 게시물을 올린 적이 있다." },
      { text: "공통 지인을 통해 상대의 근황을 자주 확인한다." },
      { text: "상대의 SNS를 하루에도 여러 번 확인한다." },
      { text: "장문의 메시지를 보내 내 감정을 설명하려 한 적이 있다." },
      { text: "우연을 가장해 상대와 마주치려 시도한 적이 있다." },
      { text: "술을 마신 후 연락한 적이 있다." },
    ],
    bands: [
      {
        min: 0,
        max: 1,
        title: "비교적 안정적으로 대처하고 있습니다",
        description:
          "감정 관리가 잘 되고 있는 편입니다. 지금의 태도를 유지하면서, 다음 단계 전략을 준비해보세요.",
        recommendedProgram: "REUNION",
      },
      {
        min: 2,
        max: 4,
        title: "몇 가지 행동이 재회 가능성을 갉아먹고 있을 수 있습니다",
        description:
          "무심코 한 행동들이 쌓여 상대에게 부담을 주고 있을 가능성이 있습니다. 지금부터라도 방향을 조정하는 것이 중요합니다.",
        recommendedProgram: "REUNION",
      },
      {
        min: 5,
        max: 7,
        title: "현재 행동 패턴을 즉시 점검해야 합니다",
        description:
          "여러 위험 행동이 반복되고 있는 상태입니다. 감정적으로 움직이기 전에 먼저 멈추고, 전문가와 함께 다음 행동을 결정하는 것을 권합니다.",
        recommendedProgram: "REUNION",
      },
    ],
  },
  {
    slug: "anxious-pattern-check",
    title: "불안형 연애 패턴 자가진단",
    description: "연애할 때마다 반복되는 내 패턴을 점검해보세요.",
    questions: [
      { text: "연락이 조금만 늦어져도 불안한 생각이 먼저 든다." },
      { text: "상대의 반응에 따라 내 하루 기분이 크게 좌우된다." },
      { text: "서운한 감정이 생기면 바로 표현해야 마음이 풀린다." },
      { text: "관계에서 확신을 자주 확인받고 싶어한다." },
      { text: "연애할 때마다 비슷한 이유로 갈등이 반복된다." },
      { text: "상대에게 맞추다가 지쳐서 관계를 끝낸 경험이 있다." },
      { text: "사랑받기 위해 애쓰다가 오히려 매달리게 된 적이 있다." },
    ],
    bands: [
      {
        min: 0,
        max: 2,
        title: "비교적 안정적인 관계 패턴을 가지고 있습니다",
        description:
          "큰 불안 패턴은 보이지 않습니다. 다만 특정 상대나 상황에서만 반복된다면, 그 조건을 살펴보는 것도 도움이 됩니다.",
        recommendedProgram: "DATING",
      },
      {
        min: 3,
        max: 5,
        title: "불안형 패턴이 관계에 영향을 주고 있을 가능성이 있습니다",
        description:
          "관계 안에서 확인받고 싶어하는 경향이 반복되고 있을 수 있습니다. 이 패턴을 구조적으로 이해하면 관계가 훨씬 편해질 수 있습니다.",
        recommendedProgram: "PREMIUM",
      },
      {
        min: 6,
        max: 7,
        title: "반복되는 관계 패턴에 대한 진단이 필요합니다",
        description:
          "여러 연애에서 비슷한 이유로 어려움을 겪고 있을 가능성이 높습니다. 상대의 문제가 아니라 내 패턴의 문제일 수 있으니, 근본적인 진단을 권합니다.",
        recommendedProgram: "PREMIUM",
      },
    ],
  },
];

export function getDiagnosisBySlug(slug: string) {
  return diagnoses.find((d) => d.slug === slug);
}

export function getResultBand(diagnosis: Diagnosis, score: number) {
  return (
    diagnosis.bands.find((b) => score >= b.min && score <= b.max) ??
    diagnosis.bands[diagnosis.bands.length - 1]
  );
}
