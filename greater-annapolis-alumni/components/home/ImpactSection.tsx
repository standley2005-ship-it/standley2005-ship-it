import { Container } from "@/components/ui/Container";
import { SectionHeading } from "@/components/ui/SectionHeading";
import { impactStats } from "@/data/site";

export function ImpactSection() {
  return (
    <section className="section bg-maroon text-white">
      <Container>
        <SectionHeading eyebrow="Our Impact" title="Hawk Pride in Action" center />
        <p className="mx-auto mt-2 max-w-2xl text-center text-sm text-white/80">
          These figures will be published once verified by the chapter. We would rather show
          &ldquo;to be confirmed&rdquo; than an inaccurate number.
        </p>
        <div className="mt-10 grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
          {impactStats.map((stat) => (
            <div key={stat.id} className="rounded-lg border border-white/25 bg-white/5 p-6 text-center">
              <p className="text-3xl font-bold">{stat.value}</p>
              <p className="mt-2 text-sm font-semibold uppercase tracking-wide text-white/80">{stat.label}</p>
            </div>
          ))}
        </div>
      </Container>
    </section>
  );
}
