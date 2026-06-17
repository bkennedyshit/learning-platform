---
title: "04.7 — Speech & Voice Processing (ASR/TTS Foundations)"
subject: "Signal Processing & DSP"
catalog: advanced
audience_tier: higher-education
chapter: "04.7"
type: chapter
objectives:
  - "Understand the concepts"
  - "Apply the theory"
open_source: true
---

*Back to [Subject_Plan](Subject_Plan) | Part of [00 - 09 - Learning Index](00---09---Learning-Index)*

# 04.7 — Speech & Voice Processing (ASR/TTS Foundations)

> *"Speech is the most information-dense signal the human auditory system processes. Milliseconds of acoustic information encode phonemes, prosody, speaker identity, emotion, and language simultaneously."*

This chapter is the direct connection between DSP mathematics and the voice AI stack Bill uses — Whisper, XTTS, Coqui TTS, and local speech models. It covers the source-filter model of speech production, pitch detection, formant analysis, and the full signal chain for both ASR (speech → text) and TTS (text → speech).

Prerequisite: [04.5](04.5---Audio-Signal-Processing-&-Psychoacoustics). Connect to: [Track 05](Subject_Plan) (AI experiments), [04.8](04.8---Spectral-Analysis-&-Applications-in-AI).

---

## 🎯 Learning Objectives

By the end of this chapter you will be able to:

1. Describe the **source-filter model** of speech production and explain voiced vs. unvoiced sounds.
2. Explain **pitch**, **fundamental frequency (f₀)**, **formants (F1, F2, F3)**, and their roles in vowel identity.
3. Implement **autocorrelation-based pitch detection (YIN algorithm)** and use `librosa.pyin`.
4. Trace the **Whisper ASR pipeline**: audio resampling → log-mel extraction → convolutional stem → Transformer encoder-decoder → text tokens.
5. Trace the **XTTS/VITS TTS pipeline**: text → phonemes → duration model → mel spectrogram → HiFi-GAN vocoder → waveform.
6. Describe the **STFT vocoder problem** and how neural vocoders (HiFi-GAN, WaveNet, EnCodec) solve it.
7. Set up a minimal Whisper inference pipeline in Python.

---

## 🖼️ Visual Anchor

![dsp__32.7-fig1](dsp__32.7-fig1.svg)

*Diagram: Top row — Whisper ASR pipeline (7 stages: audio → resample → log-mel → Conv → Transformer Enc → Transformer Dec → tokens). Second row — XTTS/VITS TTS pipeline (7 stages: text → G2P → duration → acoustic → mel → HiFi-GAN → waveform). Bottom-left — autocorrelation pitch detection with R[τ] plot. Bottom-right — STFT spectrogram simulation.*

---

## 📚 1. Speech Production — The Source-Filter Model

### 1.1 How Voice is Made

The human voice production system:

```
Lungs → Vocal Folds → Vocal Tract → Lips/Nose
(airflow)  (excitation)   (resonator)    (radiation)
```

**Voiced sounds** (vowels, nasals, voiced fricatives): the vocal folds **vibrate** periodically, creating a rich harmonic excitation at the **fundamental frequency f₀** (pitch). The period T₀ = 1/f₀.

**Unvoiced sounds** (fricatives: /s/, /f/, /sh/): vocal folds are open, air flows turbulently → **noise-like excitation** (broadband, no clear pitch).

**Plosives** (/p/, /t/, /k/): brief silence (closure) followed by an impulse burst (release).

### 1.2 The Source-Filter Model

The **source-filter model** (Fant, 1960) treats speech production as:

```
S(f) = E(f) · H(f) · R(f)
```

- **E(f)** — Excitation source: voiced (harmonic series, 1/f spectrum) or unvoiced (noise)
- **H(f)** — Vocal tract transfer function: resonances at **formant frequencies** F1, F2, F3, F4
- **R(f)** — Radiation characteristic: approximately +6 dB/octave (differentiator)

This model motivates **cepstral analysis**: in the log-spectrum domain, source and filter add (instead of multiply), making them separable by their different "quefrency" scales.

### 1.3 Fundamental Frequency (Pitch) and Harmonics

The voice spectrum of a voiced sound:

```
Harmonics at: f₀, 2f₀, 3f₀, 4f₀, …
```

- **Male voice f₀:** typically 85–180 Hz
- **Female voice f₀:** typically 165–255 Hz
- **Child voice f₀:** typically 250–400 Hz
- **Soprano singing:** up to 1 050 Hz (C6)

