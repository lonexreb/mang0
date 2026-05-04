```
        ▄▀▌
       ▐ ▄▀         ███╗   ███╗  █████╗  ███╗   ██╗  ██████╗   ██████╗
     ▄▀▀▀▀█▄        ████╗ ████║ ██╔══██╗ ████╗  ██║ ██╔════╝  ██╔═══██╗
   ▄█████████▄      ██╔████╔██║ ███████║ ██╔██╗ ██║ ██║  ███╗ ██║═══██║   🔥
  ▐███████████▌     ██║╚██╔╝██║ ██╔══██║ ██║╚██╗██║ ██║   ██║ ██║   ██║
   ▀█████████▀      ██║ ╚═╝ ██║ ██║  ██║ ██║ ╚████║ ╚██████╔╝ ╚██████╔╝
     ▀▀███▀▀        ╚═╝     ╚═╝ ╚═╝  ╚═╝ ╚═╝  ╚═══╝  ╚═════╝   ╚═════╝

      open · ai-native · unix · 128 GB on the lap
      strix-halo · hailo-10h · opentitan · coreboot · nixos
```

# mang0 🔥

*The first fully open, UNIX-native, AI-native laptop.*

A 13.3" laptop designed from the ground up to run modern local LLMs (up to 120B parameters) on entirely open firmware and a mainline Linux kernel. Successor in spirit to [anyon_e](../laptop), with every subsystem chosen against the May 2026 hardware landscape.

> *mang0 — slang for the perfect Melee technical execution. A laptop tuned for frame-perfect AI inference and Linux mainline.*

---

## Headline specs

| | |
|---|---|
| Compute | AMD Ryzen AI Max+ 395 "Strix Halo" — 16 Zen 5 cores @ 5.1 GHz, Radeon 8060S (40 RDNA 3.5 CUs), XDNA 2 NPU 50 TOPS |
| Discrete NPU | Hailo-10H M.2 (40 TOPS INT4, <5 W) — always-on inference for wake-word, vision, presence |
| Memory | 128 GB LPDDR5X-8000 unified (BGA, on-package) |
| Storage | 2 × PCIe 4.0 NVMe (OS+models, user-swappable) |
| Display | 13.3" 4K AMOLED (tandem when shipping) |
| Battery | 4S Amprius SiCore silicon-anode, ~90 Wh in v1 envelope |
| Charging | USB PD 3.1, 140 W EPR sink |
| I/O | 2 × USB4 (40 Gbps), WiFi 7 (MT7925), BT 5.4 |
| Cooling | Vapor chamber + dual blower, sustained 55 W |
| Sensors | 4-mic beamforming array, IR+RGB camera, ToF + ambient |
| Security | OpenTitan discrete RoT (TPM 2.0 over SPI) |
| Firmware | coreboot + edk2 |
| OS | NixOS reference image, Fedora 42 supported |
| AI runtime | ollama, llama.cpp (Vulkan + ROCm), mlc-llm preinstalled |

**Why these picks:** see [`CLAUDE.md`](./CLAUDE.md) §8 — every component is the only 2026 part that satisfies (a) commercial availability, (b) working open-stack support, (c) the "run a 70B model locally" thesis.

---

## Repo layout

```
mang0/
├── motherboard/   KiCad — Strix Halo carrier, 2× USB4, 2× NVMe, M.2 E-key + M-key, audio, display
├── ec/            ESP32-S3 firmware (PlatformIO), inherited & extended from anyon_e
├── power/         KiCad — PD 3.1 EPR sink, charger, gauge, protection, OpenTitan RoT
├── keyboard/      KiCad — wireless mech, nRF52840, Cherry ULP (anyon_e carryover)
├── trackpad/      Glass multi-touch on Azoteq PXM0057
├── display/       eDP 1.4 / DP 2.1 wiring + tandem OLED references
├── audio/         KiCad — TPA2028 amp + 4-mic beamforming
├── haptic/        Haptic actuator board
├── switch/        Power button board
├── chassis/       OnShape source + STEP exports
├── batteries/     Amprius SiCore pack design
├── wireless/      M.2 E-key WiFi 7 reference (MT7925)
├── sensors/       Camera, ToF, ambient, mic-array carrier boards
├── security/      OpenTitan RoT carrier + provisioning notes
├── thermal/       Vapor chamber + blower CAD
├── docs/          BUILD.md, BOM.md, theory of operation, images
├── ci/            GitHub Actions — KiCad ERC/DRC, gerbers, pio, npm
├── nix/           flake.nix for reproducible toolchain
├── hil/           Hardware-in-the-loop test fixtures
└── website/       Marketing + docs site (Astro)
```

---

## Where to start

- **Build the laptop:** [`docs/BUILD.md`](./docs/BUILD.md) — step-by-step from empty repo to working unit.
- **Source the parts:** [`docs/BOM.md`](./docs/BOM.md) — full bill of materials with vendor links.
- **Understand decisions:** [`CLAUDE.md`](./CLAUDE.md) §8 — 2026 SoC decision matrix.
- **Contribute:** see open issues. Schematic, layout, mechanical, and firmware all welcome.

---

## Status

**Pre-silicon.** Schematic capture in progress. Process infrastructure (CI, Nix flake, HIL) is the first deliverable — it ships before any hardware.

---

## License

- Hardware: CERN-OHL-S v2
- Firmware & software: MIT
- Documentation: CC-BY-SA 4.0

See [LICENSE](./LICENSE).

---

## Lineage

mang0 stands on [anyon_e](https://github.com/Hello9999901/laptop) by Byran Huang. Where anyon_e proved that an open, integrated 13.3" laptop is possible, mang0 asks: *what does that machine look like when it's also an AI-native UNIX workstation?*
