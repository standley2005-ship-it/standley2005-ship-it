"use client";

import { useMemo, useState } from "react";
import { GalleryCategory, GalleryPhoto } from "@/data/gallery";
import { GalleryGrid } from "@/components/gallery/GalleryGrid";

const categoryLabels: Record<GalleryCategory, string> = {
  event: "Event",
  "community-service": "Community Service",
  scholarship: "Scholarship Activity",
  meeting: "Chapter Meeting",
};

export function GalleryFilters({ photos }: { photos: GalleryPhoto[] }) {
  const [category, setCategory] = useState<GalleryCategory | "all">("all");
  const [year, setYear] = useState<string | "all">("all");

  const years = useMemo(() => {
    const unique = Array.from(new Set(photos.map((p) => p.year))).sort((a, b) => b.localeCompare(a));
    return unique;
  }, [photos]);

  const filtered = photos.filter((p) => (category === "all" || p.category === category) && (year === "all" || p.year === year));

  return (
    <div>
      <div className="flex flex-wrap items-end gap-4">
        <div>
          <label htmlFor="gallery-category" className="block text-sm font-semibold text-black">
            Filter by category
          </label>
          <select
            id="gallery-category"
            value={category}
            onChange={(e) => setCategory(e.target.value as GalleryCategory | "all")}
            className="mt-1 rounded-md border border-gray/40 bg-white px-3 py-2 text-sm text-black focus-visible:outline focus-visible:outline-2 focus-visible:outline-maroon"
          >
            <option value="all">All categories</option>
            {Object.entries(categoryLabels).map(([value, label]) => (
              <option key={value} value={value}>
                {label}
              </option>
            ))}
          </select>
        </div>

        <div>
          <label htmlFor="gallery-year" className="block text-sm font-semibold text-black">
            Filter by year
          </label>
          <select
            id="gallery-year"
            value={year}
            onChange={(e) => setYear(e.target.value)}
            className="mt-1 rounded-md border border-gray/40 bg-white px-3 py-2 text-sm text-black focus-visible:outline focus-visible:outline-2 focus-visible:outline-maroon"
            disabled={years.length === 0}
          >
            <option value="all">All years</option>
            {years.map((y) => (
              <option key={y} value={y}>
                {y}
              </option>
            ))}
          </select>
        </div>
      </div>

      <p className="mt-3 text-sm text-black/60" role="status">
        Showing {filtered.length} of {photos.length} photos
      </p>

      <div className="mt-6">
        <GalleryGrid
          photos={filtered}
          emptyMessage="Official chapter photography has not been supplied yet. Once approved photos are added to data/gallery.ts, they will appear here with these same filters."
        />
      </div>
    </div>
  );
}
