---
title: "34.6 — Human-Computer Interfaces: HCI Design"
subject: "Biomechanics & HCI"
catalog: advanced
audience_tier: higher-education
chapter: "34.6"
type: chapter-note
objectives:
  - "Understand the concepts"
  - "Apply the theory"
open_source: true
---

*Back to [Subject_Plan](Subject_Plan) | Part of [34 - Biomechanics & HCI](34---Biomechanics-&-HCI)*

# 34.6 — Human-Computer Interfaces: HCI Design

> *"Design is not just what it looks like and feels like. Design is how it works."* — Steve Jobs (echoing Don Norman's *The Design of Everyday Things*, 1988)

Human-Computer Interaction (HCI) is the discipline of designing interfaces that align with human cognitive, perceptual, and motor capabilities. For bio-tracking applications — heart rate monitors, HRV dashboards, trick detection displays — the interface must present complex physiological data in ways that are immediately actionable without cognitive overload.

---

## 🎯 Learning Objectives

1. Apply **Nielsen's 10 Usability Heuristics** to bio-tracking app design.
2. Derive and apply **Fitts's Law** for touch target sizing on mobile devices.
3. Understand **Hick's Law** for decision time and menu design.
4. Apply **Miller's Law** (7±2) for information chunking in dashboards.
5. Design interfaces that leverage **spatial memory** and **muscle memory**.
6. Evaluate bio-tracking UIs using **cognitive walkthrough** methodology.
7. Apply **accessibility standards** (WCAG 2.1) to health data displays.

---

## 🖼️ Visual Anchor — Bio-Tracking App Interface Anatomy

![track-13__13.6-fig1](track-13__13.6-fig1.svg)

---

## 📚 1. Definitions

### Definition 34.6.1 — Fitts's Law

The time to acquire a target is a function of the distance to and size of the target:

$$
MT = a + b \cdot \log_2\left(\frac{2D}{W}\right) = a + b \cdot ID
$$

where:
- $MT$ = movement time (ms)
- $D$ = distance from starting point to target center
- $W$ = width (size) of the target along the axis of motion
- $ID = \log_2(2D/W)$ = Index of Difficulty (bits)
- $a, b$ = empirically determined constants (intercept and slope)

(Fitts, 1954. "The Information Capacity of the Human Motor System in Controlling the Amplitude of Movement.")

### Definition 34.6.2 — Hick's Law (Hick-Hyman Law)

Decision time increases logarithmically with the number of choices:

$$
RT = a + b \cdot \log_2(n + 1)
$$

where $n$ = number of equally probable alternatives.

**Implication:** A bio-tracking dashboard with 3 main actions (Start, History, Settings) has $RT \propto \log_2(4) = 2$ bits. Adding 5 more options increases to $\log_2(9) = 3.17$ bits — 58% slower decisions.

### Definition 34.6.3 — Miller's Law (Magical Number 7±2)

Working memory can hold approximately **7 ± 2 chunks** of information simultaneously. Bio-tracking dashboards should display no more than 5–9 distinct data points without hierarchical grouping.

### Definition 34.6.4 — Nielsen's 10 Usability Heuristics

1. **Visibility of system status** — Show BLE connection state, recording status
2. **Match between system and real world** — Use "heart rate" not "cardiac frequency"
3. **User control and freedom** — Undo, back navigation, cancel recording
4. **Consistency and standards** — Follow platform conventions (iOS/Android)
5. **Error prevention** — Confirm before deleting workout data
6. **Recognition rather than recall** — Show recent workouts, not just search
7. **Flexibility and efficiency** — Shortcuts for power users, defaults for novices
8. **Aesthetic and minimalist design** — Only show relevant HRV metrics for context
9. **Help users recognize, diagnose, recover from errors** — "BLE disconnected: move closer"
10. **Help and documentation** — Explain what RMSSD means in context

### Definition 34.6.5 — Throughput (Index of Performance)

$$
TP = \frac{ID}{MT} = \frac{\log_2(2D/W)}{MT} \quad \text{(bits/s)}
$$

Human throughput for finger tapping on mobile: ~4–6 bits/s.

### Definition 34.6.6 — Cognitive Load Theory

- **Intrinsic load:** Complexity inherent to the data (HRV is complex)
- **Extraneous load:** Poor design adding unnecessary processing
- **Germane load:** Effort building mental models (desirable)

Goal: Minimize extraneous load, manage intrinsic load through progressive disclosure.

---

## 📐 2. Axioms / Postulates

### Axiom 34.6.A1 — Human Information Processing Capacity

The human visual system processes ~10 million bits/s but conscious attention handles only ~50 bits/s (Nørretranders, 1998). Interface design must bridge this 200,000× gap through pre-attentive processing (color, motion, size).

### Axiom 34.6.A2 — Proximity Principle (Gestalt)

Elements placed close together are perceived as related. In a bio-tracking dashboard:
- Group HR + HRV together (cardiac cluster)
- Group acceleration + rotation together (motion cluster)
- Separate settings from data display

### Axiom 34.6.A3 — Progressive Disclosure

Present only the information needed for the current task. Detailed HRV frequency analysis should be 1–2 taps deep, not on the main screen.

---

## 🛡️ 3. Lemmas

### Lemma 34.6.1 — Minimum Touch Target Size

From Fitts's Law and empirical studies (Apple HIG, Material Design):

$$
W_{\min} = 44 \text{ px (iOS)} = 48 \text{ dp (Android)} \approx 7\text{–}9 \text{ mm physical}
$$

For a "Start Recording" button used during exercise (reduced fine motor control due to elevated HR):

$$
W_{\text{exercise}} \geq 60 \text{ px} \approx 10 \text{ mm}
$$

### Lemma 34.6.2 — Color Contrast for Health Data

WCAG 2.1 Level AA requires:
- **Normal text:** contrast ratio ≥ 4.5:1
- **Large text (≥18px bold):** contrast ratio ≥ 3:1
- **Non-text elements (graphs, icons):** contrast ratio ≥ 3:1

For heart rate zones displayed as colored bands:
- Zone 1 (recovery): Blue on dark background — verify contrast
- Zone 5 (max): Red on dark background — verify contrast

### Lemma 34.6.3 — Optimal Information Density for Dashboards

Research (Few, 2006) shows optimal dashboard density:
- **Glanceable (while exercising):** 1–3 metrics, large font (≥24pt)
- **Review (post-workout):** 5–7 metrics with sparklines
- **Analysis (deep dive):** Full charts, tables, exportable data

---

## 👑 4. Theorems

### Theorem 34.6.1 — Fitts's Law Prediction for Bio-App Buttons

For a thumb reaching from the bottom of a phone (D = 80 mm) to a "Start" button (W = 12 mm):

$$
ID = \log_2\left(\frac{2 \times 80}{12}\right) = \log_2(34.3) = 3.74 \text{ bits}
$$

At typical mobile throughput (5 bits/s):

$$
MT = \frac{3.74}{5} = 0.75 \text{ s}
$$

Increasing button width to 20 mm:

$$
ID = \log_2\left(\frac{160}{20}\right) = \log_2(8) = 3.0 \text{ bits}
$$

$$
MT = \frac{3.0}{5} = 0.60 \text{ s}
$$

**20% faster** with a larger button — significant for repeated interactions during training.

### Theorem 34.6.2 — Optimal Menu Depth vs. Breadth

For $N$ total items organized into a hierarchy of depth $d$ with branching factor $b$ ($N = b^d$):

$$
T_{\text{total}} = d \cdot (a + b_{\text{Hick}} \cdot \log_2(b + 1))
$$

Minimizing $T_{\text{total}}$ with respect to $d$ (given $N$ fixed) yields optimal $b \approx 4\text{–}8$ items per level.

For a bio-tracking app with 30 features: $30 = 5^2$ → 2 levels of 5–6 items each is optimal.

### Theorem 34.6.3 — Spatial Consistency Reduces Cognitive Load

Users develop **spatial memory** for interface elements after 3–5 exposures (Scarr et al., 2013). Fixed-position navigation elements (bottom tab bar) are acquired 40% faster than dynamically positioned elements after the learning period.

**Implication:** The heart rate display should ALWAYS be in the same screen position. Never move it based on context.

### Theorem 34.6.4 — Feedback Timing Requirements

Human perception of causality requires feedback within specific time windows:

| Feedback Type | Max Latency | Example in Bio-App |
|:---|:---|:---|
| Instantaneous (direct manipulation) | 100 ms | Button press visual response |
| Responsive (system working) | 1000 ms | HR value update after heartbeat |
| Progress (long operation) | 10000 ms | Syncing workout to cloud |

For bio-tracking: the HR display must update within 1 second of the actual heartbeat to feel "live." Delays >2 seconds make users doubt the connection.

### Theorem 34.6.5 — Information Scent and Navigation

Users follow "information scent" — the perceived likelihood that a navigation path leads to desired information (Pirolli & Card, 1999). In bio-tracking apps:

- **Strong scent:** "Heart Rate" label → leads to HR data (obvious)
- **Weak scent:** "Analytics" → could be HR, HRV, or activity data (ambiguous)
- **No scent:** "Settings" → user won't look here for workout history

Design principle: Label navigation items with the **content** they lead to, not the **function** they perform. "My Workouts" > "History" > "Archive."

---


## ✍️ 5. Physics & Math Derivations

### 5.1 Derivation — Fitts's Law from Information Theory

**Step 1:** Fitts (1954) modeled human motor control as a communication channel. The "signal" is the target width $W$ and the "noise" is movement variability.

**Step 2:** Shannon's channel capacity:

$$
C = B \cdot \log_2\left(1 + \frac{S}{N}\right)
$$

**Step 3:** Fitts's analogy: $S/N \approx D/W$ (amplitude/precision ratio):

$$
ID = \log_2\left(\frac{2D}{W}\right) \text{ bits}
$$

The factor of 2 is empirical (Shannon formulation uses $D/W + 1$).

**Step 4:** Movement time is inversely proportional to throughput:

$$
MT = a + b \cdot ID = a + b \cdot \log_2\left(\frac{2D}{W}\right)
$$

**Step 5:** For a specific user on a specific device, calibrate $a$ and $b$ via linear regression on $(ID, MT)$ pairs.

Typical values for thumb on smartphone:
- $a \approx 50$ ms (reaction time component)
- $b \approx 150$ ms/bit (motor execution component)
- Throughput: $TP = 1/b \approx 6.7$ bits/s

---

### 5.2 Derivation — Hick's Law from Information Theory

**Step 1:** For $n$ equally probable choices, the information content of the decision is:

$$
H = \log_2(n) \text{ bits}
$$

**Step 2:** Adding 1 accounts for the "no response" option (Hyman, 1953):

$$
H = \log_2(n + 1)
$$

**Step 3:** Reaction time is linear in information:

$$
RT = a + b \cdot H = a + b \cdot \log_2(n + 1)
$$

**Step 4:** For unequal probabilities $p_i$:

$$
H = -\sum_{i=1}^{n} p_i \log_2(p_i) \text{ (Shannon entropy)}
$$

**Implication for bio-tracking:** If "Start Recording" is used 80% of the time, make it the default/prominent action. The effective information is:

$$
H = -(0.8\log_2 0.8 + 0.2\log_2 0.2) = 0.72 \text{ bits}
$$

Much less than $\log_2(2) = 1$ bit for equal probability.

---

### 5.3 Derivation — Optimal Font Size for Glanceable Displays

**Step 1:** Visual acuity: the human eye resolves ~1 arcminute (1/60°) under ideal conditions. For comfortable reading, characters should subtend ≥15 arcminutes.

**Step 2:** At viewing distance $d$, the minimum character height $h$:

$$
h = d \cdot \tan(15') = d \cdot \tan(0.25°) \approx d \times 0.00436
$$

**Step 3:** For a smartwatch at 30 cm:

$$
h_{\min} = 300 \times 0.00436 = 1.31 \text{ mm}
$$

At 326 PPI (Apple Watch): $1.31 \text{ mm} \times 326/25.4 = 16.8$ px minimum.

**Step 4:** During exercise (bouncing, peripheral vision, elevated arousal), multiply by 2–3×:

$$
h_{\text{exercise}} = 3 \times 16.8 = 50 \text{ px} \approx 24\text{pt font}
$$

This is why heart rate displays on sports watches use 24–36pt fonts.

---

### 5.4 Derivation — Color Perception Under Physiological Stress

**Step 1:** During high-intensity exercise (HR > 170 BPM):
- Peripheral vision narrows (tunnel vision) — 20–30% reduction in visual field
- Color discrimination decreases — particularly blue-green distinction
- Temporal resolution increases (faster flicker fusion) — motion detection enhanced

**Step 2:** Implications for interface design during exercise:
- Use **high-contrast** color pairs (red/green for zones, not blue/cyan)
- Place critical information **centrally** (within 10° of fixation)
- Use **motion/animation** for alerts (leverages enhanced temporal processing)
- Avoid relying on **color alone** — add shape/size coding (accessibility + physiology)

---

## 🧬 6. Biological Impact

### Motor Control and Touch Interaction

**Fitts's Law is a consequence of neuromuscular control:**

1. **Motor planning** (premotor cortex): 100–150 ms to plan the movement trajectory
2. **Ballistic phase** (primary motor cortex → corticospinal tract): Fast, open-loop movement toward target
3. **Corrective phase** (cerebellum + proprioception): Closed-loop adjustments as finger approaches target
4. **Final positioning** (visual feedback loop): 100–200 ms visual processing delay

The logarithmic relationship arises because each corrective sub-movement halves the remaining distance — a binary search in physical space.

### Cognitive Load and Working Memory

**Prefrontal cortex** (dorsolateral PFC) maintains working memory:
- Capacity: 4 ± 1 "chunks" (Cowan, 2001) — more conservative than Miller's 7±2
- Duration: 15–30 seconds without rehearsal
- **Exercise effect:** Moderate exercise (50–70% VO2max) IMPROVES working memory; high-intensity (>85%) IMPAIRS it

**Design implication:** During high-intensity training, the interface should show ≤3 metrics. During recovery/review, up to 7 is acceptable.

### Spatial Memory and the Hippocampus

- **Hippocampal place cells** encode spatial locations of interface elements
- After 3–5 uses, users develop a "cognitive map" of the app layout
- **Exercise increases hippocampal volume** (Erickson et al., 2011) — athletes may have BETTER spatial memory for interfaces
- Consistent spatial layout leverages this biological advantage

### Attention and the Reticular Activating System

During exercise:
- **Norepinephrine** levels increase → enhanced selective attention
- **Dopamine** increases → improved reward processing (gamification works better during exercise)
- **Cortisol** (if excessive) → impaired complex decision-making

---

## 💻 7. Software Implementation

### 7.1 Fitts's Law Calculator

```python
import math

def fitts_movement_time(distance: float, width: float, a: float = 50, b: float = 150) -> dict:
    """Calculate movement time using Fitts's Law (Shannon formulation).
    
    Args:
        distance: Distance to target center (px or mm)
        width: Target width (px or mm)
        a: Intercept constant (ms)
        b: Slope constant (ms/bit)
    
    Returns:
        dict with ID (bits), MT (ms), throughput (bits/s)
    """
    id_bits = math.log2(distance / width + 1)  # Shannon formulation
    mt = a + b * id_bits
    throughput = id_bits / (mt / 1000)  # bits/s
    
    return {
        'index_of_difficulty': id_bits,
        'movement_time_ms': mt,
        'throughput_bits_per_s': throughput
    }


def optimal_button_size(distance: float, target_mt: float, a: float = 50, b: float = 150) -> float:
    """Calculate minimum button width to achieve target movement time.
    
    Args:
        distance: Distance to button (px)
        target_mt: Desired movement time (ms)
        a, b: Fitts's Law constants
    
    Returns:
        Minimum button width (px)
    """
    max_id = (target_mt - a) / b
    # ID = log2(D/W + 1) => W = D / (2^ID - 1)
    min_width = distance / (2**max_id - 1)
    return max(min_width, 44)  # enforce minimum 44px
```

### 7.2 Dashboard Layout Optimizer

```python
from dataclasses import dataclass

@dataclass
class DashboardMetric:
    name: str
    priority: int        # 1=highest
    update_freq_hz: float
    glanceable: bool     # needs to be readable during exercise?

def layout_metrics(metrics: list[DashboardMetric], max_visible: int = 5) -> dict:
    """Determine which metrics to show at each detail level.
    
    Applies Miller's Law and progressive disclosure.
    """
    sorted_metrics = sorted(metrics, key=lambda m: m.priority)
    
    # Level 1: Glanceable (during exercise) — max 3
    glanceable = [m for m in sorted_metrics if m.glanceable][:3]
    
    # Level 2: Summary (post-exercise) — max 7
    summary = sorted_metrics[:min(7, max_visible)]
    
    # Level 3: Full detail — all metrics
    detail = sorted_metrics
    
    return {
        'glanceable': [m.name for m in glanceable],
        'summary': [m.name for m in summary],
        'detail': [m.name for m in detail]
    }


# Example for bio-tracking app
bio_metrics = [
    DashboardMetric("Heart Rate", 1, 1.0, True),
    DashboardMetric("HRV (RMSSD)", 2, 0.2, True),
    DashboardMetric("Duration", 3, 1.0, True),
    DashboardMetric("Calories", 4, 0.1, False),
    DashboardMetric("HR Zone", 5, 1.0, True),
    DashboardMetric("LF/HF Ratio", 6, 0.05, False),
    DashboardMetric("pNN50", 7, 0.05, False),
    DashboardMetric("SDNN", 8, 0.05, False),
]

layout = layout_metrics(bio_metrics)
# glanceable: ['Heart Rate', 'HRV (RMSSD)', 'Duration']
```

### 7.3 Accessibility Contrast Checker

```python
def relative_luminance(r: int, g: int, b: int) -> float:
    """Compute relative luminance per WCAG 2.1."""
    def linearize(c: int) -> float:
        c_srgb = c / 255.0
        return c_srgb / 12.92 if c_srgb <= 0.03928 else ((c_srgb + 0.055) / 1.055) ** 2.4
    
    return 0.2126 * linearize(r) + 0.7152 * linearize(g) + 0.0722 * linearize(b)


def contrast_ratio(fg: tuple, bg: tuple) -> float:
    """Compute WCAG contrast ratio between foreground and background colors."""
    l1 = relative_luminance(*fg)
    l2 = relative_luminance(*bg)
    lighter = max(l1, l2)
    darker = min(l1, l2)
    return (lighter + 0.05) / (darker + 0.05)


def check_bio_app_colors():
    """Verify contrast ratios for typical bio-tracking color scheme."""
    dark_bg = (18, 18, 18)       # near-black background
    hr_red = (255, 82, 82)       # heart rate color
    hrv_blue = (77, 171, 247)    # HRV color
    text_white = (240, 240, 240) # primary text
    
    results = {
        'HR red on dark': contrast_ratio(hr_red, dark_bg),
        'HRV blue on dark': contrast_ratio(hrv_blue, dark_bg),
        'White text on dark': contrast_ratio(text_white, dark_bg),
    }
    
    for name, ratio in results.items():
        status = "✓ PASS" if ratio >= 4.5 else "✗ FAIL"
        print(f"{name}: {ratio:.2f}:1 {status} (need ≥4.5:1)")
```

---

## 🧮 8. Worked Examples

<details>
<summary>Example 1: Fitts's Law — Optimizing a "Stop Recording" Button</summary>

**Problem:** During a BMX session, the rider needs to stop recording quickly. The "Stop" button is 60 px wide, positioned 200 px from the thumb's resting position. Calculate movement time. Then redesign: what width achieves MT < 400 ms?

**Solution:**

**Step 1:** Current design ($a = 50$ ms, $b = 150$ ms/bit):

$$
ID = \log_2\left(\frac{2 \times 200}{60}\right) = \log_2(6.67) = 2.74 \text{ bits}
$$

$$
MT = 50 + 150 \times 2.74 = 50 + 411 = 461 \text{ ms}
$$

**Step 2:** Target MT < 400 ms:

$$
400 = 50 + 150 \cdot ID \implies ID = \frac{350}{150} = 2.33 \text{ bits}
$$

$$
2.33 = \log_2\left(\frac{400}{W}\right) \implies \frac{400}{W} = 2^{2.33} = 5.04
$$

$$
W = \frac{400}{5.04} = 79.4 \text{ px}
$$

**Recommendation:** Increase the Stop button to ≥80 px width. Alternatively, move it closer to the thumb (reduce D to 150 px with current 60 px width: $ID = \log_2(300/60) = 2.32$, $MT = 398$ ms ✓).

</details>

<details>
<summary>Example 2: Hick's Law — Simplifying a Settings Menu</summary>

**Problem:** A bio-tracking app has 12 settings options in a flat list. Calculate decision time. Then reorganize into 2 levels and recalculate.

**Solution:**

**Step 1:** Flat list ($a = 200$ ms, $b = 150$ ms/bit):

$$
RT = 200 + 150 \cdot \log_2(12 + 1) = 200 + 150 \times 3.70 = 200 + 555 = 755 \text{ ms}
$$

**Step 2:** Reorganize into 3 categories of 4 items each:

Level 1 (choose category): $RT_1 = 200 + 150\log_2(4) = 200 + 300 = 500$ ms

Level 2 (choose item): $RT_2 = 200 + 150\log_2(5) = 200 + 348 = 548$ ms

Total: $RT_{\text{total}} = 500 + 548 = 1048$ ms

**Wait** — this is SLOWER than flat! Hick's Law shows flat is faster for small $n$.

**Step 3:** The advantage of hierarchy is **recognition** (scanning 4 items is easier than 12) and **spatial memory** (categories are memorable). For repeated use, the effective $n$ drops to 1 (user knows where to go):

$$
RT_{\text{expert}} \approx 200 + 150\log_2(2) = 350 \text{ ms per level} = 700 \text{ ms total}
$$

**Conclusion:** Hierarchy benefits expert users through spatial memory, even if naive Hick's Law suggests flat is faster for novices.

</details>

<details>
<summary>Example 3: Dashboard Design — Applying Miller's Law</summary>

**Problem:** A bio-tracking app needs to display: HR, HRV (RMSSD), HRV (SDNN), pNN50, LF power, HF power, LF/HF ratio, calories, duration, distance, pace, cadence. That's 12 metrics. Design a 3-level progressive disclosure hierarchy.

**Solution:**

**Level 1 — Glanceable (during exercise, ≤3 items):**
1. Heart Rate (BPM) — large, central
2. Duration — top corner
3. HR Zone indicator — color band

**Level 2 — Summary (swipe or tap, ≤7 items):**
1. Heart Rate
2. HRV (RMSSD) — primary recovery indicator
3. Duration
4. Calories
5. Pace/Speed
6. HR Zone distribution (mini bar chart)
7. LF/HF ratio (trend arrow)

**Level 3 — Analysis (dedicated screen):**
All 12 metrics + time-series charts + frequency spectrum + Poincaré plot

**Design rationale:**
- Level 1 respects the 3-item limit for high-cognitive-load situations (exercise)
- Level 2 respects Miller's 7±2 for post-exercise review
- Level 3 provides full data for analysis sessions (low cognitive load, seated)

</details>

<details>
<summary>Example 4: Accessibility — Color Contrast Verification</summary>

**Problem:** A bio-tracking app uses green (#4CAF50) for "recovery zone" text on a dark background (#1E1E1E). Verify WCAG 2.1 AA compliance.

**Solution:**

**Step 1:** Compute relative luminance of green (76, 175, 80):

$$
R_{\text{lin}} = (76/255 + 0.055)^{2.4}/1.055^{2.4} = 0.0730
$$

$$
G_{\text{lin}} = (175/255 + 0.055)^{2.4}/1.055^{2.4} = 0.4020
$$

$$
B_{\text{lin}} = (80/255 + 0.055)^{2.4}/1.055^{2.4} = 0.0782
$$

$$
L_{\text{fg}} = 0.2126(0.0730) + 0.7152(0.4020) + 0.0722(0.0782) = 0.0155 + 0.2875 + 0.0056 = 0.309
$$

**Step 2:** Luminance of dark background (30, 30, 30):

$$
L_{\text{bg}} = 0.2126(0.0090) + 0.7152(0.0090) + 0.0722(0.0090) = 0.009
$$

**Step 3:** Contrast ratio:

$$
CR = \frac{0.309 + 0.05}{0.009 + 0.05} = \frac{0.359}{0.059} = 6.08:1
$$

**Result:** 6.08:1 > 4.5:1 → **PASSES** WCAG AA for normal text. ✓

</details>

---

## 🔗 9. Cross-links & Further Reading

### Internal Cross-links
- [34.7 - Building Bio-metric Software Applications](34.7---Building-Bio-metric-Software-Applications) — Implementing these HCI principles in code
- [34.4 - Autonomic Nervous System Telemetry - HRV](34.4---Autonomic-Nervous-System-Telemetry---HRV) — The data being displayed
- [06 - Behavioral Psychology & Reinforcement Learning](06---Behavioral-Psychology-&-Reinforcement-Learning) — Cognitive models underlying HCI
- [05 - Neuroscience & Computational Cognition](05---Neuroscience-&-Computational-Cognition) — Neural basis of attention and memory

### Additional Derivations

#### Steering Law (Extension of Fitts's Law for Constrained Paths)

For navigating through a tunnel (e.g., scrolling through a list while maintaining finger on screen):

$$
T = a + b \cdot \frac{A}{W}
$$

where $A$ = path length and $W$ = path width. Unlike Fitts's Law (logarithmic), the Steering Law is **linear** — constrained movements are much harder.

**Application:** Scrolling through a long HRV history list on a narrow phone screen. A wider scrollable area (full-width list items) reduces navigation time linearly.

#### Power Law of Practice (Learning Curves)

User performance improves with practice following a power law:

$$
T_n = T_1 \cdot n^{-\alpha}
$$

where $T_n$ = time on the $n$-th trial, $T_1$ = first trial time, $\alpha \approx 0.3\text{–}0.5$.

**Implication:** After 10 uses of a bio-tracking app, task completion time drops to:

$$
T_{10} = T_1 \times 10^{-0.4} = T_1 \times 0.398
$$

Users become 60% faster after just 10 sessions. Design for the **expert** user (who will use the app 100+ times), not just the novice.

#### Signal Detection Theory for Alerts

Bio-tracking apps must decide when to alert the user (e.g., "abnormal HR detected"). This is a signal detection problem:

$$
d' = \frac{\mu_{\text{signal}} - \mu_{\text{noise}}}{\sigma}
$$

where $d'$ is sensitivity (discriminability). For HR anomaly detection:
- **Hit:** Correctly alerting on a true anomaly
- **False Alarm:** Alerting when HR is normal (annoying)
- **Miss:** Failing to alert on a true anomaly (dangerous)

Setting the criterion $\beta$ trades off hits vs. false alarms. For health-critical apps, bias toward **sensitivity** (accept more false alarms to avoid misses).

### Authoritative Sources
- **Norman, D.A.** (1988/2013). *The Design of Everyday Things* (Revised ed.). Basic Books.
- **Fitts, P.M.** (1954). "The Information Capacity of the Human Motor System in Controlling the Amplitude of Movement." *Journal of Experimental Psychology*, 47(6), 381–391.
- **Nielsen, J.** (1994). "10 Usability Heuristics for User Interface Design." Nielsen Norman Group.
- **Stanford CS377** — Topics in Human-Computer Interaction. [Course page](https://hci.stanford.edu/courses/)
- **Apple Human Interface Guidelines** — [developer.apple.com/design](https://developer.apple.com/design/human-interface-guidelines/)
- **Material Design 3** — [m3.material.io](https://m3.material.io/)
- **Accot, J. & Zhai, S.** (1997). "Beyond Fitts' Law: Models for Trajectory-Based HCI Tasks." *CHI '97*.

---
