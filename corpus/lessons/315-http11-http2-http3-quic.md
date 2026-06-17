---
title: "31.5 — HTTP/1.1, HTTP/2 & HTTP/3 (QUIC)"
subject: "2 & HTTP"
catalog: advanced
audience_tier: higher-education
chapter: "31.5"
type: chapter
objectives:
  - "Understand the concepts"
  - "Apply the theory"
open_source: true
---

*Back to [Subject_Plan](Subject_Plan) | Part of [00 - 09 - Learning Index](00---09---Learning-Index)*

# 31.5 — HTTP/1.1, HTTP/2 & HTTP/3 (QUIC)

> *"The story of HTTP is the story of every abstraction layer finding its bottleneck and then inventing a new protocol to eliminate it."*

HTTP/1.1 (1997) was designed for a simpler web. HTTP/2 (2015) solved the application-level head-of-line blocking by multiplexing streams over one TCP connection. HTTP/3 (2022) solved the remaining TCP-level head-of-line blocking by moving to QUIC over UDP. Each iteration removed a specific, identified performance bottleneck while maintaining backward compatibility at the application level. This chapter teaches you to *see* those bottlenecks in your own network captures.

---

## 🎯 Learning Objectives

By the end of this chapter you will be able to:

1. Explain HTTP/1.1 **head-of-line blocking** and why browsers open 6 parallel connections per origin as a workaround.
2. Explain HTTP/2's **binary framing layer**, **stream multiplexing**, **HPACK header compression**, and the deprecation of server push.
3. Explain **QUIC's** core innovations: UDP-based transport, built-in TLS 1.3, independent streams (no L4 HOL blocking), and connection migration.
4. Explain QUIC **0-RTT** and the PSK early-data flow.
5. Explain **QPACK** and how it avoids HPACK's head-of-line blocking.
6. Capture HTTP/2 and HTTP/3 traffic and identify stream IDs in Wireshark.
7. Configure a server to serve HTTP/3 and verify it with `curl --http3`.

---

## 🖼️ Visual Anchor

![net__31.5-fig1](net__31.5-fig1.svg)

---

## 📚 1. HTTP/1.1

### 1.1 Overview and Persistent Connections

HTTP/1.0 closed the TCP connection after each request-response pair — a new TCP + TLS handshake for every resource. Disastrous for pages with dozens of assets.

HTTP/1.1 (RFC 7230–7235) introduced **persistent connections** (keep-alive) by default:

```http
GET /index.html HTTP/1.1
Host: example.com
Connection: keep-alive

HTTP/1.1 200 OK
Content-Length: 1234
Connection: keep-alive
```

The TCP connection stays open after the response, ready for the next request. This eliminates the TCP+TLS handshake cost for subsequent requests on the same host.

### 1.2 The Fundamental Limitation: Request-Response Ordering

HTTP/1.1 is **strictly sequential** on a single connection: one request at a time. The server **must** respond in the order requests were received.

```
Connection 1:  [GET /style.css] ... [200 style.css] [GET /script.js] ... [200 script.js]
Connection 2:  [GET /image.png] ... [200 image.png]
```

This is the **HTTP-level head-of-line blocking**: if the response to Request 1 is slow (large file, slow DB query), Request 2 waits even if the server could answer it immediately.

### 1.3 HTTP Pipelining (Failed Attempt)

HTTP/1.1 includes **pipelining**: send multiple requests without waiting for responses. Sounds like it solves the problem.

It doesn't. Responses must still arrive in the same order as requests. A slow Response 1 blocks Responses 2, 3, 4... The exact same head-of-line blocking, just at a different point. Pipelining is **disabled by default** in all browsers.

### 1.4 The 6-Connection Hack

Browsers work around HTTP/1.1 limitations by opening **6 TCP connections per origin** (RFC 2616 recommended 2; browsers found 6 was optimal empirically). This parallelizes up to 6 requests simultaneously.

