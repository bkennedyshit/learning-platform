import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Probability Calculator: Normal, Binomial & Poisson Distributions",
  description: "Explore normal, binomial and Poisson distributions with interactive plots and statistics in Probability Studio.",
  alternates: { canonical: "/tools/probability" },
};

export default function ProbabilityLayout({ children }: { children: React.ReactNode }) {
  return children;
}
