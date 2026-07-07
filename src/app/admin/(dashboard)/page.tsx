import Link from "next/link";
import { prisma } from "@/lib/prisma";

export default async function AdminDashboardPage() {
  const [pendingReviews, approvedReviews, newApplications, totalApplications] =
    await Promise.all([
      prisma.review.count({ where: { status: "PENDING" } }),
      prisma.review.count({ where: { status: "APPROVED" } }),
      prisma.application.count({ where: { status: "NEW" } }),
      prisma.application.count(),
    ]);

  const cards = [
    { label: "승인 대기 후기", value: pendingReviews, href: "/admin/reviews" },
    { label: "게시 중인 후기", value: approvedReviews, href: "/admin/reviews" },
    { label: "신규 상담 신청", value: newApplications, href: "/admin/applications" },
    { label: "전체 상담 신청", value: totalApplications, href: "/admin/applications" },
  ];

  return (
    <div className="flex flex-col gap-8">
      <h1 className="font-serif-kr text-2xl font-medium text-navy-900">대시보드</h1>
      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        {cards.map((c) => (
          <Link
            key={c.label}
            href={c.href}
            className="flex flex-col gap-2 rounded-sm border border-warmgray-200 bg-white p-6 hover:shadow-md"
          >
            <span className="text-sm text-warmgray-500">{c.label}</span>
            <span className="font-serif-kr text-3xl font-medium text-navy-900">
              {c.value}
            </span>
          </Link>
        ))}
      </div>
    </div>
  );
}