Costs:
- 6 TCP handshakes + 6 TLS handshakes per origin
- Server must handle 6× as many connections
- Many pages with 20+ origins = 120+ connections for one page load
- Each connection needs its own TCP slow start → under-utilization

### 1.5 HTTP/1.1 Performance Optimizations (Workarounds)

Application developers invented workarounds to compensate for HTTP/1.1's limitations:

| Technique | What it does | Why it was needed |
|---|---|---|
| Domain sharding | Split resources across 4+ hostnames (cdn1/cdn2/cdn3...) | More than 6 connections per "origin" |
| CSS/JS bundling | Combine all files into one | Fewer requests |
| Image sprites | Combine all images into one | Fewer requests |
| Inlining | Embed CSS/JS in HTML | Zero requests |
| Cache-busting | `style.v1234.css` in filenames | Long cache TTLs for bundled files |

**All of these are anti-patterns in HTTP/2** — HTTP/2's multiplexing makes them unnecessary and often counterproductive.

---

## 📚 2. HTTP/2 (RFC 7540 / RFC 9113)

### 2.1 Binary Framing Layer

HTTP/2's fundamental innovation is a **binary framing layer** that sits between the HTTP semantics (headers, bodies) and the TCP connection:

```
HTTP/2 Connection
├── Stream 1  (GET /index.html)
│   ├── HEADERS frame  [stream_id=1, END_HEADERS]
│   └── DATA frame     [stream_id=1, END_STREAM]
├── Stream 3  (GET /style.css)
│   └── HEADERS frame  [stream_id=3]
├── Stream 5  (GET /script.js)
│   └── HEADERS frame  [stream_id=5]
└── ...
```

**Every HTTP/2 frame has a 9-byte header**:
```
+-----------------------------------------------+
|                 Length (24 bits)              |
+---------------+---------------+---------------+
|   Type (8)    |   Flags (8)   |
+-+-------------+---------------+-------------------------------+
|R|                 Stream Identifier (31 bits)                 |
+=+=============================================================+
|                   Frame Payload (0 to 2^24 - 1 bytes)        |
+---------------------------------------------------------------+
```

**Frame types**:
- `DATA` (0x0): HTTP body payload
- `HEADERS` (0x1): HTTP headers (HPACK-compressed)
- `PRIORITY` (0x2): Stream priority hints (deprecated in RFC 9218)
- `RST_STREAM` (0x3): Terminate a stream without closing the connection
- `SETTINGS` (0x4): Configure connection parameters
- `PUSH_PROMISE` (0x5): Server push announcement
- `PING` (0x6): RTT measurement / keepalive
- `GOAWAY` (0x7): Graceful connection close
- `WINDOW_UPDATE` (0x8): Flow control
- `CONTINUATION` (0x9): Continue HEADERS frame

### 2.2 Stream Multiplexing

Multiple streams co-exist on one TCP connection. Streams are **independent** at the HTTP/2 level:

- Stream IDs are odd for client-initiated, even for server-pushed
- A slow stream doesn't block other streams (at the HTTP layer)
- Maximum concurrent streams configured via SETTINGS frame

```
Time →
Stream 1:  [HEADERS][DATA...                            ][END]
Stream 3:  [HEADERS][DATA][END]
Stream 5:            [HEADERS][DATA][END]
Stream 7:                           [HEADERS][DATA...   ][END]
```

All interleaved on a single TCP connection. **This eliminates the application-layer head-of-line blocking** that HTTP/1.1 had.

**Remaining problem**: TCP is still involved. If a single TCP segment is lost, TCP's reliable delivery blocks **all streams** until that segment is retransmitted. This is **TCP-level head-of-line blocking** — it persists in HTTP/2 and is what HTTP/3 fixes.

### 2.3 HPACK Header Compression (RFC 7541)

HTTP headers are repetitive across requests (same `Accept-Encoding`, `Authorization`, `User-Agent`). HPACK compresses them using two techniques:

