---
title: "04.2 — Fourier Series & Fourier Transform"
subject: "Signal Processing & DSP"
catalog: advanced
audience_tier: higher-education
chapter: "04.2"
type: chapter
objectives:
  - "Understand the concepts"
  - "Apply the theory"
open_source: true
---

*Back to [Subject_Plan](Subject_Plan) | Part of [00 - 09 - Learning Index](00---09---Learning-Index)*

# 04.2 — Fourier Series & Fourier Transform

> *"The most surprising fact in all of mathematics may be that any function, however complicated, can be expressed as a sum of the simplest possible oscillations."* — paraphrased from Körner, *Fourier Analysis*

The Fourier Transform is the lens through which all of DSP is understood. When you open a spectrogram in Audacity, view a pitch detection output, examine mel features for Whisper, or design a filter — you are always looking at the result of Fourier analysis. This chapter builds that lens from scratch.

Related chapters: [04.1](04.1---Signals,-Systems-&-Sampling-Theory) (what signals are), [04.3](04.3---Discrete-Fourier-Transform-&-FFT) (computing it efficiently), [04.5](04.5---Audio-Signal-Processing-&-Psychoacoustics) (applying it to audio AI).

---

## 🎯 Learning Objectives

By the end of this chapter you will be able to:

1. Compute the **Fourier Series** coefficients for a periodic signal and state the Dirichlet convergence conditions.
2. Write the **Fourier Transform** pair (analysis/synthesis equations) and apply them.
3. Derive and use the four most important **transform pairs**: rect↔sinc, Gaussian↔Gaussian, δ(t)↔1, e^{jω₀t}↔δ(ω−ω₀).
4. Apply the **Convolution Theorem**: multiplication in time ↔ convolution in frequency.
5. State and use **Parseval's Theorem** to calculate signal energy without time-domain integration.
6. Work through the concrete example: find the spectrum of a **440 Hz + 880 Hz** mixed sine wave.
7. Explain the **Gibbs phenomenon** and why it matters for windowing (preview to [04.3](04.3---Discrete-Fourier-Transform-&-FFT)).

---

## 🖼️ Visual Anchor

![dsp-04__fig2](dsp-04__fig2.svg)

*Diagram: Left — Fourier Series formula and convergence. Middle — Fourier Transform pair and key pairs table. Right — Convolution Theorem. Bottom — time-domain plot of 440 Hz + 880 Hz mix and their two-spike frequency-domain spectrum.*

---

## 📚 1. Fourier Series — Decomposing Periodic Signals

### 1.1 Statement

Any periodic function f(t) with period T, satisfying the **Dirichlet conditions**, can be written as an infinite sum of complex exponentials (sinusoids):

```
f(t) = Σ_{n=−∞}^{∞}  cₙ · e^{j2πnt/T}
```

where the **Fourier coefficients** are:

```
cₙ = (1/T) ∫₀ᵀ f(t) · e^{−j2πnt/T} dt
```

- n = 0: DC component (mean value of f(t))
- n = ±1: fundamental frequency f₁ = 1/T
- n = ±2: second harmonic, f₂ = 2/T
- n = ±k: k-th harmonic, fₖ = k/T

The **real-valued** form using cosines and sines (for real-valued f(t)):

```
f(t) = a₀/2 + Σ_{n=1}^{∞} [aₙ cos(2πnt/T) + bₙ sin(2πnt/T)]
```

where aₙ = 2·Re(cₙ), bₙ = −2·Im(cₙ).

### 1.2 Dirichlet Conditions (Convergence)

The Fourier Series converges to f(t) at every point of continuity if:
1. f(t) is **absolutely integrable** over one period: ∫₀ᵀ |f(t)| dt < ∞
2. f(t) has a **finite number of maxima and minima** in one period.
3. f(t) has a **finite number of finite discontinuities** in one period.

These conditions hold for virtually every physical signal (voltages, pressures, currents). Mathematical pathologies like the Weierstrass function do not satisfy them but never appear in real DSP work.

### 1.3 Gibbs Phenomenon

