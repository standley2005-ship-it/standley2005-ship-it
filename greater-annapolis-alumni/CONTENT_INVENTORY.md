# Content Inventory: Previous Site vs. Redesign

## Audit method and a limitation to disclose

This task asked for a thorough audit of `https://greaterannapolischapter.org/` before rebuilding
the site. During this session, direct automated access to that domain returned an **HTTP 403
(Forbidden)** response (the site's hosting appears to block automated fetches), and an
Internet Archive lookup was also unavailable in this environment. As a result, this inventory is
built from the **known-issues brief supplied for this project** (which itself reflects a prior
human review of the live site) rather than a fresh page-by-page scrape performed in this session.

**Action item for the chapter/developer:** before production launch, someone with a normal
browser should do a manual pass of every page on the live site and compare it against this
inventory, filling in the "Needs client approval" rows with the actual current text. Do not treat
this document as a substitute for that manual review.

## Categorization key

- **Reuse** — content is accurate and can be carried into the redesign as-is
- **Rewrite** — the underlying fact is fine but the copy/presentation should be modernized
- **Archive** — outdated but historically relevant; move out of "current" surfaces (e.g. past
  events)
- **Remove** — no longer relevant and should not appear anywhere on the new site
- **Missing** — the old site doesn't appear to have this content, or it wasn't visible/accessible
  to audit, and it's needed for the new site
- **Conflicting** — the old site shows contradictory versions of this fact
- **Needs client approval** — a judgment call the chapter must make, not a content fact

## Findings

| Content Area | Old-Site Finding | Category | Notes |
|---|---|---|---|
| July 13, 2025 Crab Feast | Still shown prominently as if current/upcoming | **Archive** | Its date has passed. Redesign keeps it only in the Past Events list (`data/events.ts`), with details marked DRAFT since specifics (location, price, beneficiary) weren't confirmed. |
| Event listings generally | Past and upcoming events mixed together in one list | **Rewrite** | Redesign replaces this with automatic date-based classification (`lib/events.ts`) so this class of bug can't recur. |
| Executive board page | Reported to contain duplicated and mismatched names, photos, titles, and graduation years | **Conflicting** | Not reusable in any form — see `CONTENT_VERIFICATION.md`. Redesign ships a clean data-driven officer grid with every seat marked "Pending Confirmation" until the chapter supplies verified names. |
| Current president | Unclear from mismatched board page | **Conflicting / Missing** | Needs client approval — chapter must state definitively who currently holds this seat. |
| Scholarship application cycle | Old site does not clearly identify the next application cycle | **Missing** | Redesign ships an honest "status unconfirmed" state instead of guessing a cycle. |
| Payment / registration / membership links | Reported as unclear destinations | **Missing / Needs client approval** | All such links are implemented as configurable fields defaulting to "#" (shown as "coming soon," never a dead-looking live button) until the chapter supplies the real destination. |
| Chapter mission / "who we are" messaging | Presumed present in some form on the old site (typical of alumni chapter sites) but not independently verified this session | **Needs client approval** | Redesign drafted new mission copy for Home/About based on the chapter's stated tagline and description; chapter should review and approve final wording. |
| UMES heritage/history content | Older alumni sites sometimes reproduce long university history text | **Rewrite** | Per the brief, the redesign links out to the official UMES history page instead of reproducing a long history section. |
| Chapter email / phone / meeting schedule | Not independently confirmed this session | **Missing** | Marked DRAFT throughout; see `CONTENT_VERIFICATION.md`. |
| Chapter logo | Existing logo presumed present on old site | **Needs client approval** | This redesign deliberately does **not** recreate or alter any UMES/chapter logo. A text-based placeholder mark is used until the chapter supplies approved logo files. |
| Photography (events, service, meetings) | Presumed present on old site in some form | **Missing** | No photography was supplied for this redesign; the Gallery ships intentionally empty with a clear "coming soon" state rather than stock imagery. |
| Community service content (hygiene drive, volunteer projects) | Referenced in the project brief as an existing chapter activity area | **Needs client approval** | Structure was built (`data/initiatives.ts`) but specific current needs/partners/drop-off info must come from the chapter. |
| Social media links | Not independently confirmed this session | **Missing** | Placeholder "#" links pending chapter confirmation. |
| Impact statistics (scholarships awarded, students supported, etc.) | Not independently confirmed this session; no verified numbers available | **Missing** | Redesign explicitly avoids inventing numbers — shows "To be confirmed." |
| National Alumni Association / Alumni Relations links | Presumed to exist in some form; general Alumni Relations URL used as a best-effort placeholder | **Needs client approval** | Confirm exact URLs, especially whether a distinct National Alumni Association page exists apart from the general Alumni Relations page. |

## What was NOT carried over from the old site

- The old executive-board page's specific names/photos/titles/years — none of it could be trusted
  enough to reuse; see the Leadership row above.
- The Crab Feast as an *upcoming* event — it is only shown as a past event now.
- Any specific dollar figures, member counts, or "impact" numbers — none were available to verify,
  so none were invented.
- The old site's logo artwork itself was not copied, altered, or recreated; a placeholder stands
  in until official files are supplied.

## Net-new structure introduced in the redesign

Content areas that likely didn't exist in this form on the old site, added to meet the project's
requirements: automatic upcoming/past event classification, a filterable gallery with lightbox,
a membership FAQ, a scholarship-specific page separate from events/community-service, a
community-service completed-project archive, an accessibility statement, and a privacy notice.
