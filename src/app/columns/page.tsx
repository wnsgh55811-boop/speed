import type { Metadata } from "next";
import Link from "next/link";
import { clsx } from "clsx";
import { Container } from "@/components/Container";
import { columnCategories, columns } from "@/lib/columns";

export const metadata: Metadata = {
  title: "블로그 칼럼",
  description: "연애, 재회, 카톡 대화, 관계 심리에 관한 러브백 칼럼.",
};

export default async function ColumnsPage({
  searchParams,
}: {
  searchParams: Promise<{ category?: string }>;
}) {
  const { category } = await searchParams;
  const list = category ? columns.filter((c) => c.category === category) : columns;

  return (
    <div>
      <section className="border-b border-warmgray-200 bg-navy-950 py-16 text-ivory-50 sm:py-20">
        <Container className="flex flex-col items-center gap-4 text-center">
          <span className="text-xs font-semibold tracking-[0.2em] text-ivory-100/70 uppercase">
            Column
          </span>
          <h1 className="font-serif-kr max-w-2xl text-3xl leading-snug font-medium sm:text-4xl">
            러브백 칼럼
          </h1>
          <p className="max-w-xl text-ivory-100/75">
            연애, 재회, 카톡 대화, 관계 심리에 대한 러브백의 분석을 읽어보세요.
          </p>
        </Container>
      </section>

      <section className="bg-ivory-50 py-14">
        <Container className="flex flex-col gap-10">
          <div className="flex flex-wrap gap-2">
            <Link
              href="/columns"
              className={clsx(
                "rounded-full border px-4 py-1.5 text-sm transition-colors",
                !category
                  ? "border-navy-900 bg-navy-900 text-ivory-50"
                  : "border-warmgray-300 text-navy-800 hover:border-navy-700",
              )}
            >
              전체
            </Link>
            {columnCategories.map((c) => (
              <Link
                key={c.value}
                href={`/columns?category=${c.value}`}
                className={clsx(
                  "rounded-full border px-4 py-1.5 text-sm transition-colors",
                  category === c.value
                    ? "border-navy-900 bg-navy-900 text-ivory-50"
                    : "border-warmgray-300 text-navy-800 hover:border-navy-700",
                )}
              >
                {c.label}
              </Link>
            ))}
          </div>

          <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
            {list.map((col) => (
              <Link
                key={col.slug}
                href={`/columns/${col.slug}`}
                className="flex h-full flex-col gap-4 rounded-sm border border-warmgray-200 bg-white p-6 transition-shadow hover:shadow-md"
              >
                <span className="w-fit rounded-full bg-beige-200 px-3 py-1 text-xs font-medium text-navy-800">
                  {columnCategories.find((c) => c.value === col.category)?.label}
                </span>
                <h3 className="font-serif-kr text-lg leading-snug font-medium text-navy-900">
                  {col.title}
                </h3>
                <p className="line-clamp-2 flex-1 text-sm leading-relaxed text-warmgray-600">
                  {col.excerpt}
                </p>
                <span className="text-xs text-warmgray-500">{col.publishedAt}</span>
              </Link>
            ))}
          </div>
        </Container>
      </section>
    </div>
  );
}
