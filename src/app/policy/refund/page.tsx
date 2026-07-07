import type { Metadata } from "next";
import { PolicyPage } from "@/components/PolicyPage";

export const metadata: Metadata = { title: "환불규정" };

export default function RefundPage() {
  return (
    <PolicyPage
      title="환불규정"
      updatedAt="2026.01.01"
      sections={[
        {
          heading: "1. 상담 전 환불",
          body: [
            "결제 완료 후 상담을 위한 사전 분석(신청서 검토, 자료 분석 등)이 시작되기 전까지는 결제 금액의 전액 환불이 가능합니다.",
          ],
        },
        {
          heading: "2. 사전 분석 시작 후 환불",
          body: [
            "코치가 상담 신청서를 바탕으로 사전 분석을 시작한 이후에는, 상담 특성상 이미 투입된 분석 시간에 대한 비용을 제외하고 부분 환불이 진행됩니다.",
          ],
        },
        {
          heading: "3. 상담 진행 후 환불",
          body: [
            "1:1 상담이 완료된 이후에는 서비스 제공이 완료된 것으로 보아 환불이 제한됩니다.",
          ],
        },
        {
          heading: "4. 상담 일정 변경",
          body: [
            "상담 일정은 예정일 기준 24시간 전까지 1회에 한해 무료로 변경 가능합니다. 이후 변경 또는 노쇼의 경우 재조율이 어려울 수 있습니다.",
          ],
        },
        {
          heading: "5. 환불 절차",
          body: [
            "환불을 원하실 경우 카카오톡 채널로 결제 내역과 함께 요청해주시면, 확인 후 영업일 기준 3~5일 이내 처리됩니다.",
          ],
        },
      ]}
    />
  );
}
