# CLAUDE.md — mang0

Operating context for Claude Code working inside this repo.

---

## 1. What this repo is

**mang0** is the v2 of the [anyon_e](../laptop) open laptop, redesigned around 2026 silicon to be the first fully open, **UNIX-native, AI-native** laptop. It runs local 7B–120B LLMs on mainline Linux with no proprietary firmware in the boot path beyond the SoC's PSP.

- **Compute**: AMD Ryzen AI Max+ 395 "Strix Halo" — 16 Zen 5 + Radeon 8060S (40 RDNA 3.5 CUs) + XDNA 2 NPU 50 TOPS
- **Discrete NPU**: Hailo-10H M.2 (40 TOPS INT4, <5 W)
- **Memory**: 128 GB LPDDR5X-8000 unified, on-package
- **Security**: OpenTitan discrete RoT (TPM 2.0 over SPI)
- **Firmware**: coreboot + edk2 payload
- **OS**: NixOS reference image, Fedora 42 supported
- **Display, EC, keyboard, trackpad, chassis**: largely carryover from anyon_e; thermal solution is the major mechanical delta

See [`README.md`](./README.md) for headline specs and [`docs/BUILD.md`](./docs/BUILD.md) for the build sequence. Decision rationale lives in §8 of the [anyon_e CLAUDE.md](../laptop/CLAUDE.md).

---

## 2. Repo layout

```
mang0/
├── motherboard/   KiCad — Strix Halo carrier
├── ec/            ESP32-S3 firmware (PlatformIO, inherited from anyon_e)
├── power/         KiCad — PD 3.1 EPR sink, multiphase regulators
├── keyboard/      KiCad — wireless mech (anyon_e carryover)
├── trackpad/      Azoteq PXM0057 carrier
├── display/       eDP wiring + tandem OLED references
├── audio/         KiCad — TPA2028 + 4-mic beamforming
├── haptic/        Haptic actuator board
├── switch/        Power button board
├── chassis/       OnShape source + STEP exports
├── batteries/     Amprius SiCore pack design
├── wireless/      M.2 E-key WiFi 7 (MT7925)
├── sensors/       Camera, ToF, ambient, mic-array carriers
├── security/      OpenTitan RoT carrier + provisioning
├── thermal/       Vapor chamber + blower CAD
├── docs/          BUILD.md, BOM.md, images
├── ci/            GitHub Actions
├── nix/           flake.nix
├── hil/           Hardware-in-the-loop test fixtures
└── website/       Astro site (when stood up)
```

Each PCB subsystem is a standalone KiCad project carrying its own `library/`. Do not assume global symbol libs are available.

---

## 3. What's inherited from anyon_e

These subsystems are deliberately copied verbatim from `../laptop/` with minimal changes. Treat anyon_e as upstream:

- **Embedded controller** (`ec/`) — ESP32-S3 firmware, I²C drivers for BQ25713, LTC2943. Extended with: fan PID, mic gating, OpenTitan reset, Hailo power-state.
- **Keyboard** (`keyboard/`) — nRF52840 + Cherry ULP. Unchanged.
- **Trackpad** (`trackpad/`) — Azoteq PXM0057. Verify stock at BOM time (vendor EOL).
- **Audio amp** (`audio/`) — TPA2028D1. Mic array is new.
- **Switch** (`switch/`) — power button + LEDs. Unchanged.
- **Chassis envelope** (`chassis/`) — same anodized aluminum CNC, redesigned bottom for blower exhaust.

When upstream anyon_e ships fixes, port them. Don't fork silently.

---

## 4. What's new in mang0

- **Strix Halo motherboard** — entirely new design. AMD Glinda-class platform.
- **Power tree** — multiphase VDDCR_SOC, EPR sink. Bigger and meaner than anyon_e's.
- **Hailo-10H** — new M.2 slot, EC-controlled power.
- **OpenTitan** — new SPI bus from SoC, EC-controlled reset.
- **Sensor stack** — 4-mic beamforming, IR+RGB, ToF, ambient. New `sensors/` directory.
- **Thermal** — vapor chamber + dual blower. New `thermal/` directory.
- **CI / Nix / HIL** — process scaffolding new in mang0; intentionally landed before silicon.

---

## 5. Conventions (same spirit as anyon_e, plus)

- **Voice**: keep maintainer voice in markdown, but mang0 docs default to second-person instructional ("you do X, then Y"). The build guide is reference material, not a personal log.
- **READMEs**: short pointers — link to upstream datasheets, OnShape, vendor pages.
- **CI is mandatory.** Unlike anyon_e (no CI), every PR must pass headless KiCad ERC/DRC, `pio run`, and `npm run build`.
- **Tests**: EC firmware modules added in mang0 must have Unity tests under `ec/test/`. Existing anyon_e code is grandfathered — don't retro-test it without reason.
- **Branching**: `main` always builds. Subsystem feature branches: `mb/usb4-fanout`, `power/epr-sink`, etc.
- **Commits**: terse imperative, conventional-commit prefix optional (`feat: …`, `fix: …`).

---

## 6. Hard constraints

- **Mainline kernel only.** Do not depend on vendor BSPs in shipped images. Kernel ≥6.18.4 for Strix Halo gfx1151.
- **Open firmware only.** coreboot + edk2. No proprietary BIOS in the boot path.
- **No closed kernel modules in the default image** with one documented exception: Hailo-10H's kernel module remains closed in 2026. Document it prominently in `docs/BUILD.md` and watch upstream for replacement.
- **All schematics + gerbers committable.** No NDA-only parts in the critical path. Strix Halo PDG access is acceptable as long as the *output* (the schematic) is publishable.
- **Reproducible builds.** `nix build` reproduces every artifact: gerbers, EC firmware, NixOS image.

---

## 7. Things to NOT do

- Do not regenerate KiCad files via scripts — S-expression rounding silently shifts traces.
- Do not commit `jlcpcb/`, `gerbers/`, `*.net`, `*.csv`, `*-backups/`.
- Do not skip CI. If CI is broken, fix CI first, not the workaround.
- Do not introduce a vendor BSP shortcut even when it would unblock you. Open the upstream issue instead.
- Do not fork anyon_e subsystems silently. Port and credit.
- Do not change the Strix Halo power tree without re-reading the AMD PDG. Mistakes here brick chips.

---

## 8. Process slash-commands (when stood up)

- `/erc` — run KiCad ERC across every project, surface violations
- `/drc` — same for DRC + length match
- `/build-ec` — `pio run` for the EC firmware
- `/build-coreboot` — build coreboot + edk2 payload
- `/build-image` — `nix build .#nixosImage`
- `/review` — diff schematic netlists, EC firmware, content against `main` and run Claude review
- `/hil-smoke` — fire the HIL fixture and assert serial output

---

## 9. When in doubt

- **Architecture change?** → align to anyon_e's `CLAUDE.md` §8 decision matrix. If the answer isn't there, raise an issue tagged `arch`.
- **Subsystem swap?** → check anyon_e first. If it solved this in v1, port the solution.
- **Thermal margin doubt?** → measure, don't assume. The whole project lives or dies on the vapor chamber.
- **Anything touching DDR or USB4 layout?** → ask before merging. These rules are tight enough that "looks fine" is usually wrong.