The **vocal tract resonances** shape the amplitude envelope of these harmonics. Peaks in the spectrum are called **formants** (F1, F2, F3, …).

### 1.4 Formants and Vowel Identity

| Vowel | F1 (Hz) | F2 (Hz) | Description |
|-------|---------|---------|-------------|
| /a/ (father) | 800 | 1200 | Low jaw, back tongue |
| /e/ (bed) | 600 | 2000 | Mid jaw, front tongue |
| /i/ (see) | 300 | 2800 | Closed jaw, front tongue |
| /o/ (go) | 500 | 900 | Rounded lips |
| /u/ (boot) | 300 | 900 | Rounded lips, back tongue |

The **F1-F2 vowel space** is the acoustic 2D plane that defines vowel identity — the foundation of vowel classification in ASR acoustic models.

---

## 📚 2. Pitch Detection

### 2.1 Autocorrelation Method

The most reliable classical pitch detector exploits the **periodicity** of voiced speech. The autocorrelation function:

```
R[τ] = Σ_n x[n] · x[n + τ]
```

For a periodic signal with period T₀, R[τ] has a peak at τ = T₀ (and multiples). The pitch is:

```
f₀ = fs / τ_peak
```

**YIN algorithm (de Cheveigné & Kawahara, 2002):** improves on autocorrelation by using the difference function:

```
d[τ] = Σ_n (x[n] − x[n+τ])²
     = R[0] + R[τ] − 2·R[τ]    (related to autocorrelation)
```

Normalised cumulative mean difference to reduce harmonic errors:
```
d'[τ] = 1                           if τ = 0
      = d[τ] / [(1/τ) Σ_{j=1}^{τ} d[j]]   otherwise
```

Find the first minimum of d'[τ] below a threshold (typically 0.1). YIN achieves ~state-of-art monophonic pitch accuracy with simple computation.

### 2.2 Python Implementation

```python
import librosa
import numpy as np

y, sr = librosa.load("speech.wav", sr=16000)

# PYIN: probabilistic YIN (most robust classical method)
f0, voiced_flag, voiced_probs = librosa.pyin(
    y,
    fmin=librosa.note_to_hz('C2'),   # 65.4 Hz
    fmax=librosa.note_to_hz('C7'),   # 2093 Hz
    sr=sr,
    frame_length=2048,
    hop_length=160
)

# f0: shape (T,) — NaN for unvoiced frames
# voiced_flag: boolean array
import matplotlib.pyplot as plt
times = librosa.times_like(f0, sr=sr, hop_length=160)
plt.figure(figsize=(12, 4))
plt.plot(times[voiced_flag], f0[voiced_flag], 'o', markersize=2, label='f₀')
plt.xlabel("Time (s)"); plt.ylabel("Hz")
plt.title("Pitch (f₀) Track — PYIN")
plt.ylim(50, 400); plt.legend()
plt.tight_layout(); plt.show()

# Simple autocorrelation (from scratch) for understanding:
def autocorrelation_pitch(frame, fs, f_min=80, f_max=400):
    """Return estimated f0 for a single frame using autocorrelation."""
    lag_min = int(fs / f_max)    # min period in samples
    lag_max = int(fs / f_min)    # max period in samples
    r = np.correlate(frame, frame, mode='full')
    r = r[len(frame)-1:]          # take non-negative lags
    # Find peak in valid lag range
    peak_lag = np.argmax(r[lag_min:lag_max]) + lag_min
    return fs / peak_lag
```

---

## 📚 3. Whisper ASR — Signal Chain

### 3.1 Architecture Overview

Whisper (OpenAI, 2022) is a Transformer-based multitask model trained on 680 000 hours of weakly-supervised web audio. Architecture:

```
Audio Input (30s) → Log-Mel (80 × 3000) → 2×Conv1D stem
                 → Transformer Encoder (positional encoding + multi-head self-attention)
                 → Transformer Decoder (cross-attention to encoder output)
                 → Text Tokens (vocabulary size ~51 865)
```

### 3.2 Pre-processing Pipeline (Python)

