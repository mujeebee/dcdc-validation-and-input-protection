# 1. Test Plan — DUT-12V5 DC-DC Converter Board

> **Status: DESIGN OF A VALIDATION PACKAGE. No physical tests were run. All results elsewhere in this repo are SIMULATED.**
> Test levels below are typical planning values. Before any real test, confirm every number against your licensed copy of ISO 16750-2, ISO 7637-2 and ISO 10605 and against the customer's severity-level agreement.

## 1.1 Device under test (DUT) — assumed specification

| Item | Value |
|---|---|
| Name | DUT-12V5 (fictional board) |
| Function | 12 V automotive battery → 5 V / 3 A buck converter |
| Operating input | 9 – 16 V (full performance) |
| Output | 5.00 V, accepted band **4.85 – 5.15 V** (±3 %), 0 – 3 A |
| Input protection | Series P-FET ideal-diode (reverse polarity), 15 A fuse, TVS SMBJ33A (Vbr min 36.7 V) |
| Converter IC | Abs-max input 42 V, UVLO falling 4.0 V / rising 4.4 V |
| Connectors | J1 = battery in (pin 1 = +12 V, pin 2 = GND); J2 = 5 V out (pin 1 = +5 V, pin 2 = GND) |
| Load during tests | Electronic load, constant-current 3 A (unless stated) |

## 1.2 Functional status classes (ISO 16750-1)

| Class | Meaning |
|---|---|
| A | Full function during and after the test |
| B | Out of spec during test, normal after, no reset/latch-up needed |
| C | Function lost during test, self-recovers afterwards |
| D | Needs a manual reset / power-cycle to recover |
| E | Damaged / permanent failure |

## 1.3 Test scope and pass/fail criteria

"Vout OK" means 4.85 V ≤ Vout ≤ 5.15 V.

| Test ID | Standard / topic | Test level (planning values) | Required class | Pass criterion |
|---|---|---|---|---|
| TC-01 | ISO 16750-2 DC supply voltage | 9, 12, 14, 16 V; load 0 and 3 A | A | Vout OK at all points |
| TC-02 | ISO 16750-2 Overvoltage | 18 V for 60 min at 65 °C | A | Vout OK throughout, no damage, case ≤ 105 °C |
| TC-03 | ISO 16750-2 Superimposed AC | 1 Vpp sine on 14 V, 50 Hz – 25 kHz sweep | A | Vout OK throughout |
| TC-04 | ISO 16750-2 Slow decrease/increase | 16 → 0 → 16 V at 0.5 V/min | A for Vin ≥ 9 V | Vout OK; no overshoot > 5.5 V near UVLO; clean restart |
| TC-05 | ISO 16750-2 Short supply interruption | 100 µs, 1 ms, 10 ms drop-outs to 0 V | A (≤ 1 ms), B (10 ms) | Vout OK for ≤ 1 ms; automatic recovery ≤ 10 ms after 10 ms |
| TC-06 | ISO 16750-2 Starting profile (cranking) | 12 V → 4.5 V for 15 ms, recovery profile | B | No reset/latch; Vout OK within 10 ms of recovery |
| TC-07 | ISO 16750-2 Load dump, Test B (centrally suppressed) | Us\* = 35 V, td = 400 ms, Ri = 2 Ω, 10 pulses, 1 min apart | A | Vout OK; no damage |
| TC-08 | ISO 16750-2 Reversed voltage | −14 V for 60 s | C | Reverse current < 10 mA, Vout never < −0.3 V, full function after |
| TC-09 | ISO 7637-2 Pulse 1 | Us = −100 V, Ri = 10 Ω, td = 2 ms, 500 pulses, t1 = 0.5 s | C | Self-recovers; full function after |
| TC-10 | ISO 7637-2 Pulse 2a | Us = +50 V, Ri = 2 Ω, td = 50 µs, 500 pulses, t1 = 0.5 s | B | Normal after; no reset |
| TC-11 | ISO 7637-2 Pulse 3a | Us = −150 V, Ri = 50 Ω, 10 ms burst, 1 h | A | Vout OK throughout |
| TC-12 | ISO 7637-2 Pulse 3b | Us = +150 V, Ri = 50 Ω, 10 ms burst, 1 h | A | Vout OK throughout |
| TC-13 | ISO 7637-2 Pulse 4 | Supply dips from 12 V to ≈ 6 V for ≈ 15 – 40 ms (cranking dip) | B | No reset; Vout OK ≤ 10 ms after recovery |
| TC-14 | ISO 7637-2 Pulse 5b | Us\* = 35 V (clamped load dump), td = 400 ms, Ri = 1 Ω, 10 pulses | A | Vout OK; no damage |
| TC-15 | ISO 10605 ESD, contact, powered | ±4 kV, ±8 kV; 150 pF / 330 Ω; 3 discharges per pin per polarity, ≥ 1 s apart; J1-1, J1-2, J2-1, J2-2 | A | Vout OK during and after every discharge |
| TC-16 | ISO 10605 ESD, air, powered | ±8 kV, ±15 kV; 150 pF / 330 Ω; same pins | B | No reset/latch; normal after each discharge |

