import { Link, useLocation } from "react-router-dom";
import type { ReactNode } from "react";

const NAV_LINKS = [
  { to: "/guide", label: "Guide" },
  { to: "/scenario", label: "Scenario" },
  { to: "/expert", label: "Expert" },
];

export function Header() {
  const location = useLocation();
  const isTestFlow = location.pathname.startsWith("/test") || location.pathname.startsWith("/consent");

  return (
    <header className="sticky top-0 z-40 border-b border-ink-100/80 bg-paper/85 backdrop-blur-md">
      <div className="mx-auto flex max-w-6xl items-center justify-between px-5 py-4 sm:px-8">
        <Link to="/" className="flex items-center gap-2">
          <span className="flex h-6 w-9 shrink-0 items-center">
            <span className="h-6 w-6 rounded-full bg-plum-700" />
            <span className="-ml-2.5 h-6 w-6 rounded-full bg-gold-500/90" />
          </span>
          <span className="font-serif-kr text-[15px] font-semibold tracking-tight text-ink-950">
            MODERN RELATION UX
          </span>
        </Link>
        {!isTestFlow && (
          <nav className="hidden items-center gap-8 text-sm text-ink-600 sm:flex">
            {NAV_LINKS.map((l) => (
              <Link key={l.to} to={l.to} className="transition hover:text-ink-950">
                {l.label}
              </Link>
            ))}
          </nav>
        )}
        {!isTestFlow && (
          <Link
            to="/consent"
            className="rounded-full bg-ink-950 px-4 py-2 text-sm font-medium text-paper transition hover:bg-plum-800"
          >
            분석 시작하기
          </Link>
        )}
      </div>
    </header>
  );
}

export function Footer() {
  return (
    <footer className="border-t border-ink-100 bg-paper-dim">
      <div className="mx-auto max-w-6xl px-5 py-10 text-xs leading-relaxed text-ink-500 sm:px-8">
        <p className="mb-2 font-medium text-ink-600">
          본 서비스는 의료기관의 진단을 대체하지 않으며, 자기보고 기반의 관계·심리 패턴 분석을 제공합니다.
        </p>
        <p>
          위기 상황 시 도움받을 수 있는 곳 — 자살예방상담전화 109 · 정신건강상담전화 1577-0199 · 생명이 위급한 경우 119
        </p>
        <p className="mt-4 text-ink-400">© {new Date().getFullYear()} MODERN RELATION UX</p>
      </div>
    </footer>
  );
}

export function PageShell({ children, noChrome = false }: { children: ReactNode; noChrome?: boolean }) {
  return (
    <div className="flex min-h-screen flex-col">
      <Header />
      <main className="flex-1">{children}</main>
      {!noChrome && <Footer />}
    </div>
  );
}
