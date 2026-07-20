import Link from "next/link";
import { Container } from "@/components/ui/Container";
import { SectionHeading } from "@/components/ui/SectionHeading";
import { DraftNote } from "@/components/ui/DraftNote";
import { OfficerCard } from "@/components/leadership/OfficerCard";
import { officers } from "@/data/leadership";

export function LeadershipPreviewSection() {
  const featured = officers.filter((o) => o.featuredOnHome);

  return (
    <section className="section bg-white">
      <Container>
        <SectionHeading eyebrow="Meet the Board" title="Chapter Leadership" center />
        <div className="mx-auto mt-2 max-w-2xl text-center">
          <DraftNote>Officer names and details below are placeholders pending chapter confirmation — see CONTENT_VERIFICATION.md.</DraftNote>
        </div>
        <div className="mt-10 grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
          {featured.map((officer) => (
            <OfficerCard key={officer.id} officer={officer} />
          ))}
        </div>
        <p className="mt-8 text-center text-sm">
          <Link href="/leadership" className="font-semibold text-maroon hover:underline">
            View the full executive board &rarr;
          </Link>
        </p>
      </Container>
    </section>
  );
}
