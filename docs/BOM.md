# mang0 — bill of materials

Single-unit BOM with **live vendor links and May 2026 pricing**. All prices in USD. Quantities for one laptop unless noted.

> **Status legend:**
> - 🟢 in-stock at named vendor as of May 2026
> - 🟡 limited / multi-channel sourcing required
> - 🔴 OEM-only, partnership or harvest required

---

## 1. Compute (the long pole)

### Strix Halo SoC + 128 GB on-package memory

The Ryzen AI Max+ 395 BGA is **not generally sold standalone in the West**. AMD distributes through OEMs. Three sourcing paths, in increasing pain:

| Path | Vendor | Unit price | Notes | Status |
|---|---|---|---|---|
| **A — buy a Framework Desktop, harvest** (recommended) | [Framework Desktop, 128 GB](https://frame.work/desktop) | **$1,999** | 4.5 L Mini-ITX with Strix Halo + 128 GB LPDDR5X-8000 on-package. Designed for repairability — pull the mainboard, repurpose for laptop. Strix Halo Wiki has [teardown notes](https://strixhalo.wiki/Hardware/PCs/Framework_Desktop). | 🟢 |
| **B — GMKtec mini PC, harvest** | [GMKtec EVO-X2 AI 128 GB](https://www.gmktec.com/products/amd-ryzen%E2%84%A2-ai-max-395-evo-x2-ai-mini-pc) (also [Amazon](https://www.amazon.com/GMKtec-ryzen_ai_mini_pc_evo_x2/dp/B0F53MLYQ6)) | **~$1,499–$1,999** | Cheaper than Framework but Mini-PC PCB is harder to repurpose. | 🟢 |
| **C — bare BGA via Chinese channels** | [VideoCardz coverage](https://videocardz.com/newz/amd-ryzen-ai-max-strix-halo-processors-now-available-for-standalone-purchase-in-china) | **~$550** | Standalone BGA available in China since May 2025. No memory on-package — you'd need separate LPDDR5X. Practically only viable if you have a forwarding agent and accept supply-chain risk. | 🟡 |

**Recommendation: Path A.** $1,999 buys you a SoC + 128 GB LPDDR5X validated together, plus a working reference design to debug against. Cheapest *de-risked* route.

### Discrete NPU

| Part | Vendor | Unit | Notes | Status |
|---|---|---|---|---|
| Hailo-10H M.2 Key-M 2280 | [Hailo direct](https://hailo.ai/products/ai-accelerators/hailo-10h-m-2-ai-acceleration-module/) · [Geniatech AIM-M-H10](https://www.geniatech.com/product/aim-m-h10/) · [Revinetech](https://revinetech.com/product/73/hailo-10h-m2-generative-ai-acceleration-module) · [community ordering thread](https://community.hailo.ai/t/where-to-buy-hailo-10h-m-2-pci-card/18853) | **~$249** | 40 TOPS INT4, <5 W. PCIe Gen 3 x4. Mouser/DigiKey don't stock yet — order direct or via the partners above. | 🟢 |

### Secure element

| Part | Vendor | Unit | Notes | Status |
|---|---|---|---|---|
| OpenTitan discrete RoT | [zeroRISC early access](https://zerorisc.com/) · [Nuvoton announcement](https://www.eetimes.com/nuvoton-zerorisc-release-opentitan-based-secure-silicon/) | **$50–$150** | First commercial open-source silicon RoT. SPI/I²C TPM 2.0. EAP gating expected to lift 2026. | 🟡 |

---

## 2. Storage

| Part | Vendor | Unit | Notes | Status |
|---|---|---|---|---|
| Samsung 990 PRO 2 TB NVMe (M.2 2280) | [Samsung direct (heatsink)](https://www.samsung.com/us/memory-storage/nvme-ssd/990-pro-pcie-4-0-nvme-ssd-1tb-sku-mz-v9p2t0b-am/) · [Newegg](https://www.newegg.com/samsung-2tb-990-pro-nvme-2-0/p/N82E16820147861) · [Amazon](https://www.amazon.com/SAMSUNG-Internal-Expansion-MZ-V9P2T0B-AM/dp/B0BHJJ9Y77) · [PCPartPicker](https://pcpartpicker.com/product/34ytt6/samsung-990-pro-2-tb-m2-2280-pcie-40-x4-nvme-solid-state-drive-mz-v9p2t0bw) | **$160–$220** (volatile in 2026) | Buy ×2: one for OS+models, one user-swappable. Watch [camelcamelcamel price history](https://camelcamelcamel.com/product/B0BHJJ9Y77) — swung $160–$580 in 2026. | 🟢 |

---

## 3. Display

| Part | Vendor | Unit | Notes | Status |
|---|---|---|---|---|
| Samsung ATNA33TP11 13.3" 4K AMOLED | [Panelook listing](https://www.panelook.com/ATNA33TP11_Samsung_13.3_OLED_inventory_59424.html) · [BlissComputers](https://www.blisscomputers.net/samsung-atna33tp11-1-13-3-4k-oled-screen-glossy-display-144558/) · [LPScreen](https://www.lpscreen.com/en_laptop/for-atna33tp11-1-uhd-4k-3840x2160-13-3-amoled-display.html) · [YourITech](https://www.youritech.com/products/atna33tp11-samsung-13-3-inch-amoled-display-3840x2160-edp-oled-display.html) | **~$200–$400** | eDP 1.4b, 40-pin IPEX 20455-040E. Carryover from anyon_e. | 🟢 |
| IPEX 20455-040E eDP 40-pin connector | [DigiKey](https://www.digikey.com/en/products/filter/ffc-fpc-flat-flexible-connectors/313) (search 20455-040E) | **~$3.50** | Qty 2 (board + flex side). | 🟢 |

---

## 4. Wireless

| Part | Vendor | Unit | Notes | Status |
|---|---|---|---|---|
| MediaTek MT7925 M.2 E-key WiFi 7 + BT 5.4 | [Amazon B0F4D8TCFP](https://www.amazon.com/Network-5400Mbps-Bluetooth-Wireless-Adapter/dp/B0F4D8TCFP) · [Amazon QHUDLV B0D46XYBTH](https://www.amazon.com/QHUDLV-Wireless-Wireless-AC-802-11ax-802-11ac/dp/B0D46XYBTH) · [524 WiFi (AzureWave AW-EB600NF)](https://524wifi.net/product/mediatek-mt7925-aw-eb600nf-wifi-7-802-11be-2x2-triband-client-m-2-ae-key-module-bt-v5-4-ble-azurewave/) · [eBay](https://www.ebay.com/itm/276634655267) · AliExpress (search MT7925) | **$16–$25** | Tri-band 5400 Mbps. Preferred over Intel BE200 on AMD platforms. | 🟢 |
| Antenna pair (WiFi + BT, U.FL pigtail) | [DigiKey](https://www.digikey.com/) (search "WiFi 7 antenna U.FL") | **~$8** | | 🟢 |

---

## 5. Power tree

All TI parts available at [Mouser](https://www.mouser.com/) and [DigiKey](https://www.digikey.com/) — search by exact part number.

| Part | Function | Mouser link | Unit | Status |
|---|---|---|---|---|
| TI **TPS65987DDH** | USB-PD 3.1 EPR controller (replaces v1's HUSB238) | [Mouser TPS65987DDHRSHR](https://www.mouser.com/c/?q=TPS65987DDH) | **~$4** | 🟢 |
| TI **BQ25713** | Buck-boost charger (v1 carryover) | [Mouser BQ25713 series](https://www.mouser.com/new/Texas-Instruments/ti-bq25710-bq25713-bq25713b/) | **~$7** | 🟢 |
| TI **BQ77915** | 4S cell protector (v1 carryover) | [Mouser](https://www.mouser.com/) (search BQ77915) | **~$3** | 🟢 |
| ADI **LTC2943** | Coulomb-counter fuel gauge | [Mouser](https://www.mouser.com/) (search LTC2943) | **~$9** | 🟢 |
| TI **TPS53676** | 3-phase VDDCR_SOC controller | [Mouser](https://www.mouser.com/) (search TPS53676) | **~$8** | 🟢 |
| TI **TPS546B24** | VDD_MEM (LPDDR5X compliance) | [Mouser](https://www.mouser.com/) (search TPS546B24) | **~$6** | 🟢 |
| TI **TPS62810** | Aux rails | [Mouser](https://www.mouser.com/) (search TPS62810) | **~$1** ×4 | 🟢 |
| TI **TPS62870** | VDD09 | [Mouser](https://www.mouser.com/) (search TPS62870) | **~$2** | 🟢 |
| TI **TPS563257** | VDD33/VDD18 (v1 carryover) | [Mouser](https://www.mouser.com/) (search TPS563257) | **~$0.80** ×2 | 🟢 |
| Decoupling caps, MOSFETs, inductors | [DigiKey](https://www.digikey.com/) | **~$40** lot | 🟢 |

---

## 6. Battery

| Part | Vendor | Unit | Notes | Status |
|---|---|---|---|---|
| Amprius SiCore silicon-anode (laptop format) | [Amprius direct](https://amprius.com/) | TBD | Mass-production capability targeted Spring 2026 per Amprius press; verify SKU before BOM lock. | 🔴 |
| **Fallback:** Molicel INR-21700-P50B (×4 for 4S1P) | [18650 Battery Store](https://www.18650batterystore.com/products/molicel-21700-p50b-5000mah-50a-battery) (authorized) · [Liion Wholesale](https://liionwholesale.com/products/molicel-npe-inr-21700-p50b-60a-5000mah-flat-top-21700-battery-authorized-distributor) (authorized) · [IMR Batteries](https://imrbatteries.com/products/molicel-21700-p50b-5000mah-60a-battery) · [Battery Junction](https://www.batteryjunction.com/molicel-inr21700-p50b) | **~$8–$12 ea** ($32–$48 for 4S1P) | 5000 mAh × 4.2 V × 4 = 84 Wh. Buy from authorized only (counterfeits exist). | 🟢 |
| Battery balance flex + nickel strip | Local PCB shop / [BatteryHookup](https://batteryhookup.com/) | **~$20** | | 🟢 |

---

## 7. Cooling

| Part | Vendor | Unit | Notes | Status |
|---|---|---|---|---|
| Custom vapor chamber, 80 × 60 × 1.5 mm | Cooler Master OEM (request quote) · [NHC](https://www.nhcrl.com/) | **~$40** | 4-week lead time typical | 🟡 |
| Sunon 35×6 mm blower (MF35060V1-1000U-A99 — substitute, MC35060V2 spec'd in v1 not on DigiKey) | [DigiKey 8283924](https://www.digikey.com/en/products/detail/sunon-fans/MF35060V1-1000U-A99/8283924) | **~$25** ×2 | Note: substitute the available variant; spec was MC35060V2-000U-A99 but only the MF series is currently DigiKey-stocked. | 🟢 |
| Honeywell PTM 7950 thermal pad (40×40 mm) | [Amazon](https://www.amazon.com/) (search PTM 7950 40x40) | **~$10** ×2 | Phase-change, much better than paste for BGA. | 🟢 |

---

## 8. I/O & connectors

| Part | Vendor | Unit | Notes | Status |
|---|---|---|---|---|
| USB Type-C receptacle, USB4-rated (JAE DX07S024JJ2) | [DigiKey](https://www.digikey.com/) (search DX07S024JJ2) | **~$4** ×2 | | 🟢 |
| 3.5 mm headphone jack (CUI SJ-43514) | [DigiKey](https://www.digikey.com/) (search SJ-43514) | **~$1** | | 🟢 |
| Status LEDs (5×, side-emitting) | [DigiKey](https://www.digikey.com/) | **~$0.30** ×5 | v1 carryover | 🟢 |

---

## 9. Audio

| Part | Vendor | Unit | Notes | Status |
|---|---|---|---|---|
| TI TPA2028D1 mono speaker amp | [Mouser](https://www.mouser.com/) (search TPA2028D1) | **~$2** | v1 carryover | 🟢 |
| ST MP34DT06JTR digital MEMS mic | [Mouser](https://www.mouser.com/) (search MP34DT06JTR) | **~$1.20** ×4 | Beamforming array | 🟢 |
| 2 W neodymium speaker driver | [Knowles](https://www.knowles.com/) · [DBL](https://www.dblelectronics.com/) · [Adafruit](https://www.adafruit.com/category/61) | **~$5** ×2 | | 🟢 |

---

## 10. Sensors

| Part | Vendor | Unit | Notes | Status |
|---|---|---|---|---|
| ST VL53L8 ToF (8×8 zone) | [Mouser](https://www.mouser.com/) (search VL53L8CXV0GC) | **~$9** | Lid proximity / wake | 🟢 |
| AMS TSL2591 ambient light | [Mouser](https://www.mouser.com/) (search TSL2591) · [Adafruit breakout](https://www.adafruit.com/product/1980) | **~$3** (chip) / $7 (breakout) | | 🟢 |
| OmniVision OV5675 5 MP RGB camera + IR | [Arducam](https://www.arducam.com/) (search OV5675) | **~$25 set** | Face wake on Hailo, not SoC | 🟢 |

---

## 11. Embedded controller & keyboard

| Part | Vendor | Unit | Notes | Status |
|---|---|---|---|---|
| ESP32-S3-WROOM-1U module (8 MB flash) | [Mouser](https://www.mouser.com/c/embedded-solutions/engineering-tools/?q=ESP32-S3-WROOM-1U) · [DigiKey](https://www.digikey.com/) (search ESP32-S3-WROOM-1U) | **~$4** | v1 carryover | 🟢 |
| Nordic nRF52840 module | [Mouser](https://www.mouser.com/) (search nRF52840) | **~$7** | v1 keyboard carryover | 🟢 |
| Cherry MX ULP tactile switches (×~70) | [Mechbox UK](https://mechbox.co.uk/products/cherry-mx-ulp-tactile-switch-sample) (samples) · [keeb.supply](https://keeb.supply/products/cherry-mx-ulp) · [Cherry direct](https://www.cherry.de/en-gb/product/mx-ulp-tactile) · [pashutk/Cherry_MX_ULP repo](https://github.com/pashutk/Cherry_MX_ULP) for KiCad footprints + purchase links | **£1.99 / ~$2.50 ea** (sample); bulk ~$1 ea via Cherry direct | v1 carryover | 🟡 |
| TI BQ21040 LiPo charger (keyboard) | [Mouser](https://www.mouser.com/) (search BQ21040) | **~$2** | v1 carryover | 🟢 |
| Keyboard battery (300 mAh LiPo) | [Adafruit](https://www.adafruit.com/product/1578) · [SparkFun](https://www.sparkfun.com/categories/54) | **~$5** | v1 carryover | 🟢 |

---

## 12. Trackpad

| Part | Vendor | Unit | Notes | Status |
|---|---|---|---|---|
| Azoteq PXM0057 | [Mouser](https://www.mouser.com/) (verify stock — EOL'd 2024) · [Azoteq direct](https://www.azoteq.com/) | **~$35** | EOL warning — investigate PXM00xx successor before BOM lock | 🔴 |
| Glass top, machined to fit | Custom glass shop (e.g. [Schott](https://www.schott.com/)) | **~$30** | | 🟢 |

---

## 13. Chassis & mechanical

| Part | Vendor | Unit | Notes | Status |
|---|---|---|---|---|
| Aluminum 6061-T6 billets (lid + bottom) | [OnlineMetals](https://www.onlinemetals.com/) | **~$40** | | 🟢 |
| 5-axis CNC machining service | [Xometry](https://www.xometry.com/) · [PCBWay 3D printing/CNC](https://www.pcbway.com/rapid-prototyping/manufacture/) · [SendCutSend](https://sendcutsend.com/) | **~$400** (1-off) | | 🟢 |
| Type II anodize | Local anodizer | **~$60** | | 🟢 |
| Sugatsune lid hinge (pair) | [Sugatsune America](https://www.sugatsune.com/) | **~$30** | | 🟢 |
| M2 screws + threaded inserts | [McMaster-Carr](https://www.mcmaster.com/) | **~$20 lot** | | 🟢 |

---

## 14. Charger / external

| Part | Vendor | Unit | Notes | Status |
|---|---|---|---|---|
| 140 W USB-C PD 3.1 EPR charger | [UGREEN Nexode 140W direct](https://www.ugreen.com/products/ugreen-nexode-140w-usb-c-charger) · [Amazon](https://www.amazon.com/) (search UGREEN 140W) | **~$90** | | 🟢 |

---

## Totals

| Category | Single unit (Path A) | Batch of 5 |
|---|---|---|
| Compute (Framework Desktop $1,999 + Hailo $249 + OpenTitan $100) | **$2,348** | $11,250 |
| Storage (2× 990 PRO @ $180) | $360 | $1,800 |
| Display | $250 | $1,200 |
| Wireless | $25 | $125 |
| Power tree | $80 | $350 |
| Battery (fallback Molicel) | $50 | $250 |
| Cooling | $100 | $400 |
| I/O + audio + sensors + EC | $80 | $300 |
| Keyboard + trackpad | $150 | $750 |
| Chassis & mechanical | $550 | $2,200 |
| Charger | $90 | $450 |
| **Subtotal parts** | **$4,083** | **$19,075** |
| PCBA fabrication (5 boards × $300/board) | $1,500 | $4,500 |
| **TOTAL** | **~$5,583** | **~$23,575** |

> **Reality check:** the v1 anyon_e BOM was ~$1,500 in parts. mang0 is ~3.7× the cost, almost entirely driven by the Strix Halo + 128 GB memory. Without that, you're back at v1's price; with it, you have a laptop that runs 70B-parameter LLMs locally. Choose accordingly.

---

## Substitution policy

Document any substitution in `docs/changes/`. Verify electrical compatibility against the [AMD Strix Halo PDG](https://www.amd.com/) (request via authorized distributor under NDA) before swapping anything in:
- the power tree (wrong sequence bricks the chip)
- the DDR path (LPDDR5X compliance is tight)
- the USB4 / PCIe / eDP high-speed lanes (impedance + length-match)

Lower-stakes subs (caps, LEDs, status indicators, hinge brand) need only a one-line entry in `docs/changes/`.

---

## Sourcing notes

- **Mouser vs DigiKey**: roughly equivalent stock for TI/ST/ADI parts. Mouser tends slightly cheaper on small qty; DigiKey has better per-part datasheet links.
- **Hailo-10H**: not on Mouser/DigiKey as of May 2026. Order direct from Hailo or via Geniatech/Revinetech.
- **Strix Halo**: AMD allocation gates this. Path A (Framework Desktop harvest) is the only path that works without OEM channel access.
- **OpenTitan**: zeroRISC's early-access program is gated. Apply early — lead time is the limiting factor, not price.
- **Cherry MX ULP**: Cherry sells individual switches reluctantly. Sample channels (Mechbox, keeb.supply) are best for prototyping; bulk requires Cherry direct.
- **Vapor chamber**: 4-week minimum lead time. Order before you start motherboard layout.

---

## Sources

- [Strix Halo standalone BGA in China — VideoCardz](https://videocardz.com/newz/amd-ryzen-ai-max-strix-halo-processors-now-available-for-standalone-purchase-in-china)
- [Framework Desktop pricing & review — Tom's Hardware](https://www.tomshardware.com/desktops/gaming-pcs/framework-desktop-review)
- [Framework Desktop teardown — Strix Halo Wiki](https://strixhalo.wiki/Hardware/PCs/Framework_Desktop)
- [Best mini PCs for local LLMs in 2026 — TerminalBytes](https://terminalbytes.com/best-mini-pc-for-local-llm-2026/)
- [Hailo-10H product page — Hailo](https://hailo.ai/products/ai-accelerators/hailo-10h-m-2-ai-acceleration-module/)
- [OpenTitan commercial silicon — EE Times](https://www.eetimes.com/nuvoton-zerorisc-release-opentitan-based-secure-silicon/)
- [Samsung 990 PRO 2 TB price history — camelcamelcamel](https://camelcamelcamel.com/product/B0BHJJ9Y77)
- [ATNA33TP11 panel page — Panelook](https://www.panelook.com/ATNA33TP11_Samsung_13.3_OLED_overview_59424.html)
- [MT7925 WiFi 7 modules — CNX Software](https://www.cnx-software.com/2024/12/30/wifi-7-access-point-and-client-m-2-modules/)
- [Cherry MX ULP resource repo — pashutk/Cherry_MX_ULP](https://github.com/pashutk/Cherry_MX_ULP)
- [Sunon DC blower catalog — DigiKey datasheet](https://media.digikey.com/pdf/data%20sheets/sunon%20pdfs/maglev%20catalog.pdf)
- [Molicel P50B authorized distributor — Liion Wholesale](https://liionwholesale.com/products/molicel-npe-inr-21700-p50b-60a-5000mah-flat-top-21700-battery-authorized-distributor)
- [Amprius SiCore 450 Wh/kg launch](https://amprius.com/amprius-launches-sicore-450-wh-kg-high-energy-cell-with-near-term-mass-production-capability-to-scale/)

*Pricing snapshot: May 2026. Volatility warning on Samsung 990 PRO and on Strix Halo systems — recheck before ordering.*
