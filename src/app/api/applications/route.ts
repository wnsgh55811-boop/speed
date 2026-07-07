import { NextResponse } from "next/server";
import { prisma } from "@/lib/prisma";
import { applicationSchema } from "@/lib/validation";

export async function POST(request: Request) {
  const body = await request.json();
  const parsed = applicationSchema.safeParse(body);

  if (!parsed.success) {
    return NextResponse.json(
      { error: parsed.error.issues[0]?.message ?? "입력값을 확인해주세요." },
      { status: 400 },
    );
  }

  const data = parsed.data;

  const application = await prisma.application.create({
    data: {
      program: data.program,
      name: data.name,
      contact: data.contact,
      preferredTime: data.preferredTime || null,
      situation: data.situation,
      goal: data.goal || null,
    },
  });

  return NextResponse.json({ id: application.id }, { status: 201 });
}
