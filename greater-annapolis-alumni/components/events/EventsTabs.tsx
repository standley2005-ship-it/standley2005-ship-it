"use client";

import { useId, useState } from "react";
import { ChapterEvent } from "@/data/events";
import { EventCard } from "@/components/events/EventCard";
import { EmptyState } from "@/components/ui/EmptyState";
import { noUpcomingEventsMessage } from "@/data/events";

export function EventsTabs({ upcoming, past }: { upcoming: ChapterEvent[]; past: ChapterEvent[] }) {
  const [tab, setTab] = useState<"upcoming" | "past">("upcoming");
  const baseId = useId();
  const tabs = [
    { key: "upcoming" as const, label: `Upcoming Events (${upcoming.length})` },
    { key: "past" as const, label: `Past Events (${past.length})` },
  ];

  function onKeyDown(event: React.KeyboardEvent) {
    if (event.key !== "ArrowRight" && event.key !== "ArrowLeft") return;
    event.preventDefault();
    const currentIndex = tabs.findIndex((t) => t.key === tab);
    const nextIndex = event.key === "ArrowRight" ? (currentIndex + 1) % tabs.length : (currentIndex - 1 + tabs.length) % tabs.length;
    setTab(tabs[nextIndex].key);
    document.getElementById(`${baseId}-tab-${tabs[nextIndex].key}`)?.focus();
  }

  return (
    <div>
      <div role="tablist" aria-label="Events" className="flex gap-2 border-b border-gray/30" onKeyDown={onKeyDown}>
        {tabs.map((t) => (
          <button
            key={t.key}
            id={`${baseId}-tab-${t.key}`}
            role="tab"
            type="button"
            aria-selected={tab === t.key}
            aria-controls={`${baseId}-panel-${t.key}`}
            tabIndex={tab === t.key ? 0 : -1}
            onClick={() => setTab(t.key)}
            className={`px-4 py-3 text-sm font-bold ${
              tab === t.key ? "border-b-2 border-maroon text-maroon" : "text-black/60 hover:text-black"
            }`}
          >
            {t.label}
          </button>
        ))}
      </div>

      <div
        id={`${baseId}-panel-upcoming`}
        role="tabpanel"
        aria-labelledby={`${baseId}-tab-upcoming`}
        hidden={tab !== "upcoming"}
        className="mt-8 space-y-6"
      >
        {upcoming.length > 0 ? (
          upcoming.map((event) => <EventCard key={event.id} event={event} />)
        ) : (
          <EmptyState title="No upcoming events confirmed" message={noUpcomingEventsMessage} />
        )}
      </div>

      <div
        id={`${baseId}-panel-past`}
        role="tabpanel"
        aria-labelledby={`${baseId}-tab-past`}
        hidden={tab !== "past"}
        className="mt-8 space-y-6"
      >
        {past.length > 0 ? (
          past.map((event) => <EventCard key={event.id} event={event} past />)
        ) : (
          <EmptyState title="No past events on record" message="Past events will appear here automatically once their date has passed." />
        )}
      </div>
    </div>
  );
}
