---
title: "35.5 — Mixing Fundamentals"
subject: "Music Production & Sound Design"
catalog: advanced
audience_tier: higher-education
chapter: "35.5"
type: chapter
objectives:
  - "Understand the concepts"
  - "Apply the theory"
open_source: true
---

*Back to [Subject_Plan](Subject_Plan) | Part of [00 - 09 - Learning Index](00---09---Learning-Index)*

# 35.5 — Mixing Fundamentals

> *"Mixing is the art of making every element audible, every element purposeful, and the whole greater than the sum of its parts."*

---

## 🎯 Learning Objectives

1. Apply the frequency spectrum map to correctly place instruments in the mix.
2. Use subtractive EQ to remove resonances and high-pass filter every track appropriately.
3. Set compression parameters (threshold, ratio, attack, release, make-up gain) for kick, snare, and vocal.
4. Create a clean stereo field: mono centre, controlled stereo width, bass in mono below 150Hz.
5. Use a spectrum analyser (SPAN, free) and A/B reference track to evaluate a mix.
6. Check mono compatibility and identify phase issues.

---

## 🖼️ Visual Anchor

![music__35.5-fig1](music__35.5-fig1.svg)

---

## 📚 1. The Frequency Spectrum in a Mix

**The fundamental rule:** Every instrument occupies frequency space. When two instruments occupy the same frequency space at similar levels, they **mask** each other. Mixing is space management.

### 1.1 Frequency Regions

| Region | Hz range | Instruments | Common issues |
|--------|---------|------------|---------------|
| Sub bass | 20–80 Hz | 808, sub bass synth, kick body | Muddy if not controlled; mono only |
| Bass | 80–250 Hz | Bass guitar/synth body, kick fundamental | Competing with bass and kick |
| Low-mid | 250 Hz–1 kHz | Body of guitar, piano, snare warmth | "Mud zone" — most common over-accumulation |
| Mid | 1–4 kHz | Vocals, guitar presence, snare crack | Presence vs harshness |
| Upper-mid | 4–8 kHz | Drum attack, consonants, guitar bite | Sibilance, harshness |
| Presence | 8–12 kHz | Cymbals, vocal air, guitar clarity | Sharpness |
| Air | 12–20 kHz | Breathiness, sheen, "sparkle" | Noise floor; don't boost if not present |

---

## 📚 2. EQ Techniques

### 2.1 EQ Types

**Dynamic EQ:** Q and gain change based on input level — only cuts/boosts when the problem frequency becomes prominent. Precise surgical tool.

**Linear phase EQ:** Applies equal phase shift to all frequencies (vs minimum phase which has different phase shift per frequency). Use on buses for transparent EQ. Adds latency.

**Analog-modelling EQ (Neve, SSL, API):** Coloured, adds harmonic character. For creative adds.

### 2.2 Subtractive First, Additive Second

**Rule:** Always remove problems before adding colour.

**Surgical EQ workflow:**
1. Boost a narrow band (Q=8–10) significantly (+12 dB)
2. Sweep through the frequency range slowly
3. When you hear a resonance, harsh peak, or boxiness — stop
4. Cut that frequency (reduce gain to -3 to -8 dB)
5. Widen the Q (0.5–2.0) for a natural-sounding reduction
6. Repeat for all problem frequencies

### 2.3 High-Pass Filtering (HPF) on Every Track

**One of the biggest improvements you can make to a mix:**

```
Every track except kick and bass bass:
Apply high-pass filter to remove low frequencies that don't belong
```

| Track | HPF frequency |
|-------|-------------|
| Kick | 20–30 Hz (remove infrasub) |
| 808/sub bass | 30 Hz |
| Bass guitar | 40–50 Hz |
| Drums (snare, hats) | 80–100 Hz |
| Piano/Rhodes | 60–80 Hz |
| Acoustic guitar | 100–120 Hz |
| Electric guitar | 80–100 Hz |
| Synth pad | 100–150 Hz |
| Lead synth | 200–300 Hz (situational) |
| Vocal | 80–100 Hz |
| String section | 60–80 Hz |

**Why:** Low frequencies are where sub energy accumulates. If 12 tracks all have sub-frequency content below 80Hz (even at small levels), the sum is a muddy wash that leaves no room for the actual bass elements.

---

## 📚 3. Compression

### 3.1 What Compression Does

A compressor **reduces the dynamic range** of a signal — making loud parts quieter relative to quiet parts, then you apply **make-up gain** to bring the overall level back up.

**Key parameters:**
- **Threshold:** The level above which compression starts (-20 dBFS for subtle, -5 dBFS for limiting)
- **Ratio:** How much the level above threshold is reduced (2:1 = gentle, 4:1 = medium, 8:1 = hard, ∞:1 = brick wall limiter)
- **Attack:** How quickly compression kicks in after threshold is crossed (1ms = kill transient, 50ms = let transient through)
- **Release:** How quickly gain returns to normal after signal drops below threshold (50ms = tight, 500ms = breathing, auto = smart)
- **Make-up gain:** Compensate level lost from compression
- **Knee:** Soft knee = gradual compression onset (transparent), Hard knee = abrupt onset (punchy)

### 3.2 Instrument-Specific Settings

**Kick drum:**
- Threshold: -8 to -12 dBFS
- Ratio: 4:1
- Attack: 1–5ms (fast = tighter punch; slow = more click and transient)
- Release: 50–80ms
- Make-up: +3–4 dB
- Goal: controlled, punchy transient with consistent body

