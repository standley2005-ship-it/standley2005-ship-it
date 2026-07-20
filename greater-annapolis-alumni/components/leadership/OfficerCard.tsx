import { Officer } from "@/data/leadership";
import { PhotoPlaceholder } from "@/components/ui/PhotoPlaceholder";
import { Badge } from "@/components/ui/Badge";

export function OfficerCard({ officer }: { officer: Officer }) {
  return (
    <article className="card !p-0 overflow-hidden">
      {officer.photo ? (
        // eslint-disable-next-line @next/next/no-img-element
        <img src={officer.photo} alt="" loading="lazy" className="h-56 w-full object-cover" />
      ) : (
        <PhotoPlaceholder label={officer.name} className="h-56 w-full" />
      )}
      <div className="p-6">
        {!officer.verified && (
          <div className="mb-2">
            <Badge tone="gray">Pending Confirmation</Badge>
          </div>
        )}
        <h3 className="text-lg font-bold text-black">{officer.name}</h3>
        <p className="text-sm font-semibold text-maroon">{officer.position}</p>
        <p className="text-sm text-black/60">{officer.classYear}</p>
        {officer.bio && <p className="mt-3 text-sm text-black/75">{officer.bio}</p>}
      </div>
    </article>
  );
}
