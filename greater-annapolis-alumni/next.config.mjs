/** @type {import('next').NextConfig} */
const nextConfig = {
  eslint: {
    ignoreDuringBuilds: false,
  },
  images: {
    // No external image domains are configured yet. Once official chapter
    // photography is hosted (e.g. on a CDN), add its domain here.
    remotePatterns: [],
  },
};

export default nextConfig;
