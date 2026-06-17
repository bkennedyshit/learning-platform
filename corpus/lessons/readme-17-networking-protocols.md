---
title: "README — 17 - Networking & Protocols"
subject: "Networking & Protocols"
catalog: advanced
audience_tier: higher-education
chapter: "Chapter 1"
type: subject-readme
objectives:
  - "Understand the concepts"
  - "Apply the theory"
open_source: true
---

# 17 - Networking & Protocols — Subject Hub

> One-page subject hub. Lists chapters, source reading materials, **video / picture references stored outside the repo (linked by URL)**, and placeholders for generated study aids.
> Master practice guide: [HOW_TO_USE_PRACTICE](HOW_TO_USE_PRACTICE).

> **Asset storage convention.**
> - **SVG diagrams** (small, theme-responsive, in-vault) → `../_svgs/net__<chapter>-fig<n>.svg` and embedded inline via `![net__31.x-figN](net__31.x-figN.svg)`.
> - **Pictures, screenshots, videos, course recordings** are NOT committed to this repo. They live on YouTube, official docs, GitHub, or in your local `_assets/` sidecar (gitignored). Reference them by **URL** in this README and chapter notes.

---

## 🚀 Quick Start

```bash
# Capture packets on your primary interface and decode them
sudo tcpdump -i eth0 -n -vv -w capture.pcap
wireshark capture.pcap

# Test HTTP/3 support on a server
curl --http3 -I https://cloudflare.com

# Inspect TLS 1.3 handshake bytes
openssl s_client -connect google.com:443 -tls1_3 -state -debug 2>&1 | head -80

# Subnet calculator (Python one-liner)
python3 -c "import ipaddress; n=ipaddress.ip_network('10.0.0.0/26',False); print(list(n.hosts())[:3], '...', n.broadcast_address)"

# Decode a protobuf message (install protoc)
echo "0801120541..." | xxd -r -p | protoc --decode_raw
```

---

## 📜 Chapter Index

- [17.1 - Physical & Data Link Layer](17.1---Physical-&-Data-Link-Layer)
- [17.2 - IP, Routing & BGP](17.2---IP,-Routing-&-BGP)
- [17.3 - TCP & UDP Deep Dive](17.3---TCP-&-UDP-Deep-Dive)
- [17.4 - TLS, mTLS & PKI](17.4---TLS,-mTLS-&-PKI)
- [3 (QUIC)](3-(QUIC))
- [17.6 - WebSockets, SSE & WebRTC](17.6---WebSockets,-SSE-&-WebRTC)
- [17.7 - gRPC, Protocol Buffers & Service Mesh](17.7---gRPC,-Protocol-Buffers-&-Service-Mesh)
- [17.8 - Network Security & DDoS Mitigation](17.8---Network-Security-&-DDoS-Mitigation)

---

## 🎬 Video & Picture References (external — open in browser)

> These are the open-source / pro-grade media that supplement the chapter notes.

### 📺 Video Channels & Playlists

