---
title: "34.4 — Autonomic Nervous System Telemetry: HRV"
subject: "Biomechanics & HCI"
catalog: advanced
audience_tier: higher-education
chapter: "34.4"
type: chapter-note
objectives:
  - "Understand the concepts"
  - "Apply the theory"
open_source: true
---

*Back to [Subject_Plan](Subject_Plan) | Part of [34 - Biomechanics & HCI](34---Biomechanics-&-HCI)*

# 34.4 — Autonomic Nervous System Telemetry: HRV

> *"The autonomic nervous system is organized hierarchically, with the ventral vagal complex providing the most evolved and nuanced regulation of social engagement and physiological state."* — Stephen Porges, *The Polyvagal Theory*, 2011

Heart Rate Variability (HRV) is the beat-to-beat variation in R-R intervals — the time between successive heartbeats. Far from being noise, this variability is a direct readout of autonomic nervous system (ANS) balance. For an athlete with a 33 BPM resting heart rate, HRV analysis reveals the extraordinary parasympathetic dominance (dorsal vagal tone) that produces such profound bradycardia.

---

## 🎯 Learning Objectives

1. Define **R-R intervals** and understand their physiological origin.
2. Compute **time-domain HRV metrics**: RMSSD, SDNN, pNN50, mean RR.
3. Compute **frequency-domain HRV metrics**: VLF, LF, HF power, LF/HF ratio.
4. Understand the **Polyvagal Theory** hierarchy (Porges) and its relevance to athletic performance.
5. Distinguish **Athlete's Heart bradycardia** from pathological bradycardia using HRV.
6. Apply **spectral analysis** (FFT, Welch's method) to R-R interval time series.
7. Implement a complete HRV analysis pipeline in Python.

---

## 🖼️ Visual Anchor — HRV Time Series & Frequency Spectrum

![track-13__13.4-fig1](track-13__13.4-fig1.svg)

---

## 📚 1. Definitions

### Definition 34.4.1 — R-R Interval

The **R-R interval** (also NN interval for "normal-to-normal") is the time in milliseconds between consecutive R-peaks in the ECG:

$$
RR_i = t_{R,i+1} - t_{R,i}
$$

For 33 BPM: mean $RR = 60000/33 = 1818$ ms.

### Definition 34.4.2 — SDNN (Standard Deviation of NN Intervals)

$$
SDNN = \sqrt{\frac{1}{N-1}\sum_{i=1}^{N}(RR_i - \overline{RR})^2}
$$

Reflects **total variability** (both sympathetic and parasympathetic). Normal: 50–100 ms. Athletes: 80–200+ ms.

### Definition 34.4.3 — RMSSD (Root Mean Square of Successive Differences)

$$
RMSSD = \sqrt{\frac{1}{N-1}\sum_{i=1}^{N-1}(RR_{i+1} - RR_i)^2}
$$

Reflects **short-term** (beat-to-beat) variability, primarily mediated by the **parasympathetic** (vagal) nervous system. Normal: 20–50 ms. Athletes: 60–150+ ms.

### Definition 34.4.4 — pNN50

$$
pNN50 = \frac{\text{Number of } |RR_{i+1} - RR_i| > 50 \text{ ms}}{N-1} \times 100\%
$$

Percentage of successive differences exceeding 50 ms. Higher values indicate greater parasympathetic activity.

### Definition 34.4.5 — Frequency Domain Bands

| Band | Frequency Range | Physiological Correlate |
|:---|:---|:---|
| **VLF** | 0.003–0.04 Hz | Thermoregulation, RAAS, slow hormonal |
| **LF** | 0.04–0.15 Hz | Mixed sympathetic + parasympathetic (baroreflex) |
| **HF** | 0.15–0.40 Hz | Parasympathetic (respiratory sinus arrhythmia) |

### Definition 34.4.6 — LF/HF Ratio

$$
\frac{LF}{HF} = \frac{\int_{0.04}^{0.15} PSD(f)\,df}{\int_{0.15}^{0.40} PSD(f)\,df}
$$

Historically interpreted as "sympathovagal balance" (higher = more sympathetic). Modern interpretation: this is an oversimplification; LF contains both sympathetic and parasympathetic components.

### Definition 34.4.7 — Respiratory Sinus Arrhythmia (RSA)

The natural variation in heart rate synchronized with breathing:
- **Inspiration:** HR increases (vagal withdrawal)
- **Expiration:** HR decreases (vagal activation)

RSA amplitude is a direct index of cardiac vagal tone. At 33 BPM with slow breathing (6 breaths/min = 0.1 Hz), RSA may shift into the LF band.

### Definition 34.4.8 — Polyvagal Hierarchy (Porges)

Three phylogenetically ordered autonomic states:

1. **Ventral Vagal Complex** (VVC): Social engagement, calm alertness, high HRV
2. **Sympathetic Nervous System** (SNS): Fight/flight, elevated HR, reduced HRV
3. **Dorsal Vagal Complex** (DVC): Freeze/shutdown, extreme bradycardia, conservation

The 33 BPM athlete operates primarily in a **VVC-dominant** state with strong DVC contribution — NOT pathological freeze, but trained cardiovascular efficiency.

---

## 📐 2. Axioms / Postulates

### Axiom 34.4.A1 — Autonomic Dual Innervation

The sinoatrial (SA) node receives both:
- **Sympathetic** input (accelerates HR via norepinephrine → β₁ receptors)
- **Parasympathetic** input (decelerates HR via acetylcholine → muscarinic M₂ receptors)

At rest, parasympathetic tone dominates ("vagal brake"). The intrinsic SA node rate without any autonomic input is ~100 BPM.

### Axiom 34.4.A2 — Stationarity Requirement

HRV frequency-domain analysis assumes the R-R interval time series is **weakly stationary** (constant mean and variance) over the analysis window. Standard: 5-minute recordings for short-term analysis.

### Axiom 34.4.A3 — Nyquist Criterion for HRV Sampling

The R-R interval series is irregularly sampled (one sample per heartbeat). For frequency analysis, it must be resampled at a uniform rate. The effective sampling rate is:

$$
f_s \approx \frac{1}{\overline{RR}} = \frac{HR}{60}
$$

At 33 BPM: $f_s = 0.55$ Hz. Nyquist frequency = 0.275 Hz — barely covers the HF band (0.15–0.4 Hz). This is why athletes with very low HR need longer recording windows.

---

## 🛡️ 3. Lemmas

### Lemma 34.4.1 — Relationship Between RMSSD and HF Power

RMSSD is mathematically related to the high-frequency component of HRV. For a signal dominated by a single sinusoidal component at frequency $f$:

$$
RMSSD \approx 2\sin(\pi f \cdot \overline{RR}) \times \text{amplitude}
$$

In practice, $\ln(RMSSD)$ correlates with $\ln(HF)$ at $r > 0.95$.

### Lemma 34.4.2 — Welch's Method for PSD Estimation

The power spectral density is estimated by:
1. Divide the N-point signal into overlapping segments of length $L$ with overlap $D$
2. Apply a window function (Hanning) to each segment
3. Compute the FFT of each windowed segment
4. Average the squared magnitudes:

$$
\hat{P}(f) = \frac{1}{K \cdot L \cdot U}\sum_{k=1}^{K}\left|\sum_{n=0}^{L-1}x_k(n)w(n)e^{-j2\pi fn/L}\right|^2
$$

where $U = \frac{1}{L}\sum_{n=0}^{L-1}|w(n)|^2$ is the window normalization factor.

### Lemma 34.4.3 — Ectopic Beat Detection

Ectopic beats (premature ventricular contractions) must be removed before HRV analysis. A beat is flagged as ectopic if:

$$
|RR_i - \text{median}(RR_{i-5:i+5})| > 0.20 \times \text{median}(RR_{i-5:i+5})
$$

(More than 20% deviation from local median.)

---

## 👑 4. Theorems

### Theorem 34.4.1 — Parseval's Theorem Applied to HRV

Total variance equals total spectral power:

$$
SDNN^2 = \text{Var}(RR) = \int_0^{f_{\text{Nyquist}}} PSD(f)\,df = P_{VLF} + P_{LF} + P_{HF}
$$

### Theorem 34.4.2 — Vagal Tone Index

For short-term recordings (5 min), the primary parasympathetic indices are:
- **RMSSD** (time domain)
- **HF power** (frequency domain)
- **SD1** from Poincaré plot (geometric)

These are mathematically related:

$$
SD1 = \frac{RMSSD}{\sqrt{2}}
$$

### Theorem 34.4.3 — Polyvagal State Classification

| HRV Pattern | RMSSD | LF/HF | Interpretation |
|:---|:---|:---|:---|
| High RMSSD, low LF/HF | >80 ms | <1.0 | Ventral vagal dominant (recovery) |
| Low RMSSD, high LF/HF | <20 ms | >3.0 | Sympathetic dominant (stress/exercise) |
| Very high RMSSD, very low HR | >120 ms | <0.5 | Dorsal vagal + trained (Athlete's Heart) |
| Very low RMSSD, very low HR | <10 ms | variable | Pathological bradycardia (sick sinus) |

The 33 BPM athlete should show: RMSSD > 100 ms, HF power dominant, LF/HF < 1.0.

### Theorem 34.4.4 — Baroreflex Sensitivity from HRV

The arterial baroreflex modulates HR in response to blood pressure changes. Baroreflex sensitivity (BRS) can be estimated from the LF component:

$$
BRS \approx \sqrt{\frac{P_{LF,RR}}{P_{LF,SBP}}} \quad \text{(ms/mmHg)}
$$

Alternatively, using the sequence method: identify sequences of 3+ consecutive beats where both SBP and RR increase (or decrease):

$$
BRS = \frac{\Delta RR}{\Delta SBP} \quad \text{(slope of regression)}
$$

Normal: 10–15 ms/mmHg. Athletes: 20–40 ms/mmHg (enhanced baroreflex gain).

High BRS in the 33 BPM athlete means small blood pressure fluctuations produce large HR adjustments — contributing to the high HRV.

---


## ✍️ 5. Physics & Math Derivations

### 5.1 Derivation — RMSSD Computation Step-by-Step

**Given:** R-R intervals (ms): $[1780, 1850, 1790, 1870, 1810, 1900, 1820, 1860]$

**Step 1:** Compute successive differences:

$$
\Delta RR_i = RR_{i+1} - RR_i
$$

$$
\Delta RR = [70, -60, 80, -60, 90, -80, 40]
$$

**Step 2:** Square each difference:

$$
(\Delta RR)^2 = [4900, 3600, 6400, 3600, 8100, 6400, 1600]
$$

**Step 3:** Mean of squared differences:

$$
\overline{(\Delta RR)^2} = \frac{4900 + 3600 + 6400 + 3600 + 8100 + 6400 + 1600}{7} = \frac{34600}{7} = 4942.9
$$

**Step 4:** Square root:

$$
RMSSD = \sqrt{4942.9} = 70.3 \text{ ms}
$$

This is consistent with a well-trained athlete (normal untrained: 20–50 ms).

---

### 5.2 Derivation — Power Spectral Density via FFT

**Step 1:** Given $N$ uniformly resampled R-R intervals at rate $f_s = 4$ Hz (standard for HRV), compute the DFT:

$$
X(k) = \sum_{n=0}^{N-1} x(n) \cdot e^{-j2\pi kn/N}, \quad k = 0, 1, \ldots, N-1
$$

**Step 2:** The one-sided PSD estimate:

$$
PSD(f_k) = \frac{2}{N \cdot f_s} |X(k)|^2, \quad f_k = \frac{k \cdot f_s}{N}
$$

**Step 3:** Frequency resolution:

$$
\Delta f = \frac{f_s}{N} = \frac{4}{N}
$$

For a 5-minute recording at 33 BPM: ~165 beats. After resampling at 4 Hz: $N = 5 \times 60 \times 4 = 1200$ samples. Resolution: $\Delta f = 4/1200 = 0.0033$ Hz.

**Step 4:** Integrate over bands:

$$
P_{LF} = \sum_{k: 0.04 \leq f_k < 0.15} PSD(f_k) \cdot \Delta f
$$

$$
P_{HF} = \sum_{k: 0.15 \leq f_k \leq 0.40} PSD(f_k) \cdot \Delta f
$$

---

### 5.3 Derivation — Poincaré Plot Geometry

A **Poincaré plot** graphs $RR_{i+1}$ vs. $RR_i$. The resulting cloud is characterized by:

**Step 1:** Define the line of identity: $RR_{i+1} = RR_i$.

**Step 2:** SD1 (perpendicular to identity line) measures short-term variability:

$$
SD1 = \sqrt{\frac{1}{2}\text{Var}(RR_{i+1} - RR_i)} = \frac{RMSSD}{\sqrt{2}}
$$

**Derivation of SD1 = RMSSD/√2:**

The variance of successive differences:

$$
\text{Var}(\Delta RR) = \frac{1}{N-1}\sum_{i=1}^{N-1}(\Delta RR_i - \overline{\Delta RR})^2
$$

If the mean successive difference is approximately zero (stationary signal):

$$
\text{Var}(\Delta RR) \approx \frac{1}{N-1}\sum(\Delta RR_i)^2 = RMSSD^2
$$

The dispersion perpendicular to the identity line is:

$$
SD1 = \frac{1}{\sqrt{2}}\sqrt{\text{Var}(\Delta RR)} = \frac{RMSSD}{\sqrt{2}}
$$

**Step 3:** SD2 (along identity line) measures long-term variability:

$$
SD2 = \sqrt{2 \cdot SDNN^2 - \frac{1}{2}RMSSD^2}
$$

---

### 5.4 Derivation — Resampling Irregularly-Spaced R-R Data

R-R intervals are inherently non-uniformly sampled (one sample per beat). For FFT, we need uniform sampling.

**Step 1:** Create cumulative time axis:

$$
t_i = \sum_{k=1}^{i} RR_k, \quad t_0 = 0
$$

**Step 2:** The R-R interval at time $t_i$ is $RR_i$. Interpolate onto uniform grid using cubic spline:

$$
RR_{\text{uniform}}(t) = \text{CubicSpline}(t_i, RR_i)(t_{\text{grid}})
$$

where $t_{\text{grid}} = [0, \Delta t, 2\Delta t, \ldots]$ with $\Delta t = 1/f_s = 0.25$ s (for 4 Hz resampling).

**Step 3:** Remove the mean (detrend) before FFT:

$$
x(n) = RR_{\text{uniform}}(n\Delta t) - \overline{RR}
$$

---

## 🧬 6. Biological Impact

### Autonomic Nervous System Architecture

The ANS has two main divisions controlling heart rate:

**Parasympathetic (Vagal) Pathway:**
1. Nucleus ambiguus (ventral vagal) → myelinated vagus nerve
2. Dorsal motor nucleus (dorsal vagal) → unmyelinated vagus
3. Synapse at cardiac ganglia on SA node
4. Release acetylcholine (ACh) → M₂ muscarinic receptors
5. Opens K⁺ channels (IKACh) → hyperpolarizes SA node → slows HR
6. **Response time: 200–600 ms** (fast, beat-to-beat control)

**Sympathetic Pathway:**
1. Intermediolateral cell column (T1–T4 spinal cord)
2. Preganglionic → stellate ganglion
3. Postganglionic → SA node
4. Release norepinephrine → β₁ adrenergic receptors
5. Increases cAMP → increases If (funny current) → accelerates HR
6. **Response time: 2–5 seconds** (slow, sustained changes)

### Why 33 BPM is Healthy (Not Pathological)

| Feature | Athlete's Bradycardia | Sick Sinus Syndrome |
|:---|:---|:---|
| HRV (RMSSD) | Very high (>100 ms) | Very low (<10 ms) |
| HR response to exercise | Normal increase to 190+ | Blunted, fails to rise |
| ECG morphology | Normal P-QRS-T | Pauses, escape rhythms |
| Symptoms | None (asymptomatic) | Syncope, fatigue |
| LV ejection fraction | >60% | Often reduced |
| Mechanism | Enhanced vagal tone | SA node fibrosis |

### Circadian HRV Patterns in Athletes

- **Sleep (2–5 AM):** Maximum HRV, HR may drop to 28–30 BPM, HF power peaks
- **Waking (6–8 AM):** Sympathetic surge, HR rises, LF/HF increases
- **Training (variable):** HRV suppressed during exercise, rebounds post-exercise
- **Recovery window (1–4 hours post-training):** Parasympathetic reactivation — faster reactivation = better fitness

### Overtraining Detection via HRV

Chronic overtraining manifests as:
- **Decreased resting RMSSD** (parasympathetic withdrawal)
- **Elevated resting HR** (2–5 BPM above baseline)
- **Reduced HRV complexity** (loss of fractal scaling)
- **Blunted orthostatic response** (standing HR increase <10 BPM)

---

## 💻 7. Software Implementation

### 7.1 Complete HRV Analysis Pipeline

```python
import numpy as np
from scipy import signal, interpolate

class HRVAnalyzer:
    """Complete HRV analysis from R-R intervals."""
    
    def __init__(self, rr_intervals_ms: np.ndarray):
        """
        Args:
            rr_intervals_ms: Array of R-R intervals in milliseconds
        """
        self.rr = rr_intervals_ms.astype(float)
        self.rr_clean = self._remove_ectopics()
    
    def _remove_ectopics(self, threshold: float = 0.20) -> np.ndarray:
        """Remove ectopic beats using median filter criterion."""
        rr = self.rr.copy()
        for i in range(2, len(rr) - 2):
            local_median = np.median(rr[max(0,i-5):i+5])
            if abs(rr[i] - local_median) > threshold * local_median:
                rr[i] = local_median  # replace with local median
        return rr
    
    def time_domain(self) -> dict:
        """Compute time-domain HRV metrics."""
        rr = self.rr_clean
        N = len(rr)
        
        mean_rr = np.mean(rr)
        sdnn = np.std(rr, ddof=1)
        
        # Successive differences
        diff_rr = np.diff(rr)
        rmssd = np.sqrt(np.mean(diff_rr**2))
        
        # pNN50
        nn50 = np.sum(np.abs(diff_rr) > 50)
        pnn50 = (nn50 / (N - 1)) * 100
        
        mean_hr = 60000.0 / mean_rr
        
        return {
            'mean_RR_ms': mean_rr,
            'SDNN_ms': sdnn,
            'RMSSD_ms': rmssd,
            'pNN50_percent': pnn50,
            'mean_HR_bpm': mean_hr,
            'N_beats': N
        }
    
    def frequency_domain(self, fs_resample: float = 4.0, method: str = 'welch') -> dict:
        """Compute frequency-domain HRV metrics.
        
        Args:
            fs_resample: Resampling frequency for uniform grid (Hz)
            method: 'welch' or 'fft'
        """
        rr = self.rr_clean
        
        # Create cumulative time axis
        t_beats = np.cumsum(rr) / 1000.0  # convert to seconds
        t_beats = t_beats - t_beats[0]
        
        # Uniform resampling via cubic spline
        t_uniform = np.arange(0, t_beats[-1], 1.0/fs_resample)
        cs = interpolate.CubicSpline(t_beats, rr)
        rr_uniform = cs(t_uniform)
        
        # Detrend
        rr_detrended = rr_uniform - np.mean(rr_uniform)
        
        # PSD estimation
        if method == 'welch':
            nperseg = min(256, len(rr_detrended) // 2)
            freqs, psd = signal.welch(rr_detrended, fs=fs_resample,
                                       nperseg=nperseg, noverlap=nperseg//2)
        else:
            freqs = np.fft.rfftfreq(len(rr_detrended), d=1.0/fs_resample)
            fft_vals = np.fft.rfft(rr_detrended * np.hanning(len(rr_detrended)))
            psd = (2.0 / (len(rr_detrended) * fs_resample)) * np.abs(fft_vals)**2
        
        # Integrate bands
        vlf_mask = (freqs >= 0.003) & (freqs < 0.04)
        lf_mask = (freqs >= 0.04) & (freqs < 0.15)
        hf_mask = (freqs >= 0.15) & (freqs <= 0.40)
        
        df = freqs[1] - freqs[0] if len(freqs) > 1 else 1
        vlf_power = np.trapz(psd[vlf_mask], freqs[vlf_mask]) if vlf_mask.any() else 0
        lf_power = np.trapz(psd[lf_mask], freqs[lf_mask]) if lf_mask.any() else 0
        hf_power = np.trapz(psd[hf_mask], freqs[hf_mask]) if hf_mask.any() else 0
        
        total_power = vlf_power + lf_power + hf_power
        lf_hf_ratio = lf_power / hf_power if hf_power > 0 else float('inf')
        
        return {
            'VLF_ms2': vlf_power,
            'LF_ms2': lf_power,
            'HF_ms2': hf_power,
            'Total_Power_ms2': total_power,
            'LF_HF_ratio': lf_hf_ratio,
            'LF_nu': lf_power / (lf_power + hf_power) * 100 if (lf_power + hf_power) > 0 else 0,
            'HF_nu': hf_power / (lf_power + hf_power) * 100 if (lf_power + hf_power) > 0 else 0,
        }
    
    def poincare(self) -> dict:
        """Compute Poincaré plot descriptors."""
        rr = self.rr_clean
        rr1 = rr[:-1]
        rr2 = rr[1:]
        
        diff = rr2 - rr1
        sd1 = np.std(diff, ddof=1) / np.sqrt(2)
        sd2 = np.sqrt(2 * np.std(rr, ddof=1)**2 - sd1**2)
        
        return {'SD1_ms': sd1, 'SD2_ms': sd2, 'SD1_SD2_ratio': sd1/sd2 if sd2 > 0 else 0}
```

### 7.2 Synthetic R-R Data Generator (for Testing)

```python
def generate_synthetic_rr(mean_rr: float = 1818.0, rmssd_target: float = 100.0,
                           n_beats: int = 300, seed: int = 42) -> np.ndarray:
    """Generate synthetic R-R intervals with specified HRV characteristics.
    
    Models RSA (respiratory sinus arrhythmia) + random variability.
    """
    rng = np.random.default_rng(seed)
    
    # Respiratory component (RSA at 0.25 Hz = 15 breaths/min)
    t = np.cumsum(np.full(n_beats, mean_rr / 1000))  # approximate time
    rsa_amplitude = rmssd_target * 0.7  # RSA contributes ~70% of RMSSD
    rsa = rsa_amplitude * np.sin(2 * np.pi * 0.25 * t)
    
    # Random (Mayer wave at ~0.1 Hz + noise)
    mayer = (rmssd_target * 0.3) * np.sin(2 * np.pi * 0.1 * t)
    noise = rng.normal(0, rmssd_target * 0.2, n_beats)
    
    rr = mean_rr + rsa + mayer + noise
    rr = np.clip(rr, mean_rr * 0.7, mean_rr * 1.3)  # physiological bounds
    
    return rr
```

---

## 🧮 8. Worked Examples

<details>
<summary>Example 1: Complete Time-Domain HRV from 10 Beats</summary>

**Problem:** R-R intervals (ms): [1820, 1780, 1860, 1790, 1880, 1810, 1850, 1770, 1890, 1830]. Compute mean RR, SDNN, RMSSD, pNN50.

**Solution:**

**Step 1:** Mean RR:

$$
\overline{RR} = \frac{1820+1780+1860+1790+1880+1810+1850+1770+1890+1830}{10} = \frac{18280}{10} = 1828.0 \text{ ms}
$$

Mean HR = $60000/1828 = 32.8$ BPM ✓

**Step 2:** SDNN:

$$
\text{Deviations} = [-8, -48, 32, -38, 52, -18, 22, -58, 62, 2]
$$

$$
\text{Squared} = [64, 2304, 1024, 1444, 2704, 324, 484, 3364, 3844, 4]
$$

$$
SDNN = \sqrt{\frac{15560}{9}} = \sqrt{1728.9} = 41.6 \text{ ms}
$$

**Step 3:** RMSSD:

$$
\Delta RR = [-40, 80, -70, 90, -70, 40, -80, 120, -60]
$$

$$
(\Delta RR)^2 = [1600, 6400, 4900, 8100, 4900, 1600, 6400, 14400, 3600]
$$

$$
RMSSD = \sqrt{\frac{51900}{9}} = \sqrt{5766.7} = 75.9 \text{ ms}
$$

**Step 4:** pNN50:

Successive differences > 50 ms: $|{-40}|=40$ ✗, $|80|$ ✓, $|{-70}|$ ✓, $|90|$ ✓, $|{-70}|$ ✓, $|40|$ ✗, $|{-80}|$ ✓, $|120|$ ✓, $|{-60}|$ ✓

Count = 7 out of 9.

$$
pNN50 = \frac{7}{9} \times 100 = 77.8\%
$$

**Interpretation:** RMSSD = 75.9 ms and pNN50 = 77.8% indicate strong parasympathetic dominance — consistent with the 33 BPM athlete profile.

</details>

<details>
<summary>Example 2: Frequency-Domain Analysis Interpretation</summary>

**Problem:** A 5-minute HRV recording yields: VLF = 1200 ms², LF = 800 ms², HF = 2400 ms². Compute LF/HF ratio, normalized units, and interpret for the 33 BPM athlete.

**Solution:**

**Step 1:** LF/HF ratio:

$$
\frac{LF}{HF} = \frac{800}{2400} = 0.33
$$

**Step 2:** Normalized units:

$$
LF_{nu} = \frac{800}{800 + 2400} \times 100 = \frac{800}{3200} \times 100 = 25\%
$$

$$
HF_{nu} = \frac{2400}{3200} \times 100 = 75\%
$$

**Step 3:** Total power:

$$
P_{\text{total}} = 1200 + 800 + 2400 = 4400 \text{ ms}^2
$$

**Interpretation:**
- LF/HF = 0.33 (< 1.0): Strong parasympathetic dominance
- HF_nu = 75%: Three-quarters of the variability is in the respiratory (vagal) band
- Total power = 4400 ms²: High overall variability (healthy)
- This pattern is classic for a resting athlete with enhanced vagal tone

</details>

<details>
<summary>Example 3: Detecting Overtraining via HRV Trend</summary>

**Problem:** An athlete's morning RMSSD over 7 days: [105, 98, 92, 78, 72, 68, 65] ms. Baseline RMSSD = 105 ms. At what point should training load be reduced?

**Solution:**

**Step 1:** Compute the coefficient of variation (CV) of the 7-day rolling RMSSD:

$$
\overline{RMSSD} = \frac{105+98+92+78+72+68+65}{7} = \frac{578}{7} = 82.6 \text{ ms}
$$

$$
SD = \sqrt{\frac{\sum(x_i - 82.6)^2}{6}} = \sqrt{\frac{(22.4^2+15.4^2+9.4^2+4.6^2+10.6^2+14.6^2+17.6^2)}{6}}
$$

$$
= \sqrt{\frac{501.8+237.2+88.4+21.2+112.4+213.2+309.8}{6}} = \sqrt{\frac{1484}{6}} = \sqrt{247.3} = 15.7 \text{ ms}
$$

$$
CV = \frac{15.7}{82.6} = 19.0\%
$$

**Step 2:** Apply the "smallest worthwhile change" criterion (Plews et al., 2013):

A decline of > 0.5 × CV from baseline indicates meaningful parasympathetic suppression:

$$
\text{Threshold} = 0.5 \times 15.7 = 7.9 \text{ ms below rolling mean}
$$

Alternatively, a decline > 1 SD below baseline:

$$
\text{Alert threshold} = 105 - 15.7 = 89.3 \text{ ms}
$$

**Step 3:** Day 4 (RMSSD = 78 ms) crosses below the alert threshold. Training load should be reduced by Day 4.

**Step 4:** The consistent downward trend (no recovery days showing bounce-back) suggests accumulated fatigue — recommend 2–3 days of active recovery.

</details>

---

## 🔗 9. Cross-links & Further Reading

### Internal Cross-links
- [34.3 - Cardiovascular Bioenergetics & VO2 Max](34.3---Cardiovascular-Bioenergetics-&-VO2-Max) — Cardiac output and the 33 BPM heart
- [34.7 - Building Bio-metric Software Applications](34.7---Building-Bio-metric-Software-Applications) — Implementing HRV in mobile apps
- [05 - Neuroscience & Computational Cognition](05---Neuroscience-&-Computational-Cognition) — Neural control of autonomic function
- [06 - Behavioral Psychology & Reinforcement Learning](06---Behavioral-Psychology-&-Reinforcement-Learning) — Polyvagal theory and behavioral states
- [34.5 - Sensor Fusion - Accelerometers & Gyroscopes](34.5---Sensor-Fusion---Accelerometers-&-Gyroscopes) — Combining HRV with motion data

### Additional Derivations

#### DFA Alpha-1 (Detrended Fluctuation Analysis)

A non-linear HRV metric that quantifies fractal scaling:

**Step 1:** Integrate the RR time series (cumulative sum of deviations from mean):

$$
y(k) = \sum_{i=1}^{k}(RR_i - \overline{RR})
$$

**Step 2:** Divide into windows of size $n$, fit a linear trend $y_n(k)$ in each window.

**Step 3:** Compute the fluctuation function:

$$
F(n) = \sqrt{\frac{1}{N}\sum_{k=1}^{N}[y(k) - y_n(k)]^2}
$$

**Step 4:** Plot $\log F(n)$ vs. $\log n$. The slope is $\alpha_1$ (for short-term, $n = 4\text{–}16$ beats):

$$
F(n) \propto n^{\alpha_1}
$$

**Interpretation:**
- $\alpha_1 \approx 1.0$: Healthy, correlated fluctuations (fractal)
- $\alpha_1 \approx 0.5$: Uncorrelated (white noise) — loss of complexity
- $\alpha_1 \approx 1.5$: Brownian noise — over-correlated (pathological)
- Athletes at rest: $\alpha_1 = 1.0\text{–}1.2$ (healthy fractal scaling)
- During exercise: $\alpha_1$ decreases toward 0.5 (loss of parasympathetic modulation)

#### Sample Entropy (SampEn)

Measures the complexity/regularity of the RR time series:

$$
SampEn(m, r, N) = -\ln\frac{A}{B}
$$

where $A$ = number of template matches of length $m+1$ within tolerance $r$, and $B$ = matches of length $m$.

Standard parameters: $m = 2$, $r = 0.2 \times SDNN$.

- Higher SampEn = more complex/irregular = healthier
- Lower SampEn = more regular/predictable = reduced autonomic modulation
- Athletes: SampEn typically 1.5–2.0 (high complexity)

### Authoritative Sources
- **Porges, S.W.** (2011). *The Polyvagal Theory: Neurophysiological Foundations of Emotions, Attachment, Communication, and Self-Regulation*. Norton.
- **Task Force of ESC/NASPE** (1996). "Heart Rate Variability: Standards of Measurement, Interpretation, and Clinical Use." *European Heart Journal*, 17, 354–381.
- **Plews, D.J. et al.** (2013). "Training Adaptation and Heart Rate Variability in Elite Endurance Athletes." *International Journal of Sports Physiology and Performance*.
- **Shaffer, F. & Ginsberg, J.P.** (2017). "An Overview of Heart Rate Variability Metrics and Norms." *Frontiers in Public Health*, 5, 258.
- **Goldberger, A.L. et al.** (2002). "Fractal dynamics in physiology: Alterations with disease and aging." *PNAS*, 99, 2466–2472.

---
