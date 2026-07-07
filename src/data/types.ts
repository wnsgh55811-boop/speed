export type ScoreKey =
  | "contactSensitivity"
  | "attachmentAnxiety"
  | "avoidance"
  | "envRestriction"
  | "familyInfluence"
  | "oppositeFriendConfusion"
  | "moodSwingRisk";

export type ScoreTags = Partial<Record<ScoreKey, number>>;

export interface Option {
  label: string;
  value: string;
  tags?: ScoreTags;
}

export interface SingleChoiceStep {
  kind: "single";
  id: string;
  section: string;
  question: string;
  help?: string;
  options: Option[];
}

export interface MultiChoiceStep {
  kind: "multi";
  id: string;
  section: string;
  question: string;
  help?: string;
  max?: number;
  options: Option[];
}

export interface InfoStep {
  kind: "info";
  id: string;
  section: string;
  title: string;
  body: string[];
  cta: string;
}

export type ScaleOption = { label: string; score: number };

export interface ScaleQuestionnaireStep {
  kind: "scale";
  id: string;
  section: string;
  domain: MentalHealthDomain;
  title: string;
  intro: string;
  timeframe: string;
  items: string[];
  scaleOptions: ScaleOption[];
  light?: boolean;
}

export interface CrisisCheckStep {
  kind: "crisis";
  id: string;
  section: string;
  question: string;
  options: { label: string; value: string; risk: "none" | "low" | "mid" | "high" | "danger" }[];
}

export type Step =
  | SingleChoiceStep
  | MultiChoiceStep
  | InfoStep
  | ScaleQuestionnaireStep
  | CrisisCheckStep;

export type MentalHealthDomain =
  | "depression"
  | "anxiety"
  | "ocd"
  | "adhd"
  | "insomnia"
  | "panic";

export interface DomainResult {
  domain: MentalHealthDomain;
  rawScore: number;
  maxScore: number;
  normalized: number; // 0-100
  level: "낮음" | "경미" | "주의" | "중간" | "높음" | "매우 높음";
  isLight: boolean;
}

export type Answers = Record<string, string | string[]>;
