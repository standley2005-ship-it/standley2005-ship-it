import { ChapterEvent } from "@/data/events";
import { formatEventDate, buildIcsDataUrl } from "@/lib/events";
import { ActionLink } from "@/components/ui/ActionLink";
import { DraftNote } from "@/components/ui/DraftNote";
import { Badge } from "@/components/ui/Badge";
import { PhotoPlaceholder } from "@/components/ui/PhotoPlaceholder";

export function EventCard({ event, featured = false, past = false }: { event: ChapterEvent; featured?: boolean; past?: boolean }) {
  return (
    <article className={`card overflow-hidden !p-0 ${featured ? "lg:flex" : ""}`}>
      {event.image ? (
        // eslint-disable-next-line @next/next/no-img-element
        <img src={event.image} alt="" loading="lazy" className={featured ? "h-56 w-full object-cover lg:h-auto lg:w-72" : "h-40 w-full object-cover"} />
      ) : (
        <PhotoPlaceholder label={event.title} className={featured ? "h-56 w-full lg:h-auto lg:w-72" : "h-40 w-full"} />
      )}

      <div className="flex-1 p-6">
        <div className="flex flex-wrap items-center gap-2">
          {past && <Badge tone="gray">Past Event</Badge>}
          {!event.verified && <Badge tone="gray">Details Unconfirmed</Badge>}
        </div>
        <h3 className="mt-3 text-xl font-bold text-black">{event.title}</h3>
        <dl className="mt-3 space-y-1 text-sm text-black/70">
          <div className="flex gap-2">
            <dt className="font-semibold text-black">Date:</dt>
            <dd>{formatEventDate(event.date)}</dd>
          </div>
          <div className="flex gap-2">
            <dt className="font-semibold text-black">Time:</dt>
            <dd>{event.time}</dd>
          </div>
          <div className="flex gap-2">
            <dt className="font-semibold text-black">Location:</dt>
            <dd>{event.location}</dd>
          </div>
        </dl>
        <p className="mt-3 text-sm text-black/80">{event.description}</p>
        {!event.verified && <DraftNote>Event details have not been confirmed by the chapter yet.</DraftNote>}

        {!past && (
          <div className="mt-5 flex flex-wrap gap-3">
            <ActionLink href={event.registrationHref} unavailableNote="Registration link pending confirmation.">
              Register
            </ActionLink>
            {event.icsAvailable ? (
              <a href={buildIcsDataUrl(event)} download={`${event.id}.ics`} className="btn-secondary">
                Add to Calendar
              </a>
            ) : (
              <span className="inline-flex flex-col gap-1">
                <span className="btn-secondary cursor-not-allowed opacity-60" aria-disabled="true">
                  Add to Calendar
                </span>
                <span className="text-xs text-black/60">Calendar file available once event time is confirmed.</span>
              </span>
            )}
          </div>
        )}
      </div>
    </article>
  );
}
