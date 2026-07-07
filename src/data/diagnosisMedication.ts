import type { MultiChoiceStep, SingleChoiceStep } from "./types";

export const existingDiagnosisStep: MultiChoiceStep = {
  kind: "multi",
  id: "existingDiagnosis",
  section: "진단명 직접 확인",
  question: "현재 또는 과거에 전문가에게 진단받은 적이 있는 항목이 있나요?",
  help: "여러 개를 선택할 수 있습니다. 답변하고 싶지 않다면 건너뛰어도 괜찮습니다.",
  max: 4,
  options: [
    { label: "없음", value: "없음" },
    { label: "우울증", value: "우울증" },
    { label: "불안장애", value: "불안장애" },
    { label: "공황장애", value: "공황장애" },
    { label: "강박증/OCD", value: "강박증" },
    { label: "ADHD", value: "ADHD" },
    { label: "불면증/수면장애", value: "불면증" },
    { label: "양극성장애/조울 관련", value: "양극성장애" },
    { label: "섭식장애", value: "섭식장애" },
    { label: "충동조절 문제", value: "충동조절" },
    { label: "알코올/게임/약물 등 의존 문제", value: "의존문제" },
    { label: "PTSD/트라우마 관련", value: "PTSD" },
    { label: "성격장애 관련", value: "성격장애" },
    { label: "기타", value: "기타" },
    { label: "답변하지 않음", value: "답변하지 않음" },
  ],
};

export const diagnosisImpactStep: SingleChoiceStep = {
  kind: "single",
  id: "diagnosisImpact",
  section: "진단명 직접 확인",
  question: "그 진단이 현재 연애나 인간관계에 영향을 준다고 느끼나요?",
  options: [
    { label: "거의 영향 없음", value: "영향 없음" },
    { label: "연락에 영향", value: "연락에 영향", tags: { contactSensitivity: 20 } },
    { label: "약속/데이트에 영향", value: "약속 데이트 영향" },
    { label: "감정기복에 영향", value: "감정기복에 영향", tags: { moodSwingRisk: 20 } },
    { label: "불안/확인 행동에 영향", value: "불안 확인 행동", tags: { attachmentAnxiety: 20 } },
    { label: "회피/잠수에 영향", value: "회피 잠수", tags: { avoidance: 20 } },
    { label: "성적 친밀감에 영향", value: "성적 친밀감" },
    { label: "신뢰/질투에 영향", value: "신뢰 질투", tags: { attachmentAnxiety: 15 } },
    { label: "이별 후 회복에 영향", value: "이별 후 회복" },
  ],
};

export const medicationStatusStep: SingleChoiceStep = {
  kind: "single",
  id: "medicationStatus",
  section: "약복용 확인",
  question: "현재 정신건강, 수면, 집중, 불안, 기분조절과 관련해 약을 복용 중인가요?",
  options: [
    { label: "없음", value: "없음" },
    { label: "과거 복용 경험 있음", value: "과거 복용" },
    { label: "현재 정기 복용 중", value: "정기 복용" },
    { label: "필요할 때만 복용", value: "필요시 복용" },
    { label: "최근 중단함", value: "최근 중단" },
    { label: "복용 여부를 말하고 싶지 않음", value: "비공개" },
  ],
};

export const medicationImpactStep: MultiChoiceStep = {
  kind: "multi",
  id: "medicationImpact",
  section: "약복용 확인",
  question: "약의 이름은 묻지 않습니다. 복용이 관계에 어떤 영향을 주는지만 선택해주세요.",
  max: 4,
  options: [
    { label: "감정이 안정된다", value: "감정 안정" },
    { label: "불안이 줄어든다", value: "불안 감소" },
    { label: "잠이 개선된다", value: "잠 개선" },
    { label: "집중이 개선된다", value: "집중 개선" },
    { label: "졸림이 있다", value: "졸림" },
    { label: "무기력해진다", value: "무기력" },
    { label: "감정이 무뎌진 느낌이 있다", value: "감정 무뎌짐" },
    { label: "성욕/친밀감에 영향이 있다", value: "친밀감 영향" },
    { label: "데이트 에너지가 줄어든다", value: "데이트 에너지 감소" },
    { label: "특별한 영향 없음", value: "영향 없음" },
    { label: "잘 모르겠다", value: "잘 모름" },
  ],
};
