# 3. Validation Report — DUT-12V5 DC-DC Converter Board

> ## ⚠ ALL DATA IN THIS REPORT IS SIMULATED
> No hardware was tested. Numbers were invented to be plausible (and, for load dump / reverse polarity, computed by `sim/simulate.py`). This is a **template filled with example data** to show the format and the engineering workflow.

| Field | Value |
|---|---|
| Report ID | VR-DUT12V5-001 |
| DUT | DUT-12V5, HW rev A (and rev B after CAR-001) |
| Samples | S/N 001 (test), S/N 002 (reference) |
| Test plan | `01_test_plan.md` |
| Tester / date | *(name)* / *(date)* — placeholder |
| Equipment & calibration | *(fill from plan §1.4: model, S/N, cal. due)* — placeholder |
| Conditions | 23 ± 5 °C, supply 14.0 V, load 3 A |

## 1. Summary

| Result | Count |
|---|---|
| Tests run (rev A) | 16 |
| Pass | 15 |
| **Fail** | **1 (TC-15, ESD contact)** |
| After corrective action (rev B) | 16 / 16 pass |

**Verdict: rev A NOT released. Rev B released for next phase, subject to re-test of TC-15 on 3 samples.**

## 2. Detailed results (SIMULATED)

| Test | Level applied | Key measurement | Class required | Class achieved | Result |
|---|---|---|---|---|---|
| TC-01 | 9/12/14/16 V, 3 A | Vout 4.98 / 5.00 / 5.00 / 5.01 V | A | A | PASS |
| TC-02 | 18 V, 60 min, 65 °C | Vout 5.00–5.01 V; case max 88 °C | A | A | PASS |
| TC-03 | 1 Vpp, 50 Hz–25 kHz | Vout min 4.97 / max 5.04 V | A | A | PASS |
| TC-04 | 0.5 V/min | Vout OK to Vin 5.4 V; shutdown 4.0 V; restart 4.4 V; max Vout 5.02 V | A (≥ 9 V) | A | PASS |
| TC-05 | 100 µs / 1 ms / 10 ms | Vout min 4.91 / 4.86 V / 0 V; recovery 3.1 ms | A / A / B | A / A / B | PASS |
| TC-06 | 12 → 4.5 V, 15 ms | Vout min 4.18 V; recovery 4 ms; no latch | B | B | PASS |
| TC-07 | Us\* 35 V, 400 ms, 2 Ω | Node peak 32.2 V (sim.); Vout 4.99–5.01 V; TVS not conducting | A | A | PASS |
| TC-08 | −14 V, 60 s | Reverse current 0.8 µA; Vout min −0.02 V; normal after | C | A | PASS |
| TC-09 | P1 −100 V, 500 pulses | Vout min 4.62 V for 1.8 ms; recovers | C | B | PASS |
| TC-10 | P2a +50 V, 500 pulses | Vout 4.88–5.09 V | B | A | PASS |
| TC-11 | P3a −150 V, 1 h | Vout 4.94–5.06 V | A | A | PASS |
| TC-12 | P3b +150 V, 1 h | Vout 4.95–5.07 V | A | A | PASS |
| TC-13 | P4 12 → 6 V, 30 ms | Vout min 4.96 V | B | A | PASS |
| TC-14 | P5b Us\* 35 V, 1 Ω | Node 33.6 V; Vout 4.99–5.01 V | A | A | PASS |
| **TC-15** | **ESD contact, +8 kV, J2-1** | **Vout min 3.92 V for 180 µs** | **A** | **B** | **FAIL (rev A)** |
| TC-15 (rev B) | ESD contact ±4/±8 kV, all pins | Vout min 4.93 V (worst case), 48 discharges | A | A | PASS |
| TC-16 | ESD air ±8/±15 kV | Vout min 4.71 V for 150 µs; no reset | B | B | PASS |

Raw table: `../data/simulated_results.csv`.

## 3. Load dump and reverse-polarity simulation (Python)

Figures: `../sim/plots/load_dump.png`, `../sim/plots/reverse_polarity.png`.

