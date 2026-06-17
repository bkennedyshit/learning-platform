"use client";

import React, { ReactNode } from "react";
import styles from "./Shell.module.css";
import TutorPanel, { type TutorContext } from "./TutorPanel";
import PathNavigation, { type PathNavData } from "./PathNavigation";

interface ShellProps {
  children: ReactNode;
  currentStepName: string;
  nextStepName: string;
  nav?: PathNavData;
  tutorContext?: TutorContext;
}

export default function Shell({ children, currentStepName, nextStepName, nav, tutorContext }: ShellProps) {
  return (
    <div className={styles.shell}>
      <aside className={styles.sidebar}>
        <PathNavigation nav={nav} />
      </aside>

      <main className={styles.mainContent}>
        <header className={styles.topBar}>
          <div className={styles.progressIndicator}>
            <span className={styles.currentStep}>Currently: {currentStepName}</span>
            <span className={styles.nextStep}>Up next: {nextStepName}</span>
          </div>
          <div>
            {/* User profile / Glossary trigger can go here */}
          </div>
        </header>
        
        <div className={styles.actionArea}>
          {children}
        </div>
      </main>

      <aside className={styles.tutorPanelContainer}>
        <TutorPanel context={tutorContext} />
      </aside>
    </div>
  );
}
