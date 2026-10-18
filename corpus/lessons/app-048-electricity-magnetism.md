---
title: "APP-04.8 — Electricity & Magnetism"
subject: "Physical Science K-8"
catalog: k12
audience_tier: 9-12
chapter: "4.8"
type: chapter
objectives:
  - "Explain static charge as a transfer of electrons, predict attraction or repulsion between charges, and classify materials as conductors or insulators"
  - "Identify the parts of a closed circuit and use Ohm's law (V = IR) to find voltage, current, or resistance with units"
  - "Compare series and parallel circuits by current, voltage, total resistance, and what happens when one bulb is removed"
  - "Describe magnetic poles and field lines, and explain how an electromagnet, an electric motor, and a generator connect electricity and magnetism"
open_source: true
---

# APP-04.8 — Electricity & Magnetism

Rub a balloon on your hair and it sticks to a wall. Plug in a charger and a phone fills with energy. Hold a compass near a wire carrying current and the needle swings. Each of these comes from **electric charge**, and the last one shows that electricity and magnetism are two sides of one connected set of ideas. This lesson covers static charge, circuits and Ohm's law, magnets, and the devices (electromagnets, motors, generators) that link electricity to magnetism.

The course plan places this lesson in grades 7-8.

## Prerequisites

- [APP-04.6 — Atoms, Elements & the Periodic Table](/app-046-atoms-elements-the-periodic-table): protons are positive, electrons are negative, and atoms are neutral when the two numbers match.
- [APP-04.2 — Energy — Forms & Transfers](/app-042-energy-forms-transfers): electrical energy and energy transformations.
- Solving $V = IR$ for any one variable, as in [13.5 - Equations & Inequalities](/135-equations-inequalities).

## Learning objectives

By the end of this lesson you should be able to:

1. Explain how objects become charged and predict whether two charged objects attract or repel.
2. Use $V = IR$ with volts, amperes, and ohms.
3. Compare series and parallel circuits.
4. Explain how electromagnets, motors, and generators work at a basic level.

## Core ideas

### Electric charge

Electric charge comes in two kinds, **positive** and **negative**. **Like charges repel and unlike charges attract.** Most objects are neutral, with equal positive and negative charge.

Rubbing two materials together can move **electrons** from one to the other. The object that gains electrons becomes negatively charged; the one that loses them becomes positively charged. For example, glass rubbed with silk becomes positive and the silk becomes negative. Charge is not created in this process, only moved: the **law of conservation of charge**.

- **Conductors** let charge move through them easily. Most metals, such as copper and aluminum, are good conductors, which is why wires are metal.
- **Insulators** resist the movement of charge. Plastic, rubber, glass, and dry wood are insulators, which is why wires are coated in plastic.

### Circuits

A **circuit** is a complete, closed path that charge can flow around. It needs:

1. an energy source (a battery or cell);
2. conducting wires;
3. a **load** that uses the energy (a bulb, a motor, a buzzer);
4. usually a **switch** to open or close the path.

If the path is broken anywhere, it is an **open circuit** and no current flows.

| Quantity | Symbol | Unit | Meaning |
|---|---|---|---|
| Current | $I$ | ampere (A) | How much charge flows past a point each second |
| Voltage | $V$ | volt (V) | The energy "push" given to each unit of charge |
| Resistance | $R$ | ohm (Ω) | How much a part opposes the current |

### Ohm's law

For many materials, the current is proportional to the voltage. The constant connecting them is the resistance:

$$V = IR$$

Rearranged: $I = \dfrac{V}{R}$ and $R = \dfrac{V}{I}$. Materials that follow this rule with a constant resistance are called **ohmic**. A light-bulb filament gets very hot, and its resistance rises with temperature, so treat bulb calculations as approximate.

### Series and parallel circuits

- **Series:** all parts on **one path**. The current is the same everywhere in the loop. Resistances add: $R_{\text{total}} = R_1 + R_2 + \dots$. The voltages across the parts add up to the battery's voltage. If one bulb is removed or burns out, the path is broken and **all** the bulbs go out.
- **Parallel:** each part on **its own branch**. Every branch gets the **same voltage** as the battery. The currents in the branches add up to the total current. The total resistance is **less** than the smallest branch resistance. If one bulb is removed, the other branches still form complete paths and stay lit.

### Magnets and magnetic fields

Every magnet has a **north pole** and a **south pole**. **Like poles repel and unlike poles attract.** The region around a magnet where its force acts is its **magnetic field**. Field lines are drawn pointing from the north pole to the south pole outside the magnet; where the lines are closer together, the field is stronger. A compass is a small magnet that lines up with the field. Because a compass's north pole points north, the magnetic pole near Earth's geographic North Pole is actually a magnetic **south** pole.

