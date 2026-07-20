import Link from "next/link";
import { announcement } from "@/data/site";

export function AnnouncementBar() {
  if (!announcement.active) return null;

  return (
    <div className="bg-black text-white">
      <div className="container-page flex flex-col items-center gap-1 py-2 text-center text-sm sm:flex-row sm:justify-center sm:gap-3">
        <p>{announcement.message}</p>
        <Link href={announcement.linkHref} className="font-semibold underline underline-offset-2 hover:text-gray-200">
          {announcement.linkLabel}
        </Link>
      </div>
    </div>
  );
}
