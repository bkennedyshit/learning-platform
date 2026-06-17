---
title: "08.9 — Docker & Containers"
subject: "Python"
catalog: advanced
audience_tier: higher-education
chapter: "8.9"
type: chapter
objectives:
  - "Understand the concepts"
  - "Apply the theory"
open_source: true
---

*Back to [Subject_Plan](Subject_Plan) | Part of [09 - Learning Index](09---Learning-Index)*

# 08.9 — Docker & Containers

> *"It works on my machine. Then we'll ship your machine."* — The problem Docker solves

Containers solve the "works on my machine" problem by packaging your application with its entire runtime environment. For ML/AI work, this means reproducible training environments, consistent inference deployments, and portable GPU pipelines.

---

## 🎯 Learning Objectives

By the end of this chapter you will be able to:

1. Explain container isolation (namespaces, cgroups) vs. virtual machines.
2. Write production-grade Dockerfiles for Python applications.
3. Use multi-stage builds to minimize image size.
4. Manage volumes, networks, and docker-compose for multi-service apps.
5. Build GPU-enabled containers for ML training (NVIDIA Container Toolkit).
6. Implement CI/CD pipelines that build and push container images.

---

## 🖼️ Visual Anchor — Docker Image Layers & Container Lifecycle

![python__1.9-fig1](python__1.9-fig1.svg)

---

## 📚 1. Definitions / Concepts

### Definition 08.9.1 — Container vs. Virtual Machine

| Aspect | Container | VM |
|--------|-----------|-----|
| Isolation | Process-level (namespaces) | Hardware-level (hypervisor) |
| Overhead | ~MB, starts in ms | ~GB, starts in seconds |
| Kernel | Shares host kernel | Own kernel |
| Use case | App packaging, microservices | Full OS isolation, legacy apps |

### Definition 08.9.2 — Image Layers

A Docker image is a stack of read-only filesystem layers. Each Dockerfile instruction creates a new layer. Layers are cached and shared between images — changing only your source code rebuilds only the top layers.

### Definition 08.9.3 — Container Runtime

The container is a running instance of an image with a thin read-write layer on top. When the container stops, the R/W layer is discarded (unless you use volumes).

---

## 📐 2. Mental Models / Principles

### Principle 1.9.1 — Layer Ordering for Cache Efficiency

Put things that change **least frequently** at the bottom:
1. Base image (changes rarely)
2. System dependencies (changes occasionally)
3. Python dependencies (changes when you add packages)
4. Source code (changes every commit)

### Principle 1.9.2 — One Process Per Container

Each container should run one process. Don't put your web server, database, and cache in one container. Use `docker-compose` to orchestrate multiple containers.

---

## 🔑 3. Mechanics

### 3.1 — Production Python Dockerfile

```dockerfile
# Stage 1: Build dependencies
FROM python:3.12-slim AS builder
WORKDIR /app
RUN pip install --no-cache-dir uv
COPY pyproject.toml uv.lock ./
RUN uv pip install --system --no-cache -r pyproject.toml

# Stage 2: Runtime (minimal)
FROM python:3.12-slim AS runtime
WORKDIR /app

# Security: non-root user
RUN useradd --create-home appuser
USER appuser

# Copy installed packages from builder
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy source
COPY src/ ./src/

# Health check
HEALTHCHECK --interval=30s --timeout=3s \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"

EXPOSE 8000
CMD ["python", "-m", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 3.2 — docker-compose for Development

```yaml
# docker-compose.yml
services:
  app:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - ./src:/app/src  # Hot reload in dev
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/mydb
    depends_on:
      db:
        condition: service_healthy

  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
      POSTGRES_DB: mydb
    volumes:
      - pgdata:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U user"]
      interval: 5s

volumes:
  pgdata:
