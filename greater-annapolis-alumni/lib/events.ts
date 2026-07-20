import { ChapterEvent } from "@/data/events";

/**
 * Automatic date-based classification: an event is "upcoming" if its
 * date is today or later, otherwise it is "past". This is computed at
 * request/build time from the real clock, so nobody has to remember to
 * move an event between lists by hand.
 */
export function isUpcoming(event: ChapterEvent, now: Date = new Date()): boolean {
  const todayStart = new Date(now.getFullYear(), now.getMonth(), now.getDate());
  const eventDate = parseEventDate(event.date);
  return eventDate.getTime() >= todayStart.getTime();
}

export function parseEventDate(date: string): Date {
  const [year, month, day] = date.split("-").map(Number);
  return new Date(year, month - 1, day);
}

export function splitEvents(events: ChapterEvent[], now: Date = new Date()) {
  const upcoming = events
    .filter((e) => isUpcoming(e, now))
    .sort((a, b) => a.date.localeCompare(b.date));
  const past = events
    .filter((e) => !isUpcoming(e, now))
    .sort((a, b) => b.date.localeCompare(a.date));
  return { upcoming, past };
}

export function formatEventDate(date: string): string {
  const parsed = parseEventDate(date);
  return parsed.toLocaleDateString("en-US", {
    weekday: "long",
    year: "numeric",
    month: "long",
    day: "numeric",
  });
}

/**
 * Builds a downloadable .ics calendar file (as a data URL) for an
 * event. Uses an all-day-ish fallback since the display `time` field
 * is free text, not a machine-readable time — this keeps the file
 * honest without guessing exact start/end times.
 */
export function buildIcsDataUrl(event: ChapterEvent): string {
  const dateCompact = event.date.replace(/-/g, "");
  const nextDay = (() => {
    const d = parseEventDate(event.date);
    d.setDate(d.getDate() + 1);
    return d.toISOString().slice(0, 10).replace(/-/g, "");
  })();

  const escape = (text: string) => text.replace(/[\n,;]/g, (m) => ({ "\n": "\\n", ",": "\\,", ";": "\\;" }[m] as string));

  const ics = [
    "BEGIN:VCALENDAR",
    "VERSION:2.0",
    "PRODID:-//Greater Annapolis Alumni Chapter//Events//EN",
    "BEGIN:VEVENT",
    `UID:${event.id}@greaterannapolischapter.org`,
    `DTSTART;VALUE=DATE:${dateCompact}`,
    `DTEND;VALUE=DATE:${nextDay}`,
    `SUMMARY:${escape(event.title)}`,
    `LOCATION:${escape(event.location)}`,
    `DESCRIPTION:${escape(`${event.time} — ${event.description}`)}`,
    "END:VEVENT",
    "END:VCALENDAR",
  ].join("\r\n");

  return `data:text/calendar;charset=utf-8,${encodeURIComponent(ics)}`;
}
