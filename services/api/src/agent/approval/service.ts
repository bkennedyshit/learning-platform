import type {
  ApprovalAction,
  ApprovalRequest,
  Principal
} from "@learning-platform/agent-contract";
import type { LearnerMemory } from "../memory/index.js";
import { isEducator } from "../policy.js";
import type { Clock, IdFactory } from "../support.js";

export class ApprovalError extends Error {
  constructor(
    readonly code: string,
    message: string
  ) {
    super(message);
    this.name = "ApprovalError";
  }
}

export interface DraftApprovalInput {
  artifactId: string;
  action: ApprovalAction;
  requestedBy: string;
  version: number;
  sessionId?: string;
  provenance?: Record<string, unknown>;
}

/**
 * Approval workflow: draft → approve/reject. Only educators may decide.
 * Publishing is blocked until an approved request exists for the artifact's
 * current version. Every decision preserves version and provenance.
 */
export class ApprovalService {
  constructor(
    private readonly memory: LearnerMemory,
    private readonly clock: Clock,
    private readonly idFactory: IdFactory
  ) {}

  async draft(input: DraftApprovalInput): Promise<ApprovalRequest> {
    const request: ApprovalRequest = {
      id: this.idFactory("approval"),
      action: input.action,
      status: "draft",
      artifactId: input.artifactId,
      requestedBy: input.requestedBy,
      version: input.version,
      createdAt: this.clock().toISOString(),
      ...(input.sessionId ? { sessionId: input.sessionId } : {}),
      ...(input.provenance ? { provenance: input.provenance } : {})
    };
    await this.memory.saveApproval(request);
    return request;
  }

  async submit(id: string): Promise<ApprovalRequest> {
    const request = await this.require(id);
    if (request.status !== "draft") {
      throw new ApprovalError("invalid_transition", `Cannot submit an approval in status ${request.status}`);
    }
    const updated: ApprovalRequest = { ...request, status: "pending" };
    await this.memory.saveApproval(updated);
    return updated;
  }

  async approve(principal: Principal, id: string, reason?: string): Promise<ApprovalRequest> {
    this.assertEducator(principal);
    const request = await this.require(id);
    if (request.status === "approved" || request.status === "rejected") {
      throw new ApprovalError("invalid_transition", `Approval already ${request.status}`);
    }
    const updated: ApprovalRequest = {
      ...request,
      status: "approved",
      decidedBy: principal.accountId,
      decidedAt: this.clock().toISOString(),
      ...(reason ? { reason } : {})
    };
    await this.memory.saveApproval(updated);
    return updated;
  }

  async reject(principal: Principal, id: string, reason: string): Promise<ApprovalRequest> {
    this.assertEducator(principal);
    const request = await this.require(id);
    if (request.status === "approved" || request.status === "rejected") {
      throw new ApprovalError("invalid_transition", `Approval already ${request.status}`);
    }
    const updated: ApprovalRequest = {
      ...request,
      status: "rejected",
      decidedBy: principal.accountId,
      decidedAt: this.clock().toISOString(),
      reason
    };
    await this.memory.saveApproval(updated);
    return updated;
  }

  /** True only when an approved publish request exists for this exact version. */
  async isPublishable(artifactId: string, version: number): Promise<boolean> {
    const approvals = await this.memory.listApprovals(artifactId);
    return approvals.some(
      (a) => a.action === "publish" && a.status === "approved" && a.version === version
    );
  }

  /** Return the approved publish request for an exact version, if any. */
  async getApprovedPublish(artifactId: string, version: number): Promise<ApprovalRequest | undefined> {
    const approvals = await this.memory.listApprovals(artifactId);
    return approvals.find(
      (a) => a.action === "publish" && a.status === "approved" && a.version === version
    );
  }

  /** Publishing requires educator role AND a prior approved publish request. */
  async publish(principal: Principal, artifactId: string, version: number): Promise<void> {
    this.assertEducator(principal);
    if (!(await this.isPublishable(artifactId, version))) {
      throw new ApprovalError(
        "not_approved",
        `Artifact ${artifactId} v${version} is not approved for publishing.`
      );
    }
  }

  private assertEducator(principal: Principal): void {
    if (!isEducator(principal)) {
      throw new ApprovalError("forbidden", "Only educators may decide approvals.");
    }
  }

  private async require(id: string): Promise<ApprovalRequest> {
    const request = await this.memory.getApproval(id);
    if (!request) {
      throw new ApprovalError("not_found", `Approval ${id} not found`);
    }
    return request;
  }
}
