import { spawn } from "node:child_process";
import { randomUUID } from "node:crypto";
import { readFile, rm } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { ProviderUnavailableError } from "./errors.js";
import type { CompletionRequest, LLMProviderAdapter } from "./types.js";

export interface CodexCliConfig {
  command?: string;
  model?: string;
  workingDirectory?: string;
  timeoutMs?: number;
  runner?: (prompt: string) => Promise<string>;
}

/**
 * Use the local Codex CLI's cached ChatGPT login without reading, copying, or
 * forwarding its credential. The subprocess is ephemeral, read-only, and has
 * project/user rules disabled so it behaves as a narrow text-model boundary.
 */
export function createCodexCliAdapter(config: CodexCliConfig = {}): LLMProviderAdapter {
  const model = config.model || "gpt-5.5";
  const runner = config.runner ?? ((prompt: string) => runCodex(prompt, config));

  return {
    async complete(request) {
      const content = (await runner(formatPrompt(request))).trim();
      if (!content) {
        throw new ProviderUnavailableError("Codex CLI returned an empty completion.");
      }
      return { content, model };
    },

    async *stream(request) {
      const completion = await this.complete(request);
      yield { contentDelta: completion.content, done: false };
      yield { contentDelta: "", done: true };
    },

    async embed() {
      throw new ProviderUnavailableError(
        "Codex ChatGPT authentication provides completions, not embeddings. Configure a separate embedding provider for ingestion."
      );
    }
  };
}

function formatPrompt(request: CompletionRequest): string {
  const transcript = request.messages
    .map((message) => `${message.role.toUpperCase()}:\n${message.content}`)
    .join("\n\n");
  return [
    "Act only as a text model for a local learning application.",
    "Do not inspect files, run commands, use tools, or add commentary.",
    "Follow the message transcript and return only the requested assistant response.",
    transcript
  ].join("\n\n");
}

async function runCodex(prompt: string, config: CodexCliConfig): Promise<string> {
  const outputPath = join(tmpdir(), `learning-codex-${randomUUID()}.txt`);
  const command = config.command || "codex";
  const args = [
    "exec",
    "--ephemeral",
    "--sandbox",
    "read-only",
    "--skip-git-repo-check",
    "--ignore-user-config",
    "--ignore-rules",
    "--color",
    "never",
    ...(config.model ? ["--model", config.model] : []),
    "--output-last-message",
    outputPath,
    "-"
  ];

  try {
    await spawnCodex(command, args, prompt, config.workingDirectory, config.timeoutMs ?? 120_000);
    return await readFile(outputPath, "utf8");
  } catch (error) {
    if (error instanceof ProviderUnavailableError) throw error;
    throw new ProviderUnavailableError(error instanceof Error ? error.message : "Codex CLI failed.");
  } finally {
    await rm(outputPath, { force: true }).catch(() => undefined);
  }
}

function spawnCodex(
  command: string,
  args: string[],
  prompt: string,
  workingDirectory: string | undefined,
  timeoutMs: number
): Promise<void> {
  return new Promise((resolve, reject) => {
    const child = spawn(command, args, {
      cwd: workingDirectory || tmpdir(),
      windowsHide: true,
      shell: process.platform === "win32",
      stdio: ["pipe", "ignore", "pipe"]
    });
    let stderr = "";
    const timer = setTimeout(() => {
      child.kill();
      reject(new ProviderUnavailableError(`Codex CLI timed out after ${timeoutMs}ms.`));
    }, timeoutMs);

    child.stderr.setEncoding("utf8");
    child.stderr.on("data", (chunk: string) => {
      if (stderr.length < 16_384) stderr += chunk;
    });
    child.on("error", (error) => {
      clearTimeout(timer);
      reject(new ProviderUnavailableError(`Could not start Codex CLI: ${error.message}`));
    });
    child.on("close", (code) => {
      clearTimeout(timer);
      if (code === 0) resolve();
      else reject(new ProviderUnavailableError(`Codex CLI exited with code ${code}: ${stderr.slice(-2_000)}`));
    });
    child.stdin.end(prompt);
  });
}
