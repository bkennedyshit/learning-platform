---
date: 2026-05-26
title: "Interactive SVG Templates & Visual Style Guide"
tags: [learning, mathematics, obsidian]
status: reference
type: template
---

# Interactive SVG Templates & Visual Style Guide

This document defines the visual design system and provides high-fidelity copy-paste boilerplate codes for generating physics and mathematics diagrams inside this Obsidian vault. These diagrams are designed to render perfectly in both dark and light modes by calling Obsidian's internal CSS color variables, and they include interactive hover states.

---

## 🎨 1. The Obsidian CSS Palette Matrix

When styling lines, fills, and text in your SVGs, utilize the following CSS custom properties (variables) inside the attributes:

| Variable | Use Case | Element Example |
| :--- | :--- | :--- |
| `var(--text-normal)` | Main labels, coordinate values, outline shapes | `<text>`, `<rect>` stroke |
| `var(--text-muted)` | Grid lines, axis ticks, secondary projection lines | `<line>` stroke-dasharray |
| `var(--interactive-accent)` | High-priority vectors, highlight curves, active elements | `<path>` stroke |
| `var(--text-accent)` | Accent labels, coordinate focus points | `<text>` fill |
| `var(--background-secondary)` | Semi-opaque panels, vector labels background | `<rect>` fill |
| `var(--h1-color)` | Major title highlights, primary field elements | `<circle>` fill |

---

## 📐 2. Template 1: 2D Vector Field Grid with Flow Line
Ideal for: *Fluid Dynamics, Electromagnetism, Multivariable Calculus.*

```xml
<svg viewBox="0 0 500 400" xmlns="http://www.w3.org/2000/svg" style="width: 100%; max-width: 500px; height: auto;">
  <defs>
    <!-- Reusable arrowhead marker that inherits color from elements -->
    <marker id="arrowhead" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1.5 L 8 5 L 0 8.5 z" fill="currentColor"/>
    </marker>
  </defs>
  
  <style>
    .field-grid { stroke: var(--text-muted); stroke-width: 0.5; opacity: 0.3; }
    .axis { stroke: var(--text-normal); stroke-width: 1.5; }
    .vector-arrow {
      color: var(--text-muted);
      stroke: currentColor;
      stroke-width: 1.5;
      transition: all 0.2s ease;
      cursor: pointer;
    }
    .vector-arrow:hover {
      color: var(--interactive-accent);
      stroke-width: 2.5;
      filter: drop-shadow(0 0 3px var(--interactive-accent));
    }
    .flow-line {
      stroke: var(--interactive-accent);
      stroke-width: 3;
      fill: none;
      stroke-dasharray: 800;
      stroke-dashoffset: 800;
      animation: drawFlow 4s linear infinite;
    }
    @keyframes drawFlow {
      to { stroke-dashoffset: 0; }
    }
    .label {
      font-family: Inter, system-ui, sans-serif;
      font-size: 14px;
      fill: var(--text-normal);
    }
  </style>

  <!-- Background Grid -->
  <path class="field-grid" d="M 50 0 V 400 M 100 0 V 400 M 150 0 V 400 M 200 0 V 400 M 250 0 V 400 M 300 0 V 400 M 350 0 V 400 M 400 0 V 400 M 450 0 V 400" />
  <path class="field-grid" d="M 0 50 H 500 M 0 100 H 500 M 0 150 H 500 M 0 200 H 500 M 0 250 H 500 M 0 300 H 500 M 0 350 H 500" />

  <!-- Coordinates Axes -->
  <line x1="50" y1="350" x2="450" y2="350" class="axis" marker-end="url(#arrowhead)"/>
  <line x1="50" y1="350" x2="50" y2="50" class="axis" marker-end="url(#arrowhead)"/>
  <text x="465" y="355" class="label" text-anchor="middle">x</text>
  <text x="50" y="35" class="label" text-anchor="middle">y</text>

  <!-- Grid Vector Fields -->
  <!-- Row 1 -->
  <line x1="100" y1="300" x2="120" y2="280" class="vector-arrow" marker-end="url(#arrowhead)"/>
  <line x1="150" y1="300" x2="180" y2="270" class="vector-arrow" marker-end="url(#arrowhead)"/>
  <line x1="200" y1="300" x2="240" y2="260" class="vector-arrow" marker-end="url(#arrowhead)"/>
  <!-- Row 2 -->
  <line x1="100" y1="250" x2="130" y2="220" class="vector-arrow" marker-end="url(#arrowhead)"/>
  <line x1="150" y1="250" x2="190" y2="210" class="vector-arrow" marker-end="url(#arrowhead)"/>
  <line x1="200" y1="250" x2="250" y2="200" class="vector-arrow" marker-end="url(#arrowhead)"/>
  <!-- Row 3 -->
  <line x1="100" y1="200" x2="140" y2="160" class="vector-arrow" marker-end="url(#arrowhead)"/>
  <line x1="150" y1="200" x2="200" y2="150" class="vector-arrow" marker-end="url(#arrowhead)"/>
  <line x1="200" y1="200" x2="260" y2="130" class="vector-arrow" marker-end="url(#arrowhead)"/>

  <!-- Integration Flow Path / Streamline -->
  <path d="M 80 320 Q 150 220 350 140" class="flow-line" id="flowpath"/>
  
  <!-- Flow Particle dot -->
  <circle r="6" fill="var(--interactive-accent)">
    <animateMotion dur="4s" repeatCount="indefinite" path="M 80 320 Q 150 220 350 140" />
  </circle>

  <!-- Labels -->
  <text x="360" y="125" class="label" fill="var(--interactive-accent)" font-weight="bold">Streamline Ψ(x,y)</text>
</svg>
```

