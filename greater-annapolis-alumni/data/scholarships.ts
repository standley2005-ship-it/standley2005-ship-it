/**
 * Scholarship program content, kept separate from events and
 * community-service content per the site's content architecture.
 *
 * FOR CHAPTER OFFICERS:
 * - Set `cycleStatus` to "open", "closed", or "unconfirmed" to control
 *   which state the Scholarships page and homepage section show.
 * - Update `deadline` (YYYY-MM-DD) once a real deadline is confirmed.
 * - Edit `eligibility` and `requiredMaterials` as plain-text bullet lists.
 * - Set `applicationHref` to the live application link/form once confirmed.
 * - Only add entries to `previousRecipients` once names are verified
 *   and the chapter has approved publishing them.
 */

export type ScholarshipCycleStatus = "open" | "closed" | "unconfirmed";

export const scholarshipProgram = {
  cycleStatus: "unconfirmed" as ScholarshipCycleStatus,
  currentCycleLabel: "DRAFT — current scholarship cycle not confirmed",
  deadline: null as string | null, // e.g. "2026-04-01" once confirmed
  nextCycleExpectation:
    "DRAFT — the chapter has not yet confirmed when the next scholarship application cycle will open. This section will be updated once that information is available.",
  eligibility: [
    "DRAFT — eligibility criteria not yet confirmed (e.g. graduating high school senior in the Greater Annapolis service area).",
    "DRAFT — GPA or academic requirement not yet confirmed.",
    "DRAFT — residency or UMES-enrollment requirement not yet confirmed.",
  ],
  requiredMaterials: [
    "DRAFT — required application materials not yet confirmed (e.g. application form, transcript, essay, letters of recommendation).",
  ],
  applicationHref: "#",
  contactEmail: "DRAFT: scholarships@greaterannapolischapter.org (confirm)",
} as const;

export type ScholarshipRecipient = {
  year: string;
  name: string;
  note?: string;
};

/**
 * Empty until the chapter verifies and approves publishing recipient
 * names. Do not populate with guessed or unverified names.
 */
export const previousRecipients: ScholarshipRecipient[] = [];
