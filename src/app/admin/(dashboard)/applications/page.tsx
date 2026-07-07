import Link from "next/link";
import { clsx } from "clsx";
import { prisma } from "@/lib/prisma";
import { programLabel } from "@/lib/reviewCategories";
import { updateApplicationMemo, updateApplicationStatus } from "../../actions";

const statusLabel: Record<string, string> = {
  NEW: "신규",
  CONTACTED: "연락함",
  SCHEDULED: "일정확정",
  COMPLETED: "상담완료",
  CANCELED: "취소",
};

const statusOrder = ["NEW", "CONTACTED", "SCHEDULED", "COMPLETED", "CANCELED"];

export default async function AdminApplicationsPage({
  searchParams,
}: {
  searchParams: Promise<{ status?: string }>;
}) {
  const { status } = await searchParams;

  const applications = await prisma.application.findMany({
    where: status ? { status: status as never } : {},
    orderBy: { createdAt: "desc" },
  });

  return (
    <div className="flex flex-col gap-6">
      <h1 className="font-serif-kr text-2xl font-medium text-navy-900">
        상담 신청 관리
      </h1>

      <div className="flex flex-wrap gap-2">
        <Link
          href="/admin/applications"
          className={clsx(
            "rounded-full border px-4 py-1.5 text-sm",
            !status
              ? "border-navy-900 bg-navy-900 text-ivory-50"
              : "border-warmgray-300 text-navy-800",
          )}
        >
          전체
        </Link>
        {statusOrder.map((s) => (
          <Link
            key={s}
            href={`/admin/applications?status=${s}`}
            className={clsx(
              "rounded-full border px-4 py-1.5 text-sm",
              status === s
                ? "border-navy-900 bg-navy-900 text-ivory-50"
                : "border-warmgray-300 text-navy-800",
            )}
          >
            {statusLabel[s]}
          </Link>
        ))}
      </div>

      <div className="flex flex-col gap-4">
        {applications.length === 0 && (
          <p className="py-10 text-center text-warmgray-500">
            해당하는 상담 신청이 없습니다.
          </p>
        )}
        {applications.map((a) => (
          <div key={a.id} className="rounded-sm border border-warmgray-200 bg-white p-5">
            <div className="mb-3 flex flex-wrap items-center justify-between gap-2">
              <div className="flex flex-wrap items-center gap-2 text-sm">
                <span className="rounded-full bg-beige-200 px-2 py-0.5 text-navy-800">
                  {programLabel(a.program)}
                </span>
                <span className="font-medium text-navy-900">{a.name}</span>
                <span className="text-warmgray-500">{a.contact}</span>
              </div>
              <span className="text-xs text-warmgray-500">
                {new Date(a.createdAt).toLocaleString("ko-KR")}
              </span>
            </div>

            {a.preferredTime && (
              <p className="mb-1 text-sm text-warmgray-600">
                희망 시간대: {a.preferredTime}
              </p>
            )}
            <p className="mb-2 text-sm whitespace-pre-line text-navy-800">
              {a.situation}
            </p>
            {a.goal && (
              <p className="mb-4 text-sm whitespace-pre-line text-warmgray-600">
                목표: {a.goal}
              </p>
            )}

            <div className="mb-4 flex flex-wrap gap-2">
              {statusOrder
                .filter((s) => s !== a.status)
                .map((s) => (
                  <form key={s} action={updateApplicationStatus.bind(null, a.id, s as never)}>
                    <button className="rounded-sm border border-warmgray-300 px-3 py-1 text-xs text-navy-800 hover:border-navy-700">
                      {statusLabel[s]}(으)로 변경
                    </button>
                  </form>
                ))}
              <span className="rounded-sm bg-navy-900 px-3 py-1 text-xs text-ivory-50">
                현재: {statusLabel[a.status]}
              </span>
            </div>

            <form
              action={updateApplicationMemo.bind(null, a.id)}
              className="flex gap-2"
            >
              <input
                name="memo"
                defaultValue={a.memo ?? ""}
                placeholder="관리자 메모"
                className="flex-1 rounded-sm border border-warmgray-300 px-3 py-1.5 text-sm focus:border-navy-700 focus:outline-none"
              />
              <button className="rounded-sm bg-navy-900 px-3 py-1.5 text-xs text-ivory-50 hover:bg-navy-800">
                메모 저장
              </button>
            </form>
          </div>
        ))}
      </div>
    </div>
  );
}
