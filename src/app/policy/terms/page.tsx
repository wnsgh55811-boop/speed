import type { Metadata } from "next";
import { PolicyPage } from "@/components/PolicyPage";
import { site } from "@/lib/site";

export const metadata: Metadata = { title: "이용약관" };

export default function TermsPage() {
  return (
    <PolicyPage
      title="이용약관"
      updatedAt="2026.01.01"
      sections={[
        {
          heading: "제1조 (목적)",
          body: [
            `본 약관은 ${site.name}(이하 "회사")가 제공하는 관계 코칭 상담 서비스(이하 "서비스")의 이용조건 및 절차, 이용자와 회사의 권리·의무 및 책임사항을 규정함을 목적으로 합니다.`,
          ],
        },
        {
          heading: "제2조 (서비스의 성격)",
          body: [
            "회사가 제공하는 서비스는 연애, 이별, 재회 상황에 대한 관계 코칭 및 커뮤니케이션 전략 자문이며, 의료법상 심리치료 또는 정신과적 진단·치료 행위가 아닙니다.",
            "서비스는 이용자가 제공한 정보를 바탕으로 한 분석과 제안이며, 상담 결과(재회, 관계 개선 등)를 보장하지 않습니다.",
          ],
        },
        {
          heading: "제3조 (이용계약의 성립)",
          body: [
            "이용계약은 이용자가 상담 신청서를 작성하고 회사가 안내하는 절차에 따라 결제를 완료함으로써 성립합니다.",
          ],
        },
        {
          heading: "제4조 (회사의 의무)",
          body: [
            "회사는 이용자가 제공한 정보를 상담 목적 외로 사용하지 않으며, 관련 법령에 따라 개인정보를 안전하게 관리합니다.",
          ],
        },
        {
          heading: "제5조 (이용자의 의무)",
          body: [
            "이용자는 상담 진행을 위해 필요한 정보를 사실에 근거하여 제공해야 하며, 허위 정보 제공으로 인한 불이익은 이용자 본인에게 있습니다.",
          ],
        },
        {
          heading: "제6조 (환불)",
          body: ["환불 절차 및 기준은 별도의 환불규정 페이지를 따릅니다."],
        },
      ]}
    />
  );
}