```

### 3.3 — GPU Containers for ML

```dockerfile
FROM nvidia/cuda:12.4-runtime-ubuntu22.04
RUN apt-get update && apt-get install -y python3.12 python3-pip
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python3", "train.py"]
```

```bash
# Run with GPU access
docker run --gpus all -v ./data:/data my-training-image
```

---

## ✍️ 4. Derivations & Worked Examples

### Example 08.9.1 — Multi-Stage Build Reducing Image Size

<details>
<summary>🔍 View Step-by-Step Solution</summary>

```bash
# Naive approach: 08.2 GB
FROM python:3.12
COPY . .
RUN pip install .

# Multi-stage: 180 MB
FROM python:3.12-slim AS builder
COPY pyproject.toml .
RUN pip install --target=/deps .

FROM python:3.12-slim
COPY --from=builder /deps /usr/local/lib/python3.12/site-packages
COPY src/ ./src/
CMD ["python", "-m", "src.main"]
```

The slim base is ~120MB vs ~900MB for the full image. Multi-stage discards build tools (gcc, headers) from the final image.

</details>

---

## 💻 5. Code Patterns & Idioms

### Pattern 1.9.1 — .dockerignore

```
.git
.venv
__pycache__
*.pyc
.env
.mypy_cache
.pytest_cache
node_modules
```

---

## ⚠️ 6. Gotchas & Anti-Patterns

### Gotcha 1.9.1 — Running as Root

Default Docker containers run as root. Always add `USER nonroot` for security.

### Gotcha 1.9.2 — Secrets in Image Layers

`ENV SECRET_KEY=abc123` is visible in image history. Use Docker secrets or runtime environment variables instead.

---

## 🧮 7. Hands-On Lab

```bash
python _practice/scripts/1.9_docker.py --out _practice/1.9_lab_report.md
```

Checks Docker installation, builds a sample image, and validates GPU runtime availability.

---

## 🔗 8. Cross-links & Further Reading

- Previous: [08.8 - Git & Version Control](08.8---Git-&-Version-Control)
- Next: [08.10 - Operating Systems Essentials](08.10---Operating-Systems-Essentials)
- Distributed training containers: [08.16 - Distributed Systems & Multi-GPU Training](08.16---Distributed-Systems-&-Multi-GPU-Training)
- [Docker docs: Get Started](https://docs.docker.com/get-started/)
- [Docker Deep Dive (Nigel Poulton)](https://www.amazon.com/Docker-Deep-Dive-Nigel-Poulton/dp/1916585256)



---

## 🧠 9. Extended Worked Examples & Deep Dives

### Example 9.1 — Multi-Stage Builds for Slim Python Images

**Problem:** Your Python application's Docker image is 08.2 GB. Reduce it to under 150 MB using multi-stage builds while maintaining debuggability and fast CI builds via layer caching.

<details>
<summary>🔍 Full step-by-step solution</summary>

#### Step 1: The Bloated Single-Stage Image (Anti-Pattern)

```dockerfile
# BAD: Single stage, everything included
FROM python:3.11
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0"]

# Result: ~08.2 GB
# Includes: gcc, build headers, pip cache, .git, tests, docs, __pycache__
```

#### Step 2: Multi-Stage Build (Production-Optimized)

```dockerfile
# === Stage 1: Builder (install dependencies) ===
FROM python:3.11-slim AS builder

# Install build dependencies (needed for compiled packages like numpy, psycopg2)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install uv for fast dependency resolution
COPY --from=ghcr.io/astral-sh/uv:0.5 /uv /usr/local/bin/uv

WORKDIR /app

# Copy dependency files first (cache layer — only rebuilds when deps change)
COPY pyproject.toml uv.lock ./

# Install dependencies into a virtual environment
RUN uv sync --frozen --no-install-project --no-dev

# Copy source code (separate layer — rebuilds on code changes)
COPY src/ src/

# Install the project itself
RUN uv sync --frozen --no-dev


# === Stage 2: Runtime (minimal) ===
FROM python:3.11-slim AS runtime

# Install only runtime system dependencies (no gcc, no build tools)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN useradd --create-home --shell /bin/bash appuser

WORKDIR /app

# Copy ONLY the virtual environment from builder (not source, not build tools)
COPY --from=builder /app/.venv /app/.venv

# Copy application source
COPY --from=builder /app/src /app/src