At a **jump discontinuity** (like a square wave), the Fourier Series truncated at N harmonics **overshoots** the true value by approximately 9% of the jump height, regardless of how many terms you add. This overshoot does not go away as N → ∞ — it just narrows. This is the **Gibbs phenomenon**, and it is why:
- Rectangular windows on DFT cause high **spectral sidelobes** (see [04.3](04.3---Discrete-Fourier-Transform-&-FFT))
- Audio processing uses **smooth windows** (Hann, Hamming) to reduce the effect

### 1.4 Worked Example: Square Wave Fourier Series

Square wave: f(t) = +1 for 0 < t < T/2, −1 for T/2 < t < T.

**DC component c₀:**
```
c₀ = (1/T) ∫₀ᵀ f(t) dt = 0   (symmetric around zero)
```

**n-th coefficient (n odd):**
```
cₙ = 2 / (jπn)   for n odd
cₙ = 0           for n even, n ≠ 0
```

So the square wave = (4/π)[sin(ωt) + sin(3ωt)/3 + sin(5ωt)/5 + …]

Only **odd harmonics** with amplitude falling as 1/n. This is why a square wave sounds "buzzy" — it has rich harmonic content at all odd overtones.

---

## 📚 2. The Fourier Transform — Aperiodic Signals

The Fourier Series works for periodic signals. The **Fourier Transform** extends this to any aperiodic signal by taking T → ∞ (period becomes infinite, fundamental frequency → 0, harmonics become a continuum of frequencies).

### 2.1 The Transform Pair

**Analysis (time → frequency):**
```
F(ω) = ∫_{−∞}^{∞} f(t) · e^{−jωt} dt     (ω = 2πf in rad/s)
```

**Synthesis (frequency → time):**
```
f(t) = (1/2π) ∫_{−∞}^{∞} F(ω) · e^{jωt} dω
```

**Alternate convention (engineering, using f in Hz, symmetric):**
```
F(f) = ∫_{−∞}^{∞} f(t) · e^{−j2πft} dt
f(t) = ∫_{−∞}^{∞} F(f) · e^{j2πft} df
```

> Note: the convention changes the 1/2π factor placement. In NumPy's `fft`, the convention is the first (ω-based) with n as the variable; always check the documentation when mixing frameworks.

### 2.2 Physical Interpretation

- **|F(f)|** (magnitude spectrum): how much amplitude is present at each frequency f.
- **∠F(f)** (phase spectrum): the phase offset of each frequency component.
- **|F(f)|²** (power spectrum): power at each frequency — what you see in a spectrogram.
- **F(f)** is generally **complex-valued** even when f(t) is real-valued.

For real-valued f(t): F(f) = F*(−f) — the spectrum is **conjugate symmetric**; the negative-frequency side is a mirror of the positive side. This is why we only plot f ≥ 0 in practice (the "one-sided spectrum").

---

## 📚 3. Key Transform Pairs

These four pairs are used constantly in DSP and filter design. Derive them from the definition at least once — then memorize them.

### 3.1 Rectangular Pulse ↔ Sinc Function

```
rect(t/τ)  ⟺  τ · sinc(fτ)
```

where rect(t/τ) = 1 for |t| < τ/2, 0 otherwise, and sinc(x) = sin(πx)/(πx).

**Why it matters:** A finite-duration observation window (multiplying a signal by rect to "look" at only T seconds) convolution its spectrum with a sinc function. This creates **spectral leakage** — energy from one frequency spreads into neighboring bins. This is the fundamental problem that windowing addresses.

### 3.2 Gaussian ↔ Gaussian

```
e^{−πt²}  ⟺  e^{−πf²}
```

The Gaussian function is its own Fourier Transform. A narrow Gaussian in time gives a *wide* Gaussian in frequency, and vice versa. This is the mathematical expression of the **time-frequency uncertainty principle**:

```
σ_t · σ_f ≥ 1/(4π)
```

You cannot have both arbitrary time precision and arbitrary frequency precision simultaneously. This is why you cannot see a 10 Hz sine wave in a 5 ms window — the window is too short.

