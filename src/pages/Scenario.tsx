import { PageShell } from "../components/Layout";

const SCENARIOS = [
  {
    situation: "상대 답장이 6시간 늦을 때",
    avoid: "여러 번 연달아 메시지를 보내며 추궁하기",
    say: "바쁘면 나중에 답해도 괜찮아. 다만 오늘 안에만 짧게 말해주면 좋겠어.",
  },
  {
    situation: "상대가 인스타는 하면서 답장을 안 할 때",
    avoid: "SNS 활동을 캡처해 따지기",
    say: "인스타 보고 좀 서운했어. 잠깐이라도 답 주면 마음이 놓일 것 같아.",
  },
  {
    situation: "썸이 애매하게 이어질 때",
    avoid: "확신 없이 계속 맞춰주며 기다리기",
    say: "우리 지금 이 관계를 어떻게 정의하고 있는지 한 번 얘기해보고 싶어.",
  },
  {
    situation: "연인이 이성친구와 단둘이 만날 때",
    avoid: "말없이 참거나 SNS로 몰래 확인하기",
    say: "그 만남이 나한테는 조금 신경 쓰이는 부분이라, 미리 얘기해주면 좋겠어.",
  },
  {
    situation: "컨디션이 안 좋아 연락을 못 할 때",
    avoid: "설명 없이 잠수타기",
    say: "내가 컨디션이 안 좋을 때 답장이 느려질 수 있는데, 마음이 식어서 그런 건 아니야.",
  },
  {
    situation: "약복용 사실을 언제 말할지 고민될 때",
    avoid: "관계 초반부터 세세한 진단명까지 전부 설명하기",
    say: "요즘 컨디션 관리를 위해 약을 먹고 있어. 데이트에 영향이 있으면 미리 말해줄게.",
  },
  {
    situation: "공황 때문에 데이트 장소가 부담될 때",
    avoid: "이유 없이 약속을 취소하기",
    say: "특정 장소에서 긴장이 심해질 수 있어, 다른 곳으로 정하거나 잠깐 나갔다 올 수 있을까?",
  },
  {
    situation: "우울해서 데이트가 힘들 때",
    avoid: "아무 말 없이 약속을 미루기",
    say: "오늘은 에너지가 많이 없어서 짧게 만나거나 다음으로 미뤄도 될까?",
  },
  {
    situation: "ADHD 때문에 약속을 까먹었을 때",
    avoid: "변명 없이 넘어가거나 자책만 하기",
    say: "약속을 깜빡했어, 미안해. 앞으로는 알림을 이중으로 맞춰둘게.",
  },
  {
    situation: "불안해서 확인 연락을 보내고 싶을 때",
    avoid: "감정적인 메시지를 바로 보내기",
    say: "지금 좀 불안한 마음이 들어서 그런데, 편할 때 짧게 답 줄 수 있어?",
  },
];

export default function Scenario() {
  return (
    <PageShell>
      <div className="mx-auto max-w-4xl px-5 py-16 sm:px-8">
        <p className="text-center text-xs font-semibold tracking-[0.2em] text-plum-600 uppercase">Scenario</p>
        <h1 className="font-serif-kr mt-3 text-center text-2xl font-semibold text-ink-950 sm:text-3xl">
          상황별 대응 카드
        </h1>
        <p className="mx-auto mt-3 max-w-lg text-center text-sm text-ink-500">
          연애에서 자주 막히는 순간, 하지 말아야 할 반응과 추천 문장을 확인하세요.
        </p>
        <div className="mt-10 grid gap-4 sm:grid-cols-2">
          {SCENARIOS.map((s) => (
            <div key={s.situation} className="rounded-2xl border border-ink-100 bg-white p-6 shadow-card">
              <h3 className="font-serif-kr text-[15px] font-semibold text-ink-950">{s.situation}</h3>
              <p className="mt-3 text-xs font-semibold tracking-wide text-rose-600 uppercase">피해야 할 반응</p>
              <p className="mt-1 text-sm text-ink-600">{s.avoid}</p>
              <p className="mt-3 text-xs font-semibold tracking-wide text-plum-600 uppercase">추천 문장</p>
              <p className="mt-1 text-sm text-ink-700 italic">“{s.say}”</p>
            </div>
          ))}
        </div>
      </div>
    </PageShell>
  );
}
