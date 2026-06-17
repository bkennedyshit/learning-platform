---
title: "17.6 — WebSockets, SSE & WebRTC"
subject: "Networking & Protocols"
catalog: advanced
audience_tier: higher-education
chapter: "17.6"
type: chapter
objectives:
  - "Understand the concepts"
  - "Apply the theory"
open_source: true
---

*Back to [Subject_Plan](Subject_Plan) | Part of [00 - 09 - Learning Index](00---09---Learning-Index)*

# 17.6 — WebSockets, SSE & WebRTC

> *"HTTP is a one-way street — great for documents, terrible for conversations. The real-time web needed something different: a protocol that keeps a connection open and lets both sides speak freely."*

The modern real-time web is built on three complementary protocols. **WebSocket** gives you a full-duplex persistent connection over HTTP. **SSE (Server-Sent Events)** gives you a lightweight one-way push channel. **WebRTC** gives you peer-to-peer audio, video, and data with sub-100ms latency. Each solves a different problem; understanding the tradeoffs lets you pick the right one.

---

## 🎯 Learning Objectives

By the end of this chapter you will be able to:

1. Implement the **WebSocket HTTP upgrade handshake** including the `Sec-WebSocket-Key` validation.
2. Describe the **WebSocket frame format** and the 6 opcode types.
3. Implement an **SSE endpoint** with named events, IDs, and automatic reconnect.
4. Explain the **WebRTC ICE process**: gathering candidates (host, srflx, relay), connectivity checks, and nomination.
5. Explain **STUN** and **TURN** and when each is required.
6. Walk through an **SDP Offer/Answer** exchange including the media description fields.
7. Explain **DTLS-SRTP** — how WebRTC's media is encrypted.
8. Choose between WebSocket, SSE, WebRTC, and WebTransport for any real-time use case.

---

## 🖼️ Visual Anchor

![net__31.6-fig1](net__31.6-fig1.svg)

---

## 📚 1. WebSocket

### 1.1 The Upgrade Handshake

WebSocket begins as a regular HTTP/1.1 connection, then upgrades to a persistent full-duplex channel. The upgrade uses HTTP headers:

**Client request**:
```http
GET /ws/chat HTTP/1.1
Host: chat.example.com
Upgrade: websocket
Connection: Upgrade
Sec-WebSocket-Key: dGhlIHNhbXBsZSBub25jZQ==
Sec-WebSocket-Version: 13
Sec-WebSocket-Protocol: chat, superchat
Origin: https://example.com
```

**Server response**:
```http
HTTP/1.1 101 Switching Protocols
Upgrade: websocket
Connection: Upgrade
Sec-WebSocket-Accept: s3pPLMBiTxaQ9kYGzzhZRbK+xOo=
Sec-WebSocket-Protocol: chat
```

**`Sec-WebSocket-Accept` derivation**:
```python
import base64, hashlib
GUID = "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"
key = "dGhlIHNhbXBsZSBub25jZQ=="
accept = base64.b64encode(
    hashlib.sha1((key + GUID).encode()).digest()
).decode()
# Result: "s3pPLMBiTxaQ9kYGzzhZRbK+xOo="
```

The `Sec-WebSocket-Key` is a random 16-byte value base64-encoded by the client. The server concatenates it with the fixed GUID and SHA-1 hashes the result. This prevents HTTP caches or proxies from serving stale WebSocket handshakes. It is **not a security mechanism** against deliberate WebSocket connections — that's what the `Origin` header and server-side validation are for.

After the 101 response, the TCP connection is a raw WebSocket channel. HTTP parsing stops.

### 1.2 WebSocket Frame Format (RFC 6455)

```
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-------+-+-------------+-------------------------------+
|F|R|R|R| opcode|M| Payload len |    Extended payload length    |
|I|S|S|S|  (4)  |A|     (7)    |             (16/64)           |
|N|V|V|V|       |S|             |   (if payload len==126/127)   |
| |1|2|3|       |K|             |                               |
+-+-+-+-+-------+-+-------------+ - - - - - - - - - - - - - - - +
|     Extended payload length continued, if payload len == 127  |
+ - - - - - - - - - - - - - - -+-------------------------------+
|                               |Masking-key, if MASK set to 1  |
+-------------------------------+-------------------------------+
| Masking-key (continued)       |          Payload Data         |
+-------------------------------- - - - - - - - - - - - - - - - +
:                     Payload Data continued ...                :
+---------------------------------------------------------------+
```

