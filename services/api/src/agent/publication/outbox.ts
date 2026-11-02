import { createHash } from "node:crypto";
import { mkdir, rename, writeFile, readFile, readdir, access } from "node:fs/promises";
import path from "node:path";
import type { Artifact, ApprovalRequest } from "@learning-platform/agent-contract";

/**
 * The learning agent must NEVER write directly to the public corpus or SEO
 * catalog. The publication outbox is the honest middle ground: after an educator
 * approves an exact artifact version, an immutable *reviewed draft package* is
 * written to an internal, operator-controlled directory. A normal reviewed
 * commit / static site build later consumes the outbox and performs the actual
 * publication. Writing a package here does NOT make the artifact public.
 */

export class PublicationOutboxError extends Error {
  constructor(
    readonly code: "path_unsafe" | "exists" | "invalid",
    message: string
  ) {
    super(message);
    this.name = "PublicationOutboxError";
  }
}

/** The immutable package persisted for each approved artifact version. */
export interface ReviewedDraftPackage {
  packageVersion: 1;
  packageId: string;
  artifactId: string;
  version: number;
  /** Present, sanitized artifact — never the raw model source alone. */
  artifact: Artifact;
  /** The educator-approved publish request that authorized this package. */
  approval: {
    id: string;
    status: string;
    decidedBy?: string;
    decidedAt?: string;
    requestedBy: string;
    provenance?: Record<string, unknown>;
  };
  metadata: {
    title: string;
    lessonIds: string[];
    conceptIds: string[];
    createdBy: string;
    kind: string;
  };
  writtenAt: string;
  /** Explicit reminder that this is not yet public. */
  published: false;
}

export interface WriteReviewedDraftInput {
  artifact: Artifact;
  approval: ApprovalRequest;
  now: string;
}

export interface WriteReviewedDraftResult {
  packageId: string;
  absolutePath: string;
  relativePath: string;
}

/**
 * Convert an arbitrary id into a filename-safe token. Anything outside
 * `[A-Za-z0-9._-]` becomes `_`. Leading dots are stripped so a crafted id can
 * never produce a dotfile or traversal segment.
 */
export function toFilenameSafe(id: string): string {
  const cleaned = id.replace(/[^A-Za-z0-9._-]/g, "_").replace(/^\.+/, "");
  return cleaned.length > 0 ? cleaned : "artifact";
}

export class PublicationOutbox {
  private readonly root: string;

  constructor(root: string) {
    if (!root || !path.isAbsolute(root)) {
      throw new PublicationOutboxError("invalid", "Publication outbox root must be an absolute path.");
    }
    this.root = path.resolve(root);
  }

  /**
   * Resolve the on-disk path for an artifact/version package, guaranteeing the
   * result stays strictly inside the outbox root. A traversal attempt
   * (e.g. an artifact id containing `..` or separators) raises `path_unsafe`.
   */
  private resolvePackagePath(artifactId: string, version: number): { abs: string; rel: string } {
    if (!Number.isInteger(version) || version < 1) {
      throw new PublicationOutboxError("invalid", `Invalid version ${version}.`);
    }
    if (/[\\/]/.test(artifactId) || artifactId.includes("..")) {
      throw new PublicationOutboxError("path_unsafe", "Artifact id must not contain path separators.");
    }
    const fileName = `${toFilenameSafe(artifactId)}__v${version}.json`;
    const abs = path.resolve(this.root, fileName);
    const rootWithSep = this.root.endsWith(path.sep) ? this.root : this.root + path.sep;
    if (abs !== path.join(this.root, fileName) || !abs.startsWith(rootWithSep)) {
      throw new PublicationOutboxError("path_unsafe", "Resolved package path escapes the outbox root.");
    }
    return { abs, rel: fileName };
  }

  private packageId(artifactId: string, version: number, artifact: Artifact): string {
    const digest = createHash("sha256")
      .update(`${artifactId}:${version}:${artifact.sanitizedSource}`)
      .digest("hex")
      .slice(0, 16);
    return `pkg_${toFilenameSafe(artifactId)}_v${version}_${digest}`;
  }

  /**
   * Atomically write an immutable reviewed draft package. Refuses to overwrite
   * an existing package for the same artifact+version so prior approved versions
   * stay recoverable (immutability). Uses temp-file + rename for atomicity.
   */
  async writeReviewedDraft(input: WriteReviewedDraftInput): Promise<WriteReviewedDraftResult> {
    const { artifact, approval } = input;
    if (approval.status !== "approved" || approval.action !== "publish") {
      throw new PublicationOutboxError("invalid", "Only an approved publish request may be written.");
    }
    if (approval.artifactId !== artifact.id || approval.version !== artifact.version) {
      throw new PublicationOutboxError(
        "invalid",
        "Approval must reference the exact artifact id and version."
      );
    }

    const { abs, rel } = this.resolvePackagePath(artifact.id, artifact.version);
    await mkdir(this.root, { recursive: true });

    // Immutability: never clobber an existing package for this version.
    if (await this.exists(abs)) {
      throw new PublicationOutboxError(
        "exists",
        `A reviewed package for ${artifact.id} v${artifact.version} already exists.`
      );
    }

    const packageId = this.packageId(artifact.id, artifact.version, artifact);
    const pkg: ReviewedDraftPackage = {
      packageVersion: 1,
      packageId,
      artifactId: artifact.id,
      version: artifact.version,
      artifact,
      approval: {
        id: approval.id,
        status: approval.status,
        ...(approval.decidedBy ? { decidedBy: approval.decidedBy } : {}),
        ...(approval.decidedAt ? { decidedAt: approval.decidedAt } : {}),
        requestedBy: approval.requestedBy,
        ...(approval.provenance ? { provenance: approval.provenance } : {})
      },
      metadata: {
        title: artifact.title,
        lessonIds: artifact.lessonIds,
        conceptIds: artifact.conceptIds,
        createdBy: artifact.createdBy,
        kind: artifact.kind
      },
      writtenAt: input.now,
      published: false
    };

    const serialized = JSON.stringify(pkg, null, 2);
    const tmp = `${abs}.${packageId}.tmp`;
    await writeFile(tmp, serialized, { encoding: "utf8", flag: "wx" });
    // rename is atomic within the same directory; this never partially writes
    // the destination and cannot clobber because we checked existence above.
    await rename(tmp, abs);

    return { packageId, absolutePath: abs, relativePath: rel };
  }

  /** Recover a previously written package (e.g. a prior approved version). */
  async readReviewedDraft(artifactId: string, version: number): Promise<ReviewedDraftPackage | undefined> {
    const { abs } = this.resolvePackagePath(artifactId, version);
    try {
      const raw = await readFile(abs, "utf8");
      return JSON.parse(raw) as ReviewedDraftPackage;
    } catch {
      return undefined;
    }
  }

  /** List all package filenames currently in the outbox. */
  async list(): Promise<string[]> {
    try {
      const entries = await readdir(this.root);
      return entries.filter((e) => e.endsWith(".json")).sort();
    } catch {
      return [];
    }
  }

  private async exists(abs: string): Promise<boolean> {
    try {
      await access(abs);
      return true;
    } catch {
      return false;
    }
  }
}
