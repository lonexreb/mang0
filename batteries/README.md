# Batteries

4S pack, ~90 Wh target.

## Primary cell

**Amprius SiCore silicon-anode** when available in laptop format. SiCore launched at 450 Wh/kg with mass-production capability targeted Spring 2026.

## Fallback

**Molicel INR-21700-P50B** in 4S1P (5000 mAh × 4.2 V × 4 = 84 Wh).

## BMS

BQ77915 4S protector (carryover from anyon_e). Verify cell-balancing tolerance with new chemistry before accepting Amprius.

## Charging

Via BQ25713 in `power/`. 140 W USB-C PD EPR sink negotiated by TPS65987D.
