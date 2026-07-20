# Content Verification Checklist

This staging redesign was built without inventing or silently correcting any fact the chapter
has not confirmed. Every item below is currently a **DRAFT placeholder** in the codebase (see the
file reference in each row) and must be confirmed, corrected, or supplied by the chapter before
production launch.

**Why this list exists:** the previous live site had a July 13, 2025 Crab Feast still presented
as current, past and upcoming events mixed together, and an executive-board page with duplicated
and mismatched names, photos, titles, and graduation years. Rather than guess at corrections,
this redesign treats all of that information as unverified.

## Leadership

| Item | Status | Where it lives |
|---|---|---|
| Current president (name) | **DRAFT — not confirmed** | `data/leadership.ts` → `officers[id="president"]`, `presidentWelcome` |
| Current executive board (full roster) | **DRAFT — not confirmed.** Only four placeholder seats exist (President, VP, Secretary, Treasurer); confirm whether this is the complete board or additional seats (e.g. Financial Secretary, Chaplain, Historian, committee chairs) exist | `data/leadership.ts` → `officers` |
| Officer titles | **DRAFT** — confirm exact titles/spelling for each seat | `data/leadership.ts` |
| Graduation years (class years) for each officer | **DRAFT — not confirmed** for any officer | `data/leadership.ts` → `classYear` |
| Officer photos | **Missing** — no official headshots supplied; placeholders shown | `data/leadership.ts` → `photo: null`, `public/images/leadership/` |
| President's welcome message (About page) | **DRAFT placeholder text** — needs real, approved copy | `data/leadership.ts` → `presidentWelcome` |

## Contact & Chapter Info

| Item | Status | Where it lives |
|---|---|---|
| Chapter email | **DRAFT — not confirmed** | `data/site.ts` → `contact.email` |
| Phone number | **DRAFT — not confirmed** | `data/site.ts` → `contact.phone` |
| Meeting schedule (cadence) | **DRAFT — not confirmed** | `data/site.ts` → `contact.meetingSchedule` |
| Meeting location | **DRAFT — not confirmed** | `data/site.ts` → `contact.meetingLocation` |
| Mailing address | **DRAFT — not confirmed** | `data/site.ts` → `contact.mailingAddress` |
| Service-area boundaries | **DRAFT** — currently described generally as "Anne Arundel County and the greater Annapolis, Maryland region"; confirm exact boundaries | `data/site.ts` → `siteConfig.serviceArea` |

## Membership

| Item | Status | Where it lives |
|---|---|---|
| Membership eligibility criteria | **DRAFT — not confirmed** | `data/membership.ts` → `membershipInfo.eligibility` |
| Membership benefits | **DRAFT — not confirmed** | `data/membership.ts` → `membershipInfo.benefits` |
| Membership dues amount & frequency | **DRAFT — not confirmed** | `data/membership.ts` → `membershipInfo.dues` |
| Membership application link | **Not available — set to "#"** | `data/site.ts` → `externalLinks.localChapterApplication` |
| Local vs. national membership relationship | **DRAFT explanation** — needs chapter confirmation of exact policy | `data/membership.ts` → `membershipInfo.localVsNational` |
| National Alumni Association membership link | **Not available — set to "#"** | `data/site.ts` → `externalLinks.nationalAlumniMembership` |

## Payments & Donations

| Item | Status | Where it lives |
|---|---|---|
| Dues payment link/destination | **Not available — set to "#"** | `data/site.ts` → `externalLinks.chapterDuesPayment` |
| Donation link | **Not available — set to "#"** | `data/site.ts` → `externalLinks.donation` |

## Scholarships

