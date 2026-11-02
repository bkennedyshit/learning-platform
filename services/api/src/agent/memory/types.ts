import type {
  AgentSession,
  ApprovalRequest,
  Artifact,
  ConversationTurn,
  Plan,
  TraceEvent
} from "@learning-platform/agent-contract";

/** Durable, domain-shaped learner memory. Never stores hidden model reasoning. */

export interface Goal {
  id: string;
  accountId: string;
  description: string;
  targetConceptIds: string[];
  status: "active" | "achieved" | "abandoned";
  createdAt: string;
  updatedAt: string;
}

export interface ConceptMastery {
  accountId: string;
  conceptId: string;
  /** 0..1 estimated mastery. */
  mastery: number;
  /** 0..1 confidence in the estimate. */
  confidence: number;
  updatedAt: string;
}

export interface Attempt {
  id: string;
  accountId: string;
  conceptId: string;
  lessonId?: string;
  prompt: string;
  response: string;
  correct: boolean;
  score: number;
  at: string;
}

export interface Misconception {
  id: string;
  accountId: string;
  conceptId: string;
  description: string;
  /** References to Attempt.id values that evidence the misconception. */
  evidenceAttemptIds: string[];
  status: "open" | "resolved";
  createdAt: string;
  updatedAt: string;
}

export type ModalityStage = "read" | "listen" | "write" | "code" | "handwrite";

export interface StageRecord {
  accountId: string;
  lessonId: string;
  stage: ModalityStage;
  completedAt: string;
}

export interface ReviewRecord {
  accountId: string;
  conceptId: string;
  lessonId?: string;
  dueAt: string;
  intervalDays: number;
  lastScore: number;
  lastReviewedAt?: string;
  history: Array<{ at: string; score: number }>;
}

export interface LearnerPreferences {
  accountId: string;
  explanationDepth: "brief" | "standard" | "deep";
  preferredModality: ModalityStage;
  accommodations: string[];
  updatedAt: string;
}

export interface SessionSummary {
  sessionId: string;
  accountId: string;
  summary: string;
  sourceLessonIds: string[];
  updatedAt: string;
}

/**
 * The complete serializable memory snapshot. This is exactly what the durable
 * file store reads and writes.
 */
export interface MemoryState {
  version: 1;
  goals: Record<string, Goal>;
  mastery: Record<string, ConceptMastery>; // key: `${accountId}:${conceptId}`
  attempts: Record<string, Attempt>;
  misconceptions: Record<string, Misconception>;
  stages: StageRecord[];
  reviews: Record<string, ReviewRecord>; // key: `${accountId}:${conceptId}`
  preferences: Record<string, LearnerPreferences>; // key: accountId
  sessions: Record<string, AgentSession>;
  turns: ConversationTurn[];
  plans: Record<string, Plan>;
  traces: TraceEvent[];
  approvals: Record<string, ApprovalRequest>;
  artifacts: Record<string, Artifact>;
  summaries: Record<string, SessionSummary>; // key: sessionId
}

export function emptyMemoryState(): MemoryState {
  return {
    version: 1,
    goals: {},
    mastery: {},
    attempts: {},
    misconceptions: {},
    stages: [],
    reviews: {},
    preferences: {},
    sessions: {},
    turns: [],
    plans: {},
    traces: [],
    approvals: {},
    artifacts: {},
    summaries: {}
  };
}

export interface LearnerMemory {
  // goals
  upsertGoal(goal: Goal): Promise<Goal>;
  getActiveGoals(accountId: string): Promise<Goal[]>;

  // mastery
  setMastery(record: ConceptMastery): Promise<void>;
  getMastery(accountId: string, conceptId: string): Promise<ConceptMastery | undefined>;
  listMastery(accountId: string): Promise<ConceptMastery[]>;

  // attempts + misconceptions
  recordAttempt(attempt: Attempt): Promise<void>;
  upsertMisconception(m: Misconception): Promise<Misconception>;
  getOpenMisconceptions(accountId: string): Promise<Misconception[]>;
  getAttempt(id: string): Promise<Attempt | undefined>;

  // stages
  recordStage(record: StageRecord): Promise<void>;
  getCompletedStages(accountId: string, lessonId: string): Promise<ModalityStage[]>;

  // reviews
  upsertReview(record: ReviewRecord): Promise<void>;
  getDueReviews(accountId: string, now: Date): Promise<ReviewRecord[]>;

  // preferences
  setPreferences(prefs: LearnerPreferences): Promise<void>;
  getPreferences(accountId: string): Promise<LearnerPreferences | undefined>;

  // agent runtime records
  saveSession(session: AgentSession): Promise<void>;
  getSession(id: string): Promise<AgentSession | undefined>;
  appendTurn(turn: ConversationTurn): Promise<void>;
  getTurns(sessionId: string): Promise<ConversationTurn[]>;
  savePlan(plan: Plan): Promise<void>;
  getPlan(id: string): Promise<Plan | undefined>;
  appendTrace(event: TraceEvent): Promise<void>;
  getTraces(sessionId: string): Promise<TraceEvent[]>;
  saveApproval(request: ApprovalRequest): Promise<void>;
  getApproval(id: string): Promise<ApprovalRequest | undefined>;
  listApprovals(artifactId: string): Promise<ApprovalRequest[]>;
  saveArtifact(artifact: Artifact): Promise<void>;
  getArtifact(id: string): Promise<Artifact | undefined>;
  setSessionSummary(summary: SessionSummary): Promise<void>;
  getSessionSummary(sessionId: string): Promise<SessionSummary | undefined>;
}
