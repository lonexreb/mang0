# Wokwi simulation for EC firmware

Simulates the ESP32-S3 EC against virtual I2C peripherals (HUSB238, BQ25713, LTC2943) without flashing real silicon.

## Setup

```bash
# Build the EC firmware first
cd ec && pio run && cd -

# Install wokwi-cli
npm install -g wokwi-cli

# Run a scenario
wokwi-cli sim/firmware/wokwi --scenario sim/firmware/wokwi/scenarios/01-cold-boot.test.yaml
```

## Browser-based alternative

Open https://wokwi.com/projects/new/esp32-s3, paste `diagram.json`, drag in the firmware ELF, run interactively.

## Scenarios

- `01-cold-boot.test.yaml` — EC enumerates I2C, starts 1 Hz loop, prints battery percent
- `02-thermal-shutdown.test.yaml` — verifies EC zeros BQ25713 ChargeCurrent when LTC2943 reports ≥60 °C

Add scenarios as the EC firmware grows. CI calls `wokwi-cli` headless on every PR touching `ec/`.