**Static table (61 entries)**: Predefined common headers (`:method GET` = index 2, `:status 200` = index 8, etc.)

**Dynamic table**: Headers seen in this connection are added to a shared table and referenced by index in future requests.

```
First request:
  :method: GET        → encode as index 2 (static)
  :path: /            → encode as literal, add to dynamic table (index 62)
  host: example.com   → encode as literal, add to table (index 63)
  user-agent: Chrome  → encode as literal, add to table (index 64)

Second request to same host:
  :method: GET        → index 2 (1 byte)
  :path: /about       → new literal (small)
  host: example.com   → index 63 (1 byte)
  user-agent: Chrome  → index 64 (1 byte)
```

**HPACK danger**: The dynamic table must be synchronized between client and server. A lost or reordered HPACK update causes decompression errors for all subsequent headers on the connection. This is why HTTP/3 uses QPACK (discussed below).

### 2.4 Server Push

HTTP/2 allows the server to proactively send resources the client hasn't requested yet (e.g., push `style.css` before the client parses the HTML and requests it).

**Reality**: Server push was almost never effective in practice:
- Browsers often already have the resource cached
- Push can cause bandwidth waste if the browser drops the push
- Complex to implement correctly (when to push? when has browser already cached it?)

Server push is **deprecated in practice** (Chrome removed it in 2022; most HTTP/2 implementations ignore it). HTTP/3 (RFC 9114) removed it entirely. **Use `<link rel="preload">` instead** — it's a hint to the browser with the same effect but without the wasted bandwidth.

---

## 📚 3. HTTP/3 and QUIC

### 3.1 The Core Problem with HTTP/2 over TCP

HTTP/2 solved application-layer HOL blocking but TCP's reliable delivery still blocks all streams on a single lost packet. On a link with 1% packet loss:
- **HTTP/1.1 with 6 connections**: Likely 1 connection affected; others proceed
- **HTTP/2 with 1 connection**: All streams blocked when that 1 packet is lost

For mobile networks with 1–3% loss, HTTP/2 can actually be *slower* than HTTP/1.1 in practice.

The solution: replace TCP with a custom reliable transport that doesn't have this global blocking.

### 3.2 QUIC — Quick UDP Internet Connections (RFC 9000)

QUIC is a **new transport protocol implemented in user-space over UDP**. It was designed by Google (2012), standardized by IETF (RFC 9000, 2021), and is the transport for HTTP/3 (RFC 9114).

Key design decisions:

**1. UDP as the substrate**: UDP is used only as a thin shell. QUIC implements its own reliability, flow control, and congestion control on top.

**2. TLS 1.3 built-in**: QUIC's cryptographic layer is TLS 1.3, but tightly integrated rather than layered on top. The handshake is faster because crypto keys are established during the QUIC handshake itself.

**3. Independent streams**: Each QUIC stream is independently reliable. A lost packet only blocks the stream that was waiting for that data — not all streams. This eliminates the TCP-level HOL blocking.

**4. Connection IDs**: QUIC connections are identified by a **Connection ID** chosen by the client, not by the `{src_IP, src_port, dst_IP, dst_port}` 4-tuple. This enables connection migration.

### 3.3 QUIC Packet Structure

```
Long Header (Initial/Handshake packets):
┌────────────────────────────────────────────────┐
│ 1 | Fixed=1 | Long Packet Type | Reserved | PKT#Len │  ← Header Form, flags
├────────────────────────────────────────────────┤
│              Version (32 bits)                 │
├────────────────────────────────────────────────┤
│         Destination Connection ID              │
├────────────────────────────────────────────────┤
│           Source Connection ID                 │
├────────────────────────────────────────────────┤
│              Packet Number                     │
├────────────────────────────────────────────────┤
│              QUIC Frames...                    │
│  (STREAM, ACK, CRYPTO, PADDING, PING, ...)    │
└────────────────────────────────────────────────┘
```

