import type { Metadata } from "next";
import { Container } from "@/components/Container";
import { SectionHeading } from "@/components/SectionHeading";
import { Button } from "@/components/Button";

export const metadata: Metadata = {
  title: "상담 프로그램",
  description: "러브백 1:1 상담 프로그램 진행 방식과 상담 분야 안내.",
};

const steps = [
  {
    n: "01",
    title: "사전 상담지 작성",
    body: "상담 전 현재 상황, 관계 흐름, 이별 원인, 대화 내용, 상대 반응 등을 작성합니다.",
  },
  {
    n: "02",
    title: "관계 흐름 분석",
    body: "단순히 사건만 보는 것이 아니라 관계가 어떤 단계에서 무너졌는지 분석합니다.",
  },
  {
    n: "03",
    title: "상대 심리 분석",
    body: "상대가 왜 멀어졌는지, 지금 어떤 감정 상태인지, 어떤 접근에는 저항이 생기는지 봅니다.",
  },
  {
    n: "04",
    title: "내 패턴 진단",
    body: "내가 어떤 방식으로 관계를 밀거나 당겼는지, 불안·회피·집착·통제·과잉배려 패턴이 있었는지 봅니다.",
  },
  {
    n: "05",
    title: "실행 전략 제시",
    body: "연락 여부, 연락 시점, 메시지 방향, 대화 방식, 기다림의 기준, 관계 회복 루트를 정리합니다.",
  },
  {
    n: "06",
    title: "상담 후 정리",
    body: "상담 후 핵심 방향과 실행 가이드를 정리해 혼자서도 다시 흐름을 잡을 수 있게 합니다.",
  },
];

const categories = [
  {
    id: "dating",
    title: "연애 상담",
    audience: [
      "썸에서 관계가 애매해진 사람",
      "연애 중 상대가 식은 것 같은 사람",
      "불안형, 회피형 패턴으로 반복되는 사람",
      "연락, 표현, 서운함 문제로 자주 싸우는 사람",
    ],
    quote: "지금 관계가 어디서 꼬였는지, 어떤 순서로 풀어야 하는지 진단합니다.",
  },
  {
    id: "reunion",
    title: "재회 상담",
    audience: [
      "이별 후 연락 타이밍을 고민하는 사람",
      "차단/읽씹/무반응 상태인 사람",
      "마지막 연락을 어떻게 해야 할지 모르는 사람",
      "재회 가능성과 방향성을 알고 싶은 사람",
    ],
    quote: "재회는 감정으로 밀어붙이는 것이 아니라 상대의 심리적 저항을 낮추는 과정입니다.",
  },
  {
    id: "pattern",
    title: "관계 패턴 진단",
    audience: [
      "연애할 때마다 비슷하게 무너지는 사람",
      "항상 내가 더 불안해지는 사람",
      "상대에게 맞추다가 지치는 사람",
      "사랑받고 싶은데 오히려 매달리게 되는 사람",
    ],
    quote: "반복되는 연애 문제는 상대만의 문제가 아니라 내 관계 패턴에서 시작되는 경우가 많습니다.",
  },
];

export default function ProgramsPage() {
  return (
    <div>
      <section className="border-b border-warmgray-200 bg-navy-950 py-16 text-ivory-50 sm:py-20">
        <Container className="flex flex-col items-center gap-4 text-center">
          <span className="text-xs font-semibold tracking-[0.2em] text-ivory-100/70 uppercase">
            Programs
          </span>
          <h1 className="font-serif-kr max-w-2xl text-3xl leading-snug font-medium sm:text-4xl">
            러브백 1:1 상담 프로그램
          </h1>
          <p className="max-w-xl text-ivory-100/75">
            상담은 감으로 진행되지 않습니다. 아래 6단계 흐름으로 관계를
            구조적으로 분석합니다.
          </p>
        </Container>
      </section>

      <section className="bg-ivory-50 py-20">
        <Container className="flex flex-col gap-6">
          {steps.map((s) => (
            <div
              key={s.n}
              className="flex flex-col gap-3 rounded-sm border border-warmgray-200 bg-white p-6 sm:flex-row sm:items-start sm:gap-8 sm:p-8"
            >
              <span className="font-serif-kr shrink-0 text-3xl text-burgundy-600 sm:text-4xl">
                {s.n}
              </span>
              <div className="space-y-1">
                <h3 className="text-lg font-semibold text-navy-900 sm:text-xl">
                  Step {Number(s.n)}. {s.title}
                </h3>
                <p className="leading-relaxed text-warmgray-600">{s.body}</p>
              </div>
            </div>
          ))}
        </Container>
      </section>

      <section className="bg-beige-100 py-20">
        <Container className="flex flex-col gap-12">
          <SectionHeading eyebrow="상담 분야" title="내 상황에 맞는 상담 분야를 확인하세요" />
          <div className="flex flex-col gap-8">
            {categories.map((c) => (
              <div
                key={c.id}
                id={c.id}
                className="scroll-mt-20 rounded-sm border border-warmgray-300/60 bg-white p-8"
              >
                <h3 className="font-serif-kr mb-4 text-xl font-medium text-navy-900 sm:text-2xl">
                  {c.title}
                </h3>
                <p className="mb-4 text-sm font-semibold tracking-wide text-warmgray-500 uppercase">
                  대상
                </p>
                <ul className="mb-6 grid gap-2 text-navy-800 sm:grid-cols-2">
                  {c.audience.map((a) => (
                    <li key={a}>· {a}</li>
                  ))}
                </ul>
                <p className="border-t border-warmgray-200 pt-4 font-medium text-burgundy-700">
                  {c.quote}
                </p>
              </div>
            ))}
          </div>
        </Container>
      </section>

      <section className="bg-navy-900 py-20 text-ivory-50">
        <Container className="flex flex-col items-center gap-6 text-center">
          <h2 className="font-serif-kr text-2xl font-medium sm:text-3xl">
            내게 맞는 상담 상품과 가격이 궁금하다면
          </h2>
          <Button href="/pricing" size="lg">
            가격 안내 보기
          </Button>
        </Container>
      </section>
    </div>
  );
}
