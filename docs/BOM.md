# mang0 — bill of materials

Single-unit BOM, May 2026 pricing. Quantities for one laptop unless noted.

---

## Compute

| Part | Qty | Vendor | Approx unit | Notes |
|---|---|---|---|---|
| AMD Ryzen AI Max+ 395 ("Strix Halo", FP11 BGA) with on-package 128 GB LPDDR5X-8000 | 1 | AMD authorized distributor | $1,800–$2,400 | Allocation typically goes to OEMs first; budget extra lead time |
| Hailo-10H M.2 Key-M 2280 NPU module | 1 | Hailo direct or Mouser | $250 | Linux driver: closed kernel + open user-space |
| OpenTitan discrete chip (Nuvoton/zeroRISC) | 1 | zeroRISC early access program | $50–$150 | TPM 2.0 over SPI |

## Storage

| Part | Qty | Vendor | Approx unit | Notes |
|---|---|---|---|---|
| Samsung 990 PRO 2 TB NVMe (M.2 2280) | 2 | Anywhere | $180 | One OS+models, one user-swap |

## Display

| Part | Qty | Vendor | Approx unit | Notes |
|---|---|---|---|---|
| Samsung ATNA33TP11 13.3" 4K AMOLED (eDP) | 1 | Panelook | $400 | v1 carryover; swap to tandem OLED when 13.3" ships |
| IPEX 20455-040E eDP 40-pin connector | 2 | Digi-Key | $4 | One on motherboard, one on panel-side flex |

## Memory

(Memory is on-package with Strix Halo — no external DIMMs.)

## Wireless

| Part | Qty | Vendor | Approx unit | Notes |
|---|---|---|---|---|
| MediaTek MT7925 M.2 E-key WiFi 7 + BT 5.4 | 1 | AliExpress / Amazon | $30 | Preferred over Intel BE200 on AMD platforms |

## Power

| Part | Qty | Vendor | Approx unit | Notes |
|---|---|---|---|---|
| TI TPS65987DDH USB PD 3.1 EPR controller | 2 | Mouser | $4 | Replaces v1 HUSB238 for 140 W EPR |
| TI BQ25713 buck-boost charger | 1 | Mouser | $7 | v1 carryover |
| TI BQ77915 4S protector | 1 | Mouser | $3 | v1 carryover |
| ADI LTC2943 fuel gauge | 1 | Mouser | $9 | v1 carryover |
| TI TPS53676 multiphase controller (VDDCR_SOC) | 1 | Mouser | $8 | New for Strix Halo |
| TI TPS546B24 (VDD_MEM) | 1 | Mouser | $6 | LPDDR5X compliance |
| TI TPS62810 (VDD12 / aux rails) | 4 | Mouser | $1 | |
| TI TPS62870 (VDD09) | 1 | Mouser | $2 | |
| TI TPS563257 (VDD33 / VDD18) | 2 | Mouser | $0.80 | v1 carryover |
| Decoupling caps, inductors, MOSFETs | lot | Digi-Key | ~$40 | |

## Battery

