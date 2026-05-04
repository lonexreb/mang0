# Electrical simulation runs

```bash
# Run all decks
for sp in *.sp; do
  ngspice -b "$sp" -o "${sp%.sp}.out"
done
```

## Decks

- `01-vddcr-soc-load-step.sp` — VDDCR_SOC undershoot/recovery under 80 A step (stub — needs TI TPS53676 SPICE model)
- *(more to come as schematic capture progresses)*

## Vendor models

Drop SPICE models from TI / ADI into `../models/` (gitignored if files are huge — track via DVC if needed). Keep model headers + license terms in `../models/SOURCES.md`.