| Field | Description |
|---|---|
| **FIN** | Final fragment of a message (1 = last/only frame) |
| **RSV1/2/3** | Reserved; used by extensions (e.g., RSV1=1 means permessage-deflate compression) |
| **Opcode** | Frame type (see below) |
| **MASK** | 1 = payload is masked (client→server MUST mask; server→client MUST NOT) |
| **Payload Len** | 7 bits; if 126: next 2 bytes are length; if 127: next 8 bytes are length |
| **Masking Key** | 4 bytes; used to XOR the payload (prevents cache poisoning by proxies) |
| **Payload** | Frame data (XOR'd with masking key if MASK=1) |

**Opcodes**:
| Value | Meaning |
|---|---|
| `0x0` | Continuation frame (fragment of previous message) |
| `0x1` | Text frame (UTF-8) |
| `0x2` | Binary frame |
| `0x8` | Close connection (may include status code) |
| `0x9` | Ping (expect Pong) |
| `0xA` | Pong (reply to Ping) |

### 1.3 Connection Keep-Alive

WebSocket runs over TCP. TCP has a keepalive (off by default at ~2 hours), but application-level keepalive is better. The ping/pong mechanism:

```python
# Server sends ping every 30s
# Client must reply with pong within N seconds
# If no pong → close connection

import asyncio, websockets

async def handler(ws):
    async for message in ws:
        await ws.send(f"Echo: {message}")

async def main():
    async with websockets.serve(handler, "localhost", 8765, ping_interval=30, ping_timeout=10):
        await asyncio.Future()  # run forever
```

### 1.4 Close Handshake

Either side sends a Close frame (opcode `0x8`) with an optional 2-byte status code and text reason:

```
Status codes:
1000 — Normal closure
1001 — Going away (server shutting down)
1002 — Protocol error
1003 — Unsupported data type
1008 — Policy violation
1011 — Unexpected condition (server error)
```

The receiver must echo the Close frame back before closing the underlying TCP connection.

---

## 📚 2. Server-Sent Events (SSE)

### 2.1 Overview

SSE (EventSource, HTML5 / WHATWG, RFC 8898 context) is a simple unidirectional server-to-client push mechanism over HTTP. The client opens a normal GET request; the server keeps it open and streams events.

**When to use SSE over WebSocket**:
- Client only needs to *receive* from server (feed, notifications, LLM token streaming)
- Works through existing HTTP proxies, CDNs, and load balancers without special config
- Auto-reconnect with `Last-Event-ID` is built-in
- Works over HTTP/2 (multiplexed with other requests — no extra connection needed)

### 2.2 SSE Wire Format

**Server response headers**:
```http
HTTP/1.1 200 OK
Content-Type: text/event-stream
Cache-Control: no-cache
Connection: keep-alive
Access-Control-Allow-Origin: *
```

**Event format** (plain text, UTF-8):
```
id: 1001
event: price_update
data: {"symbol": "BTC", "price": 62450.00}
retry: 5000

data: {"symbol": "ETH", "price": 3100.00}

: this is a comment (server-side keepalive ping)

data: multiline data
data: continues here

```

**Fields**:
- `id`: The event ID. Browser stores this; on reconnect sends `Last-Event-ID` header so server can resume from the right point.
- `event`: Custom event type. Default is `message`. Browser dispatches as `EventSource.addEventListener('price_update', handler)`.
- `data`: Event payload. Multiple `data:` lines are joined with `\n`.
- `retry`: Reconnect delay in milliseconds. Default ~3s.
- `:`: Comment line — used to keep the connection alive through proxies that close idle connections.

**Each event is terminated by a blank line (`\n\n`).**

### 2.3 JavaScript Client

```javascript
const source = new EventSource('/api/events');

// Default 'message' events
source.onmessage = (event) => {
    console.log('Received:', event.data, 'id:', event.lastEventId);
};

// Named event types
source.addEventListener('price_update', (event) => {
    const data = JSON.parse(event.data);
    updateUI(data.symbol, data.price);
});

source.onerror = (err) => {
    // EventSource auto-reconnects with Last-Event-ID header
    console.error('SSE error, reconnecting...', err);
};

// Close when done
source.close();
```

### 2.4 LLM Token Streaming with SSE

OpenAI's API and most LLM inference endpoints use SSE to stream tokens as they're generated:

```python
# FastAPI SSE endpoint for LLM streaming
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import asyncio

app = FastAPI()

async def generate_tokens():
    tokens = ["Hello", " world", "!", " How", " are", " you", "?"]
    for token in tokens:
        yield f"data: {token}\n\n"
        await asyncio.sleep(0.05)  # simulate generation time
    yield "data: [DONE]\n\n"

@app.get("/api/stream")
async def stream():
    return StreamingResponse(
        generate_tokens(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache"}
    )
```

---

## 📚 3. WebRTC

### 3.1 Architecture Overview

WebRTC enables real-time peer-to-peer communication (audio, video, data) directly between browsers or native apps. The key challenge: **most peers are behind NAT**, so they don't have publicly reachable IP addresses.

WebRTC's solution: **ICE (Interactive Connectivity Establishment)**, which uses STUN and TURN servers to discover and verify connectivity paths.

```
Architecture:
  Peer A  ──────────────────────────────────────  Peer B
     ↕                                               ↕
  STUN/TURN                 Signaling           STUN/TURN
  server                    server              server
  (public IP)               (WebSocket/HTTP)    (public IP)
```

**Signaling** is application-defined — WebRTC does not specify how SDP offer/answers are exchanged. You implement signaling (typically WebSocket), and it carries the SDP blobs between peers.

### 3.2 ICE — Interactive Connectivity Establishment

ICE (RFC 8445) systematically discovers every possible way the two peers can reach each other, then picks the best working path.

**Step 1 — Gather candidates**:

Each peer gathers a list of **ICE candidates** — `{protocol, IP, port}` tuples that might work:

```
Candidate types:
  host:     192.168.1.5:50000   (local NIC address — works if both on same LAN)
  srflx:    203.0.113.5:50001   (server-reflexive — public IP:port as seen by STUN server)
  relay:    198.51.100.1:3478   (relayed through TURN server — always works, higher latency)
  prflx:    (peer-reflexive — discovered during connectivity checks)
```

**Step 2 — STUN (Session Traversal Utilities for NAT, RFC 5389)**:

STUN is a simple protocol. The peer sends a **Binding Request** to a public STUN server; the server responds with the peer's public IP and port as observed:

```
Peer A (192.168.1.5:50000) → STUN server (stun.example.com:3478):
  STUN Binding Request
  
STUN server → Peer A:
  STUN Binding Response {XOR-MAPPED-ADDRESS: 203.0.113.5:50001}
```

This gives Peer A a **server-reflexive candidate**: `203.0.113.5:50001`. Peer B can try sending UDP packets to this address.

**Step 3 — TURN (Traversal Using Relays around NAT, RFC 8656)**:

If STUN doesn't work (symmetric NAT, firewall), TURN relays traffic:

```
Peer A  ──── UDP ────►  TURN server  ──── UDP ────►  Peer B
             (relay)
```

The TURN server allocates a **relayed transport address** for Peer A. All traffic to that address is forwarded to Peer A. TURN requires authentication (username/password) and increases latency. Use as last resort.

**Step 4 — Connectivity checks**:

Both peers exchange their full candidate lists via the signaling channel. Then they systematically try all `{local_candidate, remote_candidate}` pairs using STUN Binding Requests with ICE-specific attributes:

```
Peer A → Peer B: STUN Binding Request (ICE USE-CANDIDATE)
Peer B → Peer A: STUN Binding Response (success)
→ This candidate pair is nominated as the ICE path
```

**ICE priority**: host > srflx > relay (prefers direct connections over relayed ones).

### 3.3 SDP — Session Description Protocol

SDP (RFC 4566) describes the multimedia session: what codecs are supported, what ICE candidates are available, what encryption parameters to use.

**Offer (Peer A → Peer B)**:
```sdp
v=0
o=- 8286378291 2 IN IP4 127.0.0.1
s=-
t=0 0
a=group:BUNDLE 0 1
m=audio 9 UDP/TLS/RTP/SAVPF 111
c=IN IP4 0.0.0.0
a=rtcp:9 IN IP4 0.0.0.0
a=ice-ufrag:gA12
a=ice-pwd:8Jkz9RaNdOmPaSsWord...
a=fingerprint:sha-256 00:11:22:33:...  ← DTLS certificate fingerprint
a=setup:actpass
a=mid:0
a=sendrecv
a=rtpmap:111 opus/48000/2         ← Opus codec, 48kHz stereo
a=candidate:1 1 udp 2113667327 192.168.1.5 50000 typ host
a=candidate:2 1 udp 1677729535 203.0.113.5 50001 typ srflx raddr 192.168.1.5 rport 50000
m=video 9 UDP/TLS/RTP/SAVPF 96
a=rtpmap:96 VP8/90000
a=candidate:1 1 udp 2113667327 192.168.1.5 50002 typ host
```

**Key SDP fields**:
- `ice-ufrag`, `ice-pwd`: ICE credentials for the connectivity check STUN messages
- `fingerprint`: SHA-256 hash of the DTLS certificate — prevents MITM after ICE completes
- `rtpmap`: Codec → payload type mapping (Opus for audio, VP8/VP9/H.264/AV1 for video)
- `a=sendrecv`, `a=sendonly`, `a=recvonly`: Media direction

### 3.4 DTLS-SRTP — Encrypted Media

After ICE establishes the path, WebRTC uses **DTLS (Datagram TLS, RFC 6347)** to establish encryption. The DTLS certificate fingerprint in the SDP is the mutual verification mechanism (prevents MITM).

**SRTP (Secure Real-time Transport Protocol)** encrypts the RTP media streams using keys derived from the DTLS handshake.

```
ICE path established (UDP)
    ↓
DTLS handshake (mutual cert verification via fingerprint in SDP)
    ↓
SRTP keying material extracted from DTLS master secret
    ↓
RTP packets encrypted with SRTP (AES-128-CM + HMAC-SHA1)
    ↓
RTCP encrypted with SRTCP
```

### 3.5 DataChannel — Reliable and Unreliable Data over WebRTC

**WebRTC DataChannel** provides a bidirectional data channel over SCTP-over-DTLS-over-UDP:

```javascript
const dc = pc.createDataChannel("game-state", {
    ordered: false,      // unordered (UDP-like)
    maxRetransmits: 0    // no retransmits (fire and forget)
});

dc.onopen = () => {
    dc.send(JSON.stringify({x: 100, y: 200, frame: 1234}));
};

dc.onmessage = (event) => {
    const state = JSON.parse(event.data);
    updateGameState(state);
};
```

**SCTP partial reliability** options:
- `ordered: true, maxRetransmits: undefined` — fully reliable (like TCP)
- `ordered: false, maxRetransmits: 0` — unreliable, unordered (like UDP) — best for game positions
- `ordered: true, maxPacketLifeTime: 100` — reliable but expires after 100ms

---

## 📚 4. Protocol Decision Matrix

### 4.1 When to Use Each

| Protocol | Direction | Transport | Best Use Cases | Game/VR Use |
|---|---|---|---|---|
| **WebSocket** | Bidirectional | TCP (HTTP upgrade) | Chat, collaborative editing, game events, multiplayer lobby | Game lobby, authoritative events, position sync on reliable channel |
| **SSE** | Server → Client | HTTP/1.1 or HTTP/2 | Live notifications, LLM token stream, stock tickers | Game world events broadcast |
| **WebRTC Video/Audio** | Bidirectional P2P | UDP (DTLS-SRTP) | Video/audio calls, VR telepresence, screen share | VR avatar video streaming |
| **WebRTC DataChannel** | Bidirectional P2P | UDP (SCTP/DTLS) | Low-latency game state, P2P data transfer | Game position, physics state (unreliable ordered) |
| **WebTransport** | Bidirectional | QUIC (UDP) | Replacing WebSocket when low latency needed, game clients | Future-forward game clients; Chrome 114+ |

### 4.2 Game Netcode Pattern

```python
# Typical multiplayer game: mixed protocol usage
# 
# WebSocket (reliable TCP):
#   - Player join/leave events
#   - Chat messages
#   - Inventory changes (important, can't be missed)
#   - Match start/end state
#
# WebRTC DataChannel unreliable (UDP-like):
#   - Player position updates (30-60Hz)
#   - Mouse/joystick input
#   - Projectile spawns (send 3× for redundancy)
#
# WebRTC Audio track:
#   - Voice chat (Opus codec)
#
# Authoritative server pattern:
#   Client → Server: player input (WebSocket or DataChannel)
#   Server → All Clients: authoritative world state (WebSocket broadcast)
```

### 4.3 VR Streaming Pattern

For VR experiences with high-resolution video streaming:

```
Source (render server)
    │
    ├── H.264/H.265/AV1 encoded frame @ 90Hz
    │
    ▼
WebRTC Video Track (RTP/SRTP over UDP)
    │
    ├── NACK-based selective retransmit (miss a frame → request it)
    ├── FEC (Forward Error Correction) for packet loss resilience
    │
    ▼
Client VR headset
    ├── Hardware H.264 decode
    └── Reprojection (ATW/ASW) fills gap between 90Hz server and 120Hz display
```

Target latency for VR presence: **< 20ms glass-to-glass** (encode + network + decode + display). WebRTC's UDP-based delivery is the only protocol that can achieve this over the public Internet.

---

## 🛠️ 5. Worked Example — Minimal WebRTC Signaling

```javascript
// Both peers need a signaling channel to exchange SDP and ICE candidates.
// This example uses a simple WebSocket server as the signaling channel.

// --- PEER A ---
const pc_a = new RTCPeerConnection({
    iceServers: [
        { urls: 'stun:stun.l.google.com:19302' },
        { urls: 'turn:turn.example.com:3478', username: 'user', credential: 'pass' }
    ]
});

// Add local media
const stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: true });
stream.getTracks().forEach(track => pc_a.addTrack(track, stream));

// ICE candidates → send to peer B via signaling
pc_a.onicecandidate = (event) => {
    if (event.candidate) {
        signalingSocket.send(JSON.stringify({ type: 'candidate', candidate: event.candidate }));
    }
};

// Create offer
const offer = await pc_a.createOffer();
await pc_a.setLocalDescription(offer);
signalingSocket.send(JSON.stringify({ type: 'offer', sdp: offer }));

// On receiving answer from Peer B:
signalingSocket.onmessage = async (event) => {
    const msg = JSON.parse(event.data);
    if (msg.type === 'answer') {
        await pc_a.setRemoteDescription(new RTCSessionDescription(msg.sdp));
    } else if (msg.type === 'candidate') {
        await pc_a.addIceCandidate(new RTCIceCandidate(msg.candidate));
    }
};
```

---

## ⚠️ 6. Common Misconceptions

- **"WebSocket is always the right choice for real-time."** WebSocket requires a server in the middle. For P2P use cases (video calls, file transfer between clients), WebRTC DataChannel is lower-latency and cheaper to operate.
- **"STUN solves all NAT traversal."** STUN works for cone NATs (most home routers). Symmetric NAT (common in corporate networks) blocks STUN — you need TURN. Always provision a TURN server for production WebRTC.
- **"SDP is just configuration."** SDP is the contract between peers — change one field and the connection may fail or use a suboptimal codec. Understanding SDP is essential for debugging WebRTC issues.
- **"SSE doesn't work with HTTP/2."** SSE works excellently with HTTP/2 — each SSE stream is multiplexed as a separate HTTP/2 stream, so you don't need multiple TCP connections. HTTP/2 fixes SSE's scaling issue.
- **"WebRTC is browser-only."** WebRTC has native C++ libraries (libwebrtc), Go implementations (Pion WebRTC), and Python bindings. It's used in non-browser clients extensively.

---

## 🔗 7. Cross-Links & Further Reading

### Internal
- [3 (QUIC)](3-(QUIC)) — WebSocket runs over HTTP/1.1; SSE over HTTP/1.1 or HTTP/2
- [17.4 - TLS, mTLS & PKI](17.4---TLS,-mTLS-&-PKI) — TLS wraps WebSocket (WSS); DTLS wraps WebRTC
- [17.3 - TCP & UDP Deep Dive](17.3---TCP-&-UDP-Deep-Dive) — WebSocket is TCP; WebRTC DataChannel is UDP (SCTP/DTLS)
- [27.7 - Real-Time Systems](27.7---Real-Time-Systems) — CRDTs, presence, netcode patterns
- [Subject_Plan](Subject_Plan) — VR streaming architecture
- [Subject_Plan](Subject_Plan) — game netcode implementation

### External
- [WebRTC for the Curious (free book)](https://webrtcforthecurious.com/)
- [MDN WebRTC API](https://developer.mozilla.org/en-US/docs/Web/API/WebRTC_API)
- [RFC 6455 — The WebSocket Protocol](https://www.rfc-editor.org/rfc/rfc6455)
- [RFC 8445 — ICE](https://www.rfc-editor.org/rfc/rfc8445)
- [RFC 5389 — STUN](https://www.rfc-editor.org/rfc/rfc5389)
- [RFC 8656 — TURN](https://www.rfc-editor.org/rfc/rfc8656)
- [Pion WebRTC (Go native WebRTC library)](https://github.com/pion/webrtc)
- [aiortc (Python WebRTC)](https://github.com/aiortc/aiortc)
- [WebTransport spec (W3C)](https://www.w3.org/TR/webtransport/)

---

*Next: [17.7 - gRPC, Protocol Buffers & Service Mesh](17.7---gRPC,-Protocol-Buffers-&-Service-Mesh) — Efficient RPC for microservices.*
