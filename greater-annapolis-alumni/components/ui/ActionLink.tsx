import Link from "next/link";

type Variant = "primary" | "secondary" | "inverse";

/**
 * A call-to-action link that is honest about unconfirmed destinations.
 * If `href` is "#" (the convention used throughout data/*.ts for links
 * that are not yet confirmed), this renders a disabled-looking button
 * with an explanatory note instead of a link that silently goes
 * nowhere — so the site never ships a button that looks functional but
 * isn't.
 */
export function ActionLink({
  href,
  variant = "primary",
  children,
  unavailableNote,
  external,
}: {
  href: string;
  variant?: Variant;
  children: React.ReactNode;
  unavailableNote?: string;
  external?: boolean;
}) {
  const className = {
    primary: "btn-primary",
    secondary: "btn-secondary",
    inverse: "btn-inverse",
  }[variant];

  if (href === "#") {
    return (
      <span className="inline-flex flex-col items-start gap-1">
        <span className={`${className} cursor-not-allowed opacity-60`} role="button" aria-disabled="true" tabIndex={-1}>
          {children}
        </span>
        <span className="text-xs text-black/60">{unavailableNote ?? "Link coming soon — pending chapter confirmation."}</span>
      </span>
    );
  }

  if (external) {
    return (
      <a href={href} className={className} target="_blank" rel="noopener noreferrer">
        {children}
      </a>
    );
  }

  return (
    <Link href={href} className={className}>
      {children}
    </Link>
  );
}
