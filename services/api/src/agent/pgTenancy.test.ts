import assert from "node:assert/strict";
import test from "node:test";
import { withAccountTransaction, type TenantPool, type TenantQueryClient } from "./pgTenancy.js";

function mockPool(): { pool: TenantPool; calls: Array<{ text: string; values?: unknown[] }>; released: () => boolean } {
  const calls: Array<{ text: string; values?: unknown[] }> = [];
  let released = false;
  const client: TenantQueryClient = {
    async query(text, values) {
      calls.push({ text, ...(values ? { values } : {}) });
      return { rows: [] };
    },
    release() {
      released = true;
    }
  };
  return {
    pool: { async connect() { return client; } },
    calls,
    released: () => released
  };
}

test("commits and binds the tenant via set_config for RLS", async () => {
  const { pool, calls, released } = mockPool();
  const result = await withAccountTransaction(pool, "acct-1", async (client) => {
    await client.query("SELECT 1");
    return "ok";
  });

  assert.equal(result, "ok");
  assert.equal(calls[0]?.text, "BEGIN");
  assert.equal(calls[1]?.text, "SELECT set_config($1, $2, true)");
  assert.deepEqual(calls[1]?.values, ["app.current_account_id", "acct-1"]);
  assert.equal(calls[2]?.text, "SELECT 1");
  assert.equal(calls[3]?.text, "COMMIT");
  assert.equal(released(), true);
});

test("rolls back and rethrows on error, still releasing the client", async () => {
  const { pool, calls, released } = mockPool();
  await assert.rejects(
    () =>
      withAccountTransaction(pool, "acct-1", async () => {
        throw new Error("boom");
      }),
    /boom/
  );
  assert.ok(calls.some((c) => c.text === "ROLLBACK"));
  assert.ok(!calls.some((c) => c.text === "COMMIT"));
  assert.equal(released(), true);
});
