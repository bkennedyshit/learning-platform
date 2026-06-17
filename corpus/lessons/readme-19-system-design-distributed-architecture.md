---
title: "README — 19 - System Design & Distributed Architecture"
subject: "System Design & Distributed Architecture"
catalog: advanced
audience_tier: higher-education
chapter: "Chapter 1"
type: subject-readme
objectives:
  - "Understand the concepts"
  - "Apply the theory"
open_source: true
---

# 19 - System Design & Distributed Architecture — Subject Hub

> One-page subject hub. Lists chapters, source reading materials, **video / picture references stored outside the repo (linked by URL)**, and placeholders for generated study aids.
> Master practice guide: [HOW_TO_USE_PRACTICE](HOW_TO_USE_PRACTICE).

> **Asset storage convention.**
> - **SVG diagrams** (small, theme-responsive, in-vault) → `../_svgs/sysdes__<chapter>-fig<n>.svg` and embedded inline via `![sysdes__27.x-figN](sysdes__27.x-figN.svg)`.
> - **Pictures, screenshots, videos, course recordings** are NOT committed to this repo. They live on YouTube, official docs, GitHub, or in your local "C:/Obsidian Vault/Bill's Vault/_assets/" sidecar (gitignored). Reference them by **URL** in this README and chapter notes.

---

## 🚀 Quick start

From a terminal in this folder:

```bash
cd "C:/Obsidian Vault/Bill's Vault/05-Knowledge_Foundation/09 - Learning/19 - System Design & Distributed Architecture"
# (Drill scripts to be added — k6 scripts, Saga simulator, latency-table flashcard generator)
python "_practice/scripts/<chapter>_<topic>.py" --count 8 --seed 42
```

---

## 📜 Chapter index

- [19.1 - System Design Fundamentals](19.1---System-Design-Fundamentals)
- [19.2 - Caching, CDNs & Edge](19.2---Caching,-CDNs-&-Edge)
- [19.3 - Databases at Scale](19.3---Databases-at-Scale)
- [19.4 - Message Queues & Event-Driven Architecture](19.4---Message-Queues-&-Event-Driven-Architecture)
- [19.5 - API Design](19.5---API-Design)
- [19.6 - Microservices & Service Mesh](19.6---Microservices-&-Service-Mesh)
- [19.7 - Real-Time Systems](19.7---Real-Time-Systems)
- [19.8 - Capacity Planning & Back-of-Envelope Math](19.8---Capacity-Planning-&-Back-of-Envelope-Math)

---

## 🎬 Video & Picture References (external — open in browser)

> These are the open-source / pro-grade media that supplement the chapter notes. Pictures and videos are **not** stored in this repo; they live on YouTube, official docs, GitHub, etc.

### 📺 Video Channels & Playlists

