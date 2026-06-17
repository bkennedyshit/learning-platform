---
date: 2026-05-26
type: subject-readme
tags: [practice, refresher, drills, source-materials, study-aids, robotics, ros2, slam, manipulation, humanoids]
title: "README — 32 - Robotics"
---

# 32 - Robotics — Subject Hub

> One-page subject hub. Lists chapters, source reading materials, **video / picture references stored outside the repo (linked by URL)**, and placeholders for generated study aids.
> Master practice guide: [[../HOW_TO_USE_PRACTICE|HOW_TO_USE_PRACTICE]].

> **Asset storage convention.**
> - **SVG diagrams** → `../_svgs/robo__<chapter>-fig<n>.svg`.
> - **Pictures, video tutorials, robot manufacturer media, papers, datasets, ROS bags** are NOT committed here. Reference them by **URL**.

---

## 🚀 Quick start

```bash
cd "C:/Obsidian Vault/Bill's Vault/05-Knowledge_Foundation/09 - Learning/32 - Robotics"
# Drill scripts (FK/IK calculators, ROS 2 examples, URDF loaders) — to be added
```

For hands-on practice without hardware: **Gazebo Sim**, **NVIDIA Isaac Sim**, **Drake**, **MuJoCo**, **PyBullet**, or browser-based **theconstruct.ai**.

---

## 📜 Chapter index

- [[32.1 - Robotics Foundations & Kinematics]]
- [[32.2 - Forward & Inverse Kinematics]]
- [[32.3 - Sensors & Perception - IMU, LiDAR, Cameras, Encoders]]
- [[32.4 - Actuators & Motor Control - Servos, BLDC, Steppers, Torque Control]]
- [[32.5 - ROS 2 & Middleware - Nodes, Topics, Services, Actions, DDS]]
- [[32.6 - SLAM & Autonomous Navigation - ORB-SLAM3, Cartographer, Nav2]]
- [[32.7 - Manipulation & Grasping - MoveIt, GraspNet, Whole-body Control]]
- [[32.8 - Humanoids, Drones & The Future of Robotics]]

---

## 🎬 Video & Picture References (external — open in browser)

### 📺 Video Channels & Courses

