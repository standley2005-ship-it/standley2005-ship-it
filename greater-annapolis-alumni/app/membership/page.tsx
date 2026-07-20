import type { Metadata } from "next";
import { Container } from "@/components/ui/Container";
import { SectionHeading } from "@/components/ui/SectionHeading";
import { ActionLink } from "@/components/ui/ActionLink";
import { DraftNote } from "@/components/ui/DraftNote";
import { membershipInfo, membershipFaqs } from "@/data/membership";
import { contact, externalLinks } from "@/data/site";

export const metadata: Metadata = {
  title: "Membership",
  description: "Eligibility, benefits, dues, and how to join the UMES Greater Annapolis Alumni Chapter.",
};

export default function MembershipPage() {
  return (
    <>
      <section className="section bg-maroon text-white">
        <Container>
          <SectionHeading eyebrow="Join Us" title="Membership" />
          <p className="mt-4 max-w-2xl text-white/90">
            Whether you graduated from UMES or simply believe in its mission, chapter membership
            is how you stay connected, support students, and give back to the Greater Annapolis
            community.
          </p>
          <div className="mt-8 flex flex-wrap gap-4">
            <ActionLink href={externalLinks.localChapterApplication.href} variant="inverse" unavailableNote="Local chapter application link pending confirmation.">
              Membership Application
            </ActionLink>
            <ActionLink href={externalLinks.chapterDuesPayment.href} variant="secondary" unavailableNote="Dues payment link pending confirmation.">
              Pay Dues
            </ActionLink>
          </div>
        </Container>
      </section>

      <section className="section bg-white">
        <Container className="grid gap-10 lg:grid-cols-3">
          <div>
            <h2 className="text-xl font-bold text-black">Eligibility</h2>
            <ul className="mt-3 space-y-2 text-sm text-black/75">
              {membershipInfo.eligibility.map((item, i) => (
                <li key={i}>{item}</li>
              ))}
            </ul>
          </div>
          <div>
            <h2 className="text-xl font-bold text-black">Benefits</h2>
            <ul className="mt-3 space-y-2 text-sm text-black/75">
              {membershipInfo.benefits.map((item, i) => (
                <li key={i}>{item}</li>
              ))}
            </ul>
          </div>
          <div>
            <h2 className="text-xl font-bold text-black">Dues &amp; Meetings</h2>
            <dl className="mt-3 space-y-3 text-sm">
              <div>
                <dt className="font-semibold text-black">Dues</dt>
                <dd className="text-black/75">
                  {membershipInfo.dues.amount} — {membershipInfo.dues.frequency}
                </dd>
              </div>
              <div>
                <dt className="font-semibold text-black">Meeting Schedule</dt>
                <dd className="text-black/75">{contact.meetingSchedule}</dd>
              </div>
              <div>
                <dt className="font-semibold text-black">Meeting Location</dt>
                <dd className="text-black/75">{contact.meetingLocation}</dd>
              </div>
            </dl>
          </div>
        </Container>
      </section>

      <section className="section bg-gray/10">
        <Container>
          <h2 className="text-xl font-bold text-black">Local vs. National Membership</h2>
          <p className="mt-3 max-w-3xl text-black/75">{membershipInfo.localVsNational}</p>
          <div className="mt-4">
            <ActionLink href={externalLinks.nationalAlumniMembership.href} variant="secondary" unavailableNote="National association membership link pending confirmation.">
              National Alumni Association Membership
            </ActionLink>
          </div>
        </Container>
      </section>

      <section className="section bg-white">
        <Container>
          <h2 className="text-xl font-bold text-black">Frequently Asked Questions</h2>
          <dl className="mt-6 divide-y divide-gray/25 border-t border-b border-gray/25">
            {membershipFaqs.map((faq) => (
              <div key={faq.question} className="py-5">
                <dt className="font-semibold text-black">{faq.question}</dt>
                <dd className="mt-2 text-sm text-black/75">{faq.answer}</dd>
              </div>
            ))}
          </dl>
          <DraftNote>Membership eligibility, benefits, dues, and FAQ answers above are drafts pending chapter confirmation.</DraftNote>
        </Container>
      </section>
    </>
  );
}
