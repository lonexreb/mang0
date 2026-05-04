# Signal integrity

**Goal:** validate USB4 (40 Gbps), PCIe 4.0 (16 GT/s), and LPDDR5X (8 Gbps) channels — eye openings, length-match, return loss — before motherboard tape-out.

This is the domain ngspice cannot reach. High-speed channel sims need 3D field solvers + IBIS-AMI behavioral models.

---

## Tools

- **OpenEMS** — open-source FDTD EM solver. ([openEMS.de](https://www.openems.de/start/))
- **Sonnet Lite** — free 2.5D MoM solver (limited but good for via stubs and trace coupling).
- **KiCad's built-in length tuner** for differential length-match (deterministic, no sim needed).
- **Vendor IBIS-AMI models** from AMD (Strix Halo SerDes) and the receiver chips (USB4 retimers — none in mang0 since native, but eDP receiver and NVMe controllers do).

Closed-source alternatives (only if mang0 partners with a vendor): Cadence Sigrity, ANSYS HyperLynx.

---

## Required simulations

| Channel | Validation | Pass criteria |
|---|---|---|
| USB4 (40 Gbps, ~4 in trace) | Eye diagram at receiver | Compliant per USB4 v2.0 mask, no closure |
| PCIe 4.0 ×4 (16 GT/s, ~6 in) | Insertion loss, return loss, eye | <8 dB IL @ Nyquist, RL >10 dB, eye clear |
| LPDDR5X x16 byte lanes | Setup/hold + DQ/DQS skew | <30 ps skew within byte, fly-by topology balanced |
| eDP HBR3 (8.1 Gbps × 4) | Eye + AC coupling | Compliant per VESA eDP 1.4b mask |

---

## Files (when populated)

```
sim/signal-integrity/
├── usb4/
│   ├── channel.openems          ← FDTD geometry
│   └── eye-diagrams/
├── pcie4/
│   └── ...
├── lpddr5x/
│   └── ...
└── REPORT.md
```

---

## Length-match (deterministic, no sim)

KiCad 8 has a length tuner. Constraint sets live in `motherboard/motherboard.kicad_dru`. Required tolerances:
- USB4: ±2 mil intra-pair, ±10 mil pair-to-pair
- PCIe 4.0: ±5 mil intra-pair, ±20 mil pair-to-pair
- LPDDR5X: ±5 mil within byte lane, fly-by topology
- eDP: ±1 mil intra-pair, ±5 mil pair-to-pair

If KiCad reports any tuning failure → DRC fails → CI fails → no merge.
