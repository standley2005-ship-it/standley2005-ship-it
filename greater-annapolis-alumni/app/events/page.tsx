import type { Metadata } from "next";
import { Container } from "@/components/ui/Container";
import { SectionHeading } from "@/components/ui/SectionHeading";
import { ActionLink } from "@/components/ui/ActionLink";
import { EventsTabs } from "@/components/events/EventsTabs";
import { events } from "@/data/events";
import { externalLinks } from "@/data/site";
import { splitEvents } from "@/lib/events";

export const metadata: Metadata = {
  title: "Events",
  description: "Upcoming and past events from the UMES Greater Annapolis Alumni Chapter.",
};

export default function EventsPage() {
  const { upcoming, past } = splitEvents(events);

  return (
    <>
      <section className="section bg-maroon text-white">
        <Container className="flex flex-wrap items-center justify-between gap-6">
          <div>
            <SectionHeading eyebrow="Chapter Calendar" title="Events" />
          </div>
          <ActionLink href={externalLinks.googleCalendar.href} variant="inverse" unavailableNote="Chapter calendar link pending confirmation.">
            Subscribe to Calendar
          </ActionLink>
        </Container>
      </section>

      <section className="section bg-white">
        <Container>
          <EventsTabs upcoming={upcoming} past={past} />
        </Container>
      </section>
    </>
  );
}
