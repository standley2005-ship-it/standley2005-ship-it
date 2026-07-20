"use client";

import { useEffect, useId, useState } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { Container } from "@/components/ui/Container";
import { Logo } from "@/components/ui/Logo";
import { primaryNav } from "@/data/navigation";

export function Header() {
  const [menuOpen, setMenuOpen] = useState(false);
  const pathname = usePathname();
  const menuId = useId();

  // Close the mobile menu whenever the route changes.
  useEffect(() => {
    setMenuOpen(false);
  }, [pathname]);

  // Allow closing the mobile menu with Escape for keyboard users.
  useEffect(() => {
    if (!menuOpen) return;
    const onKeyDown = (event: KeyboardEvent) => {
      if (event.key === "Escape") setMenuOpen(false);
    };
    document.addEventListener("keydown", onKeyDown);
    return () => document.removeEventListener("keydown", onKeyDown);
  }, [menuOpen]);

  return (
    <header className="sticky top-0 z-50 border-b border-gray/30 bg-white">
      <Container fluid className="flex h-20 items-center justify-between gap-4">
        <Link href="/" className="shrink-0" aria-label={`${"UMES Greater Annapolis Alumni Chapter"} home`}>
          <Logo />
        </Link>

        <nav aria-label="Primary" className="hidden 2xl:block">
          <ul className="flex items-center gap-5">
            {primaryNav.map((item) => {
              const isActive = pathname === item.href;
              return (
                <li key={item.href} className="shrink-0">
                  <Link
                    href={item.href}
                    aria-current={isActive ? "page" : undefined}
                    className={`whitespace-nowrap text-sm font-semibold transition-colors hover:text-maroon ${
                      isActive ? "text-maroon" : "text-black"
                    }`}
                  >
                    {item.label}
                  </Link>
                </li>
              );
            })}
          </ul>
        </nav>

        <div className="hidden shrink-0 2xl:block">
          <Link href="/membership" className="btn-primary whitespace-nowrap">
            Join the Chapter
          </Link>
        </div>

        <button
          type="button"
          className="inline-flex shrink-0 items-center justify-center rounded-md border border-gray/40 p-2 text-black 2xl:hidden"
          aria-expanded={menuOpen}
          aria-controls={menuId}
          aria-label={menuOpen ? "Close menu" : "Open menu"}
          onClick={() => setMenuOpen((open) => !open)}
        >
          <MenuIcon open={menuOpen} />
        </button>
      </Container>

      <div
        id={menuId}
        className={`2xl:hidden ${menuOpen ? "block" : "hidden"} border-t border-gray/30 bg-white`}
      >
        <Container className="flex flex-col gap-1 py-4">
          <nav aria-label="Mobile primary">
            <ul className="flex flex-col">
              {primaryNav.map((item) => {
                const isActive = pathname === item.href;
                return (
                  <li key={item.href}>
                    <Link
                      href={item.href}
                      aria-current={isActive ? "page" : undefined}
                      className={`block rounded-md px-2 py-3 text-base font-semibold ${
                        isActive ? "bg-maroon/10 text-maroon" : "text-black hover:bg-gray/10"
                      }`}
                    >
                      {item.label}
                    </Link>
                  </li>
                );
              })}
            </ul>
          </nav>
          <Link href="/membership" className="btn-primary mt-3 w-full">
            Join the Chapter
          </Link>
        </Container>
      </div>
    </header>
  );
}

function MenuIcon({ open }: { open: boolean }) {
  if (open) {
    return (
      <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" aria-hidden="true">
        <path d="M6 6L18 18M6 18L18 6" stroke="currentColor" strokeWidth="2" strokeLinecap="round" />
      </svg>
    );
  }
  return (
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" aria-hidden="true">
      <path d="M3 6h18M3 12h18M3 18h18" stroke="currentColor" strokeWidth="2" strokeLinecap="round" />
    </svg>
  );
}
