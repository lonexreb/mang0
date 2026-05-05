# mang0 — supply chain

Lead-time-aware procurement schedule. Pairs with [`ROADMAP.md`](./ROADMAP.md) (timeline) and [`BOM.md`](./BOM.md) (line-item BOM with vendor links).

> **Cart-ready.** Every link below points to a product page where you can put a single unit in cart and check out. Where multiple vendors are listed, prefer the first; second is the fallback.

---

## TL;DR ordering schedule

| Week | Vendor cart | Cost | Why this week |
|---|---|---|---|
| 1 (Mon) | Framework Desktop | $1,999 | 1–3 day shipping, blocks teardown |
| 1 (Mon) | Vapor-chamber vendor (Cooler Master OEM / NHC) | $40 | **4-week lead — hard floor** |
| 1 (Mon) | Hailo direct | $249 | 1–2 weeks variable, order early |
| 1 (Tue) | Panelook / BlissComputers | $300 | International shipping ~2 wk |
| 1 (Tue) | zeroRISC OpenTitan EAP application | $0 | Application, not order. May not arrive in time |
| 1 (Tue) | AMD PDG access application | $0 | Application via distributor — non-blocking for v1 |
| 4 | Tools (one cart, see `INSTRUMENTS.md`) | $1,800 | Must be on bench by week 11 |
| 8 (Mon) | JLCPCB | $120 | 5 designs × 5 boards |
| 8 (Mon) | Mouser/DigiKey parts cart | $300 | Components for PCBA |
| 8 (Wed) | Xometry / SendCutSend | $400 | Chassis CNC, 1–2 wk |
| 8 (Wed) | Local anodizer | $60 | Type II, ~1 wk |
| 9 | 18650 Battery Store / Liion Wholesale | $50 | Authorized cells |
| 9 | DigiKey misc | $100 | Speaker drivers, mics, sensors, antennas |
| 11 | Solder paste, flux, consumables | $50 | Bring-up |

