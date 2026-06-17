---
date: 2026-05-31
type: subject-readme
tags: [dsp, signal-processing, practice, refresher, drills, source-materials, study-aids, fourier, filters, mel, mfcc, spectrogram, whisper, xtts, audio-ai]
title: "README — 04 - Signal Processing & DSP"
---

# 📡 04 - Signal Processing & DSP — Subject Hub

> One-page subject hub. Lists chapters, source materials, **video / picture references stored outside the vault (linked by URL)**, and placeholders for generated study aids.
> Master practice guide: [[../HOW_TO_USE_PRACTICE|HOW_TO_USE_PRACTICE]].

> **Asset storage convention:**
> - **SVG diagrams** (small, theme-responsive, in-vault) → `../_svgs/dsp__32.x-fig1.svg` and embedded inline via `![[dsp__32.x-fig1.svg]]`.
> - **Audio files, spectrograms, course recordings, pictures** are NOT committed to this repo. They live on YouTube, official docs, GitHub, or in your local `_assets/` sidecar (gitignored). Reference them by **URL** in this README and chapter notes.

---

## 🚀 Quick Start

```bash
# Install the DSP Python stack
pip install numpy scipy librosa matplotlib soundfile pyaudio torchaudio torch

# Install ASR/TTS tools
pip install openai-whisper
pip install TTS          # Coqui TTS (XTTS v2)
pip install transformers  # HuggingFace (wav2vec2, HuBERT)

# Verify NumPy FFT works
python -c "import numpy as np; print(np.fft.fft([1,2,3,4]))"

# Quick Whisper transcription test
whisper audio.wav --model base --language en
```

---

## 📜 Chapter Index

- [[04.1 - Signals, Systems & Sampling Theory]]
- [[04.2 - Fourier Series & Fourier Transform]]
- [[04.3 - Discrete Fourier Transform & FFT]]
- [[04.4 - Digital Filters - FIR & IIR]]
- [[04.5 - Audio Signal Processing & Psychoacoustics]]
- [[04.6 - Image Processing & 2D Transforms]]
- [[04.7 - Speech & Voice Processing (ASR-TTS Foundations)]]
- [[04.8 - Spectral Analysis & Applications in AI]]

---

## 🎬 Video & Picture References (External — Open in Browser)

> These supplement the chapter notes. Files are **not** stored in the vault.

### 📺 Video Channels & Playlists

