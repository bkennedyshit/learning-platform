export interface ApiConfig {
  databaseUrl: string;
  databaseReplicaUrl: string;
}

export function loadApiConfig(env: NodeJS.ProcessEnv = process.env): ApiConfig {
  const databaseUrl = env.DATABASE_URL;

  if (!databaseUrl) {
    throw new Error("DATABASE_URL is required.");
  }

  const databaseReplicaUrl = env.DATABASE_REPLICA_URL || databaseUrl;

  return { databaseUrl, databaseReplicaUrl };
}
