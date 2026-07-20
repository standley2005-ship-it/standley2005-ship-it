import Link from "next/link";
import { Container } from "@/components/ui/Container";
import { contact, externalLinks, social, siteConfig } from "@/data/site";
import { primaryNav } from "@/data/navigation";

export function Footer() {
  const year = new Date().getFullYear();

  return (
    <footer className="bg-maroon-dark text-white">
      <Container className="grid gap-10 py-14 sm:grid-cols-2 lg:grid-cols-4">
        <div>
          <h2 className="text-lg font-bold">{siteConfig.shortName}</h2>
          <p className="mt-3 text-sm text-white/80">
            This is a local alumni chapter of the University of Maryland Eastern Shore National
            Alumni Association, serving the Greater Annapolis area.
          </p>
          <ul className="mt-4 space-y-1 text-sm text-white/80">
            <li>{contact.email}</li>
            <li>{contact.phone}</li>
          </ul>
        </div>

        <nav aria-label="Footer">
          <h2 className="text-sm font-bold uppercase tracking-wide text-white/70">Explore</h2>
          <ul className="mt-4 space-y-2 text-sm">
            {primaryNav.map((item) => (
              <li key={item.href}>
                <Link href={item.href} className="text-white/90 hover:text-white hover:underline">
                  {item.label}
                </Link>
              </li>
            ))}
          </ul>
        </nav>

        <div>
          <h2 className="text-sm font-bold uppercase tracking-wide text-white/70">University Links</h2>
          <ul className="mt-4 space-y-2 text-sm">
            <li>
              <a
                href={externalLinks.umesNationalAlumniAssociation.href}
                className="text-white/90 hover:text-white hover:underline"
                target="_blank"
                rel="noopener noreferrer"
              >
                UMES National Alumni Association
              </a>
            </li>
            <li>
              <a
                href={externalLinks.umesAlumniRelations.href}
                className="text-white/90 hover:text-white hover:underline"
                target="_blank"
                rel="noopener noreferrer"
              >
                UMES Office of Alumni Relations
              </a>
            </li>
          </ul>

          <h2 className="mt-6 text-sm font-bold uppercase tracking-wide text-white/70">Follow the Chapter</h2>
          <ul className="mt-4 flex gap-4 text-sm">
            {Object.values(social).map((s) => (
              <li key={s.label}>
                <a href={s.href} className="text-white/90 hover:text-white hover:underline" aria-label={`${s.label} (link to be confirmed)`}>
                  {s.label}
                </a>
              </li>
            ))}
          </ul>
        </div>

        <div>
          <h2 className="text-sm font-bold uppercase tracking-wide text-white/70">Legal</h2>
          <ul className="mt-4 space-y-2 text-sm">
            <li>
              <Link href="/accessibility" className="text-white/90 hover:text-white hover:underline">
                Accessibility Statement
              </Link>
            </li>
            <li>
              <Link href="/privacy" className="text-white/90 hover:text-white hover:underline">
                Privacy Notice
              </Link>
            </li>
          </ul>
        </div>
      </Container>

      <div className="border-t border-white/20">
        <Container className="flex flex-col items-center justify-between gap-2 py-6 text-xs text-white/70 sm:flex-row">
          <p>&copy; {year} {siteConfig.shortName}. A local chapter of the UMES National Alumni Association.</p>
          <p>This is not the official University of Maryland Eastern Shore website.</p>
        </Container>
      </div>
    </footer>
  );
}
