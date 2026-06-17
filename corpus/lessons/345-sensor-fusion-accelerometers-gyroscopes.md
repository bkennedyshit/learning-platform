---
title: "34.5 — Sensor Fusion: Accelerometers & Gyroscopes"
subject: "Biomechanics & HCI"
catalog: advanced
audience_tier: higher-education
chapter: "34.5"
type: chapter-note
objectives:
  - "Understand the concepts"
  - "Apply the theory"
open_source: true
---

*Back to [Subject_Plan](Subject_Plan) | Part of [34 - Biomechanics & HCI](34---Biomechanics-&-HCI)*

# 34.5 — Sensor Fusion: Accelerometers & Gyroscopes

> *"The key challenge in robotics and biomechanics is not sensing — it is the intelligent fusion of noisy, complementary sensor data into a coherent state estimate."* — Russ Tedrake, MIT 6.832 Underactuated Robotics

An Inertial Measurement Unit (IMU) combines accelerometers and gyroscopes to track orientation and motion. Neither sensor alone is sufficient: gyroscopes drift over time, while accelerometers are corrupted by dynamic acceleration. **Sensor fusion** algorithms (complementary filters, Kalman filters) combine both to produce accurate, drift-free orientation estimates — essential for tracking BMX rider body position during aerial tricks.

---

## 🎯 Learning Objectives

1. Understand the **measurement models** of MEMS accelerometers and gyroscopes.
2. Derive the **complementary filter** for attitude estimation.
3. Implement a **Kalman filter** for IMU sensor fusion.
4. Represent 3D orientation using **quaternions** and perform quaternion integration.
5. Characterize sensor noise: **bias**, **random walk**, **Allan variance**.
6. Apply sensor fusion to **BMX trick detection** and body segment tracking.
7. Implement complete sensor fusion pipelines in Python.

---

## 🖼️ Visual Anchor — IMU Sensor Fusion Architecture

![track-13__13.5-fig1](track-13__13.5-fig1.svg)

---

## 📚 1. Definitions

### Definition 34.5.1 — MEMS Accelerometer Measurement Model

A 3-axis accelerometer measures **specific force** (acceleration minus gravity):

$$
\mathbf{a}_{\text{meas}} = R^T(\mathbf{a}_{\text{body}} - \mathbf{g}) + \mathbf{b}_a + \mathbf{n}_a
$$

where $R$ is the rotation from world to sensor frame, $\mathbf{b}_a$ is bias, and $\mathbf{n}_a \sim \mathcal{N}(0, \sigma_a^2 I)$ is white noise.

At rest: $\mathbf{a}_{\text{meas}} = -R^T\mathbf{g} + \mathbf{b}_a + \mathbf{n}_a$ (measures gravity direction).

### Definition 34.5.2 — MEMS Gyroscope Measurement Model

$$
\boldsymbol{\omega}_{\text{meas}} = \boldsymbol{\omega}_{\text{true}} + \mathbf{b}_g + \mathbf{n}_g
$$

where $\mathbf{b}_g$ is slowly-varying bias (drift) and $\mathbf{n}_g$ is angular random walk noise.

Bias drift model: $\dot{\mathbf{b}}_g = \mathbf{n}_{bg}$ (random walk).

### Definition 34.5.3 — Quaternion Representation of Orientation

A unit quaternion $\mathbf{q} = [q_w, q_x, q_y, q_z]$ with $|\mathbf{q}| = 1$ represents a rotation:

$$
\mathbf{q} = \cos\frac{\theta}{2} + \sin\frac{\theta}{2}(u_x\mathbf{i} + u_y\mathbf{j} + u_z\mathbf{k})
$$

where $\theta$ is the rotation angle and $\hat{\mathbf{u}}$ is the rotation axis.

### Definition 34.5.4 — Complementary Filter

A first-order complementary filter fuses gyroscope and accelerometer:

$$
\hat\theta(t) = \alpha[\hat\theta(t-\Delta t) + \omega\Delta t] + (1-\alpha)\theta_{\text{accel}}
$$

where $\alpha \in (0.9, 0.99)$ is the filter coefficient. The gyroscope provides high-frequency response; the accelerometer provides low-frequency (DC) correction.

