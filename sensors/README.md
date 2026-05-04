# Sensors

Carrier boards for the AI-native sensor stack.

## Components

| Sensor | Part | Purpose |
|---|---|---|
| RGB camera | OmniVision OV5675 (5 MP) | Standard webcam, USB to SoC |
| IR camera | Pixart PAS6180 | Face wake (Hailo-10H pipeline) |
| ToF | ST VL53L8 (8×8 zone) | Lid proximity, gesture |
| Ambient light | AMS TSL2591 | Auto-brightness |
| MEMS mic ×4 | ST MP34DT06JTR | Beamforming array |

## Privacy

- Mic array: hardware kill switch (EC-controlled) cuts power to all four MEMS mics
- Camera: solenoid-actuated shutter, EC-controlled
- Single physical switch surfaces both kills

## Pipeline

1. Always-on: 4-mic array → EC → wake-word VAD on Hailo (<50 mW)
2. Wake confirmed: SoC powers on, full ASR pipeline
3. Face wake: IR camera → Hailo for face match → SoC unlock
4. Standard webcam: RGB camera → SoC over USB 2.0
