"use client";

import { useState } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import { Button } from "./Button";
import { programTypes } from "@/lib/reviewCategories";

const inputClass =
  "w-full rounded-sm border border-warmgray-300 bg-white px-4 py-2.5 text-navy-900 focus:border-navy-700 focus:outline-none";

function Field({
  label,
  children,
  required,
}: {
  label: string;
  children: React.ReactNode;
  required?: boolean;
}) {
  return (
    <label className="flex flex-col gap-2">
      <span className="text-sm font-medium text-navy-900">
        {label}
        {required && <span className="ml-1 text-burgundy-700">*</span>}
      </span>
      {children}
    </label>
  );
}

export function ApplyForm() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const initialProgram = searchParams.get("program") ?? "UNSURE";

  const [form, setForm] = useState({
    program: programTypes.some((p) => p.value === initialProgram)
      ? initialProgram
      : "UNSURE",
    name: "",
    contact: "",
    preferredTime: "",
    situation: "",
    goal: "",
  });
  const [error, setError] = useState("");
  const [submitting, setSubmitting] = useState(false);

  function update<K extends keyof typeof form>(key: K, value: (typeof form)[K]) {
    setForm((f) => ({ ...f, [key]: value }));
  }

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setSubmitting(true);
    setError("");
    try {
      const res = await fetch("/api/applications", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(form),
      });
      const data = await res.json();
      if (!res.ok) {
        setError(data.error ?? "제출 중 문제가 발생했습니다.");
        return;
      }
      router.push("/apply/complete");
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <form onSubmit={handleSubmit} className="flex flex-col gap-6">
      <Field label="상담 상품" required>
        <select
          className={inputClass}
          value={form.program}
          onChange={(e) => update("program", e.target.value)}
        >
          {programTypes.map((p) => (
            <option key={p.value} value={p.value}>
              {p.label}
            </option>
          ))}
        </select>
      </Field>

      <div className="grid gap-6 sm:grid-cols-2">
        <Field label="이름 또는 닉네임" required>
          <input
            className={inputClass}
            value={form.name}
            onChange={(e) => update("name", e.target.value)}
            maxLength={30}
          />
        </Field>
        <Field label="연락처 (전화번호 또는 카카오ID)" required>
          <input
            className={inputClass}
            value={form.contact}
            onChange={(e) => update("contact", e.target.value)}
            maxLength={60}
          />
        </Field>
      </div>

      <Field label="상담 희망 시간대 (선택)">
        <input
          className={inputClass}
          placeholder="예: 평일 저녁, 주말 오후"
          value={form.preferredTime}
          onChange={(e) => update("preferredTime", e.target.value)}
        />
      </Field>

      <Field label="현재 상황을 간단히 적어주세요" required>
        <textarea
          className={inputClass}
          rows={5}
          placeholder="관계 기간, 이별 시점, 갈등 원인, 마지막 대화, 현재 연락 상태, 상대의 반응 등을 적어주시면 상담에 도움이 됩니다."
          value={form.situation}
          onChange={(e) => update("situation", e.target.value)}
        />
      </Field>

      <Field label="상담을 통해 원하는 것 (선택)">
        <textarea
          className={inputClass}
          rows={3}
          value={form.goal}
          onChange={(e) => update("goal", e.target.value)}
        />
      </Field>

      {error && <p className="text-sm text-burgundy-700">{error}</p>}

      <Button type="submit" size="lg" className="w-full">
        {submitting ? "제출 중..." : "상담 신청서 제출하기"}
      </Button>
    </form>
  );
}