### 3.3 Dirac Delta ↔ Flat Spectrum

```
δ(t)  ⟺  1     (all frequencies equally)
1     ⟺  δ(f)  (pure DC has a single spike at f=0)
```

**Why it matters:** The impulse response of an LTI system is h(t), and its Fourier Transform H(f) is the **frequency response** (transfer function). Feeding δ(t) reveals all frequency content at once.

### 3.4 Complex Exponential ↔ Frequency Shift

```
e^{j2πf₀t}  ⟺  δ(f − f₀)
```

A pure sinusoid at frequency f₀ exists *only* at one point in the frequency domain — a spike (impulse) at f₀. This is the mathematical justification for the claim "a pure tone has a single frequency."

For a real cosine:
```
cos(2πf₀t) = (e^{j2πf₀t} + e^{−j2πf₀t}) / 2
            ⟺  (δ(f − f₀) + δ(f + f₀)) / 2
```
Two spikes: one at +f₀, one at −f₀ (the conjugate-symmetric mirror).

---

## 📚 4. Properties of the Fourier Transform

### 4.1 Linearity

```
α·f(t) + β·g(t)  ⟺  α·F(f) + β·G(f)
```

### 4.2 Time Shift

```
f(t − t₀)  ⟺  e^{−j2πft₀} · F(f)
```

Shifting in time multiplies the spectrum by a **linear phase** e^{−j2πft₀}. The **magnitude** spectrum is unchanged; only the phase changes. This is why linear-phase filters are preferred in audio — they delay all frequencies equally (no phase distortion, no "pre-ringing" in the perceptible sense).

### 4.3 Frequency Shift (Modulation)

```
e^{j2πf₀t} · f(t)  ⟺  F(f − f₀)
```

Multiplying in time by a complex exponential **shifts the spectrum** — this is AM modulation.

### 4.4 Duality

```
If f(t) ⟺ F(f),  then F(t) ⟺ f(−f)
```

### 4.5 Scaling

```
f(at)  ⟺  (1/|a|) · F(f/a)
```

Compressing in time (a > 1) expands in frequency, and vice versa. **Faster speech = higher-pitched and broader spectrum.** This is why pitch-shifting algorithms that naively time-compress audio also shift the formants incorrectly.

---

## 📚 5. The Convolution Theorem

This is the **most practically important property** in all of DSP:

```
Convolution theorem:
    x(t) * y(t)   ⟺   X(f) · Y(f)
    x(t) · y(t)   ⟺   X(f) * Y(f)
```

**Convolution in time = multiplication in frequency.**  
**Multiplication in time = convolution in frequency.**

### 5.1 Why This Changes Everything

A filter with impulse response h(t) produces output y(t) = x(t) * h(t). In the frequency domain:

```
Y(f) = X(f) · H(f)
```

To filter a signal, just **multiply the spectra**. Instead of computing the full convolution integral (O(N²) operations), you can:

1. FFT(x) → X  (O(N log N))
2. FFT(h) → H  (O(N log N))
3. Y = X · H   (O(N) element-wise multiply)
4. IFFT(Y) → y (O(N log N))

Total: **O(N log N)** instead of O(N²). For N = 1 million, that is a factor of ~50 000× faster. This is the **overlap-add** and **overlap-save** algorithms used in every audio effects engine.

### 5.2 Design Implication

This also means you can *design* a filter in the frequency domain: draw the shape of H(f) you want (lowpass, highpass, arbitrary equalizer curve), IFFT to get h(t), then window the result to get a practical FIR filter. This is the **frequency-sampling method** of FIR filter design.

---

## 📚 6. Parseval's Theorem — Energy Conservation

```
∫_{−∞}^{∞} |f(t)|² dt  =  ∫_{−∞}^{∞} |F(f)|² df
```

The **total energy** of a signal is the same whether calculated in the time domain or the frequency domain. Energy is conserved under the Fourier Transform.

### 6.1 Why It Matters for DSP

