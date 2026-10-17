import type { NextConfig } from "next";
import path from "node:path";

const nextConfig: NextConfig = {
  async redirects() {
    return [
      // C# and C++ previously collided on /subject/c (only C# was reachable).
      { source: "/subject/c", destination: "/subject/c-sharp", permanent: true },
    ];
  },
  turbopack: {
    root: path.join(__dirname, "../.."),
  },
};

export default nextConfig;
