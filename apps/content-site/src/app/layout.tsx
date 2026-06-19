import type { Metadata } from "next";
import Link from "next/link";
import "katex/dist/katex.min.css";
import "./globals.css";

export const metadata: Metadata = {
  title: "Learning Platform Content Site",
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
      </body>
    </html>
  );
}
