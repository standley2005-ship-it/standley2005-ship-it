/**
 * Primary site navigation, shown in the header and mobile menu.
 *
 * FOR CHAPTER OFFICERS: to add, remove, or reorder a menu item, add or
 * remove an entry below. `href` must match one of the page routes in
 * the `app/` folder (e.g. "/events" corresponds to app/events/page.tsx).
 */

export type NavItem = {
  label: string;
  href: string;
};

export const primaryNav: NavItem[] = [
  { label: "Home", href: "/" },
  { label: "About", href: "/about" },
  { label: "Leadership", href: "/leadership" },
  { label: "Membership", href: "/membership" },
  { label: "Scholarships", href: "/scholarships" },
  { label: "Events", href: "/events" },
  { label: "Community Service", href: "/community-service" },
  { label: "Gallery", href: "/gallery" },
  { label: "Contact", href: "/contact" },
];
