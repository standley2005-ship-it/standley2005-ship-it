/**
 * Community-service initiatives: active campaigns, needed items,
 * volunteer opportunities, and a completed-project archive.
 *
 * FOR CHAPTER OFFICERS:
 * - Move a finished initiative from `activeInitiatives` to
 *   `completedProjects` once it wraps up.
 * - `status` controls the badge shown on the Community Service page.
 * - `neededItems` is a simple string list — edit freely.
 */

export type InitiativeStatus = "active" | "ongoing" | "planned" | "completed";

export type Initiative = {
  id: string;
  title: string;
  status: InitiativeStatus;
  summary: string;
  neededItems?: string[];
  volunteerInfo?: string;
  verified: boolean;
};

export const activeInitiatives: Initiative[] = [
  {
    id: "hygiene-collection",
    title: "Hygiene Product Collection",
    status: "active",
    summary:
      "DRAFT — details of the chapter's hygiene-product collection drive (partner organization, drop-off locations, current needs) have not been confirmed.",
    neededItems: ["DRAFT — specific needed items not yet confirmed"],
    verified: false,
  },
  {
    id: "volunteer-projects",
    title: "Volunteer Projects",
    status: "ongoing",
    summary:
      "DRAFT — current volunteer project opportunities have not been confirmed.",
    volunteerInfo:
      "DRAFT — how to sign up to volunteer has not been confirmed.",
    verified: false,
  },
];

export type CompletedProject = {
  id: string;
  title: string;
  year: string;
  summary: string;
  verified: boolean;
};

/**
 * Empty until the chapter supplies verified information about
 * completed community-service projects.
 */
export const completedProjects: CompletedProject[] = [];

export const campaignContact = {
  label: "Community Service Chair",
  email: "DRAFT: service@greaterannapolischapter.org (confirm)",
  verified: false,
};
