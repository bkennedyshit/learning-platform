import {
  parse,
  validate,
  type Principal,
  type StructuredError,
  type ToolCategory,
  type ToolDefinition,
  type ToolResult
} from "@learning-platform/agent-contract";
import type { LearnerMemory } from "./memory/index.js";
import type { VerticalFixture } from "./tools/fixture.js";
import { authorizeTool, PolicyDeniedError } from "./policy.js";
import { InMemoryIdempotencyStore, type IdempotencyStore } from "./idempotency.js";
import { systemClock, uuidIdFactory, type Clock, type IdFactory } from "./support.js";
import type { TraceRecorder } from "./trace.js";

export interface ToolContext {
  principal: Principal;
  memory: LearnerMemory;
  fixture: VerticalFixture;
  sessionId: string;
  clock: Clock;
  idFactory: IdFactory;
  idempotency: IdempotencyStore;
  trace?: TraceRecorder;
}

export interface AgentTool<I = unknown, O = unknown> {
  definition: ToolDefinition;
  execute(input: I, ctx: ToolContext): Promise<O>;
}

export class ToolError extends Error {
  constructor(
    readonly code: string,
    message: string,
    readonly retryable = false,
    readonly details?: Record<string, unknown>
  ) {
    super(message);
    this.name = "ToolError";
  }
}

function toStructuredError(err: unknown): StructuredError {
  if (err instanceof ToolError) {
    return {
      code: err.code,
      message: err.message,
      retryable: err.retryable,
      ...(err.details ? { details: err.details } : {})
    };
  }
  if (err instanceof PolicyDeniedError) {
    return { code: err.code, message: err.message, retryable: false };
  }
  if (err instanceof Error) {
    const code = (err as { code?: unknown }).code;
    return {
      code: typeof code === "string" ? code : "tool_error",
      message: err.message,
      retryable: false
    };
  }
  return { code: "tool_error", message: "Unknown tool error", retryable: false };
}

export class ToolRegistry {
  private readonly tools = new Map<string, AgentTool>();

  register<I, O>(tool: AgentTool<I, O>): this {
    if (this.tools.has(tool.definition.name)) {
      throw new Error(`Tool ${tool.definition.name} is already registered.`);
    }
    this.tools.set(tool.definition.name, tool as AgentTool);
    return this;
  }

  get(name: string): AgentTool | undefined {
    return this.tools.get(name);
  }

  list(): ToolDefinition[] {
    return [...this.tools.values()].map((t) => t.definition).sort((a, b) => a.name.localeCompare(b.name));
  }

  listByCategory(category: ToolCategory): ToolDefinition[] {
    return this.list().filter((d) => d.category === category);
  }

  /**
   * Invoke a tool with full contract enforcement: authorization, input schema
   * validation, idempotency for state changes, output schema validation, and
   * a structured {@link ToolResult}. Never throws for expected failures.
   */
  async invoke(
    name: string,
    rawInput: unknown,
    ctx: ToolContext,
    idempotencyKey?: string
  ): Promise<ToolResult> {
    const startedAt = ctx.clock().toISOString();
    const callId = ctx.idFactory("call");
    const tool = this.tools.get(name);

    const finish = (partial: Omit<ToolResult, "callId" | "toolName" | "startedAt" | "finishedAt">): ToolResult => ({
      callId,
      toolName: name,
      startedAt,
      finishedAt: ctx.clock().toISOString(),
      ...partial
    });

    if (!tool) {
      const error: StructuredError = { code: "unknown_tool", message: `No tool named ${name}`, retryable: false };
      await ctx.trace?.emit("error", `unknown tool ${name}`, { error });
      return finish({ ok: false, error });
    }

    await ctx.trace?.emit("tool_call", name, { input: rawInput, idempotencyKey });

    try {
      authorizeTool(ctx.principal, tool.definition);

      const inputResult = validate(tool.definition.inputSchema, rawInput);
      if (!inputResult.ok) {
        throw new ToolError("invalid_input", `Invalid input for ${name}`, false, {
          errors: inputResult.errors
        });
      }

      const canReuse = tool.definition.category === "state_change" && tool.definition.idempotent && idempotencyKey;
      if (canReuse) {
        const prior = await ctx.idempotency.get(name, idempotencyKey);
        if (prior !== undefined) {
          await ctx.trace?.emit("tool_result", `${name} (idempotent replay)`, { output: prior });
          return finish({ ok: true, output: prior });
        }
      }

      const output = await tool.execute(rawInput, ctx);

      // Output must satisfy the declared schema; a violation is a server bug.
      parse(tool.definition.outputSchema, output, `${name} output`);

      if (canReuse) {
        await ctx.idempotency.set(name, idempotencyKey, output);
      }

      await ctx.trace?.emit("tool_result", name, { output });
      return finish({ ok: true, output });
    } catch (err) {
      const error = toStructuredError(err);
      await ctx.trace?.emit("error", `${name} failed: ${error.code}`, { error });
      return finish({ ok: false, error });
    }
  }
}

export interface CreateToolContextInput {
  principal: Principal;
  memory: LearnerMemory;
  fixture: VerticalFixture;
  sessionId: string;
  clock?: Clock;
  idFactory?: IdFactory;
  idempotency?: IdempotencyStore;
  trace?: TraceRecorder;
}

export function createToolContext(input: CreateToolContextInput): ToolContext {
  return {
    principal: input.principal,
    memory: input.memory,
    fixture: input.fixture,
    sessionId: input.sessionId,
    clock: input.clock ?? systemClock,
    idFactory: input.idFactory ?? uuidIdFactory,
    idempotency: input.idempotency ?? new InMemoryIdempotencyStore(),
    ...(input.trace ? { trace: input.trace } : {})
  };
}
