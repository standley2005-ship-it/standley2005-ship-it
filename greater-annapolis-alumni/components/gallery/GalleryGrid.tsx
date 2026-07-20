"use client";

import { useEffect, useRef, useState } from "react";
import { GalleryPhoto } from "@/data/gallery";
import { PhotoPlaceholder } from "@/components/ui/PhotoPlaceholder";
import { EmptyState } from "@/components/ui/EmptyState";

export function GalleryGrid({ photos, emptyMessage }: { photos: GalleryPhoto[]; emptyMessage: string }) {
  const [activeIndex, setActiveIndex] = useState<number | null>(null);
  const closeButtonRef = useRef<HTMLButtonElement>(null);
  const triggerRef = useRef<HTMLButtonElement | null>(null);

  useEffect(() => {
    if (activeIndex === null) return;
    closeButtonRef.current?.focus();

    const onKeyDown = (event: KeyboardEvent) => {
      if (event.key === "Escape") close();
      if (event.key === "ArrowRight") setActiveIndex((i) => (i === null ? i : Math.min(i + 1, photos.length - 1)));
      if (event.key === "ArrowLeft") setActiveIndex((i) => (i === null ? i : Math.max(i - 1, 0)));
    };
    document.addEventListener("keydown", onKeyDown);
    return () => document.removeEventListener("keydown", onKeyDown);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [activeIndex]);

  function close() {
    setActiveIndex(null);
    triggerRef.current?.focus();
  }

  if (photos.length === 0) {
    return (
      <EmptyState
        title="Gallery photos coming soon"
        message={emptyMessage}
      />
    );
  }

  const active = activeIndex !== null ? photos[activeIndex] : null;

  return (
    <>
      <ul className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
        {photos.map((photo, index) => (
          <li key={photo.id}>
            <button
              type="button"
              ref={index === activeIndex ? triggerRef : undefined}
              onClick={(e) => {
                triggerRef.current = e.currentTarget;
                setActiveIndex(index);
              }}
              className="card block w-full !p-0 text-left"
              aria-haspopup="dialog"
            >
              {photo.photo ? (
                // eslint-disable-next-line @next/next/no-img-element
                <img src={photo.photo} alt={photo.alt} loading="lazy" className="h-48 w-full object-cover" />
              ) : (
                <PhotoPlaceholder label={photo.title} className="h-48 w-full" />
              )}
              <div className="p-4">
                <p className="font-bold text-black">{photo.title}</p>
                <p className="text-sm text-black/70">{photo.caption}</p>
              </div>
            </button>
          </li>
        ))}
      </ul>

      {active && (
        <div
          role="dialog"
          aria-modal="true"
          aria-label={active.title}
          className="fixed inset-0 z-[100] flex items-center justify-center bg-black/80 p-4 animate-fade-in"
          onClick={close}
        >
          <div className="max-h-full w-full max-w-3xl overflow-auto rounded-lg bg-white p-4" onClick={(e) => e.stopPropagation()}>
            <div className="flex justify-end">
              <button ref={closeButtonRef} type="button" onClick={close} className="btn-secondary" aria-label="Close photo">
                Close
              </button>
            </div>
            {active.photo ? (
              // eslint-disable-next-line @next/next/no-img-element
              <img src={active.photo} alt={active.alt} className="mt-3 max-h-[70vh] w-full object-contain" />
            ) : (
              <PhotoPlaceholder label={active.title} className="mt-3 h-72 w-full" />
            )}
            <div className="mt-3">
              <p className="text-lg font-bold text-black">{active.title}</p>
              <p className="text-sm text-black/70">
                {active.date ?? "Date not confirmed"} &middot; {active.caption}
              </p>
            </div>
          </div>
        </div>
      )}
    </>
  );
}
