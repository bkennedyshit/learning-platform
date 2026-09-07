import type { Metadata } from "next";
import Link from "next/link";
import { Analytics } from "@vercel/analytics/next";
import { SpeedInsights } from "@vercel/speed-insights/next";
import "katex/dist/katex.min.css";
import "./globals.css";
import { SITE_URL } from "../lib/site";

export const metadata: Metadata = {
  metadataBase: new URL(SITE_URL),
  title: {
    default: "NEPA Learning",
    template: "%s | NEPA Learning",
  },
  description: "Browse published learning lessons and resources.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>
        {children}
        <Link className="support-fab" href="/#support" aria-label="Support the open learning library">
          <span className="support-fab__mark" aria-hidden>$</span>
          <span>Tip jar</span>
        </Link>
        <Analytics />
        <SpeedInsights />
      </body>
    </html>
  );
}
