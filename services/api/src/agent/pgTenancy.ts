/**
 * Production data-path helper. Executes learner work inside a single Postgres
 * transaction with a transaction-local `app.current_account_id` GUC so
 * row-level-security policies (migrations 0004/0005) scope every statement to
 * the acting account. `set_config(..., is_local => true)` is the parameterized,
 * injection-safe form of `SET LOCAL app.current_account_id`.
 *
 * The default quickstart uses file-backed memory; this helper is the seam the
 * production wiring uses once Postgres/pgvector is connected. It is dependency-
 * injected so it can be exercised with a mock client without a live database.
 */

export interface TenantQueryClient {
  query(text: string, values?: unknown[]): Promise<unknown>;
  release?(): void;
}

export interface TenantPool {
  connect(): Promise<TenantQueryClient>;
}

export interface WithAccountTransactionOptions {
  /** GUC name; defaults to the RLS-enforced `app.current_account_id`. */
  settingName?: string;
}

/**
 * Run `work` inside a transaction bound to `accountId`. Commits on success,
 * rolls back on any error, and always releases the client. The client passed to
 * `work` must be used for all tenant-scoped queries so RLS sees the GUC.
 */
export async function withAccountTransaction<T>(
  pool: TenantPool,
  accountId: string,
  work: (client: TenantQueryClient) => Promise<T>,
  options: WithAccountTransactionOptions = {}
): Promise<T> {
  const settingName = options.settingName ?? "app.current_account_id";
  const client = await pool.connect();
  try {
    await client.query("BEGIN");
    // Transaction-local (SET LOCAL) tenant binding, parameterized to prevent injection.
    await client.query("SELECT set_config($1, $2, true)", [settingName, accountId]);
    const result = await work(client);
    await client.query("COMMIT");
    return result;
  } catch (err) {
    try {
      await client.query("ROLLBACK");
    } catch {
      // Preserve the original error even if rollback fails.
    }
    throw err;
  } finally {
    client.release?.();
  }
}
