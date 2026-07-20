/**
 * Chapter events. Classification into "Upcoming" and "Past" is
 * AUTOMATIC and date-based (see lib/events.ts) — you never need to
 * move an event between lists by hand. Once today's date passes an
 * event's `date`, it moves itself to Past.
 *
 * FOR CHAPTER OFFICERS:
 * - To add an event, copy an object below and give it a unique `id`.
 * - `date` must be in "YYYY-MM-DD" format.
 * - `time` is a display string, e.g. "10:00 AM – 2:00 PM".
 * - Set `registrationHref` to the real registration/ticket link, or
 *   leave "#" if there is no registration link yet.
 * - `icsAvailable: true` shows an "Add to calendar" button that
 *   downloads a generated .ics file from the event's date/time/title.
 * - Set `verified: true` only after an officer confirms the details.
 *
 * The July 13, 2025 Crab Feast from the previous website is kept here
 * as a PAST event only (its date has passed) so it stops being shown
 * as an upcoming event. Its description/location were not confirmed
 * and are marked DRAFT below — see CONTENT_VERIFICATION.md.
 */

export type ChapterEvent = {
  id: string;
  title: string;
  date: string; // YYYY-MM-DD
  time: string;
  location: string;
  description: string;
  registrationHref: string;
  icsAvailable: boolean;
  verified: boolean;
  image?: string | null;
};

export const events: ChapterEvent[] = [
  {
    id: "crab-feast-2025",
    title: "Annual Crab Feast",
    date: "2025-07-13",
    time: "DRAFT — time not confirmed",
    location: "DRAFT — location not confirmed",
    description:
      "DRAFT — carried over from the previous website as a past event only. Full details (location, pricing, beneficiary) were not confirmed and must be verified before being published as historical content.",
    registrationHref: "#",
    icsAvailable: false,
    verified: false,
    image: null,
  },
];

/**
 * When there truly are no confirmed upcoming events, leave this array
 * empty — the homepage and Events page will show a polished "no
 * upcoming event" state instead of a broken or fake card. Do not add
 * a placeholder event just to fill the space.
 */
export const noUpcomingEventsMessage =
  "No upcoming events are confirmed right now. Check back soon, or follow the chapter's social channels for the latest updates.";
