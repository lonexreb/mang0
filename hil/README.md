# Hardware-in-the-loop

Pi-based test fixture for the EC firmware. Catches register regressions and PD negotiation bugs before they ship to a board.

## Hardware

- Raspberry Pi 5 (8 GB)
- USB-to-serial breakout to EC's USB-CDC
- I²C breakout to a stand-in BQ25713 dev board
- USB-PD source (Plugable USBC-TKEY) emulating chargers

## Usage

```bash
cd hil
pip install -r requirements.txt
pytest -v
```

## Test pattern

Each test:
1. Reflashes EC firmware via PlatformIO
2. Reads the USB-CDC stream for ~5 s
3. Asserts on log lines (e.g. `VBUS: 20.0`, `BQ25713 NOT CONNECTED`, `BATTERY PERCENT: <n>`)
4. Optionally injects an I²C transaction and asserts the EC response

See `tests/test_charging.py` for the canonical example (to be written).
