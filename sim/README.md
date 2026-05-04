# Simulation

**Simulate first, fab second.** mang0 is ~$5.6K in parts with 4-week chassis lead times. One thermal mistake costs a chassis re-CNC + a vapor chamber re-spin (~$500 + 4 weeks). One DDR layout error is a $1,500 motherboard scrap. Catching those in simulation is the whole point.

This directory holds the simulation models, scripts, and validation thresholds that must pass **before** anything goes to fab.

---

## Six simulation domains

| Domain | Tool | What gets validated | Gating decision |
|---|---|---|---|
| [thermal/](./thermal/) | OpenFOAM + ParaView + Blender | Vapor chamber + dual blower can dissipate sustained 55 W; package stays <95 °C under llama.cpp 70B | **Blocks**: chassis CNC, vapor-chamber order |
| [mechanical/](./mechanical/) | Autodesk Fusion (via Claude MCP), FreeCAD FEM | Chassis stiffness, hinge stress, drop test | **Blocks**: chassis CNC |
| [electrical/](./electrical/) | KiCad + ngspice | Power tree sequencing per AMD PDG, rail regulation under load step | **Blocks**: motherboard PCB tape-out |
| [signal-integrity/](./signal-integrity/) | OpenEMS / Sonnet Lite | USB4 / PCIe 4.0 / LPDDR5X eye openings, length-match validation | **Blocks**: motherboard PCB tape-out |
| [firmware/](./firmware/) | QEMU (coreboot), Wokwi (ESP32-S3) | Boot flow, EC state machine, PD negotiation, fan PID | **Blocks**: first-silicon flash |
| [workload/](./workload/) | Real Framework Desktop | Validates the thesis (70B at ≥5 tok/s on Strix Halo) **before** mang0 silicon exists | **Blocks**: project scope (kill if thesis fails) |

The **workload** domain is unusual but critical — buy a Framework Desktop now, prove that the AI thesis works on this exact silicon, then commit to the laptop build. If it doesn't hit the tok/s targets, no amount of clever PCB work will save the project.

---

## Why now (April 2026 inflection point)

Two things changed in 2026 that make this practical for a small team:

1. **Antmicro published a full OpenFOAM → ParaView → Blender pipeline** for active cooling on a CNC-milled enclosure with a Jetson AGX Thor — basically the same problem as mang0's Strix Halo + vapor chamber. ([blog](https://antmicro.com/blog/2026/04/simulating-active-cooling-using-a-cfd-based-flow))

2. **Anthropic shipped 9 Claude Creative Connectors** ([news](https://www.anthropic.com/news/claude-for-creative-work)), including:
   - **Blender** ([guide](https://claude.com/resources/tutorials/using-the-blender-connector-in-claude)) — full Python API access; Claude reads/writes the open scene
   - **Autodesk Fusion** ([Autodesk's announcement](https://aps.autodesk.com/blog/bringing-fusion-claude-creative-work)) — text-to-CAD, parametric model edits via natural language

This means the CAD/CFD loop ("change vent shape → re-mesh → re-solve → visualize → critique → iterate") goes from days-per-iteration to minutes-per-iteration when Claude is sitting inside Blender and Fusion via MCP.

---

## Connector setup (one-time)

The repo's [`.mcp.json`](../.mcp.json) wires Claude Code into the relevant MCP servers. Per-tool setup:

### Blender connector
1. Claude Desktop → **Customize → Connectors → Blender → Add**
2. In Blender 4.2+: **Edit → Preferences → Add-ons** → install official MCP add-on
3. Each session: open scene → press **N** → BlenderMCP sidebar → **Connect to Claude**
4. Reference: [Eigent guide](https://www.eigent.ai/blog/claude-blender-mcp), [MCP.Directory walkthrough](https://mcp.directory/blog/claude-blender-connector-guide)

### Autodesk Fusion connector
1. Active Fusion subscription required
2. Claude Desktop → **Customize → Connectors → Autodesk Fusion → Add**
3. No add-on install — Fusion MCP runs through Autodesk's APS layer
4. Community alternatives if you don't have a subscription: [ndoo/fusion360-mcp-bridge](https://github.com/ndoo/fusion360-mcp-bridge), [Joe-Spencer/fusion-mcp-server](https://github.com/Joe-Spencer/fusion-mcp-server), [Misterbra/fusion360-claude-ultimate](https://github.com/Misterbra/fusion360-claude-ultimate)

### What Claude can do once connected
- **Blender**: analyze the open scene, write Python that mutates geometry, run simulations from the Blender Python console, render. The Antmicro pipeline runs entirely from Blender as the host environment.
- **Fusion**: text-to-CAD ("add a 1.5 mm pocket on the heat-spreader frame for the vapor chamber"), parametric edits, derive 2D drawings.
- Reads live project context, executes code, performs actions in-app — not just chat about it.

---

## Gate review

Before any subsystem progresses to fab, the relevant simulation domain owner must check off:

| Subsystem | Gate document | Owner |
|---|---|---|
| Motherboard PCB | `sim/electrical/REPORT.md` + `sim/signal-integrity/REPORT.md` | Electrical lead |
| Power PCB | `sim/electrical/REPORT.md` | Electrical lead |
| Vapor chamber + chassis | `sim/thermal/REPORT.md` + `sim/mechanical/REPORT.md` | Mechanical lead |
| EC firmware | `sim/firmware/REPORT.md` | Firmware lead |
| AI runtime | `sim/workload/REPORT.md` | (decides if project continues) |

A gate document is a markdown file with: (1) inputs simulated, (2) acceptance thresholds, (3) measured results, (4) pass/fail, (5) sim artifacts committed (or DVC-tracked if too large).

---

## Sources

- [Anthropic — Claude for Creative Work](https://www.anthropic.com/news/claude-for-creative-work) — official April 2026 launch
- [9to5Mac coverage of the 9 connectors](https://9to5mac.com/2026/04/28/anthropic-releases-9-new-claude-connectors-for-creative-tools-including-blender-and-adobe/)
- [DEVELOP3D — "Claude for CAD" arrives with Blender + Fusion](https://develop3d.com/ai/claude-for-cad-blender-autodesk-fusion/)
- [Antmicro — Simulating active cooling using a CFD-based flow](https://antmicro.com/blog/2026/04/simulating-active-cooling-using-a-cfd-based-flow) (the canonical pipeline mang0 follows)
- [Antmicro — Open source thermal simulation pipeline](https://antmicro.com/blog/2025/03/open-source-thermal-simulation-analysis-and-visualization)
- [Blender MCP server — official Blender lab](https://www.blender.org/lab/mcp-server/)
- [Autodesk Platform Services — bringing Fusion to Claude](https://aps.autodesk.com/blog/bringing-fusion-claude-creative-work)
