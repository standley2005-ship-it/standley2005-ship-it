import type { Metadata } from "next";
import { Container } from "@/components/ui/Container";
import { SectionHeading } from "@/components/ui/SectionHeading";
import { GalleryFilters } from "@/components/gallery/GalleryFilters";
import { galleryPhotos } from "@/data/gallery";

export const metadata: Metadata = {
  title: "Gallery",
  description: "Photos from UMES Greater Annapolis Alumni Chapter events, community service, scholarship activity, and meetings.",
};

export default function GalleryPage() {
  return (
    <section className="section bg-white">
      <Container>
        <SectionHeading eyebrow="Chapter Life" title="Gallery" />
        <div className="mt-8">
          <GalleryFilters photos={galleryPhotos} />
        </div>
      </Container>
    </section>
  );
}
