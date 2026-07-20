import Link from "next/link";
import { Container } from "@/components/ui/Container";
import { SectionHeading } from "@/components/ui/SectionHeading";
import { GalleryGrid } from "@/components/gallery/GalleryGrid";
import { galleryPhotos } from "@/data/gallery";

export function GalleryPreviewSection() {
  const preview = galleryPhotos.slice(0, 6);

  return (
    <section className="section bg-gray/10">
      <Container>
        <SectionHeading eyebrow="Chapter Life" title="Chapter Highlights" center />
        <div className="mt-10">
          <GalleryGrid
            photos={preview}
            emptyMessage="Official chapter photography has not been supplied yet. Once approved photos are available, they will appear here."
          />
        </div>
        <p className="mt-8 text-center text-sm">
          <Link href="/gallery" className="font-semibold text-maroon hover:underline">
            View the full gallery &rarr;
          </Link>
        </p>
      </Container>
    </section>
  );
}
