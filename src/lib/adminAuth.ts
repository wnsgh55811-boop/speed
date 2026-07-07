import { createHmac, timingSafeEqual } from "crypto";

export const ADMIN_COOKIE_NAME = "loveback_admin_session";
const SESSION_PAYLOAD = "admin-authenticated";

function getSecret() {
  return process.env.ADMIN_SESSION_SECRET || process.env.ADMIN_PASSWORD || "dev-secret";
}

export function checkAdminPassword(password: string) {
  const expected = process.env.ADMIN_PASSWORD || "";
  if (!expected) return false;
  const a = Buffer.from(password);
  const b = Buffer.from(expected);
  if (a.length !== b.length) return false;
  return timingSafeEqual(a, b);
}

export function createSessionToken() {
  return createHmac("sha256", getSecret()).update(SESSION_PAYLOAD).digest("hex");
}

export function isValidSessionToken(token: string | undefined | null) {
  if (!token) return false;
  const expected = createSessionToken();
  const a = Buffer.from(token);
  const b = Buffer.from(expected);
  if (a.length !== b.length) return false;
  return timingSafeEqual(a, b);
}
