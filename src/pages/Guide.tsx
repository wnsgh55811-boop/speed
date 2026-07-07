import { PageShell } from "../components/Layout";

const GUIDES = [
  { title: "우울과 연애", desc: "기분 저하가 연락과 데이트 지속력에 미치는 영향" },
  { title: "불안과 연락", desc: "답장 지연을 해석하는 방식과 확인 행동 다루기" },
  { title: "ADHD와 약속", desc: "일정 관리가 흔들릴 때 오해를 줄이는 방법" },
  { title: "불면과 감정기복", desc: "수면 문제가 예민함과 관계 지속력에 주는 영향" },
  { title: "공황과 데이트 장소", desc: "장소·이동 부담을 상대와 조율하는 방법" },
  { title: "강박과 확인 행동", desc: "반복 확인 충동을 알아차리고 조절하는 법" },
  { title: "약복용과 연애 대화", desc: "복용 사실을 언제, 어떻게 설명할지" },
  { title: "이성친구 기준", desc: "애매한 기준을 명확히 하는 대화법" },
  { title: "가족환경과 연애관", desc: "가족의 영향이 관계 기대치에 미치는 영향" },
  { title: "이별 후 회복", desc: "미련, 연락 충동, 재회 고민을 다루는 순서" },
];

export default function Guide() {
  return (
    <PageShell>
      <div className="mx-auto max-w-5xl px-5 py-16 sm:px-8">
        <p className="text-center text-xs font-semibold tracking-[0.2em] text-plum-600 uppercase">Guide</p>
        <h1 className="font-serif-kr mt-3 text-center text-2xl font-semibold text-ink-950 sm:text-3xl">
          짧고 실용적인 관계 가이드
        </h1>
        <p className="mx-auto mt-3 max-w-lg text-center text-sm text-ink-500">
          이런 패턴이 나타납니다 · 오해받는 지점 · 상대에게 설명하는 문장 · 오늘 할 수 있는 행동
        </p>
        <div className="mt-10 grid gap-4 sm:grid-cols-2">
          {GUIDES.map((g) => (
            <div key={g.title} className="rounded-2xl border border-ink-100 bg-white p-6 shadow-card transition hover:shadow-card-hover">
              <h3 className="font-serif-kr text-[16px] font-semibold text-ink-950">{g.title}</h3>
              <p className="mt-2 text-[13.5px] leading-relaxed text-ink-500">{g.desc}</p>
            </div>
          ))}
        </div>
      </div>
    </PageShell>
  );
}
