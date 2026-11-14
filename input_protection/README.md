# Automotive 12 V Input Protection — LTspice Simulation vs ISO 7637-2 / ISO 16750-2

Design and simulation of a 12 V automotive input stage: **bidirectional TVS clamp + P-FET reverse-battery protection + 10 µF bulk capacitor**, simulated in **LTspice 26.0.2** against ISO 7637-2 pulses 1, 2a, 3a, 3b, 4, the ISO 16750-2 suppressed load dump (pulse 5b), an unsuppressed load dump (informational) and reverse battery.

> **Every number below was produced by an LTspice simulation run of the netlists in `netlists/`** (reproduce with `python run_sims.py`). Stimulus parameters and component ratings are *assumptions* (typical values, see Limitations).

## Circuit
```
battery/pulse ─ Ri ─ bat ──┬───────── P-FET (drain=bat, source=vin, gate─R_G─GND, 15 V zener G-S) ──┬── vin ── 10 µF ── 8 Ω load
                           └─ TVS (back-to-back SMBJ33CA model, Vbr 36.7 V, Rd 1.47 Ω)             └ (stands in for the DC-DC converter)
```
- TVS: clamps positive/negative transients at the connector.
- P-FET: blocks reverse battery (body diode blocks; gate pulled to GND turns it on with normal polarity).
- **Rev A:** R_G = 10 kΩ. **Rev B:** R_G = 1 kΩ (fix for the failures below).

## Results (all from LTspice runs; `results/summary.csv` has full precision)
Ratings used: TVS 600 W peak / 11.3 A / ~0.6 J reference (600 W × 1 ms); P-FET Vds 60 V, Vgs ±20 V; converter IC Vin max 42 V, min −0.3 V.

| Scenario | Rev | V(bat) max / min (V) | V(vin) max / min (V) | TVS Ipk (A) | TVS Ppk (W) | TVS energy (J) | P-FET Vds / Vgs max (V) | Verdict |
|---|---|---|---|---|---|---|---|---|
| P1 | A | 13.5 / -48.4 | 13.5 / -7.8 | 3.73 | 180.6 | 0.1421 | 46.3 / 13.5 | **FAIL: Vin ≥ −0.3** |
| P2a | A | 38.0 / 11.0 | 37.9 / 11.0 | 0.21 | 8.0 | 8.353e-05 | 0.4 / 15.0 | PASS |
| P3a | A | 13.5 / 13.3 | 13.5 / 13.3 | 0.00 | 0.0 | 2.043e-14 ×100 = 2.043e-12 per burst | 0.1 / 13.5 | PASS |
| P3b | A | 13.5 / 13.4 | 13.5 / 13.4 | 0.00 | 0.0 | 2.049e-14 ×100 = 2.049e-12 per burst | 0.1 / 13.5 | PASS |
| P4 | A | 13.5 / 6.0 | 13.5 / 6.0 | 0.00 | 0.0 | 6.096e-10 | 0.0 / 13.5 | PASS |
| P5b | A | 31.1 / 12.0 | 31.1 / 12.0 | 0.00 | 0.0 | 2.458e-08 | 0.1 / 15.0 | PASS |
| LD_A (info) | A | 65.6 / 11.2 | 65.4 / 11.2 | 9.53 | 625.1 | 124.2 | 0.1 / 15.1 | **FAIL: TVS Ppk, TVS energy, Vin ≤ 42** |
| REV | A | 13.4 / -14.0 | 13.4 / -0.0 | 0.00 | 0.0 | 1.69e-09 | 14.0 / 13.4 | PASS |
| REVF | A | 13.4 / -14.0 | 13.4 / -13.3 | 0.00 | 0.0 | 1.697e-09 | 14.0 / 13.5 | **FAIL: Vin ≥ −0.3** |
| P1 | B | 13.5 / -48.5 | 13.5 / 0.0 | 3.76 | 182.6 | 0.1442 | 49.3 / 13.5 | PASS |
| P2a | B | 37.9 / 11.0 | 37.9 / 11.0 | 0.20 | 7.7 | 8.01e-05 | 0.4 / 15.2 | PASS |
| P3a | B | 13.5 / 13.3 | 13.5 / 13.3 | 0.00 | 0.0 | 2.043e-14 ×100 = 2.043e-12 per burst | 0.1 / 13.5 | PASS |
| P3b | B | 13.5 / 13.4 | 13.5 / 13.4 | 0.00 | 0.0 | 2.049e-14 ×100 = 2.049e-12 per burst | 0.1 / 13.5 | PASS |
| P4 | B | 13.5 / 6.0 | 13.5 / 6.0 | 0.00 | 0.0 | 6.096e-10 | 0.0 / 13.5 | PASS |
| P5b | B | 31.1 / 12.1 | 31.0 / 12.1 | 0.00 | 0.0 | 2.458e-08 | 0.1 / 15.2 | PASS |
| LD_A (info) | B | 65.5 / 11.2 | 65.4 / 11.2 | 9.52 | 623.6 | 123.8 | 0.1 / 15.4 | **FAIL: TVS Ppk, TVS energy, Vin ≤ 42** |
| REV | B | 13.4 / -14.0 | 13.4 / -0.0 | 0.00 | 0.0 | 1.69e-09 | 14.0 / 13.4 | PASS |
| REVF | B | 13.4 / -14.0 | 13.4 / -0.0 | 0.00 | 0.0 | 1.697e-09 | 14.8 / 13.4 | PASS |

