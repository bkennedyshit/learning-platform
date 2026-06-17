---
title: "App Skeleton"
subject: "scripts"
catalog: advanced
audience_tier: higher-education
chapter: "Chapter 1"
objectives:
  - "Understand the concepts"
  - "Apply the theory"
open_source: true
---

# 13.7 App Skeleton — BLE Heart Rate Monitor

#review/biomech

---

## Flutter/Dart BLE Heart Rate Monitor — Complete App Skeleton

### Project Structure

```
bio_tracker/
├── lib/
│   ├── main.dart
│   ├── models/
│   │   ├── heart_rate_data.dart
│   │   └── session.dart
│   ├── services/
│   │   ├── ble_service.dart
│   │   └── storage_service.dart
│   ├── viewmodels/
│   │   ├── home_viewmodel.dart
│   │   └── session_viewmodel.dart
│   ├── views/
│   │   ├── home_screen.dart
│   │   ├── session_screen.dart
│   │   └── history_screen.dart
│   └── utils/
│       ├── hrv_calculator.dart
│       └── constants.dart
├── pubspec.yaml
└── test/
    └── hrv_calculator_test.dart
```

### pubspec.yaml (Dependencies)

```yaml
dependencies:
  flutter:
    sdk: flutter
  flutter_blue_plus: ^1.31.0
  provider: ^6.1.0
  sqflite: ^2.3.0
  path_provider: ^2.1.0
  fl_chart: ^0.66.0
  intl: ^0.19.0
```

---

### Core Model: heart_rate_data.dart

```dart
class HeartRateData {
  final int heartRate;
  final List<double> rrIntervalsMs;
  final DateTime timestamp;

  HeartRateData({
    required this.heartRate,
    required this.rrIntervalsMs,
    DateTime? timestamp,
  }) : timestamp = timestamp ?? DateTime.now();

  Map<String, dynamic> toMap() => {
    'hr': heartRate,
    'rr_intervals': rrIntervalsMs.join(','),
    'timestamp': timestamp.toIso8601String(),
  };

  factory HeartRateData.fromMap(Map<String, dynamic> map) => HeartRateData(
    heartRate: map['hr'],
    rrIntervalsMs: (map['rr_intervals'] as String)
        .split(',')
        .where((s) => s.isNotEmpty)
        .map(double.parse)
        .toList(),
    timestamp: DateTime.parse(map['timestamp']),
  );
}
```

---

### BLE Service: ble_service.dart

```dart
import 'dart:async';
import 'package:flutter_blue_plus/flutter_blue_plus.dart';

class BLEService {
  static const _hrServiceUuid = '0000180d-0000-1000-8000-00805f9b34fb';
  static const _hrCharUuid = '00002a37-0000-1000-8000-00805f9b34fb';

  BluetoothDevice? _connectedDevice;
  StreamSubscription? _notifySub;
  final _hrController = StreamController<HeartRateData>.broadcast();
  final _statusController = StreamController<BLEStatus>.broadcast();

  Stream<HeartRateData> get hrStream => _hrController.stream;
  Stream<BLEStatus> get statusStream => _statusController.stream;

  /// Scan for heart rate monitors
  Future<List<ScanResult>> scan({Duration timeout = const Duration(seconds: 5)}) async {
    final results = <ScanResult>[];
    final sub = FlutterBluePlus.scanResults.listen((r) => results.addAll(r));
    await FlutterBluePlus.startScan(
      withServices: [Guid(_hrServiceUuid)],
      timeout: timeout,
    );
    await sub.cancel();
    return results;
  }

  /// Connect and subscribe to HR notifications
  Future<void> connect(BluetoothDevice device) async {
    _statusController.add(BLEStatus.connecting);
    await device.connect(autoConnect: true);
    _connectedDevice = device;

    final services = await device.discoverServices();
    final hrService = services.firstWhere(
      (s) => s.uuid.toString() == _hrServiceUuid,
    );
    final hrChar = hrService.characteristics.firstWhere(
      (c) => c.uuid.toString() == _hrCharUuid,
    );

    await hrChar.setNotifyValue(true);
    _notifySub = hrChar.onValueReceived.listen(_onData);
    _statusController.add(BLEStatus.connected);
  }

  void _onData(List<int> bytes) {
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

    if ((flags & 0x08) != 0) offset += 2; // skip energy expended

    final rrList = <double>[];
    if (hasRR) {
      while (offset + 1 < bytes.length) {
        final raw = bytes[offset] | (bytes[offset + 1] << 8);
        rrList.add(raw * 1000.0 / 1024.0);
        offset += 2;
      }
    }

    _hrController.add(HeartRateData(heartRate: hr, rrIntervalsMs: rrList));
  }

  Future<void> disconnect() async {
    await _notifySub?.cancel();
    await _connectedDevice?.disconnect();
    _statusController.add(BLEStatus.disconnected);
  }

  void dispose() {
    _hrController.close();
    _statusController.close();
  }
}

enum BLEStatus { disconnected, connecting, connected, error }
```

---

### HRV Calculator: hrv_calculator.dart

