import { existsSync, copyFileSync } from "fs";
import path from "path";
import { PrismaBetterSqlite3 } from "@prisma/adapter-better-sqlite3";
import { PrismaClient } from "@/generated/prisma/client";

const globalForPrisma = globalThis as unknown as {
  prisma: PrismaClient | undefined;
};

function resolveDatabaseUrl() {
  // Vercel's serverless filesystem is read-only outside of /tmp. On first
  // invocation, copy the build-time seeded SQLite file into /tmp so reads
  // and writes both work for the lifetime of that function instance. This
  // is a demo-only workaround: writes do not persist across instances or
  // redeploys. Swap to a hosted database (Postgres, etc.) for real usage.
  if (process.env.VERCEL) {
    const tmpPath = "/tmp/dev.db";
    if (!existsSync(tmpPath)) {
      const bundledPath = path.join(process.cwd(), "dev.db");
      if (existsSync(bundledPath)) {
        copyFileSync(bundledPath, tmpPath);
      }
    }
    return `file:${tmpPath}`;
  }

  return process.env.DATABASE_URL ?? "file:./dev.db";
}

function createClient() {
  const adapter = new PrismaBetterSqlite3({ url: resolveDatabaseUrl() });
  return new PrismaClient({ adapter });
}

export const prisma = globalForPrisma.prisma ?? createClient();

if (process.env.NODE_ENV !== "production") {
  globalForPrisma.prisma = prisma;
}
