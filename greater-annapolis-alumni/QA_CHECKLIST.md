# QA Checklist

Manual + automated testing checklist for the Greater Annapolis Alumni Chapter redesign. Items
marked ✅ were verified during the initial build (dev server + production build, this session).
Re-run the full manual pass in a real browser before every production launch.

## Automated checks

- [x] `npm run lint` — passes, no errors
- [x] `npm run typecheck` (`tsc --noEmit`) — passes, no errors
- [x] `npm run build` — production build succeeds; all 17 routes prerender successfully
- [x] Dev server boots and serves `200` on all routes tested (see Routes below)
- [x] No unexpected browser console errors on any tested route (only expected Next.js dev-mode
      HMR/websocket noise was observed, which does not occur in production builds)

## Routes

| Route | Loads (200) | Notes |
|---|---|---|
| `/` | ✅ | Homepage — all 10 required sections present |
| `/about` | ✅ | |
| `/leadership` | ✅ | |
| `/membership` | ✅ | |
| `/scholarships` | ✅ | |
| `/events` | ✅ | Tabs default to Upcoming |
| `/events/[slug]` | ✅ | Tested `/events/crab-feast-2025` |
| `/community-service` | ✅ | |
| `/gallery` | ✅ | |
| `/contact` | ✅ | |
| `/accessibility` | ✅ | Linked from footer |
| `/privacy` | ✅ | Linked from footer |
| `/does-not-exist` (404) | ✅ | Returns HTTP 404 and renders the custom not-found page |
| `/sitemap.xml` | ✅ | Generated, lists all routes |
| `/robots.txt` | ✅ | Disallows all crawling (staging safety) |

## Navigation

- [x] Every header nav item (Home, About, Leadership, Membership, Scholarships, Events, Community
      Service, Gallery, Contact) links to the correct route
- [x] "Join the Chapter" button present in header (desktop) and mobile menu
- [x] Active route is indicated (`aria-current="page"`, maroon highlight) in both desktop and
      mobile nav
- [x] Footer nav mirrors header nav and links correctly
- [x] Footer "University Links" (National Alumni Association, Office of Alumni Relations) open in
      a new tab with `rel="noopener noreferrer"`
- [ ] **To re-verify by chapter before launch:** confirm no nav item is missing/extra once real
      content requirements are finalized

## Mobile menu

- [x] Hamburger button toggles the menu open/closed
- [x] `aria-expanded` reflects open/closed state; `aria-controls` points at the menu panel
- [x] Menu closes on route change
- [x] Menu closes on <kbd>Escape</kbd>
- [x] All 9 nav items + "Join the Chapter" button visible and tappable inside the mobile menu
- [x] No horizontal overflow at 320px–428px widths

## Responsive layout

- [x] 320px (smallest supported width) — no horizontal scroll, all sections readable
- [x] 375px / 390px (common phones) — verified via screenshot
- [x] 768px (tablet) — grid layouts reflow correctly (spot-checked via Tailwind breakpoints)
- [x] 1024px–1536px (laptop) — **regression found and fixed:** the full desktop nav was crowding
      and one item (`Contact`) was rendering hidden behind the "Join the Chapter" button between
      roughly 1024px–1535px wide. Fixed by moving the full nav breakpoint to `2xl` (1536px) and
      showing the mobile-style menu below that width, and by making the header container fluid
      instead of capped at the content max-width. Re-verified clean at 1280px, 1440px, 1536px,
      and 1920px.
- [x] 1920px+ (large desktop) — full nav displays with comfortable spacing

## Forms

### Contact form (`/contact`)

- [x] Required-field validation blocks submission and shows field-level error messages (Name,
      Email, Inquiry Type, Message)
- [x] Email format validation rejects invalid addresses
- [x] Phone field is optional and does not block submission when empty
- [x] Valid submission shows a success message and resets the form
- [x] Honeypot field (`company`) is present, visually hidden, and excluded from the tab order
- [x] No live email is sent (by design, staging-safe) — confirmed in code and in the on-page
      disclosure text
- [x] Error and success messages use `role="alert"` / `role="status"` for screen readers

### Email signup form (homepage)

- [x] Validates email format
- [x] Shows success state on valid submission; does not send anywhere (staging-safe)

## Events logic

