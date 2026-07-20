import { siteConfig, social } from "@/data/site";
import { ChapterEvent } from "@/data/events";

/**
 * Organization structured data limited to fields that are actually
 * confirmed (name, url). Unconfirmed fields (phone, address, social
 * profiles) are intentionally omitted rather than filled with drafts —
 * structured data is meant for search engines, so it should never
 * contain guessed facts.
 */
export function organizationJsonLd() {
  const confirmedSocialLinks = Object.values(social)
    .map((s) => s.href)
    .filter((href) => href !== "#");

  return {
    "@context": "https://schema.org",
    "@type": "Organization",
    name: siteConfig.shortName,
    url: siteConfig.url,
    description: siteConfig.description,
    ...(confirmedSocialLinks.length > 0 ? { sameAs: confirmedSocialLinks } : {}),
  };
}

/**
 * Event structured data, only emitted for events the chapter has
 * marked `verified: true` — see data/events.ts.
 */
export function eventJsonLd(event: ChapterEvent) {
  if (!event.verified) return null;

  return {
    "@context": "https://schema.org",
    "@type": "Event",
    name: event.title,
    startDate: event.date,
    location: {
      "@type": "Place",
      name: event.location,
    },
    description: event.description,
    eventAttendanceMode: "https://schema.org/OfflineEventAttendanceMode",
    eventStatus: "https://schema.org/EventScheduled",
  };
}
