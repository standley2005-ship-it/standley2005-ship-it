export function SectionHeading({
  eyebrow,
  title,
  description,
  level = 2,
  center = false,
}: {
  eyebrow?: string;
  title: string;
  description?: string;
  level?: 2 | 3;
  center?: boolean;
}) {
  const Heading = level === 2 ? "h2" : "h3";

  return (
    <div className={center ? "mx-auto max-w-2xl text-center" : "max-w-2xl"}>
      {eyebrow && <p className="eyebrow">{eyebrow}</p>}
      <Heading className="mt-2 text-3xl font-bold tracking-tight text-black sm:text-4xl">{title}</Heading>
      {description && <p className="mt-4 text-base text-black/70">{description}</p>}
    </div>
  );
}
