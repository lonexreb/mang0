# Building mang0 — step by step

End-to-end guide to building one mang0 unit, from empty repo to working laptop. Roughly **9–12 months** for a small team with PCB layout experience; **18+ months** for a first-time builder.

> **Read order:** §0 (process) → §1–§5 (electronics) → §6–§7 (mechanical) → §8 (assembly) → §9–§11 (software). Skipping §0 is the most common way this goes wrong.

---

## Table of contents

0. [Prerequisites & process setup](#0-prerequisites--process-setup)
1. [Phase 1 — System architecture & block diagram](#1-phase-1--system-architecture--block-diagram)
2. [Phase 2 — Schematic capture](#2-phase-2--schematic-capture)
3. [Phase 3 — PCB layout](#3-phase-3--pcb-layout)
4. [Phase 4 — Mechanical design](#4-phase-4--mechanical-design)
5. [Phase 5 — Thermal design](#5-phase-5--thermal-design)
5b. [Phase 5.5 — Simulation gate (everything must pass before fab)](#5b-phase-55--simulation-gate)
6. [Phase 6 — Fabrication](#6-phase-6--fabrication)
7. [Phase 7 — Assembly](#7-phase-7--assembly)
8. [Phase 8 — Bring-up](#8-phase-8--bring-up)
9. [Phase 9 — Firmware (coreboot + EC)](#9-phase-9--firmware-coreboot--ec)
10. [Phase 10 — OS & AI runtime](#10-phase-10--os--ai-runtime)
11. [Phase 11 — Validation & burn-in](#11-phase-11--validation--burn-in)
12. [Image references](#image-references)

---

## 0. Prerequisites & process setup

**Don't skip this.** The single biggest difference between a v1-style hero project and a maintainable open laptop is the process scaffolding.

### 0.1 Skills

You (or the team) need:

- KiCad 8+ schematic + layout, comfortable with high-speed routing (DDR5, USB4, PCIe 4.0)
- Mechanical CAD — OnShape or Fusion 360
- Embedded C/C++ for the EC, light Rust optional
- Linux kernel & coreboot familiarity for bring-up
- Reflow / hot-air rework for BGA & QFN

### 0.2 Tools — bench

| Tool | Why | Approximate price |
|---|---|---|
| Hot air rework station (Quick 861DW or equivalent) | BGA + QFN | $250 |
| Soldering iron (Hakko FX-951 or Pinecil V2) | Fine-pitch | $80–$300 |
| Microscope (AmScope SM-4TZ) or USB inspection scope | Inspection | $150–$700 |
| Bench DMM (Brymen BM235) | Continuity & rails | $130 |
| 4-channel oscilloscope, ≥200 MHz (Rigol DHO924) | DDR5/USB4 won't be fully measurable, but you'll catch most issues | $700+ |
| Adjustable bench PSU (Rigol DP712 / Riden RD6018) | Power-up at low current limit | $100–$400 |
| USB logic analyzer (Saleae Logic 8 / DSLogic Plus) | I²C / SPI / UART | $100–$400 |
| 3D printer (Bambu A1 / P1S) | Jigs, fixtures, prototypes | $300–$800 |
| Reflow oven or hotplate | PCBA option B | $150–$1000 |

### 0.3 Tools — software

```bash
# Core EDA
brew install --cask kicad        # 8.0+
brew install kicad-cli           # for headless CI

# Firmware
pipx install platformio
brew install --cask gcc-arm-embedded

# Coreboot toolchain
git clone https://review.coreboot.org/coreboot
cd coreboot && make crossgcc-x64 CPUS=$(nproc)

# Reproducible env
curl --proto '=https' --tlsv1.2 -sSf -L https://install.determinate.systems/nix | sh -s -- install
```

### 0.4 Stand up the process scaffolding

Before you draw a single net, land these:

1. **Clone the skeleton**
   ```bash
   git clone https://github.com/<you>/mang0.git
   cd mang0
   ```
2. **Create the Nix flake** ([`nix/flake.nix`](../nix/flake.nix)) pinning KiCad, PlatformIO, Node, kernel ≥6.18.4.
3. **Wire up CI** ([`ci/`](../ci/)) — GitHub Actions that runs:
   - `kicad-cli sch erc` on every `*.kicad_sch`
   - `kicad-cli pcb drc` on every `*.kicad_pcb`
   - `kicad-cli pcb export gerbers` on tag pushes
   - `pio run` for `ec/`
   - `npm run build` for `website/`
4. **HIL fixture stub** ([`hil/`](../hil/)) — Raspberry Pi + USB serial harness. Even an empty `pytest` skeleton today saves you weeks at bring-up.
5. **`/review` slash-command** — Claude Code reviewer that diffs schematic netlists, EC firmware, and content against `main`.

### 0.5 Budget reality check

Per-laptop, May 2026 pricing. Full vendor links and per-line breakdown live in [`BOM.md`](./BOM.md).

| Item | Per-laptop cost |
|---|---|
| Compute — Framework Desktop $1,999 (Strix Halo + 128 GB harvest) + Hailo-10H $249 + OpenTitan $100 | $2,348 |
| Storage — 2 × Samsung 990 PRO 2 TB | $360 |
| Display — ATNA33TP11 4K AMOLED + connectors | $250 |
| Wireless — MT7925 + antennas | $25 |
| Power-tree ICs | $80 |
| Battery — 4 × Molicel P50B + balance flex | $50 |
| Cooling — vapor chamber + 2 blowers + thermal pads | $100 |
| I/O + audio + sensors + EC | $80 |
| Keyboard + trackpad | $150 |
| CNC chassis + anodize + hinge + screws | $550 |
| 140 W USB-C charger | $90 |
| PCBA fabrication (one-of-each set; fab MOQ gives you 5 of each board free) | $1,500 |
| **Per-laptop total** | **~$5,583** |

Plus a one-time first-build spares kit:
- **$58** sane (TPS65987DDH, BQ25713, TPS53676 ×2, 0402 caps, USB-C ×2, ESP32-S3) — PCBs already covered by fab MOQ
- **$307** cautious (above + spare Hailo-10H)

So a working first prototype: **~$5.6K parts** + **~$1.5K bench tools** you didn't already have.

> **Why no "batch of 5" column?** Fab MOQ already gives you 5 PCBs per design. You don't need 5 SoCs, 5 displays, or 5 batteries. The honest scaling is: PCBs (free, you have them) + a small spares kit of the parts that actually die during bring-up.

---

## 1. Phase 1 — System architecture & block diagram

**Goal:** before any schematic, agree on every chip and what bus connects what to what.

### 1.1 Block diagram

```
┌──────────────────────────────────────────────────────────────────────────┐
│                                                                          │
│   ┌─────────────────────────┐                  ┌────────────────────┐    │
│   │  AMD Ryzen AI Max+ 395  │ ───── eDP ─────▶ │  13.3" 4K AMOLED   │    │
│   │  Strix Halo (FP11 BGA)  │                  └────────────────────┘    │
│   │                         │                                            │
│   │  16× Zen 5  +  40 CU    │ ── USB4 ×2 ────▶ Type-C  Type-C            │
│   │  XDNA2 50 TOPS  iGPU    │                                            │
│   │                         │ ── PCIe 4.0 ───▶ NVMe ×2 (M.2 M-key)       │
│   └────────┬────────────────┘                                            │
│            │   LPDDR5X-8000 ×128 GB on-package                           │
│            │                                                             │
│            ├── PCIe 4.0 ×4 ─────▶ Hailo-10H NPU (M.2 M-key #2)           │
│            ├── PCIe 4.0 ×1 ─────▶ MT7925 WiFi 7 (M.2 E-key)              │
│            ├── eSPI / LPC ──────▶ EC (ESP32-S3)                          │
│            ├── SPI ─────────────▶ OpenTitan RoT  (TPM 2.0)               │
│            ├── I²S ─────────────▶ TPA2028 amp + 4× MEMS mics             │
│            └── USB 2.0 ─────────▶ Trackpad (PXM0057), Keyboard dongle    │
│                                                                          │
│   ┌─────────────────────────┐                                            │
│   │   EC: ESP32-S3          │ ── I²C ────▶ HUSB238 (PD), BQ25713,        │
│   │   (PD orchestration,    │              LTC2943, ATC sensors          │
│   │    fan control, mic     │ ── GPIO ───▶ LEDs, fan PWM, kill switches  │
│   │    gating, kill switch) │                                            │
│   └─────────────────────────┘                                            │
│                                                                          │
│   ┌─────────────────────────┐                                            │
│   │  Power tree             │                                            │
│   │  USB-PD 140 W EPR ────▶ │  20 V → buck array → VDDCR_SOC, VDD_MEM,   │
│   │  4S Amprius pack ────▶  │  VDD33, VDD18, VDD12, VDD09 (per Strix     │
│   │                         │  Halo PDG)                                 │
│   └─────────────────────────┘                                            │
│                                                                          │
└──────────────────────────────────────────────────────────────────────────┘
```

Save this as `docs/images/00-block-diagram.png` (export from draw.io or excalidraw). Update on every architectural change.

### 1.2 Power budget

| Rail | V | Peak A | Source |
|---|---|---|---|
| VDDCR_SOC | 0.8–1.2 | 80 | TPS53676 multiphase |
| VDD_MEM (LPDDR5X) | 1.05 / 0.5 | 12 | TPS546B24 + TPS62810 |
| VDD33 | 3.3 | 6 | TPS563257 |
| VDD18 | 1.8 | 4 | TPS563257 |
| VDD12 | 1.2 | 4 | TPS62810 |
| VDD09 | 0.9 | 8 | TPS62870 |
| Display | 3.3 / 5.5 | 1 | TPS61177 |
| USB4 retimer (none — native) | — | — | — |
| Fans + LEDs | 5 / 12 | 1 | TPS54360 |
| EC + RoT | 3.3 | 0.3 | LDO |

**Total budget:** ~85 W steady at the wall. Sized for 140 W EPR with 50 % headroom.

### 1.3 Bus map

| Bus | From | To | Constraints |
|---|---|---|---|
| LPDDR5X-8000 | Strix Halo | On-package | 256-bit, length-matched ±2 mil, 8 layers minimum |
| USB4 | Strix Halo | 2× Type-C | 40 Gbps, ≤4 in trace, length-matched, AC-coupled |
| PCIe 4.0 ×4 | Strix Halo | NVMe + Hailo + WiFi | ≤6 in, length-matched ±5 mil per pair |
| eDP 4-lane HBR3 | Strix Halo | OLED panel | AC-coupled, length-matched ±1 mil intra-pair |
| eSPI | Strix Halo | EC | 33 MHz, 4-bit |
| SPI | Strix Halo | OpenTitan | 25 MHz |
| I²C | EC | PD/charger/gauge/sensors | 400 kHz |
| I²S | Strix Halo | TPA2028 + mic array | TDM 8-slot |

---

## 2. Phase 2 — Schematic capture

KiCad 8+, one project per subsystem, mirroring [`anyon_e`](../laptop) layout.

### 2.1 Order of operations

1. **Power tree** (`power/`) — finish before motherboard. Get every Strix Halo rail spec'd against AMD's PDG (Platform Design Guide). Sequence per AMD's startup spec.
2. **Embedded controller** (`ec/`) — ESP32-S3, mostly carryover from anyon_e with additions for fan PWM, mic gating, and OpenTitan RST control.
3. **Motherboard** (`motherboard/`) — Strix Halo carrier. This is the long pole.
4. **Display, audio, sensors, switch, haptic** in parallel after power+EC are stable.

### 2.2 Strix Halo schematic checklist

- [ ] Every BGA pin assigned per the FP11 pinout (AMD reference design as starting point)
- [ ] LPDDR5X x8 ×16 lanes, on-package — schematic still captures the connection for reference & DRC
- [ ] eDP 4-lane HBR3 with AUX channel + HPD
- [ ] 2 × USB4 with native PD message-routing to TI TPS65987D (replacing v1's HUSB238 for EPR support)
- [ ] PCIe 4.0 ×4 + ×4 + ×1 (NVMe / Hailo / WiFi)
- [ ] eSPI 4-bit to EC at 33 MHz
- [ ] SPI to OpenTitan — dedicated CS, no sharing
- [ ] All decoupling per AMD PDG: 1 nF/pin pour + 10 nF distribution + bulk
- [ ] Power sequencing per the timing diagram in PDG

### 2.3 Power tree schematic — Strix Halo deltas vs anyon_e

The anyon_e `power/` board is a great template, but Strix Halo demands:

- Multiphase VDDCR_SOC (3-phase TPS53676 minimum; 4-phase preferred)
- Tighter LPDDR5X compliance — VDDQ 0.5 V with ±2 % regulation under load step
- 140 W PD EPR negotiation via TPS65987D
- Programmable telemetry on every rail (PMBus to EC for thermal-throttle decisions)

### 2.4 Embedded controller — what's new vs anyon_e

```c
// ec/src/main.cpp additions
#define MIC_ARRAY_EN     17     // gates the 4-mic array power
#define HAILO_PWREN      18     // Hailo-10H power good
#define HAILO_RST_N      19
#define OPENTITAN_RST_N  20
#define OPENTITAN_INT    21
#define FAN1_PWM         22
#define FAN2_PWM         23
#define FAN1_TACH        24
#define FAN2_TACH        25
#define LID_HALL         26     // proximity / lid detect
#define KILL_MIC         27     // hardware mic kill switch
#define KILL_CAM         28     // camera shutter solenoid
```

Inherit the I²C driver layer from anyon_e (`ec/lib/BQ25713/`, `ec/lib/LTC2943/`). Add:
- `Fan` class (PWM out + tach in, PID temp loop)
- `Hailo` class (power-state machine: off → standby → active)
- `Privacy` class (mic + camera physical kill, EC-mediated)

### 2.5 ERC discipline

```bash
kicad-cli sch erc motherboard/motherboard.kicad_sch --severity-error all --exit-code-violations
```

CI runs this on every push. Resolve before merge.

---

## 3. Phase 3 — PCB layout

### 3.1 Stackup

**Motherboard: 12 layers (HDI, Type II)**

| L# | Function | Cu | Dielectric |
|---|---|---|---|
| 1 | Signal — high-speed (USB4, PCIe) | 0.5 oz | — |
| 2 | GND | 1 oz | 3 mil prepreg |
| 3 | Signal — DDR + low-speed | 0.5 oz | 4 mil core |
| 4 | GND | 1 oz | 4 mil prepreg |
| 5 | Power — VDDCR_SOC | 1 oz | 4 mil core |
| 6 | Power — VDD_MEM, VDD33 | 1 oz | 4 mil prepreg |
| 7 | Power — VDD18, VDD12 | 1 oz | 4 mil core |
| 8 | GND | 1 oz | 4 mil prepreg |
| 9 | Signal — DDR | 0.5 oz | 4 mil core |
| 10 | GND | 1 oz | 4 mil prepreg |
| 11 | Signal — high-speed | 0.5 oz | 3 mil core |
| 12 | Signal — peripheral | 0.5 oz | — |

Total ~1.6 mm thick. Microvias L1↔L2 and L11↔L12 for BGA fan-out.

### 3.2 Routing rules

- **USB4**: 90 Ω differential, AC-coupled at receiver, length-matched ±2 mil intra-pair, ±10 mil pair-to-pair, no stubs
- **PCIe 4.0**: 85 Ω differential, length-matched ±5 mil
- **LPDDR5X**: matched to byte-lane, fly-by topology
- **eDP**: 100 Ω differential, AC-coupled
- **Min trace**: 3.5 mil / 3.5 mil for HDI; 5/5 for the rest

### 3.3 BGA fan-out

Strix Halo is a **FP11 BGA, ~25×25 mm, 0.65 mm pitch**. Use:
- Dogbone fan-out on L1, microvia to L3 for inner rows
- VIPPO (via-in-pad plated over) on every BGA pad — non-negotiable

### 3.4 DRC & length-match

```bash
kicad-cli pcb drc motherboard/motherboard.kicad_pcb \
  --severity-error all \
  --schematic-parity \
  --exit-code-violations
```

Use KiCad's *Length Tuner* for matched groups. Save constraint sets as `motherboard.kicad_dru`.

---

## 4. Phase 4 — Mechanical design

### 4.1 Chassis

Inherit anyon_e's anodized-aluminum CNC envelope. Modifications:

- **Bottom panel**: blower exhaust grilles, redesigned vent pattern
- **Hinge**: same OEM hinge if v1's source still ships; otherwise spec a custom Sugatsune
- **Battery bay**: deepened ~1 mm to accommodate the Amprius cells (slightly thicker per Wh)
- **Vapor chamber pocket**: 1.5 mm pocket on the heat-spreader frame

OnShape source: link from `chassis/README.md`. Export STEP on every commit affecting fit.

### 4.2 Display assembly

13.3" 4K AMOLED, eDP 40-pin IPEX 20455-040E (carryover from anyon_e). When tandem OLED in 13.3" ships in volume, swap the eDP pinout per the new panel's datasheet.

### 4.3 Keyboard & trackpad

Both unchanged from anyon_e:
- Cherry ULP wireless mech, nRF52840
- Azoteq PXM0057 glass trackpad

---

## 5. Phase 5 — Thermal design

The single biggest change vs anyon_e. Strix Halo at sustained 55 W will not be cooled by passive or light-active design.

### 5.1 Vapor chamber

- Custom copper VC, ~80 × 60 × 1.5 mm, sintered wick
- Source: Cooler Master OEM, NHC, or local OEM — get a sample part first
- Direct-touch the BGA top + Hailo + memory PoP

### 5.2 Blowers

- 2 × 35 mm × 6 mm blowers (Sunon MC35060V2-000U-A99 or Delta BFB0405HHA)
- 5 V PWM, tach feedback to EC
- Combined airflow ~5 CFM, ~30 dBA at 100 %

### 5.3 Thermal validation plan

| Workload | Expected steady-state package temp | Pass threshold |
|---|---|---|
| Idle | 38 °C | <45 °C |
| Single-thread peak | 65 °C | <80 °C |
| `stress-ng --cpu 16` | 88 °C | <95 °C |
| `llama.cpp` 70B inference (sustained) | 82 °C | <95 °C |
| Hailo-10H concurrent | +3 °C | <95 °C combined |

Use FLIR ETS320 or equivalent for spot validation.

---

## 5b. Phase 5.5 — Simulation gate

**Nothing goes to fab until simulation passes.** A $1,500 motherboard scrap, a $400 chassis re-CNC, or a 4-week vapor-chamber respin all hurt enough to justify a few weeks of CFD and SPICE.

Full pipeline lives in [`sim/`](../sim/). Six domains, each with a gate document the lead must check off:

| Domain | Tool | Gates |
|---|---|---|
| [sim/workload/](../sim/workload/) | Real Framework Desktop ($1,999) running ollama/llama.cpp | **Run this first.** Project-kill switch — if Strix Halo can't hit the tok/s targets on real silicon, no PCB work saves it. |
| [sim/thermal/](../sim/thermal/) | OpenFOAM `chtMultiRegionFoam` + ParaView + Blender | Vapor chamber + dual blower keeps Strix Halo <95 °C under sustained 55 W |
| [sim/mechanical/](../sim/mechanical/) | Autodesk Fusion (Claude MCP) + FreeCAD FEM | Chassis stiffness, hinge fatigue, drop test, vapor chamber pocket fit |
| [sim/electrical/](../sim/electrical/) | KiCad + ngspice | Power-tree sequencing per AMD PDG, VDDCR_SOC load step, VDD_MEM ripple |
| [sim/signal-integrity/](../sim/signal-integrity/) | OpenEMS + KiCad length tuner | USB4/PCIe 4.0/LPDDR5X eyes + length-match |
| [sim/firmware/](../sim/firmware/) | QEMU (coreboot) + Wokwi (ESP32-S3) | Boot flow, EC state machine, fan PID, OpenTitan reset/recover |

### 5.5.1 Why this is finally tractable

Two shifts in 2026 made simulation-first viable for a small team:

1. **Antmicro published a complete OpenFOAM → ParaView → Blender pipeline** for active cooling on a CNC-milled enclosure with Jetson AGX Thor — directly analogous to mang0's Strix Halo + vapor chamber problem. ([blog](https://antmicro.com/blog/2026/04/simulating-active-cooling-using-a-cfd-based-flow))

2. **Anthropic's April 2026 Creative Connectors** ([news](https://www.anthropic.com/news/claude-for-creative-work)) put Claude inside Blender and Fusion via MCP, collapsing the iteration loop from 30 min/cycle to ~2 min/cycle. The repo's [`.mcp.json`](../.mcp.json) wires it up.

### 5.5.2 The "kill switch": run workload validation FIRST

Before any sim work on the laptop itself, **buy a Framework Desktop ($1,999, 128 GB, Strix Halo) and run [`sim/workload/`](../sim/workload/) benchmarks.** This is path A from the BOM (you'd buy this anyway to harvest the SoC) and it answers the only question that matters: *does the AI thesis actually hold on this silicon?*

Acceptance:

| Model | Min tok/s | Stretch |
|---|---|---|
| Qwen3-30B-A3B | 30 | 50 |
| Llama 3.3 70B | 4 | 7 |
| GPT-OSS 120B | 25 | 35 |
| Mistral 7B | 60 | 90 |

If any **min** target fails, project pauses for explicit re-scope. No PCB work proceeds.

### 5.5.3 Iteration loop with the connectors

Once gates 1 (workload) and 2 (thermal) are open, the design loop is:

```
You (in chat):     "The package is hitting 102 °C in the new vent layout. Try widening
                    the rear exhaust 2 mm and re-run."

Claude (Fusion):   - opens chassis.f3d
                   - locates the rear-exhaust feature
                   - mutates the parameter
                   - re-exports STEP

Claude (Blender):  - re-imports STEP
                   - re-meshes via snappyHexMesh
                   - kicks off chtMultiRegionFoam
                   - waits, then renders the heat-map

You:               looks at result, decides next move.

Total wall time:   ~2 min vs ~30 min hand-driven.
```

Without the connectors this loop is the wall the project hits. With them it's a coffee break.

### 5.5.4 Gate review

Before any subsystem progresses to Phase 6 (Fabrication), the relevant `sim/<domain>/REPORT.md` must exist on `main` and show **PASS** for every threshold. CI enforces presence; humans enforce content.

---

## 6. Phase 6 — Fabrication

### 6.1 PCBA

**Option A — JLCPCB (cheapest, slowest, EU/US shipping):**
- Generate gerbers + drill + pick-and-place + BOM via `kicad-cli pcb export`
- Order with stencil for each board
- Strix Halo BGA likely **not** in JLC's parts library — supply as consigned

**Option B — local CM:**
- Better for BGA + HDI. Sierra Circuits, Royal Circuits, Elecrow Pro

**Order quantity:** 5 of each board. You will scrap 1–2.

### 6.2 CNC + anodizing

- Source aluminum 6061-T6
- 5-axis CNC for the lid + bottom; 3-axis acceptable for keyboard plate
- Type II anodize, color = matte black or natural
- Quote in batches of 5+ for sane unit pricing

### 6.3 Vapor chamber + blowers

- Order vapor chamber from sample-friendly vendor (4-week lead time)
- Blowers on Digi-Key

### 6.4 Battery pack

- Amprius SiCore 18650 / pouch cells in 4S configuration when available
- Until then: Molicel P50B in 4S1P
- BMS: BQ77915 (anyon_e carryover) — verify cell-balancing tolerance with new chemistry

---

## 7. Phase 7 — Assembly

### 7.1 Subassembly order

1. Reflow motherboard (BGA last — preheat plate + hot air)
2. Reflow power, EC, audio, switch boards
3. Test each PCBA individually before integration (see §8)
4. Mount keyboard + plate into top assembly
5. Trackpad + glass laminate
6. Display + eDP cable into lid
7. Vapor chamber + blowers onto motherboard with thermal interface
8. Battery pack into lower chassis
9. Motherboard + I/O ports into lower chassis
10. Top + bottom mate, hinge install
11. Final closure

### 7.2 Tools per step

Photograph each step. Future you will thank present you when v2.1 starts.

---

## 8. Phase 8 — Bring-up

**Stage every PCBA by itself.** Never plug in the full system on first power.

### 8.1 Power tree first

```bash
# Bench PSU @ 20 V, current limit 0.5 A
# Probe every rail before applying full current
```

Sequence:
1. 20 V in → verify EN_VIN
2. 3.3 V LDO → verify EC reset comes out
3. EC enumerates over USB-CDC (carryover anyon_e firmware should boot)
4. Manual GPIO toggle each rail, probe, log
5. Only after all rails clean → release current limit

### 8.2 EC alone

```bash
cd ec && pio run -t upload && pio device monitor
```

Expect the same logs as anyon_e (BQ25713 / LTC2943 / HUSB238 status). New: fan tach, mic kill state, OpenTitan presence.

### 8.3 Strix Halo first power

- Hold all peripherals off (Hailo, NVMe, WiFi, panel) via EC GPIO
- Apply VDDCR_SOC last per AMD sequencing
- Watch for current jump — typical idle ~3 A @ 0.9 V SOC = 2.7 W

### 8.4 Bus bring-up order

eSPI → SPI (OpenTitan) → I²C → eDP → USB → PCIe → USB4. Each step has a known good probe point.

---

## 9. Phase 9 — Firmware (coreboot + EC)

### 9.1 coreboot port

Strix Halo is a **Glinda-class AMD platform**. Start from an existing Glinda mainboard config in `coreboot/src/mainboard/amd/`. Add `mang0/` directory with:

- `Kconfig` — board options
- `devicetree.cb` — bus/device topology
- `mainboard.c` — early init hooks
- `gpio.c` — pin states from PDG

Build:
```bash
cd coreboot
make defconfig BOARD=mang0
make -j$(nproc)
# Outputs build/coreboot.rom
```

Flash to the SPI flash via external programmer (CH341A or Dediprog SF600).

### 9.2 edk2 payload

coreboot-as-firmware + edk2 payload provides UEFI boot services. Build edk2 against the `CorebootPayloadPkg` and load as a coreboot payload.

### 9.3 EC firmware

Carryover from anyon_e + new modules. Test path:
1. PlatformIO unit tests on host (Unity)
2. HIL fixture replays known-good PD/charger I²C transactions
3. Final smoke test on real board

---

## 10. Phase 10 — OS & AI runtime

### 10.1 NixOS reference image

```nix
# nix/nixos-reference.nix
{ config, pkgs, ... }: {
  boot.kernelPackages = pkgs.linuxPackages_latest;  # ≥6.18.4 for gfx1151
  hardware.amdgpu.opencl.enable = true;
  hardware.amdgpu.amdvlk.enable = true;
  hardware.cpu.amd.updateMicrocode = true;

  services.ollama = {
    enable = true;
    acceleration = "rocm";
    rocmOverrideGfx = "11.5.1";  # Strix Halo gfx1151
  };

  environment.systemPackages = with pkgs; [
    llama-cpp
    mlc-llm
    rocmPackages.rocm-smi
  ];
}
```

### 10.2 Default model

Bundle **Qwen3-30B-A3B** (~52 tok/s on Strix Halo per benchmarks). Provide one-command download for Llama 3.3 70B and GPT-OSS 120B.

### 10.3 Hailo-10H driver

```bash
# Hailo provides a closed kernel module + open user-space
# Document this caveat clearly in README
sudo apt install hailort
```

If Hailo's open-source progress in 2026 yields a mainline driver, prefer it.

### 10.4 OpenTitan TPM

```bash
# Provision the TPM 2.0 endorsement key
sudo tpm2_createek -G rsa -c ek_handle.ctx
```

---

## 11. Phase 11 — Validation & burn-in

### 11.1 Functional acceptance

| Test | Pass criteria |
|---|---|
| Cold boot to NixOS login | <15 s |
| `ollama run qwen3:30b "hello"` | First token <2 s, ≥45 tok/s |
| USB4 — eGPU enumeration | Lspci sees AMD GPU |
| WiFi 7 — iperf3 to access point | ≥2 Gbps |
| Battery — full discharge under typical load | ≥9 h SDR web/code |
| Battery — charge 0→80 % | ≤45 min @ 140 W |
| Hailo-10H — wake-word latency | <300 ms |

### 11.2 Burn-in

- 72 h `stress-ng` + `llama.cpp` loop
- Thermal logging every 10 s
- Battery cycle 3× to verify gauge calibration

### 11.3 Open-hardware compliance audit

- All schematics published
- All gerbers buildable from repo
- No NDA-only datasheets in critical path
- Firmware reproducible from `nix build`

---

## Image references

This guide deliberately uses ASCII diagrams in repo. For polished images, drop into `docs/images/` and reference here:

| Path | What | Source / suggestion |
|---|---|---|
| `docs/images/00-block-diagram.png` | Top-level system block diagram | Export from draw.io |
| `docs/images/10-pcb-stackup.png` | 12-layer stackup illustration | Diagram in Excalidraw |
| `docs/images/20-strix-halo-fanout.png` | BGA fan-out plan | Screenshot from KiCad |
| `docs/images/30-vapor-chamber-layout.png` | Vapor chamber + blower routing | OnShape render |
| `docs/images/40-thermal-flir.jpg` | FLIR thermal under load | Capture during validation |
| `docs/images/50-bringup-bench.jpg` | Bench setup at first power | Photograph |
| `docs/images/60-final-render.png` | Hero render of finished unit | KeyShot or OnShape render |
| `docs/images/cover.jpg` | Cover photo for the README | Photograph after final assembly |

External image references that may be useful while building:
- AMD Ryzen AI Max+ 395 product page imagery — https://www.amd.com/en/products/processors/laptop/ryzen/ai-300-series/amd-ryzen-ai-max-plus-395.html
- Hailo-10H product brief PDF — https://hailo.ai/files/hailo-10h-m-2-et-product-brief-en/
- OpenTitan reference architecture — https://opentitan.org/
- Samsung tandem OLED Penta announcement — https://tftcentral.co.uk/news/samsung-display-announce-qd-oled-penta-tandem-brand-to-distinguish-latest-panel-technologies
- Amprius SiCore cell datasheet — https://amprius.com/amprius-launches-sicore-450-wh-kg-high-energy-cell-with-near-term-mass-production-capability-to-scale/

---

## When you get stuck

- KiCad routing question → KiCad forum + the [`anyon_e`](../../laptop/) precedent
- AMD power sequencing → AMD PDG (NDA — request via authorized distributor)
- Coreboot port → `#coreboot` on Libera.Chat
- ROCm / kernel issues → Phoronix forums, Framework community thread for Strix Halo
- This repo specifically → file an issue; tag with subsystem

Good luck. Build mang0.
