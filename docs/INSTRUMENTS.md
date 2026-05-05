# mang0 — bench instruments

What needs to be on your bench by **Week 11** (bring-up). Order in **Week 4** of the [`ROADMAP.md`](./ROADMAP.md) — used Rigol scopes from eBay can take 2 weeks, microscopes 1–2 weeks.

Three tiers. Pick one and stick with it. Mixing tiers is fine; sandbagging on the scope or DMM is not (you will fight bring-up problems with bad data).

---

## Tier 0 — bare minimum ($1,000)

You can bring up mang0 with this. Tight margins, slow debugging, but works.

| Tool | Purpose | Vendor | Price |
|---|---|---|---|
| Pinecil V2 soldering iron | Hand soldering, fine-pitch | [Pine Store](https://pine64.com/product/pinecil-smart-mini-portable-soldering-iron/) | $30 |
| Quick 861DW hot-air rework station | QFN, BGA reflow, rework | [Amazon](https://www.amazon.com/) (search "Quick 861DW") | $250 |
| Brymen BM235 DMM | Continuity, rail voltage | [eevblog store](https://www.eevblog.com/product/bm235/) | $130 |
| Owon HDS272S 2-ch USB scope, 70 MHz | Eyeball signals; not enough for USB4 but fine for I²C/SPI/UART/PD | [Owon direct](https://www.owon.com.cn/) / [Amazon](https://www.amazon.com/) | $300 |
| DSLogic Plus 16-ch logic analyzer | I²C, SPI, eSPI, PD CC | [SparkFun](https://www.sparkfun.com/products/15036) | $150 |
| Riden RD6018 bench PSU, 60 V/18 A programmable | First power-up at low current limit | [AliExpress official](https://www.aliexpress.com/) (Riden) | $150 |

**Tier 0 total: $1,010.**

What you cannot do at this tier: real signal-integrity validation, BGA inspection, multi-channel timing analysis. You'll guess and check more.

---

## Tier 1 — recommended ($2,600) ✅

This is what `BUILD.md` §0.2 originally listed. Comfortable margin for first-time hardware bring-up.

| Tool | Purpose | Vendor | Price |
|---|---|---|---|
| Hakko FX-951 + T15 tip kit | Hand soldering, all-day comfortable | [Amazon](https://www.amazon.com/) (search Hakko FX-951) | $300 |
| Quick 861DW hot-air station | Rework | Amazon | $250 |
| AmScope SM-4TZ stereo microscope, 0.7–4.5× | Fine-pitch inspection, hand rework under scope | [AmScope direct](https://amscope.com/) | $600 |
| Brymen BM235 DMM | Quality DMM that won't lie to you | eevblog | $130 |
| Saleae Logic 8 | I²C/SPI/PD analysis with the best software in the field | [Saleae direct](https://www.saleae.com/) | $400 |
| Rigol DHO924 4-ch 250 MHz scope | Real scope. Catches everything you'll need for I²C/SPI/eSPI/PD/eDP. **Not** sufficient for USB4 SI but fine for first-pass SoC bring-up | [Rigol direct](https://www.rigolna.com/) | $700 |
| Rigol DP712 single-channel 30 V/2 A linear PSU | Clean rail probing | Rigol direct | $100 |
| 600 W reflow hotplate (e.g. Miniware MHP30 + extension) or toaster oven | BGA reflow, large board reflow | [Miniware direct](https://miniware.com.cn/) | $150 |

**Tier 1 total: $2,630.**

---

## Tier 2 — professional ($5,000+)

Skip unless you're already running a hardware lab.

| Tool | Why upgrade |
|---|---|
| Keysight DSOX1204G or InfiniiVision 1000-X (350 MHz, 4-ch) | Better noise floor; useful when first-pass scope tells you "something's wrong" but you can't see it |
| Tektronix TDS3054C used (500 MHz) | Equivalent vintage; sometimes cheaper used |
| Rigol DG992 AWG | Stimulus injection for SI testing |
| Hakko FR-301 desoldering gun | Through-hole desolder without lifting pads |
| Mantis stereoscope | Microscope upgrade if SM-4TZ isn't enough |
| ESI 1300 LCR meter | Inductor + cap characterization |

You don't need any of this for v1. Listed so you know what the upgrade path looks like.

---

## Already-have list (don't double-buy)

If you already own these, deduct from your tier:

- Soldering iron (any quality temp-controlled iron) — saves $30–$300
- Multimeter (Fluke 87V, Brymen, etc.) — saves $130
- 3D printer (you'll need one for jigs and the speaker enclosure prototype) — Bambu A1 / P1S $300–$700 if you don't have one
- USB scope (Analog Discovery 3, Saleae, Owon) — saves $300

---

## Consumables (separate from tools)

Order with the bring-up batch in week 11 ($50, see `SUPPLY-CHAIN.md` §11):

- Solder paste (ChipQuik SMD291AX10): $15
- Solder wire 0.5 mm (Kester 245): $20
- Flux pen (ChipQuik LF-FLUX): $8
- IPA 99% (1 L): $10
- Kapton tape (10 mm × 33 m): $6
- Heat-shrink assortment: $6
- ESD-safe tweezers (Vetus or Aven): $15
- Anti-static mat for the bench: $30

---

## Workspace

Not technically instruments but get them right or your week 11 falls apart:

- **Bench**: 1.2 × 0.6 m minimum, ESD mat, no carpet
- **Lighting**: a real overhead light + a focused arm light (e.g. BenQ ScreenBar). Scope inspection in dim light is misery
- **Ventilation**: solder fume extractor or open window + fan. Important
- **Storage**: a parts organizer with at least 60 bins for SMDs

Total bench setup: ~$200 if starting from zero.

---

## What this list does *not* cover

- IBIS-AMI signal-integrity simulators (Sigrity, HyperLynx) — six-figure software, only relevant for v2 fully-custom mainboard
- BGA X-ray (Glenbrook RTX-130) — $30K+, not worth it for a single-build project. JLCPCB inspects assembled boards before shipping
- Climate chamber for thermal validation — use FLIR ETS320 thermal camera ($800) instead, listed as Tier 2 optional in `BUILD.md` §5.3

---

## Order this together (Tier 1 single-cart approximation)

| Vendor | Items | Subtotal |
|---|---|---|
| [Amazon](https://www.amazon.com/) | Hakko FX-951, Quick 861DW, hotplate, ESD mat, lighting | ~$830 |
| [AmScope](https://amscope.com/) | SM-4TZ microscope | $600 |
| [eevblog store](https://www.eevblog.com/product/bm235/) | Brymen BM235 | $130 |
| [Saleae](https://www.saleae.com/) | Logic 8 | $400 |
| [Rigol direct](https://www.rigolna.com/) | DHO924 + DP712 | $800 |

Total ~$2,760. Order Monday of week 4. By week 6 everything is on the bench. Use weeks 6–10 to build muscle memory before bring-up week 11.
