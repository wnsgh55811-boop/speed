"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";

export default function AdminLoginPage() {
  const router = useRouter();
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setLoading(true);
    setError("");
    try {
      const res = await fetch("/api/admin/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ password }),
      });
      if (!res.ok) {
        const data = await res.json();
        setError(data.error ?? "로그인에 실패했습니다.");
        return;
      }
      router.push("/admin");
      router.refresh();
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="flex min-h-screen items-center justify-center bg-navy-950 px-5">
      <form
        onSubmit={handleSubmit}
        className="flex w-full max-w-sm flex-col gap-4 rounded-sm border border-ivory-100/15 bg-navy-900 p-8"
      >
        <h1 className="font-serif-kr text-center text-xl font-medium text-ivory-50">
          러브백 관리자
        </h1>
        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder="관리자 비밀번호"
          className="rounded-sm border border-ivory-100/20 bg-navy-950 px-4 py-2.5 text-ivory-50 focus:border-burgundy-500 focus:outline-none"
          autoFocus
        />
        {error && <p className="text-sm text-burgundy-400">{error}</p>}
        <button
          type="submit"
          className="rounded-sm bg-burgundy-700 py-2.5 font-medium text-ivory-50 hover:bg-burgundy-800"
        >
          {loading ? "확인 중..." : "로그인"}
        </button>
      </form>
    </div>
  );
}
