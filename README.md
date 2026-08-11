# Learning Platform

A self-hostable learning platform built around inspectable lessons, deliberate practice, and a provider-neutral AI tutor. The public catalog is generated from Markdown curriculum, and the learner app supports a Read -> Listen -> Write -> Code -> Handwrite loop.

The project is designed to run locally with Ollama. A hosted model is optional, not required.

## Try It Locally

Requirements: Node.js 20+, pnpm 9+, and Ollama if you want the AI tutor.

```powershell
git clone https://github.com/bkennedyshit/learning-platform.git
cd learning-platform
pnpm install
ollama pull llama3.2:3b
Copy-Item apps/learning-app/.env.local.example apps/learning-app/.env.local
$env:TUTOR_PROVIDER = "local"
pnpm --filter @learning-platform/learning-app dev
```

Open `http://localhost:3000`. The tutor will call Ollama at `http://localhost:11434` and will not use a paid API.

To use a hosted OpenAI-compatible provider instead, set `TUTOR_PROVIDER=hosted`, `LLM_BASE_URL`, `LLM_API_KEY`, and `LLM_COMPLETION_MODEL` in the app environment. Never put a provider key in client-side code or commit it to Git.

The public, static catalog can be run separately:

```powershell
pnpm --filter @learning-platform/content-site dev
```

## Workspace Layout

- `apps/learning-app` - interactive learner experience and grounded tutor.
- `apps/content-site` - public, SEO-friendly lesson catalog.
- `apps/educator-console` - educator/admin surface under development.
- `apps/spatial-calculator` - interactive math tools.
- `services/api` - domain services for accounts, progress, RAG, practice, and tutoring.
- `services/problem-generator` - Python/SymPy practice-problem sidecar.
- `packages/llm-adapter` - provider-neutral completion and embedding interface.
- `corpus` - Markdown curriculum and source material.

## Project Status

The catalog and learner UI are usable locally. Persistent accounts, progress, spaced repetition, and database-backed RAG are present as platform work but are not yet the default local quickstart. See [docs/self-hosting.md](docs/self-hosting.md) for the boundary between the demo path and the full stack.

## Licensing

Source code is released under the MIT License. Curriculum, source material, brand assets, and third-party material are governed separately; see [CONTENT-LICENSE.md](CONTENT-LICENSE.md) before redistributing the corpus.

Contributions are welcome. Read [CONTRIBUTING.md](CONTRIBUTING.md) and [SECURITY.md](SECURITY.md) first.
