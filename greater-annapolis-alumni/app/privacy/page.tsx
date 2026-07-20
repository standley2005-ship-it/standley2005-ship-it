import type { Metadata } from "next";
import { Container } from "@/components/ui/Container";
import { SectionHeading } from "@/components/ui/SectionHeading";
import { contact } from "@/data/site";

export const metadata: Metadata = {
  title: "Privacy Notice",
  description: "Privacy notice for the UMES Greater Annapolis Alumni Chapter website.",
};

export default function PrivacyPage() {
  return (
    <section className="section bg-white">
      <Container className="max-w-3xl">
        <SectionHeading eyebrow="Your Privacy" title="Privacy Notice" />
        <div className="mt-6 space-y-4 text-black/80">
          <p>
            This staging site is a redesign preview for the UMES Greater Annapolis Alumni
            Chapter and is not connected to any production system. The contact and email signup
            forms on this staging site do not send data anywhere — submissions are handled only
            in your browser for preview purposes.
          </p>
          <p>
            When this site is connected to production, this notice will be updated to describe
            what information is collected (for example, through the contact form or email
            signup), how it is used, and how long it is retained.
          </p>
          <p>
            Questions about this notice can be directed to {contact.email}.
          </p>
        </div>
      </Container>
    </section>
  );
}
