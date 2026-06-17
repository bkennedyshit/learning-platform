---
title: "32.1 — Robotics Foundations & Kinematics"
subject: "Robotics"
catalog: advanced
audience_tier: higher-education
chapter: "32.1"
type: chapter
objectives:
  - "Understand the concepts"
  - "Apply the theory"
open_source: true
---

*Back to [Subject_Plan](Subject_Plan) | Part of [00 - 09 - Learning Index](00---09---Learning-Index)*

# 32.1 — Robotics Foundations & Kinematics

> *"Pick a frame and the world becomes simple. Forget which frame you're in and the world becomes a bug."*

---

## 🎯 Learning Objectives

1. Define a **rigid body** and the special Euclidean group $SE(3)$ as the space of poses.
2. Use **homogeneous transformation matrices** $T \in SE(3)$ to compose frames.
3. Distinguish the three rotation parameterizations (rotation matrix, Euler angles, **quaternion**) and pick correctly.
4. Read a **DH (Denavit–Hartenberg) table** and build the per-joint transform.
5. Recognize the major joint types (revolute, prismatic, spherical, floating-base) and their DOF counts.
6. Compute the workspace and DOF of a kinematic chain.
7. Define **screws** and **twists** as a velocity description in $\mathfrak{se}(3)$.

---

## 🖼️ Visual Anchor

![robo__22.1-fig1](robo__22.1-fig1.svg)

External:
- 📖 [Modern Robotics Ch. 1–3 (Lynch & Park, free)](http://hades.mech.northwestern.edu/index.php/Modern_Robotics)
- 📺 [Lynch's lecture playlist on YouTube](https://www.youtube.com/@northwesternrobotics)

---

## 📚 1. Definitions

### Definition 32.1.1 — Pose / Frame
A **pose** is a position + orientation. A **frame** $\{A\}$ is a coordinate system attached to a body. The pose of frame $\{B\}$ relative to $\{A\}$ is denoted $T^A_B$.

### Definition 32.1.2 — Homogeneous Transform
$$
T^A_B = \begin{bmatrix} R^A_B & p^A_B \\ 0\ 0\ 0 & 1 \end{bmatrix} \in SE(3)
$$
where $R \in SO(3)$ (rotation) and $p \in \mathbb{R}^3$ (position).

### Definition 32.1.3 — Composition Rule
$$
T^A_C = T^A_B \cdot T^B_C
$$
**Read right-to-left:** transform from $C$ to $B$, then from $B$ to $A$. Subscript-superscript matching is the universal sanity check.

### Definition 32.1.4 — Joint
A constraint between two links. Standard taxonomy:

| Joint | DOF | Symbol |
|---|---|---|
| Revolute | 1 (rotation) | R |
| Prismatic | 1 (translation) | P |
| Helical | 1 (coupled R+P) | H |
| Cylindrical | 2 (R+P) | C |
| Spherical | 3 (rotation) | S |
| Universal | 2 (R+R) | U |
| Planar | 3 (in plane) | – |
| Floating base | 6 | – |

### Definition 32.1.5 — DH Parameters
Each link has 4 numbers $(a_i, \alpha_i, d_i, \theta_i)$:
- $a_i$ — link length
- $\alpha_i$ — link twist
- $d_i$ — joint offset
- $\theta_i$ — joint angle

Per-link transform:
$$
A_i = R_z(\theta_i)\,T_z(d_i)\,T_x(a_i)\,R_x(\alpha_i)
$$

### Definition 32.1.6 — Screw / Twist
A **twist** $\mathcal{V} = (\omega, v) \in \mathfrak{se}(3)$ describes spatial velocity (angular + linear). For a **screw axis** $\mathcal{S}$ with angle $\theta$:
$$
T = e^{[\mathcal{S}]\theta}
$$
This is the matrix-exponential view of a transform; equivalent to DH but coordinate-free.

---

## 📐 2. Rotation Parameterizations

| Form | Storage | Pros | Cons |
|---|---|---|---|
| Rotation matrix $R \in SO(3)$ | 9 numbers | Direct compose | Redundant, drift requires re-orthogonalization |
| Euler angles (RPY, ZYZ, …) | 3 numbers | Intuitive | Gimbal lock, ordering ambiguity |
| **Quaternion** $q = (w, x, y, z)$ | 4 numbers | No singularity, slerp | Less intuitive |
| Axis-angle | 3 numbers (× angle) | Compact | Singular at $\theta = 0$ |

Default for code: **quaternions** for storage + slerp, rotation matrices for math.

---

## 🤖 3. Why "Pick a Frame" Matters

When a control loop runs at 1 kHz and a perception module runs at 30 Hz, every measurement carries an implicit "in which frame?" assumption. ROS 2's **tf2** library exists exactly to make this explicit — every transform has a parent + child + timestamp.

Common frames in a real robot:
- `world` / `map` — global, fixed.
- `odom` — drifts but is smooth.
- `base_link` — robot body.
- `imu_link`, `lidar_link`, `camera_link`, `gripper_link` — sensors / tools.
- `ee_link` — end-effector for a manipulator.

Get the **tf tree** right and your entire pipeline becomes debuggable.

---

## 🛠️ 4. Worked Example (skeleton) — A 3-Link Planar Arm

DH table:
| i | $a_i$ | $\alpha_i$ | $d_i$ | $\theta_i$ |
|---|---|---|---|---|
| 1 | $L_1$ | 0 | 0 | $\theta_1$ |
| 2 | $L_2$ | 0 | 0 | $\theta_2$ |
| 3 | $L_3$ | 0 | 0 | $\theta_3$ |

End-effector transform:
$$
T^0_3 = A_1 A_2 A_3
$$

For $L_1=L_2=L_3=1$ and $\theta_1=\theta_2=\theta_3=\pi/3$, you can compute $T^0_3$ by hand or in 4 lines of NumPy. Plot the arm; verify by drawing.

---

## 🔗 5. Cross-links & Further Reading

### Internal
- [2.4 - Linear Maps & Matrix Algebra](2.4---Linear-Maps-&-Matrix-Algebra)
- [28.1 - 3D Math Fundamentals](28.1---3D-Math-Fundamentals)
- [28.2 - Quaternions & Rotations](28.2---Quaternions-&-Rotations)
- [32.2 - Forward & Inverse Kinematics](32.2---Forward-&-Inverse-Kinematics)

### External
- [Modern Robotics Ch. 1–3 (free)](http://hades.mech.northwestern.edu/index.php/Modern_Robotics)
- [Coursera — Modern Robotics Specialization](https://www.coursera.org/specializations/modernrobotics)
- [Stanford CS223A](https://see.stanford.edu/Course/CS223A)
- [tf2 ROS 2 docs](https://docs.ros.org/en/jazzy/Concepts/About-Tf2.html)

---

## ⚠️ 6. Common Misconceptions

- **"Euler angles are always 'roll, pitch, yaw'."** Different fields use different conventions — aerospace ZYX vs robotics XYZ vs Maya ZYX. Always specify.
- **"Quaternions don't have singularities."** They have a sign ambiguity ($q$ and $-q$ give the same rotation) and need normalization to stay on $S^3$.
- **"DH parameters are unique."** Two conventions exist (Standard vs Modified DH); pick one and document it.
- **"More frames is overkill."** It's the opposite — explicit frames + tf2 prevent the most common robotics bugs.
