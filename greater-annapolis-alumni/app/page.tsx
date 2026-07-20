import { Hero } from "@/components/home/Hero";
import { UpcomingEventSection } from "@/components/home/UpcomingEventSection";
import { MissionSection } from "@/components/home/MissionSection";
import { ImpactSection } from "@/components/home/ImpactSection";
import { MembershipSection } from "@/components/home/MembershipSection";
import { ScholarshipSection } from "@/components/home/ScholarshipSection";
import { CommunityServiceSection } from "@/components/home/CommunityServiceSection";
import { GalleryPreviewSection } from "@/components/home/GalleryPreviewSection";
import { LeadershipPreviewSection } from "@/components/home/LeadershipPreviewSection";
import { ContactCtaSection } from "@/components/home/ContactCtaSection";

export default function HomePage() {
  return (
    <>
      <Hero />
      <UpcomingEventSection />
      <MissionSection />
      <ImpactSection />
      <MembershipSection />
      <ScholarshipSection />
      <CommunityServiceSection />
      <GalleryPreviewSection />
      <LeadershipPreviewSection />
      <ContactCtaSection />
    </>
  );
}
