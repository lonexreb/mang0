# Workload validation

**Goal:** prove the AI thesis (run useful local LLMs on this exact silicon) on a *bought* Framework Desktop **before** committing to mang0's custom hardware path.

This is the **kill switch** for the project. If a $1,999 Framework Desktop with Strix Halo + 128 GB can't deliver the target tok/s, no amount of clever PCB work makes mang0 viable as a laptop. Run this gate **first**.

---

## The thesis (must pass)

| Model | Quantization | Min tok/s | Stretch tok/s |
|---|---|---|---|
| Qwen3-30B-A3B | Q4_K_M | 30 | 50 |
| Llama 3.3 70B | Q4_K_M | 4 | 7 |
| GPT-OSS 120B | Q4_K_M | 25 | 35 |
| Mistral 7B | Q5_K_M | 60 | 90 |

Targets sourced from [Framework community thread](https://community.frame.work/t/linux-rocm-january-2026-stable-configurations-update/79876) and [kyuz0/amd-strix-halo-toolboxes](https://github.com/kyuz0/amd-strix-halo-toolboxes).

If any **min** target fails on a stock Framework Desktop with the recommended ROCm config, **stop the project** until either (a) the target is achievable on a future kernel/ROCm version, or (b) the target is revised down with explicit user buy-in.

---

## Setup

1. Buy [Framework Desktop 128 GB](https://frame.work/desktop) ($1,999) — this becomes both the workload reference and the SoC source for mang0 prototype #1.
2. Install Fedora 42 or Ubuntu 25.10 with kernel ≥6.18.4 (gfx1151 stability fix).
3. Install ROCm per [AMD's Strix Halo guide](https://rocm.docs.amd.com/en/latest/how-to/system-optimization/strixhalo.html).
4. Run benchmarks (below) and commit results to `sim/workload/REPORT.md`.

---

## Benchmark script

```bash
#!/bin/bash
# sim/workload/run.sh
set -euo pipefail

MODELS=(
  "qwen3:30b-a3b-q4_K_M"
  "llama3.3:70b-instruct-q4_K_M"
  "gpt-oss:120b-q4_K_M"
  "mistral:7b-instruct-q5_K_M"
)

for m in "${MODELS[@]}"; do
  echo "=== $m ==="
  ollama run "$m" --verbose <<< "Explain the OSI model in two sentences."
done | tee REPORT.txt
```

Capture: prompt eval tok/s, generation tok/s, total time, peak VRAM, peak package temp (`rocm-smi -t` in another terminal).

---

## What "pass" looks like

`sim/workload/REPORT.md` should land like:

```markdown
# Workload validation — REPORT

Hardware: Framework Desktop, Strix Halo, 128 GB LPDDR5X-8000
Kernel: 6.18.7
ROCm: 7.0.2

| Model         | Min target | Measured | Pass |
|---------------|------------|----------|------|
| Qwen3-30B-A3B | 30 tok/s   | 52 tok/s | ✅   |
| Llama 3.3 70B | 4 tok/s    | 5.3 tok/s| ✅   |
| GPT-OSS 120B  | 25 tok/s   | 34 tok/s | ✅   |
| Mistral 7B    | 60 tok/s   | 91 tok/s | ✅   |

Verdict: thesis confirmed. Proceed to motherboard layout.
```

If it doesn't pass, the report says exactly which target failed and by how much, and the project pauses for explicit triage.

---

## Sources

- [Framework community ROCm config thread, January 2026](https://community.frame.work/t/linux-rocm-january-2026-stable-configurations-update/79876)
- [Strix Halo backend benchmarks — kyuz0](https://kyuz0.github.io/amd-strix-halo-toolboxes/)
- [Strix Halo LLM optimization findings — Hardware Corner](https://www.hardware-corner.net/strix-halo-llm-optimization/)
- [AMD Strix Halo system optimization — ROCm Documentation](https://rocm.docs.amd.com/en/latest/how-to/system-optimization/strixhalo.html)
