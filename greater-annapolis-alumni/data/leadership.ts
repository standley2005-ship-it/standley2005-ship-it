/**
 * Executive board / officer roster.
 *
 * IMPORTANT CONTEXT: the previous live site's executive-board page had
 * duplicated and mismatched names, photos, titles, and graduation
 * years. None of that data was trustworthy enough to reuse, so every
 * entry below is a clearly-labeled placeholder, not a real officer.
 * Do NOT fill in a guessed name, year, or photo — replace each
 * placeholder only once the chapter confirms the real officer.
 *
 * FOR CHAPTER OFFICERS: to replace a board member, edit the matching
 * object below:
 *   - `name`: full name as the chapter wants it displayed.
 *   - `position`: official title (e.g. "President", "Treasurer").
 *   - `classYear`: UMES graduation year, e.g. "Class of 2011".
 *   - `photo`: path to a photo placed in /public/images/leadership/,
 *     or leave null to show the placeholder avatar.
 *   - `bio`: optional, one short paragraph.
 *   - `verified`: leave `false` until the chapter has confirmed this
 *     specific entry. Unverified officers still display, but the
 *     leadership page marks them as pending confirmation.
 * To add or remove a board seat, add or remove an object from the array.
 */

export type Officer = {
  id: string;
  name: string;
  position: string;
  classYear: string;
  photo: string | null;
  bio?: string;
  verified: boolean;
  featuredOnHome: boolean;
};

export const officers: Officer[] = [
  {
    id: "president",
    name: "Name Not Confirmed",
    position: "President",
    classYear: "Class year not confirmed",
    photo: null,
    bio: "DRAFT — president's biography not yet provided by the chapter.",
    verified: false,
    featuredOnHome: true,
  },
  {
    id: "vice-president",
    name: "Name Not Confirmed",
    position: "Vice President",
    classYear: "Class year not confirmed",
    photo: null,
    verified: false,
    featuredOnHome: true,
  },
  {
    id: "secretary",
    name: "Name Not Confirmed",
    position: "Secretary",
    classYear: "Class year not confirmed",
    photo: null,
    verified: false,
    featuredOnHome: true,
  },
  {
    id: "treasurer",
    name: "Name Not Confirmed",
    position: "Treasurer",
    classYear: "Class year not confirmed",
    photo: null,
    verified: false,
    featuredOnHome: false,
  },
];

/** President's welcome message shown on the About page. */
export const presidentWelcome = {
  authorName: "Name Not Confirmed",
  authorTitle: "President, Greater Annapolis Alumni Chapter",
  message:
    "DRAFT PLACEHOLDER — a personal welcome message from the current chapter president has not yet been provided. Replace this paragraph with the president's approved welcome text before launch.",
  verified: false,
};
