# Thermal simulation

**Goal:** prove the vapor chamber + dual-blower design can dissipate sustained **55 W package power** with peak <95 °C, before ordering the vapor chamber (4-week lead) or CNC'ing the chassis ($400+).

Single highest-risk subsystem in mang0. The v1 anyon_e thermal solution will not survive Strix Halo under inference load.

---

## Pipeline

Modelled on [Antmicro's April 2026 active-cooling flow](https://antmicro.com/blog/2026/04/simulating-active-cooling-using-a-cfd-based-flow), validated on a Jetson AGX Thor in a CNC enclosure.

```
CAD source (Fusion or chassis/blender/) ──► STEP export
                                              │
                                              ▼
                                       snappyHexMesh
                                              │
                                              ▼
                                       OpenFOAM
                                       chtMultiRegionFoam
                                       (conjugate heat transfer)
                                              │
                                              ▼
                                       ParaView (post-process)
                                              │
                                              ▼
                                       Blender (color-gradient render)
                                              │
                                              ▼
                                       iterate on geometry
```

---

## Geometry inputs

- Strix Halo BGA package, 25 × 25 mm, top surface as 55 W heat source
- LPDDR5X PoP, ~10 W secondary
- Hailo-10H M.2, ~5 W tertiary
- Vapor chamber, 80 × 60 × 1.5 mm, copper, sintered wick (model as constant-temp spreader for first cut, conjugate for second)
- 2 × Sunon 35 × 6 mm blowers, modeled from datasheet curves
- Chassis aluminum bottom with parameterized vent pattern
- Honeywell PTM 7950 thermal pad, 0.25 mm, k = 8.5 W/m·K

---

## Acceptance thresholds

| Workload | Target steady-state package temp |
|---|---|
| Idle (5 W) | <45 °C |
| Single-thread peak (15 W) | <80 °C |
| All-core stress (55 W) | <95 °C |
| Sustained inference (55 W package + 4 W Hailo) | <95 °C combined |

Ambient: 25 °C. Margin: any sim result within 5 °C of threshold = re-design.

---

## Files (when populated)

```
sim/thermal/
├── geometry/
│   ├── chassis-v1.step
│   ├── vapor-chamber.step
│   └── pcb-stackup.step
├── case/
│   ├── system/
│   │   ├── controlDict
│   │   ├── snappyHexMeshDict
│   │   └── decomposeParDict
│   ├── constant/
│   │   ├── regionProperties
│   │   └── polyMesh/
│   └── 0/
│       ├── T
│       ├── U
│       └── p_rgh
├── scripts/
│   ├── run-cfd.sh
│   ├── post-paraview.py
│   └── render-blender.py
└── REPORT.md
```

---

## Quickstart

```bash
brew install openfoam              # macOS
sudo apt install openfoam2406      # Ubuntu

cd sim/thermal/case
./scripts/run-cfd.sh

paraview case.foam &
blender --python scripts/render-blender.py
```

---

## Sources

- [Antmicro — CFD-based active cooling, April 2026](https://antmicro.com/blog/2026/04/simulating-active-cooling-using-a-cfd-based-flow)
- [Antmicro — Improved thermal sim flow, Nov 2025](https://antmicro.com/blog/2025/11/improved-thermal-sim-flow)
- [OpenFOAM main site](https://www.openfoam.com/)
- [interThermalPhaseChangeFoam — vapor chamber phase change solver](https://github.com/MahdiNabil/CFD-PC)
- [PCB Cooling CFD with OpenFOAM — Tensor Engineering](https://tensorengineering.us/pcb-cooling-cfd-simulation-using-openfoam/)