---

## 🌌 3. Template 2: 3D Orthographic Spacetime / Wave Projection
Ideal for: *Special & General Relativity, Quantum Spacetime, Vector Calculus (3D).*

```xml
<svg viewBox="0 0 600 450" xmlns="http://www.w3.org/2000/svg" style="width: 100%; max-width: 600px; height: auto;">
  <defs>
    <marker id="arrowhead-3d" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1.5 L 8 5 L 0 8.5 z" fill="currentColor"/>
    </marker>
  </defs>
  
  <style>
    .axis-3d { stroke: var(--text-normal); stroke-width: 1.5; fill: none; }
    .grid-plane { stroke: var(--text-muted); stroke-width: 0.5; opacity: 0.4; fill: none; }
    .envelope { stroke: var(--interactive-accent); stroke-width: 2.5; fill: none; }
    .projection-dashes { stroke: var(--text-muted); stroke-dasharray: 4,4; stroke-width: 1; fill: none; }
    .math-text { font-family: Inter, system-ui, sans-serif; font-size: 14px; fill: var(--text-normal); }
    .wave-fill { fill: var(--interactive-accent); opacity: 0.1; }
    .node-dot { fill: var(--text-accent); stroke: var(--text-normal); stroke-width: 1; }
  </style>

  <!-- 3D Grid Floor (Perspective projection) -->
  <!-- Constant Y lines -->
  <line x1="100" y1="350" x2="350" y2="200" class="grid-plane"/>
  <line x1="150" y1="380" x2="400" y2="230" class="grid-plane"/>
  <line x1="200" y1="410" x2="450" y2="260" class="grid-plane"/>
  
  <!-- Constant X lines -->
  <line x1="100" y1="350" x2="200" y2="410" class="grid-plane"/>
  <line x1="183" y1="300" x2="283" y2="360" class="grid-plane"/>
  <line x1="266" y1="250" x2="366" y2="310" class="grid-plane"/>
  <line x1="350" y1="200" x2="450" y2="260" class="grid-plane"/>

  <!-- 3D Axes -->
  <!-- Z-Axis (Vertical) -->
  <line x1="100" y1="350" x2="100" y2="50" class="axis-3d" marker-end="url(#arrowhead-3d)"/>
  <text x="100" y="35" class="math-text" text-anchor="middle">z (Amplitude Ψ)</text>

  <!-- X-Axis (Relatively Horizontal) -->
  <line x1="100" y1="350" x2="520" y2="350" class="axis-3d" marker-end="url(#arrowhead-3d)"/>
  <text x="535" y="355" class="math-text">x (Position)</text>

  <!-- Y-Axis (Depth Plane) -->
  <line x1="100" y1="350" x2="350" y2="200" class="axis-3d" marker-end="url(#arrowhead-3d)"/>
  <text x="360" y="190" class="math-text">y (Spacetime Grid)</text>

  <!-- Quantum Wave Envelope (Sine Modulation along X) -->
  <!-- Shaded probability area -->
  <path d="M 100 350 
           Q 150 200 200 350 
           T 300 350 
           T 400 350 
           T 500 350" class="wave-fill"/>
  
  <!-- Wave Stroke -->
  <path d="M 100 350 
           Q 150 200 200 350 
           T 300 350 
           T 400 350 
           T 500 350" class="envelope"/>

  <!-- Vertical projections demonstrating superposition/integration -->
  <line x1="150" y1="275" x2="150" y2="350" class="projection-dashes"/>
  <line x1="250" y1="425" x2="250" y2="350" class="projection-dashes"/>
  <line x1="350" y1="275" x2="350" y2="350" class="projection-dashes"/>
  <line x1="450" y1="425" x2="450" y2="350" class="projection-dashes"/>

  <!-- Probability Density Nodes -->
  <circle cx="150" cy="275" r="4" class="node-dot"/>
  <circle cx="350" cy="275" r="4" class="node-dot"/>

  <!-- Formulas Embedded inside diagrams -->
  <rect x="250" y="60" width="240" height="60" rx="6" fill="var(--background-secondary)" stroke="var(--text-muted)" stroke-width="1"/>
  <text x="370" y="95" class="math-text" fill="var(--interactive-accent)" font-weight="bold" font-family="serif" font-size="16" text-anchor="middle">iℏ ∂/∂t |Ψ⟩ = Ĥ |Ψ⟩</text>
</svg>
```

