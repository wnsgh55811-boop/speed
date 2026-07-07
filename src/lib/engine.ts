import {
  basicInfoSteps,
  attachmentSteps,
  conflictSteps,
  contactSteps,
  lifestyleSteps,
  relationshipEnvSteps,
  relationshipFollowUps,
  relationshipStatusStep,
} from "../data/lifestyleQuestions";
import {
  bipolarSignalStep,
  buildScaleStep,
  crisisStep,
  domainDefinitions,
  quickScreenStep,
} from "../data/mentalHealth";
import {
  diagnosisImpactStep,
  existingDiagnosisStep,
  medicationImpactStep,
  medicationStatusStep,
} from "../data/diagnosisMedication";
import { resultTypes, type SignalKey } from "../data/resultTypes";
import type {
  Answers,
  DomainResult,
  MentalHealthDomain,
  Option,
  ScoreKey,
  Step,
} from "../data/types";

const scoreKeys: ScoreKey[] = [
  "contactSensitivity",
  "attachmentAnxiety",
  "avoidance",
  "envRestriction",
  "familyInfluence",
  "oppositeFriendConfusion",
  "moodSwingRisk",
];

const domainOrder: MentalHealthDomain[] = ["depression", "anxiety", "ocd", "adhd", "insomnia", "panic"];

function findOption(options: Option[], value: string): Option | undefined {
  return options.find((o) => o.value === value);
}

/** Builds the ordered list of steps given the answers collected so far. */
export function buildSteps(answers: Answers): Step[] {
  const steps: Step[] = [...basicInfoSteps, relationshipStatusStep];

  const relStatus = answers.relationshipStatus as string | undefined;
  if (relStatus && relationshipFollowUps[relStatus]) {
    steps.push(relationshipFollowUps[relStatus]);
  }

  steps.push(...lifestyleSteps, ...relationshipEnvSteps, ...contactSteps, ...conflictSteps, ...attachmentSteps);

  steps.push({
    kind: "info",
    id: "mentalHealthIntro",
    section: "감정·컨디션 스크리닝",
    title: "감정과 컨디션에 대한 질문",
    body: [
      "이제 관계에 영향을 줄 수 있는 감정·컨디션 질문이 나옵니다.",
      "이 질문은 병명을 확정하기 위한 것이 아니라, 연락, 약속, 감정표현, 갈등반응에 영향을 주는 심리적 요인을 확인하기 위한 것입니다.",
      "답변이 불편한 문항은 건너뛸 수 있습니다.",
    ],
    cta: "다음",
  });

  steps.push(quickScreenStep);

  const primary = answers.quickScreen as MentalHealthDomain | "none" | undefined;
  if (primary && primary !== "none") {
    steps.push(buildScaleStep(primary, false));
    for (const domain of domainOrder) {
      if (domain !== primary) steps.push(buildScaleStep(domain, true));
    }
  } else if (primary === "none") {
    for (const domain of domainOrder) steps.push(buildScaleStep(domain, true));
  }

  steps.push(bipolarSignalStep);
  steps.push(existingDiagnosisStep);

  const diagnosis = answers.existingDiagnosis as string[] | undefined;
  if (diagnosis && diagnosis.length > 0 && !diagnosis.includes("없음") && !diagnosis.includes("답변하지 않음")) {
    steps.push(diagnosisImpactStep);
  }

  steps.push(medicationStatusStep);
  const medStatus = answers.medicationStatus as string | undefined;
  if (medStatus && medStatus !== "없음" && medStatus !== "비공개") {
    steps.push(medicationImpactStep);
  }

  steps.push(crisisStep);

  return steps;
}

function combineProbabilistic(values: number[]): number {
  if (values.length === 0) return 0;
  let survive = 1;
  for (const v of values) {
    survive *= 1 - Math.min(Math.max(v, 0), 100) / 100;
  }
  return Math.round((1 - survive) * 100);
}

function collectSignalScores(answers: Answers, allSteps: Step[]): Record<ScoreKey, number> {
  const contributions: Record<ScoreKey, number[]> = {
    contactSensitivity: [],
    attachmentAnxiety: [],
    avoidance: [],
    envRestriction: [],
    familyInfluence: [],
    oppositeFriendConfusion: [],
    moodSwingRisk: [],
  };

  for (const step of allSteps) {
    if (step.kind !== "single" && step.kind !== "multi") continue;
    const answer = answers[step.id];
    if (!answer) continue;
    const values = Array.isArray(answer) ? answer : [answer];
    for (const val of values) {
      const opt = findOption(step.options, val);
      if (!opt?.tags) continue;
      for (const key of scoreKeys) {
        const contribution = opt.tags[key];
        if (contribution) contributions[key].push(contribution);
      }
    }
  }

  const result = {} as Record<ScoreKey, number>;
  for (const key of scoreKeys) result[key] = combineProbabilistic(contributions[key]);
  return result;
}

