# Simulation

**Simulate the laptop before you fab it.** mang0 is ~$5.6K of parts with multi-week chassis and vapor-chamber lead times. One thermal mistake costs a chassis re-CNC + a vapor-chamber respin (~$500 + 4 weeks). One DDR layout error is a $1,500 motherboard scrap.

This directory holds the simulation models, scripts, and validation thresholds that must pass **before** any subsystem goes to fab. Scope is strictly the laptop's physical/electrical behavior — nothing else.

---

## Five domains

| Domain | Tool | What gets validated | Gates |
|---|---|---|---|
| [thermal/](./thermal/) | OpenFOAM (`chtMultiRegionFoam`) + ParaView + Blender | Vapor chamber + dual blower can dissipate sustained 55 W; package <95 °C | chassis CNC, vapor-chamber order |
| [mechanical/](./mechanical/) | Autodesk Fusion or FreeCAD FEM | Chassis stiffness, hinge fatigue, drop test, vapor-chamber pocket fit | chassis CNC |
| [electrical/](./electrical/) | KiCad + ngspice | Power-tree sequencing per AMD PDG, rail regulation under load step | motherboard PCB tape-out |
| [signal-integrity/](./signal-integrity/) | OpenEMS / Sonnet Lite + KiCad length tuner | USB4 / PCIe 4.0 / LPDDR5X eye openings + length-match | motherboard PCB tape-out |
| [firmware/](./firmware/) | QEMU (coreboot), Wokwi (ESP32-S3) | Boot flow, EC state machine, fan PID, OpenTitan reset/recover | first-silicon flash |

The thermal pipeline is modelled on [Antmicro's April 2026 active-cooling flow](https://antmicro.com/blog/2026/04/simulating-active-cooling-using-a-cfd-based-flow), already validated on a Jetson AGX Thor in a CNC enclosure — directly analogous to mang0's Strix Halo + vapor chamber.

---

## Gate review

Before any subsystem progresses to fab, the relevant `sim/<domain>/REPORT.md` must exist on `main` and show **PASS** for every threshold. CI ([`ci/sim-gate.yml`](../ci/sim-gate.yml)) enforces presence on PRs; humans enforce content during review.

| Subsystem PR touches | Required REPORT.md |
|---|---|
| `motherboard/` | `sim/electrical/` + `sim/signal-integrity/` |
| `power/` | `sim/electrical/` |
| `thermal/` | `sim/thermal/` |
| `chassis/` | `sim/thermal/` + `sim/mechanical/` |
| `ec/` | `sim/firmware/` |

A `REPORT.md` is a markdown file with: (1) inputs simulated, (2) acceptance thresholds, (3) measured results, (4) PASS/FAIL per threshold, (5) artifacts committed (or DVC-tracked if too large).

---

## Sources

- [Antmicro — CFD-based active cooling, April 2026](https://antmicro.com/blog/2026/04/simulating-active-cooling-using-a-cfd-based-flow)
- [Antmicro — Improved thermal sim flow, Nov 2025](https://antmicro.com/blog/2025/11/improved-thermal-sim-flow)
- [OpenFOAM main site](https://www.openfoam.com/)
- [KiCad SPICE integration](https://www.kicad.org/discover/spice/)
