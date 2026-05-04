# EC

Embedded controller firmware for the ESP32-S3, in Arduino + PlatformIO. Inherits the anyon_e firmware and extends it.

## What's new vs anyon_e

- Fan PID loop (2 channels, PWM out + tach in)
- Hailo-10H power-state machine
- OpenTitan reset + interrupt handling
- 4-mic array power gating
- Hardware mic + camera kill switches
- TPS65987D (replacing HUSB238) for USB PD 3.1 EPR

## Build

```bash
cd ec
pio run                    # build
pio run -t upload          # flash
pio device monitor         # serial @ 115200
```

## Tests

```bash
pio test -e native         # host-side unit tests
```

HIL tests live in `../hil/`.

## Pin map

See `src/main.cpp` `#define`s. Document any addition in this README.
