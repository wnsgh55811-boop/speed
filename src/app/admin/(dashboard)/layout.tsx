import Link from "next/link";
import { LogoutButton } from "../LogoutButton";

export default function AdminLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="min-h-screen bg-ivory-100">
      <header className="border-b border-warmgray-300 bg-navy-950 text-ivory-50">
        <div className="mx-auto flex max-w-5xl items-center justify-between px-5 py-4">
          <Link href="/admin" className="font-serif-kr text-lg font-medium">
            러브백 관리자
          </Link>
          <nav className="flex items-center gap-5 text-sm">
            <Link href="/admin/reviews" className="hover:text-ivory-100/80">
              후기 관리
            </Link>
            <Link href="/admin/applications" className="hover:text-ivory-100/80">
              상담 신청 관리
            </Link>
            <Link href="/" className="hover:text-ivory-100/80">
              사이트 보기
            </Link>
            <LogoutButton />
          </nav>
        </div>
      </header>
      <main className="mx-auto max-w-5xl px-5 py-10">{children}</main>
    </div>
  );
}