- [x] An event dated in the past never appears under "Upcoming Events" (verified: the July 13,
      2025 Crab Feast appears only under Past Events)
- [x] Empty upcoming-events state renders a polished message instead of a blank area or fake card,
      both on the homepage and on `/events`
- [x] Empty past-events state (hypothetical, if all events were removed) also has a friendly
      message
- [x] "Add to Calendar" is only offered when `icsAvailable: true`; otherwise a disabled button with
      an explanatory note is shown instead of a broken/dead link
- [x] Event detail pages 404 correctly for unknown slugs (via `notFound()`)

## Images / missing-image fallback

- [x] Leadership photos: `photo: null` renders a labeled "Photo Coming Soon" placeholder instead
      of a broken image icon
- [x] Gallery photos: same placeholder pattern; gallery with zero photos shows an empty state
      instead of an empty grid
- [x] Event image: same placeholder pattern when `image` is null

## Keyboard navigation & focus

- [x] Skip-to-content link is the first focusable element and becomes visible on focus
- [x] Visible focus outline (`:focus-visible`) present on links, buttons, and form fields —
      verified via screenshot
- [x] Mobile menu button and menu items are reachable and operable via keyboard
- [x] Events tabs are operable via Left/Right arrow keys per the ARIA tabs pattern, with roving
      `tabIndex`
- [x] Gallery lightbox: opens on Enter/Space (native `<button>`), closes on Escape, arrow keys
      move between photos, focus returns to the trigger photo on close

## Accessibility

- [x] Semantic landmarks: `<header>`, `<nav aria-label="...">`, `<main id="main-content">`,
      `<footer>`
- [x] Heading hierarchy: single `<h1>` per page, nested `<h2>`/`<h3>` in order (spot-checked
      Home, About, Leadership, Events)
- [x] Form fields have associated `<label>` elements (via `useId()`); invalid fields set
      `aria-invalid` and `aria-describedby`
- [x] Reduced-motion preference respected (`prefers-reduced-motion` disables animation/scroll
      easing in `app/globals.css`)
- [x] Color contrast spot-check: found `text-gray` (`#888B8D`) on white failed WCAG AA for small
      text (~3.4:1); replaced with `text-black/60` (~5.7:1) in `ActionLink` and `EventCard`
- [x] All meaningful images require `alt` text in the data model (gallery `alt` field is required
      by type); decorative icons use `aria-hidden="true"`
- [x] Disabled/"coming soon" action buttons use `role="button"` + `aria-disabled="true"` +
      `tabIndex={-1}` rather than looking clickable while doing nothing
- [ ] **Recommended before launch:** run an automated pass (e.g. axe DevTools or Lighthouse
      Accessibility) against the deployed staging URL and a manual screen-reader pass (VoiceOver
      or NVDA) — not performed in this environment

## SEO / quality

- [x] Unique `<title>` and meta description per route (via Next.js `metadata` exports)
- [x] Open Graph metadata set at the root layout level
- [x] `sitemap.xml` lists every page
- [x] `robots.txt` currently disallows all crawling — **intentional for staging**; must be relaxed
      for production
- [x] Organization JSON-LD emitted with only confirmed fields (name, url, description); no
      unconfirmed contact/address data included
- [x] Event JSON-LD only emitted for events with `verified: true` (currently none, so none is
      emitted — correct, since nothing is confirmed yet)
- [x] Custom 404 page
- [x] No event on the site displays a hardcoded expired date as "upcoming"
- [x] No button links to "#" without an explanatory "coming soon" note — see `ActionLink`
- [x] No invented statistics, names, or claims anywhere in the shipped copy

## Known remaining limitations (see also `CONTENT_VERIFICATION.md`)

- All leadership, contact, membership, scholarship, and event details are unverified drafts.
- No official logo or photography has been supplied; placeholders are used throughout.
- Contact and email-signup forms do not send real email yet — no email provider is connected.
- Spam protection is a honeypot placeholder only; add a real provider (reCAPTCHA/hCaptcha/
  Turnstile) before production.
- No automated accessibility scanner (axe/Lighthouse) or screen-reader pass was run in this
  environment — recommended before launch.
- Live audit of `greaterannapolischapter.org` could not be performed in this session (site
  returned HTTP 403 to automated fetches); see `CONTENT_INVENTORY.md` for details.
