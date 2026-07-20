import type { Metadata } from "next";
import { Container } from "@/components/ui/Container";
import { SectionHeading } from "@/components/ui/SectionHeading";
import { ContactForm } from "@/components/forms/ContactForm";
import { DraftNote } from "@/components/ui/DraftNote";
import { contact } from "@/data/site";

export const metadata: Metadata = {
  title: "Contact",
  description: "Get in touch with the UMES Greater Annapolis Alumni Chapter.",
};

export default function ContactPage() {
  return (
    <section className="section bg-white">
      <Container className="grid gap-10 lg:grid-cols-2">
        <div>
          <SectionHeading eyebrow="We'd Love to Hear From You" title="Contact the Chapter" />
          <dl className="mt-6 space-y-4 text-sm">
            <div>
              <dt className="font-semibold text-black">Email</dt>
              <dd className="text-black/75">{contact.email}</dd>
            </div>
            <div>
              <dt className="font-semibold text-black">Phone</dt>
              <dd className="text-black/75">{contact.phone}</dd>
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
          <DraftNote>Contact details above are drafts pending chapter confirmation.</DraftNote>
        </div>

        <div className="card">
          <ContactForm />
        </div>
      </Container>
    </section>
  );
}
