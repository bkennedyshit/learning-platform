export const ACCOUNT_ROLES = [
  "b2c_learner",
  "student",
  "educator",
  "org_admin",
  "affiliate",
  "platform_admin"
] as const;

export type AccountRole = (typeof ACCOUNT_ROLES)[number];

export type ConsentStatus = "not_required" | "pending" | "granted" | "revoked";

export interface Account {
  id: string;
  email: string;
  passwordHash: string;
  role: AccountRole;
  organizationId?: string;
  birthdate?: string;
  consentStatus: ConsentStatus;
}

export interface Principal {
  accountId: string;
  role: AccountRole;
  organizationId?: string;
}

export interface RegisterAccountInput {
  email: string;
  password: string;
  role?: AccountRole;
  organizationId?: string;
  birthdate?: string;
}

export interface Session {
  token: string;
  cookie: string;
  principal: Principal;
}

export interface PasswordResetRequest {
  resetToken: string;
  expiresAt: Date;
}

export function isAccountRole(value: unknown): value is AccountRole {
  return typeof value === "string" && ACCOUNT_ROLES.includes(value as AccountRole);
}

export function isPrincipal(value: unknown): value is Principal {
  if (!value || typeof value !== "object") {
    return false;
  }

  const candidate = value as Partial<Principal>;
  return typeof candidate.accountId === "string" && isAccountRole(candidate.role);
}
