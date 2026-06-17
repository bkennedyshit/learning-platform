---
title: "31.4 — Spatial Light Modulators & Holographic Displays: LCoS, DMD, Metasurfaces"
subject: "Holographics"
catalog: advanced
audience_tier: higher-education
chapter: "31.4"
type: chapter
objectives:
  - "Understand the concepts"
  - "Apply the theory"
open_source: true
---

*Back to [Subject_Plan](Subject_Plan) | Part of [00 - 09 - Learning Index](00---09---Learning-Index)*

# 31.4 — Spatial Light Modulators & Holographic Displays: LCoS, DMD, Metasurfaces

> *"The CGH solver writes the hologram. The SLM is the actual mouth that speaks it. Without SLMs, holography is theory; with them, it is a product."*

---

## 🎯 Learning Objectives

1. Compare the major **SLM modalities**: LCoS phase-only, DMD binary amplitude, MEMS piston, AOM, EOM.
2. Read SLM datasheet specs: pixel pitch, fill factor, frame rate, bit depth, addressing scheme.
3. Distinguish **amplitude-only**, **phase-only**, and **complex** modulation strategies.
4. Drive an SLM via **HOEYE / Meadowlark / Texas Instruments DLP** SDKs.
5. Recognize 2026 **metasurface-based SLMs** — the new frontier with tighter pixel pitch + multifunctional behavior (per Nature Nanotechnology 2026 work).
6. Understand the role of **holographic optical elements (HOEs)** + **photopolymer films** (Bayfol HX) in modern AR optics.

---

## 🖼️ Visual Anchor

![holo__23.4-fig1](holo__23.4-fig1.svg)

> *Picture / video reference (external):*
> - 📺 [HOLOEYE Photonics — SLM SDK & devices](https://holoeye.com/)
> - 📺 [Meadowlark Optics — phase-only SLMs](https://www.meadowlark.com/)
> - 📺 [TI DLP Lightcrafter (DMD)](https://www.ti.com/dlp-chip/overview.html)
> - 📺 [Phys.org — Metasurface-based SLM (2026)](https://phys.org/news/2026-02-metasurface-based-slm-ar-vr.html)

---

## 📚 1. SLM Modality Comparison

| Type | Modulates | Speed | Strengths | Weaknesses |
|---|---|---|---|---|
| **LCoS phase-only** | Phase 0–2π | 60–360 Hz | Low loss, dense pixels | Slow vs DMD; polarization-sensitive |
| **LCoS amplitude** | Amplitude 0–1 | 60–360 Hz | Easy intensity control | Loses 50%+ of light |
| **DMD (TI DLP)** | Binary amplitude | up to 32 kHz binary | Very fast | Binary only → dithering needed for grayscale |
| **MEMS piston** | Phase via micro-mirror travel | kHz | Wide-spectrum | Few prototypes commercial |
| **AOM (Acousto-Optic)** | Beam deflection | MHz–GHz | Very fast scanners | Single-axis, narrow band |
| **EOM (Electro-Optic)** | Phase, fast | GHz | Beam steering | Costly |
| **Metasurface SLM (2026)** | Phase + amplitude + spectral | Variable | Sub-wavelength pixels, multifunctional | Research stage |

> Source: [Phys.org — Metasurface-based SLM 2026](https://phys.org/news/2026-02-metasurface-based-slm-ar-vr.html) — content rephrased for compliance.

---

## 🔬 2. Datasheet Vocabulary

- **Pixel pitch** — center-to-center spacing (8 μm typical for LCoS, 5–17 μm for DMD).
- **Fill factor** — fraction of pixel that's active (>90% for LCoS, ~92% for DMD).
- **Frame rate** — refresh rate; phase-only LCoS often 60 Hz, fast variants 360+ Hz.
- **Bit depth** — phase levels (8-bit = 256 levels = 0…2π in steps of ~0.025 rad).
- **Diffraction efficiency** — fraction of incident light into desired order.
- **Active area** — physical display extent (e.g., 15.36 × 9.6 mm for a 1080p LCoS).

---

## 🧮 3. Modulation Strategies

| Strategy | Implementation | Trade-off |
|---|---|---|
| Phase-only | Use only $\arg(u)$ | Need GS / SGD / encoding |
| Amplitude-only | Use only $|u|$ | Loses phase info, 4× resolution loss for full image |
| **Complex via dual SLM** | One amplitude + one phase | Complex alignment |
| **Complex via single LCoS (LCoS-SLM)** | Modulate AM + PM in one device using polarization manipulation | Active 2026 research |
| **Time multiplexing** | Several phase patterns per frame | Frame rate divided |

> Source: [Holographic Display with Both AM + PM in single LCoS-SLM (2024 conference)](https://www.researchgate.net/publication/379900038) — content rephrased for compliance.

---

## 🪞 4. HOEs and Photopolymer Films

A **Holographic Optical Element (HOE)** is a static volume hologram that acts as a beam combiner, lens, or grating. **Bayfol HX** photopolymer films are the modern medium of choice. Used in:
- HoloLens 2 (waveguide combiners — see [31.6](31.6---Holographic-AR---HoloLens,-Magic-Leap,-Waveguides-&-the-Marketing-vs-Physics-Gap)).
- Heads-up displays.
- Solar concentrators.

---

## 🛠️ 5. Worked Example (skeleton) — Drive an HOEYE SLM with a Computed Phase Mask

1. Compute a phase mask in NumPy (from [31.3](31.3---Computer-Generated-Holography---Algorithms,-FFT,-Neural-CGH)).
2. Quantize to 8-bit (0–255 → 0–2π).
3. Load via HOLOEYE SDK Python wrapper: `slm.show_phaseimage(np_array)`.
4. Illuminate with a green laser through a beam expander.
5. Verify reconstruction at the target plane with a CCD.

---

## 🔗 6. Cross-links & Further Reading

### Internal
- [31.3 - Computer-Generated Holography - Algorithms, FFT, Neural CGH](31.3---Computer-Generated-Holography---Algorithms,-FFT,-Neural-CGH)
- [31.6 - Holographic AR - HoloLens, Magic Leap, Waveguides & the Marketing-vs-Physics Gap](31.6---Holographic-AR---HoloLens,-Magic-Leap,-Waveguides-&-the-Marketing-vs-Physics-Gap)
- [21.6 - Motherboards & Computer Architecture - CPU, RAM, Chipset, PCIe, UEFI](21.6---Motherboards-&-Computer-Architecture---CPU,-RAM,-Chipset,-PCIe,-UEFI) — driver electronics

### External
- [HOLOEYE Photonics](https://holoeye.com/)
- [Meadowlark Optics](https://www.meadowlark.com/)
- [TI DLP](https://www.ti.com/dlp-chip/overview.html)
- [Bayfol HX product page (Covestro)](https://solutions.covestro.com/en/products/bayfol/bayfol-hx)
- [Phys.org — Metasurface-based SLM (2026)](https://phys.org/news/2026-02-metasurface-based-slm-ar-vr.html)
- [Stanford Wetzstein Lab — display papers](https://www.computationalimaging.org/)

---

## ⚠️ 7. Common Misconceptions

- **"All SLMs are the same chip with different software."** Different modulation modalities require different optical setups + algorithms.
- **"Faster = always better."** Faster SLMs draw more power and may have lower diffraction efficiency. Pick by the *eye-rate* you need.
- **"Pixel pitch is the only thing that matters."** Diffraction efficiency, polarization purity, and uniformity matter equally.
- **"Metasurfaces will replace LCoS tomorrow."** Promising, but as of 2026 commercial deployment is limited. Expect 5–10 years to broad adoption for full-frame displays.