**Snare:**
- Ratio: 4:1
- Attack: 5–10ms (let initial attack through)
- Release: 80–150ms
- Make-up: +2–3 dB

**Vocal:**
- Ratio: 2:1 to 3:1
- Attack: 8–12ms (preserve natural attack)
- Release: 150–300ms or auto
- GR: -3 to -6 dB average
- Often use two passes: first compressor for peaks, second for dynamic consistency

**Bus compression (glue):**
- Ratio: 1.5:1 to 2:1
- Very slow attack (50–100ms)
- Medium release (300ms)
- GR: 1–3 dB
- Goal: cohesion, not audible compression

### 3.3 Parallel Compression (New York Compression)

Blend heavily compressed signal (ratio 8:1+, attack 0ms) with uncompressed signal.

**Effect:** Preserves transient punch while adding sustained body and density. Subtle but powerful on drums.

---

## 📚 4. Stereo Field

### 4.1 Placement Rules

| Element | Placement | Why |
|---------|-----------|-----|
| Kick | Centre | Maximum energy transfer, mono compatibility |
| Bass / 808 | Centre (LP to mono below 150Hz) | Bass is non-directional below 80Hz; phase issues in mono |
| Lead vocal | Centre | The listener's anchor |
| Snare | Centre (or very slight) | Punch needs mono |
| Hi-hats | 30–40% L or R (alternating or fixed) | Width without center competition |
| Pad/chords | Wide (L–R pair or stereo widener) | Creates the "wall of sound" behind focal elements |
| Backing vocals | Panned opposite pairs (-30/+30) | Stereo support without masking lead |
| Reverb returns | Leave in stereo | Creates the sense of acoustic space |

### 4.2 Low-End Mono Rule

**Apply Low-pass-to-mono processing below 150Hz on all wide/stereo tracks.**

Why: Bass frequencies are not directional to human hearing. Stereo bass creates phase cancellation when summed to mono (streaming, one speaker, phone). All the sub energy can vanish in mono.

**In practice:** Mid/Side EQ plugin — cut the Side channel below 150Hz while leaving the Mid alone. Result: clean, solid low end that's mono-compatible.

### 4.3 Mono Check

Before finalising a mix, fold everything to mono (most DAWs have a mono button):
- Can you hear all the elements clearly?
- Does the kick still punch?
- Does the bass have body?
- Has the snare disappeared? (phase issue!)

If elements disappear in mono, there's a phase relationship problem. Common fixes: time-align samples, invert phase on one channel, reposition sample triggers.

---

## 🛠️ 5. Worked Example — Reference Track Comparison

**Step 1:** Find a commercial track in the same genre with a mix you admire. Import it into your DAW.

**Step 2:** Level-match: bring reference track to same perceived loudness as your mix (use SPAN to compare integrated LUFS — both should be roughly equal for fair comparison).

**Step 3:** A/B switch between your mix and reference:
- Does your mix have more or less sub bass?
- Is your mix brighter or darker in the high-mids?
- Is your stereo width similar?
- Does your kick have similar punch?

**Step 4:** Make corrections. A/B again.

**The key insight:** Reference mixing is not copying — it's calibrating your perception. Every room sounds different. Every set of headphones colours frequency response differently. The reference anchors your decisions to a known good standard.

---

## ⚠️ 6. Common Misconceptions

1. **"More EQ boost = better sound."** Boosting creates narrow peaks that can sound harsh and compete with other frequencies. Subtle boosts (2–4 dB, wide Q) are the limit for most mixing EQ decisions.

2. **"Compression makes everything louder and better."** Compression reduces dynamics. Overcompression makes music feel flat, lifeless, and fatiguing. The goal is control and cohesion, not maximum density.

3. **"My mix should be as loud as possible before mastering."** Mix at -6 dBFS peak headroom minimum. The mastering engineer (or limiter) needs headroom to work. A mix that's already hitting 0 dBFS has no room for mastering.

4. **"Panning to the sides makes a mix wide."** True wideness comes from stereo CONTENT (two different audio signals) — not just panning the same mono signal hard left and right. That creates a Haas effect illusion that breaks down in mono.

5. **"Once EQ'd once, the track is done."** Mix elements interact. When you change the kick EQ, the bass may need adjustment. When you add the vocal, the piano may need to be cut in the mid-range. Mixing is iterative, holistic, and never happens in solo mode.

6. **"Attack fast = more compression."** Attack fast = MORE compression on transients. Attack slow = LESS compression on transients (lets them through). Slow attack with high ratio = punchy, transient-forward sound. Fast attack with high ratio = squashed, controlled.

---

## 🔗 7. Cross-links & Further Reading

### Internal
- [35.6 - Mastering & Loudness](35.6---Mastering-&-Loudness) — what comes after mixing

### External
- [SPAN free spectrum analyser (Voxengo)](https://www.voxengo.com/product/span/)
- [Youlean Loudness Meter 2 (free)](https://youlean.co/youlean-loudness-meter/)
- [In The Mix YouTube — mixing tutorials](https://www.youtube.com/@InTheMix)
- [Ian Shepherd Mastering Media podcast](https://www.mastthemix.com/)

---

*Prev: [35.4 - Sampling, Slicing & Resampling](35.4---Sampling,-Slicing-&-Resampling) | Next: [35.6 - Mastering & Loudness](35.6---Mastering-&-Loudness)*
