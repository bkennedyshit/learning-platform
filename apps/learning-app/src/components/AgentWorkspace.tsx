"use client";

import React, { useMemo, useRef, useState } from "react";
import type { Artifact, ConversationTurn } from "@learning-platform/agent-contract";
import styles from "./AgentWorkspace.module.css";
import SafeSvg from "./SafeSvg";
import SafeMermaid from "./SafeMermaid";
import { renderSvgToPng, downloadDataUri } from "../lib/pngExport";
import {
  AGENT_BASE,
  createOrResumeSession,
  ensureDevSession,
  normalizeTurnResponse,
  sendTurn,
  type TurnView
} from "../lib/agentClient";

export interface AgentContext {
  title: string;
  text: string;
  lessonId?: string;
}

const EMPTY_VIEW: TurnView = {
  turns: [],
  toolSummaries: [],
  citations: [],
  artifacts: [],
  whyNext: ""
};

export default function AgentWorkspace({ context }: { context?: AgentContext }): React.JSX.Element {
  const [sessionId, setSessionId] = useState<string | undefined>();
  const [goal, setGoal] = useState("");
  const [committedGoal, setCommittedGoal] = useState("");
  const [view, setView] = useState<TurnView>(EMPTY_VIEW);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [lastMessage, setLastMessage] = useState<string | null>(null);
  const [modal, setModal] = useState<Artifact | null>(null);
  const abortRef = useRef<AbortController | null>(null);

  const artifactsById = useMemo(() => {
    const map = new Map<string, Artifact>();
    for (const a of view.artifacts) map.set(a.id, a);
    return map;
  }, [view.artifacts]);

  async function ensureSession(): Promise<string | undefined> {
    if (sessionId) return sessionId;
    const payload = {
      ...(context?.lessonId ? { lessonId: context.lessonId } : {}),
      ...(committedGoal ? { goal: { description: committedGoal } } : {})
    };
    let created = await createOrResumeSession(payload);
    if (!created.ok && created.status === 401) {
      // Local dev convenience: bootstrap a dev session when enabled server-side.
      await ensureDevSession({});
      created = await createOrResumeSession(payload);
    }
    if (!created.ok || !created.data) {
      setError(created.error ?? "Could not start a learning session.");
      return undefined;
    }
    setSessionId(created.data.session.id);
    return created.data.session.id;
  }

  async function submit(message: string) {
    if (!message.trim() || loading) return;
    setLoading(true);
    setError(null);
    setLastMessage(message);
    // Abort any in-flight turn and start a fresh controller for this one.
    abortRef.current?.abort();
    const controller = new AbortController();
    abortRef.current = controller;

    const sid = await ensureSession();
    if (!sid) {
      setLoading(false);
      return;
    }
    if (controller.signal.aborted) return;
    const res = await sendTurn(
      sid,
      {
        message,
        ...(context?.lessonId ? { lessonId: context.lessonId } : {})
      },
      controller.signal
    );
    // A superseded/cancelled request must never overwrite current UI state.
    if (controller.signal.aborted || abortRef.current !== controller) {
      return;
    }
    abortRef.current = null;
    if (res.aborted) {
      return;
    }
    if (!res.ok || !res.data) {
      setError(res.error ?? "The tutor could not respond.");
      setLoading(false);
      return;
    }
    setView(normalizeTurnResponse(res.data));
    setInput("");
    setLoading(false);
  }

  function cancel() {
    abortRef.current?.abort();
    abortRef.current = null;
    setLoading(false);
    setError("Cancelled.");
  }

  function commitGoal() {
    if (!goal.trim()) return;
    if (committedGoal && !window.confirm(`Change your goal from "${committedGoal}" to "${goal}"?`)) {
      return;
    }
    setCommittedGoal(goal.trim());
    // A goal change starts a fresh durable session on the next turn.
    setSessionId(undefined);
  }

  async function callTool(name: string, toolInput: unknown): Promise<void> {
    const sid = await ensureSession();
    if (!sid) return;
    await fetch(`${AGENT_BASE}/v1/tools/${name}`, {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({ sessionId: sid, input: toolInput })
    });
  }

  async function reviseArtifact(a: Artifact): Promise<void> {
    const next = window.prompt("Describe the revision (new source for this visual):", a.source);
    if (next == null) return;
    const sid = await ensureSession();
    if (!sid) return;
    const res = await fetch(`${AGENT_BASE}/v1/tools/visual.revise`, {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({ sessionId: sid, input: { artifactId: a.id, source: next } })
    });
    const data = (await res.json().catch(() => null)) as { result?: { ok?: boolean; output?: Artifact } } | null;
    const revised = data?.result?.output;
    if (data?.result?.ok && revised) {
      setView((v) => ({ ...v, artifacts: v.artifacts.map((x) => (x.id === a.id ? revised : x)) }));
    } else {
      setError("Could not revise the visual.");
    }
  }

  return (
    <section className={styles.workspace} aria-label="Learning agent workspace">
      <header className={styles.header}>
        <span className={styles.title}>Learning Agent</span>
        {context?.title && <span className={styles.context}>Lesson: {context.title}</span>}
      </header>

      <div className={styles.goalRow}>
        <input
          className={styles.goalInput}
          value={goal}
          onChange={(e) => setGoal(e.target.value)}
          placeholder="Your learning goal (optional)"
          aria-label="Learning goal"
        />
        <button className={styles.secondaryButton} onClick={commitGoal} disabled={!goal.trim()}>
          {committedGoal ? "Update goal" : "Set goal"}
        </button>
      </div>
      {committedGoal && (
        <div className={styles.goalBadge} data-testid="committed-goal">
          Goal: {committedGoal}
        </div>
      )}

      {view.plan && view.plan.steps.length > 0 && (
        <div className={styles.plan} data-testid="plan">
          <div className={styles.planHeading}>Plan</div>
          <ol className={styles.planSteps}>
            {view.plan.steps.map((step) => (
              <li
                key={step.id}
                className={`${styles.planStep} ${step.id === view.currentStep?.id ? styles.planStepCurrent : ""}`}
                data-status={step.status}
              >
                {step.description}
              </li>
            ))}
          </ol>
        </div>
      )}

      <div className={styles.conversation} data-testid="conversation">
        {view.turns.length === 0 && !loading && (
          <p className={styles.placeholder}>
            Ask about this lesson or set a goal. Reading works even if the agent is offline.
          </p>
        )}
        {view.turns.map((turn) => (
          <TurnBubble key={turn.id} turn={turn} artifactsById={artifactsById} onExpand={setModal} onSave={(a) => callTool("artifact.save", { artifactId: a.id })} onRevise={reviseArtifact} />
        ))}
        {loading && <div className={`${styles.bubble} ${styles.agent}`}>Thinking…</div>}
      </div>

      {view.toolSummaries.length > 0 && (
        <div className={styles.toolActivity} data-testid="tool-activity">
          <div className={styles.subHeading}>What I did</div>
          <ul>
            {view.toolSummaries.map((t, i) => (
              <li key={i} className={t.ok ? styles.toolOk : styles.toolFail}>
                {t.summary}
              </li>
            ))}
          </ul>
        </div>
      )}

      {view.whyNext && (
        <div className={styles.whyNext} data-testid="why-next">
          <strong>Why this next?</strong> {view.whyNext}
        </div>
      )}

      {view.citations.length > 0 && (
        <div className={styles.citations} data-testid="citations">
          Grounded in: {view.citations.map((c) => c.passageId ?? c.lessonId).join(", ")}
        </div>
      )}

      {error && (
        <div className={styles.error} role="alert" data-testid="error">
          <span>{error}</span>
          {lastMessage && (
            <button className={styles.secondaryButton} onClick={() => submit(lastMessage)}>
              Retry
            </button>
          )}
        </div>
      )}

      <div className={styles.inputArea}>
        <input
          className={styles.input}
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && submit(input)}
          placeholder="Ask the tutor about this lesson..."
          disabled={loading}
          aria-label="Message the tutor"
        />
        {loading ? (
          <button className={styles.secondaryButton} onClick={cancel}>
            Cancel
          </button>
        ) : (
          <button className={styles.primaryButton} onClick={() => submit(input)} disabled={!input.trim()}>
            Send
          </button>
        )}
      </div>

      {modal && (
        <div className={styles.modalOverlay} role="dialog" aria-modal="true" onClick={() => setModal(null)}>
          <div className={styles.modalCard} onClick={(e) => e.stopPropagation()}>
            <div className={styles.modalHeader}>
              <span>{modal.title}</span>
              <button className={styles.secondaryButton} onClick={() => setModal(null)}>
                Close
              </button>
            </div>
            <ArtifactBody artifact={modal} large />
          </div>
        </div>
      )}
    </section>
  );
}

