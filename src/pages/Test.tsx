import { useEffect, useMemo } from "react";
import { useNavigate } from "react-router-dom";
import { PageShell } from "../components/Layout";
import { ProgressBar } from "../components/ProgressBar";
import { StepRenderer } from "../components/StepRenderer";
import { buildSteps } from "../lib/engine";
import { useAssessment } from "../lib/store";

export default function Test() {
  const navigate = useNavigate();
  const { answers, stepIndex, setStepIndex, setAnswer, consented } = useAssessment();

  const steps = useMemo(() => buildSteps(answers), [answers]);
  const clampedIndex = Math.min(stepIndex, steps.length - 1);
  const step = steps[clampedIndex];

  useEffect(() => {
    if (!consented) navigate("/consent", { replace: true });
  }, [consented, navigate]);

  useEffect(() => {
    if (stepIndex >= steps.length) {
      navigate("/result", { replace: true });
    }
  }, [stepIndex, steps.length, navigate]);

  if (!step) return null;

  const progress = ((clampedIndex + 1) / (steps.length + 1)) * 100;

  const goNext = () => setStepIndex(clampedIndex + 1);
  const goBack = () => setStepIndex(Math.max(0, clampedIndex - 1));
  const handleAnswer = (value: string | string[]) => setAnswer(step.id, value);
  const handleSkip = () => goNext();

  return (
    <PageShell noChrome>
      <div className="mx-auto flex min-h-screen max-w-xl flex-col px-5 py-8 sm:px-8">
        <div className="mb-8 flex items-center gap-4">
          <button
            onClick={goBack}
            disabled={clampedIndex === 0}
            className="text-ink-400 transition hover:text-ink-700 disabled:opacity-0"
            aria-label="이전"
          >
            ←
          </button>
          <ProgressBar value={progress} />
        </div>

        <div className="flex-1" key={step.id}>
          <StepRenderer
            step={step}
            currentAnswer={answers[step.id]}
            onAnswer={handleAnswer}
            onNext={goNext}
            onSkip={handleSkip}
          />
        </div>
      </div>
    </PageShell>
  );
}
