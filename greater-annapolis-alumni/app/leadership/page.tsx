import type { Metadata } from "next";
import { Container } from "@/components/ui/Container";
import { SectionHeading } from "@/components/ui/SectionHeading";
import { DraftNote } from "@/components/ui/DraftNote";
import { OfficerCard } from "@/components/leadership/OfficerCard";
import { officers } from "@/data/leadership";

export const metadata: Metadata = {
  title: "Leadership",
  description: "Meet the executive board of the UMES Greater Annapolis Alumni Chapter.",
};

export default function LeadershipPage() {
  return (
    <section className="section bg-white">
      <Container>
        <SectionHeading eyebrow="Executive Board" title="Chapter Leadership" />
        <div className="mt-4 max-w-2xl">
          <DraftNote>
            The previous website&rsquo;s executive-board page contained duplicated and mismatched
            names, photos, titles, and graduation years. Rather than guess who is currently
            correct, every officer below is shown as an unverified placeholder until the chapter
            confirms each seat. See CONTENT_VERIFICATION.md for the full list of items to confirm.
          </DraftNote>
        </div>

        <div className="mt-10 grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
          {officers.map((officer) => (
            <OfficerCard key={officer.id} officer={officer} />
          ))}
        </div>
      </Container>
    </section>
  );
}
