import { useState } from "react";
import type { Step } from "../data/types";

interface Props {
  step: Step;
  currentAnswer?: string | string[];
  onAnswer: (value: string | string[]) => void;
  onNext: () => void;
  onSkip: () => void;
}

function SectionTag({ children }: { children: string }) {
  return (
    <p className="mb-3 text-xs font-semibold tracking-[0.18em] text-plum-600 uppercase">{children}</p>
  );
}

function SkipLink({ onSkip }: { onSkip: () => void }) {
  return (
    <button
      onClick={onSkip}
      className="mt-6 block text-center text-xs text-ink-400 underline-offset-4 transition hover:text-ink-600 hover:underline"
    >
      건너뛰기
    </button>
  );
}

function SingleChoiceView({ step, onAnswer, onNext, onSkip }: Props & { step: Extract<Step, { kind: "single" }> }) {
  const [selected, setSelected] = useState<string | null>(null);

  const pick = (value: string) => {
    setSelected(value);
    onAnswer(value);
    window.setTimeout(onNext, 220);
  };

  return (
    <div className="animate-fade-up">
      <SectionTag>{step.section}</SectionTag>
      <h2 className="font-serif-kr text-xl leading-snug font-semibold text-ink-950 sm:text-2xl">{step.question}</h2>
      {step.help && <p className="mt-2 text-sm text-ink-500">{step.help}</p>}
      <div className="mt-7 grid gap-2.5">
        {step.options.map((opt) => (
          <button
            key={opt.value}
            onClick={() => pick(opt.value)}
            className={`rounded-xl border px-5 py-3.5 text-left text-[15px] transition ${
              selected === opt.value
                ? "border-plum-600 bg-plum-100 text-plum-900"
                : "border-ink-100 bg-white text-ink-800 hover:border-plum-300 hover:bg-plum-50"
            }`}
          >
            {opt.label}
          </button>
        ))}
      </div>
      <SkipLink onSkip={onSkip} />
    </div>
  );
}

function MultiChoiceView({ step, currentAnswer, onAnswer, onNext, onSkip }: Props & { step: Extract<Step, { kind: "multi" }> }) {
  const initial = Array.isArray(currentAnswer) ? currentAnswer : [];
  const [selected, setSelected] = useState<string[]>(initial);

  const toggle = (value: string) => {
    setSelected((prev) => {
      const has = prev.includes(value);
      if (has) return prev.filter((v) => v !== value);
      if (step.max && prev.length >= step.max) return prev;
      return [...prev, value];
    });
  };

  const submit = () => {
    onAnswer(selected);
    onNext();
  };

  return (
    <div className="animate-fade-up">
      <SectionTag>{step.section}</SectionTag>
      <h2 className="font-serif-kr text-xl leading-snug font-semibold text-ink-950 sm:text-2xl">{step.question}</h2>
      {step.help && <p className="mt-2 text-sm text-ink-500">{step.help}</p>}
      <div className="mt-7 grid gap-2.5 sm:grid-cols-2">
        {step.options.map((opt) => {
          const active = selected.includes(opt.value);
          return (
            <button
              key={opt.value}
              onClick={() => toggle(opt.value)}
              className={`rounded-xl border px-4 py-3 text-left text-sm transition ${
                active
                  ? "border-plum-600 bg-plum-100 text-plum-900"
                  : "border-ink-100 bg-white text-ink-800 hover:border-plum-300 hover:bg-plum-50"
              }`}
            >
              {opt.label}
            </button>
          );
        })}
      </div>
      <button
        onClick={submit}
        disabled={selected.length === 0}
        className="mt-7 w-full rounded-full bg-ink-950 px-6 py-3.5 text-[15px] font-medium text-paper transition enabled:hover:bg-plum-800 disabled:cursor-not-allowed disabled:opacity-30"
      >
        다음
      </button>
      <SkipLink onSkip={onSkip} />
    </div>
  );
}

function InfoView({ step, onNext }: Props & { step: Extract<Step, { kind: "info" }> }) {
  return (
    <div className="animate-fade-up text-center">
      <SectionTag>{step.section}</SectionTag>
      <h2 className="font-serif-kr text-xl font-semibold text-ink-950 sm:text-2xl">{step.title}</h2>
      <div className="mx-auto mt-5 max-w-md space-y-3 text-sm leading-relaxed text-ink-600">
        {step.body.map((b, i) => (
          <p key={i}>{b}</p>
        ))}
      </div>
      <button
        onClick={onNext}
        className="mt-8 rounded-full bg-ink-950 px-8 py-3.5 text-[15px] font-medium text-paper transition hover:bg-plum-800"
      >
        {step.cta}
      </button>
    </div>
  );
}