---

## ⚛️ 4. Template 3: Particle/Feynman Diagram
Ideal for: *Quantum Mechanics, Particle Interactions, Standard Model.*

```xml
<svg viewBox="0 0 500 350" xmlns="http://www.w3.org/2000/svg" style="width: 100%; max-width: 500px; height: auto;">
  <defs>
    <marker id="feynman-arrow" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1.5 L 8 5 L 0 8.5 z" fill="currentColor"/>
    </marker>
  </defs>

  <style>
    .fermion { stroke: var(--text-normal); stroke-width: 2.5; fill: none; }
    .photon { stroke: var(--interactive-accent); stroke-width: 2.5; fill: none; stroke-linecap: round; }
    .vertex { fill: var(--text-accent); stroke: var(--text-normal); stroke-width: 1.5; }
    .axis-label { font-family: Inter, system-ui, sans-serif; font-size: 14px; fill: var(--text-muted); }
    .particle-name { font-family: Inter, system-ui, sans-serif; font-size: 15px; fill: var(--text-normal); font-weight: bold; }
  </style>

  <!-- Left: Space/Time Indicator Axes -->
  <line x1="40" y1="310" x2="100" y2="310" stroke="var(--text-muted)" stroke-width="1.5" marker-end="url(#feynman-arrow)"/>
  <line x1="40" y1="310" x2="40" y2="250" stroke="var(--text-muted)" stroke-width="1.5" marker-end="url(#feynman-arrow)"/>
  <text x="110" y="315" class="axis-label">Space (x)</text>
  <text x="40" y="240" class="axis-label" text-anchor="middle">Time (t)</text>

  <!-- Electron / Positron Annihilation (In-states) -->
  <!-- Electron (e-) -->
  <line x1="100" y1="280" x2="200" y2="200" class="fermion" marker-end="url(#feynman-arrow)"/>
  <text x="80" y="290" class="particle-name">e⁻</text>
  
  <!-- Positron (e+) - Arrow backward in time -->
  <line x1="200" y1="200" x2="100" y2="120" class="fermion" marker-end="url(#feynman-arrow)"/>
  <text x="80" y="125" class="particle-name">e⁺</text>

  <!-- Virtual Photon Propagator (Wavy Line) -->
  <path d="M 200 200 
           C 220 200, 220 190, 240 190
           C 260 190, 260 200, 280 200
           C 300 200, 300 190, 320 190" class="photon"/>
  <text x="260" y="170" class="particle-name" fill="var(--interactive-accent)">γ (Photon)</text>

  <!-- Muon Out-states -->
  <!-- Muon (μ-) -->
  <line x1="320" y1="190" x2="420" y2="280" class="fermion" marker-end="url(#feynman-arrow)"/>
  <text x="435" y="290" class="particle-name">μ⁻</text>

  <!-- Anti-muon (μ+) - Arrow backward in time -->
  <line x1="420" y1="100" x2="320" y2="190" class="fermion" marker-end="url(#feynman-arrow)"/>
  <text x="435" y="105" class="particle-name">μ⁺</text>

  <!-- Interaction Vertices -->
  <circle cx="200" cy="200" r="5" class="vertex"/>
  <circle cx="320" cy="190" r="5" class="vertex"/>
</svg>
```

