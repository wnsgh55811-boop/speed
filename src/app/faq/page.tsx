import type { Metadata } from "next";
import { Container } from "@/components/Container";
import { Button } from "@/components/Button";
import { Accordion } from "@/components/Accordion";

export const metadata: Metadata = {
  title: "FAQ",
  description: "러브백 상담 신청 전 자주 묻는 질문.",
};

const faqs = [
  {
    question: "재회 가능성을 정확히 알 수 있나요?",
    answer:
      "재회 가능성은 단정할 수 없습니다. 다만 이별 과정, 상대의 반응, 현재 관계 상태, 마지막 연락 내용, 차단 여부, 감정 소모 정도를 바탕으로 현실적인 가능성과 방향을 분석할 수 있습니다.",
  },
  {
    question: "상담받으면 무조건 재회할 수 있나요?",
    answer:
      "무조건적인 결과를 약속하지 않습니다. 러브백은 결과를 보장하기보다 현재 상황에서 가능성을 높이는 방향과 피해야 할 행동을 정리해드립니다.",
  },
  {
    question: "카톡 내용도 봐주시나요?",
    answer:
      "네. 필요한 경우 실제 대화 흐름을 함께 보며 어떤 지점에서 상대가 부담을 느꼈는지, 어떤 메시지가 관계 흐름을 악화시켰는지 분석합니다.",
  },
  {
    question: "상담 전에 무엇을 준비해야 하나요?",
    answer:
      "관계 기간, 이별 시점, 갈등 원인, 마지막 대화, 현재 연락 상태, 상대의 반응, 본인의 목표를 정리해주시면 좋습니다.",
  },
  {
    question: "상담은 어떻게 진행되나요?",
    answer:
      "사전 신청서를 바탕으로 전화 또는 온라인 방식으로 진행됩니다. 상담 방식은 상품별로 다르게 안내할 수 있습니다.",
  },
  {
    question: "환불은 가능한가요?",
    answer:
      "상담 특성상 사전 분석이 시작된 이후에는 환불이 제한될 수 있습니다. 환불 규정은 신청 전 반드시 확인할 수 있도록 별도 안내합니다. 자세한 내용은 환불규정 페이지를 참고해주세요.",
  },
];

export default function FaqPage() {
  return (
    <div>
      <section className="border-b border-warmgray-200 bg-navy-950 py-16 text-ivory-50 sm:py-20">
        <Container className="flex flex-col items-center gap-4 text-center">
          <span className="text-xs font-semibold tracking-[0.2em] text-ivory-100/70 uppercase">
            FAQ
          </span>
          <h1 className="font-serif-kr max-w-2xl text-3xl leading-snug font-medium sm:text-4xl">
            자주 묻는 질문
          </h1>
        </Container>
      </section>

      <section className="bg-ivory-50 py-16">
        <Container className="max-w-2xl">
          <Accordion items={faqs} />
        </Container>
      </section>

      <section className="bg-beige-100 py-16">
        <Container className="flex flex-col items-center gap-6 text-center">
          <p className="max-w-lg text-navy-800">
            더 궁금한 점이 있다면 카카오톡으로 편하게 문의해주세요.
          </p>
          <Button href="/apply" size="lg">
            상담 신청하기
          </Button>
        </Container>
      </section>
    </div>
  );
}
