/**
 * Approved-logo placeholder. The real UMES / chapter logo must not be
 * recreated or altered by this project — once the chapter supplies an
 * official logo file, replace this component's contents (or swap in
 * an <Image> pointing at /public/images/logo/) rather than drawing a
 * new mark.
 */
export function Logo({ variant = "maroon" }: { variant?: "maroon" | "white" }) {
  const textColor = variant === "white" ? "text-white" : "text-maroon";
  const borderColor = variant === "white" ? "border-white" : "border-maroon";

  return (
    <span className="inline-flex items-center gap-2">
      <span
        aria-hidden="true"
        className={`flex h-10 w-10 shrink-0 items-center justify-center rounded-full border-2 ${borderColor} font-serif text-sm font-bold ${textColor}`}
      >
        GA
      </span>
      <span className={`flex flex-col leading-tight ${textColor}`}>
        <span className="text-sm font-bold sm:text-base">UMES Greater Annapolis</span>
        <span className="text-[11px] font-medium uppercase tracking-wide sm:text-xs">Alumni Chapter</span>
      </span>
    </span>
  );
}