**Weekly cumulative budget:** see [`ROADMAP.md` §Budget](./ROADMAP.md#budget-by-week-cumulative-cash-outlay). Total ~$6,000 (parts + tools), ~$4,200 if you already own tools.

---

## Week 1 — long-pole orders (the only orders that gate the whole project)

### 1.1 Framework Desktop 128 GB ($1,999) — Monday morning

- **[Framework Desktop, AMD Ryzen AI Max+ 395, 128 GB](https://frame.work/desktop)**
- Configure: 128 GB unified memory, no SSD (you'll use Samsung 990 PRO from your own order), no OS
- Shipping: 1–3 days standard
- **What it gives you**: validated Strix Halo + LPDDR5X compute brain + reference open-hardware mainboard schematics
- Backup: [GMKtec EVO-X2 AI 128 GB](https://www.gmktec.com/products/amd-ryzen%E2%84%A2-ai-max-395-evo-x2-ai-mini-pc) if Framework allocation slips

### 1.2 Vapor chamber ($40, 4-WEEK LEAD) — Monday morning, do not skip

This is the **hard floor** of the schedule. Order day 1 or you slip.

- Spec: ~80 × 60 × 1.5 mm copper, sintered wick. Direct-touch heat input on one face.
- **[Cooler Master OEM RFQ form](https://www.coolermaster.com/contact/)** — request "vapor chamber sample for laptop dev project, 80×60×1.5 mm, 1 unit"
- Backup: [NHC (Nordic Heat-Chamber) sample order](https://www.nhcrl.com/) — same spec
- Both are sample-friendly; expect a quote email within 1 business day, then 4-week fab.
- Backup-backup: source a "thin laptop heat pipe + heat spreader" stack from Mouser if vapor chamber fully unavailable. Lower performance, but at least available.

### 1.3 Hailo-10H M.2 ($249) — Monday morning

- **[Hailo-10H M.2 product page](https://hailo.ai/products/ai-accelerators/hailo-10h-m-2-ai-acceleration-module/)** — order via "request quote" button
- Backup: [Geniatech AIM-M-H10](https://www.geniatech.com/product/aim-m-h10/) (same module, different distributor)
- Backup-backup: [Revinetech](https://revinetech.com/product/73/hailo-10h-m2-generative-ai-acceleration-module)
- Lead time: 1–2 weeks, variable

### 1.4 Display panel ($300) — Tuesday

- **[Panelook ATNA33TP11 listing](https://www.panelook.com/ATNA33TP11_Samsung_13.3_OLED_inventory_59424.html)** — multiple suppliers, pick lowest-shipping
- Backup: [BlissComputers](https://www.blisscomputers.net/samsung-atna33tp11-1-13-3-4k-oled-screen-glossy-display-144558/) (US warehouse, faster)
- Backup-backup: [LPScreen](https://www.lpscreen.com/en_laptop/for-atna33tp11-1-uhd-4k-3840x2160-13-3-amoled-display.html)
- 1–2 weeks international

### 1.5 OpenTitan EAP application — Tuesday

- **[zeroRISC early access program](https://zerorisc.com/)** — fill the EAP form
- $0 to apply; if accepted, Nuvoton chip pricing is $50–$150
- May not arrive in time for week-12 integration. **Mitigation:** ship v1 without OpenTitan, retrofit when chip arrives. The v1 firmware must boot without it.

### 1.6 AMD PDG access — Tuesday

- Apply via authorized AMD distributor (Avnet, Arrow, Future Electronics)
- Required only for v2 escalation (fully custom Strix Halo mainboard)
- 2–6 weeks response time; may not arrive
- v1 doesn't need this — Framework's open mainboard schematics + their public Embedded reference cover ~80% of what PDG would tell you

---

## Week 4 — bench instruments (one cart, $1,800)

See [`INSTRUMENTS.md`](./INSTRUMENTS.md) for the full bench-tools list. Key insight: **order in week 4, not week 8**. Used Rigol scopes from eBay can take 2 weeks; new microscopes 1–2 weeks; everything must be on your bench by week 11.

---

## Week 8 — fab + parts (~$1,500 cart, three vendors)

### 8.1 JLCPCB ($120)

- 5 designs × 5 boards each = 25 PCBs
- Standard lead time (5 business days fab) + DHL Express (3 day ship) = 1.5 weeks total
- Use **JLCPCB Standard Assembly** for any board with >20 SMD parts; consigned parts for the rest
- **[JLCPCB capabilities + pricing](https://jlcpcb.com/capabilities/pcb-capabilities)**

### 8.2 Mouser parts cart (~$300)

Single cart for entire PCBA, paste this into Mouser's "Quick Cart" with quantities:

```
TPS65987DDHRSHR    1   (PD 3.1 controller)
BQ25713RSNT        1   (charger)
BQ77915DPJT        1   (4S protector)
LTC2943IDD-PBF     1   (gauge)
TPS53676RSBR       1   (multiphase VDDCR)
TPS546B24QRVFRQ1   1   (VDD_MEM)
TPS62810QWRWYRQ1   4   (aux rails)
TPS62870QWRYRRQ1   1   (VDD09)
TPS563257DDCR      2   (VDD33/18)
ESP32-S3-WROOM-1U-N8  1
TPA2028D1YZFR      1   (audio amp)
MP34DT06JTR        4   (mic array)
VL53L8CXV0GC/1     1   (ToF)
TSL2591FN          1   (ambient)
DX07S024JJ2        2   (USB-C receptacle)
SJ-43514           1   (3.5mm jack)
```

Plus: passives kit (0402 caps, resistors, ferrites), MOSFETs, inductors — see `BOM.md` lots.

**Single Mouser cart link**: [mouser.com/cart](https://www.mouser.com/cart/) (paste BOM CSV from `kicad-cli pcb export bom`)

### 8.3 Xometry CNC ($400)

- Upload `chassis/blender/mang0.blend` STEP export to **[Xometry instant quote](https://get.xometry.com/instant-quote-create)**
- Material: 6061-T6 aluminum, 5-axis preferred
- Finish: as-machined (anodize handled separately by local anodizer to control color/quality)
- Alternative: [SendCutSend](https://sendcutsend.com/) for laser-cut + bend variant if you want to skip CNC

### 8.4 Local anodizer ($60)

- Type II, matte black or natural
- 1-week turn typical
- Hand off after Xometry chassis arrives (week 9–10)

---

## Week 9 — battery + speakers + sensors (~$150)

### 9.1 Cells

- **[Liion Wholesale Molicel P50B (authorized)](https://liionwholesale.com/products/molicel-npe-inr-21700-p50b-60a-5000mah-flat-top-21700-battery-authorized-distributor)** — buy ×4 ($32–$48)
- *Note: switch to 2×2 pouch arrangement per `chassis/blender/dimensions.py` — pouches don't fit a 16 mm laptop in 4S1P. ROADMAP and chassis updates needed if cells are 21700 cylindrical.*

### 9.2 Audio drivers, antennas, FFC cables

- 2 W speaker driver: [Adafruit](https://www.adafruit.com/category/61) — $10
- WiFi 7 antennas: [DigiKey "WiFi 7 antenna U.FL"](https://www.digikey.com/) — $8 pair
- FFC cables (display 40-pin, plus various small): [DigiKey](https://www.digikey.com/) — $20 lot
- Speaker enclosure 3D-print filament: PETG, $25 for a roll

---

## Week 11 — bring-up consumables ($50)

- Solder paste: ChipQuik SMD291AX10 ($15)
- Flux pen: ChipQuik (for hand rework) ($8)
- IPA + ESD-safe wipes ($15)
- Kapton tape ($6)
- Heat-shrink kit ($6)

All available on Amazon for next-day delivery.

---

## Cancellation policy (in case the project pauses)

The only orders you can't cancel cheaply:
- **Vapor chamber** (custom fab, locked once they cut wick): non-refundable after week 1 day 3
- **CNC chassis** (custom): non-refundable after upload acceptance
- **PCBA fab + assembly** (custom): non-refundable after gerber upload

Everything else is returnable within 30 days. Plan your decision points (Roadmap §Decision points) **before** these locks-in if you have any doubt.

---

## What you do NOT order

Listed for clarity:

- **Strix Halo BGA standalone** — not viable for v1, scope is "harvest Framework Desktop mainboard"
- **AMD PDG documents under NDA** — application only, no parts. v1 doesn't need them
- **OS license** — NixOS / Fedora are free
- **Coreboot ROM** — built from source, no purchase
- **AI models** — pulled from Ollama, no purchase
