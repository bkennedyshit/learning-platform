import type { Metadata } from "next";
import Link from "next/link";

export const metadata: Metadata = {
  title: "Learning Resources",
  description: "Practical guides for building a reliable, accessible learning setup.",
  alternates: { canonical: "/resources" },
};

export default function ResourcesPage() {
  return (
    <main style={{ maxWidth: 900, margin: "0 auto", padding: "3rem 1.25rem 5rem" }}>
      <Link href="/">← Browse lessons</Link>
      <header style={{ margin: "2rem 0" }}>
        <p style={{ color: "#315bd6", fontWeight: 800, letterSpacing: ".08em", textTransform: "uppercase" }}>Practical resources</p>
        <h1>Build a learning setup that keeps working</h1>
        <p>Focused guides for the technology around the lesson: connectivity, devices, study workflows, and access.</p>
      </header>
      <article style={{ padding: "1.5rem", border: "1px solid #d9deea", borderRadius: 16 }}>
        <h2><Link href="/resources/mobile-connectivity-for-students-and-remote-learning">Mobile Connectivity for Students and Remote Learning</Link></h2>
        <p>How to measure the workload, compare hotspot terms, plan offline study, and avoid paying for capacity the student does not need.</p>
      </article>
    </main>
  );
}
