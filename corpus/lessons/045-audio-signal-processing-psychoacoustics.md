---
title: "04.5 — Audio Signal Processing & Psychoacoustics"
subject: "Signal Processing & DSP"
catalog: advanced
audience_tier: higher-education
chapter: "04.5"
type: chapter
objectives:
  - "Understand the concepts"
  - "Apply the theory"
open_source: true
---

*Back to [Subject_Plan](Subject_Plan) | Part of [00 - 09 - Learning Index](00---09---Learning-Index)*

# 04.5 — Audio Signal Processing & Psychoacoustics

> *"The ear is not a spectrum analyser. It is a time-frequency, loudness-normalising, pattern-recognising machine shaped by evolution. DSP for audio has to meet the ear where it is."*

This chapter is the bridge between DSP mathematics and AI audio systems. We cover how the human auditory system works (psychoacoustics), how this motivates the mel scale and MFCCs, and how modern AI models like Whisper and XTTS consume audio features. It is the most directly applicable chapter for the voice/audio experiments in [Track 05](Subject_Plan).

Prerequisite: [04.3](04.3---Discrete-Fourier-Transform-&-FFT) and [04.4](04.4---Digital-Filters---FIR-&-IIR). Related: [04.7](04.7---Speech-&-Voice-Processing-(ASR-TTS-Foundations)), [04.8](04.8---Spectral-Analysis-&-Applications-in-AI).

---

## 🎯 Learning Objectives

By the end of this chapter you will be able to:

1. Describe the **human hearing system** (outer ear → basilar membrane → auditory nerve) and explain why it motivates log-frequency and log-amplitude analysis.
2. Convert between **linear frequency (Hz)**, **Mel scale**, **Bark scale**, and **ERB scale**.
3. Compute the **mel filterbank** from scratch and explain why bins are dense at low frequencies.
4. Extract **MFCCs** step-by-step: pre-emphasis → framing → windowing → FFT → mel filterbank → log → DCT.
5. Generate a **log-mel spectrogram** using Librosa and understand its dimensions.
6. Explain **simultaneous and temporal masking** and how audio codecs exploit them.
7. Choose the correct **feature type** for a given audio AI task.

---

## 🖼️ Visual Anchor

![dsp__32.5-fig1](dsp__32.5-fig1.svg)

*Diagram: MFCC pipeline (7-step chain from audio to coefficients). Bottom-left: Mel vs. linear frequency scale comparison with overlapping triangular filters. Bottom-right: Psychoacoustic principles table — hearing range, critical bands, masking, log-mel spec parameters for Whisper.*

---

## 📚 1. Human Auditory System — Why DSP Must Match the Ear

### 1.1 Anatomy of Hearing (Brief)

The auditory pathway: **pinna (outer ear)** → ear canal resonance → **eardrum** → **ossicles** (hammer/anvil/stirrup amplification, ~30 dB) → **oval window** → **cochlea** (fluid-filled spiral) → **basilar membrane** → **hair cells** → **auditory nerve** → auditory cortex.

The **basilar membrane** performs mechanical frequency analysis: high frequencies maximally deflect near the base (stapes end), low frequencies near the apex. This is a biological analog of the Fourier Transform — but with **logarithmic frequency spacing**.

### 1.2 Hearing Range

| Parameter | Value |
|-----------|-------|
| Frequency range | 20 Hz – 20 000 Hz (20 kHz) |
| Dynamic range | ~120 dB (threshold of pain - threshold of hearing) |
| Best sensitivity | 2 000 – 5 000 Hz (speech intelligibility range) |
| Frequency resolution | ~1/30 octave at middle frequencies (≈ 3% relative) |

### 1.3 Loudness is Logarithmic

The **decibel (dB SPL)** scale reflects the logarithmic perception of loudness (Weber-Fechner law):

```
L_dB = 20 · log₁₀(p / p_ref)     p_ref = 20 μPa (threshold of hearing at 1 kHz)
```