### Electricity makes magnetism, and magnetism makes electricity

- Hans Christian Oersted found that an electric current **deflects a compass needle**: a current produces a magnetic field.
- An **electromagnet** is a coil of wire carrying current. More loops of wire or more current make a stronger field, and switching off the current switches off the magnet.
- An **electric motor** uses the force that a magnetic field exerts on a current-carrying coil. The force makes the coil turn a shaft, converting electrical energy into motion.
- In 1831 Michael Faraday and Joseph Henry independently showed that a **changing** magnetic field can produce a current. A **generator** spins a coil near magnets (or magnets near a coil) to convert motion into electrical energy. A motor and a generator are built from the same parts, run in opposite directions of energy conversion.

## Worked examples

### Example 1: Ohm's law with a resistor

*Illustrative example.* A 9 V battery is connected across a 450 Ω resistor. What current flows?

1. Choose the form: $I = \dfrac{V}{R}$.
2. Substitute: $I = \dfrac{9\ \text{V}}{450\ \Omega} = 0.02\ \text{A}$.
3. Convert: 0.02 A = 20 milliamperes (mA), since 1 A = 1,000 mA.
4. Check by working backward: $V = IR = 0.02 \times 450 = 9\ \text{V}$. ✓

### Example 2: The same two resistors in series and in parallel

*Illustrative example.* Two 10 Ω resistors and a 6 V battery.

**Series:**

1. $R_{\text{total}} = 10 + 10 = 20\ \Omega$.
2. $I = 6\ \text{V} \div 20\ \Omega = 0.3\ \text{A}$, the same through both resistors.
3. Voltage across each: $V = IR = 0.3 \times 10 = 3\ \text{V}$. Check: 3 V + 3 V = 6 V. ✓

**Parallel:**

1. Each resistor gets the full 6 V.
2. Current in each branch: $6 \div 10 = 0.6\ \text{A}$.
3. Total current from the battery: 0.6 + 0.6 = 1.2 A.
4. Total resistance: $R = V \div I = 6 \div 1.2 = 5\ \Omega$, less than either 10 Ω resistor. ✓

**Compare:** the parallel arrangement draws four times as much current from the battery (1.2 A versus 0.3 A), so it drains the battery faster.

### Example 3: The balloon and the wall

1. Rubbing a balloon on hair transfers electrons to the balloon, giving it a negative charge. (The hair, having lost electrons, is left positive, which is why it may stand up toward the balloon.)
2. Bring the balloon near a neutral wall. The balloon's negative charge repels electrons in the wall's surface slightly away, leaving that surface a little positive.
3. Unlike charges attract, and the nearby positive side is closer than the pushed-away negative side, so the attraction wins.
4. The balloon sticks. No charge had to flow onto the wall: the wall stays neutral overall.

### Example 4: Troubleshooting a string of lights

*Illustrative example.* In one string of decorative lights, removing a single bulb makes the whole string go dark. In another, removing one bulb leaves the rest lit.

1. The whole string going dark means there was only one path: a **series** circuit.
2. The rest staying lit means each bulb had its own path: a **parallel** circuit.
3. Prediction for the parallel string: each remaining bulb still has the full voltage across it, so its brightness should stay about the same.

## Common misconceptions and boundary cases

- **"A battery stores charge and the current gets used up."** The current is the same going into a bulb as coming out of it. What the bulb uses is **energy**, transferred from the charges as they pass through.
- **"Current flows out of both ends of a battery to the bulb."** Current needs one complete loop: out of one terminal, through the circuit, and back to the other.
- **"Static electricity and current electricity are different things."** Both are electric charge. Static charge is built up and stays put (until it jumps, as a spark); current is charge flowing around a circuit.
- **"Magnets attract all metals."** Magnets strongly attract iron, steel, nickel, and cobalt, but not aluminum, copper, or gold. A magnet will not pick up a soda can made of aluminum.
- **"A compass points to the geographic North Pole."** It lines up with Earth's magnetic field, whose pole is near, but not exactly at, the geographic pole.
- **"Ohm's law always holds."** It describes ohmic materials. Bulbs, diodes, and many other parts do not keep a constant resistance.

## Practice

