import type { Job, JobProgressEvent, StructuredError } from "@learning-platform/agent-contract";
import type { Clock, IdFactory } from "./support.js";

export class JobCancelledError extends Error {
  constructor() {
    super("job cancelled");
    this.name = "JobCancelledError";
  }
}

export interface JobWorkerHelpers {
  reportProgress(progress: number, message?: string): Promise<void>;
  readonly signal: { readonly cancelled: boolean };
}

export type JobWorker = (helpers: JobWorkerHelpers) => Promise<string[]>;

export interface JobHandle {
  jobId: string;
  done: Promise<Job>;
}

/**
 * In-process background job manager with progress reporting and cooperative
 * cancellation. `reportProgress` throws {@link JobCancelledError} once a job is
 * cancelled so cooperative workers unwind promptly.
 */
export class JobManager {
  private readonly jobs = new Map<string, Job>();
  private readonly events = new Map<string, JobProgressEvent[]>();
  private readonly cancels = new Map<string, { cancelled: boolean }>();

  constructor(
    private readonly clock: Clock,
    private readonly idFactory: IdFactory
  ) {}

  start(input: { sessionId: string; kind: string; worker: JobWorker }): JobHandle {
    const now = this.clock().toISOString();
    const jobId = this.idFactory("job");
    const job: Job = {
      id: jobId,
      sessionId: input.sessionId,
      kind: input.kind,
      status: "running",
      progress: 0,
      createdAt: now,
      updatedAt: now
    };
    this.jobs.set(jobId, job);
    this.events.set(jobId, []);
    const signal = { cancelled: false };
    this.cancels.set(jobId, signal);

    const helpers: JobWorkerHelpers = {
      signal,
      reportProgress: async (progress, message) => {
        if (signal.cancelled) {
          throw new JobCancelledError();
        }
        this.update(jobId, { progress: Math.min(1, Math.max(0, progress)) });
        const event: JobProgressEvent = {
          jobId,
          progress: Math.min(1, Math.max(0, progress)),
          at: this.clock().toISOString(),
          ...(message ? { message } : {})
        };
        this.events.get(jobId)?.push(event);
      }
    };

    const done = (async (): Promise<Job> => {
      try {
        const resultArtifactIds = await input.worker(helpers);
        if (signal.cancelled) {
          return this.update(jobId, { status: "cancelled" });
        }
        return this.update(jobId, { status: "succeeded", progress: 1, resultArtifactIds });
      } catch (err) {
        if (signal.cancelled || err instanceof JobCancelledError) {
          return this.update(jobId, { status: "cancelled" });
        }
        const error: StructuredError = {
          code: "job_failed",
          message: err instanceof Error ? err.message : "job failed",
          retryable: true
        };
        return this.update(jobId, { status: "failed", error });
      }
    })();

    return { jobId, done };
  }

  cancel(jobId: string): void {
    const signal = this.cancels.get(jobId);
    if (signal) {
      signal.cancelled = true;
    }
  }

  get(jobId: string): Job | undefined {
    const job = this.jobs.get(jobId);
    return job ? { ...job } : undefined;
  }

  getEvents(jobId: string): JobProgressEvent[] {
    return [...(this.events.get(jobId) ?? [])];
  }

  private update(jobId: string, patch: Partial<Job>): Job {
    const current = this.jobs.get(jobId);
    if (!current) {
      throw new Error(`Job ${jobId} not found`);
    }
    const updated: Job = { ...current, ...patch, updatedAt: this.clock().toISOString() };
    this.jobs.set(jobId, updated);
    return { ...updated };
  }
}