function classifyLevel(score: number, levels: { max: number; label: string }[]): string {
  for (const l of levels) {
    if (score <= l.max) return l.label;
  }
  return levels[levels.length - 1].label;
}

function computeDomainResults(answers: Answers): DomainResult[] {
  const primary = answers.quickScreen as MentalHealthDomain | "none" | undefined;
  const results: DomainResult[] = [];

  for (const domain of domainOrder) {
    const def = domainDefinitions[domain];
    const isLight = !(primary === domain);
    const stepId = `scale_${domain}_${isLight ? "light" : "full"}`;
    const raw = answers[stepId] as string[] | undefined;

    const maxItemScore = def.scaleOptions[def.scaleOptions.length - 1].score;
    const fullMax = def.items.length * maxItemScore;
    const lightItems = def.lightItemIdx.length;
    const lightMax = lightItems * maxItemScore;

    let rawScore = 0;
    if (raw) {
      rawScore = raw.reduce((sum, v) => sum + Number(v || 0), 0);
    }

    const estimatedFull = isLight && lightMax > 0 ? Math.round((rawScore / lightMax) * fullMax) : rawScore;
    const normalized = fullMax > 0 ? Math.round((estimatedFull / fullMax) * 100) : 0;
    const level = classifyLevel(estimatedFull, def.levels) as DomainResult["level"];

    results.push({
      domain,
      rawScore: estimatedFull,
      maxScore: fullMax,
      normalized: Math.min(100, Math.max(0, normalized)),
      level,
      isLight,
    });
  }

  return results;
}

export interface CrisisAssessment {
  risk: "none" | "low" | "mid" | "high" | "danger";
  shouldInterrupt: boolean;
}

function computeCrisis(answers: Answers): CrisisAssessment {
  const val = answers.crisisCheck as string | undefined;
  const opt = crisisStep.options.find((o) => o.value === val);
  const risk = opt?.risk ?? "none";
  return { risk, shouldInterrupt: risk === "high" || risk === "danger" };
}

export interface ResultPayload {
  signals: Record<ScoreKey, number>;
  domainResults: DomainResult[];
  crisis: CrisisAssessment;
  primaryType: (typeof resultTypes)[number];
  secondaryType: (typeof resultTypes)[number];
  topCauses: string[];
  summarySentence: string;
}

function scoreType(type: (typeof resultTypes)[number], signals: Record<SignalKey, number>): number {
  let total = 0;
  let weightSum = 0;
  for (const [key, weight] of Object.entries(type.weights)) {
    const s = signals[key as SignalKey] ?? 0;
    total += s * (weight ?? 0);
    weightSum += weight ?? 0;
  }
  return weightSum > 0 ? total / weightSum : 0;
}

export function computeResult(answers: Answers): ResultPayload {
  const allSteps = buildSteps(answers);
  const scoreSignals = collectSignalScores(answers, allSteps);
  const domainResults = computeDomainResults(answers);
  const crisis = computeCrisis(answers);

  const signals: Record<SignalKey, number> = {
    ...scoreSignals,
    depression: domainResults.find((d) => d.domain === "depression")!.normalized,
    anxiety: domainResults.find((d) => d.domain === "anxiety")!.normalized,
    ocd: domainResults.find((d) => d.domain === "ocd")!.normalized,
    adhd: domainResults.find((d) => d.domain === "adhd")!.normalized,
    insomnia: domainResults.find((d) => d.domain === "insomnia")!.normalized,
    panic: domainResults.find((d) => d.domain === "panic")!.normalized,
  };

  const moodSignal = signals.moodSwingRisk;
  const bipolarAns = answers.moodSwingSignal as string | undefined;
  if (bipolarAns && bipolarAns !== "없음") {
    signals.moodSwingRisk = combineProbabilistic([moodSignal, 55]);
  }

  const ranked = [...resultTypes].sort((a, b) => scoreType(b, signals) - scoreType(a, signals));
  const primaryType = ranked[0];
  const secondaryType = ranked[1];

  const topCauses = Array.from(new Set([...primaryType.coreCauses, ...secondaryType.coreCauses])).slice(0, 3);

  const summarySentence = `당신은 현재 ${primaryType.name} + ${secondaryType.name}에 가깝습니다.`;

  return { signals, domainResults, crisis, primaryType, secondaryType, topCauses, summarySentence };
}
