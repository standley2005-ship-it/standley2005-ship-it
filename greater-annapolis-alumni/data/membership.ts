/**
 * Membership program content: eligibility, benefits, dues, and FAQs.
 *
 * FOR CHAPTER OFFICERS:
 * - Edit `benefits`, `eligibility` as plain bullet lists.
 * - Update `dues` once the current amount is confirmed.
 * - `applicationHref` / `paymentHref` should point at the real forms —
 *   see data/site.ts `externalLinks` for the shared link config used
 *   across the site (this file mirrors the ones membership pages need).
 * - Add or edit FAQ entries in `faqs`.
 */

export const membershipInfo = {
  eligibility: [
    "DRAFT — membership eligibility criteria not yet confirmed (e.g. UMES graduates, friends of UMES).",
  ],
  benefits: [
    "DRAFT — member benefits not yet confirmed (e.g. networking events, voting rights, scholarship-committee eligibility).",
  ],
  dues: {
    amount: "DRAFT — dues amount not yet confirmed",
    frequency: "DRAFT — dues frequency not yet confirmed (annual/lifetime)",
  },
  localVsNational:
    "DRAFT — explanation of how local chapter membership relates to National Alumni Association membership has not been confirmed. Typically chapter membership is separate from, and in addition to, national UMES Alumni Association membership — confirm the exact relationship and any requirement to hold both before publishing.",
} as const;

export type MembershipFaq = {
  question: string;
  answer: string;
};

export const membershipFaqs: MembershipFaq[] = [
  {
    question: "Do I need to be a UMES graduate to join?",
    answer:
      "DRAFT — eligibility for non-graduates ('friends of UMES') has not been confirmed.",
  },
  {
    question: "Is local chapter membership the same as National Alumni Association membership?",
    answer:
      "DRAFT — the relationship between local chapter dues and national membership has not been confirmed.",
  },
  {
    question: "How often does the chapter meet?",
    answer:
      "DRAFT — meeting schedule not yet confirmed. See the Contact page for the latest information once available.",
  },
  {
    question: "How do I pay my dues?",
    answer:
      "DRAFT — dues payment method/link not yet confirmed.",
  },
];