### Definition 34.5.5 — Kalman Filter State Vector

For IMU fusion, the state vector typically includes:

$$
\mathbf{x} = \begin{pmatrix} \theta \\ \dot\theta \\ b_g \end{pmatrix} = \begin{pmatrix} \text{angle} \\ \text{angular rate} \\ \text{gyro bias} \end{pmatrix}
$$

### Definition 34.5.6 — Allan Variance

The **Allan variance** characterizes sensor noise as a function of averaging time $\tau$:

$$
\sigma^2(\tau) = \frac{1}{2(N-1)}\sum_{i=1}^{N-1}(\bar{y}_{i+1} - \bar{y}_i)^2
$$

On a log-log plot: slope $-1/2$ = white noise; slope $+1/2$ = random walk (bias instability).

---

## 📐 2. Axioms / Postulates

### Axiom 34.5.A1 — Complementary Noise Characteristics

Gyroscopes and accelerometers have **complementary** noise spectra:
- **Gyroscope:** Accurate at high frequencies, drifts at low frequencies (integration of bias)
- **Accelerometer:** Accurate at low frequencies (gravity reference), noisy at high frequencies (vibration, dynamic acceleration)

Optimal fusion exploits this complementarity.

### Axiom 34.5.A2 — Quaternion Unit Constraint

The orientation quaternion must remain on the unit sphere:

$$
q_w^2 + q_x^2 + q_y^2 + q_z^2 = 1
$$

After each integration step, renormalize: $\mathbf{q} \leftarrow \mathbf{q}/|\mathbf{q}|$.

### Axiom 34.5.A3 — Small Angle Approximation for Kalman Linearization

For small angular errors $\delta\theta$:

$$
\sin(\delta\theta) \approx \delta\theta, \quad \cos(\delta\theta) \approx 1
$$

This allows linearization of the rotation dynamics for the Extended Kalman Filter (EKF).

---

## 🛡️ 3. Lemmas

### Lemma 34.5.1 — Tilt Angle from Accelerometer

When stationary (or in uniform motion), the tilt angles are:

$$
\phi_{\text{roll}} = \text{atan2}(a_y, a_z)
$$

$$
\theta_{\text{pitch}} = \text{atan2}\left(-a_x, \sqrt{a_y^2 + a_z^2}\right)
$$

**Limitation:** Cannot determine yaw (heading) from accelerometer alone — requires magnetometer.

### Lemma 34.5.2 — Gyroscope Integration (Euler Method)

$$
\theta(t + \Delta t) = \theta(t) + \omega(t)\Delta t
$$

Drift accumulation after time $T$:

$$
\theta_{\text{drift}} = b_g \cdot T + \sigma_g\sqrt{T} \cdot z
$$

where $b_g$ is constant bias and $\sigma_g$ is angular random walk coefficient.

For a typical MEMS gyro ($b_g = 1°/s$, $\sigma_g = 0.01°/\sqrt{s}$): after 10 s, drift ≈ 10° — unacceptable for trick tracking.

### Lemma 34.5.3 — Quaternion Derivative

The time derivative of the orientation quaternion:

$$
\dot{\mathbf{q}} = \frac{1}{2}\mathbf{q} \otimes \boldsymbol{\omega}_q
$$

where $\boldsymbol{\omega}_q = [0, \omega_x, \omega_y, \omega_z]$ is the angular velocity as a pure quaternion, and $\otimes$ is quaternion multiplication.

**Discrete integration (first-order):**

$$
\mathbf{q}(t+\Delta t) = \mathbf{q}(t) + \frac{\Delta t}{2}\mathbf{q}(t) \otimes \boldsymbol{\omega}_q
$$

Then renormalize.

---

## 👑 4. Theorems

### Theorem 34.5.1 — Complementary Filter as High-Pass + Low-Pass

The complementary filter is equivalent to:

$$
\hat\theta = \underbrace{H_{HP}(s) \cdot \theta_{\text{gyro}}}_{\text{high-freq from gyro}} + \underbrace{H_{LP}(s) \cdot \theta_{\text{accel}}}_{\text{low-freq from accel}}
$$

