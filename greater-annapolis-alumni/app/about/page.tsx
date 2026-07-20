import type { Metadata } from "next";
import { Container } from "@/components/ui/Container";
import { SectionHeading } from "@/components/ui/SectionHeading";
import { DraftNote } from "@/components/ui/DraftNote";
import { PhotoPlaceholder } from "@/components/ui/PhotoPlaceholder";
import { presidentWelcome } from "@/data/leadership";
import { siteConfig, externalLinks } from "@/data/site";

export const metadata: Metadata = {
  title: "About",
  description:
    "Learn about the mission, service area, and University of Maryland Eastern Shore heritage behind the Greater Annapolis Alumni Chapter.",
};

export default function AboutPage() {
  return (
    <>
      <section className="section bg-maroon text-white">
        <Container>
          <SectionHeading eyebrow="About Us" title="Our Chapter" />
          <p className="mt-4 max-w-2xl text-white/90">{siteConfig.description}</p>
        </Container>
      </section>

      <section className="section bg-white">
        <Container className="grid gap-10 lg:grid-cols-2">
          <div>
            <h2 className="text-2xl font-bold text-black">Our Mission</h2>
            <p className="mt-3 text-black/75">
              The Greater Annapolis Alumni Chapter unites University of Maryland Eastern Shore
              graduates and friends of the university through fellowship, student support, and
              community service — carrying Hawk pride into everyday life across the region.
            </p>

            <h2 className="mt-8 text-2xl font-bold text-black">Our Service Area</h2>
            <p className="mt-3 text-black/75">{siteConfig.serviceArea}</p>

            <h2 className="mt-8 text-2xl font-bold text-black">UMES Heritage</h2>
            <p className="mt-3 text-black/75">
              The University of Maryland Eastern Shore is a historically Black land-grant
              university located in Princess Anne, Maryland, with roots dating back to 1886. For
              the full institutional history, visit the official university history page rather
              than a summary here.
            </p>
            <a
              href={externalLinks.umesUniversityHistory.href}
              target="_blank"
              rel="noopener noreferrer"
              className="mt-2 inline-block font-semibold text-maroon hover:underline"
            >
              Read the official UMES history &rarr;
            </a>
          </div>

          <div className="card !p-0 overflow-hidden">
            <PhotoPlaceholder label="Chapter president" className="h-56 w-full" />
            <div className="p-6">
              <h2 className="text-xl font-bold text-black">A Welcome from the President</h2>
              <p className="mt-3 text-black/75">{presidentWelcome.message}</p>
              <p className="mt-4 text-sm font-semibold text-black">{presidentWelcome.authorName}</p>
              <p className="text-sm text-black/60">{presidentWelcome.authorTitle}</p>
              {!presidentWelcome.verified && (
                <DraftNote>President&rsquo;s name and welcome message are pending chapter confirmation.</DraftNote>
              )}
            </div>
          </div>
        </Container>
      </section>
    </>
  );
}
