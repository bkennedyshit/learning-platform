import assert from "node:assert/strict";
import test from "node:test";
import { assertOwnsResource } from "./authorization.js";
import { AuthorizationDeniedError } from "./errors.js";
import { hashPassword, verifyPassword } from "./password.js";
import { createSessionEndpoint } from "./sessionEndpoint.js";
import { createSessionSigner } from "./session.js";
import { AuthService } from "./service.js";
import { InvalidTokenError } from "./errors.js";
import type { AuthRepository } from "./repository.js";

const sessionSecret = "0123456789abcdef0123456789abcdef";

test("password hashes verify only the original password", async () => {
  const hash = await hashPassword("correct horse battery staple");

  assert.equal(await verifyPassword(hash, "correct horse battery staple"), true);
  assert.equal(await verifyPassword(hash, "wrong password"), false);
});

test("session signer round-trips a principal and rejects tampered tokens", () => {
  const signer = createSessionSigner(sessionSecret);
  const token = signer.sign({
    accountId: "learner-1",
    role: "b2c_learner"
  });

  assert.deepEqual(signer.verify(token), {
    accountId: "learner-1",
    role: "b2c_learner"
  });

  assert.equal(signer.verify(`${token}tampered`), undefined);
  assert.match(signer.toCookie(token), /HttpOnly/);
});

test("session signer rejects signed payloads with unknown roles", () => {
  const signer = createSessionSigner(sessionSecret);
  const token = signer.sign({
    accountId: "learner-1",
    role: "superuser"
  } as never);

  assert.equal(signer.verify(token), undefined);
});

test("session endpoint returns the current principal from the session cookie", () => {
  const signer = createSessionSigner(sessionSecret);
  const endpoint = createSessionEndpoint(signer);
  const token = signer.sign({
    accountId: "educator-1",
    role: "educator",
    organizationId: "org-1"
  });

  assert.deepEqual(
    endpoint.current({
      headers: {
        cookie: `theme=light; ${signer.toCookie(token)}`
      }
    }),
    {
      status: 200,
      body: {
        principal: {
          accountId: "educator-1",
          role: "educator",
          organizationId: "org-1"
        }
      }
    }
  );
});

test("session endpoint returns unauthenticated when the cookie is missing", () => {
  const endpoint = createSessionEndpoint(createSessionSigner(sessionSecret));

  assert.deepEqual(endpoint.current({ headers: {} }), {
    status: 401,
    body: { error: "Unauthenticated." }
  });
});

test("ownership authorization allows matching owner", async () => {
  await assert.doesNotReject(() =>
    assertOwnsResource(
      { accountId: "learner-1", role: "b2c_learner" },
      "progress-1",
      async () => "learner-1"
    )
  );
});

test("ownership authorization fails closed when ownership cannot be resolved", async () => {
  await assert.rejects(
    () =>
      assertOwnsResource(
        { accountId: "learner-1", role: "b2c_learner" },
        "progress-1",
        async () => undefined
      ),
    AuthorizationDeniedError
  );

  await assert.rejects(
    () =>
      assertOwnsResource(
        { accountId: "learner-1", role: "b2c_learner" },
        "progress-1",
        async () => {
          throw new Error("database unavailable");
        }
      ),
    AuthorizationDeniedError
  );
});

test("password reset flow generates token, consumes it, and updates password", async () => {
  let createdToken: string | undefined;
  let updatedPasswordHash: string | undefined;

  const mockRepo = {
    findAccountByEmail: async (email: string) => 
      email === "test@example.com" ? { id: "account-1", role: "b2c_learner" } : undefined,
    createPasswordResetToken: async (accountId: string, token: string, expiresAt: Date) => {
      createdToken = token;
    },
    consumePasswordResetToken: async (token: string) => {
      return token === createdToken ? "account-1" : undefined;
    },
    updatePassword: async (accountId: string, hash: string) => {
      updatedPasswordHash = hash;
    }
  } as unknown as AuthRepository;

  const service = new AuthService(mockRepo, createSessionSigner(sessionSecret));

  const req = await service.requestPasswordReset("test@example.com");
  assert.ok(req);
  assert.equal(req.resetToken, createdToken);

  await service.resetPassword(req.resetToken, "new-password");

  assert.ok(updatedPasswordHash);
  assert.equal(await verifyPassword(updatedPasswordHash, "new-password"), true);
});

test("password reset fails on invalid token", async () => {
  const mockRepo = {
    consumePasswordResetToken: async () => undefined
  } as unknown as AuthRepository;

  const service = new AuthService(mockRepo, createSessionSigner(sessionSecret));

  await assert.rejects(
    () => service.resetPassword("invalid-token", "new-password"),
    InvalidTokenError
  );
});
