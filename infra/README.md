# Local Infrastructure

The local stack provides the backing services required by wave 1:

- Postgres 16 with `pgvector`
- MinIO as the S3-compatible object store
- buckets for corpus SVG assets and cached TTS audio

Start it from the repo root:

```powershell
docker compose -f infra/docker-compose.yml up -d
```

Run API migrations:

```powershell
cd services/api
$env:DATABASE_URL = "postgres://postgres:postgres@localhost:5432/learning_platform"
corepack pnpm run migrate
```

MinIO console:

- URL: `http://localhost:9001`
- user: `minioadmin`
- password: `minioadmin`

Dev bucket names:

- `learning-corpus-assets`
- `learning-tts-audio`
