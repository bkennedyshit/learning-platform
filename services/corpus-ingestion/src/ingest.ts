import { createDatabase } from "../../api/src/db.js";
import { loadProviderConfig, createLLMProviderAdapter } from "@learning-platform/llm-adapter";
import { createLocalObjectStorageClient } from "@learning-platform/object-storage";
import { ingestCorpus } from "./pipeline.js";
import path from "path";
import { fileURLToPath } from "url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const corpusDir = path.resolve(__dirname, "../../../corpus");

async function main() {
  process.env.LLM_PROVIDER = "stub"; // Default to stub for fast local ingestion
  
  const db = createDatabase(process.env.DATABASE_URL || "postgres://postgres:postgres@localhost:5432/learning_platform");
  const config = loadProviderConfig();
  const adapter = createLLMProviderAdapter(config);
  
  const storage = createLocalObjectStorageClient({
    rootDir: path.resolve(__dirname, "../../../storage"),
    publicBaseUrl: "http://localhost:3000"
  });

  console.log("Starting ingestion from", corpusDir);
  const manifest = await ingestCorpus({
    db: db.pool as any, // Pool proxy type
    adapter,
    storage,
    corpusDir
  });

  console.log(`Successfully ingested ${manifest.length} lessons into the database.`);
  await db.close();
}

main().catch((err) => {
  console.error("Ingestion failed:", err);
  process.exit(1);
});