```dart
import 'dart:math';

class HRVMetrics {
  final double meanRR;
  final double meanHR;
  final double rmssd;
  final double sdnn;
  final double pnn50;

  HRVMetrics({
    required this.meanRR,
    required this.meanHR,
    required this.rmssd,
    required this.sdnn,
    required this.pnn50,
  });
}

class HRVCalculator {
  final int windowSize;
  final List<double> _buffer = [];

  HRVCalculator({this.windowSize = 30});

  void addRR(double rrMs) {
    _buffer.add(rrMs);
    if (_buffer.length > windowSize) _buffer.removeAt(0);
  }

  HRVMetrics? compute() {
    if (_buffer.length < 5) return null;

    final n = _buffer.length;
    final mean = _buffer.reduce((a, b) => a + b) / n;

    // SDNN
    final variance = _buffer.map((x) => pow(x - mean, 2)).reduce((a, b) => a + b) / (n - 1);
    final sdnn = sqrt(variance);

    // RMSSD
    double sumSqDiff = 0;
    int nn50 = 0;
    for (int i = 0; i < n - 1; i++) {
      final diff = _buffer[i + 1] - _buffer[i];
      sumSqDiff += diff * diff;
      if (diff.abs() > 50) nn50++;
    }
    final rmssd = sqrt(sumSqDiff / (n - 1));
    final pnn50 = nn50 / (n - 1) * 100;

    return HRVMetrics(
      meanRR: mean,
      meanHR: 60000 / mean,
      rmssd: rmssd,
      sdnn: sdnn,
      pnn50: pnn50,
    );
  }

  void reset() => _buffer.clear();
}
```

---

### Main Screen: home_screen.dart (Simplified)

```dart
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

class HomeScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Consumer<SessionViewModel>(
      builder: (context, vm, _) => Scaffold(
        backgroundColor: Colors.black,
        body: SafeArea(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              // Large HR display (Fitts's Law: large, central)
              Text(
                '${vm.currentHR}',
                style: TextStyle(
                  fontSize: 72,
                  fontWeight: FontWeight.bold,
                  color: _hrColor(vm.currentHR),
                ),
              ),
              Text('BPM', style: TextStyle(fontSize: 18, color: Colors.white70)),
              SizedBox(height: 24),
              // HRV display
              Text(
                'RMSSD: ${vm.rmssd.toStringAsFixed(1)} ms',
                style: TextStyle(fontSize: 20, color: Colors.cyanAccent),
              ),
              SizedBox(height: 48),
              // Large start/stop button (≥80px, thumb zone)
              SizedBox(
                width: 200,
                height: 60,
                child: ElevatedButton(
                  onPressed: vm.isRecording ? vm.stop : vm.start,
                  style: ElevatedButton.styleFrom(
                    backgroundColor: vm.isRecording ? Colors.red : Colors.green,
                  ),
                  child: Text(
                    vm.isRecording ? 'STOP' : 'START',
                    style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
                  ),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  Color _hrColor(int hr) {
    if (hr < 60) return Colors.blue;       // Recovery zone
    if (hr < 120) return Colors.green;     // Aerobic
    if (hr < 160) return Colors.orange;    // Threshold
    return Colors.red;                      // Max
  }
}
```

---

## Python Post-Processing Pipeline

### Complete Analysis Script

