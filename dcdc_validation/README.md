# Automotive Electrical Validation Package — 12 V DC-DC Converter Board

A complete validation package for a fictional 12 V → 5 V / 3 A DC-DC converter board (DUT-12V5), covering **ISO 16750-2** (supply voltage tests), **ISO 7637-2** (transient pulses 1, 2a, 3a, 3b, 4, 5b) and **ISO 10605** (ESD).

> **All results are SIMULATED.** No lab equipment was used. Test levels are typical planning values; confirm against the licensed standards before real use. The standards are not reproduced here.

## Contents
| File | What it is |
|---|---|
| [docs/01_test_plan.md](docs/01_test_plan.md) | Scope, DUT spec, 16 test cases, pass/fail criteria, equipment list |
| [docs/02_test_procedures.md](docs/02_test_procedures.md) | Step-by-step procedure per test |
| [docs/03_validation_report.md](docs/03_validation_report.md) | Report template filled with simulated data, incl. one failure (ESD) with root cause and corrective action (CAR-001) |
| [docs/04_traceability_matrix.md](docs/04_traceability_matrix.md) | 15 requirements ↔ 16 test cases |
| [sim/simulate.py](sim/simulate.py) | Python simulation of load dump and reverse polarity |
| [sim/plots/](sim/plots) | `load_dump.png`, `reverse_polarity.png` |
| [data/simulated_results.csv](data/simulated_results.csv) | Results table (machine-readable) |
| [EXPLAINED_SIMPLY.md](EXPLAINED_SIMPLY.md) | Plain-language explanation |

## Run the simulation
```bash
pip install -r requirements.txt
python sim/simulate.py
```

## Key findings (simulated)
- 15 of 16 tests pass on hardware rev A.
- **TC-15 ESD contact +8 kV fails**: output dips to 3.92 V for 180 µs. Root cause: ESD noise couples into the feedback divider. Fix: output TVS, 1 nF on FB, re-routed trace. Rev B passes.
- Load dump Test A (101 V) would destroy the board (node peaks at 62.8 V vs 42 V IC limit), so central suppression is a documented system assumption.
- P-FET reverse protection loses ~45 mW vs ~675 mW for a Schottky at 1.5 A.

## Skills demonstrated
Test planning, requirements traceability, ISO 16750 / 7637 / 10605 knowledge, failure analysis (8D-style root cause), Python simulation and plotting, technical documentation.

## Limitations
Simplified first-order models; invented measurements; no EMC emissions testing; no thermal/humidity/vibration (ISO 16750-3/-4). Next step: build a real board and replace simulated data.
