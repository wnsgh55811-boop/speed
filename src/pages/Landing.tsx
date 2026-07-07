import { Link } from "react-router-dom";
import { PageShell } from "../components/Layout";

const REASONS = [
  "사람마다 생활환경이 다르기 때문입니다.",
  "감정과 컨디션이 관계에 영향을 주기 때문입니다.",
  "불안, 우울, ADHD, 불면, 공황, 강박은 연락과 갈등 방식에 영향을 줄 수 있기 때문입니다.",
  "연애 문제는 대화 스킬만으로 해결되지 않기 때문입니다.",
];

const DIMENSIONS = [
  { title: "생활환경", desc: "시간, 거주, 경제, 가족환경이 연애에 남기는 흔적" },
  { title: "관계환경", desc: "친구관계, 이성친구 기준, 새로운 만남의 경로" },
  { title: "연락·갈등 반응", desc: "답장 해석, 연락 빈도, 서운함을 다루는 방식" },
  { title: "애착 반응", desc: "가까워질 때와 거리가 느껴질 때의 진짜 반응" },
  { title: "감정·컨디션", desc: "우울·불안·강박·ADHD·불면·공황 가능성 스크리닝" },
  { title: "진단·약복용 영향", desc: "기존 진단과 약 복용이 관계에 주는 실제 영향" },
];

const STEPS = [
  { n: "01", title: "사전 동의", desc: "민감한 질문을 다루는 방식에 먼저 동의합니다" },
  { n: "02", title: "관계 흐름 분석", desc: "생활환경부터 애착반응, 감정·컨디션까지 단계별로 답합니다" },
  { n: "03", title: "리포트 확인", desc: "막힘의 원인, 위험 신호, 맞는 상대 유형, 행동 가이드를 받습니다" },
];

const IMG_HERO =
  "https://d8j0ntlcm91z4.cloudfront.net/user_36TmLGicluGODkcYejmrwLWoKV7/hf_20260707_044331_a480edd5-0285-449a-8b84-a448ad08c688.png";
const IMG_BENCH =
  "https://d8j0ntlcm91z4.cloudfront.net/user_36TmLGicluGODkcYejmrwLWoKV7/hf_20260707_044408_c06cc3f3-9eea-451b-a913-a2a445b0ce61.png";

