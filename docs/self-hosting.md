# Self-Hosting Guide

There are two useful local modes.

## Quickstart: catalog plus local tutor

This is the lowest-cost path. It needs Node, pnpm, and Ollama. It does not require Postgres, MinIO, Gemini, OpenAI, or a hosted database.

```powershell
pnpm install
ollama pull llama3.2:3b
Copy-Item apps/learning-app/.env.local.example apps/learning-app/.env.local
$env:TUTOR_PROVIDER = "local"
pnpm --filter @learning-platform/learning-app dev
```

The Next.js route calls Ollama from the server at `OLLAMA_URL`. The browser never receives a model key. Use a larger model when the machine can support it by changing `OLLAMA_MODEL`.

## Full stack: persistence and retrieval

The repository also contains Postgres with pgvector, MinIO, migrations, ingestion, progress services, practice generation, and RAG orchestration. Start the local dependencies with:

```powershell
docker compose -f infra/docker-compose.yml up -d
```

Then follow [infra/README.md](../infra/README.md), [services/api/migrations/README.md](../services/api/migrations/README.md), and the ingestion scripts. This path is still under active development and should not be presented as a turnkey production deployment yet.

## Provider choices

The platform separates model access from tutoring logic:

- `local`: Ollama or another OpenAI-compatible local server.
- `hosted`: an OpenAI-compatible hosted endpoint configured by the operator.
- Gemini: supported by the learning app's current tutor route when `GEMINI_API_KEY` is present.

For a public deployment, each operator supplies their own provider and pays that provider directly. The project does not need to subsidize inference for every visitor.

## Download and distribution

GitHub is the canonical download surface. Visitors can use **Code -> Download ZIP** or clone the repository. A future release can add a tagged demo bundle after the curriculum licensing audit is complete.
