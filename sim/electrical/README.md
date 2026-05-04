# Electrical simulation

**Goal:** validate the power tree (sequencing, regulation, transient response) against AMD's Strix Halo PDG before tape-out.

---

## Tools

- **KiCad → ngspice** for SPICE simulation. KiCad's Schematic Editor has integrated ngspice support since KiCad 7. ([KiCad SPICE docs](https://www.kicad.org/discover/spice/), [ngspice tutorial](https://ngspice.sourceforge.io/ngspice-eeschema.html))
- **TI WEBENCH** for per-rail buck regulator validation against TI part datasheets.
- Vendor SPICE models from TI/ADI for TPS53676, TPS546B24, BQ25713.

---

## Required simulations

| Sim | What it validates | Pass criteria |
|---|---|---|
| **Power-up sequencing** | All Strix Halo rails come up in the order/timing AMD PDG specifies | All rails meet PG within ±5 % of nominal at the right time slot |
| **VDDCR_SOC load step** | Multiphase TPS53676 holds VDDCR_SOC under 0→80 A step | Undershoot <50 mV, recovery <50 µs |
| **VDD_MEM ripple** | LPDDR5X compliance — VDDQ 0.5 V regulation | Ripple <2 % of nominal under worst-case toggle |
| **PD 3.1 EPR negotiation** | TPS65987DDH negotiates 140 W with VBUS at 28 V | Sink reports 140 W, no chirp/glitch |
| **Battery cutoff** | BQ77915 cuts at 2.5 V/cell | No discharge below cutoff threshold |
| **Charge curve** | BQ25713 + LTC2943 deliver clean CC/CV charge | No oscillation; charge-current setpoint matches readback within 3 % |

---

## Files (when populated)

```
sim/electrical/
├── power-tree.kicad_sch         ← schematic of the power tree only
├── models/
│   ├── tps53676.lib
│   ├── tps546b24.lib
│   ├── bq25713.lib
│   └── ... (TI/ADI vendor SPICE)
├── runs/
│   ├── 01-sequencing.sp
│   ├── 02-vddcr-load-step.sp
│   ├── 03-vdd-mem-ripple.sp
│   └── ...
└── REPORT.md
```

---

## Quickstart

```bash
# In KiCad Schematic Editor (Eeschema):
# Inspect → Simulator → Run
# Or headless:
ngspice -b runs/02-vddcr-load-step.sp -o results/02.out
```