1. **Filter attenuation is energy loss.** A lowpass filter that removes high frequencies reduces the total signal energy by the amount of energy above the cutoff.
2. **Spectrogram energy sums.** If you sum the power across all bins of a log-mel spectrogram, you get (proportionally) the total signal power.
3. **Normalization.** When comparing FFT outputs of different lengths N, energy scales with N. Use 1/N normalization consistently.

For discrete signals (DFT):
```
Σₙ |x[n]|² = (1/N) Σₖ |X[k]|²
```

---

## 📚 7. Worked Example — Spectrum of 440 Hz + 880 Hz

**Problem:** Signal x(t) = A₁ sin(2π · 440 · t) + A₂ sin(2π · 880 · t), where A₁ = 1.0 and A₂ = 0.5. Find X(f).

**Step 1 — Express as complex exponentials:**

```
sin(2πf₀t) = (e^{j2πf₀t} − e^{−j2πf₀t}) / (2j)
```

So:
```
x(t) = (A₁/2j)[e^{j2π·440·t} − e^{−j2π·440·t}]
     + (A₂/2j)[e^{j2π·880·t} − e^{−j2π·880·t}]
```

**Step 2 — Apply transform pair e^{j2πf₀t} ↔ δ(f − f₀):**

```
X(f) = (A₁/2j)[δ(f−440) − δ(f+440)]
     + (A₂/2j)[δ(f−880) − δ(f+880)]
```

**Step 3 — Compute magnitude spectrum |X(f)|:**

```
|X(f)| = A₁/2 · δ(f±440)  +  A₂/2 · δ(f±880)
       = 0.5 at f = ±440 Hz
       = 0.25 at f = ±880 Hz
       = 0 everywhere else
```

**Physical interpretation:** The frequency domain contains exactly four impulses — at ±440 Hz and ±880 Hz. The one-sided spectrum (f ≥ 0) shows two spikes at 440 Hz and 880 Hz with heights 0.5 and 0.25 respectively. This is exactly what an FFT of a recorded A4 note plus its octave would show.

**Step 4 — Verify with Parseval's theorem:**

Time domain energy over one period T of the fundamental (T = 1/440 s):
```
E = ∫₀ᵀ |x(t)|² dt = A₁²/2 · T + A₂²/2 · T = (1/2 + 0.125) · T
```

Frequency domain energy:
```
∫ |X(f)|² df = (A₁/2)² · 2 + (A₂/2)² · 2 = 0.25 + 0.0625 = 0.3125
             × T (for the one-period integral) ✓
```

Both methods give the same energy. ✓

### 7.1 Python Verification

```python
import numpy as np
import matplotlib.pyplot as plt

fs = 44100
duration = 1.0
t = np.linspace(0, duration, int(fs * duration), endpoint=False)

A1, A2, f1, f2 = 1.0, 0.5, 440, 880
x = A1 * np.sin(2 * np.pi * f1 * t) + A2 * np.sin(2 * np.pi * f2 * t)

# FFT
N = len(t)
X = np.fft.rfft(x) / N           # normalize by N
freqs = np.fft.rfftfreq(N, 1/fs)

# Plot magnitude spectrum
plt.figure(figsize=(10, 4))
plt.plot(freqs, 2 * np.abs(X))   # × 2 for one-sided convention
plt.xlim(0, 1200)
plt.xlabel("Frequency (Hz)")
plt.ylabel("|X(f)|")
plt.title("Magnitude Spectrum of 440 Hz + 880 Hz")
plt.axvline(440, color='green', linestyle='--', label='440 Hz (A₄)')
plt.axvline(880, color='orange', linestyle='--', label='880 Hz (A₅)')
plt.legend()
plt.tight_layout()
plt.show()

# Parseval check
energy_time = np.sum(x**2) / fs          # power estimate
energy_freq = np.sum(np.abs(X)**2) * 2   # × 2 for one-sided
print(f"Time energy: {energy_time:.4f}")
print(f"Freq energy: {energy_freq:.4f}")  # should match
```

Expected output: two sharp spikes at 440 Hz and 880 Hz with heights ≈ 0.5 and ≈ 0.25. Parseval values match (within floating-point error).

