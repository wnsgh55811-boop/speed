import { z } from "zod";

export const reviewCategoryEnum = z.enum([
  "REUNION",
  "DATING",
  "SOME",
  "CHAT_ANALYSIS",
  "PATTERN",
  "LONGFORM",
  "CHANGE",
]);

export const reviewSchema = z.object({
  category: reviewCategoryEnum,
  nickname: z.string().min(1, "닉네임을 입력해주세요.").max(30),
  ageGroup: z.string().max(30).optional().or(z.literal("")),
  situationTag: z.string().max(50).optional().or(z.literal("")),
  title: z.string().min(2, "제목을 입력해주세요.").max(120),
  beforeContent: z.string().min(5, "상담 전 상황을 입력해주세요.").max(2000),
  hardestPart: z.string().min(2, "가장 힘들었던 부분을 입력해주세요.").max(2000),
  helpfulPart: z.string().min(2, "가장 도움 됐던 부분을 입력해주세요.").max(2000),
  afterContent: z.string().min(2, "상담 후 변화를 입력해주세요.").max(2000),
  messageToOthers: z.string().max(2000).optional().or(z.literal("")),
  isSecret: z.boolean().optional(),
  password: z.string().max(30).optional().or(z.literal("")),
});

export const programEnum = z.enum(["DATING", "REUNION", "PREMIUM", "UNSURE"]);

export const applicationSchema = z.object({
  program: programEnum,
  name: z.string().min(1, "이름 또는 닉네임을 입력해주세요.").max(30),
  contact: z.string().min(4, "연락처를 입력해주세요.").max(60),
  preferredTime: z.string().max(60).optional().or(z.literal("")),
  situation: z.string().min(5, "현재 상황을 간단히 적어주세요.").max(3000),
  goal: z.string().max(1000).optional().or(z.literal("")),
});
