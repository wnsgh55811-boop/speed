import Link from "next/link";
import { ArrowRight, Check } from "lucide-react";
import { Container } from "@/components/Container";
import { Button } from "@/components/Button";
import { SectionHeading } from "@/components/SectionHeading";
import { ReviewCard } from "@/components/ReviewCard";
import { prisma } from "@/lib/prisma";
import { site } from "@/lib/site";

const painPoints = [
  "상대가 예전 같지 않다.",
  "연락 빈도가 줄었는데 이유를 모르겠다.",
  "내가 뭘 잘못했는지 계속 생각하게 된다.",
  "붙잡아야 할지, 기다려야 할지 모르겠다.",
  "재회를 원하지만 먼저 연락하면 더 멀어질까 봐 두렵다.",
  "연애할 때마다 비슷한 패턴으로 무너진다.",
];

const programs = [
  {
    title: "연애 상담",
    href: "/programs#dating",
    audience: [
      "썸에서 관계가 애매해진 사람",
      "연애 중 상대가 식은 것 같은 사람",
      "불안형, 회피형 패턴으로 반복되는 사람",
      "연락, 표현, 서운함 문제로 자주 싸우는 사람",
    ],
    quote: "지금 관계가 어디서 꼬였는지, 어떤 순서로 풀어야 하는지 진단합니다.",
  },
  {
    title: "재회 상담",
    href: "/programs#reunion",
    audience: [
      "이별 후 연락 타이밍을 고민하는 사람",
      "차단/읽씹/무반응 상태인 사람",
      "마지막 연락을 어떻게 해야 할지 모르는 사람",
      "재회 가능성과 방향성을 알고 싶은 사람",
    ],
    quote: "재회는 감정으로 밀어붙이는 것이 아니라 상대의 심리적 저항을 낮추는 과정입니다.",
  },
  {
    title: "관계 패턴 진단",
    href: "/programs#pattern",
    audience: [
      "연애할 때마다 비슷하게 무너지는 사람",
      "항상 내가 더 불안해지는 사람",
      "상대에게 맞추다가 지치는 사람",
      "사랑받고 싶은데 오히려 매달리게 되는 사람",
    ],
    quote: "반복되는 연애 문제는 상대만의 문제가 아니라 내 관계 패턴에서 시작되는 경우가 많습니다.",
  },
];

const situations = [
  { text: "연애 중인데 불안하다", href: "/programs#dating", target: "연애 상담" },
  { text: "헤어진 지 얼마 안 됐다", href: "/programs#reunion", target: "재회 상담" },
  { text: "연락을 보내야 할지 모르겠다", href: "/programs#reunion", target: "재회 전략 상담" },
  { text: "매번 같은 연애를 반복한다", href: "/programs#pattern", target: "관계 패턴 진단" },
  { text: "카톡을 어떻게 해야 할지 모르겠다", href: "/reviews?category=CHAT_ANALYSIS", target: "카톡 분석 상담" },
];

const differentiators = [
  "연락 문장보다 관계 흐름을 먼저 본다.",
  "감정 위로보다 현실적인 전략을 제시한다.",
  "상대 심리와 내 패턴을 함께 분석한다.",
  "재회 가능성을 무조건 긍정하지 않는다.",
  "상담 후 바로 실행할 수 있는 방향을 준다.",
  "실제 카톡, 이별 과정, 상대 반응을 바탕으로 분석한다.",
];

