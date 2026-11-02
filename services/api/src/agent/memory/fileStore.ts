import { mkdirSync, readFileSync, writeFileSync, existsSync, renameSync } from "node:fs";
import { isAbsolute, resolve, sep } from "node:path";
import { InMemoryLearnerMemory } from "./inMemoryStore.js";
import { emptyMemoryState, type MemoryState } from "./types.js";

export interface FileLearnerMemoryConfig {
  /**
   * Configured internal directory owned by the service. This is never a
   * model-supplied path. The store persists a single JSON snapshot here.
   */
  root: string;
  fileName?: string;
}

/**
 * Ensures `root` is an absolute path and the resolved snapshot file stays
 * inside it. Model-authored paths must never reach this store.
 */
function resolveSnapshotPath(root: string, fileName: string): string {
  if (!isAbsolute(root)) {
    throw new Error("FileLearnerMemory root must be an absolute, service-configured path.");
  }
  if (fileName.includes("/") || fileName.includes("\\") || fileName.includes("..")) {
    throw new Error("FileLearnerMemory fileName must be a plain file name.");
  }
  const normalizedRoot = resolve(root);
  const target = resolve(normalizedRoot, fileName);
  const rootWithSep = normalizedRoot.endsWith(sep) ? normalizedRoot : normalizedRoot + sep;
  if (target !== resolve(normalizedRoot, fileName) || !target.startsWith(rootWithSep)) {
    throw new Error("Resolved memory path escapes the configured internal root.");
  }
  return target;
}

/**
 * Durable learner memory backed by an atomically-written JSON snapshot.
 * State survives process restart: construct a new instance with the same
 * config to resume.
 */
export class FileLearnerMemory extends InMemoryLearnerMemory {
  private readonly filePath: string;

  constructor(config: FileLearnerMemoryConfig) {
    const filePath = resolveSnapshotPath(config.root, config.fileName ?? "learner-memory.json");
    mkdirSync(config.root, { recursive: true });
    const initial = FileLearnerMemory.load(filePath);
    super(initial);
    this.filePath = filePath;
  }

  private static load(filePath: string): MemoryState {
    if (!existsSync(filePath)) {
      return emptyMemoryState();
    }
    const raw = readFileSync(filePath, "utf8").trim();
    if (raw.length === 0) {
      return emptyMemoryState();
    }
    const parsed = JSON.parse(raw) as MemoryState;
    // Merge onto an empty state so newly added collections are always present.
    return { ...emptyMemoryState(), ...parsed, version: 1 };
  }

  protected override async flush(): Promise<void> {
    const tmp = `${this.filePath}.tmp`;
    writeFileSync(tmp, JSON.stringify(this.state, null, 2), "utf8");
    renameSync(tmp, this.filePath);
  }

  /** Exposed for diagnostics/tests. */
  get snapshotPath(): string {
    return this.filePath;
  }
}