---

## 🌡️ 5. Template 4: Thermodynamic Cycle (P-V Carnot Cycle)
Ideal for: *Thermodynamics, Classical & Statistical Mechanics.*

```xml
<svg viewBox="0 0 500 400" xmlns="http://www.w3.org/2000/svg" style="width: 100%; max-width: 500px; height: auto;">
  <defs>
    <marker id="thermo-arrow" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1.5 L 8 5 L 0 8.5 z" fill="currentColor"/>
    </marker>
  </defs>

  <style>
    .pv-axis { stroke: var(--text-normal); stroke-width: 2; fill: none; }
    .isotherm { stroke: #ff6b6b; stroke-width: 3; fill: none; }
    .adiabat { stroke: #4dabf7; stroke-width: 3; fill: none; }
    .work-fill { fill: var(--interactive-accent); opacity: 0.15; }
    .state-point { fill: var(--text-accent); stroke: var(--text-normal); stroke-width: 1.5; cursor: pointer; transition: all 0.2s; }
    .state-point:hover { fill: var(--interactive-accent); r: 7; }
    .label-style { font-family: Inter, system-ui, sans-serif; font-size: 14px; fill: var(--text-normal); }
    .title-style { font-family: Inter, system-ui, sans-serif; font-size: 16px; fill: var(--interactive-accent); font-weight: bold; }
  </style>

  <!-- PV Axis -->
  <line x1="60" y1="340" x2="450" y2="340" class="pv-axis" marker-end="url(#thermo-arrow)"/>
  <line x1="60" y1="340" x2="60" y2="40" class="pv-axis" marker-end="url(#thermo-arrow)"/>
  <text x="465" y="345" class="label-style" text-anchor="middle">V (Volume)</text>
  <text x="60" y="25" class="label-style" text-anchor="middle">P (Pressure)</text>

  <!-- Shaded Area for Carnot Work W_net -->
  <path d="M 120 120 
           Q 190 150 260 170 
           Q 220 250 180 300 
           Q 110 250 80 200 
           Z" class="work-fill"/>

  <!-- Carnot Cycle Curves -->
  <!-- Isothermal Expansion 1 -> 2 (Hot Reservoir Th) -->
  <path d="M 120 120 Q 190 150 260 170" class="isotherm" marker-end="url(#thermo-arrow)"/>
  <text x="180" y="130" class="label-style" fill="#ff6b6b">Isotherm (T_h)</text>

  <!-- Adiabatic Expansion 2 -> 3 (Expansion) -->
  <path d="M 260 170 Q 220 250 180 300" class="adiabat" marker-end="url(#thermo-arrow)"/>

  <!-- Isothermal Compression 3 -> 4 (Cold Reservoir Tc) -->
  <path d="M 180 300 Q 110 250 80 200" class="isotherm"/>
  <text x="110" y="280" class="label-style" fill="#4dabf7">Isotherm (T_c)</text>

  <!-- Adiabatic Compression 4 -> 1 (Compression) -->
  <path d="M 80 200 Q 100 160 120 120" class="adiabat"/>

  <!-- State Points -->
  <circle cx="120" cy="120" r="5" class="state-point"/>
  <text x="120" y="105" class="label-style" font-weight="bold">1</text>

  <circle cx="260" cy="170" r="5" class="state-point"/>
  <text x="275" y="175" class="label-style" font-weight="bold">2</text>

  <circle cx="180" cy="300" r="5" class="state-point"/>
  <text x="190" y="315" class="label-style" font-weight="bold">3</text>

  <circle cx="80" cy="200" r="5" class="state-point"/>
  <text x="65" y="205" class="label-style" font-weight="bold">4</text>

  <!-- Annotations -->
  <text x="160" y="210" class="title-style">W_net</text>
  <text x="320" y="80" class="label-style" fill="var(--text-muted)">Carnot Efficiency:</text>
  <text x="320" y="105" class="label-style" font-weight="bold">η = 1 - T_c/T_h</text>
</svg>
```

---

## Related Notes
- [[AGENT_MANUAL]] - Shared mathematics/learning focus
- [[SVG Design for learning]] - Shared learning/obsidian focus
- [[Externalizing memory into a layered system-Aug3125-005]] - Shared learning/obsidian focus
- [[VAULT_UPDATED]] - Shared learning/obsidian focus
- [[07 - Math and Physics Index]] - Shared mathematics/learning focus