| Channel / Course | Track Use | Link |
|---|---|---|
| **Modern Robotics video lectures (Lynch)** | Math + kinematics + dynamics | [northwestern hosted](http://hades.mech.northwestern.edu/index.php/Modern_Robotics) + [Coursera Specialization](https://www.coursera.org/specializations/modernrobotics) |
| **MIT 6.4210 — Robotic Manipulation (Tedrake)** | Modern manipulation | [manipulation.csail.mit.edu](https://manipulation.csail.mit.edu/) |
| **MIT 6.832 — Underactuated Robotics (Tedrake)** | Walking, flight | [underactuated.csail.mit.edu](https://underactuated.csail.mit.edu/) |
| **Stanford CS223A — Khatib** | Manipulator robotics | [Stanford Online](https://see.stanford.edu/Course/CS223A) |
| **Articulated Robotics (Josh Newans)** | ROS 2 + Gazebo + real robot | [@articulatedrobotics](https://www.youtube.com/@ArticulatedRobotics) |
| **Robotics Back-End** | ROS 2 + Nav2 + MoveIt 2 | [@RoboticsBackEnd](https://www.youtube.com/@RoboticsBackEnd) |
| **The Construct** | Free + paid ROS courses | [theconstruct.ai](https://www.theconstruct.ai/) |
| **NVIDIA Robotics on YouTube** | Isaac Sim + Isaac Lab | [@NVIDIADeveloper](https://www.youtube.com/@NVIDIADeveloper) |
| **Boston Dynamics YouTube** | Atlas + Spot field footage | [@BostonDynamics](https://www.youtube.com/@BostonDynamics) |
| **Figure / 1X / Tesla / Unitree / Apptronik / Agility on YouTube** | Humanoid demos | manufacturer channels |
| **IEEE Spectrum — Automaton** | News + analysis | [spectrum.ieee.org/topic/robotics](https://spectrum.ieee.org/topic/robotics) |
| **Robot Report** | Industry news | [therobotreport.com](https://www.therobotreport.com/) |

### 🖼️ Picture / Diagram Reference Sources

| Source | Use | Link |
|---|---|---|
| **Modern Robotics figures** | DH frames, screws, twists | book site (free) |
| **ROS 2 docs diagrams** | Architecture, DDS, tf trees | [docs.ros.org](https://docs.ros.org/en/jazzy/) |
| **Nav2 docs** | Costmap, BT, planner diagrams | [docs.nav2.org](https://docs.nav2.org/) |
| **MoveIt 2 docs** | Planning pipeline | [moveit.picknik.ai](https://moveit.picknik.ai/) |
| **ORB-SLAM3 paper** | Visual-inertial pipeline | [arXiv](https://arxiv.org/abs/2007.11898) |
| **Tedrake's Robotic Manipulation textbook** | Beautiful figures, free | [manipulation.csail.mit.edu](https://manipulation.csail.mit.edu/) |
| **Manufacturer technical blogs** | Block diagrams of real robots | Boston Dynamics, NVIDIA, Figure, Unitree |

### 📚 Open-Source / Free Books & Reference

| Title | Author / Provider | Link |
|---|---|---|
| Modern Robotics | Lynch & Park | [hades.mech.northwestern.edu](http://hades.mech.northwestern.edu/index.php/Modern_Robotics) |
| Robotic Manipulation | Russ Tedrake (MIT) | [manipulation.csail.mit.edu](https://manipulation.csail.mit.edu/) |
| Underactuated Robotics | Russ Tedrake (MIT) | [underactuated.csail.mit.edu](https://underactuated.csail.mit.edu/) |
| ROS 2 Documentation (Jazzy / Humble) | Open Robotics | [docs.ros.org](https://docs.ros.org/) |
| Nav2 Documentation | Steve Macenski et al. | [docs.nav2.org](https://docs.nav2.org/) |
| MoveIt 2 Documentation | PickNik Robotics | [moveit.picknik.ai](https://moveit.picknik.ai/) |
| ORB-SLAM3 (paper + code) | UZ-SLAMLab | [github.com/UZ-SLAMLab/ORB_SLAM3](https://github.com/UZ-SLAMLab/ORB_SLAM3) |
| Cartographer ROS | Google / Open Robotics | [google-cartographer.readthedocs.io](https://google-cartographer.readthedocs.io/) |
| Drake | Toyota Research / MIT | [drake.mit.edu](https://drake.mit.edu/) |
| MuJoCo (open-source) | Google DeepMind | [mujoco.readthedocs.io](https://mujoco.readthedocs.io/) |
| NVIDIA Isaac Lab | NVIDIA | [isaac-sim.github.io/IsaacLab](https://isaac-sim.github.io/IsaacLab) |
| micro-ROS | eProsima + community | [micro.ros.org](https://micro.ros.org/) |

### 🤖 2026 Industry Snapshot (links for chapter 32.8)

| Source | Use |
|---|---|
| [TechTimes — Robotics Summit 2026 (ROS vs proprietary AI)](https://www.techtimes.com/articles/317154/20260525/humanoid-robots-reach-production-scale-robotics-summit-opens-ros-vs-proprietary-physical-ai.htm) | Industry analysis |
| [aimagicx — Humanoid Robots in the Workplace 2026](https://www.aimagicx.com/blog/humanoid-robots-workplace-tesla-optimus-atlas-2026) | Deployment numbers |
| [robozaps — Best Humanoid Robots 2026 ranking](https://blog.robozaps.com/b/best-humanoid-robots) | Comparison |
| [Tesla AI / Optimus](https://www.tesla.com/AI) | Manufacturer page |
| [IEEE Spectrum — Robotics](https://spectrum.ieee.org/topic/robotics) | Authoritative news |

---

## 🧰 Generated study aids

### 🎙️ Audio overviews
- [ ] TODO: NotebookLM audio of Subject_Plan

### 🧠 Mind maps
- [ ] TODO: NotebookLM mind-map URL

### ❓ Quizzes
- [ ] TODO: NotebookLM-generated quiz

### 📊 Reports & summaries
- [ ] TODO: 2026 humanoid landscape briefing doc

### 🃏 Flash cards
- [ ] TODO: Anki / Obsidian SR deck (DH parameters, ROS 2 vocab, Nav2 BT nodes)

### 🎬 Video overviews
- [ ] TODO: personal Loom of your robot demos

### 📋 Data tables
- [ ] TODO: comparison matrix (Atlas vs Optimus vs Figure 03 vs Digit vs Unitree G1 vs NEO vs Apollo)

---

## 🔗 Cross-links

- Syllabus & curriculum mindmap: [[Bill's Vault/05-Knowledge_Foundation/09 - Learning/32 - Robotics/Subject_Plan]]
- Visual roadmap: [[Bill's Vault/05-Knowledge_Foundation/09 - Learning/32 - Robotics/LEARNING_PATH]]
- Direct prereq: [[../30 - Electronics/Subject_Plan]]
- Math foundations: [[../07 - Math and Physics/04 - Classical Mechanics & Dynamical Systems/Subject_Plan]], [[../07 - Math and Physics/11 - Control Theory & Systems Engineering/Subject_Plan]]
- 3D side: [[../27 - 3D Modelling/Subject_Plan]] (URDFs, mesh decimation), [[../28 - VR & 3D Engineering/Subject_Plan]] (math foundations)
- AI side: [[../23 - AI & Machine Learning Systems/Subject_Plan]]
- Master Learning index: [[00 - 09 - Learning Index]]
- Master practice guide: [[../HOW_TO_USE_PRACTICE]]
