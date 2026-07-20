# UMES Greater Annapolis Alumni Chapter — Website Redesign (Staging)

A modern, accessible, mobile-friendly redesign of the UMES Greater Annapolis Alumni Chapter
website, built with Next.js, TypeScript, and Tailwind CSS.

**This is a staging project.** It is not connected to the live site
(`greaterannapolischapter.org`), any production DNS, payment links, or chapter email accounts.
Forms on this site do not send real email. See `CONTENT_VERIFICATION.md` before any production
launch.

## Tech Stack

- [Next.js 14](https://nextjs.org/) (App Router) + TypeScript
- [Tailwind CSS](https://tailwindcss.com/) with a UMES-inspired design system (maroon `#651D32`,
  gray `#888B8D`, white, black)
- No backend/database — all content lives in typed files under `data/`

## Setup

```bash
npm install
```

## Development

```bash
npm run dev
```

Visit `http://localhost:3000`.

Other useful commands:

```bash
npm run lint       # ESLint
npm run typecheck  # TypeScript, no emit
npm run build      # production build (also runs during CI/deploys)
npm run start      # serve the production build locally
```

## Project Structure

```
app/                 Routes (Next.js App Router) — one folder per page
components/
  layout/             Header, Footer, AnnouncementBar
  home/                Homepage sections (Hero, Impact, Membership, etc.)
  events/              Event card, events tabs
  gallery/             Gallery grid + filters + lightbox
  leadership/          Officer card
  forms/               Contact form, email signup form
  ui/                  Small shared primitives (buttons, badges, empty states)
data/                 All editable content (see "Content Editing" below)
lib/                  Small helpers (event date logic, ICS generation, structured data)
public/images/        Static images (logo, gallery, leadership photos)
```

## Content Editing (for Chapter Officers)

**You do not need to know how to code to update most of this site.** All editable content lives
in plain TypeScript files under `data/`. Each file has a comment block at the top explaining what
it controls. Open the file in any text editor, change the text between quotes, save, and (if
using a deploy pipeline) commit + push — the site rebuilds automatically.

| File | Controls |
|---|---|
| `data/site.ts` | Chapter contact info, announcement bar, external links (membership, dues, donation, scholarship application, Google Calendar), social links, homepage impact statistics |
| `data/navigation.ts` | Header/mobile menu links |
| `data/leadership.ts` | Executive board roster and the About page's president's welcome |
| `data/events.ts` | All events — upcoming/past classification is automatic based on today's date |
| `data/scholarships.ts` | Scholarship cycle status, eligibility, deadline, required materials |
| `data/initiatives.ts` | Community-service initiatives and completed-project archive |
| `data/gallery.ts` | Gallery photos, captions, alt text, categories, years |
| `data/membership.ts` | Membership eligibility, benefits, dues, FAQ |

### Adding an event

Open `data/events.ts` and add a new object to the `events` array:

```ts
{
  id: "spring-mixer-2026",
  title: "Spring Alumni Mixer",
  date: "2026-04-18",       // YYYY-MM-DD
  time: "6:00 PM – 8:00 PM",
  location: "Annapolis, MD",
  description: "An evening of fellowship for chapter members and friends.",
  registrationHref: "https://...",   // or "#" if not yet available
  icsAvailable: true,
  verified: true,             // set true once details are confirmed
  image: null,
}
```

The event automatically appears under **Upcoming Events** until its date passes, then it moves
itself to **Past Events** — you never need to move it manually.

### Editing an event

Find the event by its `id` in `data/events.ts` and change any field.

### Replacing a board member

Open `data/leadership.ts` and edit the matching object in the `officers` array (`name`,
`position`, `classYear`, `photo`, `bio`). Set `verified: true` once the chapter has confirmed
that specific officer. To add or remove a board seat, add or remove an object from the array.

### Opening or closing scholarship applications

Open `data/scholarships.ts` and set `cycleStatus` to `"open"`, `"closed"`, or `"unconfirmed"`.

### Updating a deadline

Scholarship deadline: `data/scholarships.ts` → `deadline` (format `"YYYY-MM-DD"`).
Event dates: `data/events.ts` → the event's `date` field.

### Changing membership/dues/donation links

Open `data/site.ts` → `externalLinks`. Replace the `href` for `localChapterApplication`,
`chapterDuesPayment`, `donation`, `scholarshipApplication`, `nationalAlumniMembership`, or
`googleCalendar`. Any link left as `"#"` is automatically shown as "coming soon" instead of a
dead clickable button, so it's safe to leave unconfirmed links as `"#"` until they're ready.

### Changing the announcement bar

Open `data/site.ts` → `announcement`. Edit `message` and `linkHref`/`linkLabel`, or set
`active: false` to hide the bar entirely.

### Adding photographs

1. Place the image file in `public/images/gallery/` (or `public/images/leadership/` for officer
   headshots).
2. In `data/gallery.ts`, add an entry with `photo: "/images/gallery/your-file.jpg"` and a
   meaningful `alt` description (for screen readers).

### Updating contact information

Open `data/site.ts` → `contact` (email, phone, meeting schedule, meeting location).

## Building

```bash
npm run build
```

Outputs a fully static-optimized Next.js production build (all pages currently prerender to
static HTML).

## Deploying to Staging

This project is deployed to a **staging URL only** — see the top of this file. The
`robots.ts`/`app/robots.ts` route disallows all crawling and `app/layout.tsx` sets
`robots: { index: false, follow: false }` so the staging deployment is not indexed by search
engines. Do not point production DNS at this deployment without first:

1. Completing every item in `CONTENT_VERIFICATION.md`.
2. Removing the noindex/robots-disallow staging settings referenced above.
3. Confirming real payment, registration, and application links replace every `"#"` placeholder.

## Related Documentation

- `CONTENT_VERIFICATION.md` — everything the chapter must confirm before production launch
- `CONTENT_INVENTORY.md` — how content from the old site was categorized (reuse/rewrite/etc.)
- `QA_CHECKLIST.md` — manual test checklist for routes, forms, accessibility, and responsiveness
