/**
 * Photo gallery. Each photo needs official, chapter-approved
 * photography — none has been supplied yet, so `photo` is `null` on
 * every draft entry below and the gallery UI shows a placeholder tile
 * instead of a broken image.
 *
 * FOR CHAPTER OFFICERS:
 * - To add a real photo, place the image file in
 *   /public/images/gallery/ and set `photo` to its path, e.g.
 *   "/images/gallery/2025-crab-feast-1.jpg".
 * - Always fill in `alt` with a short, meaningful description of what
 *   is in the photo (for screen-reader users), not just the file name.
 * - `category` must be one of: "event", "community-service",
 *   "scholarship", "meeting".
 * - `year` is a four-digit string used for the year filter.
 */

export type GalleryCategory = "event" | "community-service" | "scholarship" | "meeting";

export type GalleryPhoto = {
  id: string;
  title: string;
  date: string | null; // YYYY-MM-DD if known
  year: string;
  category: GalleryCategory;
  caption: string;
  alt: string;
  photo: string | null;
  verified: boolean;
};

/**
 * No official chapter photography has been supplied yet. This array is
 * intentionally empty so the gallery shows an honest empty state
 * rather than placeholder or stock imagery. Add entries once real,
 * approved photos are provided.
 */
export const galleryPhotos: GalleryPhoto[] = [];
