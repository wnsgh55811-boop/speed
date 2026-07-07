import type { Metadata } from "next";
import { notFound } from "next/navigation";
import Link from "next/link";
import { Container } from "@/components/Container";
import { ColumnCta } from "@/components/ColumnCta";
import { columnCategoryLabel, columns, getColumnBySlug } from "@/lib/columns";

export function generateStaticParams() {
  return columns.map((c) => ({ slug: c.slug }));
}

export async function generateMetadata({
  params,
}: {
  params: Promise<{ slug: string }>;
}): Promise<Metadata> {
  const { slug } = await params;
  const column = getColumnBySlug(slug);
  return {
    title: column?.title ?? "칼럼",
    description: column?.excerpt,
  };
}

export default async function ColumnDetailPage({
  params,
}: {
  params: Promise<{ slug: string }>;
}) {
  const { slug } = await params;
  const column = getColumnBySlug(slug);

  if (!column) notFound();

  return (
    <div className="bg-ivory-50 py-16">
      <Container className="max-w-2xl">
        <article className="flex flex-col gap-8">
          <div className="flex flex-col gap-3">
            <Link
              href={`/columns?category=${column.category}`}
              className="w-fit rounded-full bg-beige-200 px-3 py-1 text-xs font-medium text-navy-800"
            >
              {columnCategoryLabel(column.category)}
            </Link>
            <h1 className="font-serif-kr text-2xl leading-snug font-medium text-navy-900 sm:text-3xl">
              {column.title}
            </h1>
            <p className="text-sm text-warmgray-500">{column.publishedAt}</p>
          </div>

          <div className="flex flex-col gap-5 text-base leading-relaxed text-navy-800 sm:text-lg">
            {column.body.map((p, i) => (
              <p key={i}>{p}</p>
            ))}
          </div>

          <ColumnCta />
        </article>
      </Container>
    </div>
  );
}
