---
title: "31.2 — Classical Holography: Gabor, Denisyuk, Transmission & Reflection"
subject: "Holographics"
catalog: advanced
audience_tier: higher-education
chapter: "31.2"
type: chapter
objectives:
  - "Understand the concepts"
  - "Apply the theory"
open_source: true
---

*Back to [Subject_Plan](Subject_Plan) | Part of [00 - 09 - Learning Index](00---09---Learning-Index)*

# 31.2 — Classical Holography: Gabor, Denisyuk, Transmission & Reflection

> *"Before computers, we recorded waves on silver halide. Understanding the original setups makes the algorithms in 31.3 obvious — they're just lab procedures translated into code."*

---

## 🎯 Learning Objectives

1. Describe **Gabor's in-line geometry** (1948 Nobel) and its limitations.
2. Describe the **Leith-Upatnieks off-axis transmission** geometry that solved Gabor's twin-image problem.
3. Describe **Denisyuk reflection holograms** (white-light viewable, no laser needed for playback).
4. Distinguish **thin** (amplitude) vs **thick / volume** (Bragg) holograms; Bragg condition.
5. Recognize **rainbow holograms** (Benton) and **embossed holograms** (the credit-card variety) as practical mass-production methods.
6. Identify the recording materials: silver halide, dichromated gelatin, photopolymers, photorefractives.

---

## 🖼️ Visual Anchor

![holo__23.2-fig1](holo__23.2-fig1.svg)

> *Picture / video reference (external):*
> - 📺 [MIT MAS.450 lectures + lab videos](https://ocw.mit.edu/courses/mas-450-holographic-imaging-spring-2003/)
> - 📺 [International School of Holography curriculum](https://www.internationalschoolofholography.com/)

---

## 📚 1. Gabor's In-Line Hologram (1948)

Setup:
- Single laser beam.
- Object is a **thin transparent** scatterer.
- Reference = the unscattered beam.
- Recording medium catches both.

Problem: the **twin image** appears collinear with the real reconstruction → blurred views.

This won Gabor the Nobel Prize in 1971 anyway — the conceptual breakthrough was that you can record both phase + amplitude on an intensity-only medium.

---

## 🛤️ 2. Leith-Upatnieks Off-Axis Transmission (1962)

Setup (the iconic textbook diagram):
- Beam splitter splits laser into reference + object beams.
- Object beam scatters off the (reflective or transmissive) object onto the plate.
- Reference beam hits the plate **at an angle**.
- Off-axis geometry separates the twin image angularly during reconstruction → clean reconstruction in one diffraction order.

**Reconstructs by transmission:** illuminate plate with the reference and view the diffracted real / virtual image on the other side.

---

## 🪞 3. Denisyuk Reflection Hologram (1962)

Setup:
- Reference beam passes *through* the photographic plate.
- Object behind the plate scatters light back.
- Reference + scattered waves interfere **inside the emulsion thickness** → volumetric Bragg planes.

**Plays back in white light:** the Bragg planes auto-select the recorded wavelength. This is what makes "decorative" holograms (gift cards, security stickers) viewable without a laser.

The bandwidth of the playback is set by the Bragg condition:
$$
2d_{Bragg}\sin\theta = m\lambda
$$

---

## 🌈 4. Rainbow & Embossed Holograms

### Rainbow (Benton, 1969)
A two-step process that limits vertical parallax to gain bright, white-light reconstruction with chromatic dispersion (the rainbow). Used widely in art prints, promotional cards.

### Embossed
Master hologram → nickel shim → roll-emboss into a metallized plastic. **Mass production** at fractions of a cent each — credit-card security holograms, packaging.

---

## 🧪 5. Recording Materials

| Material | Resolution | Sensitivity | Notes |
|---|---|---|---|
| Silver halide | 5000+ lp/mm | High | Wet-process; classical |
| Dichromated gelatin (DCG) | 5000+ lp/mm | Low | Bright reflection holograms |
| Photopolymer (Du Pont, Bayfol HX) | 4000+ lp/mm | Medium | Dry-process; modern AR/VR optics use it for HOEs |
| Photorefractive (LiNbO₃, BSO) | 5000+ lp/mm | Variable | Real-time / dynamic |
| Photoresist | – | – | For embossed-master fabrication |

---

## 🛠️ 6. Worked Example (skeleton) — Predict Reconstruction Wavelength of a Denisyuk Hologram

Given:
- Recording wavelength $\lambda_{rec} = 532$ nm (green Nd:YAG SHG).
- Emulsion shrinkage during processing → Bragg layer spacing $d$ shrinks ~10%.

Predict playback wavelength:
$$
\lambda_{play} \approx 0.9 \times 532\,\text{nm} \approx 480\,\text{nm}
$$
(blue) — which matches what you typically see when a Denisyuk is processed in standard developers without expansion to compensate.

---

## 🔗 7. Cross-links & Further Reading

### Internal
- [31.1 - Optics Foundations - Interference, Diffraction, Coherence, Fourier Optics](31.1---Optics-Foundations---Interference,-Diffraction,-Coherence,-Fourier-Optics)
- [31.3 - Computer-Generated Holography - Algorithms, FFT, Neural CGH](31.3---Computer-Generated-Holography---Algorithms,-FFT,-Neural-CGH)
- [31.4 - Spatial Light Modulators & Holographic Displays - LCoS, DMD, Metasurfaces](31.4---Spatial-Light-Modulators-&-Holographic-Displays---LCoS,-DMD,-Metasurfaces)

### External
- [MIT MAS.450](https://ocw.mit.edu/courses/mas-450-holographic-imaging-spring-2003/pages/syllabus)
- [International School of Holography curriculum](https://www.internationalschoolofholography.com/)
- *Holography Handbook* — Unterseher, Hansen, Schlesinger (the practitioner's bible)
- *Optical Holography* — Collier, Burckhardt, Lin (canonical)
- *Optical Holography — Principles, Techniques and Applications* — Hariharan

---

## ⚠️ 8. Common Misconceptions

- **"Holograms always need a laser to view."** Reflection (Denisyuk) and embossed holograms work under white light.
- **"Holograms record images."** They record interference patterns. The image is reconstructed by the diffraction of the reference during playback.
- **"Hologram = Princess Leia."** That's volumetric / aerial display, not a hologram in the classical optical sense. (See [31.6](31.6---Holographic-AR---HoloLens,-Magic-Leap,-Waveguides-&-the-Marketing-vs-Physics-Gap).)
- **"Higher-resolution film = better hologram."** True only up to a point — recording bandwidth is set by the angle between reference and object beams.