("×100" = single-pulse energy multiplied by the 100 pulses of a 10 ms burst; that multiplication is arithmetic, not a simulated burst. REVF = reverse battery with a 10 µs edge, REV = 1 ms edge.)

## What the simulations show
1. **Rev A fails pulse 1 and fast reverse-battery.** When the connector node drops by tens of volts in microseconds, the drain-gate capacitance drags the gate down with it and the P-FET stays on briefly, so current flows backwards out of the input capacitor and the converter-side node goes to **−7.8 V (P1)** and **−13.3 V (REVF)** — far below a typical −0.3 V IC limit. A slower reversal (1 ms) is fine.
2. **Rev B (R_G 10 kΩ → 1 kΩ) passes both.** The stiffer gate pull-down keeps the FET off. Note in P1-B the converter-side node still falls to 0 V (the capacitor discharges until the FET turns off), so the converter would lose its supply during the pulse — consistent with a "recovers by itself" class, **not** with "keeps running". Recovery time is *not* claimed here (see Limitations).
3. **Pulses 3a/3b are absorbed by the 10 µF capacitor through the conducting P-FET** in this idealised model, so the TVS never conducts. Real boards have inductance and capacitance that this model omits — treat this as a first-order simulation result.
4. **Pulse 2a (+50 V)** is clamped to 37.9 V at the converter side, only ~4 V below a 42 V IC limit.
5. **Suppressed load dump (35 V)** never reaches the TVS breakdown (31 V at the node), so the TVS does nothing. The **unsuppressed load dump (101 V)** drives the TVS to 625 W / 124 J, above its ratings, and the node to 65 V — far beyond the IC. A 600 W SMBJ-class TVS is the wrong device for it; the system needs central suppression or a much larger clamp.

## Files
| Path | Content |
|---|---|
| `netlists/*.cir` | 18 LTspice netlists (9 scenarios × Rev A/B), generated by the script |
| `run_sims.py` | Generates netlists, runs LTspice in batch, parses output, computes peaks/power/energy, plots, writes the table |
| `rawread.py` | Small reader for LTspice binary `.raw` files |
| `plots/*.png` | Waveforms: node voltages, TVS current, TVS power, P-FET Vds/Vgs, with ratings as dotted lines |
| `results/summary.csv`, `results/summary.md` | Full results table |
| `EXPLAINED_SIMPLY.md` | Plain-language explanation |

## Run it
Needs LTspice (free from Analog Devices), Python 3 with numpy and matplotlib.
```bash
pip install -r requirements.txt
python run_sims.py          # set LTSPICE_EXE=path\to\LTspice.exe if not auto-found
```
Tested with LTspice 26.0.2 on Windows. Raw output (`results/raw/`) is git-ignored and regenerated.

## Limitations (please read)
- **Pulse parameters** (e.g. pulse 1 = −100 V/10 Ω/2 ms) are typical planning values from memory, not copied from the standards (which are paid documents). Waveforms are a double-exponential approximation of the generator output, with the 13.5 V supply added. Confirm against ISO 7637-2 / 16750-2 before real use. Pulse 4 is a simplified 13.5 V → 6 V dip.
- **Component ratings** (SMBJ33CA 600 W / 11.3 A / Vbr 36.7 V; 60 V P-FET; 42 V IC) are assumed typical values, not checked against datasheets. The TVS is modelled as a diode with Vbr and a series resistance fitted to those numbers; the P-FET uses a generic LTspice VDMOS model. The 0.6 J TVS energy reference (600 W × 1 ms) is a rough, conservative stand-in for a datasheet pulse-energy curve.
- **No parasitics** (wiring inductance, ESL/ESR, TVS capacitance). This matters most for pulses 3a/3b.
- The generator source resistance Ri is switched in only during a time window around the pulse (visible as a step in the plots, e.g. ~17 ms for pulse 1); waveform tails and recovery times after the window are therefore **not** meaningful.
- The converter is an 8 Ω resistor (~1.5 A), not a constant-power converter model.
- No thermal, no EMC emissions, no component tolerance or temperature sweeps.
