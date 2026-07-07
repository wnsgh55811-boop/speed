import type { Metadata } from "next";
import Link from "next/link";
import { ArrowRight } from "lucide-react";
import { Container } from "@/components/Container";
import { SectionHeading } from "@/components/SectionHeading";
import { diagnoses } from "@/lib/diagnosis";

export const metadata: Metadata = {
  title: "무료 진단",
  description: "결제 전, 내 관계 상태를 가볍게 점검해보는 무료 체크리스트.",
};

export default function DiagnosisPage() {
  return (
    <div>
      <section className="border-b border-warmgray-200 bg-navy-950 py-16 text-ivory-50 sm:py-20">
        <Container className="flex flex-col items-center gap-4 text-center">
          <span className="text-xs font-semibold tracking-[0.2em] text-ivory-100/70 uppercase">
            Free Diagnosis
          </span>
          <h1 className="font-serif-kr max-w-2xl text-3xl leading-snug font-medium sm:text-4xl">
            내 관계가 지금 회복 가능한 흐름인지 알고 싶다면?
          </h1>
          <p className="max-w-xl text-ivory-100/75">
            상담 신청이 아직 부담스럽다면, 무료 체크리스트로 먼저 현재
            상태를 점검해보세요.
          </p>
        </Container>
      </section>

      <section className="bg-ivory-50 py-16">
        <Container>
          <SectionHeading title="체크리스트 선택" />
          <div className="mt-10 grid gap-6 sm:grid-cols-2">
            {diagnoses.map((d) => (
              <Link
                key={d.slug}
                href={`/diagnosis/${d.slug}`}
                className="flex h-full flex-col gap-4 rounded-sm border border-warmgray-200 bg-white p-7 transition-shadow hover:shadow-md"
              >
                <h3 className="font-serif-kr text-xl font-medium text-navy-900">
                  {d.title}
                </h3>
                <p className="flex-1 leading-relaxed text-warmgray-600">
                  {d.description}
                </p>
                <span className="flex items-center gap-1 text-sm font-medium text-burgundy-700">
                  체크리스트 시작하기 <ArrowRight size={15} />
                </span>
              </Link>
            ))}
          </div>
        </Container>
      </section>
    </div>
  );
}
