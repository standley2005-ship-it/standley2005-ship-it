export function EmptyState({
  title,
  message,
  icon,
}: {
  title: string;
  message: string;
  icon?: React.ReactNode;
}) {
  return (
    <div className="flex flex-col items-center rounded-lg border-2 border-dashed border-gray/40 bg-white px-6 py-14 text-center">
      {icon ?? <CalendarIcon />}
      <h3 className="mt-4 text-lg font-bold text-black">{title}</h3>
      <p className="mt-2 max-w-md text-sm text-black/70">{message}</p>
    </div>
  );
}

function CalendarIcon() {
  return (
    <svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" viewBox="0 0 24 24" fill="none" aria-hidden="true">
      <rect x="3" y="5" width="18" height="16" rx="2" stroke="#651D32" strokeWidth="1.5" />
      <path d="M3 9h18M8 3v4M16 3v4" stroke="#651D32" strokeWidth="1.5" strokeLinecap="round" />
    </svg>
  );
}
