# Firmware simulation

**Goal:** test coreboot boot flow and EC firmware state machine without burning a board.

---

## Coreboot in QEMU

Coreboot supports QEMU as a target board. While it doesn't model Strix Halo specifically, it validates the high-level boot flow, SeaBIOS/edk2 payload integration, and your `mainboard/mang0/` configuration's syntax + ramstage.

```bash
cd coreboot
make defconfig BOARD=qemu-q35   # validate config plumbing first
make -j$(nproc)
qemu-system-x86_64 -bios build/coreboot.rom -nographic
```

For Strix Halo–specific bring-up you'll still need real silicon eventually — but get every avoidable mistake out of the way in QEMU first.

---

## EC firmware in Wokwi

[Wokwi](https://wokwi.com/) simulates ESP32-S3 + I²C peripherals in-browser. Ideal for testing the EC's state machine without flashing.

```bash
# wokwi-cli for headless / CI use
npm install -g wokwi-cli
wokwi-cli ec/ --timeout 30
```

Add `ec/wokwi.toml`:

```toml
[wokwi]
version = 1
firmware = '.pio/build/esp32-s3-devkitc-1/firmware.bin'
elf = '.pio/build/esp32-s3-devkitc-1/firmware.elf'
```

And `ec/diagram.json` describing the peripherals (I²C devices, LED pins, etc.) — Wokwi can simulate BQ25713 / LTC2943 stubs that respond to register reads.

---

## Required tests (gate)

| Test | Pass criteria |
|---|---|
| Cold-boot serial trace | EC enumerates HUSB238, requests 20 V PD, initializes BQ25713 within 2 s |
| Charge-current setpoint write | EC writes `0x0800` to BQ25713 ChargeCurrent register; readback matches |
| Thermal shutdown | At simulated 60 °C+, EC zeros charge current within 1 loop iteration |
| Fan PID | Step response to temperature ramp; no oscillation, settles in <10 s |
| OpenTitan reset/recover | EC drives RST_N pulse, OpenTitan stub reports reboot, EC re-establishes SPI link |

---

## Files

```
sim/firmware/
├── qemu/
│   └── boot-trace.txt          ← expected QEMU boot output
├── wokwi/
│   ├── diagram.json
│   └── scenarios/
│       ├── 01-cold-boot.test.json
│       ├── 02-thermal-shutdown.test.json
│       └── ...
└── REPORT.md
```

This complements the [`hil/`](../../hil/) (hardware-in-the-loop) directory: HIL runs against real silicon, sim runs against virtual silicon. Both use the same test scenarios where possible.
