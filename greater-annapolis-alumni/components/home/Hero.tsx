import { Container } from "@/components/ui/Container";
import { ActionLink } from "@/components/ui/ActionLink";
import { siteConfig, externalLinks } from "@/data/site";

export function Hero() {
  return (
    <section className="bg-maroon text-white">
      <Container className="grid gap-10 py-16 sm:py-24 lg:grid-cols-[3fr_2fr] lg:items-center">
        <div>
          <h1 className="text-3xl font-bold leading-tight sm:text-4xl lg:text-5xl">{siteConfig.tagline}</h1>
          <p className="mt-6 max-w-xl text-base text-white/90 sm:text-lg">{siteConfig.description}</p>
          <div className="mt-8 flex flex-wrap gap-4">
            <ActionLink href={externalLinks.localChapterApplication.href} variant="inverse" unavailableNote="Application link pending confirmation.">
              Join the Chapter
            </ActionLink>
            <a href="/events" className="btn-secondary border-white text-white hover:bg-white hover:text-maroon">
              View Upcoming Events
            </a>
            <a href="/scholarships" className="btn-secondary border-white text-white hover:bg-white hover:text-maroon">
              Support Scholarships
            </a>
          </div>
        </div>
        <div
          aria-hidden="true"
          className="hidden h-64 items-center justify-center rounded-lg border-2 border-dashed border-white/40 text-center text-sm font-semibold uppercase tracking-wide text-white/60 lg:flex"
        >
          Chapter photography coming soon
        </div>
      </Container>
    </section>
  );
}