| Item | Status | Where it lives |
|---|---|---|
| Current scholarship cycle status (open/closed) | **DRAFT — set to "unconfirmed"** | `data/scholarships.ts` → `scholarshipProgram.cycleStatus` |
| Scholarship application deadline | **Not confirmed (null)** | `data/scholarships.ts` → `scholarshipProgram.deadline` |
| Scholarship eligibility criteria | **DRAFT — not confirmed** | `data/scholarships.ts` → `scholarshipProgram.eligibility` |
| Required application materials | **DRAFT — not confirmed** | `data/scholarships.ts` → `scholarshipProgram.requiredMaterials` |
| Next-cycle expectations | **DRAFT — not confirmed** | `data/scholarships.ts` → `scholarshipProgram.nextCycleExpectation` |
| Scholarship application link | **Not available — set to "#"** | `data/scholarships.ts` → `scholarshipProgram.applicationHref` |
| Previous scholarship recipients | **Empty — none verified/approved for publication** | `data/scholarships.ts` → `previousRecipients` |

## Events

| Item | Status | Where it lives |
|---|---|---|
| Upcoming events | **None confirmed** — homepage/Events page show an honest "no upcoming event" empty state | `data/events.ts` → `events` |
| July 13, 2025 Crab Feast | Carried over from the old site **as a past event only** (its date has passed). Time, exact location, pricing, and beneficiary were never confirmed | `data/events.ts` → `events[id="crab-feast-2025"]` |
| Google Calendar link | **Not available — set to "#"** | `data/site.ts` → `externalLinks.googleCalendar` |

## Community Service

| Item | Status | Where it lives |
|---|---|---|
| Hygiene collection drive details (partner org, drop-off locations, current needs) | **DRAFT — not confirmed** | `data/initiatives.ts` → `activeInitiatives[id="hygiene-collection"]` |
| Current volunteer project opportunities | **DRAFT — not confirmed** | `data/initiatives.ts` → `activeInitiatives[id="volunteer-projects"]` |
| Campaign contact | **DRAFT — not confirmed** | `data/initiatives.ts` → `campaignContact` |
| Completed-project archive | **Empty — none verified** | `data/initiatives.ts` → `completedProjects` |

## Gallery / Photography

| Item | Status | Where it lives |
|---|---|---|
| Approved chapter logo files | **Missing.** A text/monogram placeholder is used site-wide; do not treat it as final branding | `components/ui/Logo.tsx`, `public/images/logo/` |
| Official event/meeting/service photographs | **Missing.** Gallery is intentionally empty rather than filled with stock or placeholder imagery | `data/gallery.ts` |

## Impact Statistics

| Item | Status | Where it lives |
|---|---|---|
| Scholarships awarded (total) | **"To be confirmed."** — no number has been invented | `data/site.ts` → `impactStats` |
| Students supported (total) | **"To be confirmed."** | `data/site.ts` → `impactStats` |
| Community projects (total) | **"To be confirmed."** | `data/site.ts` → `impactStats` |
| Active members (count) | **"To be confirmed."** | `data/site.ts` → `impactStats` |

## Social Media

| Item | Status | Where it lives |
|---|---|---|
| Facebook page URL | **Not confirmed — set to "#"** | `data/site.ts` → `social.facebook` |
| Instagram handle/URL | **Not confirmed — set to "#"** | `data/site.ts` → `social.instagram` |
| LinkedIn presence | **Not confirmed — set to "#"**; confirm whether one exists at all | `data/site.ts` → `social.linkedin` |

## University Links

| Item | Status | Where it lives |
|---|---|---|
| UMES National Alumni Association URL | **DRAFT** — currently points at the general UMES Alumni Relations page; confirm the exact National Alumni Association URL if it differs | `data/site.ts` → `externalLinks.umesNationalAlumniAssociation` |
| UMES Office of Alumni Relations URL | Believed correct (`https://www.umes.edu/alumni/`) but should be spot-checked before launch | `data/site.ts` → `externalLinks.umesAlumniRelations` |

## Sign-off

Before removing the staging `noindex`/robots-disallow settings and pointing production DNS at
this redesign, a chapter officer (ideally the President or designated web coordinator) should:

1. Go through every row above and either confirm the current draft or supply the corrected value.
2. Update the corresponding field in the listed `data/*.ts` file (see `README.md` → "Content
   Editing" for how).
3. Set the matching `verified: true` flag where one exists (leadership, events, initiatives) so
   the "Pending Confirmation" / "Details Unconfirmed" badges disappear from the live site.
4. Confirm no `href: "#"` placeholders remain for any link that should be live in production.