| Case | Result (simulated) | Interpretation |
|---|---|---|
| Load dump Test B (35 V, 2 Ω) | Input node peak 32.2 V, TVS current 0 A | Below TVS breakdown (36.7 V) and IC abs-max (42 V): passes with margin |
| Load dump Test A (101 V, 2 Ω) — informational | Node peak 62.8 V, TVS peak 17.7 A, TVS energy ≈ 267 J | Exceeds IC abs-max 42 V and SMBJ33A rating (11.3 A, ~0.6 J at 10/1000 µs): board would fail. Needs central suppression or a bigger clamp |
| Reverse −14 V, no protection | ≈ 133 A until 15 A fuse opens | Fuse blows; output rail is pulled below 0 V |
| Reverse −14 V, series Schottky | Loss at 1.5 A ≈ 675 mW | Safe but wastes power as heat |
| Reverse −14 V, P-FET (DUT) | ≈ 0.5 µA, loss at 1.5 A ≈ 45 mW | Chosen design |

Model limits: constant-power load treated as constant current; TVS as linear V/I curve; load dump waveform is a simplified exponential; no inductance/parasitics. It is an engineering illustration, not a substitute for a real test.

## 4. Deviations and observations
- TC-02: case temperature rise of 23 °C over ambient, within limit but the highest of all tests → keep monitoring in design verification.
- TC-09: the 1.8 ms Vout dip comes from the 22 µF hold-up capacitor discharging while the P-FET blocks reverse input; acceptable for Class C.

## 5. Failure analysis — CAR-001

| Field | Content |
|---|---|
| CAR ID | CAR-001 |
| Failed test | TC-15 ESD contact discharge, +8 kV to J2-1 (5 V output pin), rev A, S/N 001 |
| Observed | Vout fell from 5.00 V to **3.92 V for 180 µs** then self-recovered. No reset, no damage. Required Class A (Vout ≥ 4.85 V) → achieved Class B → **FAIL**. Reproducible 3/3 at +8 kV and 3/3 at −8 kV; ±4 kV pass. |
| Severity | Medium (system supplied by this rail may reset a microcontroller) |
| Investigation (simulated) | 1) Scope on FB pin: 1.1 V spike at the same instant as Vout dip. 2) Layout review: feedback trace runs ~12 mm beside J2-1 and under the pad, loop area ≈ 80 mm². 3) Probing with the gun on J2-1 with FB divider removed: dip disappears → coupling into feedback confirmed. |
| **Root cause** | ESD current injected at J2-1 returns through ground; the fast di/dt couples (inductive/capacitive) into the high-impedance feedback divider (10 kΩ/3.3 kΩ). The error amplifier sees a false "high" FB, commands minimum duty cycle, and Vout falls until the loop recovers. Contributing causes: no ESD diode at J2, no FB filter capacitor, FB routed beside the connector. |
| Corrective actions | (1) Add TVS diode (5 V, e.g. PESD5V0-type, ≤ 30 pF) from J2-1 to GND next to the connector. (2) Add 1 nF capacitor FB-to-GND at the IC. (3) Re-route FB away from J2, guard with ground pour, reduce loop area to < 20 mm². (4) Add 10 Ω series resistor? — rejected: costs output regulation. |
| Verification | Rev B built; TC-15 re-run: ±4 and ±8 kV, 3 discharges × 4 pins × 2 polarities = 24 discharges per level (48 total) → worst-case Vout min 4.93 V. TC-01 and TC-03 re-run to check regulation/ripple unaffected: PASS (no change > 5 mV). TC-16 re-run: PASS. |
| Preventive action | Add layout rule "keep FB nodes ≥ 5 mm from connectors; protect every off-board pin with a TVS" to the design checklist; run a pre-compliance ESD scan at the layout stage. |
| Status | Closed (simulated) |

## 6. Conclusion and sign-off

Rev A failed one requirement (REQ-14). Rev B meets all 15 requirements in simulation. Open item: confirm with the system owner that the vehicle provides central load-dump suppression, because the board alone does not meet Test A.

| Role | Name | Signature | Date |
|---|---|---|---|
| Test engineer | | | |
| Design engineer | | | |
| Quality | | | |
