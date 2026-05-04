# Power

Power tree and PD 3.1 EPR sink for Strix Halo.

## What's different vs anyon_e

- **Multiphase VDDCR_SOC** (3-phase TPS53676 minimum) — Strix Halo SOC current can spike to 80 A
- **VDD_MEM** for LPDDR5X with tight 0.5 V VDDQ regulation
- **TPS65987DDH** USB PD 3.1 controllers replacing HUSB238 — required for 140 W EPR negotiation
- **PMBus telemetry** to EC on every rail for thermal-throttle decisions

## What's carryover from anyon_e

- BQ25713 buck-boost charger
- LTC2943 fuel gauge
- BQ77915 4S protector
- TPS563257 for 3.3 V / 1.8 V auxiliaries

## Reference

AMD Strix Halo Platform Design Guide (NDA, request via distributor). Power sequencing per the AMD timing diagram is non-negotiable — wrong sequence bricks the chip.

## Status

Schematic capture in progress.
