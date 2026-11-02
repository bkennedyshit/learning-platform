import type { AccountRole, Principal, ToolCategory, ToolDefinition } from "@learning-platform/agent-contract";

export class PolicyDeniedError extends Error {
  readonly code = "policy_denied";
  constructor(message: string) {
    super(message);
    this.name = "PolicyDeniedError";
  }
}

const ROLE_RANK: Record<AccountRole, number> = {
  b2c_learner: 1,
  student: 1,
  affiliate: 1,
  educator: 2,
  org_admin: 3,
  platform_admin: 4
};

export function hasRoleAtLeast(principal: Principal, required: AccountRole): boolean {
  return ROLE_RANK[principal.role] >= ROLE_RANK[required];
}

const EDUCATOR_ROLES: AccountRole[] = ["educator", "org_admin", "platform_admin"];

export function isEducator(principal: Principal): boolean {
  return EDUCATOR_ROLES.includes(principal.role);
}

/** Category-level gate. `educator` tools are restricted to educator+ roles. */
export function canUseCategory(principal: Principal, category: ToolCategory): boolean {
  if (category === "educator") {
    return isEducator(principal);
  }
  return true;
}

/** Full authorization check for a tool definition. Throws on denial. */
export function authorizeTool(principal: Principal, definition: ToolDefinition): void {
  if (!canUseCategory(principal, definition.category)) {
    throw new PolicyDeniedError(`Role ${principal.role} may not use ${definition.category} tools.`);
  }
  if (definition.requiredRole && !hasRoleAtLeast(principal, definition.requiredRole)) {
    throw new PolicyDeniedError(
      `Tool ${definition.name} requires role ${definition.requiredRole} or higher.`
    );
  }
}

/**
 * Ownership: a principal may only act on their own account records, unless they
 * are an educator+ acting within the same organization.
 */
export function assertAccountAccess(principal: Principal, targetAccountId: string, targetOrgId?: string): void {
  if (principal.accountId === targetAccountId) {
    return;
  }
  if (isEducator(principal) && targetOrgId !== undefined && principal.organizationId === targetOrgId) {
    return;
  }
  throw new PolicyDeniedError("Principal may not access another learner's records.");
}
