import { Container } from "@/components/Container";
import { Button } from "@/components/Button";

export default function ReviewWriteCompletePage() {
  return (
    <div className="bg-ivory-50 py-24">
      <Container className="flex flex-col items-center gap-6 text-center">
        <h1 className="font-serif-kr text-2xl font-medium text-navy-900 sm:text-3xl">
          후기가 제출되었습니다
        </h1>
        <p className="max-w-md text-warmgray-600">
          소중한 후기 감사합니다. 관리자 확인 후 게시판에 노출됩니다.
        </p>
        <Button href="/reviews">후기 게시판으로 돌아가기</Button>
      </Container>
    </div>
  );
}
