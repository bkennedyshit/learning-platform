import type { NextConfig } from "next";
import path from "node:path";

const nextConfig: NextConfig = {
  turbopack: {
    root: path.join(__dirname, "../.."),
  },
  async redirects() {
    return [
      {
        source: "/415-past-tenses-passé-composé-imparfait-plus-que-parfait",
        destination: "/415-past-tenses-passe-compose-imparfait-plus-que-parfait",
        permanent: true,
      },
      {
        source: "/308-from-electronics-to-robotics-i²c-spi-uart-can-sensors-actuators",
        destination: "/308-from-electronics-to-robotics-i2c-spi-uart-can-sensors-actuators",
        permanent: true,
      },
      {
        source: "/225-serial-verbs-把-被-resultative-complements",
        destination: "/225-serial-verbs-resultative-complements",
        permanent: true,
      },
      {
        source: "/37.3---Kanji-—-System-Overview-&-First-100-\\(JLPT-N5\\)",
        destination: "/373-kanji-system-overview-first-100-jlpt-n5",
        permanent: true,
      },
    ];
  },
};

export default nextConfig;
