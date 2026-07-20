import type { Metadata } from "next";
import { Container } from "@/components/ui/Container";
import { SectionHeading } from "@/components/ui/SectionHeading";
import { Badge } from "@/components/ui/Badge";
import { DraftNote } from "@/components/ui/DraftNote";
import { activeInitiatives, completedProjects, campaignContact } from "@/data/initiatives";

export const metadata: Metadata = {
  title: "Community Service",
  description: "Active initiatives, volunteer opportunities, and needed items for UMES Greater Annapolis Alumni Chapter community service.",
};

const statusTone = {
  active: "maroon",
  ongoing: "maroon",
  planned: "gray",
  completed: "gray",
} as const;

export default function CommunityServicePage() {
  return (
    <>
      <section className="section bg-maroon text-white">
        <Container>
          <SectionHeading eyebrow="Serving Greater Annapolis" title="Community Service" />
          <p className="mt-4 max-w-2xl text-white/90">
            Hawk pride means showing up for our community. Here&rsquo;s where the chapter is
            focused right now, and how you can help.
          </p>
        </Container>
      </section>

      <section className="section bg-white">
        <Container>
          <h2 className="text-xl font-bold text-black">Active Initiatives</h2>
          <div className="mt-6 grid gap-6 sm:grid-cols-2">
            {activeInitiatives.map((initiative) => (
              <div key={initiative.id} className="card">
                <div className="flex items-center justify-between gap-2">
                  <h3 className="text-lg font-bold text-black">{initiative.title}</h3>
                  <Badge tone={statusTone[initiative.status]}>{initiative.status}</Badge>
                </div>
                <p className="mt-2 text-sm text-black/75">{initiative.summary}</p>
                {initiative.neededItems && (
                  <p className="mt-3 text-sm">
                    <span className="font-semibold text-black">Needed items:</span>{" "}
                    <span className="text-black/70">{initiative.neededItems.join(", ")}</span>
                  </p>
                )}
                {initiative.volunteerInfo && (
                  <p className="mt-3 text-sm">
                    <span className="font-semibold text-black">Volunteering:</span>{" "}
                    <span className="text-black/70">{initiative.volunteerInfo}</span>
                  </p>
                )}
                {!initiative.verified && <DraftNote>Details pending chapter confirmation.</DraftNote>}
              </div>
            ))}
          </div>
        </Container>
      </section>

      <section className="section bg-gray/10">
        <Container>
          <h2 className="text-xl font-bold text-black">Campaign Contact</h2>
          <p className="mt-2 text-sm text-black/75">
            Questions about a drive or volunteer opportunity? Reach the {campaignContact.label} at{" "}
            {campaignContact.email}.
          </p>
          {!campaignContact.verified && <DraftNote>Campaign contact is pending chapter confirmation.</DraftNote>}
        </Container>
      </section>

      <section className="section bg-white">
        <Container>
          <h2 className="text-xl font-bold text-black">Completed Project Archive</h2>
          {completedProjects.length === 0 ? (
            <p className="mt-3 text-sm text-black/75">
              No completed projects have been verified for the archive yet. This section will
              grow as finished initiatives are confirmed by the chapter.
            </p>
          ) : (
            <ul className="mt-3 space-y-3 text-sm text-black/75">
              {completedProjects.map((project) => (
                <li key={project.id}>
                  <span className="font-semibold text-black">
                    {project.title} ({project.year})
                  </span>{" "}
                  — {project.summary}
                </li>
              ))}
            </ul>
          )}
        </Container>
      </section>
    </>
  );
}
