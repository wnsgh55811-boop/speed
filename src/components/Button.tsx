import Link from "next/link";
import { clsx } from "clsx";

type Variant = "primary" | "secondary" | "ghost" | "kakao";

const variantClasses: Record<Variant, string> = {
  primary:
    "bg-burgundy-700 text-ivory-50 hover:bg-burgundy-800 border border-burgundy-700",
  secondary:
    "bg-transparent text-navy-900 border border-navy-800 hover:bg-navy-900 hover:text-ivory-50",
  ghost:
    "bg-ivory-100 text-navy-800 border border-warmgray-300 hover:border-navy-700",
  kakao: "bg-[#fee500] text-[#391b1b] hover:bg-[#f5da00] border border-[#fee500]",
};

export function Button({
  href,
  children,
  variant = "primary",
  className,
  size = "md",
  type,
  onClick,
  target,
}: {
  href?: string;
  children: React.ReactNode;
  variant?: Variant;
  className?: string;
  size?: "sm" | "md" | "lg";
  type?: "button" | "submit";
  onClick?: () => void;
  target?: string;
}) {
  const sizeClasses = {
    sm: "px-4 py-2 text-sm",
    md: "px-6 py-3 text-sm sm:text-base",
    lg: "px-8 py-4 text-base sm:text-lg",
  }[size];

  const classes = clsx(
    "inline-flex items-center justify-center gap-2 rounded-sm font-medium tracking-wide transition-colors duration-150",
    variantClasses[variant],
    sizeClasses,
    className,
  );

  if (href) {
    return (
      <Link href={href} className={classes} target={target}>
        {children}
      </Link>
    );
  }

  return (
    <button type={type ?? "button"} onClick={onClick} className={classes}>
      {children}
    </button>
  );
}