```python
import whisper
import numpy as np

# Load model (tiny/base/small/medium/large/large-v3)
model = whisper.load_model("base")

# Transcribe
result = model.transcribe("audio.wav", language="en")
print(result["text"])

# Manual pre-processing to inspect the features:
audio = whisper.load_audio("audio.wav")   # Loads and resamples to 16 kHz
audio = whisper.pad_or_trim(audio)         # Pads/trims to 30 s (480 000 samples)
mel = whisper.log_mel_spectrogram(audio)   # Shape: (80, 3000)
print(f"Mel spectrogram shape: {mel.shape}")  # (80, 3000)

# Detect language
_, probs = model.detect_language(mel)
print(f"Detected language: {max(probs, key=probs.get)}")

# Manual decode with options
options = whisper.DecodingOptions(language="en", without_timestamps=True)
result = whisper.decode(model, mel, options)
print(result.text)
```

### 3.3 Key Whisper Signal Processing Parameters

| Parameter | Value | Reasoning |
|-----------|-------|-----------|
| fs | 16 000 Hz | Sufficient for speech (f_max ≈ 7–8 kHz) |
| n_fft | 512 | 32 ms @ 16 kHz — fine enough for formant resolution |
| win_length | 400 | 25 ms window — standard speech frame |
| hop_length | 160 | 10 ms hop — standard for MFCC tradition |
| n_mels | 80 | 80 filterbank channels — enough for robust features |
| f_max | 8 000 Hz | Nyquist of 16 kHz recording |
| Chunk duration | 30 s | Fixed context window |
| Normalisation | log10 + clamp to [max-8, max] | Compresses dynamic range |

---

## 📚 4. TTS Synthesis — VITS/XTTS Signal Chain

### 4.1 Text-to-Speech Overview

Modern neural TTS systems (VITS, XTTS, StyleTTS2) operate end-to-end from text to waveform. The signal chain:

**Stage 1 — Grapheme-to-Phoneme (G2P):**
```
"hello" → [h ɛ l oʊ]    (IPA phonemes)
```
G2P uses pronunciation dictionaries (CMU DICT) or neural G2P models (e.g. `phonemizer`, `gruut`).

**Stage 2 — Duration Model:**
Predicts how many mel frames each phoneme occupies. Typically an MLP or Transformer trained on aligned text-audio pairs. Stochastic duration models (VITS) sample from a duration distribution for natural prosody variation.

**Stage 3 — Acoustic Model:**
Generates the mel spectrogram conditioned on phonemes and their durations. Options:
- **Transformer TTS / FastSpeech2:** non-autoregressive, fast
- **VITS:** variational auto-encoder + normalising flows → end-to-end mel + waveform in one pass
- **XTTS v2:** Transformer language model on audio codes + speaker conditioning

**Stage 4 — Vocoder:**
Converts mel spectrogram to waveform.

| Vocoder | Method | Quality | Speed |
|---------|--------|---------|-------|
| Griffin-Lim | Iterative phase estimation | Low | Fast |
| WaveNet | Autoregressive WaveNet | Very high | Slow |
| WaveRNN | Recurrent, smaller | High | Medium |
| **HiFi-GAN** | GAN on mel → waveform | High | Fast (real-time) |
| **BigVGAN** | GAN + periodic activation | Very high | Fast |
| **EnCodec** | Neural codec (RVQ tokens) | High | Fast |

### 4.2 HiFi-GAN Vocoder

**HiFi-GAN** (Kong et al., 2020) is the standard neural vocoder used in most modern TTS systems (FastSpeech2, XTTS). Architecture:

```
mel spectrogram (n_mels × T)
  → Generator (multi-receptive field fusion with residual dilated convolutions)
  → waveform (1 × T')

T' = T × hop_length
```

The generator is a fully convolutional network with **multi-receptive field fusion (MRF)** — parallel residual blocks with different dilation patterns capture spectral features at multiple time scales simultaneously.

**Training:** adversarial — a **multi-period discriminator** and **multi-scale discriminator** ensure the generated waveform has correct periodicity at multiple time scales (speech harmonics at different pitches).

### 4.3 XTTS v2 Quick Start

```python
# Using Coqui TTS (XTTS v2)
from TTS.api import TTS

# List available models
TTS.list_models()

# Load XTTS v2 (multilingual, voice cloning)
tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to("cuda")

# Synthesize with voice cloning from a reference clip
tts.tts_to_file(
    text="The Fourier Transform is the lens through which all of DSP is understood.",
    speaker_wav="reference_speaker.wav",   # 3–30 sec reference clip
    language="en",
    file_path="output.wav"
)
```