where $H_{HP}(s) = \frac{\tau s}{\tau s + 1}$ and $H_{LP}(s) = \frac{1}{\tau s + 1}$ with $\tau = \alpha\Delta t/(1-\alpha)$.

Note: $H_{HP} + H_{LP} = 1$ (complementary property).

### Theorem 34.5.2 — Kalman Filter Equations (Discrete)

**Predict:**

$$
\hat{\mathbf{x}}_{k|k-1} = F\hat{\mathbf{x}}_{k-1|k-1} + Bu_k
$$

$$
P_{k|k-1} = FP_{k-1|k-1}F^T + Q
$$

**Update:**

$$
K_k = P_{k|k-1}H^T(HP_{k|k-1}H^T + R)^{-1}
$$

$$
\hat{\mathbf{x}}_{k|k} = \hat{\mathbf{x}}_{k|k-1} + K_k(z_k - H\hat{\mathbf{x}}_{k|k-1})
$$

$$
P_{k|k} = (I - K_kH)P_{k|k-1}
$$

### Theorem 34.5.3 — Optimal Complementary Filter Coefficient

The optimal $\alpha$ minimizes the variance of the fused estimate. For a gyro with bias random walk $\sigma_{bg}$ and accelerometer noise $\sigma_a$:

$$
\alpha_{\text{opt}} = 1 - \frac{\Delta t}{\tau_{\text{opt}}}, \quad \tau_{\text{opt}} = \sqrt{\frac{\sigma_a}{\sigma_{bg}}}
$$

Typical values: $\alpha = 0.96\text{–}0.98$ for consumer MEMS IMUs at 100 Hz.

### Theorem 34.5.4 — Rotation Matrix from Quaternion

The rotation matrix corresponding to quaternion $\mathbf{q} = [w, x, y, z]$:

$$
R(\mathbf{q}) = \begin{pmatrix} 1-2(y^2+z^2) & 2(xy-wz) & 2(xz+wy) \\ 2(xy+wz) & 1-2(x^2+z^2) & 2(yz-wx) \\ 2(xz-wy) & 2(yz+wx) & 1-2(x^2+y^2) \end{pmatrix}
$$

This converts a vector from body frame to world frame: $\mathbf{v}_{\text{world}} = R(\mathbf{q})\mathbf{v}_{\text{body}}$.

**Application:** To determine if the BMX rider is inverted (upside down), check the (3,3) element of $R$:
- $R_{33} > 0$: Upright
- $R_{33} < 0$: Inverted
- $R_{33} = 0$: Horizontal (90° tilt)

### Theorem 34.5.5 — Gravity Removal for Dynamic Acceleration

To isolate dynamic acceleration (actual body movement) from the accelerometer signal:

$$
\mathbf{a}_{\text{dynamic}} = \mathbf{a}_{\text{meas}} - R(\mathbf{q})^T\mathbf{g}
$$

where $R(\mathbf{q})$ is the current orientation estimate. This requires accurate orientation — hence the circular dependency between sensor fusion (needs accel) and gravity removal (needs orientation).

**Solution:** Use the fused orientation from the previous time step to remove gravity, then use the residual to detect dynamic motion (which invalidates the accelerometer for tilt estimation during that period).

---


## ✍️ 5. Physics & Math Derivations

### 5.1 Derivation — Complementary Filter (Continuous Domain)

**Step 1:** The gyroscope gives angular rate. Integrating gives angle with drift:

$$
\theta_{\text{gyro}}(t) = \int_0^t \omega(\tau)\,d\tau + b_g t
$$

**Step 2:** The accelerometer gives a noisy but drift-free angle estimate:

$$
\theta_{\text{accel}}(t) = \text{atan2}(a_y, a_z) + n_a(t)
$$

**Step 3:** We want a filter that uses gyro for fast changes and accel for DC correction. Define:

$$
\hat\theta(s) = \frac{\tau s}{\tau s + 1}\theta_{\text{gyro}}(s) + \frac{1}{\tau s + 1}\theta_{\text{accel}}(s)
$$

**Step 4:** In discrete time (bilinear transform with $\alpha = \tau/(\tau + \Delta t)$):

