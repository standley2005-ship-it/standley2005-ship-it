import { ReactNode } from "react";

/**
 * `fluid` drops the max-w-content cap (used by the header, which needs
 * the full viewport width on large monitors so the nav has room)
 * while keeping the same responsive side padding as every other
 * section.
 */
export function Container({
  children,
  className = "",
  fluid = false,
}: {
  children: ReactNode;
  className?: string;
  fluid?: boolean;
}) {
  const base = fluid ? "mx-auto w-full px-4 sm:px-6 lg:px-8" : "container-page";
  return <div className={`${base} ${className}`}>{children}</div>;
}
