"use client";

import { usePathname } from "next/navigation";
import { site } from "@/lib/site";
import { Button } from "./Button";

export function MobileCta() {
  const pathname = usePathname();
  if (pathname?.startsWith("/admin")) return null;

  return (
    <div className="fixed inset-x-0 bottom-0 z-40 flex border-t border-warmgray-300 bg-ivory-50 md:hidden">
      <Button
        href={site.kakaoChannelUrl}
        target="_blank"
        variant="kakao"
        className="flex-1 rounded-none py-4"
      >
        카톡 상담 문의
      </Button>
      <Button href="/apply" variant="primary" className="flex-1 rounded-none py-4">
        상담 신청하기
      </Button>
    </div>
  );
}
