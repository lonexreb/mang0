# Motherboard

AMD Ryzen AI Max+ 395 ("Strix Halo") carrier. The long-pole subsystem.

## What's on it

- Strix Halo BGA (FP11)
- 128 GB LPDDR5X-8000 on-package
- 2 × USB4 Type-C (native, no retimer)
- 2 × NVMe M-key (one for OS+models, one user-swappable)
- 1 × M-key for Hailo-10H NPU
- 1 × E-key for MT7925 WiFi 7
- eDP 4-lane HBR3 to display
- I²S to audio codec + 4-mic array
- eSPI to ESP32-S3 EC
- SPI to OpenTitan TPM

## Stackup

12-layer HDI Type II. See [`docs/BUILD.md`](../docs/BUILD.md) §3.1.

## Reference designs

- AMD Strix Halo PDG (NDA — request via authorized distributor)
- HP OmniBook Ultra 14 (G2) teardowns for inspiration

## Status

Schematic capture not yet started. CI scaffolding lands first.
