"use client";

import React from "react";
import { useRouter } from "next/navigation";
import Shell from "../../../../components/Shell";
import ModalityLoop from "../../../../components/ModalityLoop";
import type { PathNavData } from "../../../../components/PathNavigation";

interface Props {
  title: string;
  htmlContent: string;
  textContent: string;
  isProgramming: boolean;
  nextHref: string;
  nextStepName: string;
  nav: PathNavData;
  lessonId?: string;
}

export default function LessonClient({
  title,
  htmlContent,
  textContent,
  isProgramming,
  nextHref,
  nextStepName,
  nav,
  lessonId,
}: Props) {
  const router = useRouter();

  return (
    <Shell
      currentStepName={title}
      nextStepName={nextStepName}
      nav={nav}
      tutorContext={{ title, text: textContent, ...(lessonId ? { lessonId } : {}) }}
    >
      <ModalityLoop
        title={title}
        htmlContent={htmlContent}
        textContent={textContent}
        isProgramming={isProgramming}
        onComplete={() => router.push(nextHref)}
      />
    </Shell>
  );
}
