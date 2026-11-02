import { redactData, type TraceEvent, type TraceEventType } from "@learning-platform/agent-contract";
import type { LearnerMemory } from "./memory/index.js";
import type { Clock, IdFactory } from "./support.js";

/**
 * Records trace events into durable memory. All event `data` is redacted before
 * storage so secrets and raw PII never persist. No hidden reasoning is stored.
 */
export class TraceRecorder {
  private seq = 0;

  constructor(
    private readonly sessionId: string,
    private readonly memory: LearnerMemory,
    private readonly clock: Clock,
    private readonly idFactory: IdFactory
  ) {}

  async emit(type: TraceEventType, summary: string, data?: Record<string, unknown>): Promise<TraceEvent> {
    const event: TraceEvent = {
      id: this.idFactory("trace"),
      sessionId: this.sessionId,
      seq: this.seq++,
      type,
      at: this.clock().toISOString(),
      summary,
      ...(data ? { data: redactData(data) } : {})
    };
    await this.memory.appendTrace(event);
    return event;
  }
}
