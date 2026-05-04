# Mechanical simulation

**Goal:** validate chassis stiffness, hinge stress, drop tolerance, and battery bay deformation under load — before CNC.

---

## Tools

- **Autodesk Fusion** via [Claude MCP connector](https://aps.autodesk.com/blog/bringing-fusion-claude-creative-work) — primary CAD + native FEA. Text-to-CAD edits ("widen the vapor chamber pocket by 0.5 mm") and parametric updates driven by Claude.
- **FreeCAD FEM** as open-source fallback if no Fusion subscription.
- **Blender** via Claude MCP for visualization and the [Antmicro thermal-render pipeline](https://antmicro.com/blog/2026/04/simulating-active-cooling-using-a-cfd-based-flow) which assumes Blender as host.

---

## Required studies

| Study | Acceptance threshold |
|---|---|
| Lid torsion | <0.5° twist under 2 kgf at corner |
| Bottom deflection | <0.3 mm at battery bay center under 5 kgf |
| Hinge fatigue | 30,000 cycles, no plastic deformation |
| Drop test (1 m, 6 faces + 4 corners) | No structural failure; display + battery survive |
| Vapor chamber pocket fit | ±0.05 mm tolerance check vs vapor chamber STEP |
| Thermal expansion match | Aluminum chassis vs Strix Halo BGA solder over 0–95 °C |

---

## Files (when populated)

```
sim/mechanical/
├── fusion/
│   ├── chassis.f3d              ← parametric Fusion model
│   └── README.md                ← which parameters Claude is allowed to mutate
├── studies/
│   ├── lid-torsion/
│   ├── drop-test/
│   └── hinge-fatigue/
└── REPORT.md
```

---

## Workflow with Claude

```
You: "Run the lid torsion study with 2 kgf at the rear-right corner."
Claude (via Fusion MCP):
  - Locates the existing Static Stress study
  - Updates the load magnitude and location
  - Runs the solve
  - Reports max von Mises stress + max deflection
  - Flags if either exceeds threshold
  - If failed, suggests rib geometry and proposes the parametric change
You: "Apply the suggested rib and re-run."
Claude: applies, re-runs, reports.
```

This is the loop the Connectors enable. Without it, every iteration is "export STEP, open in mesh tool, set up boundary conditions, wait, look at result, go back to CAD" — 30+ minutes per iteration. With it, ~2 minutes.