function TurnBubble({
  turn,
  artifactsById,
  onExpand,
  onSave,
  onRevise
}: {
  turn: ConversationTurn;
  artifactsById: Map<string, Artifact>;
  onExpand: (a: Artifact) => void;
  onSave: (a: Artifact) => void;
  onRevise: (a: Artifact) => void;
}): React.JSX.Element {
  const artifacts = (turn.artifactIds ?? [])
    .map((id) => artifactsById.get(id))
    .filter((a): a is Artifact => a !== undefined);
  return (
    <div className={`${styles.bubble} ${turn.author === "learner" ? styles.learner : styles.agent}`}>
      <div>{turn.content}</div>
      {artifacts.map((a) => (
        <ArtifactCard key={a.id} artifact={a} onExpand={onExpand} onSave={onSave} onRevise={onRevise} />
      ))}
    </div>
  );
}

function ArtifactCard({
  artifact,
  onExpand,
  onSave,
  onRevise
}: {
  artifact: Artifact;
  onExpand: (a: Artifact) => void;
  onSave: (a: Artifact) => void;
  onRevise: (a: Artifact) => void;
}): React.JSX.Element {
  const [pngNote, setPngNote] = useState<string | null>(null);
  const svgExport = artifact.exports?.find((e) => e.format === "svg");
  const serverPng = artifact.exports?.find((e) => e.format === "png");
  const revisable = artifact.kind === "svg" || artifact.kind === "mermaid" || artifact.kind === "plot";
  const rasterizable =
    artifact.kind === "svg" || artifact.kind === "plot" || artifact.kind === "interactive";

  async function handlePng(): Promise<void> {
    setPngNote(null);
    if (rasterizable) {
      // Real client-side rasterization: re-check the sanitized SVG and render it
      // to a bounded canvas, then download the produced PNG.
      const result = await renderSvgToPng(artifact.sanitizedSource);
      if (result.ok && result.dataUri) {
        downloadDataUri(result.dataUri, `${artifact.id}.png`);
        return;
      }
    }
    // Rendering unavailable/failed → offer the explicitly labeled fallback.
    if (serverPng) {
      downloadDataUri(serverPng.dataUri, `${artifact.id}-placeholder.png`);
      setPngNote("PNG rendering was unavailable; downloaded a labeled placeholder instead.");
    } else {
      setPngNote("PNG export is not available for this artifact.");
    }
  }

  return (
    <div className={styles.artifactCard} data-testid="artifact-card">
      <div className={styles.artifactTitle}>{artifact.title}</div>
      <ArtifactBody artifact={artifact} />
      <div className={styles.artifactActions}>
        <button className={styles.linkButton} onClick={() => onExpand(artifact)}>
          Expand
        </button>
        <button className={styles.linkButton} onClick={() => onSave(artifact)}>
          Save
        </button>
        {revisable && (
          <button className={styles.linkButton} onClick={() => onRevise(artifact)}>
            Revise
          </button>
        )}
        {svgExport && (
          <a className={styles.linkButton} href={svgExport.dataUri} download={`${artifact.id}.svg`}>
            SVG
          </a>
        )}
        {(rasterizable || serverPng) && (
          <button className={styles.linkButton} onClick={handlePng} data-testid="png-export">
            PNG
          </button>
        )}
      </div>
      {pngNote && (
        <p className={styles.artifactText} role="status" data-testid="png-note">
          {pngNote}
        </p>
      )}
    </div>
  );
}

function ArtifactBody({ artifact, large }: { artifact: Artifact; large?: boolean }): React.JSX.Element {
  const className = large ? styles.artifactLarge : styles.artifactVisual;
  if (artifact.kind === "svg" || artifact.kind === "plot" || artifact.kind === "interactive") {
    return <SafeSvg source={artifact.sanitizedSource} altText={artifact.altText} className={className} />;
  }
  if (artifact.kind === "mermaid") {
    return <SafeMermaid source={artifact.sanitizedSource} altText={artifact.altText} className={className} />;
  }
  if (artifact.kind === "flashcard") {
    let cards: Array<{ front: string; back: string }> = [];
    try {
      cards = (JSON.parse(artifact.source) as { cards?: Array<{ front: string; back: string }> }).cards ?? [];
    } catch {
      /* ignore */
    }
    return (
      <ul className={styles.flashcards}>
        {cards.map((c, i) => (
          <li key={i}>
            <strong>{c.front}</strong> — {c.back}
          </li>
        ))}
      </ul>
    );
  }
  return <p className={styles.artifactText}>{artifact.source}</p>;
}
