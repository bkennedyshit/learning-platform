import type { LLMProviderAdapter } from "@learning-platform/llm-adapter";
import type { ToolDefinition } from "@learning-platform/agent-contract";

/**
 * Provider-neutral model boundary. The runtime only ever talks to an
 * {@link AgentModel}; concrete providers (local Ollama, hosted OpenAI-compatible,
 * Gemini) and the deterministic fake model implement the same interface. No
 * provider-specific payloads leak into tools or memory.
 */

export interface ModelObservation {
  toolName: string;
  ok: boolean;
  summary: string;
  output?: unknown;
}

export interface AgentModelStepInput {
  goal: string;
  step: number;
  toolCatalog: ToolDefinition[];
  observations: ModelObservation[];
  context?: {
    learnerMessage?: string;
    lessonId?: string;
    conceptId?: string;
  };
}

export interface AgentModelAction {
  kind: "tool" | "finish";
  toolName?: string;
  input?: unknown;
  idempotencyKey?: string;
  /** The learner-facing answer when kind is finish. */
  response?: string;
  /**
   * A short, observable decision summary. This is NOT hidden chain-of-thought:
   * it is a user-facing justification recorded in the trace.
   */
  rationaleSummary: string;
}

export interface AgentModel {
  readonly name: string;
  planStep(input: AgentModelStepInput): Promise<AgentModelAction>;
}

/**
 * Deterministic scripted model. Replays a fixed list of actions, one per step,
 * finishing when the script is exhausted. Used for deterministic runtime tests
 * and the local no-provider quickstart.
 */
export class ScriptedFakeModel implements AgentModel {
  readonly name: string;
  private index = 0;

  constructor(
    private readonly script: AgentModelAction[],
    name = "scripted-fake"
  ) {
    this.name = name;
  }

  async planStep(_input: AgentModelStepInput): Promise<AgentModelAction> {
    const action = this.script[this.index];
    this.index += 1;
    if (!action) {
      return { kind: "finish", rationaleSummary: "Script complete; goal addressed." };
    }
    return action;
  }
}

/**
 * Thin adapter that turns a provider-neutral {@link LLMProviderAdapter} into an
 * {@link AgentModel} by asking for a strict JSON action. Deliberately NOT used
 * in deterministic tests — live-provider behavior is never asserted here.
 */
export function createLlmAgentModel(adapter: LLMProviderAdapter, name = "llm"): AgentModel {
  return {
    name,
    async planStep(input) {
      const completion = await adapter.complete({
        temperature: 0,
        messages: [
          {
            role: "system",
            content:
              'Respond ONLY with valid JSON: {"kind":"tool"|"finish","toolName"?:string,"input"?:object,"rationaleSummary":string,"response"?:string}. Use exactly one listed tool per tool action and obey its inputSchema. When enough grounded observations exist, finish with a concise learner-facing answer in response. rationaleSummary is only a short observable action summary. Do not include hidden reasoning.'
          },
          {
            role: "user",
            content: JSON.stringify({
              goal: input.goal,
              context: input.context,
              step: input.step,
              tools: input.toolCatalog.map((t) => ({
                name: t.name,
                category: t.category,
                description: t.description,
                inputSchema: t.inputSchema
              })),
              observations: input.observations
            })
          }
        ]
      });
      try {
        const parsed = JSON.parse(completion.content) as AgentModelAction;
        return parsed;
      } catch {
        return { kind: "finish", rationaleSummary: "Model returned unparseable output; stopping safely." };
      }
    }
  };
}
