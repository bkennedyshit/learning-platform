import { readdir, readFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";
import type { PoolClient } from "pg";
import { createDatabase } from "./db.js";
import { loadApiConfig } from "./config.js";

const currentFile = fileURLToPath(import.meta.url);
const currentDir = path.dirname(currentFile);
const migrationsDir = path.resolve(currentDir, "../migrations");

interface MigrationRecord {
  name: string;
}

async function ensureMigrationTable(client: PoolClient): Promise<void> {
  await client.query(`
    CREATE TABLE IF NOT EXISTS schema_migrations (
      name text PRIMARY KEY,
      applied_at timestamptz NOT NULL DEFAULT now()
    )
  `);
}

async function getAppliedMigrations(client: PoolClient): Promise<Set<string>> {
  const result = await client.query<MigrationRecord>("SELECT name FROM schema_migrations");
  return new Set(result.rows.map((row) => row.name));
}

async function applyMigration(client: PoolClient, fileName: string): Promise<void> {
  const sql = await readFile(path.join(migrationsDir, fileName), "utf8");

  await client.query("BEGIN");
  try {
    await client.query(sql);
    await client.query("INSERT INTO schema_migrations (name) VALUES ($1)", [fileName]);
    await client.query("COMMIT");
  } catch (error) {
    await client.query("ROLLBACK");
    throw error;
  }
}

export async function runMigrations(): Promise<string[]> {
  const config = loadApiConfig();
  const database = createDatabase(config.databaseUrl, config.databaseReplicaUrl);
  const client = await database.pool.connect();

  try {
    await ensureMigrationTable(client);
    const applied = await getAppliedMigrations(client);
    const files = (await readdir(migrationsDir))
      .filter((fileName) => fileName.endsWith(".sql"))
      .sort();

    const appliedNow: string[] = [];

    for (const fileName of files) {
      if (applied.has(fileName)) {
        continue;
      }

      await applyMigration(client, fileName);
      appliedNow.push(fileName);
    }

    return appliedNow;
  } finally {
    client.release();
    await database.close();
  }
}

if (import.meta.url === `file://${process.argv[1]}`) {
  runMigrations()
    .then((applied) => {
      if (applied.length === 0) {
        console.log("No migrations to apply.");
        return;
      }

      console.log(`Applied migrations: ${applied.join(", ")}`);
    })
    .catch((error: unknown) => {
      console.error(error);
      process.exitCode = 1;
    });
}