$$
\hat\theta_k = \alpha(\hat\theta_{k-1} + \omega_k \Delta t) + (1-\alpha)\theta_{\text{accel},k}
$$

**Step 5:** Time constant selection: $\tau = \alpha\Delta t/(1-\alpha)$. For $\alpha = 0.98$, $\Delta t = 0.01$ s:

$$
\tau = \frac{0.98 \times 0.01}{0.02} = 0.49 \text{ s}
$$

This means the filter trusts the gyro for motions faster than ~2 Hz and the accelerometer for slower changes.

---

### 5.2 Derivation — Kalman Filter for 1D Tilt Estimation

**State vector:** $\mathbf{x} = [\theta, b_g]^T$ (angle and gyro bias)

**Step 1:** State transition model (gyro integration):

$$
\begin{pmatrix}\theta_k \\ b_{g,k}\end{pmatrix} = \begin{pmatrix}1 & -\Delta t \\ 0 & 1\end{pmatrix}\begin{pmatrix}\theta_{k-1} \\ b_{g,k-1}\end{pmatrix} + \begin{pmatrix}\Delta t \\ 0\end{pmatrix}\omega_k
$$

So $F = \begin{pmatrix}1 & -\Delta t \\ 0 & 1\end{pmatrix}$, $B = \begin{pmatrix}\Delta t \\ 0\end{pmatrix}$.

**Step 2:** Process noise covariance:

$$
Q = \begin{pmatrix}\sigma_\omega^2 \Delta t^2 & 0 \\ 0 & \sigma_b^2 \Delta t\end{pmatrix}
$$

where $\sigma_\omega$ is gyro noise density and $\sigma_b$ is bias random walk.

**Step 3:** Measurement model (accelerometer gives angle):

$$
z_k = \theta_k + v_k, \quad H = \begin{pmatrix}1 & 0\end{pmatrix}, \quad R = \sigma_a^2
$$

**Step 4:** Predict:

$$
\hat{\mathbf{x}}_{k|k-1} = F\hat{\mathbf{x}}_{k-1} + B\omega_k
$$

$$
P_{k|k-1} = FP_{k-1}F^T + Q
$$

**Step 5:** Kalman gain:

$$
S = HP_{k|k-1}H^T + R = P_{11,k|k-1} + \sigma_a^2
$$

$$
K = P_{k|k-1}H^T S^{-1} = \begin{pmatrix}P_{11}/S \\ P_{21}/S\end{pmatrix}
$$

**Step 6:** Update:

$$
\hat{\mathbf{x}}_{k|k} = \hat{\mathbf{x}}_{k|k-1} + K(z_k - H\hat{\mathbf{x}}_{k|k-1})
$$

$$
P_{k|k} = (I - KH)P_{k|k-1}
$$

The Kalman filter automatically learns the gyro bias and produces an optimal angle estimate.

---

### 5.3 Derivation — Quaternion Integration for 3D Orientation

**Step 1:** Given angular velocity $\boldsymbol{\omega} = [\omega_x, \omega_y, \omega_z]$ in body frame, the quaternion derivative is:

$$
\dot{\mathbf{q}} = \frac{1}{2}\mathbf{q} \otimes [0, \omega_x, \omega_y, \omega_z]
$$

**Step 2:** Expand quaternion multiplication. If $\mathbf{q} = [w, x, y, z]$:

$$
\dot{\mathbf{q}} = \frac{1}{2}\begin{pmatrix} -x\omega_x - y\omega_y - z\omega_z \\ w\omega_x + y\omega_z - z\omega_y \\ w\omega_y + z\omega_x - x\omega_z \\ w\omega_z + x\omega_y - y\omega_x \end{pmatrix}
$$

**Step 3:** In matrix form:

$$
\dot{\mathbf{q}} = \frac{1}{2}\Omega(\boldsymbol{\omega})\mathbf{q}
$$

where:

$$
\Omega(\boldsymbol{\omega}) = \begin{pmatrix} 0 & -\omega_x & -\omega_y & -\omega_z \\ \omega_x & 0 & \omega_z & -\omega_y \\ \omega_y & -\omega_z & 0 & \omega_x \\ \omega_z & \omega_y & -\omega_x & 0 \end{pmatrix}
$$

