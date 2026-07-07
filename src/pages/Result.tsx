import { useMemo, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { PageShell } from "../components/Layout";
import { computeResult } from "../lib/engine";
import { useAssessment } from "../lib/store";
import { domainDefinitions } from "../data/mentalHealth";
import type { DomainResult } from "../data/types";

function statusColor(normalized: number) {
  if (normalized <= 30) return { bg: "bg-[var(--color-signal-low)]", text: "text-[var(--color-signal-low)]" };
  if (normalized <= 60) return { bg: "bg-[var(--color-signal-watch)]", text: "text-[var(--color-signal-watch)]" };
  if (normalized <= 80) return { bg: "bg-[var(--color-signal-high)]", text: "text-[var(--color-signal-high)]" };
  return { bg: "bg-[var(--color-signal-crisis)]", text: "text-[var(--color-signal-crisis)]" };
}

function DomainBar({ result }: { result: DomainResult }) {
  const def = domainDefinitions[result.domain];
  const color = statusColor(result.normalized);
  return (
    <div>
      <div className="mb-1.5 flex items-baseline justify-between">
        <span className="text-sm font-medium text-ink-800">
          {def.label}
          {result.isLight && <span className="ml-1.5 text-[10px] font-normal text-ink-400">간이 추정</span>}
        </span>
        <span className={`text-xs font-semibold ${color.text}`}>{result.level}</span>
      </div>
      <div className="h-2 w-full overflow-hidden rounded-full bg-ink-100">
        <div className={`h-full rounded-full ${color.bg} transition-all duration-700`} style={{ width: `${Math.max(4, result.normalized)}%` }} />
      </div>
    </div>
  );
}

const HOTLINES = [
  { label: "생명이 위급한 경우", value: "119" },
  { label: "자살예방상담전화", value: "109" },
  { label: "정신건강상담전화", value: "1577-0199" },
];

function CrisisNotice({ onDismiss, dismissible }: { onDismiss: () => void; dismissible: boolean }) {
  return (
    <div className="rounded-2xl border border-rose-500/40 bg-rose-100 p-6 sm:p-8">
      <p className="text-xs font-semibold tracking-widest text-rose-600 uppercase">지금은 안전이 먼저입니다</p>
      <h2 className="font-serif-kr mt-3 text-xl font-semibold text-ink-950 sm:text-2xl">
        지금은 연애 분석보다 안전이 먼저입니다
      </h2>
      <p className="mt-3 text-sm leading-relaxed text-ink-700">
        혼자 판단하지 말고, 가까운 사람이나 전문가에게 즉시 알려주세요. 아래 연락처를 통해 도움을 받을 수 있습니다.
      </p>
      <div className="mt-5 grid gap-2 sm:grid-cols-3">
        {HOTLINES.map((h) => (
          <div key={h.value} className="rounded-xl border border-rose-500/30 bg-white px-4 py-3 text-center">
            <p className="text-[11px] text-ink-500">{h.label}</p>
            <p className="mt-0.5 font-serif-kr text-lg font-semibold text-rose-600">{h.value}</p>
          </div>
        ))}
      </div>
      {dismissible && (
        <button onClick={onDismiss} className="mt-6 text-xs text-ink-500 underline underline-offset-4 hover:text-ink-800">
          그래도 관계 분석 리포트를 확인할게요
        </button>
      )}
    </div>
  );
}

export default function Result() {
  const navigate = useNavigate();
  const { answers, consented, reset } = useAssessment();
  const [showReportAnyway, setShowReportAnyway] = useState(false);

  const result = useMemo(() => computeResult(answers), [answers]);

  if (!consented || Object.keys(answers).length === 0) {
    navigate("/", { replace: true });
    return null;
  }

  const { primaryType, secondaryType, topCauses, domainResults, crisis, summarySentence } = result;
  const showCrisis = crisis.shouldInterrupt && !showReportAnyway;

  const startOver = () => {
    reset();
    navigate("/");
  };

  return (
    <PageShell>
      <div className="mx-auto max-w-3xl px-5 py-14 sm:px-8">
        <p className="text-center text-xs font-semibold tracking-[0.2em] text-plum-600 uppercase">Your Report</p>
        <h1 className="font-serif-kr mt-3 text-center text-2xl font-semibold text-ink-950 sm:text-3xl">
          당신의 MODERN RELATION MAP
        </h1>

        {crisis.risk === "mid" && !showCrisis && (
          <div className="mt-8 rounded-xl border border-gold-400/60 bg-gold-100 px-5 py-4 text-sm text-ink-700">
            최근 마음이 힘든 신호가 있었어요. 필요하다면 정신건강상담전화 <b>1577-0199</b>에서 도움을 받을 수 있습니다.
          </div>
        )}

        {showCrisis ? (
          <div className="mt-8">
            <CrisisNotice onDismiss={() => setShowReportAnyway(true)} dismissible={crisis.risk === "high"} />
          </div>
        ) : (
          <div className="mt-8 space-y-10">
            <section className="rounded-2xl border border-ink-100 bg-white p-6 shadow-card sm:p-8">
              <p className="text-xs font-semibold tracking-widest text-gold-600 uppercase">핵심 요약</p>
              <h2 className="font-serif-kr mt-2 text-lg font-semibold text-ink-950 sm:text-xl">{summarySentence}</h2>
              <p className="mt-3 text-sm leading-relaxed text-ink-600">{primaryType.description}</p>

              <div className="mt-6 grid gap-3 sm:grid-cols-3">
                {topCauses.map((c) => (
                  <div key={c} className="rounded-xl bg-paper-dim px-4 py-3 text-center text-sm font-medium text-ink-700">
                    {c}
                  </div>
                ))}
              </div>
            </section>

            <section>
              <h3 className="font-serif-kr text-lg font-semibold text-ink-950">정신건강 가능성 요약</h3>
              <p className="mt-1 text-xs text-ink-500">
                이 결과는 진단이 아니라 자기보고 기반의 스크리닝입니다. 정확한 진단과 치료는 정신건강 전문가와 상의해야 합니다.
              </p>
              <div className="mt-5 space-y-4 rounded-2xl border border-ink-100 bg-white p-6 shadow-card">
                {domainResults.map((d) => (
                  <DomainBar key={d.domain} result={d} />
                ))}
              </div>
            </section>

            <section className="grid gap-4 sm:grid-cols-2">
              <div className="rounded-2xl border border-ink-100 bg-white p-6 shadow-card">
                <h3 className="text-sm font-semibold text-ink-950">잘 맞는 상대 유형</h3>
                <ul className="mt-3 space-y-2 text-sm text-ink-600">
                  {primaryType.goodMatch.map((m) => (
                    <li key={m} className="flex gap-2">
                      <span className="text-[var(--color-signal-low)]">＋</span>
                      {m}
                    </li>
                  ))}
                </ul>
              </div>
              <div className="rounded-2xl border border-ink-100 bg-white p-6 shadow-card">
                <h3 className="text-sm font-semibold text-ink-950">조심해야 할 상대 유형</h3>
                <ul className="mt-3 space-y-2 text-sm text-ink-600">
                  {primaryType.badMatch.map((m) => (
                    <li key={m} className="flex gap-2">
                      <span className="text-[var(--color-signal-crisis)]">－</span>
                      {m}
                    </li>
                  ))}
                </ul>
              </div>
            </section>

            <section
              className="rounded-2xl border border-ink-100 p-6 text-ink-900 sm:p-8"
              style={{ background: "var(--gradient-band)" }}
            >
              <h3 className="font-serif-kr text-lg font-semibold">행동 가이드</h3>
              <div className="mt-4 space-y-4">
                {primaryType.actionGuide.map((g) => (
                  <div key={g.label} className="rounded-xl bg-white/60 p-4">
                    <p className="text-xs font-semibold tracking-wide text-gold-600 uppercase">{g.label}</p>
                    <p className="mt-1.5 text-sm leading-relaxed text-ink-700">{g.text}</p>
                  </div>
                ))}
              </div>
            </section>

            <section className="rounded-2xl border border-dashed border-ink-200 p-6 text-center">
              <p className="text-sm text-ink-500">
                보조 유형: <span className="font-medium text-ink-800">{secondaryType.name}</span> 성향도 함께 나타났습니다.
              </p>
              <p className="mt-2 text-xs text-ink-400">
                6개 심리영역 상세 점수, 상황별 대화 문장, 7일 행동 미션은 심화 리포트에서 확인할 수 있습니다.
              </p>
              <Link
                to="/expert"
                className="mt-4 inline-block rounded-full bg-coral-500 px-6 py-3 text-sm font-medium text-paper transition hover:bg-coral-600"
              >
                심화 리포트 · 1:1 해석 알아보기
              </Link>
            </section>
          </div>
        )}

        <div className="mt-12 text-center">
          <button onClick={startOver} className="text-xs text-ink-400 underline underline-offset-4 hover:text-ink-700">
            처음부터 다시 분석하기
          </button>
        </div>
      </div>
    </PageShell>
  );
}
