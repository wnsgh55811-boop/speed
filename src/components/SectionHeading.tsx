import { clsx } from "clsx";

export function SectionHeading({
  eyebrow,
  title,
  description,
  align = "center",
  light = false,
}: {
  eyebrow?: string;
  title: React.ReactNode;
  description?: React.ReactNode;
  align?: "center" | "left";
  light?: boolean;
}) {
  return (
    <div
      className={clsx(
        "flex flex-col gap-4",
        align === "center" ? "items-center text-center" : "items-start text-left",
      )}
    >
      {eyebrow && (
        <span
          className={clsx(
            "text-xs font-semibold tracking-[0.2em] uppercase",
            light ? "text-ivory-200/70" : "text-burgundy-700",
          )}
        >
          {eyebrow}
        </span>
      )}
      <h2
        className={clsx(
          "font-serif-kr text-2xl leading-snug font-medium sm:text-3xl md:text-4xl",
          light ? "text-ivory-50" : "text-navy-900",
          align === "center" ? "max-w-2xl" : "max-w-xl",
        )}
      >
        {title}
      </h2>
      {description && (
        <p
          className={clsx(
            "text-base leading-relaxed sm:text-lg",
            light ? "text-ivory-100/80" : "text-warmgray-600",
            align === "center" ? "max-w-xl" : "max-w-lg",
          )}
        >
          {description}
        </p>
      )}
    </div>
  );
}
