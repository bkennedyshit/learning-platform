"use client";

import React from "react";
import Link from "next/link";
import styles from "./PathNavigation.module.css";

export interface PathNavData {
  currentSubject: { name: string; slug: string; progress: number };
  upNext: { slug: string; title: string; subjectSlug: string }[];
  catalogs: { href: string; name: string }[];
}

export default function PathNavigation({ nav }: { nav?: PathNavData }) {
  const currentSubject = nav?.currentSubject ?? { name: "Browse the catalog", slug: "", progress: 0 };
  const upNext = nav?.upNext ?? [];
  const catalogs = nav?.catalogs ?? [
    { href: "/learn?catalog=k12", name: "K-12 Catalog" },
    { href: "/learn?catalog=advanced", name: "Advanced Track" },
  ];

  return (
    <nav className={styles.nav}>
      <Link href="/" className={styles.brand} style={{ textDecoration: "none", color: "inherit" }}>
        <svg className={styles.brandIcon} width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
          <polygon points="12 2 2 7 12 12 22 7 12 2" />
          <polyline points="2 17 12 22 22 17" />
          <polyline points="2 12 12 17 22 12" />
        </svg>
        Aura
      </Link>

      <div className={styles.section}>
        <div className={styles.sectionTitle}>Current Path</div>
        <Link
          href={currentSubject.slug ? `/learn/${currentSubject.slug}` : "/learn"}
          className={`${styles.pathItem} ${styles.active}`}
          style={{ textDecoration: "none", color: "inherit" }}
        >
          <svg className={styles.icon} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="m9 18 6-6-6-6" />
          </svg>
          <div>
            <div>{currentSubject.name}</div>
            <div className={styles.progressBar}>
              <div className={styles.progressFill} style={{ width: `${currentSubject.progress}%` }} />
            </div>
          </div>
        </Link>
      </div>

      {upNext.length > 0 && (
        <div className={styles.section}>
          <div className={styles.sectionTitle}>Up Next in Path</div>
          {upNext.map((item) => (
            <Link
              key={item.slug}
              href={`/learn/${item.subjectSlug}/${item.slug}`}
              className={styles.pathItem}
              style={{ textDecoration: "none", color: "inherit" }}
            >
              <svg className={styles.icon} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <rect width="18" height="18" x="3" y="3" rx="2" ry="2" />
                <path d="M3 9h18" />
                <path d="M9 21V9" />
              </svg>
              {item.title}
            </Link>
          ))}
        </div>
      )}

      <div className={styles.section}>
        <div className={styles.sectionTitle}>Explore Catalogs</div>
        {catalogs.map((c) => (
          <Link key={c.href} href={c.href} className={styles.pathItem} style={{ textDecoration: "none", color: "inherit" }}>
            {c.name}
          </Link>
        ))}
        <Link href="/tools" className={styles.pathItem} style={{ textDecoration: "none", color: "inherit" }}>
          🧮 Tools &amp; Calculators
        </Link>
      </div>
    </nav>
  );
}
