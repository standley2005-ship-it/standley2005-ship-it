/**
 * Fallback tile shown wherever a photo has not been supplied yet
 * (leadership headshots, gallery images). Keeps layouts stable and
 * honest instead of showing a broken image icon.
 */
export function PhotoPlaceholder({ label, className = "" }: { label: string; className?: string }) {
  return (
    <div
      role="img"
      aria-label={`Photo not yet available: ${label}`}
      className={`flex items-center justify-center bg-gray/15 text-center ${className}`}
    >
      <span className="px-4 text-xs font-semibold uppercase tracking-wide text-black/50">Photo Coming Soon</span>
    </div>
  );
}
