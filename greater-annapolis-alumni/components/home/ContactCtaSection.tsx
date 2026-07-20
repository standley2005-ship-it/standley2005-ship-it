import Link from "next/link";
import { Container } from "@/components/ui/Container";
import { EmailSignupForm } from "@/components/forms/EmailSignupForm";

export function ContactCtaSection() {
  return (
    <section className="section bg-black text-white">
      <Container className="grid gap-10 lg:grid-cols-2 lg:items-center">
        <div>
          <h2 className="text-3xl font-bold sm:text-4xl">Stay Connected</h2>
          <p className="mt-4 max-w-xl text-white/80">
            Have a question, want to get involved, or need to reach an officer? Send us a message,
            or sign up for chapter email updates so you never miss a meeting, event, or
            scholarship deadline.
          </p>
          <Link href="/contact" className="btn-inverse mt-6 inline-flex">
            Contact the Chapter
          </Link>
        </div>
        <div className="card bg-white text-black">
          <h3 className="text-lg font-bold">Email Updates</h3>
          <p className="mt-1 text-sm text-black/70">
            Sign up to receive chapter announcements. (Staging site — signups are not sent
            anywhere yet.)
          </p>
          <EmailSignupForm />
        </div>
      </Container>
    </section>
  );
}