---

## 📚 8. The Continuous vs. Discrete Transform Family

```
Signal type          Transform           Frequency domain
─────────────────────────────────────────────────────────────
Continuous, periodic  → Fourier Series  → Discrete harmonics  {cₙ}
Continuous, aperiodic → Fourier Transform → Continuous F(f)
Discrete, periodic    → DFT             → Discrete spectrum   {X[k]}
Discrete, aperiodic   → DTFT            → Continuous 2π-periodic Θ(e^{jω})
```

The DFT (and its fast implementation, the FFT) is what runs on computers. It's covered in full depth in [04.3](04.3---Discrete-Fourier-Transform-&-FFT). The DTFT is the theoretical bridge between continuous-time and digital-domain analysis — it appears in Z-transform theory (filter design).

---

## 📚 9. Common Misconceptions

- **"The Fourier Transform only works for sine waves."** No — it works for *any* square-integrable function. Every waveform can be decomposed into sinusoids, regardless of shape.
- **"Negative frequencies are a mathematical fiction."** They are a natural consequence of using complex exponentials. For a real signal, they carry no additional information (conjugate symmetry), but they are essential in modulation, SSB radio, and analytic signal theory.
- **"Convolution is expensive."** In time domain, yes: O(N²). In the frequency domain, it's O(N log N) via FFT. Real-time audio effects engines all use FFT-based fast convolution (overlap-add).
- **"Phase doesn't matter — only magnitude matters."** For many perceptual applications, phase has limited audibility, but for **reconstruction** you need both. Stripping phase makes IFFT output incoherent noise. MFCCs deliberately discard phase (via DCT on log-power), which is fine for recognition but not synthesis.
- **"Parseval is just a math curiosity."** Parseval is the sanity check for every DSP system: feed in energy E, get out energy ≤ E. A filter that claims to preserve energy but output energy > input energy has a bug.

---

## 🔗 10. Cross-links & Further Reading

### Internal
- [04.1 - Signals, Systems & Sampling Theory](04.1---Signals,-Systems-&-Sampling-Theory) — the signal foundation this chapter analyses
- [04.3 - Discrete Fourier Transform & FFT](04.3---Discrete-Fourier-Transform-&-FFT) — computing the transform efficiently
- [04.4 - Digital Filters - FIR & IIR](04.4---Digital-Filters---FIR-&-IIR) — filter design in the frequency domain
- [04.5 - Audio Signal Processing & Psychoacoustics](04.5---Audio-Signal-Processing-&-Psychoacoustics) — mel spectrograms use log|FT|²
- [04.6 - Image Processing & 2D Transforms](04.6---Image-Processing-&-2D-Transforms) — 2D DFT for images
- [04.8 - Spectral Analysis & Applications in AI](04.8---Spectral-Analysis-&-Applications-in-AI) — spectral features for deep learning
- [Track 07](Subject_Plan) — complex analysis, Euler's formula, integration
- [Track 23](Subject_Plan) — wavefront propagation uses Fourier optics

### External
- [dspguide.com — Chapter 8–9: Fourier Transform](https://www.dspguide.com/ch8.htm) — the best intuitive introduction available free
- [Julius O. Smith III — Mathematics of the DFT (CCRMA)](https://ccrma.stanford.edu/~jos/mdft/) — rigorous treatment, free
- [MIT OCW 6.341 — Discrete-Time Signal Processing](https://ocw.mit.edu/courses/6-341-discrete-time-signal-processing-fall-2005/) — Oppenheim & Schafer lectures
- [3Blue1Brown — "But what is the Fourier Transform?" (YouTube)](https://www.youtube.com/watch?v=spUNpyF58BY) — best visual intuition on the internet
- [numpy.fft documentation](https://numpy.org/doc/stable/reference/routines.fft.html)

---

*Next: [04.3 - Discrete Fourier Transform & FFT](04.3---Discrete-Fourier-Transform-&-FFT) — The algorithm that makes frequency analysis fast enough to run in real-time.*