| Channel / Course | Track Use | Link |
|---|---|---|
| **MIT 6.824 — Distributed Systems lectures** | Raft, replication, consistency | [pdos.csail.mit.edu/6.824](https://pdos.csail.mit.edu/6.824/) |
| **CMU 15-445 / 15-721 — Database Systems** | Database internals, indexing, sharding | [15445.courses.cs.cmu.edu](https://15445.courses.cs.cmu.edu/) |
| **ByteByteGo (YouTube + newsletter)** | Visual explainers across the whole track | [@ByteByteGo](https://www.youtube.com/@ByteByteGo) |
| **Hussein Nasser** | Deep dives on Postgres, gRPC, HTTP/2/3 | [@hnasr](https://www.youtube.com/@hnasr) |
| **Gaurav Sen** | System design interview prep | [@gkcs](https://www.youtube.com/@gkcs) |
| **DesignGurus** | Pattern-first system design | [designgurus.io](https://designgurus.io/) |
| **Confluent Developer (Kafka)** | Free Kafka course | [developer.confluent.io](https://developer.confluent.io/) |
| **NATS Synadia channel** | Practical NATS / JetStream | [@SynadiaCommunications](https://www.youtube.com/@SynadiaCommunications) |
| **Discord Engineering YouTube** | Real-time at scale | [@DiscordEngineering](https://www.youtube.com/@DiscordEngineering) |
| **Stripe Sessions / Stripe Press** | API + scale lessons | [stripe.com/sessions](https://stripe.com/sessions) |

### 🖼️ Picture / Diagram Reference Sources

| Source | What it gives you | Link |
|---|---|---|
| **System Design Primer** | Diagrams + cheat sheets | [github.com/donnemartin/system-design-primer](https://github.com/donnemartin/system-design-primer) |
| **microservices.io** | Pattern catalog with diagrams | [microservices.io/patterns](https://microservices.io/patterns/) |
| **High Scalability case studies** | Real-world architecture decompositions | [highscalability.com](http://highscalability.com/) |
| **Netflix Tech Blog** | Production architecture posts | [netflixtechblog.com](https://netflixtechblog.com/) |
| **AWS Architecture Center** | Reference architectures | [aws.amazon.com/architecture](https://aws.amazon.com/architecture/) |
| **Latency numbers (jboner gist)** | The Rosetta Stone of "how slow" | [gist.github.com/jboner/2841832](https://gist.github.com/jboner/2841832) |

### 📚 Open-Source / Free Books

| Title | Author / Provider | Link |
|---|---|---|
| Designing Data-Intensive Applications (preview chapters) | Martin Kleppmann | [dataintensive.net](https://dataintensive.net/) |
| The Twelve-Factor App | Adam Wiggins / Heroku | [12factor.net](https://12factor.net/) |
| System Design Primer (CC-BY-SA 4.0) | Donne Martin | [github.com/donnemartin/system-design-primer](https://github.com/donnemartin/system-design-primer) |
| Microservices Patterns | Chris Richardson | [microservices.io](https://microservices.io/) |
| Awesome Distributed Systems | theanalyst | [github.com/theanalyst/awesome-distributed-systems](https://github.com/theanalyst/awesome-distributed-systems) |
| DDIA References (per-chapter primary sources) | Martin Kleppmann | [github.com/ept/ddia-references](https://github.com/ept/ddia-references) |
| Awesome Scalability | binhnguyennus | [github.com/binhnguyennus/awesome-scalability](https://github.com/binhnguyennus/awesome-scalability) |

---

## 🔭 2026 Industry Snapshot

> Sources rephrased for compliance — never more than 30 consecutive words from any single source.

| Area | 2026 Reality | Primary sources |
|---|---|---|
| Message brokers | Kafka 4.0 (Jan 2026) deprecated ZooKeeper; KRaft is the only consensus mode. RabbitMQ 4.1 (Feb 2026) added native streams + quorum-queue improvements. NATS JetStream is the single-binary alternative gaining traction. | [tech-insider.org Kafka vs RabbitMQ](https://tech-insider.org/kafka-vs-rabbitmq-2026/), [synadia](https://www.synadia.com/resources/beyond-streaming) |
| Vector DBs | Pinecone (managed leader), Qdrant (Rust speed leader), Weaviate (hybrid + GraphQL), Milvus (large-scale), Chroma (DX), pgvector (Postgres default). | [digitalapplied 2026](https://www.digitalapplied.com/blog/vector-databases-for-ai-agents-pinecone-qdrant-2026), [jusdb](https://www.jusdb.com/blog/vector-databases-comparison-pgvector-pinecone-weaviate) |
| Distributed SQL | CockroachDB vs YugabyteDB vs TiDB vs Spanner each occupy a different niche; pick by Postgres/MySQL preference, region locality, and HTAP needs. | [jusdb NewSQL](https://www.jusdb.com/blog/cockroachdb-vs-spanner-vs-yugabytedb-newsql), [pingcap](https://pingcap.com/compare/cockroachdb-vs-tidb) |
| API style | REST stays the default for ~80% of business APIs; GraphQL Federation wins cross-team graphs; gRPC for internal services. | [optimum-web 2026](https://www.optimum-web.com/blog/api-development-services-2026-rest-graphql-grpc-guide), [wundergraph](https://wundergraph.com/blog/six-year-graphql-recap) |
| Service mesh | Istio Ambient Mesh (sidecarless) is the 2026 headline. Linkerd remains the "small, fast, just works" pick. Cilium adds eBPF-native mesh. | [tasrieit Istio vs Linkerd](https://www.tasrieit.com/blog/istio-vs-linkerd-service-mesh-comparison-2026), [reintech 2026 mesh](https://reintech.io/blog/kubernetes-service-mesh-comparison-2026-istio-linkerd-cilium) |
| CRDTs / real-time | Yjs is dominant; Hocuspocus is the websocket backend; AI agents now join as CRDT peers (Electric Cloud + y-durable-streams, 2026). | [electric-sql AI as CRDT peers](https://electric-sql.com/blog/2026/04/08/ai-agents-as-crdt-peers-with-yjs), [yjs.dev](https://docs.yjs.dev/) |
| Load testing | k6 (Grafana, Go+JS) leads modern dev-friendly load testing; JMeter/Gatling/Locust still relevant for scale and Python-native stacks. | [grafana k6](https://github.com/grafana/k6), [apidog 2026](https://apidog.com/blog/software-performance-testing-tool/) |

---

## 🧰 Generated study aids

### 🎙️ Audio overviews & podcasts (NotebookLM)
- [ ] TODO: paste the NotebookLM "Audio Overview" link

### 🧠 Mind maps
- [ ] TODO: NotebookLM mind-map URL or screenshot

### ❓ Quizzes
- [ ] TODO: NotebookLM-generated quiz (CAP/PACELC, sharding, queueing)

### 📊 Reports & summaries
- [ ] TODO: NotebookLM "Briefing Doc" or "Study Guide"

### 🃏 Flash cards
- [ ] TODO: deck export (Latency numbers; consistency models; HTTP cache headers; Kafka semantics)

### 🎬 Video overviews
- [ ] TODO: YouTube / Loom personal recording walking the tower of scale

### 📋 Data tables
- [ ] TODO: comparison matrices (Kafka vs NATS vs RabbitMQ vs SQS; CockroachDB vs Yugabyte vs TiDB vs Spanner; vector DBs; service meshes)

---

## 🔗 Cross-links

- Syllabus & curriculum mindmap: [Subject_Plan](Subject_Plan)
- Visual roadmap: [LEARNING_PATH](LEARNING_PATH)
- Concurrency primitives: [1.4 - Concurrency - asyncio, threading, multiprocessing & the GIL](1.4---Concurrency---asyncio,-threading,-multiprocessing-&-the-GIL)
- OS essentials: [1.10 - Operating Systems Essentials](1.10---Operating-Systems-Essentials)
- Networking essentials: [1.11 - Computer Networks Essentials](1.11---Computer-Networks-Essentials)
- Distributed systems & multi-GPU: [1.16 - Distributed Systems & Multi-GPU Training](1.16---Distributed-Systems-&-Multi-GPU-Training)
- SQL track: [Subject_Plan](Subject_Plan)
- ROS 2 pub/sub (same patterns): [22.5 - ROS 2 & Middleware - Nodes, Topics, Services, Actions, DDS](22.5---ROS-2-&-Middleware---Nodes,-Topics,-Services,-Actions,-DDS)
- Real-time multi-user (CRDTs): [24.7 - Networking, Avatars & Multi-User Spaces](24.7---Networking,-Avatars-&-Multi-User-Spaces)
- Cybersecurity (secure-by-design): [Subject_Plan](Subject_Plan)
- DevOps & SRE (operate the design): [Subject_Plan](Subject_Plan)
- Cloud platforms (provider impl): [Subject_Plan](Subject_Plan)
- AI/ML systems (vector DBs, RAG): [Subject_Plan](Subject_Plan)
- Scaling north star: [BUILDING_AT_SCALE](BUILDING_AT_SCALE)
- Master Learning index: [00 - 09 - Learning Index](00---09---Learning-Index)
- Master practice guide: [HOW_TO_USE_PRACTICE](HOW_TO_USE_PRACTICE)
