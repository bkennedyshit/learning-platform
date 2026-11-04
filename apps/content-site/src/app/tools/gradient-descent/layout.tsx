import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Gradient Descent Visualizer: Explore Optimization",
  description: "Explore gradient descent with an interactive loss landscape and see how optimization progresses toward a minimum.",
  alternates: { canonical: "/tools/gradient-descent" },
};

export default function GradientDescentLayout({ children }: { children: React.ReactNode }) {
  return children;
}
