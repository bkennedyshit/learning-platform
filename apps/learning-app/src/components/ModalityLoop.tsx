"use client";

import React, { useState, useEffect, useRef } from "react";
import styles from "./ModalityLoop.module.css";

type Stage = "Read" | "Listen" | "Write" | "Code" | "Handwrite";

export interface ModalityLoopProps {
  title: string;
  htmlContent: string;
  textContent: string;
  isProgramming: boolean;
  writePrompt?: string;
  codePrompt?: string;
  onComplete?: () => void;
}

export default function ModalityLoop({
  title,
  htmlContent,
  textContent,
  isProgramming,
  writePrompt = "Summarize the key idea of this lesson in your own words.",
  codePrompt = "Write a short snippet that demonstrates a concept from this lesson.",
  onComplete,
}: ModalityLoopProps) {
  const [stage, setStage] = useState<Stage>("Read");
  const [activeWordIndex, setActiveWordIndex] = useState(-1);
  const readRef = useRef<HTMLDivElement>(null);

  // Render any mermaid diagrams in the Read stage content.
  useEffect(() => {
    if (stage !== "Read") return;
    const el = readRef.current;
    if (!el) return;
    const blocks = Array.from(
      el.querySelectorAll<HTMLElement>('pre.mermaid:not([data-processed="true"])')
    );
    if (blocks.length === 0) return;
    let cancelled = false;
    (async () => {
      try {
        const mermaid = (await import("mermaid")).default;
        mermaid.initialize({ startOnLoad: false, theme: "dark", securityLevel: "loose" });
        if (cancelled) return;
        await mermaid.run({ nodes: blocks });
      } catch {
        /* leave source on failure */
      }
    })();
    return () => {
      cancelled = true;
    };
  }, [stage, htmlContent]);

  // First ~120 words drive the Listen highlight (full lesson can be long).
  const words = textContent.split(/\s+/).filter(Boolean).slice(0, 120);

  useEffect(() => {
    if (stage === "Listen") {
      let current = 0;
      const interval = setInterval(() => {
        setActiveWordIndex(current);
        current++;
        if (current >= words.length) {
          clearInterval(interval);
          setActiveWordIndex(-1);
        }
      }, 220);
      return () => clearInterval(interval);
    }
  }, [stage]); // eslint-disable-line react-hooks/exhaustive-deps

  const advance = () => {
    switch (stage) {
      case "Read":
        setStage("Listen");
        break;
      case "Listen":
        setStage("Write");
        break;
      case "Write":
        setStage(isProgramming ? "Code" : "Handwrite");
        break;
      case "Code":
        setStage("Handwrite");
        break;
      case "Handwrite":
        onComplete?.();
        break;
    }
  };

  return (
    <div className={styles.container}>
      <h1 className={styles.lessonTitle}>{title}</h1>

      {stage === "Read" && (
        <div
          ref={readRef}
          className={`${styles.lessonBody} lesson-content`}
          dangerouslySetInnerHTML={{ __html: htmlContent }}
        />
      )}

      {stage === "Listen" && (
        <div className={styles.lessonBody}>
          <p>
            {words.map((w, i) => (
              <span key={i} className={`${styles.listenWord} ${i === activeWordIndex ? styles.active : ""}`}>
                {w}{" "}
              </span>
            ))}
          </p>
        </div>
      )}

      {stage === "Write" && (
        <div className={styles.writeArea}>
          <div className={styles.problemPrompt}>{writePrompt}</div>
          <textarea className={styles.textarea} placeholder="Type your step-by-step solution here..." />
        </div>
      )}

      {stage === "Code" && (
        <div className={styles.writeArea}>
          <div className={styles.problemPrompt}>{codePrompt}</div>
          <textarea className={styles.codeArea} placeholder="// write your code here" spellCheck={false} />
        </div>
      )}

      {stage === "Handwrite" && (
        <div className={styles.writeArea}>
          <div className={styles.handwriteInstructions}>
            <svg className={styles.handwriteIcon} width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M12 20h9" />
              <path d="M16.5 3.5a2.12 2.12 0 0 1 3 3L7 19l-4 1 1-4Z" />
            </svg>
            <h2>Retention Step</h2>
            <p style={{ marginTop: "1rem", color: "var(--text-secondary)" }}>
              Take out a physical notebook and handwrite the core concepts of this lesson.
              Writing by hand improves long-term retention.
            </p>
          </div>
        </div>
      )}

      <div className={styles.controls}>
        <button className={styles.primaryButton} onClick={advance}>
          {stage === "Handwrite" ? "Complete Lesson" : "Continue to Next Step"}
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M5 12h14" />
            <path d="m12 5 7 7-7 7" />
          </svg>
        </button>
      </div>
    </div>
  );
}