Notes:
- Pulses 1, 2a, 3a, 3b, 4, 5b are the ISO 7637-2 **transient immunity** pulses for a 12 V system. Pulse 5b is the "suppressed" load dump; TC-07 and TC-14 overlap on purpose (one cites ISO 16750-2, one ISO 7637-2).
- **Load dump Test A** (unsuppressed, Us = 79 – 101 V) is **not** in scope: the system integrator is assumed to provide central suppression. The simulation in `sim/` shows why the board alone cannot survive it (see report §6).
- Pre/post checks for every test: Vout at 12 V / 3 A, quiescent current, visual inspection, power-good/enable response.

## 1.4 Equipment list

| # | Equipment | Minimum capability | Used for |
|---|---|---|---|
| 1 | Programmable DC power supply | 0 – 60 V, ≥ 10 A, arbitrary waveform / fast slew | TC-01 – 06 |
| 2 | Automotive transient pulse generator | ISO 7637-2 pulses 1, 2a, 3a, 3b, 4, 5b; ISO 16750-2 load dump | TC-07 – 14 |
| 3 | ESD gun | ISO 10605, 150 pF/330 Ω (and 330 pF/2 kΩ module), ±15 kV air, ±8 kV contact | TC-15, 16 |
| 4 | Oscilloscope | ≥ 4 ch, ≥ 200 MHz, ≥ 1 GS/s | all |
| 5 | HV probes / differential probe | 1:10 passive, 100 V-rated differential | TC-09 – 14 |
| 6 | Current probe | DC – 50 MHz, 30 A | TC-08 – 14 |
| 7 | Electronic load | CC mode, 0 – 5 A | all |
| 8 | 6½-digit DMM | µA range | TC-01, 08 |
| 9 | Thermal chamber | −40 … +125 °C | TC-02 |
| 10 | Thermocouples (K-type) + logger | 2 ch | TC-02 |
| 11 | ESD ground reference plane, 0.5 mm insulating mat | per ISO 10605 setup | TC-15, 16 |
| 12 | Fused harness, 15 A fuse, short leads | — | all |
| 13 | Safety items | HV-rated gloves, ESD wrist strap, labelled test area | all |

## 1.5 General test conditions
- Ambient 23 ± 5 °C unless stated; DUT supply 14.0 V ± 0.2 V unless stated.
- Calibrated instruments; record serial numbers and calibration due dates in the report.
- Two samples (S/N 001, 002); S/N 001 for the full sequence, 002 held as reference.
- Stop on first Class D/E result, document, and open a corrective-action record (CAR).

## 1.6 Test sequence and risk order
Run non-destructive tests first (TC-01, 03 – 06, 08), then pulses (TC-09 – 14), then ESD (TC-15, 16), and overvoltage at temperature (TC-02) last, because it stresses the board thermally.