export default async function Home() {
  const reviews = await prisma.review.findMany({
    where: { status: "APPROVED" },
    orderBy: { createdAt: "desc" },
    take: 3,
  });

  return (
    <div>
      {/* 1. Hero */}
      <section className="border-b border-warmgray-200 bg-navy-950 text-ivory-50">
        <Container className="flex flex-col items-center gap-8 py-20 text-center sm:py-28">
          <span className="rounded-full border border-ivory-100/20 px-4 py-1.5 text-xs tracking-wide text-ivory-100/80">
            누적 {site.statsCases}건 이상 연애·재회 상담 분석
          </span>
          <h1 className="font-serif-kr max-w-3xl text-3xl leading-snug font-medium sm:text-4xl md:text-5xl">
            연락 한 번을 더 보내기 전에,
            <br />
            먼저 관계의 흐름부터 봐야 합니다.
          </h1>
          <p className="max-w-xl text-base leading-relaxed text-ivory-100/75 sm:text-lg">
            러브백 관계 연구소는 연애, 이별, 재회 상황을 감정이 아닌
            관계 패턴과 상대 심리로 분석합니다.
          </p>
          <div className="flex flex-col gap-3 sm:flex-row">
            <Button href="/apply" size="lg">
              상담 신청하기
            </Button>
            <Button href="/reviews" variant="secondary" size="lg" className="border-ivory-100/30 text-ivory-50 hover:bg-ivory-50 hover:text-navy-900">
              후기 먼저 보기
            </Button>
          </div>
        </Container>
      </section>

      {/* 2. Pain point empathy */}
      <section className="bg-ivory-50 py-20">
        <Container className="flex flex-col items-center gap-12">
          <SectionHeading
            eyebrow="Are you here?"
            title="지금 당신이 힘든 이유는 연락 때문만이 아닙니다."
            description="혹시 이런 상황인가요?"
          />
          <div className="grid w-full gap-4 sm:grid-cols-2">
            {painPoints.map((point) => (
              <div
                key={point}
                className="flex items-start gap-3 rounded-sm border border-warmgray-200 bg-white px-5 py-4 text-left"
              >
                <Check size={18} className="mt-0.5 shrink-0 text-burgundy-600" />
                <span className="text-sm leading-relaxed text-navy-800 sm:text-base">
                  {point}
                </span>
              </div>
            ))}
          </div>
        </Container>
      </section>

      {/* 3. Brand philosophy */}
      <section className="bg-navy-900 py-20 text-ivory-50">
        <Container className="flex flex-col items-center gap-8 text-center">
          <SectionHeading
            eyebrow="러브백의 관점"
            title="연애도 결국 남녀 간의 인간관계입니다."
            light
          />
          <div className="max-w-2xl space-y-4 text-base leading-relaxed text-ivory-100/80 sm:text-lg">
            <p>
              러브백은 단순히 “언제 연락해야 하나요?”, “카톡 뭐라고 보내야 하나요?”만
              보는 곳이 아닙니다.
            </p>
            <p>
              관계가 어디서 틀어졌는지, 상대는 지금 어떤 심리 상태인지, 내가 어떤
              위치에 서 있는지, 이 관계를 계속 회복할 수 있는지부터 봅니다.
            </p>
            <p>
              연락은 기술이 아니라 결과물입니다. 관계의 흐름이 정리되지 않은
              상태에서 보내는 연락은 오히려 상대를 더 멀어지게 만들 수 있습니다.
            </p>
          </div>
        </Container>
      </section>

      {/* 4. Program categories */}
      <section className="bg-ivory-50 py-20">
        <Container className="flex flex-col items-center gap-12">
          <SectionHeading
            eyebrow="상담 분야"
            title="지금 상황에 맞는 상담을 찾아보세요"
          />
          <div className="grid w-full gap-6 md:grid-cols-3">
            {programs.map((p) => (
              <Link
                key={p.title}
                href={p.href}
                className="flex h-full flex-col gap-5 rounded-sm border border-warmgray-200 bg-white p-7 transition-shadow hover:shadow-lg"
              >
                <h3 className="font-serif-kr text-xl font-medium text-navy-900">
                  {p.title}
                </h3>
                <ul className="flex-1 space-y-2 text-sm leading-relaxed text-warmgray-600">
                  {p.audience.map((a) => (
                    <li key={a}>· {a}</li>
                  ))}
                </ul>
                <p className="border-t border-warmgray-200 pt-4 text-sm font-medium text-burgundy-700">
                  {p.quote}
                </p>
                <span className="flex items-center gap-1 text-sm font-medium text-navy-900">
                  자세히 보기 <ArrowRight size={15} />
                </span>
              </Link>
            ))}
          </div>
        </Container>
      </section>

      {/* 5. Situational recommendation */}
      <section className="bg-beige-100 py-20">
        <Container className="flex flex-col items-center gap-10">
          <SectionHeading title="내 상황에는 어떤 상담이 맞을까요?" />
          <div className="flex w-full flex-col gap-3">
            {situations.map((s) => (
              <Link
                key={s.text}
                href={s.href}
                className="flex items-center justify-between rounded-sm border border-warmgray-300/70 bg-white px-6 py-4 text-sm transition-colors hover:border-burgundy-600 sm:text-base"
              >
                <span className="text-navy-800">{s.text}</span>
                <span className="flex shrink-0 items-center gap-1 font-medium text-burgundy-700">
                  {s.target} <ArrowRight size={15} />
                </span>
              </Link>
            ))}
          </div>
        </Container>
      </section>

      {/* 6. Reviews preview */}
      {reviews.length > 0 && (
        <section className="bg-ivory-50 py-20">
          <Container className="flex flex-col items-center gap-12">
            <SectionHeading
              eyebrow="상담 후기"
              title="나와 비슷한 사람들의 이야기"
              description="후기는 자랑이 아니라, 지금의 내 상황을 대입해보는 공간입니다."
            />
            <div className="grid w-full gap-6 md:grid-cols-3">
              {reviews.map((r) => (
                <ReviewCard
                  key={r.id}
                  id={r.id}
                  category={r.category}
                  title={r.title}
                  helpfulPart={r.helpfulPart}
                  ageGroup={r.ageGroup}
                  situationTag={r.situationTag}
                />
              ))}
            </div>
            <Button href="/reviews" variant="secondary">
              후기 전체 보기
            </Button>
          </Container>
        </section>
      )}

      {/* Differentiators */}
      <section className="bg-navy-950 py-20 text-ivory-50">
        <Container className="flex flex-col items-center gap-10">
          <SectionHeading eyebrow="러브백의 차별점" title="상담 사이트가 아니라, 관계 연구소입니다" light />
          <ol className="grid w-full gap-4 sm:grid-cols-2">
            {differentiators.map((d, i) => (
              <li
                key={d}
                className="flex items-start gap-3 rounded-sm border border-ivory-100/15 px-5 py-4 text-sm leading-relaxed text-ivory-100/85 sm:text-base"
              >
                <span className="font-serif-kr text-burgundy-500">{String(i + 1).padStart(2, "0")}</span>
                {d}
              </li>
            ))}
          </ol>
        </Container>
      </section>

      {/* Free diagnosis teaser */}
      <section className="bg-beige-100 py-20">
        <Container className="flex flex-col items-center gap-6 text-center">
          <SectionHeading
            eyebrow="무료 진단"
            title="내 관계가 지금 회복 가능한 흐름인지 알고 싶다면?"
            description="결제 전에 먼저 체크리스트로 현재 상태를 가볍게 점검해보세요."
          />
          <Button href="/diagnosis" size="lg">
            무료 관계 진단 체크리스트 하기
          </Button>
        </Container>
      </section>

      {/* Final CTA */}
      <section className="bg-navy-900 py-20 text-ivory-50">
        <Container className="flex flex-col items-center gap-6 text-center">
          <h2 className="font-serif-kr max-w-xl text-2xl leading-snug font-medium sm:text-3xl">
            지금 이 관계, 혼자 고민하지 마세요.
          </h2>
          <p className="max-w-lg text-ivory-100/75">
            현재 관계의 흐름, 상대 심리, 내 행동 패턴을 함께 분석해
            지금 해야 할 선택을 정리해드립니다.
          </p>
          <div className="flex flex-col gap-3 sm:flex-row">
            <Button href="/apply" size="lg">
              1:1 상담 신청하기
            </Button>
            <Button
              href={site.kakaoChannelUrl}
              target="_blank"
              variant="kakao"
              size="lg"
            >
              카카오톡으로 문의하기
            </Button>
          </div>
        </Container>
      </section>
    </div>
  );
}
