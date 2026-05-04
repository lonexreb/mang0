# Thermal

Vapor chamber + dual blower cooling for sustained 55 W package power.

## Why this is hard

Strix Halo at sustained AI-inference load draws ~55 W. The anyon_e v1 cooling solution will not survive this. Thermal is the single biggest mechanical change in mang0.

## Design

- **Vapor chamber**: ~80 × 60 × 1.5 mm, sintered wick, copper. Direct-touch the BGA top + Hailo-10H + LPDDR PoP via Honeywell PTM 7950.
- **Blowers**: 2 × Sunon MC35060V2-000U-A99 (35 × 6 mm), 5 V PWM + tach.
- **Exhaust**: rear and side vents in the bottom chassis.
- **Intake**: bottom grille, dust filter optional.

## Targets

| Workload | Steady-state package temp | Pass |
|---|---|---|
| Idle | <45 °C | |
| Single-thread | <80 °C | |
| All-core stress | <95 °C | |
| llama.cpp 70B sustained | <95 °C | |

## Validation

FLIR thermal under each workload, logged to CSV. Required before any unit ships.