# Set environment
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Switch to non-root user
USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### Step 3: Size Comparison

```bash
# Build and compare:
docker build -t app:slim .
docker images app

# REPOSITORY   TAG    SIZE
# app          slim   142 MB   ← Multi-stage (python:3.11-slim base = 120MB)
# app          fat    08.2 GB   ← Single-stage

# Further reduction with distroless (no shell, no package manager):
# FROM gcr.io/distroless/python3-debian12 AS runtime
# Size: ~85 MB (but no shell for debugging)
```

#### Step 4: Layer Caching Strategy

```dockerfile
# Layer cache hierarchy (top = changes least, bottom = changes most):
#
# Layer 1: Base image (python:3.11-slim)     — changes: monthly
# Layer 2: System packages (apt-get)          — changes: rarely
# Layer 3: pyproject.toml + uv.lock           — changes: when deps change
# Layer 4: uv sync (install deps)             — changes: when deps change
# Layer 5: COPY src/                          — changes: every commit
# Layer 6: uv sync --no-deps (install project)— changes: every commit
#
# Key insight: Layers 1-4 are cached on most builds.
# Only layers 5-6 rebuild when you change code.
# This makes builds take ~5 seconds instead of ~60 seconds.
```

#### Step 5: Debug Stage (Optional Third Stage)

```dockerfile
# === Stage 3: Debug (for development/troubleshooting) ===
FROM runtime AS debug

USER root

# Add debugging tools
RUN apt-get update && apt-get install -y --no-install-recommends \
    vim \
    strace \
    net-tools \
    procps \
    && rm -rf /var/lib/apt/lists/*

# Install dev dependencies
COPY --from=builder /app/.venv /app/.venv
# Could re-run uv sync with dev deps here

USER appuser
CMD ["bash"]
```

```bash
# Build specific stage:
docker build --target runtime -t app:prod .   # 142 MB
docker build --target debug -t app:debug .    # 180 MB

# Use debug image for troubleshooting:
docker run -it app:debug bash
```

**Final Answer:**

```dockerfile
# Multi-stage build checklist:
# 1. Builder stage: install build deps + compile packages
# 2. Runtime stage: copy only .venv + source (no build tools)
# 3. Order COPY commands: least-changing first (cache optimization)
# 4. Use .dockerignore to exclude .git, __pycache__, tests, docs
# 5. Non-root user in runtime stage (security)
# 6. HEALTHCHECK for orchestrator integration
# 7. Optional debug stage for troubleshooting
```

</details>

### Example 9.2 — BuildKit Cache Mounts: Eliminating Redundant Downloads

**Problem:** Every Docker build re-downloads pip packages and apt packages from scratch, even when nothing changed. Use BuildKit cache mounts to persist these caches across builds.

<details>
<summary>🔍 Full step-by-step solution</summary>

#### Step 1: Understanding Cache Mounts

```dockerfile
# syntax=docker/dockerfile:1
# ↑ Required for BuildKit features

# Cache mounts create a persistent directory that survives between builds.
# Unlike layer caching (which invalidates on ANY change above), cache mounts
# persist independently. They're like a local package mirror.

# Enable BuildKit:
# export DOCKER_BUILDKIT=1
# Or in docker daemon.json: {"features": {"buildkit": true}}
```

#### Step 2: Caching apt Downloads

```dockerfile
# syntax=docker/dockerfile:1
FROM python:3.11-slim AS builder

# Cache apt downloads — survives between builds
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt,sharing=locked \
    apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev

# Without cache mount: downloads ~50MB of .deb files every build
# With cache mount: downloads only NEW/UPDATED packages (usually 0)
```

#### Step 3: Caching pip/uv Downloads

```dockerfile
# Cache pip downloads
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -r requirements.txt

# Cache uv downloads (even faster)
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

# Without cache: downloads all wheels from PyPI every build (~200MB for ML projects)
# With cache: only downloads packages not already in cache (usually 0)
```

#### Step 4: Complete Optimized Dockerfile

