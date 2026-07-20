/**
 * Small inline flag for unverified content, so visitors (and the
 * chapter, during review) can see at a glance what still needs
 * confirmation without digging into CONTENT_VERIFICATION.md.
 */
export function DraftNote({ children }: { children: React.ReactNode }) {
  return (
    <p className="mt-2 inline-flex items-start gap-1.5 text-xs font-medium text-black/60">
      <span aria-hidden="true">⚠</span>
      <span>{children}</span>
    </p>
  );
}