QUIC **encrypts the packet header** (except the Connection ID) — even packet numbers are encrypted. This prevents middleboxes from interpreting or manipulating QUIC packets.

### 3.4 QUIC Connection Establishment

```
Client                                              Server
  │                                                   │
  │  Initial packet (CRYPTO: ClientHello)             │
  │  ─────────────────────────────────────────────►  │
  │                                                   │
  │  Initial packet (CRYPTO: ServerHello)             │
  │  Handshake packet (CRYPTO: EncryptedExts+Cert+Fin)│
  │  ◄─────────────────────────────────────────────  │
  │                                                   │
  │  Handshake packet (CRYPTO: Finished)              │
  │  1-RTT packet (HTTP/3 HEADERS frames)             │
  │  ─────────────────────────────────────────────►  │
  │                                                   │
  │  1-RTT Application Data                           │
  │  ◄───────────────────────────────────────────── ►│
```

Total: **1 RTT for QUIC+TLS** combined (vs 2 RTTs for TCP+TLS). The cryptographic handshake is integrated with the connection establishment.

### 3.5 QUIC 0-RTT

Using a session ticket from a previous connection:

```
Client → Server: Initial packet {
  CRYPTO: ClientHello [PSK, early_data extension]
  1-RTT: HTTP/3 HEADERS frames [0-RTT application data]
}
```

The application data arrives at the server in the **very first packet** — zero round trips after IP routing delivers the first UDP datagram.

**As with TLS 1.3 0-RTT**, this is only safe for idempotent operations (see [17.4 - TLS, mTLS & PKI](17.4---TLS,-mTLS-&-PKI)).

### 3.6 Connection Migration

Traditional TCP connections die when your IP address changes (e.g., switching from Wi-Fi to mobile data). The entire 4-tuple `{client_IP, client_port, server_IP, server_port}` identifies the connection; any change breaks it.

QUIC connections are identified by the **Connection ID** (a random byte string chosen by the client). When the client's IP changes:

```
Client (old: 192.168.1.5:50001)  ──────────────►  Server
  ... changes network ...
Client (new: 10.0.0.2:50001)    ──────────────►  Server
  PATH_CHALLENGE frame (prove new address is reachable)
  Server: PATH_RESPONSE frame
  Connection continues without re-handshake
```

This is critical for mobile clients switching between Wi-Fi and 5G, VPN connections, and any scenario where the client's IP might change mid-session.

### 3.7 QPACK Header Compression (RFC 9204)

HTTP/3 uses **QPACK** instead of HPACK to avoid HPACK's synchronization problem.

HPACK required the dynamic table to be synchronized across the stream (since HTTP/2 uses one ordered TCP stream for all header blocks). QUIC streams can be delivered out of order, which would break HPACK.

QPACK splits header encoding into two streams:
- **Encoder stream** (unidirectional): Sends dynamic table updates
- **Decoder stream** (unidirectional): Sends acknowledgments of table updates
- **Request streams**: Can reference only table entries the decoder has confirmed

This allows QPACK to use the dynamic table without waiting for all previous streams to complete.

---

## 📚 4. Practical Comparison

### 4.1 When Does HTTP/3 Win Most?

HTTP/3 / QUIC wins most noticeably when:
- **High packet loss** (mobile, last-mile broadband): TCP HOL blocking is eliminated
- **Mobile network switching** (Wi-Fi → 5G): Connection migration preserves session
- **High-latency connections** (intercontinental, satellite): 0-RTT saves one full RTT
- **Many small requests** (API servers, CDN edge): Less handshake overhead per connection

HTTP/3 may not win on:
- Low-latency, reliable datacenter LAN: TCP is already optimal
- Server-to-server internal calls: TLS 1.3 0-RTT resumption over TCP is nearly as good

### 4.2 Configuration Example

