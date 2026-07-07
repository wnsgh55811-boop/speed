import type { Metadata } from "next";
import { PolicyPage } from "@/components/PolicyPage";
import { site } from "@/lib/site";

export const metadata: Metadata = { title: "개인정보처리방침" };

export default function PrivacyPage() {
  return (
    <PolicyPage
      title="개인정보처리방침"
      updatedAt="2026.01.01"
      sections={[
        {
          heading: "1. 수집하는 개인정보 항목",
          body: [
            "회사는 상담 신청 및 후기 작성을 위해 다음 정보를 수집합니다.",
            "· 상담 신청: 이름 또는 닉네임, 연락처, 상담 희망 시간대, 상담을 위해 이용자가 직접 작성한 상황 및 대화 내용\n· 후기 작성: 닉네임, 연령/성별(선택), 후기 내용, 비밀글 설정 시 비밀번호",
          ],
        },
        {
          heading: "2. 개인정보의 수집 및 이용 목적",
          body: [
            "수집한 정보는 상담 신청 확인 및 안내, 상담 진행, 후기 게시판 운영, 서비스 개선 목적으로만 이용하며, 명시한 목적 외의 용도로 사용하지 않습니다.",
          ],
        },
        {
          heading: "3. 개인정보의 보유 및 이용 기간",
          body: [
            "상담 신청 정보는 상담 종료 후 관련 법령에 따른 보관 의무 기간 동안 보관 후 파기하며, 후기 게시글은 이용자가 삭제를 요청하기 전까지 게시판에 보관됩니다.",
          ],
        },
        {
          heading: "4. 개인정보의 제3자 제공",
          body: ["회사는 이용자의 동의 없이 개인정보를 제3자에게 제공하지 않습니다."],
        },
        {
          heading: "5. 이용자의 권리",
          body: [
            "이용자는 언제든지 본인의 개인정보 열람, 정정, 삭제를 요청할 수 있습니다. 문의는 카카오톡 채널을 통해 접수해주시기 바랍니다.",
          ],
        },
        {
          heading: "6. 문의처",
          body: [`카카오톡 채널: ${site.name} · 담당: ${site.coachName} 코치`],
        },
      ]}
    />
  );
}
