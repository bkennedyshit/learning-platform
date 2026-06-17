import { createHash } from "node:crypto";
import type { Pool } from "pg";
import type { Account, AccountRole, ConsentStatus, RegisterAccountInput } from "./types.js";

interface AccountRow {
  id: string;
  email: string;
  password_hash: string;
  role: AccountRole;
  organization_id: string | null;
  birthdate: string | null;
  consent_status: ConsentStatus;
}

export class AuthRepository {
  constructor(private readonly pool: Pool) {}

  async createAccount(input: RegisterAccountInput, passwordHash: string): Promise<Account> {
    const result = await this.pool.query<AccountRow>(
      `
        INSERT INTO accounts (email, password_hash, role, organization_id, birthdate)
        VALUES ($1, $2, $3, $4, $5)
        RETURNING id, email, password_hash, role, organization_id, birthdate, consent_status
      `,
      [
        input.email.toLowerCase(),
        passwordHash,
        input.role ?? "b2c_learner",
        input.organizationId ?? null,
        input.birthdate ?? null
      ]
    );

    const row = result.rows[0];
    if (!row) {
      throw new Error("Account insert did not return a row.");
    }

    return mapAccount(row);
  }

  async findAccountByEmail(email: string): Promise<Account | undefined> {
    const result = await this.pool.query<AccountRow>(
      `
        SELECT id, email, password_hash, role, organization_id, birthdate, consent_status
        FROM accounts
        WHERE email = $1
      `,
      [email.toLowerCase()]
    );

    const row = result.rows[0];
    return row ? mapAccount(row) : undefined;
  }

  async createPasswordResetToken(accountId: string, resetToken: string, expiresAt: Date): Promise<void> {
    const tokenHash = hashResetToken(resetToken);

    await this.pool.query(
      `
        INSERT INTO password_reset_tokens (account_id, token_hash, expires_at)
        VALUES ($1, $2, $3)
      `,
      [accountId, tokenHash, expiresAt]
    );
  }

  async consumePasswordResetToken(resetToken: string): Promise<string | undefined> {
    const tokenHash = hashResetToken(resetToken);

    const result = await this.pool.query<{ account_id: string }>(
      `
        UPDATE password_reset_tokens
        SET consumed_at = now()
        WHERE token_hash = $1
          AND consumed_at IS NULL
          AND expires_at > now()
        RETURNING account_id
      `,
      [tokenHash]
    );

    return result.rows[0]?.account_id;
  }

  async updatePassword(accountId: string, passwordHash: string): Promise<void> {
    await this.pool.query(
      `
        UPDATE accounts
        SET password_hash = $1, updated_at = now()
        WHERE id = $2
      `,
      [passwordHash, accountId]
    );
  }
}

function mapAccount(row: AccountRow): Account {
  return {
    id: row.id,
    email: row.email,
    passwordHash: row.password_hash,
    role: row.role,
    organizationId: row.organization_id ?? undefined,
    birthdate: row.birthdate ?? undefined,
    consentStatus: row.consent_status
  };
}

function hashResetToken(resetToken: string): string {
  return createHash("sha256").update(resetToken).digest("hex");
}
