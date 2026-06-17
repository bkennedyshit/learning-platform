---
title: "34.7 — Building Bio-metric Software Applications"
subject: "Biomechanics & HCI"
catalog: advanced
audience_tier: higher-education
chapter: "34.7"
type: chapter-note
objectives:
  - "Understand the concepts"
  - "Apply the theory"
open_source: true
---

*Back to [Subject_Plan](Subject_Plan) | Part of [34 - Biomechanics & HCI](34---Biomechanics-&-HCI)*

# 34.7 — Building Bio-metric Software Applications

> *"The best interface is no interface."* — Golden Krishna, 2015 (adapted from Don Norman's principle of invisible design)

This capstone chapter synthesizes all prior knowledge — kinematics, rotational dynamics, cardiovascular physiology, HRV analysis, sensor fusion, and HCI design — into a complete software architecture for bio-tracking applications. We build from Bluetooth Low Energy (BLE) heart rate monitor communication through real-time data processing to cloud-based analytics and visualization.

---

## 🎯 Learning Objectives

1. Architect a **full-stack bio-tracking system** (sensor → mobile → cloud → analytics).
2. Implement **BLE communication** with heart rate monitors using Flutter/Dart.
3. Design **real-time data pipelines** for streaming physiological data.
4. Build **offline-first** mobile applications with local storage and sync.
5. Implement **post-processing analytics** with Python (pandas, matplotlib, scipy).
6. Apply **software design patterns** appropriate for bio-tracking (Observer, Repository, MVVM).
7. Handle **data quality** issues (dropouts, artifacts, sensor disconnection).

---

## 🖼️ Visual Anchor — Bio-Tracking System Architecture

![track-13__13.7-fig1](track-13__13.7-fig1.svg)

---

## 📚 1. Definitions

### Definition 34.7.1 — Bluetooth Low Energy (BLE) GATT Profile

The **Generic Attribute Profile** (GATT) defines how BLE devices expose data:
- **Service:** A collection of related characteristics (e.g., Heart Rate Service UUID: `0x180D`)
- **Characteristic:** A single data point (e.g., Heart Rate Measurement: `0x2A37`)
- **Descriptor:** Metadata about a characteristic (e.g., Client Characteristic Configuration for notifications)

### Definition 34.7.2 — Heart Rate Measurement Characteristic (0x2A37)

The BLE Heart Rate Measurement packet format:

| Byte | Field | Description |
|:---|:---|:---|
| 0 | Flags | Bit 0: HR format (0=UINT8, 1=UINT16) |
| 1 (or 1-2) | Heart Rate | BPM value |
| Next 2 bytes | RR Interval | 1/1024 s resolution (if flag bit 4 set) |

**Critical:** R-R intervals are in units of 1/1024 seconds. Convert to ms: $RR_{ms} = RR_{raw} \times 1000/1024$.

### Definition 34.7.3 — MVVM Architecture Pattern

**Model-View-ViewModel** separates concerns:
- **Model:** Data layer (BLE service, local DB, API client)
- **View:** UI widgets (Flutter widgets displaying HR, charts)
- **ViewModel:** Business logic (HRV computation, state management)

### Definition 34.7.4 — Repository Pattern

A **Repository** abstracts data sources behind a unified interface:

```
HRRepository
├── LocalDataSource (SQLite)
├── RemoteDataSource (REST API)
└── BLEDataSource (real-time stream)
```

The ViewModel only talks to the Repository, never directly to data sources.

### Definition 34.7.5 — Reactive Streams (Rx Pattern)

BLE data arrives as an asynchronous stream. The **Observer pattern** (via Dart Streams / RxDart) handles this:

$$
\text{BLE Notifications} \xrightarrow{\text{Stream}} \text{Transform} \xrightarrow{\text{map/filter}} \text{UI Update}
$$

### Definition 34.7.6 — Offline-First Architecture

Data is always written to local storage first, then synced to cloud when connectivity is available. This ensures:
- No data loss during outdoor activities (poor signal)
- Instant UI responsiveness (no network latency)
- Conflict resolution via timestamps

---

## 📐 2. Axioms / Postulates

### Axiom 34.7.A1 — Data Integrity First

No physiological data point should ever be lost due to software failure. Design principle: **write-ahead logging** — persist raw sensor data before any processing.

### Axiom 34.7.A2 — Real-Time Constraint

Heart rate display must update within 1 second of the physical heartbeat. BLE notification latency (~20–100 ms) + processing (~5 ms) + UI render (~16 ms) = well within budget.

### Axiom 34.7.A3 — Privacy by Design

Biometric data is sensitive (GDPR Article 9, HIPAA). Architecture must:
- Encrypt data at rest (AES-256)
- Encrypt in transit (TLS 1.3)
- Minimize cloud storage (process locally when possible)
- Provide data export and deletion capabilities

---

## 🛡️ 3. Lemmas

### Lemma 34.7.1 — BLE Throughput for Heart Rate

Heart Rate Service notification rate: 1 Hz (one packet per second).
Each packet: 2–6 bytes (flags + HR + optional RR intervals).
Throughput: ~48 bits/s — trivial for BLE (theoretical max: 1 Mbps).

Multiple RR intervals can be packed into one notification (up to 9 RR values per packet for very fast heart rates).

### Lemma 34.7.2 — Local Storage Requirements

For continuous HR + RR recording:
- 1 HR value/s × 4 bytes = 4 B/s
- ~2 RR intervals/s × 4 bytes = 8 B/s
- Total: ~12 B/s = 43.2 KB/hour = 1.04 MB/day (24h recording)

SQLite can easily handle years of data on a mobile device.

### Lemma 34.7.3 — Battery Impact of BLE

BLE heart rate monitoring power consumption:
- Phone BLE radio: ~5–15 mW during active connection
- Typical phone battery: 15,000 mWh (4000 mAh × 3.7V)
- BLE-only drain: 15 mW × 24h = 360 mWh = 2.4% of battery per day

Negligible impact — BLE was designed for this use case.

---

## 👑 4. Theorems

### Theorem 34.7.1 — Minimum Viable Bio-Tracking Architecture

A complete bio-tracking application requires exactly 5 layers:

1. **Sensor Layer:** BLE communication, raw data acquisition
2. **Processing Layer:** Artifact removal, HRV computation, sensor fusion
3. **Storage Layer:** Local persistence, data model, export
4. **Presentation Layer:** Real-time UI, charts, notifications
5. **Sync Layer:** Cloud backup, cross-device access, sharing

Each layer communicates only with adjacent layers (layered architecture principle).

### Theorem 34.7.2 — Data Quality Pipeline

Raw sensor data must pass through a quality pipeline before analysis:

$$
\text{Raw} \xrightarrow{\text{1. Validate}} \xrightarrow{\text{2. Filter}} \xrightarrow{\text{3. Interpolate}} \xrightarrow{\text{4. Compute}} \text{Clean Metrics}
$$

1. **Validate:** Reject physiologically impossible values (HR < 20 or > 250)
2. **Filter:** Remove ectopic beats (>20% deviation from local median)
3. **Interpolate:** Fill gaps from missed BLE notifications (cubic spline)
4. **Compute:** Calculate derived metrics (RMSSD, SDNN, frequency domain)

### Theorem 34.7.3 — State Management for Real-Time Bio Data

The application state machine for a recording session:

$$
\text{Idle} \xrightarrow{\text{connect}} \text{Connected} \xrightarrow{\text{start}} \text{Recording} \xrightarrow{\text{stop}} \text{Saving} \xrightarrow{\text{done}} \text{Idle}
$$

Error transitions: any state → Disconnected → auto-reconnect → previous state.

---


## ✍️ 5. Physics & Math Derivations

### 5.1 Derivation — BLE Heart Rate Packet Parsing

**Given:** Raw BLE notification bytes: `[0x16, 0x21, 0x1C, 0x03, 0x20, 0x03]`

**Step 1:** Parse flags byte (0x16 = 0b00010110):
- Bit 0 = 0: HR is UINT8 (1 byte)
- Bit 1 = 1: Sensor contact detected
- Bit 2 = 1: Sensor contact supported
- Bit 3 = 0: Energy expended not present
- Bit 4 = 1: RR intervals present

**Step 2:** Parse HR value (byte 1):
- HR = 0x21 = 33 BPM ✓ (our athlete!)

**Step 3:** Parse RR intervals (remaining bytes, UINT16 little-endian):
- RR₁ = 0x031C = 796 (in 1/1024 s units)
- RR₂ = 0x0320 = 800 (in 1/1024 s units)

**Step 4:** Convert to milliseconds:

$$
RR_1 = 796 \times \frac{1000}{1024} = 777.3 \text{ ms}
$$

$$
RR_2 = 800 \times \frac{1000}{1024} = 781.3 \text{ ms}
$$

**Step 5:** Verify: $60000 / 779.3 \approx 77$ BPM per interval... but HR shows 33 BPM.

This discrepancy indicates the sensor is reporting instantaneous RR for the most recent beats, while the displayed HR is a longer average. At 33 BPM, mean RR should be ~1818 ms. The 777 ms intervals suggest the athlete was exercising when these specific RR values were captured.

---

### 5.2 Derivation — Real-Time RMSSD Sliding Window

**Problem:** Compute RMSSD in real-time as new RR intervals arrive, without storing all history.

**Step 1:** Define a sliding window of size $W$ (e.g., last 30 beats):

$$
RMSSD_k = \sqrt{\frac{1}{W-1}\sum_{i=k-W+1}^{k-1}(RR_{i+1} - RR_i)^2}
$$

**Step 2:** Efficient update — maintain running sum of squared differences:

$$
S_k = S_{k-1} + (RR_k - RR_{k-1})^2 - (RR_{k-W+1} - RR_{k-W})^2
$$

$$
RMSSD_k = \sqrt{\frac{S_k}{W-1}}
$$

This is O(1) per new beat — no need to recompute from scratch.

**Step 3:** Implementation requires a circular buffer of size $W$ storing RR intervals.

---

### 5.3 Derivation — Data Synchronization Conflict Resolution

**Scenario:** User records on phone (offline), then syncs to cloud. Meanwhile, they edited a note on the web.

**Step 1:** Each record has a timestamp $t_{\text{modified}}$ and a version counter $v$.

**Step 2:** Conflict detection:

$$
\text{Conflict} \iff v_{\text{local}} \neq v_{\text{remote}} \text{ AND } t_{\text{local}} \neq t_{\text{remote}}
$$

**Step 3:** Resolution strategy for bio data:
- **Sensor data (immutable):** Last-write-wins (timestamps from sensor are authoritative)
- **User annotations:** Prompt user to choose
- **Computed metrics:** Recompute from raw data (deterministic)

---

### 5.4 Derivation — Battery Life Estimation for Continuous Monitoring

**Given:** Phone battery = 4000 mAh at 3.7V = 14,800 mWh.

**Step 1:** Power consumers during bio-tracking:

| Component | Power (mW) | Duty Cycle | Effective (mW) |
|:---|:---|:---|:---|
| BLE radio | 15 | 100% | 15 |
| CPU (processing) | 200 | 5% | 10 |
| Display (OLED, dim) | 100 | 30% | 30 |
| GPS (if enabled) | 150 | 100% | 150 |
| Baseline (OS, radios) | 50 | 100% | 50 |

**Step 2:** Total without GPS: $15 + 10 + 30 + 50 = 105$ mW

$$
t_{\text{battery}} = \frac{14800}{105} = 141 \text{ hours} = 5.9 \text{ days}
$$

**Step 3:** With GPS: $105 + 150 = 255$ mW

$$
t_{\text{battery}} = \frac{14800}{255} = 58 \text{ hours} = 2.4 \text{ days}
$$

**Conclusion:** BLE-only HR monitoring has negligible battery impact. GPS is the dominant consumer.

---

## 🧬 6. Biological Impact

### Data Quality Challenges from Physiology

**Why bio-data is noisy:**

1. **Motion artifact:** Chest strap shifts during BMX → false R-peaks or missed beats
2. **Sweat bridge:** Excessive sweating creates electrical shorts → erratic readings
3. **Ectopic beats:** Premature ventricular contractions (PVCs) create short-long RR pairs
4. **Respiratory artifact:** Deep breathing modulates HR by 10–30 BPM (RSA)
5. **Electrode contact:** Dry skin at start of exercise → poor signal for first 2–3 minutes

**Software mitigation strategies:**
- Motion artifact: Require 3+ consecutive valid beats before updating display
- Sweat: No software fix (hardware issue) — alert user to re-wet strap
- Ectopic beats: Median filter + 20% deviation threshold
- RSA: This is SIGNAL, not noise — preserve it for HRV analysis
- Contact: Show "acquiring signal..." state, don't display erratic values

### Physiological Constraints on Software Design

The 33 BPM athlete presents unique software challenges:

1. **Very long RR intervals (1818 ms):** UI must handle 1.8-second gaps between beats without showing "disconnected"
2. **High HRV:** RR intervals may vary 1500–2200 ms — the ectopic detection threshold must be wider
3. **Slow HR response:** Takes 30–60 seconds for HR to rise from 33 to 100 BPM at exercise onset — don't flag this as "sensor error"
4. **Multiple RR per notification:** At 33 BPM, only ~0.55 beats/second — BLE may send notifications with 0 or 1 RR interval

### Circadian Data Patterns

Software should account for:
- **Morning:** HR lowest (28–35 BPM), HRV highest — best time for baseline measurement
- **Post-meal:** HR elevated 5–10 BPM (digestive blood flow)
- **Training:** HR 33 → 190 BPM in 30 seconds (massive dynamic range)
- **Sleep:** HR may drop to 28 BPM with pauses up to 2.5 seconds (normal for athletes)

---

## 💻 7. Software Implementation

### 7.1 Flutter/Dart BLE Heart Rate Monitor

```dart
import 'dart:async';
import 'dart:typed_data';
import 'package:flutter_blue_plus/flutter_blue_plus.dart';

/// BLE Heart Rate Service UUIDs
class HRServiceUUIDs {
  static const heartRateService = '0000180d-0000-1000-8000-00805f9b34fb';
  static const heartRateMeasurement = '00002a37-0000-1000-8000-00805f9b34fb';
}

/// Parsed heart rate measurement data
class HeartRateData {
  final int heartRate;
  final List<double> rrIntervalsMs;
  final DateTime timestamp;

  HeartRateData({
    required this.heartRate,
    required this.rrIntervalsMs,
    DateTime? timestamp,
  }) : timestamp = timestamp ?? DateTime.now();
}

/// BLE Heart Rate Monitor connection manager
class BLEHeartRateManager {
  BluetoothDevice? _device;
  StreamSubscription? _subscription;
  final _dataController = StreamController<HeartRateData>.broadcast();

  Stream<HeartRateData> get dataStream => _dataController.stream;

  /// Parse raw BLE heart rate measurement characteristic
  HeartRateData parseHRMeasurement(List<int> bytes) {
    final flags = bytes[0];
    final isUint16 = (flags & 0x01) != 0;
    final hasRR = (flags & 0x10) != 0;

    int hr;
    int offset;
    if (isUint16) {
      hr = bytes[1] | (bytes[2] << 8);
      offset = 3;
    } else {
      hr = bytes[1];
      offset = 2;
    }

    // Skip energy expended if present
    if ((flags & 0x08) != 0) offset += 2;

    // Parse RR intervals (1/1024 second units)
    final rrIntervals = <double>[];
    if (hasRR) {
      while (offset + 1 < bytes.length) {
        final rrRaw = bytes[offset] | (bytes[offset + 1] << 8);
        rrIntervals.add(rrRaw * 1000.0 / 1024.0); // Convert to ms
        offset += 2;
      }
    }

    return HeartRateData(heartRate: hr, rrIntervalsMs: rrIntervals);
  }

  /// Connect to a heart rate monitor and start receiving data
  Future<void> connect(BluetoothDevice device) async {
    _device = device;
    await device.connect(autoConnect: true);

    final services = await device.discoverServices();
    final hrService = services.firstWhere(
      (s) => s.uuid.toString() == HRServiceUUIDs.heartRateService,
    );

    final hrChar = hrService.characteristics.firstWhere(
      (c) => c.uuid.toString() == HRServiceUUIDs.heartRateMeasurement,
    );

    await hrChar.setNotifyValue(true);
    _subscription = hrChar.onValueReceived.listen((bytes) {
      final data = parseHRMeasurement(bytes);
      _dataController.add(data);
    });
  }

  Future<void> disconnect() async {
    await _subscription?.cancel();
    await _device?.disconnect();
  }

  void dispose() {
    _dataController.close();
  }
}
```

### 7.2 Real-Time HRV ViewModel

```dart
import 'dart:math';

/// Sliding-window HRV computation
class HRVComputer {
  final int windowSize;
  final List<double> _rrBuffer = [];
  double _sumSquaredDiffs = 0;

  HRVComputer({this.windowSize = 30});

  /// Add new RR interval(s) and return updated metrics
  Map<String, double> addRR(List<double> newRRs) {
    for (final rr in newRRs) {
      if (_rrBuffer.isNotEmpty) {
        final diff = rr - _rrBuffer.last;
        _sumSquaredDiffs += diff * diff;
      }
      _rrBuffer.add(rr);

      // Remove oldest if window exceeded
      if (_rrBuffer.length > windowSize) {
        final oldDiff = _rrBuffer[1] - _rrBuffer[0];
        _sumSquaredDiffs -= oldDiff * oldDiff;
        _rrBuffer.removeAt(0);
      }
    }

    return compute();
  }

  Map<String, double> compute() {
    if (_rrBuffer.length < 2) return {};

    final n = _rrBuffer.length;
    final meanRR = _rrBuffer.reduce((a, b) => a + b) / n;
    final rmssd = sqrt(_sumSquaredDiffs / (n - 1));

    // SDNN
    final variance = _rrBuffer.map((rr) => pow(rr - meanRR, 2)).reduce((a, b) => a + b) / (n - 1);
    final sdnn = sqrt(variance);

    // pNN50
    int nn50 = 0;
    for (int i = 0; i < n - 1; i++) {
      if ((_rrBuffer[i + 1] - _rrBuffer[i]).abs() > 50) nn50++;
    }
    final pnn50 = nn50 / (n - 1) * 100;

    return {
      'meanRR': meanRR,
      'meanHR': 60000 / meanRR,
      'RMSSD': rmssd,
      'SDNN': sdnn,
      'pNN50': pnn50,
    };
  }
}
```

### 7.3 Python Post-Processing Pipeline

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal, interpolate

def load_session(filepath: str) -> pd.DataFrame:
    """Load exported session data (CSV with timestamp, hr, rr_ms columns)."""
    df = pd.read_csv(filepath, parse_dates=['timestamp'])
    df = df.sort_values('timestamp').reset_index(drop=True)
    return df


def clean_rr_data(rr: np.ndarray, threshold: float = 0.20) -> np.ndarray:
    """Remove ectopic beats using median filter."""
    rr_clean = rr.copy()
    for i in range(2, len(rr) - 2):
        local_med = np.median(rr[max(0,i-5):i+5])
        if abs(rr[i] - local_med) > threshold * local_med:
            rr_clean[i] = local_med
    return rr_clean


def compute_session_hrv(df: pd.DataFrame) -> dict:
    """Compute full HRV analysis for a session."""
    rr = df['rr_ms'].dropna().values
    rr_clean = clean_rr_data(rr)
    
    # Time domain
    diffs = np.diff(rr_clean)
    metrics = {
        'mean_RR': np.mean(rr_clean),
        'mean_HR': 60000 / np.mean(rr_clean),
        'SDNN': np.std(rr_clean, ddof=1),
        'RMSSD': np.sqrt(np.mean(diffs**2)),
        'pNN50': np.sum(np.abs(diffs) > 50) / len(diffs) * 100,
    }
    
    # Frequency domain
    t_beats = np.cumsum(rr_clean) / 1000
    t_uniform = np.arange(0, t_beats[-1], 0.25)  # 4 Hz
    cs = interpolate.CubicSpline(t_beats, rr_clean)
    rr_uniform = cs(t_uniform) - np.mean(rr_clean)
    
    freqs, psd = signal.welch(rr_uniform, fs=4.0, nperseg=min(256, len(rr_uniform)//2))
    
    lf_mask = (freqs >= 0.04) & (freqs < 0.15)
    hf_mask = (freqs >= 0.15) & (freqs <= 0.40)
    
    metrics['LF_power'] = np.trapz(psd[lf_mask], freqs[lf_mask])
    metrics['HF_power'] = np.trapz(psd[hf_mask], freqs[hf_mask])
    metrics['LF_HF_ratio'] = metrics['LF_power'] / metrics['HF_power'] if metrics['HF_power'] > 0 else 0
    
    return metrics


def plot_session_dashboard(df: pd.DataFrame, output_path: str = 'session_dashboard.png'):
    """Generate a comprehensive session visualization."""
    fig, axes = plt.subplots(3, 1, figsize=(12, 10))
    
    # Panel 1: Heart Rate over time
    axes[0].plot(df['timestamp'], df['hr'], 'r-', linewidth=0.8)
    axes[0].set_ylabel('Heart Rate (BPM)')
    axes[0].set_title('Session Overview')
    axes[0].axhline(33, color='blue', linestyle='--', alpha=0.5, label='Resting HR')
    axes[0].legend()
    
    # Panel 2: RR intervals (tachogram)
    rr = df['rr_ms'].dropna()
    axes[1].plot(range(len(rr)), rr, 'b-', linewidth=0.5)
    axes[1].set_ylabel('RR Interval (ms)')
    axes[1].set_xlabel('Beat number')
    
    # Panel 3: Rolling RMSSD (30-beat window)
    diffs = np.diff(rr.values)
    window = 30
    rolling_rmssd = pd.Series(diffs**2).rolling(window).mean().apply(np.sqrt)
    axes[2].plot(range(len(rolling_rmssd)), rolling_rmssd, 'g-')
    axes[2].set_ylabel('RMSSD (ms)')
    axes[2].set_xlabel('Beat number')
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
```

---

## 🧮 8. Worked Examples

<details>
<summary>Example 1: Parsing a BLE Heart Rate Notification</summary>

**Problem:** A BLE notification arrives with bytes: `[0x16, 0x21, 0x1C, 0x07, 0x18, 0x07]`. Parse the heart rate and RR intervals.

**Solution:**

**Step 1:** Flags = 0x16 = 0b00010110:
- Bit 0 = 0: HR is UINT8
- Bit 4 = 1: RR intervals present

**Step 2:** HR = byte[1] = 0x21 = 33 BPM

**Step 3:** RR intervals (UINT16 little-endian):
- RR₁ = byte[2] | (byte[3] << 8) = 0x1C | (0x07 << 8) = 28 + 1792 = 1820

$$
RR_1 = 1820 \times \frac{1000}{1024} = 1777.3 \text{ ms}
$$

- RR₂ = byte[4] | (byte[5] << 8) = 0x18 | (0x07 << 8) = 24 + 1792 = 1816

$$
RR_2 = 1816 \times \frac{1000}{1024} = 1773.4 \text{ ms}
$$

**Step 4:** Verify: $60000/1777 = 33.8$ BPM — consistent with displayed HR of 33.

</details>

<details>
<summary>Example 2: Sliding Window RMSSD Update</summary>

**Problem:** Current RMSSD window (last 5 RR values): [1800, 1850, 1780, 1870, 1810] ms. Sum of squared diffs = 26800. A new RR arrives: 1860 ms. Window size = 5. Compute updated RMSSD.

**Solution:**

**Step 1:** New squared difference (entering):

$$
(1860 - 1810)^2 = 50^2 = 2500
$$

**Step 2:** Old squared difference (leaving — between positions 0 and 1):

$$
(1850 - 1800)^2 = 50^2 = 2500
$$

**Step 3:** Update sum:

$$
S_{\text{new}} = 26800 + 2500 - 2500 = 26800
$$

**Step 4:** New RMSSD:

$$
RMSSD = \sqrt{\frac{26800}{5-1}} = \sqrt{6700} = 81.9 \text{ ms}
$$

**Step 5:** New window: [1850, 1780, 1870, 1810, 1860]

Verify: diffs = [-70, 90, -60, 50], squared = [4900, 8100, 3600, 2500], sum = 19100... 

Wait — let me recount. The sum of squared diffs for the ORIGINAL window [1800, 1850, 1780, 1870, 1810]:
- diffs: [50, -70, 90, -60]
- squared: [2500, 4900, 8100, 3600]
- sum = 19100 (not 26800 as stated)

Using the corrected sum: $S = 19100 + 2500 - 2500 = 19100$

$$
RMSSD = \sqrt{19100/4} = \sqrt{4775} = 69.1 \text{ ms}
$$

</details>

<details>
<summary>Example 3: Battery Life Estimation for a Training Session</summary>

**Problem:** A 2-hour BMX training session uses: BLE HR (continuous), GPS (continuous), screen on 50% of time (bright). Estimate battery consumption on a 4000 mAh phone.

**Solution:**

**Step 1:** Power budget:

| Component | Power (mW) |
|:---|:---|
| BLE radio | 15 |
| GPS | 150 |
| Screen (50% duty, bright) | 300 × 0.5 = 150 |
| CPU (processing, 10%) | 200 × 0.1 = 20 |
| Baseline | 50 |
| **Total** | **385 mW** |

**Step 2:** Energy consumed in 2 hours:

$$
E = 385 \times 2 = 770 \text{ mWh}
$$

**Step 3:** Battery percentage:

$$
\% = \frac{770}{14800} \times 100 = 5.2\%
$$

**Conclusion:** A 2-hour training session consumes only ~5% battery. The app can confidently run all-day recording.

</details>

---

## 🔗 9. Cross-links & Further Reading

### Internal Cross-links
- [34.4 - Autonomic Nervous System Telemetry - HRV](34.4---Autonomic-Nervous-System-Telemetry---HRV) — HRV algorithms implemented here
- [34.5 - Sensor Fusion - Accelerometers & Gyroscopes](34.5---Sensor-Fusion---Accelerometers-&-Gyroscopes) — IMU data pipeline
- [34.6 - Human-Computer Interfaces - HCI Design](34.6---Human-Computer-Interfaces---HCI-Design) — UI/UX principles applied
- [34.3 - Cardiovascular Bioenergetics & VO2 Max](34.3---Cardiovascular-Bioenergetics-&-VO2-Max) — VO2 estimation from HR data
- [05 - Neuroscience & Computational Cognition](05---Neuroscience-&-Computational-Cognition) — Neural basis of biofeedback

### Additional Derivations

#### Sampling Rate Requirements for Different Metrics

Different bio-metrics require different minimum sampling rates:

| Metric | Min Sample Rate | Justification |
|:---|:---|:---|
| Heart Rate (BPM) | 1 Hz | Changes slowly (seconds) |
| RR Intervals | Beat-by-beat (~0.5–3 Hz) | One per heartbeat |
| HRV (RMSSD) | 1 per 30 beats | Sliding window |
| Accelerometer | 50–200 Hz | Human movement bandwidth |
| Gyroscope | 100–400 Hz | Fast rotations (BMX tricks) |
| GPS position | 1–10 Hz | Movement speed |

For BMX trick detection, the IMU must sample at ≥200 Hz to capture the full 360°/s rotation without aliasing:

$$
f_s \geq 2 \times f_{\max} = 2 \times \frac{\omega_{\max}}{2\pi} = 2 \times \frac{2\pi \times 2}{2\pi} = 4 \text{ Hz (for 2 rev/s)}
$$

But for accurate peak detection and waveform reconstruction, oversample by 10×: $f_s = 40$ Hz minimum, 200 Hz preferred.

#### Data Compression for Long-Term Storage

For 24-hour HRV monitoring:
- Raw RR at 33 BPM: $33 \times 60 \times 24 = 47,520$ beats/day
- At 4 bytes per RR: 190 KB/day (trivial)
- With IMU at 200 Hz × 6 axes × 2 bytes: $200 \times 6 \times 2 \times 86400 = 207$ MB/day

**Compression strategy for IMU:**
- Delta encoding (store differences): 60–70% reduction
- Downsample to 50 Hz when not in "trick mode": 75% reduction
- Trigger-based recording: only store full-rate during detected motion events

#### Error Handling State Machine

```
                    ┌─────────────────────┐
                    │                     │
    ┌───────┐      │  ┌──────────────┐   │
    │ IDLE  │──────┼─▶│  CONNECTING  │   │
    └───────┘      │  └──────┬───────┘   │
        ▲          │         │           │
        │          │         ▼           │
        │          │  ┌──────────────┐   │
        │          │  │  CONNECTED   │   │
        │          │  └──────┬───────┘   │
        │          │         │           │
        │          │         ▼           │
        │          │  ┌──────────────┐   │
        │          └──│  RECORDING   │◀──┘
        │             └──────┬───────┘
        │                    │
        │                    ▼
        │             ┌──────────────┐
        └─────────────│   SAVING     │
                      └──────────────┘
```

Each state transition has:
- **Guard condition:** What must be true to transition
- **Action:** What happens during transition
- **Error handler:** What to do if transition fails

### Authoritative Sources
- **Bluetooth SIG** — Heart Rate Profile Specification v1.0. [bluetooth.com](https://www.bluetooth.com/specifications/specs/heart-rate-profile-1-0/)
- **Flutter Documentation** — [flutter.dev](https://flutter.dev/docs)
- **flutter_blue_plus** — BLE plugin for Flutter. [pub.dev](https://pub.dev/packages/flutter_blue_plus)
- **Norman, D.A.** (2013). *The Design of Everyday Things*. Basic Books.
- **Martin, R.C.** (2017). *Clean Architecture*. Prentice Hall.
- **Fowler, M.** (2002). *Patterns of Enterprise Application Architecture*. Addison-Wesley.

---
