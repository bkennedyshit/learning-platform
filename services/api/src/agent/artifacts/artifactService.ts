import type { Artifact, ArtifactAuthor, ArtifactExport, ArtifactKind } from "@learning-platform/agent-contract";
import type { LearnerMemory } from "../memory/index.js";
import type { Clock, IdFactory } from "../support.js";
import { sanitizeMermaid, sanitizeSvg } from "./sanitizer.js";

export class ArtifactSanitizationError extends Error {
  readonly code = "artifact_unsafe";
  constructor(
    message: string,
    readonly violations: string[]
  ) {
    super(message);
    this.name = "ArtifactSanitizationError";
  }
}

/**
 * Deterministic 1x1 transparent PNG. Real rasterization requires a headless
 * renderer that is out of scope for deterministic tests; this placeholder is
 * always labeled `fallback: true`.
 */
const PNG_FALLBACK_DATA_URI =
  "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+M8AAAMBAQDJ/pLvAAAAAElFTkSuQmCC";

export interface CreateVisualInput {
  kind: ArtifactKind;
  title: string;
  description?: string;
  altText: string;
  source: string;
  lessonIds: string[];
  conceptIds: string[];
  createdBy: ArtifactAuthor;
  provider?: string;
}

export interface ReviseVisualInput {
  artifactId: string;
  source?: string;
  title?: string;
  altText?: string;
  description?: string;
  revisedBy: ArtifactAuthor;
}

function sanitizeForKind(kind: ArtifactKind, source: string): string {
  if (kind === "svg" || kind === "plot" || kind === "interactive") {
    const result = sanitizeSvg(source);
    if (!result.ok || result.sanitized === undefined) {
      throw new ArtifactSanitizationError("SVG failed sanitization", result.violations);
    }
    return result.sanitized;
  }
  if (kind === "mermaid") {
    const result = sanitizeMermaid(source);
    if (!result.ok || result.sanitized === undefined) {
      throw new ArtifactSanitizationError("Mermaid failed sanitization", result.violations);
    }
    return result.sanitized;
  }
  // Text-like artifacts (note/flashcard/study_plan/assessment) store as-is.
  return source;
}

function buildExports(kind: ArtifactKind, sanitizedSource: string): ArtifactExport[] {
  const exports: ArtifactExport[] = [
    { format: "png", dataUri: PNG_FALLBACK_DATA_URI, fallback: true }
  ];
  if (kind === "svg" || kind === "plot" || kind === "interactive") {
    exports.unshift({
      format: "svg",
      dataUri: `data:image/svg+xml;utf8,${encodeURIComponent(sanitizedSource)}`,
      fallback: false
    });
  }
  return exports;
}

export class ArtifactService {
  constructor(
    private readonly memory: LearnerMemory,
    private readonly clock: Clock,
    private readonly idFactory: IdFactory
  ) {}

  async create(input: CreateVisualInput): Promise<Artifact> {
    const sanitizedSource = sanitizeForKind(input.kind, input.source);
    const artifact: Artifact = {
      id: this.idFactory("artifact"),
      version: 1,
      kind: input.kind,
      title: input.title,
      description: input.description ?? "",
      altText: input.altText,
      source: input.source,
      sanitizedSource,
      lessonIds: input.lessonIds,
      conceptIds: input.conceptIds,
      createdBy: input.createdBy,
      ...(input.provider ? { provider: input.provider } : {}),
      createdAt: this.clock().toISOString(),
      exports: buildExports(input.kind, sanitizedSource)
    };
    await this.memory.saveArtifact(artifact);
    return artifact;
  }

  async revise(input: ReviseVisualInput): Promise<Artifact> {
    const existing = await this.memory.getArtifact(input.artifactId);
    if (!existing) {
      throw new Error(`Artifact ${input.artifactId} not found`);
    }
    const nextSource = input.source ?? existing.source;
    const sanitizedSource = sanitizeForKind(existing.kind, nextSource);
    const revised: Artifact = {
      ...existing,
      version: existing.version + 1,
      title: input.title ?? existing.title,
      altText: input.altText ?? existing.altText,
      description: input.description ?? existing.description,
      source: nextSource,
      sanitizedSource,
      createdBy: input.revisedBy,
      createdAt: this.clock().toISOString(),
      exports: buildExports(existing.kind, sanitizedSource)
    };
    await this.memory.saveArtifact(revised);
    return revised;
  }

  /** Read-only presentation view (sanitized source + export metadata). */
  async present(artifactId: string): Promise<Artifact> {
    const artifact = await this.memory.getArtifact(artifactId);
    if (!artifact) {
      throw new Error(`Artifact ${artifactId} not found`);
    }
    return artifact;
  }

  /** Persist/attach an artifact (e.g., to learner notes). */
  async save(artifact: Artifact): Promise<Artifact> {
    await this.memory.saveArtifact(artifact);
    return artifact;
  }

  exportArtifact(artifact: Artifact, format: "svg" | "png"): ArtifactExport {
    const found = artifact.exports?.find((e) => e.format === format);
    if (found) {
      return found;
    }
    if (format === "png") {
      return { format: "png", dataUri: PNG_FALLBACK_DATA_URI, fallback: true };
    }
    return {
      format: "svg",
      dataUri: `data:image/svg+xml;utf8,${encodeURIComponent(artifact.sanitizedSource)}`,
      fallback: false
    };
  }
}