**Step 4:** First-order integration:

$$
\mathbf{q}_{k+1} = \mathbf{q}_k + \frac{\Delta t}{2}\Omega(\boldsymbol{\omega}_k)\mathbf{q}_k = \left(I + \frac{\Delta t}{2}\Omega\right)\mathbf{q}_k
$$

**Step 5:** Renormalize: $\mathbf{q}_{k+1} \leftarrow \mathbf{q}_{k+1}/|\mathbf{q}_{k+1}|$

---

### 5.4 Derivation — Sensor Noise Characterization

**Allan Variance for Gyroscope:**

Given $N$ samples at rate $f_s$, cluster into groups of size $m$ (averaging time $\tau = m/f_s$):

$$
\sigma^2_A(\tau) = \frac{1}{2(M-1)}\sum_{k=1}^{M-1}(\bar\omega_{k+1} - \bar\omega_k)^2
$$

**Noise identification from log-log plot:**

| Slope | Noise Type | Parameter |
|:---|:---|:---|
| $-1/2$ | Angle Random Walk (ARW) | $\sigma_{ARW}$ at $\tau = 1$ s |
| $0$ | Bias Instability | Minimum of Allan deviation |
| $+1/2$ | Rate Random Walk | $\sigma_{RRW}$ |

Typical MEMS gyro (BMI160): ARW = 0.014°/√s, Bias instability = 3°/hr.

---

## 🧬 6. Biological Impact

### Why IMU Placement Matters on the Human Body

The human body is not a single rigid body — it's a kinematic chain of ~15 segments. IMU placement determines what motion is captured:

| Placement | Measures | Application |
|:---|:---|:---|
| Sacrum (lower back) | Whole-body COM acceleration | Gait analysis, jump height |
| Wrist | Hand/arm dynamics | Trick detection, gesture |
| Shank (tibia) | Leg swing kinematics | Running gait, pedaling |
| Helmet | Head orientation | Vestibular correlation, spotting |
| Bike frame | Bike lean angle, rotation | Trick classification |

### Soft Tissue Artifact

Skin-mounted IMUs experience **soft tissue artifact** (STA):
- Muscle contraction shifts the sensor 1–3 cm relative to bone
- Impact events (landing) cause 10–50 g vibration spikes lasting 5–20 ms
- Solution: low-pass filter at 15–20 Hz for human movement, but preserve high-frequency for impact detection

### Vestibular-IMU Correlation

The human vestibular system IS a biological IMU:
- **Semicircular canals** = 3-axis gyroscope (angular velocity)
- **Otolith organs** = 3-axis accelerometer (linear acceleration + gravity)
- Bandwidth: 0.1–10 Hz (similar to MEMS IMU useful range)
- The brain performs its own "sensor fusion" — combining vestibular, visual, and proprioceptive data

During a BMX backflip, the vestibular system saturates at ~300°/s. The rider must rely on visual spotting and proprioception for orientation awareness beyond this rate.

---

## 💻 7. Software Implementation

### 7.1 Complementary Filter

```python
import numpy as np

class ComplementaryFilter:
    """First-order complementary filter for 1D tilt estimation."""
    
    def __init__(self, alpha: float = 0.98, dt: float = 0.01):
        self.alpha = alpha
        self.dt = dt
        self.angle = 0.0
    
    def update(self, gyro_rate: float, accel_angle: float) -> float:
        """Fuse gyroscope rate and accelerometer angle.
        
        Args:
            gyro_rate: Angular velocity from gyroscope (rad/s)
            accel_angle: Tilt angle from accelerometer (rad)
        
        Returns:
            Fused angle estimate (rad)
        """
        self.angle = self.alpha * (self.angle + gyro_rate * self.dt) + \
                     (1 - self.alpha) * accel_angle
        return self.angle
    
    def process_batch(self, gyro: np.ndarray, accel_angles: np.ndarray) -> np.ndarray:
        """Process arrays of sensor data."""
        N = len(gyro)
        angles = np.zeros(N)
        for i in range(N):
            angles[i] = self.update(gyro[i], accel_angles[i])
        return angles
```