```dockerfile
# syntax=docker/dockerfile:1
FROM python:3.11-slim AS builder

# System deps with apt cache
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt,sharing=locked \
    apt-get update && apt-get install -y --no-install-recommends \
    gcc libpq-dev

COPY --from=ghcr.io/astral-sh/uv:0.5 /uv /usr/local/bin/uv
WORKDIR /app
COPY pyproject.toml uv.lock ./

# Python deps with uv cache
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project --no-dev

COPY src/ src/
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

# Runtime stage
FROM python:3.11-slim AS runtime
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt,sharing=locked \
    apt-get update && apt-get install -y --no-install-recommends libpq5 curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY --from=builder /app/.venv /app/.venv
COPY --from=builder /app/src /app/src
ENV PATH="/app/.venv/bin:$PATH"
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0"]
```

#### Step 5: Build Time Comparison

```bash
# First build (cold cache):
# Without cache mounts: 90s (download everything)
# With cache mounts: 90s (same — cache is empty)

# Second build (deps unchanged, code changed):
# Without cache mounts: 45s (re-download all pip packages due to layer invalidation)
# With cache mounts: 8s (pip packages cached, only copies new source)

# Third build (one new dependency added):
# Without cache mounts: 45s (re-download ALL packages)
# With cache mounts: 12s (download only the new package, rest cached)
```

**Final Answer:**

```dockerfile
# Cache mount types:
# --mount=type=cache,target=/path    Persistent cache directory
# --mount=type=bind,source=./file    Bind file without COPY (no layer)
# --mount=type=secret,id=key         Inject secrets without layer storage
# --mount=type=ssh                   Forward SSH agent for private repos
#
# Key targets to cache:
# /var/cache/apt          — apt package downloads
# /root/.cache/pip        — pip wheel downloads
# /root/.cache/uv         — uv package downloads
# /root/.npm              — npm package cache
# /root/.cargo/registry   — Rust crate downloads
```

</details>

### Example 9.3 — docker-compose.yml: Full Development Stack

**Problem:** Create a complete `docker-compose.yml` for a Python web application with: API server, Celery worker, PostgreSQL, Redis, and Nginx reverse proxy. Include health checks, volume mounts for development, and production overrides.

<details>
<summary>🔍 Full step-by-step solution</summary>

#### Step 1: Development Compose File

```bash
# docker-compose.yml (development)
# version: "3.9"  # Deprecated in Compose V2, but harmless

services:
  # === Application Services ===
  api:
    build:
      context: .
      dockerfile: Dockerfile
      target: runtime  # Use runtime stage from multi-stage build
    ports:
      - "8000:8000"
    volumes:
      - ./src:/app/src:cached  # Live reload — code changes reflected immediately
    environment:
      - DATABASE_URL=postgresql://app:secret@postgres:5432/appdb
      - REDIS_URL=redis://redis:6379/0
      - ENV=development
      - DEBUG=1
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 10s
      timeout: 5s
      retries: 3
      start_period: 10s
    restart: unless-stopped

  worker:
    build:
      context: .
      target: runtime
    command: celery -A app.worker worker --loglevel=info --concurrency=2
    volumes:
      - ./src:/app/src:cached
    environment:
      - DATABASE_URL=postgresql://app:secret@postgres:5432/appdb
      - REDIS_URL=redis://redis:6379/0
      - ENV=development
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    restart: unless-stopped

  # === Infrastructure Services ===
  postgres:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: app
      POSTGRES_PASSWORD: secret
      POSTGRES_DB: appdb
    ports:
      - "5432:5432"  # Expose for local tools (pgAdmin, DBeaver)
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./scripts/init.sql:/docker-entrypoint-initdb.d/init.sql
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U app -d appdb"]
      interval: 5s
      timeout: 3s
      retries: 5

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 5s
      timeout: 3s
      retries: 5
    command: redis-server --maxmemory 256mb --maxmemory-policy allkeys-lru

  # === Reverse Proxy ===
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx/dev.conf:/etc/nginx/conf.d/default.conf:ro
    depends_on:
      api:
        condition: service_healthy

volumes:
  postgres_data:
  redis_data:
```

