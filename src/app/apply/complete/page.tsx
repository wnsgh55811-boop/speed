import { Container } from "@/components/Container";
import { Button } from "@/components/Button";
import { site } from "@/lib/site";

export default function ApplyCompletePage() {
  return (
    <div className="bg-ivory-50 py-24">
      <Container className="flex flex-col items-center gap-6 text-center">
        <h1 className="font-serif-kr text-2xl font-medium text-navy-900 sm:text-3xl">
          상담 신청서가 접수되었습니다
        </h1>
        <p className="max-w-md text-warmgray-600">
          작성해주신 내용을 바탕으로 코치가 확인 후, 결제 및 상담 일정을
          카카오톡 또는 연락처로 안내드립니다. 빠른 확인을 원하시면 카카오톡
          채널로 문의해주세요.
        </p>
        <div className="flex flex-col gap-3 sm:flex-row">
          <Button href={site.kakaoChannelUrl} target="_blank" variant="kakao">
            카카오톡 채널 바로가기
          </Button>
          <Button href="/" variant="secondary">
            홈으로 돌아가기
          </Button>
        </div>
      </Container>
    </div>
  );
}