| Channel / Course | Track Use | Link |
|---|---|---|
| **3Blue1Brown — "But what is the Fourier Transform?"** | Visual FT intuition — **the best starting point** | [youtube.com/watch?v=spUNpyF58BY](https://www.youtube.com/watch?v=spUNpyF58BY) |
| **3Blue1Brown — Fourier Series visual** | Fourier Series animation | [youtube.com/watch?v=r6sGWTCMz2k](https://www.youtube.com/watch?v=r6sGWTCMz2k) |
| **MIT OCW 6.341 Lecture Videos** | Full graduate DSP — Oppenheim & Schafer | [ocw.mit.edu/6.341](https://ocw.mit.edu/courses/6-341-discrete-time-signal-processing-fall-2005/) |
| **MIT OCW 6.003 Signals & Systems** | Continuous + discrete systems | [ocw.mit.edu/6.003](https://ocw.mit.edu/courses/6-003-signals-and-systems-fall-2011/) |
| **Julius O. Smith III lectures (CCRMA)** | DSP for music + audio, filter theory | [ccrma.stanford.edu/~jos](https://ccrma.stanford.edu/~jos/) |
| **Haytham Fayek — Speech Processing blog** | MFCC tutorial with plots | [haythamfayek.com](https://haythamfayek.com/2016/04/21/speech-processing-for-machine-learning.html) |
| **Librosa tutorial notebooks** | Audio analysis in Python | [librosa.org/doc/latest](https://librosa.org/doc/latest/) |
| **Whisper demo / GitHub** | ASR pipeline code + paper | [github.com/openai/whisper](https://github.com/openai/whisper) |
| **Coqui TTS / XTTS v2 docs** | TTS synthesis + voice cloning | [docs.coqui.ai](https://docs.coqui.ai/) |
| **HuggingFace Audio Course** | End-to-end audio + transformers | [huggingface.co/learn/audio-course](https://huggingface.co/learn/audio-course/) |

### 🖼️ Diagram & Reference Sources

| Source | What it gives you | Link |
|---|---|---|
| **dspguide.com** | Complete free DSP textbook — all chapters | [dspguide.com](https://www.dspguide.com/) |
| **Julius Smith — MathDFT** | DFT matrix, twiddle factors, proofs | [ccrma.stanford.edu/~jos/mdft](https://ccrma.stanford.edu/~jos/mdft/) |
| **NumPy FFT docs** | rfft, rfftfreq, fftshift | [numpy.org/doc/stable/reference/routines.fft](https://numpy.org/doc/stable/reference/routines.fft.html) |
| **SciPy Signal docs** | butter, sosfilt, firwin, remez, stft, spectrogram | [docs.scipy.org/doc/scipy/reference/signal](https://docs.scipy.org/doc/scipy/reference/signal.html) |
| **Audio EQ Cookbook** | Biquad EQ formulas (peaking, shelving, allpass) | [webaudio.github.io/Audio-EQ-Cookbook](https://webaudio.github.io/Audio-EQ-Cookbook/audio-eq-cookbook.html) |
| **Fletcher-Munson equal-loudness curves** | Why we need A-weighting | [en.wikipedia.org/wiki/Equal-loudness_contour](https://en.wikipedia.org/wiki/Equal-loudness_contour) |
| **Whisper audio.py (source)** | Exact log-mel preprocessing code | [github.com/openai/whisper/blob/main/whisper/audio.py](https://github.com/openai/whisper/blob/main/whisper/audio.py) |

### 📚 Open-Source / Free Books

| Title | Author | Link |
|---|---|---|
| The Scientist & Engineer's Guide to DSP | Steven W. Smith | [dspguide.com](https://www.dspguide.com/) |
| Mathematics of the DFT | Julius O. Smith III | [ccrma.stanford.edu/~jos/mdft](https://ccrma.stanford.edu/~jos/mdft/) |
| Introduction to Digital Filters | Julius O. Smith III | [ccrma.stanford.edu/~jos/filters](https://ccrma.stanford.edu/~jos/filters/) |
| Spectral Audio Signal Processing | Julius O. Smith III | [ccrma.stanford.edu/~jos/sasp](https://ccrma.stanford.edu/~jos/sasp/) |
| Think DSP (Python-focused) | Allen Downey | [greenteapress.com/wp/think-dsp](https://greenteapress.com/wp/think-dsp/) |

---

## 🔭 2026 Industry Snapshot

| Area | 2026 Reality | Primary sources |
|---|---|---|
| ASR | Whisper large-v3-turbo runs faster than real-time on modern GPU; tiny/base on CPU. OpenAI Canary architecture adds learnable filterbanks. | [github.com/openai/whisper](https://github.com/openai/whisper) |
| TTS | XTTS v2 + Kokoro (82M params open-source) deliver near-commercial quality. Full-duplex voice AI (Moshi) now practical in real-time. | [docs.coqui.ai](https://docs.coqui.ai/), [kyutai.org/moshi](https://kyutai.org/moshi) |
| Audio codecs | EnCodec and DAC enable language-model-style audio generation (AudioLM, VALL-E, MusicGen). Codec tokens are the new "audio word embeddings." | [arXiv 2210.13438](https://arxiv.org/abs/2210.13438) |
| Music AI | MusicGen v2 / Stable Audio 2.0 generate 5-minute 44.1 kHz stereo from text + melody conditioning. | [stability.ai](https://stability.ai/news/stable-audio-2-0) |
| Browser DSP | WebAssembly SIMD enables real-time FFT and Whisper-tiny in browser (no GPU). | [web.dev/articles/webassembly-simd](https://web.dev/articles/webassembly-simd) |

---

## 🧰 Generated Study Aids

### 🎙️ Audio Overviews (NotebookLM)
- [ ] TODO: Paste the NotebookLM "Audio Overview" link for Track 04

### 🧠 Mind Maps
- [ ] TODO: NotebookLM mind-map URL — DSP concept hierarchy

### ❓ Quizzes
- [ ] TODO: NotebookLM quiz — Nyquist, Fourier pairs, filter comparison, mel conversion
- [ ] TODO: Flashcard deck: all transform pairs, SQNR formula, window sidelobe values

### 📊 Reports & Summaries
- [ ] TODO: NotebookLM "Briefing Doc" — Track 04 summary
- [ ] TODO: Comparison table: FIR vs IIR (printable)
- [ ] TODO: Comparison table: audio feature → use case → librosa function (printable)

### 🃏 Flash Cards
- [ ] TODO: Anki deck — Nyquist theorem, sampling equations, mel formula, MFCC steps, FFT complexity
- [ ] TODO: Transform pairs deck: rect↔sinc, δ(t)↔1, Gaussian↔Gaussian, e^jωt↔δ(ω-ω0)

### 🎬 Video Overviews
- [ ] TODO: Personal Loom walkthrough — "Whisper mel spectrogram dissected"
- [ ] TODO: Screen recording — real-time FFT of voice with Python/PyAudio

### 📋 Data Tables
- [ ] TODO: Sample rate comparison table (printable: 8kHz → 192kHz, use cases, Nyquist)
- [ ] TODO: Window function comparison (printable: sidelobe levels, transition widths)
- [ ] TODO: Audio AI model reference card (printable: Whisper, XTTS, wav2vec2, HuBERT, EnCodec parameters)

---

## 🔗 Cross-links

- Syllabus & curriculum mindmap: [[Bill's Vault/05-Knowledge_Foundation/09 - Learning/04 - Signal Processing & DSP/Subject_Plan]]
- Visual roadmap: [[Bill's Vault/05-Knowledge_Foundation/09 - Learning/04 - Signal Processing & DSP/LEARNING_PATH]]
- Track 07 — Math & Physics (complex analysis prerequisite): [[../07 - Math and Physics/Subject_Plan]]
- Track 21 — Electronics (ADC/DAC hardware): [[../30 - Electronics/Subject_Plan]]
- Track 23 — Holographics (Fourier optics, angular spectrum): [[../31 - Holographics/Subject_Plan]]
- Track 05 — AI Experiments (Whisper, XTTS applications): [[../24 - AI Experiments/Subject_Plan]]
- Track 10 — AI & ML Systems (foundation model architecture): [[../23 - AI & Machine Learning Systems/Subject_Plan]]
- Track 09 — VR & 3D (spatial audio, HRTF): [[../28 - VR & 3D Engineering/Subject_Plan]]
- Track 22 — Robotics (sensor signal processing): [[../32 - Robotics/Subject_Plan]]
- Master learning index: [[00 - 09 - Learning Index]]
- Master practice guide: [[../HOW_TO_USE_PRACTICE]]
- Scaling north star: [[../BUILDING_AT_SCALE]]