### 7.2 Kalman Filter for IMU Fusion

```python
import numpy as np

class KalmanIMU:
    """2-state Kalman filter for 1D angle estimation with bias tracking."""
    
    def __init__(self, dt: float = 0.01, sigma_gyro: float = 0.01,
                 sigma_bias: float = 0.003, sigma_accel: float = 0.1):
        self.dt = dt
        # State: [angle, gyro_bias]
        self.x = np.array([0.0, 0.0])
        # Covariance
        self.P = np.eye(2) * 0.1
        # Process noise
        self.Q = np.array([
            [sigma_gyro**2 * dt**2, 0],
            [0, sigma_bias**2 * dt]
        ])
        # Measurement noise
        self.R = sigma_accel**2
        # State transition
        self.F = np.array([1, -dt], [0, 1](1,--dt],-[0,-1))
        # Control input
        self.B = np.array([dt, 0])
        # Measurement matrix
        self.H = np.array([1, 0](1,-0))
    
    def predict(self, gyro_rate: float):
        """Prediction step using gyroscope measurement."""
        self.x = self.F @ self.x + self.B * gyro_rate
        self.P = self.F @ self.P @ self.F.T + self.Q
    
    def update(self, accel_angle: float):
        """Update step using accelerometer angle measurement."""
        # Innovation
        y = accel_angle - self.H @ self.x
        # Innovation covariance
        S = self.H @ self.P @ self.H.T + self.R
        # Kalman gain
        K = (self.P @ self.H.T) / S
        # State update
        self.x = self.x + K.flatten() * y
        # Covariance update
        self.P = (np.eye(2) - np.outer(K.flatten(), self.H)) @ self.P
    
    def step(self, gyro_rate: float, accel_angle: float) -> float:
        """Complete predict+update cycle. Returns estimated angle."""
        self.predict(gyro_rate)
        self.update(accel_angle)
        return self.x[0]
    
    @property
    def angle(self) -> float:
        return self.x[0]
    
    @property
    def bias_estimate(self) -> float:
        return self.x[1]
```

### 7.3 Quaternion Attitude Estimation

```python
import numpy as np

def quaternion_multiply(q1: np.ndarray, q2: np.ndarray) -> np.ndarray:
    """Hamilton product of two quaternions [w, x, y, z]."""
    w1, x1, y1, z1 = q1
    w2, x2, y2, z2 = q2
    return np.array([
        w1*w2 - x1*x2 - y1*y2 - z1*z2,
        w1*x2 + x1*w2 + y1*z2 - z1*y2,
        w1*y2 - x1*z2 + y1*w2 + z1*x2,
        w1*z2 + x1*y2 - y1*x2 + z1*w2
    ])

def integrate_quaternion(q: np.ndarray, omega: np.ndarray, dt: float) -> np.ndarray:
    """Integrate quaternion one step given angular velocity (body frame).
    
    Args:
        q: Current quaternion [w, x, y, z]
        omega: Angular velocity [wx, wy, wz] in rad/s
        dt: Time step
    
    Returns:
        Updated quaternion (normalized)
    """
    omega_q = np.array([0, omega[0], omega[1], omega[2]])
    q_dot = 0.5 * quaternion_multiply(q, omega_q)
    q_new = q + q_dot * dt
    return q_new / np.linalg.norm(q_new)  # renormalize
```

---

## 🧮 8. Worked Examples

<details>
<summary>Example 1: Complementary Filter — BMX Rider Tilt</summary>

**Problem:** A BMX rider's IMU reads: gyro = 5.0 rad/s (pitching backward), accel_angle = 0.15 rad (from gravity). Previous fused angle = 0.10 rad. $\alpha = 0.98$, $\Delta t = 0.01$ s. Compute the new fused angle.

**Solution:**

**Step 1:** Gyro prediction:

$$
\theta_{\text{gyro}} = \hat\theta_{\text{prev}} + \omega\Delta t = 0.10 + 5.0 \times 0.01 = 0.15 \text{ rad}
$$

**Step 2:** Complementary fusion:

$$
\hat\theta = \alpha \cdot \theta_{\text{gyro}} + (1-\alpha) \cdot \theta_{\text{accel}}
$$

$$
= 0.98 \times 0.15 + 0.02 \times 0.15 = 0.147 + 0.003 = 0.150 \text{ rad}
$$

**Step 3:** Convert to degrees: $0.150 \times 180/\pi = 8.6°$ backward tilt.

In this case, both sources agree (0.15 rad), so the fused estimate equals both. The filter's value becomes apparent when they disagree (dynamic motion vs. static reference).

</details>

<details>
<summary>Example 2: Gyroscope Drift Calculation</summary>

**Problem:** A MEMS gyroscope has bias = 0.5°/s and ARW = 0.02°/√s. After a 2-second aerial trick with no accelerometer correction, what is the expected angle error?

**Solution:**

**Step 1:** Bias-induced drift:

$$
\theta_{\text{bias}} = b_g \times T = 0.5°/\text{s} \times 2 \text{ s} = 1.0°
$$

**Step 2:** Random walk contribution (1σ):

$$
\theta_{\text{ARW}} = \sigma_{ARW}\sqrt{T} = 0.02 \times \sqrt{2} = 0.028°
$$

**Step 3:** Total error (dominated by bias):

$$
\theta_{\text{error}} \approx 1.0° + 0.028° \approx 1.03°
$$

**Interpretation:** After 2 seconds, the gyro-only estimate has ~1° error. For a backflip (360°), this is 0.28% error — acceptable for trick detection but not for precise landing angle prediction. The complementary filter corrects this drift when the rider is no longer in pure rotation.

</details>

<details>
<summary>Example 3: Kalman Gain Interpretation</summary>

**Problem:** A Kalman filter has $P_{11} = 0.05$ (angle variance) and $R = 0.2$ (accelerometer noise variance). Compute the Kalman gain and interpret.

**Solution:**

**Step 1:** Innovation covariance:

$$
S = P_{11} + R = 0.05 + 0.2 = 0.25
$$

**Step 2:** Kalman gain (for angle state):

$$
K_1 = \frac{P_{11}}{S} = \frac{0.05}{0.25} = 0.20
$$

**Step 3:** Interpretation:

The filter applies 20% weight to the accelerometer measurement and 80% to the gyro-predicted angle. This makes sense: the predicted state is more certain ($P_{11} = 0.05$) than the measurement ($R = 0.2$).

**Step 4:** Updated covariance:

$$
P_{11,\text{new}} = (1 - K_1)P_{11} = 0.80 \times 0.05 = 0.04
$$

The uncertainty decreased from 0.05 to 0.04 after incorporating the measurement.

</details>

<details>
<summary>Example 4: Quaternion Integration — 90° Rotation</summary>

**Problem:** Starting from identity quaternion $\mathbf{q} = [1, 0, 0, 0]$, apply constant angular velocity $\boldsymbol{\omega} = [0, 0, \pi/2]$ rad/s (yaw rotation) for $\Delta t = 0.01$ s. Compute the new quaternion after one step.

**Solution:**

**Step 1:** Form the angular velocity quaternion:

$$
\boldsymbol{\omega}_q = [0, 0, 0, \pi/2] = [0, 0, 0, 1.5708]
$$

**Step 2:** Quaternion derivative:

$$
\dot{\mathbf{q}} = \frac{1}{2}\mathbf{q} \otimes \boldsymbol{\omega}_q = \frac{1}{2}[1,0,0,0] \otimes [0,0,0,1.5708]
$$

$$
= \frac{1}{2}[0, 0, 0, 1.5708] = [0, 0, 0, 0.7854]
$$

**Step 3:** Euler integration:

$$
\mathbf{q}_{\text{new}} = [1,0,0,0] + 0.01 \times [0,0,0,0.7854] = [1, 0, 0, 0.007854]
$$

**Step 4:** Normalize:

$$
|\mathbf{q}| = \sqrt{1 + 0.007854^2} = \sqrt{1.0000617} \approx 1.0000308
$$

$$
\mathbf{q}_{\text{norm}} \approx [0.99997, 0, 0, 0.00785]
$$

