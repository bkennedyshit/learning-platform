import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Calculus Visualizer: Functions, Derivatives & Tangent Lines",
  description: "Plot a function, explore its derivative and move a tangent line to connect calculus concepts with an interactive graph.",
  alternates: { canonical: "/tools/calculus" },
};

export default function CalculusLayout({ children }: { children: React.ReactNode }) {
  return children;
}
