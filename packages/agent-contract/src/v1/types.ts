import type { SchemaNode } from "./schema.js";

/** The contract version implemented by this module. */
export const CONTRACT_VERSION = "v1" as const;
export type ContractVersion = typeof CONTRACT_VERSION;

export const ACCOUNT_ROLES = [
  "b2c_learner",
  "student",
  "educator",
  "org_admin",
  "affiliate",
  "platform_admin"
] as const;
export type AccountRole = (typeof ACCOUNT_ROLES)[number];

export const TOOL_CATEGORIES = ["read", "state_change", "educator"] as const;
export type ToolCategory = (typeof TOOL_CATEGORIES)[number];

export interface Principal {
  accountId: string;
  role: AccountRole;
  organizationId?: string;
}

/* ------------------------------- Sessions ------------------------------- */

export const SESSION_STATUSES = ["active", "completed", "cancelled"] as const;
export type SessionStatus = (typeof SESSION_STATUSES)[number];

export interface AgentSession {
  id: string;
  accountId: string;
  role: AccountRole;
  status: SessionStatus;
  goalId?: string;
  lessonId?: string;
  summary?: string;
  createdAt: string;
  updatedAt: string;
}

export const TURN_AUTHORS = ["learner", "agent", "system", "educator"] as const;
export type TurnAuthor = (typeof TURN_AUTHORS)[number];

export interface Citation {
  lessonId: string;
  passageId?: string;
}

export interface ConversationTurn {
  id: string;
  sessionId: string;
  index: number;
  author: TurnAuthor;
  content: string;
  createdAt: string;
  artifactIds?: string[];
  citations?: Citation[];
}

/* -------------------------------- Tools --------------------------------- */

export interface ToolDefinition {
  name: string;
  category: ToolCategory;
  description: string;
  inputSchema: SchemaNode;
  outputSchema: SchemaNode;
  /** Minimum role required to invoke the tool. */
  requiredRole?: AccountRole;
  /** State-changing tools that are safe to retry with an idempotency key. */
  idempotent?: boolean;
}

export interface ToolCall {
  id: string;
  sessionId: string;
  toolName: string;
  input: unknown;
  idempotencyKey?: string;
  createdAt: string;
}

export interface ToolResult {
  callId: string;
  toolName: string;
  ok: boolean;
  output?: unknown;
  error?: StructuredError;
  startedAt: string;
  finishedAt: string;
}

/* -------------------------------- Plans --------------------------------- */

export const PLAN_STEP_STATUSES = ["pending", "active", "done", "skipped", "failed"] as const;
export type PlanStepStatus = (typeof PLAN_STEP_STATUSES)[number];

export interface PlanStep {
  id: string;
  description: string;
  status: PlanStepStatus;
  toolName?: string;
}

export interface Plan {
  id: string;
  sessionId: string;
  goal: string;
  revision: number;
  steps: PlanStep[];
  createdAt: string;
}

/* --------------------------------- Jobs --------------------------------- */

export const JOB_STATUSES = ["queued", "running", "succeeded", "failed", "cancelled"] as const;
export type JobStatus = (typeof JOB_STATUSES)[number];

export interface Job {
  id: string;
  sessionId: string;
  kind: string;
  status: JobStatus;
  progress: number;
  createdAt: string;
  updatedAt: string;
  resultArtifactIds?: string[];
  error?: StructuredError;
}

export interface JobProgressEvent {
  jobId: string;
  progress: number;
  message?: string;
  at: string;
}

/* ------------------------------- Artifacts ------------------------------ */

export const ARTIFACT_KINDS = [
  "svg",
  "mermaid",
  "plot",
  "interactive",
  "note",
  "flashcard",
  "study_plan",
  "assessment"
] as const;
export type ArtifactKind = (typeof ARTIFACT_KINDS)[number];

export const ARTIFACT_AUTHORS = ["learner", "educator", "agent"] as const;
export type ArtifactAuthor = (typeof ARTIFACT_AUTHORS)[number];

export const ARTIFACT_EXPORT_FORMATS = ["svg", "png"] as const;
export type ArtifactExportFormat = (typeof ARTIFACT_EXPORT_FORMATS)[number];

export interface ArtifactExport {
  format: ArtifactExportFormat;
  dataUri: string;
  /** True when the export is a deterministic placeholder rather than a real render. */
  fallback: boolean;
}

export interface Artifact {
  id: string;
  version: number;
  kind: ArtifactKind;
  title: string;
  description: string;
  altText: string;
  source: string;
  sanitizedSource: string;
  lessonIds: string[];
  conceptIds: string[];
  createdBy: ArtifactAuthor;
  provider?: string;
  createdAt: string;
  exports?: ArtifactExport[];
}

/* ------------------------------- Approvals ------------------------------ */

export const APPROVAL_ACTIONS = [
  "publish",
  "share",
  "contact_educator",
  "change_goal",
  "submit_graded"
] as const;
export type ApprovalAction = (typeof APPROVAL_ACTIONS)[number];

export const APPROVAL_STATUSES = ["draft", "pending", "approved", "rejected"] as const;
export type ApprovalStatus = (typeof APPROVAL_STATUSES)[number];

export interface ApprovalRequest {
  id: string;
  action: ApprovalAction;
  status: ApprovalStatus;
  artifactId: string;
  requestedBy: string;
  version: number;
  createdAt: string;
  sessionId?: string;
  decidedBy?: string;
  decidedAt?: string;
  reason?: string;
  provenance?: Record<string, unknown>;
}

/* --------------------------------- Errors ------------------------------- */

export interface StructuredError {
  code: string;
  message: string;
  retryable: boolean;
  details?: Record<string, unknown>;
}

/* --------------------------------- Traces ------------------------------- */

export const TRACE_EVENT_TYPES = [
  "plan_created",
  "plan_revised",
  "tool_call",
  "tool_result",
  "observation",
  "decision",
  "approval",
  "job_progress",
  "memory_update",
  "error"
] as const;
export type TraceEventType = (typeof TRACE_EVENT_TYPES)[number];

/**
 * Trace events record observable decisions, evidence, and tool activity.
 * They deliberately contain no hidden model reasoning / chain-of-thought field.
 */
export interface TraceEvent {
  id: string;
  sessionId: string;
  seq: number;
  type: TraceEventType;
  at: string;
  summary: string;
  data?: Record<string, unknown>;
}