function ScaleView({ step, currentAnswer, onAnswer, onNext, onSkip }: Props & { step: Extract<Step, { kind: "scale" }> }) {
  const initial = Array.isArray(currentAnswer) ? currentAnswer : step.items.map(() => "");
  const [values, setValues] = useState<string[]>(initial.length === step.items.length ? initial : step.items.map(() => ""));

  const setItem = (idx: number, score: number) => {
    setValues((prev) => {
      const next = [...prev];
      next[idx] = String(score);
      return next;
    });
  };

  const allAnswered = values.every((v) => v !== "");

  const submit = () => {
    onAnswer(values);
    onNext();
  };

  return (
    <div className="animate-fade-up">
      <SectionTag>{step.section}</SectionTag>
      <h2 className="font-serif-kr text-xl font-semibold text-ink-950 sm:text-2xl">{step.title}</h2>
      <p className="mt-2 text-sm leading-relaxed text-ink-500">{step.intro}</p>
      <p className="mt-3 text-xs font-medium text-ink-400">{step.timeframe}, 아래 경험이 얼마나 있었나요?</p>

      <div className="mt-6 space-y-4">
        {step.items.map((item, idx) => (
          <div key={idx} className="rounded-xl border border-ink-100 bg-white p-4">
            <p className="mb-3 text-sm font-medium text-ink-800">{idx + 1}. {item}</p>
            <div className="flex flex-wrap gap-2">
              {step.scaleOptions.map((so) => (
                <button
                  key={so.label}
                  onClick={() => setItem(idx, so.score)}
                  className={`rounded-full border px-3 py-1.5 text-xs transition ${
                    values[idx] === String(so.score)
                      ? "border-plum-600 bg-plum-600 text-white"
                      : "border-ink-200 bg-paper text-ink-600 hover:border-plum-300"
                  }`}
                >
                  {so.label}
                </button>
              ))}
            </div>
          </div>
        ))}
      </div>

      <button
        onClick={submit}
        disabled={!allAnswered}
        className="mt-7 w-full rounded-full bg-ink-950 px-6 py-3.5 text-[15px] font-medium text-paper transition enabled:hover:bg-plum-800 disabled:cursor-not-allowed disabled:opacity-30"
      >
        다음
      </button>
      <SkipLink onSkip={onSkip} />
    </div>
  );
}

function CrisisView({ step, onAnswer, onNext }: Props & { step: Extract<Step, { kind: "crisis" }> }) {
  const [selected, setSelected] = useState<string | null>(null);

  const pick = (value: string) => {
    setSelected(value);
    onAnswer(value);
    window.setTimeout(onNext, 220);
  };

  return (
    <div className="animate-fade-up">
      <SectionTag>{step.section}</SectionTag>
      <h2 className="font-serif-kr text-xl leading-snug font-semibold text-ink-950 sm:text-2xl">{step.question}</h2>
      <p className="mt-2 text-sm text-ink-500">
        솔직한 답변이 더 정확한 안내로 이어집니다. 이 질문은 건너뛸 수 없지만, 편한 선택지를 골라주세요.
      </p>
      <div className="mt-7 grid gap-2.5">
        {step.options.map((opt) => (
          <button
            key={opt.value}
            onClick={() => pick(opt.value)}
            className={`rounded-xl border px-5 py-3.5 text-left text-[15px] transition ${
              selected === opt.value
                ? "border-rose-500 bg-rose-100 text-ink-950"
                : "border-ink-100 bg-white text-ink-800 hover:border-rose-300 hover:bg-rose-100/40"
            }`}
          >
            {opt.label}
          </button>
        ))}
      </div>
    </div>
  );
}

export function StepRenderer(props: Props) {
  switch (props.step.kind) {
    case "single":
      return <SingleChoiceView {...props} step={props.step} />;
    case "multi":
      return <MultiChoiceView {...props} step={props.step} />;
    case "info":
      return <InfoView {...props} step={props.step} />;
    case "scale":
      return <ScaleView {...props} step={props.step} />;
    case "crisis":
      return <CrisisView {...props} step={props.step} />;
    default:
      return null;
  }
}
