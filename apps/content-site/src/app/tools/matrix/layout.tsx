import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Matrix Calculator: Operations, Determinants & Inverses",
  description: "Calculate matrix sums, products, transposes, determinants and inverses with the interactive Matrix Commander tool.",
  alternates: { canonical: "/tools/matrix" },
};

export default function MatrixLayout({ children }: { children: React.ReactNode }) {
  return children;
}