**Signal chain internal to XTTS v2:**
1. `text` → BPE tokenizer → token sequence
2. G2P (via IPA phonemes internal to the model)
3. GPT-like language model generates VQ audio tokens
4. XTTS decoder converts tokens → mel spectrogram
5. HiFi-GAN vocoder → waveform at 22 050 Hz or 24 000 Hz

---

## 📚 5. Voice Activity Detection (VAD)

Before sending audio to Whisper, it's efficient to detect and strip silence.

```python
# Using webrtcvad (lightweight VAD)
import webrtcvad
import wave

def is_speech(audio_bytes, sample_rate=16000, aggressiveness=2):
    """Returns True if this 10/20/30 ms frame contains speech."""
    vad = webrtcvad.Vad(aggressiveness)  # 0=least aggressive, 3=most
    return vad.is_speech(audio_bytes, sample_rate)

# Using Silero VAD (neural, more accurate)
import torch
model, utils = torch.hub.load(repo_or_dir='snakers4/silero-vad',
                               model='silero_vad')
(get_speech_ts, save_audio, read_audio,
 VADIterator, collect_chunks) = utils

wav = read_audio("audio.wav", sampling_rate=16000)
speech_timestamps = get_speech_ts(wav, model)
# Returns list of {start, end} in samples for each speech segment
```

---

## 📚 6. Common Misconceptions

- **"Whisper works best at 44.1 kHz."** No — Whisper resamples all input to 16 kHz internally. Passing 44.1 kHz audio just adds unnecessary resampling work. Pass 16 kHz directly.
- **"TTS is just recording and stitching."** Modern neural TTS synthesises novel mel spectrograms from the acoustic model; it does not concatenate recordings. Concatenative TTS (unit selection) was common until ~2017.
- **"Voiced = loud, unvoiced = quiet."** Voicing refers to vocal fold vibration, not loudness. A whispered /a/ is voiced (folds vibrate) even at low amplitude. A loud /s/ is unvoiced (air turbulence, no fold vibration).
- **"The fundamental frequency is the loudest harmonic."** For many vowels, the second harmonic (2f₀) or third (3f₀) can be louder than f₀, especially when a formant overlaps. Pitch trackers look for periodicity, not the loudest spectral peak.
- **"f₀ = 440 Hz means the fundamental is always at 440 Hz."** Yes — but overtones at 880, 1320, 1760 Hz etc. carry most of the perceived timbre. Remove the fundamental and most listeners still correctly identify the pitch (the "missing fundamental" effect).

---

## 🔗 7. Cross-links & Further Reading

### Internal
- [04.5 - Audio Signal Processing & Psychoacoustics](04.5---Audio-Signal-Processing-&-Psychoacoustics) — mel features this chapter consumes
- [04.3 - Discrete Fourier Transform & FFT](04.3---Discrete-Fourier-Transform-&-FFT) — STFT foundation
- [04.8 - Spectral Analysis & Applications in AI](04.8---Spectral-Analysis-&-Applications-in-AI) — spectral features for AI
- [Track 05](Subject_Plan) — Whisper & XTTS experiments
- [Track 10](Subject_Plan) — Transformer architecture
- [Subject_Plan](Subject_Plan) — resource catalog

### External
- [OpenAI Whisper paper (arXiv 2212.04356)](https://arxiv.org/abs/2212.04356) — Radford et al. 2022
- [OpenAI Whisper GitHub](https://github.com/openai/whisper)
- [Coqui TTS / XTTS documentation](https://docs.coqui.ai/)
- [HiFi-GAN paper (arXiv 2010.05646)](https://arxiv.org/abs/2010.05646) — Kong et al. 2020
- [VITS paper (arXiv 2106.06103)](https://arxiv.org/abs/2106.06103) — Kim et al. 2021
- [Librosa — yin / pyin](https://librosa.org/doc/latest/generated/librosa.pyin.html)
- [Julius O. Smith III — Spectral Audio Signal Processing (CCRMA)](https://ccrma.stanford.edu/~jos/sasp/)
- [dspguide.com — Chapter 22: Speech Synthesis and Recognition](https://www.dspguide.com/ch22.htm)

---

*Next: [04.8 - Spectral Analysis & Applications in AI](04.8---Spectral-Analysis-&-Applications-in-AI) — How spectral DSP connects to deep learning: wav2vec2, AudioLM, EnCodec, and real-time AI audio.*
