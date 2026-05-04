# Industrial design — Blender

Blender is the **primary mechanical sketch tool** for mang0. It owns the closed-lid envelope, internal component placement, and the visualization that feeds CFD ([`sim/thermal/`](../../sim/thermal/)) and FEA ([`sim/mechanical/`](../../sim/mechanical/)).

Blender pairs with Claude via the [Blender MCP connector](https://www.anthropic.com/news/claude-for-creative-work) (wired in [`.mcp.json`](../../.mcp.json)) so the design loop runs conversationally:

> "Move the vapor chamber 5 mm forward and re-export STEP."
> "Show me a cross-section through the SoC and the battery."
> "Verify nothing in the Cooling collection clips into the Battery collection."

---

## Files

| File | What |
|---|---|
| [`dimensions.py`](./dimensions.py) | **Single source of truth** for every mechanical dimension. Importable from the scene script. Re-runnable as a sanity check (`python3 dimensions.py` — runs fit assertions). |
| [`generate_starter_scene.py`](./generate_starter_scene.py) | Idempotent Blender script that builds the parametric assembly: chassis, motherboard, SoC, NPU, NVMe, WiFi, vapor chamber, dual blowers, battery pack (4 × 21700), trackpad, USB-C ports, lid + AMOLED panel. Re-runs cleanly. |
| `mang0.blend` *(generated, not committed)* | The working scene. Save in Blender or generate headlessly. |

---

## First-time setup

1. **Install Blender 4.2+** ([blender.org](https://www.blender.org/download/)).
2. **Sanity-check dimensions:**
   ```bash
   python3 chassis/blender/dimensions.py
   ```
   Should print the dimensional table and `ALL FITS OK`.
3. **Generate the scene:**
   - **GUI**: open Blender → Scripting tab → Open `generate_starter_scene.py` → Run Script → save as `chassis/blender/mang0.blend` (gitignored).
   - **Headless**:
     ```bash
     blender --background --python chassis/blender/generate_starter_scene.py \
             --output-file chassis/blender/mang0.blend
     ```
4. **Wire up Claude connector:**
   - Claude Desktop → Customize → Connectors → Blender → Add
   - In Blender: Edit → Preferences → Add-ons → install the official MCP add-on
   - In your scene: press N → BlenderMCP sidebar → **Connect to Claude**
   - Reference: [official Blender connector tutorial](https://claude.com/resources/tutorials/using-the-blender-connector-in-claude)

---

## Scene structure

```
Collections:
├── Chassis      Lower shell (floor + 4 side walls), wall thickness 1.5 mm
├── Display      Lid shell + AMOLED panel
├── Motherboard  PCB + Strix Halo SoC + Hailo-10H + NVMe + WiFi 7
├── Cooling      Vapor chamber + 2 blowers
├── Battery      4 × 21700 cells in 4S1P, axes along X
└── Input        Trackpad glass + USB-C port openings
```

Materials are pre-set so each subsystem renders distinctly: anodized aluminum for chassis, FR-4 green for PCB, copper for vapor chamber, dark silicon for BGA, blue PCB for daughter modules, glass for trackpad, near-black AMOLED.

Camera + 3-point lighting set up for hero renders. Cycles, 1920×1080.

---

## Workflow with Claude

The connector lets Claude:
- **Read** the live scene (object names, collections, transforms)
- **Execute** Python in Blender's interpreter (`bpy` etc.)
- **Mutate** geometry, materials, modifiers, collections
- **Render** through `bpy.ops.render.render(write_still=True)`

Patterns that work well:

| You ask | Claude does |
|---|---|
| "Move the vapor chamber 5 mm forward" | locates `Cooling_VaporChamber`, mutates `.location.y`, optionally re-runs the fit assertions |
| "Are the blowers clipping the battery?" | reads bounding boxes of `Cooling_Blower_*` and `Battery_Cell_*`, computes overlap, reports |
| "Generate a cross-section through SoC and battery" | adds a Boolean modifier with a slicing plane, renders to PNG |
| "Round the lower-chassis edges 1 mm" | applies a Bevel modifier to `Chassis_Lower*`, regenerates |
| "Bump the lid open 110°" | rotates lid + display objects about the rear hinge axis |
| "Export STEP for the chassis bodies only" | calls Blender's STEP exporter scoped to the Chassis collection (or hands off to Fusion via the Fusion connector) |

Treat `dimensions.py` as authoritative — when Claude makes a change worth keeping, it should also update `dimensions.py` and re-run `generate_starter_scene.py` rather than letting the `.blend` drift away from the script.

---

## What this is not

- **Not the production CAD model.** Final manufacturable geometry lives in Fusion / OnShape (`chassis/`). Blender owns *concept* and *visualization*.
- **Not a CFD mesh.** OpenFOAM consumes a STEP export of the relevant volumes — see [`sim/thermal/`](../../sim/thermal/).
- **Not a render farm.** One hero render at a time; throughput isn't the goal.

---

## Reference

- [Anthropic — Claude for Creative Work](https://www.anthropic.com/news/claude-for-creative-work) (April 2026 launch)
- [Official Blender connector tutorial](https://claude.com/resources/tutorials/using-the-blender-connector-in-claude)
- [Blender MCP server announcement](https://www.blender.org/lab/mcp-server/)
- [MCP.Directory walkthrough](https://mcp.directory/blog/claude-blender-connector-guide)
- [Antmicro's Blender + OpenFOAM render pipeline](https://antmicro.com/blog/2026/04/simulating-active-cooling-using-a-cfd-based-flow) — what mang0 follows for the thermal sim hand-off