#### Step 2: Production Override

```bash
# docker-compose.prod.yml (production overrides)
# Usage: docker compose -f docker-compose.yml -f docker-compose.prod.yml up

services:
  api:
    build:
      target: runtime  # Same stage, but no volume mounts
    volumes: []  # Remove dev volume mounts
    environment:
      - ENV=production
      - DEBUG=0
    deploy:
      replicas: 3
      resources:
        limits:
          cpus: "08.0"
          memory: 512M

  worker:
    volumes: []
    environment:
      - ENV=production
    command: celery -A app.worker worker --loglevel=warning --concurrency=4
    deploy:
      replicas: 2
      resources:
        limits:
          cpus: "2.0"
          memory: 1G

  postgres:
    ports: []  # Don't expose in production
    environment:
      POSTGRES_PASSWORD_FILE: /run/secrets/db_password
    secrets:
      - db_password

  redis:
    ports: []  # Don't expose in production

  nginx:
    volumes:
      - ./nginx/prod.conf:/etc/nginx/conf.d/default.conf:ro
      - /etc/letsencrypt:/etc/letsencrypt:ro
    ports:
      - "80:80"
      - "443:443"

secrets:
  db_password:
    file: ./secrets/db_password.txt
```

#### Step 3: Common Commands

```bash
# Development workflow:
docker compose up -d              # Start all services (detached)
docker compose logs -f api        # Follow API logs
docker compose exec api bash      # Shell into running container
docker compose down               # Stop and remove containers
docker compose down -v            # Also remove volumes (reset data)

# Production:
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d
docker compose -f docker-compose.yml -f docker-compose.prod.yml ps
```

**Final Answer:**

```bash
# docker-compose.yml best practices:
# 1. Use depends_on with condition: service_healthy (not just "started")
# 2. Named volumes for persistent data (postgres, redis)
# 3. Bind mounts for development (live reload)
# 4. Health checks on every service
# 5. Production overrides in separate file (no dev volumes, no exposed ports)
# 6. Secrets for sensitive values (not environment variables in prod)
# 7. Resource limits in production (prevent OOM)
```

</details>

---

## 📘 10. Appendix: Extended Derivations & Special Cases

### 10.1 The OCI Image Specification — What a Container Image Actually Is

A Docker/container image is not a VM disk. It's a layered filesystem defined by the Open Container Initiative (OCI) Image Specification. Understanding this explains why images are fast to build, share, and deploy.

**The Three Components:**

1. **Image Manifest** (`application/vnd.oci.image.manifest.v1+json`):
   Points to the config and all layers. This is what a registry stores.

```python
# Conceptual manifest structure:
manifest = {
    "schemaVersion": 2,
    "mediaType": "application/vnd.oci.image.manifest.v1+json",
    "config": {
        "mediaType": "application/vnd.oci.image.config.v1+json",
        "digest": "sha256:abc123...",  # Points to config blob
        "size": 1234
    },
    "layers": [
        {
            "mediaType": "application/vnd.oci.image.layer.v1.tar+gzip",
            "digest": "sha256:def456...",  # Layer 1 (base OS)
            "size": 45_000_000
        },
        {
            "mediaType": "application/vnd.oci.image.layer.v1.tar+gzip",
            "digest": "sha256:ghi789...",  # Layer 2 (apt packages)
            "size": 12_000_000
        },
        # ... more layers
    ]
}
```

2. **Image Config** (`application/vnd.oci.image.config.v1+json`):
   Contains: architecture, OS, environment variables, entrypoint, CMD, exposed ports, labels, and the ordered list of layer diff IDs.

3. **Layers** (tar+gzip archives):
   Each layer is a filesystem diff — files added, modified, or deleted relative to the layer below. Layers are content-addressable (identified by SHA-256 of their content).

**Why Layers Enable Sharing:**

