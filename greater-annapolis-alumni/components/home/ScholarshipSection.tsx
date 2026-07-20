import Link from "next/link";
import { Container } from "@/components/ui/Container";
import { SectionHeading } from "@/components/ui/SectionHeading";
import { ActionLink } from "@/components/ui/ActionLink";
import { Badge } from "@/components/ui/Badge";
import { DraftNote } from "@/components/ui/DraftNote";
import { scholarshipProgram } from "@/data/scholarships";

const statusLabel = {
  open: "Applications Open",
  closed: "Applications Closed",
  unconfirmed: "Status Unconfirmed",
} as const;

export function ScholarshipSection() {
  return (
    <section className="section bg-gray/10">
      <Container className="grid gap-10 lg:grid-cols-2 lg:items-start">
        <div>
          <SectionHeading eyebrow="Invest in Students" title="Scholarships" />
          <div className="mt-4">
            <Badge tone={scholarshipProgram.cycleStatus === "open" ? "maroon" : "gray"}>
              {statusLabel[scholarshipProgram.cycleStatus]}
            </Badge>
          </div>
          <p className="mt-4 text-sm text-black/75">{scholarshipProgram.currentCycleLabel}</p>
          <p className="mt-2 text-sm text-black/75">{scholarshipProgram.nextCycleExpectation}</p>
          <DraftNote>Scholarship eligibility, deadline, and required materials are pending chapter confirmation.</DraftNote>
        </div>

        <div className="card">
          <h3 className="text-lg font-bold text-black">Eligibility</h3>
          <ul className="mt-2 space-y-2 text-sm text-black/75">
            {scholarshipProgram.eligibility.map((item, i) => (
              <li key={i} className="flex gap-2">
                <span aria-hidden="true" className="text-maroon">•</span>
                <span>{item}</span>
              </li>
            ))}
          </ul>
          <div className="mt-6 flex flex-wrap gap-3">
            <ActionLink href={scholarshipProgram.applicationHref} unavailableNote="Scholarship application link pending confirmation.">
              Scholarship Application
            </ActionLink>
          </div>
          <p className="mt-4 text-sm">
            <Link href="/scholarships" className="font-semibold text-maroon hover:underline">
              Full scholarship details &rarr;
            </Link>
          </p>
        </div>
      </Container>
    </section>
  );
}
