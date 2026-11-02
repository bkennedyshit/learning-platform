import {
  emptyMemoryState,
  type Attempt,
  type ConceptMastery,
  type Goal,
  type LearnerMemory,
  type LearnerPreferences,
  type MemoryState,
  type Misconception,
  type ModalityStage,
  type ReviewRecord,
  type SessionSummary,
  type StageRecord
} from "./types.js";
import type {
  AgentSession,
  ApprovalRequest,
  Artifact,
  ConversationTurn,
  Plan,
  TraceEvent
} from "@learning-platform/agent-contract";

const masteryKey = (accountId: string, conceptId: string): string => `${accountId}:${conceptId}`;
const clone = <T>(value: T): T => JSON.parse(JSON.stringify(value)) as T;

/**
 * In-memory learner memory. Also serves as the shared core for durable stores:
 * subclasses override {@link flush} to persist {@link state} after each write.
 */
export class InMemoryLearnerMemory implements LearnerMemory {
  protected state: MemoryState;

  constructor(state: MemoryState = emptyMemoryState()) {
    this.state = state;
  }

  /** Persistence hook. No-op for the pure in-memory store. */
  protected async flush(): Promise<void> {
    // intentionally empty
  }

  async upsertGoal(goal: Goal): Promise<Goal> {
    this.state.goals[goal.id] = clone(goal);
    await this.flush();
    return goal;
  }

  async getActiveGoals(accountId: string): Promise<Goal[]> {
    return Object.values(this.state.goals)
      .filter((g) => g.accountId === accountId && g.status === "active")
      .map(clone);
  }

  async setMastery(record: ConceptMastery): Promise<void> {
    this.state.mastery[masteryKey(record.accountId, record.conceptId)] = clone(record);
    await this.flush();
  }

  async getMastery(accountId: string, conceptId: string): Promise<ConceptMastery | undefined> {
    const found = this.state.mastery[masteryKey(accountId, conceptId)];
    return found ? clone(found) : undefined;
  }

  async listMastery(accountId: string): Promise<ConceptMastery[]> {
    return Object.values(this.state.mastery)
      .filter((m) => m.accountId === accountId)
      .map(clone);
  }

  async recordAttempt(attempt: Attempt): Promise<void> {
    this.state.attempts[attempt.id] = clone(attempt);
    await this.flush();
  }

  async getAttempt(id: string): Promise<Attempt | undefined> {
    const found = this.state.attempts[id];
    return found ? clone(found) : undefined;
  }

  async upsertMisconception(m: Misconception): Promise<Misconception> {
    this.state.misconceptions[m.id] = clone(m);
    await this.flush();
    return m;
  }

  async getOpenMisconceptions(accountId: string): Promise<Misconception[]> {
    return Object.values(this.state.misconceptions)
      .filter((m) => m.accountId === accountId && m.status === "open")
      .map(clone);
  }

  async recordStage(record: StageRecord): Promise<void> {
    const exists = this.state.stages.some(
      (s) => s.accountId === record.accountId && s.lessonId === record.lessonId && s.stage === record.stage
    );
    if (!exists) {
      this.state.stages.push(clone(record));
      await this.flush();
    }
  }

  async getCompletedStages(accountId: string, lessonId: string): Promise<ModalityStage[]> {
    return this.state.stages
      .filter((s) => s.accountId === accountId && s.lessonId === lessonId)
      .map((s) => s.stage);
  }

  async upsertReview(record: ReviewRecord): Promise<void> {
    this.state.reviews[masteryKey(record.accountId, record.conceptId)] = clone(record);
    await this.flush();
  }

  async getDueReviews(accountId: string, now: Date): Promise<ReviewRecord[]> {
    const cutoff = now.getTime();
    return Object.values(this.state.reviews)
      .filter((r) => r.accountId === accountId && new Date(r.dueAt).getTime() <= cutoff)
      .sort((a, b) => new Date(a.dueAt).getTime() - new Date(b.dueAt).getTime())
      .map(clone);
  }

  async setPreferences(prefs: LearnerPreferences): Promise<void> {
    this.state.preferences[prefs.accountId] = clone(prefs);
    await this.flush();
  }

  async getPreferences(accountId: string): Promise<LearnerPreferences | undefined> {
    const found = this.state.preferences[accountId];
    return found ? clone(found) : undefined;
  }

  async saveSession(session: AgentSession): Promise<void> {
    this.state.sessions[session.id] = clone(session);
    await this.flush();
  }

  async getSession(id: string): Promise<AgentSession | undefined> {
    const found = this.state.sessions[id];
    return found ? clone(found) : undefined;
  }

  async appendTurn(turn: ConversationTurn): Promise<void> {
    this.state.turns.push(clone(turn));
    await this.flush();
  }

  async getTurns(sessionId: string): Promise<ConversationTurn[]> {
    return this.state.turns
      .filter((t) => t.sessionId === sessionId)
      .sort((a, b) => a.index - b.index)
      .map(clone);
  }

  async savePlan(plan: Plan): Promise<void> {
    this.state.plans[plan.id] = clone(plan);
    await this.flush();
  }

  async getPlan(id: string): Promise<Plan | undefined> {
    const found = this.state.plans[id];
    return found ? clone(found) : undefined;
  }

  async appendTrace(event: TraceEvent): Promise<void> {
    this.state.traces.push(clone(event));
    await this.flush();
  }

  async getTraces(sessionId: string): Promise<TraceEvent[]> {
    return this.state.traces
      .filter((t) => t.sessionId === sessionId)
      .sort((a, b) => a.seq - b.seq)
      .map(clone);
  }

  async saveApproval(request: ApprovalRequest): Promise<void> {
    this.state.approvals[request.id] = clone(request);
    await this.flush();
  }

  async getApproval(id: string): Promise<ApprovalRequest | undefined> {
    const found = this.state.approvals[id];
    return found ? clone(found) : undefined;
  }

  async listApprovals(artifactId: string): Promise<ApprovalRequest[]> {
    return Object.values(this.state.approvals)
      .filter((a) => a.artifactId === artifactId)
      .map(clone);
  }

  async saveArtifact(artifact: Artifact): Promise<void> {
    this.state.artifacts[artifact.id] = clone(artifact);
    await this.flush();
  }

  async getArtifact(id: string): Promise<Artifact | undefined> {
    const found = this.state.artifacts[id];
    return found ? clone(found) : undefined;
  }

  async setSessionSummary(summary: SessionSummary): Promise<void> {
    this.state.summaries[summary.sessionId] = clone(summary);
    await this.flush();
  }

  async getSessionSummary(sessionId: string): Promise<SessionSummary | undefined> {
    const found = this.state.summaries[sessionId];
    return found ? clone(found) : undefined;
  }
}