| Channel / Course | Track Use | Link |
|---|---|---|
| **Hussein Nasser** | HTTP/2, HTTP/3, WebSocket, gRPC, TCP internals | [@hnasr](https://www.youtube.com/@hnasr) |
| **Kurose & Ross lecture playlist** | Full networking textbook companion | YouTube search "Kurose Ross Computer Networking" |
| **Practical Networking** | Subnetting, routing, switching fundamentals | [practicalnetworking.net](https://www.practicalnetworking.net/) |
| **LiveOverflow (network-focused)** | Packet analysis, network protocol exploitation | [@LiveOverflow](https://www.youtube.com/@LiveOverflow) |
| **David Bombal** | Cisco networking, Wireshark, packet capture | [@davidbombal](https://www.youtube.com/@davidbombal) |
| **ByteByteGo** | TCP/IP, DNS, HTTPS visual explainers | [@ByteByteGo](https://www.youtube.com/@ByteByteGo) |
| **WebRTC.ventures YouTube** | WebRTC STUN/TURN/ICE video deep dives | YouTube "WebRTC ventures" |
| **Cloudflare TV** | QUIC, HTTP/3, DDoS presentations | [cloudflare.tv](https://cloudflare.tv/) |
| **IETF Meeting Recordings** | Protocol design discussions (QUIC, TLS WGs) | [ietf.org/how/meetings](https://www.ietf.org/how/meetings/) |

### 🖼️ Picture / Diagram Reference Sources

| Source | What it gives you | Link |
|---|---|---|
| **tls13.xargs.org** | Byte-by-byte TLS 1.3 handshake (interactive) | [tls13.xargs.org](https://tls13.xargs.org/) |
| **quic.xargs.org** | Byte-by-byte QUIC connection (interactive) | [quic.xargs.org](https://quic.xargs.org/) |
| **Julia Evans networking zines** | DNS, HTTP, TCP visual cheat sheets | [jvns.ca](https://jvns.ca/) |
| **bgp.tools** | Live BGP routing table explorer | [bgp.tools](https://bgp.tools/) |
| **Cloudflare Radar** | HTTP/3 adoption, QUIC stats, DDoS reports | [radar.cloudflare.com](https://radar.cloudflare.com/) |
| **Wireshark sample captures** | Real pcap files for every protocol | [wiki.wireshark.org/SampleCaptures](https://wiki.wireshark.org/SampleCaptures) |
| **WebRTC for the Curious diagrams** | ICE, DTLS, SRTP flow diagrams | [webrtcforthecurious.com](https://webrtcforthecurious.com/) |
| **MANRS Observatory** | BGP hijacking and RPKI adoption stats | [observatory.manrs.org](https://observatory.manrs.org/) |

### 📚 Open-Source / Free Books

| Title | Author / Provider | Link |
|---|---|---|
| Computer Networking: A Top-Down Approach | Kurose & Ross (lecture slides free) | [gaia.cs.umass.edu/kurose_ross](http://gaia.cs.umass.edu/kurose_ross/) |
| Beej's Guide to Network Programming | Brian Hall | [beej.us/guide/bgnet](https://beej.us/guide/bgnet/) |
| High Performance Browser Networking | Ilya Grigorik (O'Reilly free online) | [hpbn.co](https://hpbn.co/) |
| WebRTC for the Curious | WebRTC community | [webrtcforthecurious.com](https://webrtcforthecurious.com/) |
| Cloudflare Learning Center | Cloudflare | [cloudflare.com/learning](https://www.cloudflare.com/learning/) |
| TCP/IP Guide | Charles Kozierok | [tcpipguide.com](http://www.tcpipguide.com/) |
| RFC 8446 — TLS 1.3 | IETF | [rfc-editor.org/rfc/rfc8446](https://www.rfc-editor.org/rfc/rfc8446) |
| RFC 9000 — QUIC Transport | IETF | [rfc-editor.org/rfc/rfc9000](https://www.rfc-editor.org/rfc/rfc9000) |
| RFC 9114 — HTTP/3 | IETF | [rfc-editor.org/rfc/rfc9114](https://www.rfc-editor.org/rfc/rfc9114) |

---

## 🔭 2026 Industry Snapshot

> Sources rephrased for compliance — never more than 30 consecutive words from any single source.

| Area | 2026 Reality | Primary Sources |
|---|---|---|
| HTTP/3 adoption | ~30% of global web traffic; Cloudflare reports 70%+ of their traffic over QUIC; enabled by default in all major browsers | [Cloudflare Radar 2025](https://radar.cloudflare.com/year-in-review/2025) |
| BBR congestion control | BBR v3 in Linux mainline; default in major cloud VMs; meaningfully reduces buffer bloat vs CUBIC | [LWN.net BBR v3 coverage](https://lwn.net/) |
| QUIC ecosystem | MSQUIC (open-source, powers Azure + SMB), Google QUICHE, Cloudflare quiche are dominant implementations | [IETF QUIC WG](https://quicwg.org/) |
| gRPC | Default for polyglot internal services; gRPC-Web for browser clients; gRPC over HTTP/3 production-ready in Go/Java | [grpc.io](https://grpc.io/) |
| Service mesh | Istio Ambient Mesh (no sidecars) production-stable; Cilium eBPF mesh gaining in Kubernetes-native environments | [istio.io blog](https://istio.io/latest/blog/) |
| DDoS scale | Largest recorded attack: 5.6 Tbit/s (Oct 2024, targeting Cloudflare), auto-mitigated | [Cloudflare Q4 2024 DDoS report](https://blog.cloudflare.com/ddos-threat-report-for-2024-q4/) |
| RPKI adoption | ~45% of Internet prefixes have ROAs; major transit ISPs enforce ROV; hijacks of signed prefixes mostly self-correcting | [NIST RPKI monitor](https://rpki-monitor.antd.nist.gov/) |
| WebTransport | GA in Chrome 114+; QUIC-based alternative to WebSocket for low-latency non-media use cases | [W3C WebTransport spec](https://www.w3.org/TR/webtransport/) |

---

## 🧰 Generated Study Aids

### 🎙️ Audio Overviews & Podcasts (NotebookLM)
- [ ] TODO: paste the NotebookLM "Audio Overview" link for this track

### 🧠 Mind Maps
- [ ] TODO: NotebookLM mind-map URL or screenshot

### ❓ Quizzes
- [ ] TODO: NotebookLM-generated quiz (TCP handshake, TLS key exchange, HTTP/3 vs HTTP/2, subnetting)

### 📊 Reports & Summaries
- [ ] TODO: NotebookLM "Briefing Doc" or "Study Guide"

### 🃏 Flash Cards
- [ ] TODO: deck export (OSI layers; TCP flags; TLS messages; QUIC vs TCP differences; BGP attributes; DDoS types)

### 🎬 Video Overviews
- [ ] TODO: Loom walkthrough of Wireshark captures demonstrating TLS 1.3 and HTTP/2 live

### 📋 Data Tables
- [ ] TODO: comparison matrix (HTTP/1.1 vs HTTP/2 vs HTTP/3; WebSocket vs SSE vs WebRTC; TCP vs UDP; CUBIC vs BBR)
- [ ] TODO: protocol port numbers reference (80/443, 53, 22, 25, 443+QUIC, 5353, etc.)
- [ ] TODO: TLS cipher suite reference

---

## 🔗 Cross-Links

- Syllabus & curriculum mindmap: [Subject_Plan](Subject_Plan)
- Visual roadmap: [LEARNING_PATH](LEARNING_PATH)
- OS & sockets prerequisite: [1.10 - Operating Systems Essentials](1.10---Operating-Systems-Essentials)
- Networking intro (Python track): [1.11 - Computer Networks Essentials](1.11---Computer-Networks-Essentials)
- Concurrency & async I/O: [1.4 - Concurrency - asyncio, threading, multiprocessing & the GIL](1.4---Concurrency---asyncio,-threading,-multiprocessing-&-the-GIL)
- Distributed systems: [1.16 - Distributed Systems & Multi-GPU Training](1.16---Distributed-Systems-&-Multi-GPU-Training)
- System Design (architecture layer above): [Subject_Plan](Subject_Plan)
- Cybersecurity (network attack surface): [Subject_Plan](Subject_Plan)
- DevOps & SRE (mesh, k8s networking): [Subject_Plan](Subject_Plan)
- Cloud Platforms (VPC, transit gateways): [Subject_Plan](Subject_Plan)
- VR (WebRTC, QUIC streaming): [Subject_Plan](Subject_Plan)
- Game Dev (netcode): [Subject_Plan](Subject_Plan)
- Scaling north star: [BUILDING_AT_SCALE](BUILDING_AT_SCALE)
- Master Learning index: [00 - 09 - Learning Index](00---09---Learning-Index)
- Master practice guide: [HOW_TO_USE_PRACTICE](HOW_TO_USE_PRACTICE)
