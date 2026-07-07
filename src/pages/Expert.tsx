import { PageShell } from "../components/Layout";

const OFFERINGS = [
  { title: "1:1 관계 분석 상담", desc: "리포트를 함께 해석하고 구체적인 상황에 맞춰 조언을 받습니다." },
  { title: "심화 리포트 해석", desc: "12개 결과유형, 애착반응, 약복용 영향을 전문가와 함께 확인합니다." },
  { title: "정신건강 전문가 연결 안내", desc: "필요한 경우 정신건강의학과·상담센터 연결을 안내합니다." },
  { title: "위기 상황 안내", desc: "위기 신호가 감지된 경우 즉시 도움받을 수 있는 창구를 안내합니다." },
];

const HOTLINES = [
  { label: "생명이 위급하거나 즉각적인 위험이 있는 경우", value: "119" },
  { label: "자살예방상담전화", value: "109" },
  { label: "정신건강상담전화", value: "1577-0199" },
];

export default function Expert() {
  return (
    <PageShell>
      <div className="mx-auto max-w-3xl px-5 py-16 sm:px-8">
        <p className="text-center text-xs font-semibold tracking-[0.2em] text-plum-600 uppercase">Expert</p>
        <h1 className="font-serif-kr mt-3 text-center text-2xl font-semibold text-ink-950 sm:text-3xl">
          전문가와 함께 더 깊이 이해하기
        </h1>

        <div className="mt-10 grid gap-4 sm:grid-cols-2">
          {OFFERINGS.map((o) => (
            <div key={o.title} className="rounded-2xl border border-ink-100 bg-white p-6 shadow-card">
              <h3 className="font-serif-kr text-[15px] font-semibold text-ink-950">{o.title}</h3>
              <p className="mt-2 text-[13.5px] leading-relaxed text-ink-500">{o.desc}</p>
            </div>
          ))}
        </div>

        <div className="mt-10 rounded-2xl border border-ink-100 bg-paper-dim p-6 text-sm leading-relaxed text-ink-600">
          MODERN RELATION UX는 심리교육과 관계 코칭을 제공하며, 의학적 진단이나 약물 처방은 정신건강의학과 전문의와
          상의해야 합니다.
        </div>

        <div className="mt-6 rounded-2xl border border-rose-500/30 bg-rose-100 p-6">
          <p className="text-xs font-semibold tracking-widest text-rose-600 uppercase">위기 지원 안내</p>
          <div className="mt-4 grid gap-2 sm:grid-cols-3">
            {HOTLINES.map((h) => (
              <div key={h.value} className="rounded-xl border border-rose-500/30 bg-white px-4 py-3 text-center">
                <p className="text-[11px] text-ink-500">{h.label}</p>
                <p className="mt-0.5 font-serif-kr text-lg font-semibold text-rose-600">{h.value}</p>
              </div>
            ))}
          </div>
        </div>
      </div>
    </PageShell>
  );
}
