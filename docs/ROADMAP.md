# mang0 — 12-week build roadmap

The honest 3-month plan. Assumes:

- **Full-time** work (40 hr/wk). Evenings/weekends doubles every interval below.
- **Solo** builder; second person scales some weeks (layout + bring-up) ~1.5×.
- **Scope = "Framework Desktop mainboard + everything else custom".** Strix Halo silicon and 128 GB LPDDR5X live on the harvested Framework Desktop board (`$1,999`, see [`SUPPLY-CHAIN.md`](./SUPPLY-CHAIN.md)). Everything mechanical, electrical, and firmware *around* it is mang0 custom: chassis, EC board, power-management daughterboard, mic-array + sensor board, display carrier, battery pack with BMS, vapor-chamber cooling. **Five custom PCBs**, one custom CNC chassis, one custom firmware.
- A **fully custom Strix Halo mainboard** is a v2 / 6-month escalation — see [§13](#13-v2-escalation-path).

---

## Critical path (the only schedule that matters)

```
Week 1   2   3   4   5   6   7   8   9   10  11  12
        ─┬─────────────────────────────────────────
Vapor ch.│●━━━━━━━━━━━━━━━━━ARRIVES                      ← order day 1, 4-wk lead
Strix HW │●━ARRIVES                                      ← Framework Desktop
PDG appl.│●━━━━━━━━━━━━━━━━━━━━━ MAYBE arrives           ← non-blocking for v1
Schemati.│   ━━━━━━━━━━━━━                               ← weeks 2–4
PCB lay. │              ━━━━━━━━━━━━                     ← weeks 5–7
Sim gate │                          ━━━                  ← week 7
PCBA fab │                            ━━━━━━━            ← order wk 8, 3-wk fab
Chassis  │                            ━━━━━━━            ← order wk 8, 2-wk CNC
Bring-up │                                       ━━━     ← weeks 11–12
Integr.  │                                          ━━   ← week 12
```

The vapor chamber is the absolute floor — order **day 1**, no exceptions. Everything else stacks behind that.

---

## Week 1 — orders out, dev env up

**Goals**: long-pole orders placed, validation rig running, schematic capture starts day 5.

| Day | Task |
|---|---|
| Mon | Order Framework Desktop 128 GB ($1,999). Order vapor chamber sample ($40, 4-wk lead). Order Hailo-10H ($249). |
| Tue | Order ATNA33TP11 panel ($300). Apply to zeroRISC OpenTitan EAP. Apply to AMD PDG via authorized distributor. Set up dev env (Nix flake, KiCad 8.0, PlatformIO, OpenFOAM, FreeCAD/Fusion). |
| Wed | Framework Desktop arrives. Boot Fedora 42, install ROCm, verify ollama runs. *This is your "is the silicon real" check.* |
| Thu | Strip the Framework Desktop. Document every connector, every rail, every interface the mainboard exposes. Photograph teardown for `docs/images/teardown/`. |
| Fri | Power-tree budget locked (see `docs/BUILD.md` §1.2). Begin `power/` schematic capture in KiCad. |

**Deliverables:** orders confirmed; teardown notes committed; `power/` schematic skeleton.

**Risks:** Hailo stock; Framework allocation. **Mitigation:** order day 1, accept 2-week slip if needed and start schematic capture in parallel (Hailo isn't blocking schematic).

---

## Week 2 — power + EC schematics

| Day | Task |
|---|---|
| Mon–Wed | `power/` schematic complete. PD 3.1 EPR sink (TPS65987DDH), BQ25713 charger, BQ77915 protector, LTC2943 gauge, harvest taps for the rails Framework already provides. ERC clean. |
| Thu–Fri | `ec/` schematic. Carryover from anyon_e + new pins: fan PWM ×2, fan tach ×2, OpenTitan RST_N + INT, mic array EN, camera shutter solenoid driver, lid Hall sensor, Hailo PWREN/RST_N. |

**Deliverables:** `power/power.kicad_sch`, `ec/ec.kicad_sch`, both ERC-clean and pushed.

---

## Week 3 — sensors + display + battery

| Day | Task |
|---|---|
| Mon–Tue | `sensors/` schematic. 4× ST MP34DT06JTR mics on I²S TDM, ST VL53L8 ToF, AMS TSL2591 ambient, OmniVision OV5675 + Pixart PAS6180 (USB to Framework). EC-gated power for hardware kill switches. |
| Wed–Thu | `display/` carrier schematic. Routes Framework's eDP/DP-out to ATNA33TP11's IPEX 20455-040E connector. Backlight driver (TPS61177). |
| Fri | `batteries/` BMS schematic. 4× Molicel P50B in 4S1P (or pouch when SiCore ships) with BQ77915 protection. |

**Deliverables:** three more ERC-clean schematics. Five-board set is now schematically complete in draft.

---

## Week 4 — schematic review + chassis concept + tools order

| Day | Task |
|---|---|
| Mon | All-day schematic review with `code-reviewer` agent + your own pass. Fix everything before layout starts. |
| Tue | **Order bench tools** (see [`INSTRUMENTS.md`](./INSTRUMENTS.md)). Lead time on used Rigol scope can be 1–2 weeks; everything must be on your bench by week 11. |
| Wed | Concept lock in Blender. Re-run `chassis/blender/dimensions.py`, fit assertions clean. Adjust for Framework mainboard's 125 × 125 mm footprint vs original 280 × 90 — this is a meaningful redesign. |
| Thu–Fri | Translate Blender concept → Fusion parametric model. First STEP export. |

**Deliverables:** schematics frozen for layout. Tools en route. Chassis concept locked.

---

## Week 5 — layout starts, motherboard interface board (the long pole)

| Day | Task |
|---|---|
| Mon | Layout setup: stackup definitions, design rules in `*.kicad_dru`. |
| Tue–Fri | `power/` PCB layout. 4-layer, ~80 × 60 mm. Multiphase VDDCR_SOC layout is the trickiest part — get the inductor placement and gate-drive loops right. |

**Deliverables:** `power/power.kicad_pcb` with 90 % of placement done.

---

## Week 6 — EC + sensors + display layout

| Day | Task |
|---|---|
| Mon–Tue | `ec/` layout. 4-layer, ~50 × 50 mm. ESP32-S3 antenna keep-out, I²C routing, fan-control headers. |
| Wed | `sensors/` layout. 4-layer, ~60 × 30 mm. I²S TDM length-match. |
| Thu–Fri | `display/` layout. eDP differential pairs, length-match ±2 mil, AC coupling at receiver. |

**Deliverables:** four PCBs at "ready for review" stage.

---

## Week 7 — sim gates, layout cleanup

| Day | Task |
|---|---|
| Mon | `sim/electrical/` ngspice runs on power tree. VDDCR_SOC load step, EPR sink. Drop TI vendor models. Commit `sim/electrical/REPORT.md`. |
| Tue | `sim/signal-integrity/` length-match validation in KiCad's tuner. Limited OpenEMS for eDP if needed. Commit `REPORT.md`. |
| Wed | `sim/thermal/` first OpenFOAM CFD pass. Geometry from Fusion → STEP → snappyHexMesh → chtMultiRegionFoam. Iterate vent layout. Commit `REPORT.md`. |
| Thu | `sim/mechanical/` Fusion FEA: lid torsion, bottom deflection, hinge fatigue. Commit `REPORT.md`. |
| Fri | DRC clean on all boards. Length-match clean. Schematic ↔ PCB parity check. |

**Deliverables:** four sim REPORT.md files showing PASS. CI gate green. Layout frozen.

---

## Week 8 — orders go out

| Day | Task |
|---|---|
| Mon | Generate gerbers + drill + pick-and-place + BOM via `kicad-cli`. Upload to JLCPCB Standard Lead Time (5 boards × 5 designs = 25 PCBs, ~$120). Order assembly with consigned parts for SMD-heavy ones. |
| Tue | Battery cells, mics, ToF, ambient sensor, camera modules, vapor-chamber thermal pads — order in one Mouser/DigiKey cart. ~$300. |
| Wed | Submit chassis CNC to Xometry / SendCutSend (lid + bottom + plate). Submit Type II anodize quote separately. |
| Thu–Fri | Begin EC firmware port + Wokwi sim. Run `sim/firmware/` cold-boot scenario; commit `REPORT.md`. |

**Deliverables:** all fab orders out. Cash outlay this week ~$1,200. EC firmware in Wokwi.

---

## Week 9 — wait, build subassemblies

| Day | Task |
|---|---|
| Mon–Tue | Battery pack assembly. Spot-weld nickel strip, install BMS, terminate balance flex. |
| Wed | Speaker assembly + acoustic chamber design (3D-print prototype). Antenna pigtails terminated. |
| Thu–Fri | Wire harnesses for chassis-internal cabling. Display flex cable terminated. |

**Deliverables:** battery, audio, antennas, harnesses ready for integration.

---

## Week 10 — boards arrive, fixtures ready

| Day | Task |
|---|---|
| Mon | PCBs arrive. Initial visual inspection under microscope. |
| Tue | Chassis arrives from CNC. Fit-check against Framework mainboard, vapor chamber, battery pack. |
| Wed | Build HIL fixtures in `hil/` for power and EC. Pi + serial harness. |
| Thu–Fri | Anodize handoff (1 week). Use the time for thermal-pad pre-cuts and final cable management plan. |

**Deliverables:** parts in hand, fixtures live, anodize in progress.

---

## Week 11 — bring-up

| Day | Task |
|---|---|
| Mon | **Power board first.** Bench PSU at 20 V, 0.5 A current limit. Probe every rail in sequence. Validate against `sim/electrical/REPORT.md`. |
| Tue | Power board good → EC board. Flash anyon_e firmware base, verify I²C enumeration. Run HIL `01-cold-boot.test.yaml`. |
| Wed | Display board → drive ATNA33TP11 from a known-good HDMI source first, then wire to Framework mainboard's eDP/DP-out. |
| Thu | Sensor board bring-up. Validate ToF, ambient, mic array via I²C/I²S sniff. |
| Fri | Hailo-10H standalone test on bench. Run a 7B model, confirm 10 tok/s @ <5 W. |

**Deliverables:** five PCBs verified individually.

---

## Week 12 — integration + first boot in chassis

| Day | Task |
|---|---|
| Mon | Anodize back. Mount Framework mainboard + vapor chamber + blowers in lower chassis. Thermal pads applied. |
| Tue | Mount power board, EC board, sensor board, display carrier, battery. Cable harness routed. |
| Wed | Display + lid hinge install. Antenna routing through hinge. |
| Thu | **First closed-shell boot.** Power, fan ramp, display, ROCm, ollama. |
| Fri | Photos. Burn-in: 24-h `stress-ng + llama.cpp` loop. Thermal logging to CSV. Commit final `sim/thermal/REPORT.md` matched against measured. |

**Deliverables:** working laptop. 1 unit. Photos. Burn-in data.

---

## Budget by week (cumulative cash outlay)

| Week | Outlay | Cumulative | What |
|---|---|---|---|
| 1 | $2,700 | $2,700 | Framework Desktop, vapor chamber sample, Hailo-10H, panel, sensor parts, OpenTitan EAP fee |
| 2 | $50 | $2,750 | Connectors, sample components |
| 3 | $50 | $2,800 | More small components |
| 4 | $1,800 | $4,600 | Bench tools (recommended tier — see `INSTRUMENTS.md`) |
| 5 | $0 | $4,600 | Layout work — no outlay |
| 6 | $0 | $4,600 | Layout work — no outlay |
| 7 | $0 | $4,600 | Sim work — no outlay |
| 8 | $1,200 | $5,800 | PCBA fab + parts cart + CNC + anodize quote |
| 9 | $150 | $5,950 | Battery cells, balance flex, speaker drivers |
| 10 | $0 | $5,950 | Receive only |
| 11 | $50 | $6,000 | Bring-up consumables (flux, solder paste, etc.) |
| 12 | $0 | $6,000 | Integration |

**Cap-ex total ~$6,000.** That's parts ($4,200) + tools ($1,800). If you already own tools, drop to ~$4,200.

---

## Risks + mitigations

| Risk | Probability | Impact | Mitigation |
|---|---|---|---|
| Vapor chamber slips past 4 weeks | Medium | High (blocks chassis assembly) | Order from 2 vendors in parallel; accept the better-quality one |
| Framework mainboard interfaces don't expose what we expect | Medium | High | Week 1 teardown is exactly to derisk this. If a key signal isn't exposed, reduce scope (e.g. drop tandem-OLED ambition) |
| AMD PDG never arrives | High | Low for v1 | Not blocking — Framework already validated the platform. Only matters if we escalate to v2 (custom mainboard) |
| First-pass thermal sim shows package >100 °C | Medium | Medium | Iterate vent layout in week 7. If still failing, increase blower count to 3 or relax sustained power target |
| BGA reflow yield issues on EC | Low (no BGAs in mang0 PCBs) | Low | All custom PCBs are 0.5 mm pitch QFN max. Reflow hotplate sufficient |
| coreboot port lags | High | Low for v1 | Framework's existing firmware boots Linux fine. Only relevant if we replace Framework mainboard |
| Bench tools delivery slips past week 11 | Medium | High | Order week 4, not week 8. Buy used on eBay if new is slow |
| You burn out | Medium | Critical | Take Sundays off. Write the burn-in down on Friday week 12 either way |

---

## Decision points (when to escalate or descope)

| Week | Decision |
|---|---|
| 1 (end) | Strix Halo on Framework Desktop hits target tok/s? If no → stop, re-scope, do not order more parts |
| 4 (end) | All five schematics ERC-clean? If two or more are still failing → slip layout by 1 week, do not let bad schematics into layout |
| 7 (end) | All four sim gates PASS? If thermal fails → stop, re-design vent layout or relax sustained power. Do **not** order PCBs against a failing thermal sim |
| 8 | Pull v2-escalation lever? See §13 |
| 11 (end) | All five PCBs bring-up clean? If two or more are dead → debug week 12, accept 1-week slip, ship in week 13 |

---

## 13. v2 escalation path

If at the end of Week 8 you want to escalate to a *fully* custom Strix Halo mainboard (replacing the Framework board), here's the realistic add-on:

- +6 weeks for motherboard schematic capture (with PDG access, +12 weeks without)
- +4 weeks for 12-layer HDI layout (USB4, PCIe 4.0, LPDDR5X)
- +3 weeks for PCBA fab on the motherboard (rush)
- +6 weeks for coreboot port to a brand-new mainboard
- = **+19 weeks (4.5 months) on top of v1**

Total v2 = ~7.5 months from project start. Not 3 months. Do not commit to v2 until you have v1 working in chassis.

The custom-everything-around-Framework v1 is itself a real open-hardware laptop — chassis, EC, power, sensors, display carrier, battery, firmware all custom. It's a credible end product, not a stepping stone.

---

## Where this document goes wrong

If by week 5 the schedule is slipping by 1 week or more, **the assumption is wrong**, not the schedule. Stop, re-baseline, and if the slip is irreparable, descope:

1. First descope target: tandem OLED → keep the ATNA33TP11 v1 panel
2. Second: drop the mic array → use Framework's audio in
3. Third: drop OpenTitan → use Framework's existing TPM via mainboard
4. Fourth: drop Hailo-10H → SoC NPU only

Each descope buys ~1 week. Use them in order, don't fight reality.
