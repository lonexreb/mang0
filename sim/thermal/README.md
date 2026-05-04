# Thermal simulation

**Goal:** prove the vapor chamber + dual-blower design can dissipate sustained **55 W package power** with peak <95 °C, before ordering the vapor chamber (4-week lead) or CNC'ing the chassis ($400+).

This is the **single highest-risk subsystem in mang0**. The v1 anyon_e thermal solution will not survive Strix Halo under inference load. Get this wrong and the laptop thermal-throttles to uselessness.

---

## Pipeline (Antmicro, April 2026)

Mang0 follows [Antmicro's CFD pipeline](https://antmicro.com/blog/2026/04/simulating-active-cooling-using-a-cfd-based-flow), already validated on a Jetson AGX Thor in a CNC enclosure — directly analogous to our problem.

```
Fusion 360 ─────► STEP export ─────► Blender (geometry prep)
   │                                       │
   │ via Claude MCP                        │ via Claude MCP
   ▼                                       ▼
edit chassis ◄─── (iterate on CFD result) ─── snappyHexMesh (mesh)
                                              │
                                              ▼
                                       OpenFOAM
                                       (chtMultiRegionFoam:
                                        conjugate heat transfer)
                                              │
                                              ▼
                                       ParaView (post-process)
                                              │
                                              ▼
                                       Blender (color-gradient render)
```

Claude sits inside Blender + Fusion via MCP. The "iterate on CFD result" loop ("the package is hitting 102 °C — widen the side vents 2 mm and rerun") goes from days to minutes.

---

## Geometry inputs

- Strix Halo BGA package, 25 × 25 mm, top surface as heat source
- LPDDR5X PoP, ~10 W secondary heat source
- Hailo-10H M.2, ~5 W tertiary
- Vapor chamber, 80 × 60 × 1.5 mm, copper, sintered wick (model as constant-temperature spreader for first cut, conjugate for second)
- 2 × Sunon 35×6 mm blowers, model from datasheet curves
- Chassis aluminum bottom with vent pattern (parameterized)
- Honeywell PTM 7950 thermal pad, 0.25 mm thick, k = 8.5 W/m·K

---

## Thermal acceptance thresholds

Same table as in [`/thermal/README.md`](../../thermal/README.md) at the project root — sim must hit these before fab is allowed:

| Workload | Target steady-state package temp |
|---|---|
| Idle (5 W) | <45 °C |
| Single-thread peak (15 W) | <80 °C |
| All-core stress (55 W) | <95 °C |
| llama.cpp 70B sustained (55 W package + 4 W Hailo) | <95 °C combined |

Ambient: 25 °C. Margin: any sim result within 5 °C of threshold = re-design.

---

## Files (when populated)

```
sim/thermal/
├── geometry/
│   ├── chassis-v1.step          ← exported from Fusion via Claude
│   ├── vapor-chamber.step
│   └── pcb-stackup.step
├── case/
│   ├── system/
│   │   ├── controlDict
│   │   ├── snappyHexMeshDict
│   │   └── decomposeParDict
│   ├── constant/
│   │   ├── regionProperties     ← solid + fluid regions
│   │   └── polyMesh/
│   └── 0/
│       ├── T                    ← initial temperatures
│       ├── U                    ← initial velocities
│       └── p_rgh
├── scripts/
│   ├── run-cfd.sh               ← snappyHexMesh + chtMultiRegionFoam
│   ├── post-paraview.py
│   └── render-blender.py        ← Antmicro PCBooth-style
└── REPORT.md                    ← gate document, must be checked in
```

---

## Quickstart (when ready)

```bash
# Install OpenFOAM (Linux/WSL/macOS via Homebrew openfoam)
brew install openfoam              # macOS
sudo apt install openfoam2406      # Ubuntu

# Run a sim
cd sim/thermal/case
./scripts/run-cfd.sh

# Visualize
paraview case.foam &

# Render via Blender (Claude MCP can drive this)
blender --python scripts/render-blender.py
```

---

## Sources

- [Antmicro — CFD-based active cooling simulation, April 2026](https://antmicro.com/blog/2026/04/simulating-active-cooling-using-a-cfd-based-flow)
- [Antmicro — Improved thermal sim flow, Nov 2025](https://antmicro.com/blog/2025/11/improved-thermal-sim-flow)
- [OpenFOAM main site](https://www.openfoam.com/)
- [interThermalPhaseChangeFoam — vapor chamber phase change solver](https://github.com/MahdiNabil/CFD-PC)
- [PCB Cooling CFD with OpenFOAM — Tensor Engineering](https://tensorengineering.us/pcb-cooling-cfd-simulation-using-openfoam/)
