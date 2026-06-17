# Learning Platform

Monorepo scaffold for the Kiro `learning-platform` spec.

## Workspace Layout

- `apps/content-site` - public lesson site.
- `apps/learning-app` - signed-in learner SaaS.
- `apps/educator-console` - B2E admin surface.
- `apps/spatial-calculator` - separate WebXR calculator deployable.
- `services/api` - shared platform API.
- `services/problem-generator` - Python/SymPy sidecar.
- `packages/corpus-types` - shared catalog, lesson, path, and practice problem types.

## Current Scope

This initial pass implements the monorepo foundation and corpus type package from tasks 1.1 and 1.2 in `C:\Users\billk\projects\.kiro\specs\learning-platform\tasks.md`.

## Local Infrastructure

See [infra/README.md](infra/README.md) for the local Postgres + pgvector and MinIO stack.
