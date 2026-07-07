import { NextResponse } from "next/server";
import { prisma } from "@/lib/prisma";
import { reviewSchema } from "@/lib/validation";

export async function POST(request: Request) {
  const body = await request.json();
  const parsed = reviewSchema.safeParse(body);

  if (!parsed.success) {
    return NextResponse.json(
      { error: parsed.error.issues[0]?.message ?? "입력값을 확인해주세요." },
      { status: 400 },
    );
  }

  const data = parsed.data;

  if (data.isSecret && !data.password) {
    return NextResponse.json(
      { error: "비밀글로 설정하려면 비밀번호를 입력해주세요." },
      { status: 400 },
    );
  }

  const review = await prisma.review.create({
    data: {
      category: data.category,
      nickname: data.nickname,
      ageGroup: data.ageGroup || null,
      situationTag: data.situationTag || null,
      title: data.title,
      beforeContent: data.beforeContent,
      hardestPart: data.hardestPart,
      helpfulPart: data.helpfulPart,
      afterContent: data.afterContent,
      messageToOthers: data.messageToOthers || null,
      isSecret: !!data.isSecret,
      password: data.isSecret ? data.password : null,
      status: "PENDING",
    },
  });

  return NextResponse.json({ id: review.id }, { status: 201 });
}
