import type { Metadata } from "next";
import { notFound } from "next/navigation";
import Link from "next/link";
import { Container } from "@/components/ui/Container";
import { EventCard } from "@/components/events/EventCard";
import { events } from "@/data/events";
import { isUpcoming } from "@/lib/events";
import { eventJsonLd } from "@/lib/structuredData";

export function generateStaticParams() {
  return events.map((event) => ({ slug: event.id }));
}

export function generateMetadata({ params }: { params: { slug: string } }): Metadata {
  const event = events.find((e) => e.id === params.slug);
  if (!event) return {};
  return {
    title: event.title,
    description: event.description,
  };
}

export default function EventDetailPage({ params }: { params: { slug: string } }) {
  const event = events.find((e) => e.id === params.slug);
  if (!event) notFound();

  const jsonLd = eventJsonLd(event);

  return (
    <section className="section bg-white">
      {jsonLd && (
        <script
          type="application/ld+json"
          // eslint-disable-next-line react/no-danger
          dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
        />
      )}
      <Container className="max-w-3xl">
        <p className="text-sm">
          <Link href="/events" className="font-semibold text-maroon hover:underline">
            &larr; Back to all events
          </Link>
        </p>
        <div className="mt-6">
          <EventCard event={event} featured past={!isUpcoming(event)} />
        </div>
      </Container>
    </section>
  );
}
