import "dotenv/config";
import { PrismaBetterSqlite3 } from "@prisma/adapter-better-sqlite3";
import { PrismaClient } from "../src/generated/prisma/client";

const adapter = new PrismaBetterSqlite3({
  url: process.env.DATABASE_URL ?? "file:./dev.db",
});
const prisma = new PrismaClient({ adapter });

const reviews = [
  {
    category: "REUNION" as const,
    nickname: "하늘달",
    ageGroup: "20대 여성",
    situationTag: "이별 후 3주",
    title: "연락만 고민했는데, 사실은 제 태도와 위치가 문제였다는 걸 알게 됐습니다.",
    beforeContent:
      "헤어진 지 3주쯤 됐는데 계속 연락 타이밍만 고민하고 있었어요. 언제 연락해야 할지, 뭐라고 보내야 할지 하루 종일 생각만 하다가 잠도 잘 못 잤습니다.",
    hardestPart:
      "제가 뭘 잘못했는지 계속 복기하게 되는 게 제일 힘들었어요. 상대 반응 하나하나에 일희일비하면서 감정 소모가 너무 컸습니다.",
    helpfulPart:
      "상담을 받고 나니 제가 왜 계속 밀어붙이게 됐는지, 관계 안에서 제 위치가 어땠는지 정리가 됐어요. 연락 문장보다 먼저 봐야 할 게 있다는 걸 알게 됐습니다.",
    afterContent:
      "지금은 무작정 붙잡는 게 아니라 제 상황을 정리하면서 접근하고 있어요. 마음은 여전히 조급하지만 최소한 어떤 순서로 움직여야 하는지는 알게 됐습니다.",
    messageToOthers:
      "연락 타이밍만 검색하지 마시고, 관계가 왜 이렇게 됐는지부터 정리해보세요. 그게 먼저입니다.",
  },
  {
    category: "DATING" as const,
    nickname: "봄날의곰",
    ageGroup: "30대 남성",
    situationTag: "연애 8개월차",
    title: "잘해줄수록 멀어지는 이유를 알게 됐어요.",
    beforeContent:
      "여자친구가 예전 같지 않다는 느낌을 받았습니다. 저는 더 잘해주려고 했는데 오히려 반응이 시큰둥해지는 게 이상했어요.",
    hardestPart:
      "제가 뭘 더 해야 할지 몰라서 계속 맞춰주기만 했는데, 그게 오히려 역효과였다는 걸 몰랐던 게 가장 답답했습니다.",
    helpfulPart:
      "제 과잉배려 패턴과 상대가 부담을 느끼는 지점을 짚어주셔서, 제가 관계에서 어떤 역할을 자처하고 있었는지 알게 됐습니다.",
    afterContent:
      "지금은 무조건 맞추기보다 제 기준을 먼저 세우고 대화하려고 합니다. 관계가 훨씬 편해졌어요.",
    messageToOthers: "잘해주는 것과 맞춰주기만 하는 건 다르다는 걸 꼭 아셨으면 좋겠습니다.",
  },
  {
    category: "SOME" as const,
    nickname: "라떼한잔",
    ageGroup: "20대 여성",
    situationTag: "소개팅 후 3주",
    title: "썸 타는 상대의 연락이 느려졌을 때 어떻게 해야 하는지 알게 됐습니다.",
    beforeContent:
      "소개팅 이후 잘 되어가나 싶었는데 갑자기 연락이 뜸해져서 어떻게 해야 할지 몰랐어요.",
    hardestPart: "먼저 연락하자니 매달리는 것 같고, 안 하자니 이대로 끝날 것 같아 불안했습니다.",
    helpfulPart:
      "지금 단계에서 상대가 어떤 신호를 보내고 있는지, 제가 어떤 포지션으로 대화해야 하는지 구체적으로 알려주셔서 도움이 됐습니다.",
    afterContent: "조급해하지 않고 적절한 거리에서 대화를 이어가고 있습니다.",
    messageToOthers: "썸 단계에서 혼자 불안해하지 말고 흐름부터 파악하세요.",
  },
  {
    category: "CHAT_ANALYSIS" as const,
    nickname: "새벽별",
    ageGroup: "20대 여성",
    situationTag: "카톡 분석",
    title: "제가 보낸 장문 카톡이 관계를 더 멀어지게 했다는 걸 알았습니다.",
    beforeContent:
      "이별 후 마지막으로 장문의 카톡을 보냈는데 답장이 없어서 괴로웠습니다.",
    hardestPart: "제가 보낸 메시지 어디가 문제였는지 스스로는 전혀 몰랐던 게 힘들었어요.",
    helpfulPart:
      "실제 대화 내용을 같이 보면서 어떤 문장에서 상대가 부담을 느꼈을지 하나하나 짚어주셨어요.",
    afterContent: "지금은 짧고 담백한 대화만 이어가고 있고, 마음도 한결 편해졌습니다.",
    messageToOthers: "감정이 격할 때 보낸 장문 메시지, 꼭 다시 한번 생각해보세요.",
  },
  {
    category: "PATTERN" as const,
    nickname: "고요한바다",
    ageGroup: "30대 여성",
    situationTag: "관계 패턴 진단",
    title: "연애할 때마다 비슷하게 무너지는 이유를 처음 알았습니다.",
    beforeContent:
      "매번 연애가 비슷한 패턴으로 끝났어요. 처음엔 좋다가 제가 점점 불안해지고 매달리게 되는 식이었습니다.",
    hardestPart: "상대만 바뀌었을 뿐인데 왜 똑같은 상황이 반복되는지 이해할 수 없었어요.",
    helpfulPart:
      "제 애착 유형과 반복되는 행동 패턴을 구조적으로 정리해주셔서, 문제가 상대가 아니라 제 패턴에 있었다는 걸 알게 됐습니다.",
    afterContent: "관계에서 불안해질 때 제 패턴을 먼저 점검하는 습관이 생겼습니다.",
    messageToOthers: "계속 비슷한 연애를 반복하고 있다면 상대가 아니라 패턴을 먼저 보세요.",
  },
  {
    category: "CHANGE" as const,
    nickname: "단단한하루",
    ageGroup: "20대 남성",
    situationTag: "상담 후 2개월",
    title: "상담 후 가장 크게 달라진 건 제 태도였습니다.",
    beforeContent: "재회를 원했지만 뭘 어떻게 해야 할지 몰라 조급하게만 움직였습니다.",
    hardestPart: "혼자 판단하고 혼자 행동하다 상황을 더 악화시켰던 게 가장 후회됩니다.",
    helpfulPart: "단계별 실행 전략을 정리해주셔서 감정적으로 행동하지 않을 수 있었습니다.",
    afterContent:
      "재회 여부를 떠나서, 관계를 대하는 제 태도 자체가 달라진 게 가장 큰 변화입니다.",
    messageToOthers: "결과보다 태도가 먼저 바뀌어야 한다는 말, 진짜였습니다.",
  },
  {
    category: "LONGFORM" as const,
    nickname: "잔잔한파도",
    ageGroup: "30대 여성",
    situationTag: "장문 후기",
    title: "6개월 연애, 이별, 그리고 상담까지의 긴 기록입니다.",
    beforeContent:
      "6개월 만난 사람과 헤어지고 저는 한 달 넘게 매일 연락 여부만 고민했습니다. 일상생활이 안 될 정도로 그 생각뿐이었어요.",
    hardestPart:
      "제가 이 관계에서 어떤 역할이었는지, 왜 이렇게까지 매달리게 됐는지 스스로 설명이 안 됐던 게 가장 힘들었습니다.",
    helpfulPart:
      "상담을 통해 관계 전체 흐름을 시간순으로 정리하면서 제가 언제부터 불안해졌는지, 상대는 언제부터 멀어졌는지 명확히 보였습니다. 감정을 배제하고 사실관계를 정리하니 다음 행동이 훨씬 명확해졌어요.",
    afterContent:
      "지금은 결과에 집착하기보다 이 경험에서 배운 제 패턴을 기억하려고 합니다. 다음 관계에서는 같은 실수를 반복하지 않을 자신이 생겼습니다.",
    messageToOthers:
      "지금 너무 힘드시겠지만, 감정적으로 움직이기 전에 흐름부터 정리해보시길 권합니다.",
  },
];

async function main() {
  for (const r of reviews) {
    await prisma.review.create({
      data: { ...r, status: "APPROVED" },
    });
  }
  console.log(`Seeded ${reviews.length} reviews.`);
}

main()
  .catch((e) => {
    console.error(e);
    process.exit(1);
  })
  .finally(async () => {
    await prisma.$disconnect();
  });
