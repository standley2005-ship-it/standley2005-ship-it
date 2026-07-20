import type { Metadata } from "next";
import { Container } from "@/components/ui/Container";
import { SectionHeading } from "@/components/ui/SectionHeading";
import { contact } from "@/data/site";

export const metadata: Metadata = {
  title: "Accessibility Statement",
  description: "Accessibility commitment for the UMES Greater Annapolis Alumni Chapter website.",
};

export default function AccessibilityPage() {
  return (
    <section className="section bg-white">
      <Container className="max-w-3xl">
        <SectionHeading eyebrow="Our Commitment" title="Accessibility Statement" />
        <div className="mt-6 space-y-4 text-black/80">
          <p>
            The UMES Greater Annapolis Alumni Chapter is committed to making this website usable
            by as many people as possible, including alumni and community members who use
            assistive technology. This site targets the Web Content Accessibility Guidelines
            (WCAG) 2.2 Level AA.
          </p>
          <p>
            This includes semantic HTML, keyboard navigation, visible focus indicators, labeled
            form fields, sufficient color contrast, alternative text for images, and support for
            reduced-motion preferences.
          </p>
          <p>
            If you experience difficulty accessing any part of this site, please contact the
            chapter at {contact.email} so we can address the issue.
          </p>
        </div>
      </Container>
    </section>
  );
}