This represents a tiny rotation of $2\arcsin(0.00785) \approx 0.9°$ about the z-axis — correct for $(\pi/2) \times 0.01 \times (180/\pi) = 0.9°$.

</details>

---

## 🔗 9. Cross-links & Further Reading

### Internal Cross-links
- [4.7 - Rigid Body Dynamics & Euler Angles](4.7---Rigid-Body-Dynamics-&-Euler-Angles) — Euler angles and rotation matrices
- [34.2 - Rotational Dynamics in Extreme Sports](34.2---Rotational-Dynamics-in-Extreme-Sports) — The rotations we're measuring
- [34.1 - Kinematics of Human Movement](34.1---Kinematics-of-Human-Movement) — Position/velocity from integrated IMU data
- [34.7 - Building Bio-metric Software Applications](34.7---Building-Bio-metric-Software-Applications) — Deploying sensor fusion in apps
- [1.6 - Vector Fields, Div & Curl](1.6---Vector-Fields,-Div-&-Curl) — Vector calculus for angular velocity fields

### Additional Derivations

#### Madgwick Filter (Gradient Descent Orientation)

The Madgwick filter uses gradient descent to find the orientation that aligns the measured gravity with the expected gravity:

**Step 1:** Define the objective function — the accelerometer should measure pure gravity in the earth frame:

$$
f(\mathbf{q}, \hat{\mathbf{a}}) = \mathbf{q}^* \otimes [0, 0, 0, g] \otimes \mathbf{q} - [0, a_x, a_y, a_z]
$$

**Step 2:** Compute the gradient:

$$
\nabla f = J^T f
$$

where $J$ is the Jacobian of $f$ with respect to quaternion components.

**Step 3:** Update rule (gradient descent with step size $\beta$):

$$
\mathbf{q}_{\nabla} = \frac{\nabla f}{|\nabla f|}
$$

**Step 4:** Fuse with gyroscope integration:

$$
\dot{\mathbf{q}} = \frac{1}{2}\mathbf{q} \otimes \boldsymbol{\omega}_q - \beta\mathbf{q}_{\nabla}
$$

The parameter $\beta$ controls the trade-off (like $\alpha$ in complementary filter). Typical: $\beta = 0.04\text{–}0.1$.

**Advantage over complementary filter:** Works in full 3D without gimbal lock, handles magnetic distortion gracefully.

#### Extended Kalman Filter for Full 3D Orientation

For 3D orientation, the state vector is:

$$
\mathbf{x} = [q_w, q_x, q_y, q_z, b_{gx}, b_{gy}, b_{gz}]^T \quad (7 \text{ states})
$$

The process model is non-linear (quaternion kinematics), requiring linearization:

$$
F = \frac{\partial f}{\partial \mathbf{x}}\bigg|_{\hat{\mathbf{x}}} = \begin{pmatrix} \frac{\partial \dot{\mathbf{q}}}{\partial \mathbf{q}} & \frac{\partial \dot{\mathbf{q}}}{\partial \mathbf{b}} \\ 0_{3\times4} & I_{3\times3} \end{pmatrix}
$$

The measurement model uses accelerometer (and optionally magnetometer) to correct drift:

$$
\mathbf{z} = h(\mathbf{x}) + \mathbf{v} = R(\mathbf{q})^T\mathbf{g} + \mathbf{v}
$$

This EKF provides optimal fusion but is computationally heavier than complementary or Madgwick filters.

### Authoritative Sources
- **Madgwick, S.O.H.** (2010). "An Efficient Orientation Filter for Inertial and Inertial/Magnetic Sensor Arrays." University of Bristol.
- **Tedrake, R.** — MIT 6.832 Underactuated Robotics. [Notes](http://underactuated.mit.edu/)
- **Titterton, D. & Weston, J.** (2004). *Strapdown Inertial Navigation Technology* (2nd ed.). IET.
- **Woodman, O.J.** (2007). "An Introduction to Inertial Navigation." University of Cambridge Technical Report.
- **Sabatini, A.M.** (2011). "Estimating Three-Dimensional Orientation of Human Body Parts by Inertial/Magnetic Sensing." *Sensors*, 11(2), 1489–1525.

---
