import { Container } from "@/components/ui/Container";
import { SectionHeading } from "@/components/ui/SectionHeading";
import { EmptyState } from "@/components/ui/EmptyState";
import { EventCard } from "@/components/events/EventCard";
import { events, noUpcomingEventsMessage } from "@/data/events";
import { splitEvents } from "@/lib/events";

export function UpcomingEventSection() {
  const { upcoming } = splitEvents(events);
  const nextEvent = upcoming[0];

  return (
    <section className="section bg-white">
      <Container>
        <SectionHeading eyebrow="Save the Date" title="Upcoming Event" />
        <div className="mt-8">
          {nextEvent ? (
            <EventCard event={nextEvent} featured />
          ) : (
            <EmptyState
              title="No upcoming event confirmed yet"
              message={noUpcomingEventsMessage}
            />
          )}
        </div>
      </Container>
    </section>
  );
}