1. A rubbed plastic rod has a negative charge. Did it gain or lose electrons? What will it do to another negatively charged rod?
2. Sort into conductors or insulators: copper wire, rubber glove, aluminum foil, plastic ruler, iron nail, glass.
3. *Illustrative example:* A 3 V battery pushes 0.5 A through a motor. What is the motor's resistance (treating it as ohmic)?
4. *Illustrative example:* A 12 V source is connected to a 4 Ω heating element. What is the current?
5. *Illustrative example:* Three 2 Ω resistors are connected in series to a 12 V battery. Find the total resistance, the current, and the voltage across each resistor.
6. In a parallel circuit, one branch has a bulb and another has a buzzer. The bulb burns out. What happens to the buzzer? Why?
7. Give two ways to make an electromagnet stronger.
8. Which device converts motion into electrical energy, a motor or a generator? What does the other one do?

<details>
<summary>Answer key and self-check</summary>

1. It gained electrons. It will repel the other negatively charged rod (like charges repel).
2. Conductors: copper wire, aluminum foil, iron nail. Insulators: rubber glove, plastic ruler, glass.
3. $R = V \div I = 3 \div 0.5 = 6\ \Omega$.
4. $I = V \div R = 12 \div 4 = 3\ \text{A}$.
5. $R_{\text{total}} = 2 + 2 + 2 = 6\ \Omega$; $I = 12 \div 6 = 2\ \text{A}$; each resistor: $V = 2 \times 2 = 4\ \text{V}$ (and 4 + 4 + 4 = 12 V).
6. The buzzer keeps working. Its branch is still a complete path with the full source voltage across it.
7. Add more loops (turns) of wire, or increase the current.
8. A generator converts motion into electrical energy. A motor converts electrical energy into motion.

**Self-check:** Check every calculation by substituting back into $V = IR$. In a series circuit, the voltages across the parts must add to the source voltage; in a parallel circuit, the branch currents must add to the total current.

</details>

> **Safety note:** Build circuits only with low-voltage batteries such as 1.5 V AA cells, ideally in a battery holder. Never experiment with wall outlets or household wiring. Do not connect a wire straight from one battery terminal to the other without a load: this short circuit makes the wire and battery hot. Keep button and coin batteries and small, strong magnets away from young children; swallowed button batteries can cause serious injury, and in that case call Poison Control or emergency services immediately.

## Where this fits

This is the last lesson in the [Physical Science K-8 course](/subject/physical-science-k-8), following [APP-04.7 — Chemical Reactions](/app-047-chemical-reactions), whose chemistry is what powers a battery. It also connects back to the magnets in [APP-04.1 — Forces & Motion — Foundations](/app-041-forces-motion-foundations) and forward from the electromagnetic waves in [APP-04.3 — Waves — Light & Sound](/app-043-waves-light-sound). For a deeper, more mathematical treatment of circuits, continue with [30.1 - Electrical Fundamentals: Charge, Current, Voltage, Ohm & Kirchhoff](/301-electrical-fundamentals-charge-current-voltage-ohm-kirchhoff).

## Sources

- OpenStax, *Physics* (high school), [18.1 Electrical Charges, Conservation of Charge, and Transfer of Charge](https://openstax.org/books/physics/pages/18-1-electrical-charges-conservation-of-charge-and-transfer-of-charge) (two kinds of charge; like charges repel; glass and silk; conservation of charge; conductors and insulators; polarization)
- OpenStax, *Physics*, [19.1 Ohm's Law](https://openstax.org/books/physics/pages/19-1-ohms-law) ($V = IR$; ohmic and nonohmic materials; resistance rises at high temperature), [19.2 Series Circuits](https://openstax.org/books/physics/pages/19-2-series-circuits) (the same current everywhere; resistances add; voltages add to the battery voltage), and [19.3 Parallel Circuits](https://openstax.org/books/physics/pages/19-3-parallel-circuits) (the same voltage across each branch; equivalent resistance less than the smallest)
- OpenStax, *Physics*, [20.1 Magnetic Fields, Field Lines, and Force](https://openstax.org/books/physics/pages/20-1-magnetic-fields-field-lines-and-force) (like poles repel; field lines; Earth's magnetic south pole near the geographic North Pole; iron, cobalt, and nickel are ferromagnetic; Oersted; electromagnets and solenoids, field proportional to the number of loops and current), [20.2 Motors, Generators, and Transformers](https://openstax.org/books/physics/pages/20-2-motors-generators-and-transformers), and [20.3 Electromagnetic Induction](https://openstax.org/books/physics/pages/20-3-electromagnetic-induction) (Faraday and Henry, 1831)
- National Capital Poison Center, [Button battery ingestion](https://www.poison.org/battery)
- PhET Interactive Simulations, [Circuit Construction Kit: DC](https://phet.colorado.edu/en/simulations/circuit-construction-kit-dc) and [Magnets and Electromagnets](https://phet.colorado.edu/en/simulations/magnets-and-electromagnets)
