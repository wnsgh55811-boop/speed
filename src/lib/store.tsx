import { createContext, useContext, useMemo, useState, type ReactNode } from "react";
import type { Answers } from "../data/types";

interface AssessmentState {
  answers: Answers;
  stepIndex: number;
  consented: boolean;
  setAnswer: (id: string, value: string | string[]) => void;
  setStepIndex: (i: number) => void;
  setConsented: (v: boolean) => void;
  reset: () => void;
}

const AssessmentContext = createContext<AssessmentState | null>(null);

const STORAGE_KEY = "mru_assessment_v1";

function loadInitial(): { answers: Answers; stepIndex: number; consented: boolean } {
  try {
    const raw = sessionStorage.getItem(STORAGE_KEY);
    if (raw) return JSON.parse(raw);
  } catch {
    /* ignore */
  }
  return { answers: {}, stepIndex: 0, consented: false };
}

export function AssessmentProvider({ children }: { children: ReactNode }) {
  const initial = loadInitial();
  const [answers, setAnswers] = useState<Answers>(initial.answers);
  const [stepIndex, setStepIndex] = useState<number>(initial.stepIndex);
  const [consented, setConsented] = useState<boolean>(initial.consented);

  const persist = (next: { answers: Answers; stepIndex: number; consented: boolean }) => {
    try {
      sessionStorage.setItem(STORAGE_KEY, JSON.stringify(next));
    } catch {
      /* ignore */
    }
  };

  const setAnswer = (id: string, value: string | string[]) => {
    setAnswers((prev) => {
      const next = { ...prev, [id]: value };
      persist({ answers: next, stepIndex, consented });
      return next;
    });
  };

  const setStepIndexWrapped = (i: number) => {
    setStepIndex(i);
    persist({ answers, stepIndex: i, consented });
  };

  const setConsentedWrapped = (v: boolean) => {
    setConsented(v);
    persist({ answers, stepIndex, consented: v });
  };

  const reset = () => {
    setAnswers({});
    setStepIndex(0);
    setConsented(false);
    try {
      sessionStorage.removeItem(STORAGE_KEY);
    } catch {
      /* ignore */
    }
  };

  const value = useMemo(
    () => ({
      answers,
      stepIndex,
      consented,
      setAnswer,
      setStepIndex: setStepIndexWrapped,
      setConsented: setConsentedWrapped,
      reset,
    }),
    [answers, stepIndex, consented],
  );

  return <AssessmentContext.Provider value={value}>{children}</AssessmentContext.Provider>;
}

export function useAssessment() {
  const ctx = useContext(AssessmentContext);
  if (!ctx) throw new Error("useAssessment must be used within AssessmentProvider");
  return ctx;
}
