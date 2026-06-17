import { randomBytes } from "node:crypto";
import { EmailAlreadyRegisteredError, InvalidCredentialsError, InvalidTokenError } from "./errors.js";
import { hashPassword, verifyPassword } from "./password.js";
import type { AuthRepository } from "./repository.js";
import type { SessionSigner } from "./session.js";
import type { PasswordResetRequest, Principal, RegisterAccountInput, Session } from "./types.js";

export class AuthService {
  constructor(
    private readonly repository: AuthRepository,
    private readonly sessionSigner: SessionSigner
  ) {}

  async register(input: RegisterAccountInput): Promise<Session> {
    const existing = await this.repository.findAccountByEmail(input.email);
    if (existing) {
      throw new EmailAlreadyRegisteredError();
    }

    const account = await this.repository.createAccount(input, await hashPassword(input.password));
    return this.createSession(toPrincipal(account));
  }

  async login(email: string, password: string): Promise<Session> {
    const account = await this.repository.findAccountByEmail(email);

    if (!account || !(await verifyPassword(account.passwordHash, password))) {
      throw new InvalidCredentialsError();
    }

    return this.createSession(toPrincipal(account));
  }

  async requestPasswordReset(email: string): Promise<PasswordResetRequest | undefined> {
    const account = await this.repository.findAccountByEmail(email);
    if (!account) {
      return undefined;
    }

    const resetToken = randomBytes(32).toString("base64url");
    const expiresAt = new Date(Date.now() + 1000 * 60 * 60);
    await this.repository.createPasswordResetToken(account.id, resetToken, expiresAt);

    return { resetToken, expiresAt };
  }

  async resetPassword(resetToken: string, newPassword: string): Promise<void> {
    const accountId = await this.repository.consumePasswordResetToken(resetToken);
    if (!accountId) {
      throw new InvalidTokenError();
    }

    const passwordHash = await hashPassword(newPassword);
    await this.repository.updatePassword(accountId, passwordHash);
  }

  private createSession(principal: Principal): Session {
    const token = this.sessionSigner.sign(principal);
    return {
      token,
      cookie: this.sessionSigner.toCookie(token),
      principal
    };
  }
}

function toPrincipal(account: {
  id: string;
  role: Principal["role"];
  organizationId?: string;
}): Principal {
  return {
    accountId: account.id,
    role: account.role,
    organizationId: account.organizationId
  };
}
