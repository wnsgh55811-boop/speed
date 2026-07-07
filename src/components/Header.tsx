"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useState } from "react";
import { Menu, X } from "lucide-react";
import { Container } from "./Container";
import { Button } from "./Button";
import { mainNav, site } from "@/lib/site";

export function Header() {
  const pathname = usePathname();
  const [open, setOpen] = useState(false);

  if (pathname?.startsWith("/admin")) return null;

  return (
    <header className="sticky top-0 z-40 border-b border-warmgray-200 bg-ivory-50/95 backdrop-blur">
      <Container className="flex h-16 items-center justify-between">
        <Link href="/" className="font-serif-kr text-lg font-semibold text-navy-900">
          {site.shortName}
          <span className="ml-1 text-xs font-sans font-normal text-warmgray-500">
            관계 연구소
          </span>
        </Link>

        <nav className="hidden items-center gap-7 lg:flex">
          {mainNav.map((item) => (
            <Link
              key={item.href}
              href={item.href}
              className="text-sm font-medium text-navy-800 transition-colors hover:text-burgundy-700"
            >
              {item.label}
            </Link>
          ))}
        </nav>

        <div className="hidden items-center gap-3 lg:flex">
          <Button href="/apply" size="sm">
            상담 신청하기
          </Button>
        </div>

        <button
          className="flex h-10 w-10 items-center justify-center text-navy-900 lg:hidden"
          onClick={() => setOpen(!open)}
          aria-label="메뉴 열기"
        >
          {open ? <X size={22} /> : <Menu size={22} />}
        </button>
      </Container>

      {open && (
        <div className="border-t border-warmgray-200 bg-ivory-50 lg:hidden">
          <Container className="flex flex-col gap-1 py-3">
            {mainNav.map((item) => (
              <Link
                key={item.href}
                href={item.href}
                onClick={() => setOpen(false)}
                className="rounded-sm px-2 py-3 text-sm font-medium text-navy-800 hover:bg-ivory-200"
              >
                {item.label}
              </Link>
            ))}
            <Button href="/apply" className="mt-2 w-full">
              상담 신청하기
            </Button>
          </Container>
        </div>
      )}
    </header>
  );
}
