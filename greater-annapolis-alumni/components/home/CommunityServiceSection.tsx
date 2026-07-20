import Link from "next/link";
import { Container } from "@/components/ui/Container";
import { SectionHeading } from "@/components/ui/SectionHeading";
import { Badge } from "@/components/ui/Badge";
import { activeInitiatives } from "@/data/initiatives";

const statusTone = {
  active: "maroon",
  ongoing: "maroon",
  planned: "gray",
  completed: "gray",
} as const;

export function CommunityServiceSection() {
  return (
    <section className="section bg-white">
      <Container>
        <SectionHeading eyebrow="Serving Our Community" title="Community Service" center />
        <div className="mt-10 grid gap-6 sm:grid-cols-2">
          {activeInitiatives.map((initiative) => (
            <div key={initiative.id} className="card">
              <div className="flex items-center justify-between gap-2">
                <h3 className="text-lg font-bold text-black">{initiative.title}</h3>
                <Badge tone={statusTone[initiative.status]}>{initiative.status}</Badge>
              </div>
              <p className="mt-2 text-sm text-black/75">{initiative.summary}</p>
              {initiative.neededItems && (
                <p className="mt-3 text-sm">
                  <span className="font-semibold text-black">Needed:</span>{" "}
                  <span className="text-black/70">{initiative.neededItems.join(", ")}</span>
                </p>
              )}
            </div>
          ))}
        </div>
        <p className="mt-8 text-center text-sm">
          <Link href="/community-service" className="font-semibold text-maroon hover:underline">
            See all initiatives &amp; how to volunteer &rarr;
          </Link>
        </p>
      </Container>
    </section>
  );
}