| Part | Qty | Vendor | Approx unit | Notes |
|---|---|---|---|---|
| Amprius SiCore pouch cells (when in 13" laptop format) | 4 | Amprius / authorized | TBD | Until then, fall back to Molicel P50B 4S1P |
| Molicel INR-21700-P50B (fallback) | 4 | 18650batterystore | $8 | 5000 mAh @ 4.2 V |
| Battery balance flex + nickel strip | 1 | Local PCB shop | $20 | |

## Cooling

| Part | Qty | Vendor | Approx unit | Notes |
|---|---|---|---|---|
| Custom vapor chamber, 80 × 60 × 1.5 mm | 1 | Cooler Master OEM / NHC | $40 | 4-week lead time |
| Sunon MC35060V2-000U-A99 35×6 mm blower | 2 | Digi-Key / Mouser | $25 | |
| Honeywell PTM 7950 thermal pad (40×40 mm) | 2 | Amazon | $10 | Phase-change preferred over paste |

## I/O & connectors

| Part | Qty | Vendor | Approx unit | Notes |
|---|---|---|---|---|
| USB Type-C receptacle (USB4-rated, e.g. JAE DX07S024JJ2) | 2 | Digi-Key | $4 | |
| 3.5 mm headphone jack (CUI SJ-43514) | 1 | Digi-Key | $1 | |
| Status LEDs (5×, side-emitting) | 5 | Digi-Key | $0.30 | v1 carryover |

## Audio

| Part | Qty | Vendor | Approx unit | Notes |
|---|---|---|---|---|
| TI TPA2028D1 mono speaker amp | 1 | Mouser | $2 | v1 carryover |
| ST MP34DT06JTR digital MEMS mic | 4 | Mouser | $1.20 | Beamforming array |
| 2 W neodymium speaker driver | 2 | Knowles / DBL | $5 | |

## Sensors

| Part | Qty | Vendor | Approx unit | Notes |
|---|---|---|---|---|
| ST VL53L8 ToF (8×8 zone) | 1 | Mouser | $9 | Lid proximity |
| AMS TSL2591 ambient light | 1 | Mouser | $3 | |
| OmniVision OV5675 5 MP RGB camera + Pixart PAS6180 IR | 1 set | Arducam | $25 | Face wake on Hailo |

## Embedded controller

| Part | Qty | Vendor | Approx unit | Notes |
|---|---|---|---|---|
| ESP32-S3-WROOM-1U (8 MB flash) | 1 | Mouser | $4 | v1 carryover |

## Keyboard

| Part | Qty | Vendor | Approx unit | Notes |
|---|---|---|---|---|
| Nordic nRF52840 module | 1 | Mouser | $7 | v1 carryover |
| Cherry MX ULP switches | ~70 | Cherry direct | $1 | v1 carryover |
| TI BQ21040 LiPo charger | 1 | Mouser | $2 | v1 carryover |
| Keyboard battery (300 mAh LiPo) | 1 | Adafruit / SparkFun | $5 | v1 carryover |

## Trackpad

| Part | Qty | Vendor | Approx unit | Notes |
|---|---|---|---|---|
| Azoteq PXM0057 module | 1 | Mouser | $35 | v1 carryover; check stock — EOL'd |
| Glass top, machined to fit | 1 | Custom glass shop | $30 | |

## Chassis & mechanical

| Part | Qty | Vendor | Approx unit | Notes |
|---|---|---|---|---|
| Aluminum 6061-T6 billets | 2 | OnlineMetals | $40 | Lid + bottom |
| CNC machining service | 1 | Xometry / PCBWay 3D | $400 | 5-axis preferred |
| Type II anodize | 1 | Local anodizer | $60 | |
| Sugatsune lid hinge (pair) | 1 | Sugatsune | $30 | |
| M2 screws, threaded inserts | lot | McMaster-Carr | $20 | |

## Misc

| Part | Qty | Vendor | Approx unit | Notes |
|---|---|---|---|---|
| Antenna kit (WiFi + BT) | 1 | Digi-Key | $8 | |
| Display flex cable | 1 | Custom | $25 | |
| FFC cables (various pitches) | lot | Digi-Key | $15 | |
| 140 W USB-C PD charger (UGREEN Nexode 140W) | 1 | UGREEN | $90 | |

---

## Totals

| | Single unit | Batch of 5 |
|---|---|---|
| Compute | $2,100–$2,800 | $9,500 |
| Storage | $360 | $1,800 |
| Display | $410 | $1,800 |
| Power | $80 | $350 |
| Battery | $50 (fallback) | $250 |
| Cooling | $100 | $400 |
| I/O + audio + sensors + EC | $80 | $300 |
| Keyboard + trackpad | $150 | $750 |
| Chassis & mechanical | $550 | $2,200 |
| Misc | $140 | $500 |
| **Total parts** | **$4,020–$4,720** | **$17,850** |

PCBA fabrication adds ~$300/unit. Fully loaded one-off ≈ **$4,500**; small batch of 5 ≈ **$20,000**.

---

## Substitution policy

Document any substitution in `docs/changes/`. Verify electrical compatibility against the Strix Halo PDG and AMD reference design before swapping anything in the power tree or DDR path.
