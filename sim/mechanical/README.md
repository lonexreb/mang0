# Mechanical simulation

**Goal:** validate chassis stiffness, hinge stress, drop tolerance, and battery-bay deformation under load — before CNC.

---

## Tools

- **Autodesk Fusion** — primary parametric CAD + native FEA (Static Stress, Modal, Nonlinear). Subscription required.
- **FreeCAD FEM** — open-source fallback if no Fusion subscription.
- **Blender** — concept layout and visualization (see [`chassis/blender/`](../../chassis/blender/)). Hands off STEP geometry to Fusion / FreeCAD for FEA, and to OpenFOAM for thermal.

---

## Required studies

| Study | Acceptance threshold |
|---|---|
| Lid torsion | <0.5° twist under 2 kgf at corner |
| Bottom deflection | <0.3 mm at battery-bay center under 5 kgf |
| Hinge fatigue | 30,000 cycles, no plastic deformation |
| Drop test (1 m, 6 faces + 4 corners) | No structural failure; display + battery survive |
| Vapor-chamber pocket fit | ±0.05 mm tolerance vs vapor-chamber STEP |
| Thermal expansion match | Aluminum chassis vs Strix Halo BGA solder over 0–95 °C |

---

## Files (when populated)

```
sim/mechanical/
├── fusion/
│   └── chassis.f3d              ← parametric Fusion model
├── studies/
│   ├── lid-torsion/
│   ├── drop-test/
│   └── hinge-fatigue/
└── REPORT.md
```
