import type { Metadata } from "next";
import { notFound } from "next/navigation";
import { Container } from "@/components/Container";
import { diagnoses, getDiagnosisBySlug } from "@/lib/diagnosis";
import { QuizClient } from "./QuizClient";

export function generateStaticParams() {
  return diagnoses.map((d) => ({ slug: d.slug }));
}

export async function generateMetadata({
  params,
}: {
  params: Promise<{ slug: string }>;
}): Promise<Metadata> {
  const { slug } = await params;
  const diagnosis = getDiagnosisBySlug(slug);
  return { title: diagnosis?.title ?? "무료 진단" };
}

export default async function DiagnosisDetailPage({
  params,
}: {
  params: Promise<{ slug: string }>;
}) {
  const { slug } = await params;
  const diagnosis = getDiagnosisBySlug(slug);

  if (!diagnosis) notFound();

  return (
    <div className="bg-ivory-50 py-16">
      <Container className="max-w-xl">
        <div className="mb-10 flex flex-col gap-3 text-center">
          <h1 className="font-serif-kr text-2xl font-medium text-navy-900 sm:text-3xl">
            {diagnosis.title}
          </h1>
          <p className="text-warmgray-600">
            해당하는 항목을 모두 체크한 뒤 결과를 확인해보세요.
          </p>
        </div>
        <QuizClient diagnosis={diagnosis} />
      </Container>
    </div>
  );
}