```bash
# Image A: python:3.11-slim (3 layers)
# Layer 1: debian:bookworm-slim base (80 MB)
# Layer 2: Python runtime (40 MB)
# Layer 3: pip + setuptools (5 MB)

# Image B: your-app (5 layers)
# Layer 1: debian:bookworm-slim base (80 MB)  ← SHARED with Image A
# Layer 2: Python runtime (40 MB)             ← SHARED with Image A
# Layer 3: pip + setuptools (5 MB)            ← SHARED with Image A
# Layer 4: your dependencies (50 MB)          ← unique
# Layer 5: your source code (2 MB)            ← unique

# Disk usage: 80 + 40 + 5 + 50 + 2 = 177 MB (not 80+40+5 + 80+40+5+50+2 = 302 MB)
# Shared layers are stored ONCE on disk, referenced by both images.
```

**The Union Filesystem:**

At runtime, all layers are stacked using a union filesystem (OverlayFS on Linux). The container sees a single merged filesystem. Writes go to a thin read-write layer on top (copy-on-write semantics).

### 10.2 Container Networking Modes

Docker provides several networking modes that control how containers communicate with each other and the host.

**Bridge (Default):**

```bash
# Each container gets its own network namespace with a virtual ethernet interface.
# Containers on the same bridge network can communicate via container name (DNS).
# Host access via published ports (-p 8080:80).

docker network create my-net
docker run --network my-net --name api my-api
docker run --network my-net --name db postgres
# api can reach db at: postgres://db:5432 (Docker DNS resolves "db")
```

**Host:**

```bash
# Container shares the host's network namespace directly.
# No port mapping needed — container binds directly to host ports.
# Maximum performance (no NAT overhead) but no isolation.

docker run --network host my-api
# API is directly accessible at host:8000 (no -p flag needed)
# DANGER: container can bind to any host port, see all host traffic
```

**None:**

```bash
# Container has no network access at all.
# Use for: batch processing, security-sensitive computation.

docker run --network none my-batch-job
```

**Overlay (Swarm/Multi-Host):**

```bash
# Spans multiple Docker hosts. Uses VXLAN tunneling.
# Containers on different physical machines can communicate as if on same LAN.
# Used by Docker Swarm and can be used with Kubernetes.

docker network create --driver overlay --attachable my-overlay
```

**Performance Comparison:**

| Mode | Latency Overhead | Throughput | Isolation | Use Case |
|------|-----------------|------------|-----------|----------|
| Host | 0 (native) | 100% | None | High-performance, single-tenant |
| Bridge | ~50μs | ~95% | Container-level | Default, multi-container apps |
| Overlay | ~200μs | ~85% | Cross-host | Distributed systems |
| Macvlan | ~10μs | ~99% | VLAN-level | Legacy apps needing real IPs |

---



### 10.3 .dockerignore — The Most Overlooked Optimization

A `.dockerignore` file prevents unnecessary files from being sent to the Docker daemon as build context. Without it, Docker sends your entire project directory (including `.git`, `node_modules`, `__pycache__`, test data) to the daemon — even if no `COPY` instruction uses them.

**Impact:**

```bash
# Without .dockerignore:
# Sending build context to Docker daemon  2.3GB  ← includes .git, data/, venv/
# Build time: 45 seconds (just to send context!)

# With .dockerignore:
# Sending build context to Docker daemon  15MB   ← only source + config
# Build time: 2 seconds to send context
```

**Recommended .dockerignore for Python projects:**

```bash
# .dockerignore

# Version control
.git
.gitignore

# Python
__pycache__
*.pyc
*.pyo
*.egg-info
.eggs
dist/
build/
*.egg

# Virtual environments
.venv
venv
env

# IDE
.vscode
.idea
*.swp
*.swo

# Testing & CI
.pytest_cache
.coverage
htmlcov/
.mypy_cache
.ruff_cache

# Documentation
docs/
*.md
!README.md

# Data & models (large files)
data/
models/
*.h5
*.pkl
*.parquet

# Docker (prevent recursive context)
Dockerfile*
docker-compose*
.dockerignore

# OS
.DS_Store
Thumbs.db
```

**Key Rules:**

