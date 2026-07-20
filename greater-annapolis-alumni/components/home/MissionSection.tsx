import { Container } from "@/components/ui/Container";
import { SectionHeading } from "@/components/ui/SectionHeading";

const pillars = [
  {
    title: "Alumni Connection",
    description:
      "Building lasting fellowship among UMES graduates in the Greater Annapolis area through gatherings, networking, and Hawk pride.",
  },
  {
    title: "Student Support",
    description:
      "Supporting current and future UMES students through scholarships, mentorship, and encouragement toward graduation.",
  },
  {
    title: "Community Service",
    description:
      "Serving the Greater Annapolis community through volunteer projects and initiatives that make a lasting difference.",
  },
];

export function MissionSection() {
  return (
    <section className="section bg-gray/10">
      <Container>
        <SectionHeading eyebrow="Our Mission" title="Three Ways We Serve" center />
        <div className="mt-10 grid gap-6 sm:grid-cols-3">
          {pillars.map((pillar) => (
            <div key={pillar.title} className="card">
              <h3 className="text-lg font-bold text-maroon">{pillar.title}</h3>
              <p className="mt-2 text-sm text-black/75">{pillar.description}</p>
            </div>
          ))}
        </div>
      </Container>
    </section>
  );
}