A 10 dB increase corresponds approximately to a doubling of perceived loudness (Stevens's power law).

Equal loudness contours (Fletcher-Munson curves) show that the ear is most sensitive between 2–5 kHz — you need more SPL at 100 Hz or 10 kHz to perceive the same loudness as 1 kHz. This motivates **A-weighting** in acoustic measurements.

---

## 📚 2. Frequency Scales for Audio

### 2.1 Mel Scale

The **mel scale** approximates how the ear perceives pitch differences. Named after the unit "mel" (from "melody"), it was empirically derived by asking listeners to judge equal pitch intervals:

```
m = 2595 · log₁₀(1 + f/700)       (mel to frequency: f = 700 · (10^(m/2595) − 1))
```

The mel scale is approximately **linear below 1 kHz** and **logarithmic above 1 kHz**. At 1 kHz, 1 mel ≈ 1 Hz; at 10 kHz, 100 Hz difference ≈ ~100 mels (compressed).

### 2.2 Bark Scale (Critical Bands)

The **Bark scale** divides the auditory frequency range into ~24 **critical bands**, each roughly one "auditory filter" wide:

```
B = 13 · arctan(0.76f/1000) + 3.5 · arctan(f/7500)²
```

Critical bands are approximately 100 Hz wide below 500 Hz and 20% of frequency width above 500 Hz. They define the limits of **simultaneous masking** — a loud tone masks quieter tones within the same critical band.

### 2.3 ERB Scale (Equivalent Rectangular Bandwidth)

The **ERB** (Equivalent Rectangular Bandwidth) models the auditory filter more accurately than the Bark scale:

```
ERB(f) = 24.7 · (4.37f/1000 + 1)    Hz
```

Used in the **gammatone filterbank**, which is the most physiologically accurate auditory model.

### 2.4 Conversion Table

| Frequency (Hz) | Mel | Bark | Description |
|---------------|-----|------|-------------|
| 100 | 150 | 1 | Below speech fundamental |
| 300 | 401 | 3 | Male voice f₀ range |
| 500 | 607 | 5 | Vowel formant F1 |
| 1 000 | 1000 | 8.5 | Reference point |
| 2 000 | 1474 | 13 | F2 formant, speech clarity |
| 4 000 | 1978 | 17 | Best hearing sensitivity |
| 8 000 | 2534 | 21 | Consonant sibilants |
| 16 000 | 3177 | 24 | Upper hearing limit |

---

## 📚 3. Mel Filterbank

### 3.1 Definition

A **mel filterbank** is a bank of M overlapping triangular bandpass filters, **equally spaced in mel frequency**. Applied to the power spectrum of an STFT frame, it compresses the frequency axis to match auditory perception.

**Construction algorithm:**
1. Define mel-spaced filter centers: m₁, m₂, …, m_M in mel, from f_low to f_high.
2. Convert centers back to linear Hz: fₖ = 700 · (10^(mₖ/2595) − 1).
3. Find the nearest FFT bin for each center.
4. Each filter is a triangle: ramps up from previous center to current center, then down to next center.

### 3.2 Python Implementation from Scratch

```python
import numpy as np

def mel_filterbank(fs, n_fft, n_mels=80, f_min=0.0, f_max=None):
    """Mel filterbank matrix: shape (n_mels, n_fft//2 + 1)."""
    if f_max is None:
        f_max = fs / 2.0
    
    # Convert f_min, f_max to mel
    m_min = 2595 * np.log10(1 + f_min / 700)
    m_max = 2595 * np.log10(1 + f_max / 700)
    
    # n_mels+2 equally spaced mel points (includes two boundary points)
    mel_points = np.linspace(m_min, m_max, n_mels + 2)
    
    # Convert back to Hz
    hz_points = 700 * (10**(mel_points / 2595) - 1)
    
    # Convert to nearest FFT bin
    n_bins = n_fft // 2 + 1
    bin_points = np.floor((n_fft + 1) * hz_points / fs).astype(int)
    
    # Create filterbank matrix
    fb = np.zeros((n_mels, n_bins))
    for m in range(1, n_mels + 1):
        f_m_minus = bin_points[m - 1]   # left boundary
        f_m       = bin_points[m]        # center
        f_m_plus  = bin_points[m + 1]   # right boundary
        
        for k in range(f_m_minus, f_m):
            fb[m-1, k] = (k - f_m_minus) / (f_m - f_m_minus)
        for k in range(f_m, f_m_plus):
            fb[m-1, k] = (f_m_plus - k) / (f_m_plus - f_m)
    
    return fb

# Test
fb = mel_filterbank(16000, 512, n_mels=80)
print(f"Filterbank shape: {fb.shape}")   # (80, 257)
print(f"Total filters: {fb.shape[0]}")   # 80
```

### 3.3 Using Librosa

```python
import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np

# Load audio
y, sr = librosa.load("speech.wav", sr=16000)

# Log-mel spectrogram (Whisper-style)
n_fft = 400         # 25 ms at 16 kHz
hop_length = 160    # 10 ms hop
n_mels = 80

mel_spec = librosa.feature.melspectrogram(
    y=y, sr=sr, n_fft=n_fft, hop_length=hop_length,
    n_mels=n_mels, fmin=0.0, fmax=sr//2
)
log_mel = librosa.power_to_db(mel_spec, ref=np.max)

plt.figure(figsize=(12, 4))
librosa.display.specshow(log_mel, sr=sr, hop_length=hop_length,
                          x_axis='time', y_axis='mel')
plt.colorbar(format='%+2.0f dB')
plt.title(f'Log-Mel Spectrogram ({n_mels} bins, {n_fft}-point FFT)')
plt.tight_layout(); plt.show()

print(f"Shape: {log_mel.shape}")  # (80, T) where T = n_samples/hop_length
```

---

## 📚 4. MFCC — Mel-Frequency Cepstral Coefficients

### 4.1 Motivation

The mel spectrogram still contains correlated features (adjacent mel bins overlap significantly). The **Discrete Cosine Transform (DCT)** step decorrelates them and compresses to a small set of coefficients — the MFCCs.

MFCCs model the **vocal tract shape** (spectral envelope) separately from the **pitch** (excitation). For speech recognition, vocal tract shape is the linguistically relevant part.

### 4.2 The 7-Step MFCC Pipeline

**Step 1 — Pre-emphasis filter:**
```
y[n] = x[n] − α · x[n−1]     α ≈ 0.97
```
Boosts high frequencies (compensates for the −6 dB/octave rolloff of the human voice).

**Step 2 — Frame signal into overlapping blocks:**
```
Frame length: 25 ms (400 samples at 16 kHz)
Frame shift:  10 ms (160 samples)  ← hop
```
Typical speech signals have ~10–30 ms stationarity (vowel formants, consonants change slowly).

**Step 3 — Apply window function (Hann):**
```
frame[n] = frame[n] · w_Hann[n]
```

**Step 4 — FFT:**
```
FRAME_FFT = |FFT(windowed_frame)|²    (power spectrum, one-sided)
```

**Step 5 — Apply mel filterbank:**
```
mel_energies[m] = Σ_k H_m[k] · FRAME_FFT[k]    m = 0…M−1
```

**Step 6 — Log compression:**
```
log_mel[m] = log(mel_energies[m] + ε)    ε = small constant to avoid log(0)
```

**Step 7 — DCT:**
```
MFCC[n] = Σ_{m=0}^{M−1}  log_mel[m] · cos(π·n·(m+0.5)/M)    n = 0…C−1
```
Typically C = 13 coefficients are kept. MFCC[0] is related to energy (often replaced by log-energy); MFCC[1]–[12] encode spectral shape.

**Delta and delta-delta features:** Compute first and second temporal derivatives of MFCCs:
```
Δ[n, t] ≈ MFCC[n, t+1] − MFCC[n, t−1]    (first difference)
ΔΔ[n, t] ≈ Δ[n, t+1] − Δ[n, t−1]          (second difference)
```
Concatenating MFCC (13) + Δ (13) + ΔΔ (13) = **39-dimensional feature vector** per frame — the traditional GMM-HMM speech recognition input.

```python
import librosa
mfccs = librosa.feature.mfcc(y=y, sr=16000, n_mfcc=13, n_mels=40)
print(mfccs.shape)   # (13, T)

# With delta features
delta = librosa.feature.delta(mfccs, order=1)
delta2 = librosa.feature.delta(mfccs, order=2)
features = np.vstack([mfccs, delta, delta2])
print(features.shape)  # (39, T)
```

---

## 📚 5. Psychoacoustic Masking

### 5.1 Simultaneous Masking

A **loud sound masks quieter sounds** at nearby frequencies within the same critical band. The amount of masking depends on:
- **Frequency separation:** masking decreases rapidly with distance from the masker frequency.
- **Masker level:** louder maskers spread masking further.
- **Direction (upward/downward):** masking spreads further upward in frequency than downward.

**MP3/AAC exploit simultaneous masking:** if a frequency component's energy is below the masking threshold, it is **removed or heavily quantised** — the listener cannot hear the difference.

### 5.2 Temporal Masking

- **Forward masking (post-masking):** a loud sound suppresses detection of a quieter sound up to ~200 ms *after* the loud sound ends.
- **Backward masking (pre-masking):** up to ~20 ms *before* the loud sound starts (this is possible because codecs have lookahead).

### 5.3 The Masking Threshold

The **perceptual masking threshold** is computed for each audio frame in codecs:
1. Compute power spectrum.
2. Identify **tonal components** (narrow peaks) and **noise-like components** (broad regions).
3. Spread masking contributions from each component using spreading functions.
4. Sum to get the total masking threshold as a function of frequency.
5. The **signal-to-mask ratio (SMR)** = signal power / masking threshold.

Bits are allocated to frequency bands proportionally to SMR — bands with high SMR get more bits (audible), bands with low SMR get fewer (masked).

---

## 📚 6. Log-Mel Spectrogram for Whisper

**Whisper (OpenAI, 2022) input specification:**

| Parameter | Value | Notes |
|-----------|-------|-------|
| Sample rate | 16 000 Hz | Resample all input to this |
| Window size | 400 samples | 25 ms Hann window |
| Hop size | 160 samples | 10 ms hop |
| FFT size | 512 | Zero-padded from 400-sample window |
| Mel bins | 80 | f_min=0, f_max=8000 Hz |
| Chunk length | 30 s = 480 000 samples | Padded/truncated to this |
| Output shape | (80, 3000) | 80 mel × 3000 frames |
| Normalisation | log(max(mel, 1e-10)) → clamp to [−8, max] | See whisper/audio.py |

```python
# Whisper-style log-mel extraction (simplified)
import numpy as np
import librosa

def whisper_log_mel(audio, sr=16000):
    """Compute Whisper's log-mel spectrogram."""
    # Resample if needed
    if sr != 16000:
        audio = librosa.resample(audio, orig_sr=sr, target_sr=16000)
    
    # Pad or trim to 30 seconds
    n_samples = 16000 * 30
    if len(audio) > n_samples:
        audio = audio[:n_samples]
    else:
        audio = np.pad(audio, (0, n_samples - len(audio)))
    
    # STFT with Hann window
    D = np.abs(librosa.stft(audio, n_fft=512, hop_length=160,
                             win_length=400, window='hann'))
    
    # Mel filterbank
    mel_fb = librosa.filters.mel(sr=16000, n_fft=512, n_mels=80,
                                  fmin=0, fmax=8000)
    mel_spec = mel_fb @ (D ** 2)      # filterbank · power spectrum
    
    # Log compression (Whisper convention)
    log_mel = np.log10(np.maximum(mel_spec, 1e-10))
    log_mel = np.maximum(log_mel, log_mel.max() - 8.0)
    log_mel = (log_mel + 4.0) / 4.0   # normalise to ~[-1, 1]
    
    return log_mel.astype(np.float32)  # shape: (80, 3000)
```

---

## 📚 7. Common Misconceptions

- **"MFCCs are what neural networks use for audio."** MFCCs dominated until ~2018. Modern models (wav2vec2, HuBERT, Whisper, XTTS) use raw waveforms or log-mel spectrograms. MFCCs are still used in lightweight models and on-device inference.
- **"More mel bins = better accuracy."** Not necessarily. Whisper uses 80 bins; many speech models use 40 or even 20. The diminishing returns above 40 bins are well-documented for most tasks.
- **"MP3 destroys audio quality."** Modern MP3 at 320 kbps is perceptually transparent for most listeners on most content. The masking model is remarkably effective. For music production masters, use lossless (FLAC/WAV).
- **"Pre-emphasis is always necessary."** Pre-emphasis was originally designed for old telephone channels with high-frequency rolloff. For modern microphones with flat response, it is optional — but it can help by boosting weak high-frequency fricatives.
- **"MFCC[0] is the pitch."** MFCC[0] approximates log-energy (related to loudness), not pitch. Pitch is encoded in the cepstrum at a different quefrency — see [04.8](04.8---Spectral-Analysis-&-Applications-in-AI).

---

## 🔗 8. Cross-links & Further Reading

### Internal
- [04.3 - Discrete Fourier Transform & FFT](04.3---Discrete-Fourier-Transform-&-FFT) — FFT behind every mel frame
- [04.4 - Digital Filters - FIR & IIR](04.4---Digital-Filters---FIR-&-IIR) — mel filterbank = bank of bandpass filters
- [04.7 - Speech & Voice Processing (ASR-TTS Foundations)](04.7---Speech-&-Voice-Processing-(ASR-TTS-Foundations)) — Whisper & XTTS consume these features
- [04.8 - Spectral Analysis & Applications in AI](04.8---Spectral-Analysis-&-Applications-in-AI) — broader spectral features for AI
- [Track 05](Subject_Plan) — TTS/ASR experiments using these features
- [Subject_Plan](Subject_Plan) — resource catalog including Librosa docs

### External
- [Librosa documentation](https://librosa.org/doc/latest/) — the canonical Python audio analysis library
- [dspguide.com — Chapter 22: Audio Processing](https://www.dspguide.com/ch22.htm) — free
- [Haytham Fayek — Practical Cryptography — MFCCs](https://haythamfayek.com/2016/04/21/speech-processing-for-machine-learning.html) — excellent free tutorial
- [OpenAI Whisper paper (arXiv 2022)](https://arxiv.org/abs/2212.04356) — the source for Whisper's feature spec
- [OpenAI Whisper audio.py (GitHub)](https://github.com/openai/whisper/blob/main/whisper/audio.py) — reference implementation
- [Julius O. Smith III — Spectral Audio Signal Processing (CCRMA)](https://ccrma.stanford.edu/~jos/sasp/) — free online textbook

---

*Next: [04.6 - Image Processing & 2D Transforms](04.6---Image-Processing-&-2D-Transforms) — The same Fourier tools applied to images: 2D DFT, convolution, edge detection.*
