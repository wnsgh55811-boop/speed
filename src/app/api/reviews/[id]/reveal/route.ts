import { NextResponse } from "next/server";
import { prisma } from "@/lib/prisma";

export async function POST(
  request: Request,
  { params }: { params: Promise<{ id: string }> },
) {
  const { id } = await params;
  const { password } = await request.json();

  const review = await prisma.review.findUnique({ where: { id } });

  if (!review || review.status !== "APPROVED") {
    return NextResponse.json({ error: "후기를 찾을 수 없습니다." }, { status: 404 });
  }

  if (!review.isSecret) {
    return NextResponse.json(review);
  }

  if (!password || password !== review.password) {
    return NextResponse.json(
      { error: "비밀번호가 일치하지 않습니다." },
      { status: 403 },
    );
  }

  return NextResponse.json(review);
}
