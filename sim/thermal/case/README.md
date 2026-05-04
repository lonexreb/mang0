# OpenFOAM case stub

Skeleton `chtMultiRegionFoam` case. Populate `0/`, `constant/`, `system/` per Antmicro's flow.

## Quickstart (when populated)

```bash
cd sim/thermal/case

# Mesh
blockMesh
snappyHexMesh -overwrite

# Solve (steady-state CHT)
chtMultiRegionFoam

# Inspect
paraFoam &
```

## Reference flow

Antmicro's [April 2026 active-cooling pipeline](https://antmicro.com/blog/2026/04/simulating-active-cooling-using-a-cfd-based-flow) is the canonical reference. Their case structure is recommended unchanged.

## Region structure

```
constant/
├── regionProperties        # lists solid + fluid regions
├── air/                    # fluid region — turbulence, transport, polyMesh
├── chassis/                # solid — aluminum 6061-T6
├── vapor_chamber/          # solid — copper, modeled as high-k anisotropic
├── pcb_motherboard/        # solid — FR-4 + Cu layers averaged
├── strix_halo/             # solid + heat source 55 W
├── hailo/                  # solid + heat source 5 W
└── lpddr_pop/              # solid + heat source 10 W
```

## Don't commit

- `0.*/` time-step results (huge)
- `processor*/` decomposition
- `postProcessing/` paraview cache

These are in `.gitignore`. Track final results via image renders committed to `sim/thermal/results/`.
