import type { NextConfig } from "next";
import path from "node:path";
import { SITE_URL } from "./src/lib/site";

const nextConfig: NextConfig = {
  async redirects() {
    return [
      // C# and C++ previously collided on /subject/c (only C# was reachable).
      { source: "/subject/c", destination: "/subject/c-sharp", permanent: true },
      {
        source: "/:path*",
        has: [{ type: "host", value: "learning-platform-content-site\\.vercel\\.app" }],
        destination: `${SITE_URL}/:path*`,
        permanent: true,
      },
    ];
  },
  turbopack: {
    root: path.join(__dirname, "../.."),
  },
};

export default nextConfig;