1. `.dockerignore` uses the same syntax as `.gitignore` (glob patterns)
2. It's evaluated relative to the build context root (the path you pass to `docker build`)
3. `!` prefix negates a pattern (include something previously excluded)
4. Order matters: later rules override earlier ones
5. Always exclude `.git` — it's often the largest directory and never needed in images

**The Security Angle:**

Without `.dockerignore`, sensitive files can accidentally end up in image layers:
- `.env` files with secrets
- `.git/config` with credentials
- SSH keys in `~/.ssh/`
- AWS credentials

Even if you don't `COPY` them explicitly, they're in the build context and could be accessed by malicious build steps or leaked through layer inspection.

---



### 10.4 Container Security Best Practices for Python Applications

Running containers securely requires more than just packaging your app. These practices prevent common attack vectors.

**Principle of Least Privilege:**

```dockerfile
# 1. Run as non-root user
FROM python:3.11-slim
RUN useradd --create-home --shell /bin/bash appuser
WORKDIR /home/appuser/app
COPY --chown=appuser:appuser . .
USER appuser
# Container processes run as appuser, not root
# Even if attacker gets shell, they can't modify system files

# 2. Read-only filesystem
# docker run --read-only --tmpfs /tmp my-app
# Prevents attackers from writing malware to the filesystem

# 3. Drop all capabilities, add only what's needed
# docker run --cap-drop=ALL --cap-add=NET_BIND_SERVICE my-app

# 4. No new privileges (prevent setuid escalation)
# docker run --security-opt=no-new-privileges my-app
```

**Image Scanning and Supply Chain:**

```bash
# Scan for known vulnerabilities (CVEs):
docker scout cves my-app:latest
# Or: trivy image my-app:latest
# Or: grype my-app:latest

# Pin base image digests (not just tags — tags are mutable!):
# BAD: FROM python:3.11-slim  (tag can be overwritten)
# GOOD: FROM python:3.11-slim@sha256:abc123...  (immutable digest)

# Verify image provenance:
# Use Docker Content Trust (DCT) or cosign for image signing
# DOCKER_CONTENT_TRUST=1 docker pull python:3.11-slim
```

**Secrets Management:**

```dockerfile
# NEVER put secrets in environment variables in Dockerfile:
# BAD: ENV DATABASE_PASSWORD=secret123  ← visible in image layers!

# GOOD: Use Docker secrets (Swarm) or mount at runtime:
# docker run -v /path/to/secrets:/run/secrets:ro my-app

# GOOD: Use BuildKit secrets for build-time secrets:
# syntax=docker/dockerfile:1
RUN --mount=type=secret,id=pip_token \
    PIP_INDEX_URL="https://$(cat /run/secrets/pip_token)@pypi.private.com/simple" \
    pip install private-package
# Secret is never stored in any image layer
```

**Network Isolation:**

```bash
# Create isolated networks for service groups:
docker network create --internal backend  # No internet access
docker network create frontend            # Internet access

# API container: connected to both (receives requests, talks to DB)
# Database container: connected to backend only (no internet)
# This prevents a compromised DB container from exfiltrating data

docker run --network backend postgres
docker run --network frontend --network backend my-api
```

**Runtime Monitoring:**

```python
# Health checks detect compromised containers:
# HEALTHCHECK --interval=30s --timeout=5s \
#     CMD python -c "import requests; requests.get('http://localhost:8000/health').raise_for_status()"

# Resource limits prevent crypto-mining:
# docker run --memory=512m --cpus=08.0 my-app
# Container is killed if it exceeds memory limit (OOMKilled)
# CPU is throttled (not killed) if it exceeds CPU limit
```

**The Security Checklist:**

| Practice | Risk Mitigated |
|----------|---------------|
| Non-root user | Privilege escalation |
| Read-only filesystem | Malware persistence |
| Minimal base image (distroless) | Reduced attack surface |
| Image scanning | Known vulnerabilities |
| Pinned digests | Supply chain attacks |
| No secrets in layers | Credential exposure |
| Network isolation | Lateral movement |
| Resource limits | Resource abuse (mining) |
| Health checks | Detect compromised state |

---
