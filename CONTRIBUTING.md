# Contributing

Start with a focused issue or discussion for substantial changes. Small fixes, provider adapters, lesson corrections, tests, and self-hosting improvements are welcome.

Before opening a pull request:

1. Run `pnpm check` for TypeScript changes.
2. Run the relevant package tests, such as `pnpm --filter @learning-platform/content-site test`.
3. Do not commit `.env.local`, API keys, database dumps, private curriculum, or generated build output.
4. Keep curriculum and code licensing explicit. Do not copy third-party text or assets into the corpus without documenting permission.

Pull requests should explain what changed, how it was tested, and whether the change affects local Ollama, hosted providers, or the public catalog.
