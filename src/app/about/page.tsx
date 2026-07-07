import type { Metadata } from "next";
import { Container } from "@/components/Container";
import { SectionHeading } from "@/components/SectionHeading";
import { Button } from "@/components/Button";
import { site } from "@/lib/site";

export const metadata: Metadata = {
  title: "러브백 소개",
  description: "러브백 관계 연구소의 철학과 코치 소개.",
};

const credentials = [
  `누적 ${site.statsCases}건 이상 연애·재회 상담 분석`,
  `${site.statsYears}년간 연애, 이별, 재회 케이스 연구`,
  "연애 심리, 애착 유형, 관계 패턴 기반 상담",
  "카톡 대화, 이별 과정, 상대 반응 분석",
  "재회 가능성 및 실행 전략 설계",
];

export default function AboutPage() {
  return (
    <div>
      <section className="border-b border-warmgray-200 bg-navy-950 py-16 text-ivory-50 sm:py-20">
        <Container className="flex flex-col items-center gap-4 text-center">
          <span className="text-xs font-semibold tracking-[0.2em] text-ivory-100/70 uppercase">
            About Loveback
          </span>
          <h1 className="font-serif-kr max-w-2xl text-3xl leading-snug font-medium sm:text-4xl">
            연애도 결국, 남녀 간의 인간관계입니다.
          </h1>
        </Container>
      </section>

      <section className="bg-ivory-50 py-20">
        <Container className="flex flex-col gap-8">
          <SectionHeading align="left" eyebrow="철학" title="러브백이 보는 관점" />
          <div className="grid gap-6 md:grid-cols-2">
            <div className="space-y-4 text-base leading-relaxed text-navy-800">
              <p>
                러브백은 단순히 “언제 연락해야 하나요?”, “카톡 뭐라고 보내야
                하나요?”만 보는 곳이 아닙니다.
              </p>
              <p>
                관계가 어디서 틀어졌는지, 상대는 지금 어떤 심리 상태인지, 내가
                어떤 위치에 서 있는지, 이 관계를 계속 회복할 수 있는지부터
                봅니다.
              </p>
            </div>
            <div className="space-y-4 rounded-sm border border-warmgray-200 bg-beige-100 p-6 text-base leading-relaxed text-navy-800">
              <p>
                연락은 기술이 아니라 결과물입니다. 관계의 흐름이 정리되지
                않은 상태에서 보내는 연락은 오히려 상대를 더 멀어지게 만들
                수 있습니다.
              </p>
              <p className="font-medium text-burgundy-700">
                그래서 러브백은 연락 문장보다, 관계의 흐름을 먼저 봅니다.
              </p>
            </div>
          </div>
        </Container>
      </section>

      <section className="bg-navy-900 py-20 text-ivory-50">
        <Container className="flex flex-col gap-10">
          <SectionHeading
            align="left"
            eyebrow="코치 소개"
            title={`${site.coachName} 코치`}
            light
          />
          <div className="grid gap-10 md:grid-cols-[1fr_1.2fr]">
            <div className="space-y-4 leading-relaxed text-ivory-100/85">
              <p>안녕하세요. 러브백 관계 연구소의 {site.coachName} 코치입니다.</p>
              <p>
                저는 지난 {site.statsYears}년간 {site.statsCases}건 이상의
                연애, 이별, 재회 사례를 분석하며 사람들이 관계 안에서 왜
                같은 방식으로 무너지고, 왜 같은 방식으로 붙잡고, 왜 같은
                방식으로 상처받는지를 봐왔습니다.
              </p>
              <p>
                러브백은 단순히 “상대를 다시 돌아오게 만드는 말”을
                알려드리는 곳이 아닙니다. 관계가 무너진 이유, 상대가 멀어진
                심리, 내가 반복한 행동 패턴, 그리고 지금 상황에서 가능한
                선택지를 함께 분석합니다.
              </p>
            </div>
            <div>
              <h3 className="mb-4 text-sm font-semibold tracking-wide text-ivory-100/60 uppercase">
                전문성 근거
              </h3>
              <ul className="space-y-3">
                {credentials.map((c) => (
                  <li
                    key={c}
                    className="rounded-sm border border-ivory-100/15 px-5 py-4 text-sm leading-relaxed text-ivory-50 sm:text-base"
                  >
                    {c}
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </Container>
      </section>

      <section className="bg-beige-100 py-20">
        <Container className="flex flex-col items-center gap-6 text-center">
          <p className="font-serif-kr max-w-2xl text-xl leading-relaxed text-navy-900 sm:text-2xl">
            연애는 감정의 문제처럼 보이지만, 깊이 들어가면 결국 관계를
            대하는 태도와 패턴의 문제입니다.
          </p>
          <p className="max-w-xl text-warmgray-600">
            러브백은 당신이 지금 이 관계에서 무엇을 해야 하고, 무엇을
            멈춰야 하며, 어떤 기준으로 움직여야 하는지 함께 정리합니다.
          </p>
          <Button href="/apply" size="lg">
            상담 신청하기
          </Button>
        </Container>
      </section>
    </div>
  );
}