**Nginx HTTP/3 (1.25+ or nginx-quic):**
```nginx
server {
    listen 443 quic reuseport;
    listen 443 ssl;
    http2 on;
    
    ssl_certificate      /etc/nginx/ssl/cert.pem;
    ssl_certificate_key  /etc/nginx/ssl/key.pem;
    
    # Advertise HTTP/3 support
    add_header Alt-Svc 'h3=":443"; ma=86400';
    
    quic_retry on;
    ssl_early_data on;    # 0-RTT
}
```

```bash
# Verify HTTP/3 is served
curl --http3 -I https://your-domain.com
# HTTP/3 200
# alt-svc: h3=":443"; ma=86400
```

---

## ⚠️ 5. Common Misconceptions

- **"HTTP/2 is always faster than HTTP/1.1."** On high-loss or congested connections, HTTP/2's single TCP connection can be slower than HTTP/1.1's 6 connections. Measure; don't assume.
- **"Server push is a good idea."** In theory yes; in practice it caused more problems than it solved. Use `<link rel="preload">` or 103 Early Hints instead.
- **"QUIC replaces UDP for everything."** QUIC is a specific protocol. Plain UDP (for real-time media, game netcode, DNS) is unaffected. QUIC is the HTTP/3 transport, not a universal UDP replacement.
- **"HTTP/3 requires HTTP/2 first."** No. HTTP/3 is a completely separate protocol. A client/server can speak HTTP/3 directly without ever using HTTP/2. The `Alt-Svc` header allows upgrading from HTTP/2 to HTTP/3 in a subsequent request.
- **"HPACK is broken in HTTP/2."** HPACK works correctly over HTTP/2's single ordered stream. The CRIME and BREACH attacks on TLS compression are different (they exploit the interaction of compression with encryption when attacker-controlled data is mixed with secrets). HPACK itself is secure when TLS is used.

---

## 🔗 6. Cross-Links & Further Reading

### Internal
- [17.4 - TLS, mTLS & PKI](17.4---TLS,-mTLS-&-PKI) — TLS 1.3 is integral to QUIC; 0-RTT discussed in depth there
- [17.3 - TCP & UDP Deep Dive](17.3---TCP-&-UDP-Deep-Dive) — TCP congestion control and HOL blocking that HTTP/2 and HTTP/3 address
- [17.6 - WebSockets, SSE & WebRTC](17.6---WebSockets,-SSE-&-WebRTC) — WebSocket and WebRTC are separate from HTTP; when to use each
- [17.7 - gRPC, Protocol Buffers & Service Mesh](17.7---gRPC,-Protocol-Buffers-&-Service-Mesh) — gRPC runs over HTTP/2 (and increasingly HTTP/3)
- [27.2 - Caching, CDNs & Edge](27.2---Caching,-CDNs-&-Edge) — CDNs serve HTTP/3

### External
- [High Performance Browser Networking — HTTP/2 and QUIC chapters](https://hpbn.co/)
- [RFC 9000 — QUIC: A UDP-Based Multiplexed and Secure Transport](https://www.rfc-editor.org/rfc/rfc9000)
- [RFC 9114 — HTTP/3](https://www.rfc-editor.org/rfc/rfc9114)
- [quic.xargs.org — byte-level QUIC walkthrough](https://quic.xargs.org/)
- [Cloudflare blog — HTTP/3: the past, the present, and the future](https://blog.cloudflare.com/http3-the-past-present-and-future/)
- [Cloudflare Radar — HTTP/3 adoption stats](https://radar.cloudflare.com/)
- [Hussein Nasser — HTTP/2 vs HTTP/3 (YouTube)](https://www.youtube.com/@hnasr)
- [IETF QUIC Working Group](https://quicwg.org/)

---

*Next: [17.6 - WebSockets, SSE & WebRTC](17.6---WebSockets,-SSE-&-WebRTC) — Real-time bidirectional and peer-to-peer communication.*
