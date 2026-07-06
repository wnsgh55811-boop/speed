import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { PageShell } from "../components/Layout";
import { useAssessment } from "../lib/store";

const TOPICS = [
  "생활환경",
  "가족 및 친구관계",
  "연애상태",
  "연락과 갈등반응",
  "감정 및 컨디션 변화",
  "정신건강 진단 경험",
  "약복용 여부",
  "자해 및 위기 위험 여부",
];

const CHECKS = [
  "민감한 질문이 포함될 수 있음을 이해했습니다.",
  "본 결과가 의료 진단이 아니라 자기이해용 분석임을 이해했습니다.",
  "위기 위험이 높게 감지될 경우 도움받을 수 있는 기관 안내가 표시될 수 있음을 이해했습니다.",
];

export default function Consent() {
  const navigate = useNavigate();
  const { setConsented } = useAssessment();
  const [checked, setChecked] = useState<boolean[]>([false, false, false]);

  const allChecked = checked.every(Boolean);

  const toggle = (i: number) => {
    setChecked((prev) => prev.map((v, idx) => (idx === i ? !v : v)));
  };

  const start = () => {
    setConsented(true);
    navigate("/test");
  };

  return (
    <PageShell noChrome>
      <div className="mx-auto flex min-h-[calc(100vh-73px)] max-w-2xl flex-col justify-center px-5 py-16 sm:px-8">
        <p className="text-xs font-semibold tracking-[0.2em] text-plum-600 uppercase">시작 전에</p>
        <h1 className="font-serif-kr mt-3 text-2xl font-semibold text-ink-950 sm:text-[28px]">
          분석을 위해 다음 정보를 선택적으로 묻습니다
        </h1>

        <div className="mt-7 grid grid-cols-2 gap-2 sm:grid-cols-4">
          {TOPICS.map((t) => (
            <span
              key={t}
              className="rounded-lg border border-ink-100 bg-white px-3 py-2 text-center text-xs text-ink-600"
            >
              {t}
            </span>
          ))}
        </div>

        <div className="mt-8 space-y-2 rounded-2xl border border-ink-100 bg-white p-5 text-sm leading-relaxed text-ink-600">
          <p>민감한 질문은 건너뛸 수 있습니다.</p>
          <p>진단명과 약복용 정보는 사용자가 직접 선택하거나 입력한 경우에만 분석에 반영됩니다.</p>
        </div>

        <div className="mt-8 space-y-3">
          {CHECKS.map((c, i) => (
            <label
              key={c}
              className="flex cursor-pointer items-start gap-3 rounded-xl border border-ink-100 bg-white p-4 transition hover:border-plum-300"
            >
              <input
                type="checkbox"
                checked={checked[i]}
                onChange={() => toggle(i)}
                className="mt-0.5 h-4 w-4 shrink-0 accent-plum-700"
              />
              <span className="text-sm text-ink-700">{c}</span>
            </label>
          ))}
        </div>

        <button
          onClick={start}
          disabled={!allChecked}
          className="mt-9 w-full rounded-full bg-ink-950 px-7 py-4 text-[15px] font-medium text-paper transition enabled:hover:bg-plum-800 disabled:cursor-not-allowed disabled:opacity-30"
        >
          동의하고 시작하기
        </button>
      </div>
    </PageShell>
  );
}
