"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { Container } from "@/components/Container";
import { Button } from "@/components/Button";
import { reviewCategories } from "@/lib/reviewCategories";

const initialState = {
  category: reviewCategories[0].value as string,
  nickname: "",
  ageGroup: "",
  situationTag: "",
  title: "",
  beforeContent: "",
  hardestPart: "",
  helpfulPart: "",
  afterContent: "",
  messageToOthers: "",
  isSecret: false,
  password: "",
};

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

const inputClass =
  "w-full rounded-sm border border-warmgray-300 bg-white px-4 py-2.5 text-navy-900 focus:border-navy-700 focus:outline-none";

export default function WriteReviewPage() {
  const router = useRouter();
  const [form, setForm] = useState(initialState);
  const [error, setError] = useState("");
  const [submitting, setSubmitting] = useState(false);

  function update<K extends keyof typeof initialState>(
    key: K,
    value: (typeof initialState)[K],
  ) {
    setForm((f) => ({ ...f, [key]: value }));
  }

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setSubmitting(true);
    setError("");
    try {
      const res = await fetch("/api/reviews", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(form),
      });
      const data = await res.json();
      if (!res.ok) {
        setError(data.error ?? "제출 중 문제가 발생했습니다.");
        return;
      }
      router.push("/reviews/write/complete");
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <div className="bg-ivory-50 py-16">
      <Container className="max-w-2xl">
        <div className="mb-10 flex flex-col gap-3 text-center">
          <h1 className="font-serif-kr text-2xl font-medium text-navy-900 sm:text-3xl">
            상담 후기 작성
          </h1>
          <p className="text-warmgray-600">
            작성해주신 후기는 관리자 확인 후 게시판에 노출됩니다.
          </p>
        </div>

        <form onSubmit={handleSubmit} className="flex flex-col gap-6">
          <Field label="상담 분야" required>
            <select
              className={inputClass}
              value={form.category}
              onChange={(e) => update("category", e.target.value)}
            >
              {reviewCategories.map((c) => (
                <option key={c.value} value={c.value}>
                  {c.label}
                </option>
              ))}
            </select>
          </Field>

          <div className="grid gap-6 sm:grid-cols-3">
            <Field label="닉네임" required>
              <input
                className={inputClass}
                value={form.nickname}
                onChange={(e) => update("nickname", e.target.value)}
                maxLength={30}
              />
            </Field>
            <Field label="연령/성별 (선택)">
              <input
                className={inputClass}
                placeholder="예: 20대 여성"
                value={form.ageGroup}
                onChange={(e) => update("ageGroup", e.target.value)}
              />
            </Field>
            <Field label="상황 태그 (선택)">
              <input
                className={inputClass}
                placeholder="예: 이별 후 3주"
                value={form.situationTag}
                onChange={(e) => update("situationTag", e.target.value)}
              />
            </Field>
          </div>

          <Field label="후기 제목" required>
            <input
              className={inputClass}
              value={form.title}
              onChange={(e) => update("title", e.target.value)}
              maxLength={120}
            />
          </Field>

          <Field label="1. 상담 전 어떤 상황이었나요?" required>
            <textarea
              className={inputClass}
              rows={3}
              value={form.beforeContent}
              onChange={(e) => update("beforeContent", e.target.value)}
            />
          </Field>

          <Field label="2. 가장 힘들었던 부분은 무엇이었나요?" required>
            <textarea
              className={inputClass}
              rows={3}
              value={form.hardestPart}
              onChange={(e) => update("hardestPart", e.target.value)}
            />
          </Field>

          <Field label="3. 상담에서 가장 도움 됐던 부분은 무엇인가요?" required>
            <textarea
              className={inputClass}
              rows={3}
              value={form.helpfulPart}
              onChange={(e) => update("helpfulPart", e.target.value)}
            />
          </Field>

          <Field label="4. 상담 후 생각이나 행동이 어떻게 달라졌나요?" required>
            <textarea
              className={inputClass}
              rows={3}
              value={form.afterContent}
              onChange={(e) => update("afterContent", e.target.value)}
            />
          </Field>

          <Field label="5. 비슷한 상황의 사람에게 해주고 싶은 말이 있다면?">
            <textarea
              className={inputClass}
              rows={3}
              value={form.messageToOthers}
              onChange={(e) => update("messageToOthers", e.target.value)}
            />
          </Field>

          <div className="flex flex-col gap-3 rounded-sm border border-warmgray-200 bg-white p-5">
            <label className="flex items-center gap-2 text-sm font-medium text-navy-900">
              <input
                type="checkbox"
                checked={form.isSecret}
                onChange={(e) => update("isSecret", e.target.checked)}
              />
              비밀글로 작성 (비밀번호를 아는 사람만 열람 가능)
            </label>
            {form.isSecret && (
              <input
                type="password"
                className={inputClass}
                placeholder="비밀번호 설정"
                value={form.password}
                onChange={(e) => update("password", e.target.value)}
              />
            )}
          </div>

          {error && <p className="text-sm text-burgundy-700">{error}</p>}

          <Button type="submit" size="lg" className="w-full">
            {submitting ? "제출 중..." : "후기 제출하기"}
          </Button>
        </form>
      </Container>
    </div>
  );
}
