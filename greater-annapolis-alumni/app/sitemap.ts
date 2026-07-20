import type { MetadataRoute } from "next";
import { siteConfig } from "@/data/site";

const routes = [
  "",
  "/about",
  "/leadership",
  "/membership",
  "/scholarships",
  "/events",
  "/community-service",
  "/gallery",
  "/contact",
  "/accessibility",
  "/privacy",
];

export default function sitemap(): MetadataRoute.Sitemap {
  return routes.map((route) => ({
    url: `${siteConfig.url}${route}`,
    lastModified: new Date(),
  }));
}
