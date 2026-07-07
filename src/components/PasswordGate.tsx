"use client";

import { useState } from "react";
import { Lock } from "lucide-react";
import { Button } from "./Button";
import { ReviewDetail, type ReviewDetailData } from "./ReviewDetail";

export function PasswordGate({ reviewId }: { reviewId: string }) {
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [review, setReview] = useState<ReviewDetailData | null>(null);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setLoading(true);
    setError("");
    try {
      const res = await fetch(`/api/reviews/${reviewId}/reveal`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ password }),
      });
      const data = await res.json();
      if (!res.ok) {
        setError(data.error ?? "확인할 수 없습니다.");
        return;
      }
      setReview(data);
    } finally {
      setLoading(false);
    }
  }

  if (review) {
    return <ReviewDetail review={review} />;
  }

  return (
    <div className="flex flex-col items-center gap-6 rounded-sm border border-warmgray-200 bg-white px-6 py-16 text-center">
      <Lock size={28} className="text-warmgray-400" />
      <p className="text-navy-800">
        비밀글입니다. 작성 시 등록한 비밀번호를 입력해주세요.
      </p>
      <form onSubmit={handleSubmit} className="flex w-full max-w-xs flex-col gap-3">
        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder="비밀번호"
          className="rounded-sm border border-warmgray-300 px-4 py-2.5 text-center focus:border-navy-700 focus:outline-none"
        />
        {error && <p className="text-sm text-burgundy-700">{error}</p>}
        <Button type="submit" className="w-full">
          {loading ? "확인 중..." : "확인"}
        </Button>
      </form>
    </div>
  );
}
