/**
 * Chapter-wide settings: contact info, external links, social accounts,
 * and the homepage announcement bar.
 *
 * FOR CHAPTER OFFICERS (no coding experience needed):
 * - To change the announcement bar text, edit `announcement` below.
 * - To change the chapter email/phone, edit `contact`.
 * - To point "Join," "Pay Dues," or "Donate" buttons at a real form,
 *   replace the matching URL in `externalLinks`. Leave a URL as "#"
 *   only if the destination is not confirmed yet — pages will show a
 *   "coming soon" style notice instead of a live link when the value
 *   is "#".
 * - To update social links, edit `social`.
 *
 * Every value marked DRAFT must be confirmed by the chapter before
 * production launch. See CONTENT_VERIFICATION.md for the full list.
 */

export const siteConfig = {
  name: "UMES Greater Annapolis Alumni Chapter",
  shortName: "Greater Annapolis Alumni Chapter",
  university: "University of Maryland Eastern Shore",
  tagline: "Connecting Hawks. Supporting Students. Serving Greater Annapolis.",
  description:
    "The Greater Annapolis Alumni Chapter brings University of Maryland Eastern Shore alumni and friends together through fellowship, service, student support, and Hawk pride.",
  // Set to the confirmed staging or production URL before launch.
  url: "https://staging.greaterannapolischapter.example.org",
  serviceArea:
    "Anne Arundel County and the greater Annapolis, Maryland region (DRAFT — confirm exact service-area boundaries with the chapter).",
} as const;

export const contact = {
  // DRAFT — none of these have been confirmed against a current chapter source.
  email: "DRAFT: info@greaterannapolischapter.org (confirm current inbox)",
  phone: "DRAFT: (000) 000-0000 (confirm current chapter phone line)",
  mailingAddress: "DRAFT: mailing address not confirmed",
  meetingSchedule:
    "DRAFT: meeting cadence not confirmed (e.g. \"2nd Saturday of each month\")",
  meetingLocation: "DRAFT: meeting location not confirmed",
} as const;

/**
 * Homepage announcement bar. Keep this short — one line of text plus a
 * link. Set `active: false` to hide the bar entirely (e.g. between
 * campaigns) without deleting the content.
 */
export const announcement = {
  active: true,
  message:
    "DRAFT: Next chapter meeting, scholarship deadline, and event details are being confirmed — check back soon.",
  linkLabel: "See upcoming events",
  linkHref: "/events",
} as const;

/**
 * External destinations the site links out to. Replace "#" with a real,
 * chapter-approved URL when one is confirmed. Until then, components
 * treat "#" as "not yet available" and avoid presenting the link as
 * live/clickable action.
 */
export const externalLinks = {
  nationalAlumniMembership: {
    label: "National Alumni Association Membership",
    href: "#",
    note: "DRAFT — link to the UMES National Alumni Association membership page not yet confirmed.",
  },
  localChapterApplication: {
    label: "Local Chapter Application",
    href: "#",
    note: "DRAFT — local Greater Annapolis Chapter application link not yet confirmed.",
  },
  chapterDuesPayment: {
    label: "Pay Chapter Dues",
    href: "#",
    note: "DRAFT — dues payment destination not yet confirmed.",
  },
  donation: {
    label: "Donate",
    href: "#",
    note: "DRAFT — approved donation link not yet confirmed.",
  },
  scholarshipApplication: {
    label: "Scholarship Application",
    href: "#",
    note: "DRAFT — scholarship application link not yet confirmed.",
  },
  googleCalendar: {
    label: "Subscribe on Google Calendar",
    href: "#",
    note: "DRAFT — chapter Google Calendar link not yet confirmed.",
  },
  umesAlumniRelations: {
    label: "UMES Office of Alumni Relations",
    href: "https://www.umes.edu/alumni/",
    note: "University alumni relations landing page.",
  },
  umesNationalAlumniAssociation: {
    label: "UMES National Alumni Association",
    href: "https://www.umes.edu/alumni/",
    note: "DRAFT — confirm the exact National Alumni Association URL (may differ from general Alumni Relations page).",
  },
  umesUniversityHistory: {
    label: "UMES University History",
    href: "https://www.umes.edu/about/",
    note: "Official university history/about page, linked instead of reproducing a long history on this site.",
  },
} as const;

export const social = {
  facebook: { label: "Facebook", href: "#", note: "DRAFT — confirm chapter Facebook page URL." },
  instagram: { label: "Instagram", href: "#", note: "DRAFT — confirm chapter Instagram handle." },
  linkedin: { label: "LinkedIn", href: "#", note: "DRAFT — confirm chapter LinkedIn presence, if any." },
} as const;

/**
 * Editable homepage impact statistics. Replace `value` with a verified
 * number and set `confirmed: true` only once the chapter has approved
 * the figure. Never invent a number — leave "To be confirmed." as shown.
 */
export const impactStats = [
  { id: "scholarships-awarded", label: "Scholarships Awarded", value: "To be confirmed.", confirmed: false },
  { id: "students-supported", label: "Students Supported", value: "To be confirmed.", confirmed: false },
  { id: "community-projects", label: "Community Projects", value: "To be confirmed.", confirmed: false },
  { id: "active-members", label: "Active Members", value: "To be confirmed.", confirmed: false },
] as const;