```python
#!/usr/bin/env python3
"""Post-process exported bio-tracking session data."""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal, interpolate
from pathlib import Path
import argparse


def load_and_clean(filepath: str) -> pd.DataFrame:
    """Load CSV export and clean RR data."""
    df = pd.read_csv(filepath, parse_dates=['timestamp'])
    
    # Remove physiologically impossible values
    df = df[(df['rr_ms'] > 300) & (df['rr_ms'] < 3000)]
    
    # Ectopic beat removal (20% median filter)
    rr = df['rr_ms'].values
    for i in range(2, len(rr) - 2):
        local_med = np.median(rr[max(0,i-5):i+5])
        if abs(rr[i] - local_med) > 0.20 * local_med:
            rr[i] = local_med
    df['rr_clean'] = rr
    
    return df


def compute_hrv(rr: np.ndarray) -> dict:
    """Full HRV analysis (time + frequency domain)."""
    diffs = np.diff(rr)
    
    metrics = {
        'N_beats': len(rr),
        'mean_RR_ms': np.mean(rr),
        'mean_HR_bpm': 60000 / np.mean(rr),
        'SDNN_ms': np.std(rr, ddof=1),
        'RMSSD_ms': np.sqrt(np.mean(diffs**2)),
        'pNN50_%': np.sum(np.abs(diffs) > 50) / len(diffs) * 100,
    }
    
    # Frequency domain (resample to 4 Hz, Welch PSD)
    t = np.cumsum(rr) / 1000
    t_uniform = np.arange(0, t[-1], 0.25)
    
    if len(t_uniform) > 64:
        cs = interpolate.CubicSpline(t, rr)
        rr_resampled = cs(t_uniform) - np.mean(rr)
        
        nperseg = min(256, len(rr_resampled) // 2)
        freqs, psd = signal.welch(rr_resampled, fs=4.0, nperseg=nperseg)
        
        lf = (freqs >= 0.04) & (freqs < 0.15)
        hf = (freqs >= 0.15) & (freqs <= 0.40)
        
        metrics['LF_ms2'] = np.trapz(psd[lf], freqs[lf])
        metrics['HF_ms2'] = np.trapz(psd[hf], freqs[hf])
        metrics['LF_HF'] = metrics['LF_ms2'] / metrics['HF_ms2'] if metrics['HF_ms2'] > 0 else 0
    
    return metrics


def generate_report(df: pd.DataFrame, output_dir: str = '.'):
    """Generate visual report with 4-panel dashboard."""
    rr = df['rr_clean'].values
    metrics = compute_hrv(rr)
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle(f"Session Report — Mean HR: {metrics['mean_HR_bpm']:.0f} BPM | RMSSD: {metrics['RMSSD_ms']:.1f} ms", fontsize=14)
    
    # Panel 1: HR time series
    hr_series = 60000 / rr
    axes[0,0].plot(hr_series, 'r-', linewidth=0.5)
    axes[0,0].axhline(33, color='blue', linestyle='--', alpha=0.5)
    axes[0,0].set_title('Heart Rate')
    axes[0,0].set_ylabel('BPM')
    
    # Panel 2: RR tachogram
    axes[0,1].plot(rr, 'b-', linewidth=0.5)
    axes[0,1].set_title('RR Intervals')
    axes[0,1].set_ylabel('ms')
    
    # Panel 3: Poincaré plot
    axes[1,0].scatter(rr[:-1], rr[1:], s=5, alpha=0.5, c='green')
    axes[1,0].plot([min(rr), max(rr)], [min(rr), max(rr)], 'k--', alpha=0.3)
    axes[1,0].set_title('Poincaré Plot')
    axes[1,0].set_xlabel('RR_n (ms)')
    axes[1,0].set_ylabel('RR_n+1 (ms)')
    axes[1,0].set_aspect('equal')
    
    # Panel 4: PSD
    t = np.cumsum(rr) / 1000
    t_uniform = np.arange(0, t[-1], 0.25)
    if len(t_uniform) > 64:
        cs = interpolate.CubicSpline(t, rr)
        rr_r = cs(t_uniform) - np.mean(rr)
        freqs, psd = signal.welch(rr_r, fs=4.0, nperseg=min(256, len(rr_r)//2))
        axes[1,1].semilogy(freqs, psd, 'k-')
        axes[1,1].axvspan(0.04, 0.15, alpha=0.2, color='red', label='LF')
        axes[1,1].axvspan(0.15, 0.40, alpha=0.2, color='blue', label='HF')
        axes[1,1].set_title('Power Spectral Density')
        axes[1,1].set_xlabel('Frequency (Hz)')
        axes[1,1].set_ylabel('PSD (ms²/Hz)')
        axes[1,1].legend()
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/session_report.png', dpi=150)
    plt.close()
    
    # Print metrics
    print("\n=== HRV Metrics ===")
    for k, v in metrics.items():
        print(f"  {k}: {v:.2f}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Bio-tracking session post-processor')
    parser.add_argument('file', help='Path to exported CSV')
    parser.add_argument('--output', default='.', help='Output directory')
    args = parser.parse_args()
    
    df = load_and_clean(args.file)
    generate_report(df, args.output)
```

---

## Data Export Format Specification

### CSV Schema

```csv
timestamp,hr,rr_ms,accel_x,accel_y,accel_z,gyro_x,gyro_y,gyro_z
2026-05-23T10:00:00.000Z,33,1818.4,0.02,-0.01,9.81,0.001,0.002,-0.001
2026-05-23T10:00:01.818Z,33,1825.1,0.03,-0.02,9.80,0.001,0.001,-0.002
```

### JSON Schema (for API sync)

```json
{
  "session_id": "uuid-v4",
  "user_id": "uuid-v4",
  "start_time": "2026-05-23T10:00:00Z",
  "end_time": "2026-05-23T12:00:00Z",
  "device": {"name": "Polar H10", "mac": "AA:BB:CC:DD:EE:FF"},
  "summary": {
    "mean_hr": 33,
    "max_hr": 185,
    "rmssd": 112.4,
    "sdnn": 95.2,
    "duration_s": 7200
  },
  "data_points": [
    {"t": 0, "hr": 33, "rr": [1818.4]},
    {"t": 1818, "hr": 33, "rr": [1825.1]}
  ]
}
```

---

---

## Related Notes
- [34.7 - Building Bio-metric Software Applications](34.7---Building-Bio-metric-Software-Applications) - Shared software-architecture/flutter focus
- [13.6_hci_heuristics](13.6_hci_heuristics) - Shared review/biomech/practice focus
- [00 - ARC-219_Estimating_Architectural_Practice Index](00---ARC-219_Estimating_Architectural_Practice-Index) - Related practice topic
- [12 - Unit Price Estimating](12---Unit-Price-Estimating) - Related practice topic
- [13 - Labor, Material, and Equipment Costs](13---Labor,-Material,-and-Equipment-Costs) - Related practice topic
