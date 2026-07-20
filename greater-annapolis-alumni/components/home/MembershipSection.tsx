import Link from "next/link";
import { Container } from "@/components/ui/Container";
import { SectionHeading } from "@/components/ui/SectionHeading";
import { ActionLink } from "@/components/ui/ActionLink";
import { DraftNote } from "@/components/ui/DraftNote";
import { membershipInfo } from "@/data/membership";
import { contact, externalLinks } from "@/data/site";

export function MembershipSection() {
  return (
    <section className="section bg-white">
      <Container className="grid gap-10 lg:grid-cols-2 lg:items-start">
        <div>
          <SectionHeading eyebrow="Get Involved" title="Membership" />
          <ul className="mt-6 space-y-2 text-sm text-black/80">
            {membershipInfo.benefits.map((b, i) => (
              <li key={i} className="flex gap-2">
                <span aria-hidden="true" className="text-maroon">•</span>
                <span>{b}</span>
              </li>
            ))}
          </ul>
          <dl className="mt-6 space-y-3 text-sm">
            <div>
              <dt className="font-semibold text-black">Meeting Schedule</dt>
              <dd className="text-black/70">{contact.meetingSchedule}</dd>
            </div>
            <div>
              <dt className="font-semibold text-black">Dues</dt>
              <dd className="text-black/70">
                {membershipInfo.dues.amount} — {membershipInfo.dues.frequency}
              </dd>
            </div>
          </dl>
          <DraftNote>Membership details above are drafts pending chapter confirmation.</DraftNote>
        </div>

        <div className="card">
          <h3 className="text-lg font-bold text-black">Local vs. National Membership</h3>
          <p className="mt-2 text-sm text-black/75">{membershipInfo.localVsNational}</p>
          <div className="mt-6 flex flex-wrap gap-3">
            <ActionLink href={externalLinks.localChapterApplication.href} unavailableNote="Local chapter application link pending confirmation.">
              Membership Application
            </ActionLink>
            <ActionLink href={externalLinks.chapterDuesPayment.href} variant="secondary" unavailableNote="Dues payment link pending confirmation.">
              Pay Dues
            </ActionLink>
          </div>
          <p className="mt-4 text-sm">
            <Link href="/membership" className="font-semibold text-maroon hover:underline">
              Full membership details &amp; FAQ &rarr;
            </Link>
          </p>
        </div>
      </Container>
    </section>
  );
}
