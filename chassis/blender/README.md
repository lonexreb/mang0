# Industrial design — Blender

Blender is the **primary mechanical sketch tool** for mang0. It owns the closed-lid envelope, internal component placement, and the visualization that feeds CFD ([`sim/thermal/`](../../sim/thermal/)) and FEA ([`sim/mechanical/`](../../sim/mechanical/)).

---

## Files

| File | What |
|---|---|
| [`dimensions.py`](./dimensions.py) | **Single source of truth** for every mechanical dimension. Importable by the scene script. Self-checks via fit assertions when run as a script. |
| [`generate_starter_scene.py`](./generate_starter_scene.py) | Idempotent Blender script that builds the parametric assembly: chassis, motherboard, SoC, NPU, NVMe, WiFi, vapor chamber, dual blowers, battery pack, trackpad, USB-C ports, lid + AMOLED panel. |
| `mang0.blend` *(generated, not committed)* | The working scene. Save in Blender or generate headlessly. |

---

## Setup

1. **Install Blender 4.2+** ([blender.org](https://www.blender.org/download/)).
2. **Sanity-check dimensions:**
   ```bash
   python3 chassis/blender/dimensions.py
   ```
   Should print the dimensional table and `ALL FITS OK`.
3. **Generate the scene:**
   - **GUI**: Blender → Scripting tab → Open `generate_starter_scene.py` → Run Script → save as `chassis/blender/mang0.blend` (gitignored).
   - **Headless**:
     ```bash
     blender --background --python chassis/blender/generate_starter_scene.py \
             --output-file chassis/blender/mang0.blend
     ```

---

## Scene structure

```
Collections:
├── Chassis      Lower shell (floor + 4 side walls), wall thickness 1.5 mm
├── Display      Lid shell + AMOLED panel
├── Motherboard  PCB + Strix Halo SoC + Hailo-10H + NVMe + WiFi 7
├── Cooling      Vapor chamber + 2 blowers
├── Battery      4 pouch cells in 2×2 grid
└── Input        Trackpad glass + USB-C port openings
```

Materials are pre-set so each subsystem renders distinctly: anodized aluminum for chassis, FR-4 green for PCB, copper for vapor chamber, dark silicon for BGA, blue PCB for daughter modules, glass for trackpad, near-black AMOLED. Three-point lighting + hero camera, Cycles 1920×1080.

---

## Discipline

`dimensions.py` is authoritative. Any scene edit worth keeping should also update `dimensions.py` so the script and the `.blend` don't drift. Re-run `generate_starter_scene.py` after dimension changes to refresh the scene from source.

---

## What this is not

- **Not the production CAD model.** Final manufacturable geometry lives in Fusion / OnShape (`chassis/`). Blender owns *concept* and *visualization*.
- **Not a CFD mesh.** OpenFOAM consumes a STEP export of the relevant volumes — see [`sim/thermal/`](../../sim/thermal/).
- **Not a render farm.** One hero render at a time; throughput isn't the goal.
