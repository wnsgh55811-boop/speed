"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { Container } from "./Container";
import { footerNav, site } from "@/lib/site";

export function Footer() {
  const pathname = usePathname();
  if (pathname?.startsWith("/admin")) return null;

  return (
    <footer className="border-t border-warmgray-200 bg-navy-950 text-ivory-100/70">
      <Container className="flex flex-col gap-6 py-12 text-sm">
        <div className="flex flex-col gap-2">
          <span className="font-serif-kr text-lg text-ivory-50">{site.name}</span>
          <p className="max-w-md leading-relaxed">
            연애, 이별, 재회를 감정이 아닌 관계 패턴과 상대 심리로 분석하는
            1:1 상담 연구소입니다.
          </p>
        </div>

        <div className="flex flex-wrap gap-x-6 gap-y-2">
          {footerNav.map((item) => (
            <Link key={item.href} href={item.href} className="hover:text-ivory-50">
              {item.label}
            </Link>
          ))}
          <Link href="/admin" className="hover:text-ivory-50">
            관리자
          </Link>
        </div>

        <div className="flex flex-col gap-1 text-xs text-ivory-100/50">
          <span>대표 코치: {site.coachName} · 카카오톡 채널: 러브백 관계 연구소</span>
          <span>
            본 상담은 심리 상담이 아닌 관계 코칭 서비스이며, 결과를 보장하지 않습니다.
          </span>
          <span>© {new Date().getFullYear()} {site.name}. All rights reserved.</span>
        </div>
      </Container>
    </footer>
  );
}