export default function Landing() {
  return (
    <PageShell>
      <section className="relative overflow-hidden px-5 pt-16 pb-24 sm:px-8 sm:pt-20">
        <div
          className="pointer-events-none absolute -top-24 right-[-10%] h-[420px] w-[420px] rounded-full opacity-40 blur-3xl"
          style={{ background: "radial-gradient(circle, var(--color-plum-300), transparent 70%)" }}
        />
        <div
          className="pointer-events-none absolute top-40 left-[-8%] h-[320px] w-[320px] rounded-full opacity-40 blur-3xl"
          style={{ background: "radial-gradient(circle, var(--color-gold-300), transparent 70%)" }}
        />
        <div className="relative mx-auto grid max-w-6xl items-center gap-10 lg:grid-cols-[1.05fr_0.95fr] lg:gap-14">
          <div className="text-center lg:text-left">
            <p className="animate-fade-up mb-6 text-xs font-semibold tracking-[0.2em] text-plum-600 uppercase">
              Modern Relation UX
            </p>
            <h1
              className="animate-fade-up font-serif-kr text-[32px] leading-[1.3] font-semibold tracking-tight text-ink-950 sm:text-[44px]"
              style={{ animationDelay: "0.05s" }}
            >
              연애 문제는
              <br className="sm:hidden" /> 성격만의 문제가 아닙니다
            </h1>
            <p
              className="animate-fade-up mx-auto mt-6 max-w-xl text-[15px] leading-relaxed text-ink-600 sm:text-base lg:mx-0"
              style={{ animationDelay: "0.1s" }}
            >
              생활패턴, 가족환경, 친구관계, 감정기복, 불안, 우울, ADHD, 불면, 공황, 강박 성향까지 —
              당신의 생활환경, 감정패턴, 컨디션, 관계반응을 함께 분석합니다.
            </p>
            <div
              className="animate-fade-up mt-9 flex flex-col items-center justify-center gap-3 sm:flex-row lg:justify-start"
              style={{ animationDelay: "0.15s" }}
            >
              <Link
                to="/consent"
                className="w-full rounded-full bg-coral-500 px-7 py-3.5 text-[15px] font-medium text-paper shadow-card transition hover:bg-coral-600 sm:w-auto"
              >
                내 관계 흐름 분석하기
              </Link>
              <a
                href="#how-it-works"
                className="w-full rounded-full border border-ink-200 px-7 py-3.5 text-[15px] font-medium text-ink-700 transition hover:border-ink-400 hover:bg-ink-50 sm:w-auto"
              >
                진단 방식 보기
              </a>
            </div>
            <p
              className="animate-fade-up mt-6 text-xs text-ink-400"
              style={{ animationDelay: "0.2s" }}
            >
              본 서비스는 의료기관의 진단을 대체하지 않으며, 자기보고 기반의 관계·심리 패턴 분석을 제공합니다.
            </p>
          </div>
          <div className="animate-fade-up relative aspect-[4/3] overflow-hidden rounded-[28px] shadow-card" style={{ animationDelay: "0.1s" }}>
            <img src={IMG_HERO} alt="따뜻하게 대화를 나누는 커플" className="h-full w-full object-cover" loading="eager" />
          </div>
        </div>
      </section>

      <section className="border-t border-ink-100 bg-white px-5 py-20 sm:px-8">
        <div className="mx-auto max-w-4xl text-center">
          <h2 className="font-serif-kr text-2xl font-semibold text-ink-950 sm:text-3xl">
            왜 기존 연애 조언은 효과가 없을까요?
          </h2>
          <div className="mt-10 grid gap-4 text-left sm:grid-cols-2">
            {REASONS.map((r, i) => (
              <div key={r} className="flex gap-3 rounded-2xl border border-ink-100 bg-paper p-5">
                <span className="font-serif-kr text-lg font-semibold text-gold-600">{String(i + 1).padStart(2, "0")}</span>
                <p className="text-sm leading-relaxed text-ink-700">{r}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section id="how-it-works" className="px-5 py-20 sm:px-8">
        <div className="mx-auto max-w-5xl">
          <div className="mb-12 text-center">
            <p className="text-xs font-semibold tracking-[0.2em] text-plum-600 uppercase">6 Dimensions</p>
            <h2 className="mt-3 font-serif-kr text-2xl font-semibold text-ink-950 sm:text-3xl">
              6가지 축으로 관계 흐름을 분석합니다
            </h2>
          </div>
          <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
            {DIMENSIONS.map((d) => (
              <div
                key={d.title}
                className="rounded-2xl border border-ink-100 bg-white p-6 shadow-card transition hover:shadow-card-hover"
              >
                <h3 className="font-serif-kr text-[17px] font-semibold text-ink-950">{d.title}</h3>
                <p className="mt-2 text-[13.5px] leading-relaxed text-ink-500">{d.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section
        className="border-t border-ink-100 px-5 py-20 text-ink-900 sm:px-8"
        style={{ background: "var(--gradient-band)" }}
      >
        <div className="mx-auto max-w-4xl">
          <div className="mb-12 text-center">
            <p className="text-xs font-semibold tracking-[0.2em] text-gold-600 uppercase">Process</p>
            <h2 className="mt-3 font-serif-kr text-2xl font-semibold sm:text-3xl">3분이면 첫 요약을 받습니다</h2>
          </div>
          <div className="grid gap-8 sm:grid-cols-3">
            {STEPS.map((s) => (
              <div key={s.n}>
                <span className="font-serif-kr text-3xl font-semibold text-gold-600">{s.n}</span>
                <h3 className="mt-3 text-[17px] font-semibold">{s.title}</h3>
                <p className="mt-2 text-sm leading-relaxed text-ink-600">{s.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section className="px-5 py-24 sm:px-8">
        <div className="mx-auto grid max-w-5xl items-center gap-8 sm:grid-cols-[0.85fr_1.15fr] sm:gap-10">
          <div className="aspect-[4/3] overflow-hidden rounded-[24px] shadow-card">
            <img
              src={IMG_BENCH}
              alt="진솔한 대화를 나누는 커플"
              className="h-full w-full object-cover object-[50%_25%]"
              loading="lazy"
            />
          </div>
          <div className="text-center sm:text-left">
            <h2 className="font-serif-kr text-2xl font-semibold text-ink-950 sm:text-3xl">
              3분 요약 분석부터 시작하세요
            </h2>
            <p className="mt-3 text-sm leading-relaxed text-ink-600">
              더 깊은 분석은 심화 리포트에서 확인할 수 있습니다.
            </p>
            <Link
              to="/consent"
              className="mt-8 inline-block rounded-full bg-coral-500 px-8 py-3.5 text-[15px] font-medium text-paper shadow-card transition hover:bg-coral-600"
            >
              무료 분석 시작
            </Link>
          </div>
        </div>
      </section>
    </PageShell>
  );
}
