"use server";

import { cookies } from "next/headers";
import { revalidatePath } from "next/cache";
import { prisma } from "@/lib/prisma";
import { ADMIN_COOKIE_NAME, isValidSessionToken } from "@/lib/adminAuth";

async function assertAdmin() {
  const store = await cookies();
  const token = store.get(ADMIN_COOKIE_NAME)?.value;
  if (!isValidSessionToken(token)) {
    throw new Error("관리자 인증이 필요합니다.");
  }
}

export async function updateReviewStatus(id: string, status: "APPROVED" | "HIDDEN" | "PENDING") {
  await assertAdmin();
  await prisma.review.update({ where: { id }, data: { status } });
  revalidatePath("/admin/reviews");
  revalidatePath("/reviews");
}

export async function updateApplicationStatus(
  id: string,
  status: "NEW" | "CONTACTED" | "SCHEDULED" | "COMPLETED" | "CANCELED",
) {
  await assertAdmin();
  await prisma.application.update({ where: { id }, data: { status } });
  revalidatePath("/admin/applications");
}

export async function updateApplicationMemo(id: string, formData: FormData) {
  await assertAdmin();
  const memo = String(formData.get("memo") ?? "");
  await prisma.application.update({ where: { id }, data: { memo } });
  revalidatePath("/admin/applications");
}
