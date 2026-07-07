"use client";

import { useState } from "react";
import { Button } from "@/components/Button";
import { programLabel } from "@/lib/reviewCategories";
import type { Diagnosis } from "@/lib/diagnosis";
import { getResultBand } from "@/lib/diagnosis";

export function QuizClient({ diagnosis }: { diagnosis: Diagnosis }) {
  const [answers, setAnswers] = useState<boolean[]>(
    Array(diagnosis.questions.length).fill(false),
  );
  const [submitted, setSubmitted] = useState(false);

  const score = answers.filter(Boolean).length;
  const band = submitted ? getResultBand(diagnosis, score) : null;

  function toggle(i: number) {
    setAnswers((a) => a.map((v, idx) => (idx === i ? !v : v)));
  }

  if (submitted && band) {
    return (
      <div className="flex flex-col gap-6 rounded-sm border border-warmgray-200 bg-white p-8 text-center">
        <p className="text-sm text-warmgray-500">
          {score} / {diagnosis.questions.length}개 해당
        </p>
        <h2 className="font-serif-kr text-2xl font-medium text-navy-900">
          {band.title}
        </h2>
        <p className="leading-relaxed text-warmgray-700">{band.description}</p>
        <p className="text-sm text-burgundy-700">
          추천 프로그램: {programLabel(band.recommendedProgram)}
        </p>
        <div className="flex flex-col justify-center gap-3 sm:flex-row">
          <Button href={`/apply?program=${band.recommendedProgram}`} size="lg">
            추천 상담 신청하기
          </Button>
          <Button
            variant="secondary"
            onClick={() => {
              setSubmitted(false);
              setAnswers(Array(diagnosis.questions.length).fill(false));
            }}
          >
            다시 체크하기
          </Button>
        </div>
      </div>
    );
  }

  return (
    <div className="flex flex-col gap-6">
      <div className="flex flex-col gap-3">
        {diagnosis.questions.map((q, i) => (
          <label
            key={q.text}
            className="flex cursor-pointer items-center gap-4 rounded-sm border border-warmgray-200 bg-white px-6 py-4 hover:border-navy-700"
          >
            <input
              type="checkbox"
              checked={answers[i]}
              onChange={() => toggle(i)}
              className="h-4 w-4 accent-burgundy-700"
            />
            <span className="text-navy-800">{q.text}</span>
          </label>
        ))}
      </div>
      <Button size="lg" onClick={() => setSubmitted(true)} className="w-full">
        결과 확인하기
      </Button>
    </div>
  );
}
