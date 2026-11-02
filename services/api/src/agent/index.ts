import { ArtifactService } from "./artifacts/index.js";
import { VerticalFixture } from "./tools/fixture.js";
import { createDomainTools } from "./tools/domainTools.js";
import { ToolRegistry } from "./toolRegistry.js";
import { systemClock, uuidIdFactory, type Clock, type IdFactory } from "./support.js";
import { ApprovalService } from "./approval/index.js";
import { PublicationOutbox } from "./publication/index.js";
import { JobManager } from "./jobs.js";

export * from "./support.js";
export * from "./policy.js";
export * from "./idempotency.js";
export * from "./trace.js";
export * from "./toolRegistry.js";
export * from "./model.js";
export * from "./runtime.js";
export * from "./jobs.js";
export * from "./memory/index.js";
export * from "./tools/fixture.js";
export * from "./tools/catalog.js";
export * from "./tools/domainTools.js";
export * from "./artifacts/index.js";
export * from "./approval/index.js";
export * from "./publication/index.js";
export * from "./workflows/index.js";
export * from "./pgTenancy.js";

export interface LearningAgentDeps {
  fixture: VerticalFixture;
  artifacts: ArtifactService;
  registry: ToolRegistry;
  approvals: ApprovalService;
  jobs: JobManager;
  /** Present only when an internal publication outbox is configured. */
  publicationOutbox?: PublicationOutbox;
}

export interface CreateLearningAgentInput {
  memory: import("./memory/index.js").LearnerMemory;
  clock?: Clock;
  idFactory?: IdFactory;
  fixture?: VerticalFixture;
  /** Optional internal reviewed-draft outbox (absolute directory). */
  publicationOutbox?: PublicationOutbox;
}

/**
 * Wire a complete deterministic agent stack: fixture-backed domain tools, the
 * artifact service (with sanitizer), the approval service, and a job manager.
 * When a publication outbox is provided, the educator publish tool queues an
 * immutable reviewed draft package instead of only signaling readiness.
 */
export function createLearningAgent(input: CreateLearningAgentInput): LearningAgentDeps {
  const clock = input.clock ?? systemClock;
  const idFactory = input.idFactory ?? uuidIdFactory;
  const fixture = input.fixture ?? new VerticalFixture();
  const artifacts = new ArtifactService(input.memory, clock, idFactory);
  const registry = new ToolRegistry();
  const approvals = new ApprovalService(input.memory, clock, idFactory);
  for (const tool of createDomainTools(artifacts, approvals, input.publicationOutbox)) {
    registry.register(tool);
  }
  const jobs = new JobManager(clock, idFactory);
  return {
    fixture,
    artifacts,
    registry,
    approvals,
    jobs,
    ...(input.publicationOutbox ? { publicationOutbox: input.publicationOutbox } : {})
  };
}
