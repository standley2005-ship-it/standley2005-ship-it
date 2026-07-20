import type { MetadataRoute } from "next";
import { siteConfig } from "@/data/site";

// This is a staging deployment: keep it out of search engines entirely
// until the chapter confirms production launch. Flip `disallow` to
// specific paths (or remove this rule) when promoting to production.
export default function robots(): MetadataRoute.Robots {
  return {
    rules: {
      userAgent: "*",
      disallow: "/",
    },
    sitemap: `${siteConfig.url}/sitemap.xml`,
  };
}
