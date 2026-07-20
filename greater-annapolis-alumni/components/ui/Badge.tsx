type Tone = "maroon" | "gray" | "black";

export function Badge({ children, tone = "maroon" }: { children: React.ReactNode; tone?: Tone }) {
  const toneClasses: Record<Tone, string> = {
    maroon: "bg-maroon/10 text-maroon",
    gray: "bg-gray/15 text-black/70",
    black: "bg-black text-white",
  };

  return (
    <span className={`inline-flex items-center rounded-full px-3 py-1 text-xs font-bold uppercase tracking-wide ${toneClasses[tone]}`}>
      {children}
    </span>
  );
}
