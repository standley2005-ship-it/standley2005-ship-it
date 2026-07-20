import type { Metadata } from "next";
import { Container } from "@/components/ui/Container";
import { SectionHeading } from "@/components/ui/SectionHeading";
import { ActionLink } from "@/components/ui/ActionLink";
import { Badge } from "@/components/ui/Badge";
import { DraftNote } from "@/components/ui/DraftNote";
import { scholarshipProgram, previousRecipients } from "@/data/scholarships";

export const metadata: Metadata = {
  title: "Scholarships",
  description: "Scholarship eligibility, required materials, deadlines, and application status for the UMES Greater Annapolis Alumni Chapter.",
};

const statusLabel = {
  open: "Applications Open",
  closed: "Applications Closed",
  unconfirmed: "Status Unconfirmed",
} as const;

export default function ScholarshipsPage() {
  return (
    <>
      <section className="section bg-maroon text-white">
        <Container>
          <SectionHeading eyebrow="Invest in Students" title="Scholarships" />
          <div className="mt-4">
            <Badge tone="gray">{statusLabel[scholarshipProgram.cycleStatus]}</Badge>
          </div>
          <p className="mt-4 max-w-2xl text-white/90">{scholarshipProgram.currentCycleLabel}</p>
        </Container>
      </section>

      <section className="section bg-white">
        <Container className="grid gap-10 lg:grid-cols-3">
          <div>
            <h2 className="text-xl font-bold text-black">Eligibility</h2>
            <ul className="mt-3 space-y-2 text-sm text-black/75">
              {scholarshipProgram.eligibility.map((item, i) => (
                <li key={i}>{item}</li>
              ))}
            </ul>
          </div>
          <div>
            <h2 className="text-xl font-bold text-black">Required Materials</h2>
            <ul className="mt-3 space-y-2 text-sm text-black/75">
              {scholarshipProgram.requiredMaterials.map((item, i) => (
                <li key={i}>{item}</li>
              ))}
            </ul>
          </div>
          <div>
            <h2 className="text-xl font-bold text-black">Timeline</h2>
            <dl className="mt-3 space-y-3 text-sm">
              <div>
                <dt className="font-semibold text-black">Deadline</dt>
                <dd className="text-black/75">
                  {scholarshipProgram.deadline ?? "Not yet confirmed"}
                </dd>
              </div>
              <div>
                <dt className="font-semibold text-black">Next Cycle</dt>
                <dd className="text-black/75">{scholarshipProgram.nextCycleExpectation}</dd>
              </div>
              <div>
                <dt className="font-semibold text-black">Questions</dt>
                <dd className="text-black/75">{scholarshipProgram.contactEmail}</dd>
              </div>
            </dl>
          </div>
        </Container>
      </section>

      <section className="section bg-gray/10">
        <Container>
          <div className="card">
            <h2 className="text-xl font-bold text-black">Apply</h2>
            <p className="mt-2 text-sm text-black/75">
              Keep scholarship applications separate from event registration and community-service
              sign-ups — use the button below only for the scholarship application itself.
            </p>
            <div className="mt-4">
              <ActionLink href={scholarshipProgram.applicationHref} unavailableNote="Scholarship application link pending confirmation.">
                Scholarship Application
              </ActionLink>
            </div>
            <DraftNote>Eligibility, required materials, and deadline above are drafts pending chapter confirmation.</DraftNote>
          </div>
        </Container>
      </section>

      <section className="section bg-white">
        <Container>
          <h2 className="text-xl font-bold text-black">Previous Recipients</h2>
          {previousRecipients.length === 0 ? (
            <p className="mt-3 text-sm text-black/75">
              No previous recipients have been verified and approved for publication yet. This
              section will be updated once the chapter confirms names for public display.
            </p>
          ) : (
            <ul className="mt-3 space-y-2 text-sm text-black/75">
              {previousRecipients.map((r) => (
                <li key={`${r.year}-${r.name}`}>
                  {r.year} — {r.name}
                  {r.note ? ` (${r.note})` : ""}
                </li>
              ))}
            </ul>
          )}
        </Container>
      </section>
    </>
  );
}
