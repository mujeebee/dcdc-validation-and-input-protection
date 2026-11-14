# 2. Test Procedures

Companion to `01_test_plan.md`. Test levels and pass criteria are defined there; this file gives the steps. Always confirm levels against the licensed standards first.

## 2.0 Common setup (all tests)
1. Wear ESD strap; check the fuse (15 A) and harness; label the DUT with S/N and date.
2. Connect: supply → fuse → J1; J2 → electronic load (CC, 3 A). Scope CH1 = DUT input at J1 (differential or 1:10 probe, short ground spring), CH2 = Vout at J2, CH3 = input current (probe), CH4 = trigger/pulse monitor.
3. **Pre-check:** supply 14.0 V, load 3 A → record Vout, input current, quiescent current (load off), visual check. Must be 4.85 – 5.15 V.
4. Run the test below, capture waveforms (save as `<TestID>_<step>.png/csv`).
5. **Post-check:** repeat pre-check; compare. Any change > 20 mV or new heating → record as finding.
6. Fill in the results row of the report (Vout min/max, class achieved, pass/fail).

## 2.1 ISO 16750-2 tests

**TC-01 DC supply voltage**
1. Load 3 A. Set supply to 9 V → wait 2 min → record Vout, Iin. Repeat for 12, 14, 16 V.
2. Repeat at load 0 A.
3. Pass: all Vout within 4.85 – 5.15 V.

**TC-02 Overvoltage**
1. Place DUT and thermocouples in chamber at 65 °C; soak 30 min; load 3 A.
2. Set supply 18 V; run 60 min; log Vout and case temperature every 10 s.
3. Return to 14 V, cool to ambient, post-check. Pass: Vout OK throughout, case ≤ 105 °C, post-check unchanged.

**TC-03 Superimposed AC**
1. Supply 14 V DC + 1 Vpp sine (supply AC modulation input). Sweep 50 Hz → 25 kHz logarithmically over 2 min.
2. Monitor Vout peak-to-peak and min/max. Pass: Vout OK throughout.

**TC-04 Slow decrease/increase**
1. Start 16 V, load 3 A. Ramp down 0.5 V/min to 0 V, record Vin at which Vout leaves tolerance, UVLO shutdown and any overshoot.
2. Ramp up at 0.5 V/min to 16 V; record restart voltage.
3. Pass: Vout OK for Vin ≥ 9 V; max Vout < 5.5 V everywhere; clean restart without oscillation.

**TC-05 Short supply interruption**
1. Use programmable supply to drop from 14 V to 0 V for 100 µs, 1 ms and 10 ms (fall/rise ≤ 10 µs). Three repetitions each, 10 s apart.
2. Record min Vout and recovery time to 4.85 V.
3. Pass: Vout OK for ≤ 1 ms; ≤ 10 ms recovery after the 10 ms drop-out (Class B).

**TC-06 Starting profile**
1. Program profile: 12 V → 4.5 V in ≤ 5 ms, hold 15 ms, ramp to 12 V in 20 ms.
2. Record Vout min, any reset/latch behaviour (PG pin), recovery time. Three repetitions.
3. Pass: no latch; Vout OK ≤ 10 ms after Vin returns above 9 V.

**TC-07 Load dump, Test B**
1. Configure pulse generator: Us\* = 35 V, td = 400 ms, Ri = 2 Ω, rise ≤ 10 ms.
2. **Verify the pulse into a dummy load before connecting the DUT** (open-circuit amplitude and width).
3. Apply 10 pulses, 1 min apart, DUT powered at 14 V, load 3 A. Capture Vin node, Vout, Iin.
4. Pass: Vout OK; no damage; post-check unchanged.

**TC-08 Reversed voltage**
1. Supply set to −14 V (or reverse leads via a relay) through the 15 A fuse, load connected.
2. Apply for 60 s. Measure input current with DMM (µA range), Vout with scope (DC coupled, trigger on negative).
3. Restore 14 V, post-check. Pass: reverse current < 10 mA, Vout ≥ −0.3 V, normal function afterwards.

## 2.2 ISO 7637-2 pulses (all: DUT powered 14 V, load 3 A)

For each pulse: **calibrate on a 50 Ω/dummy load first** (verify Us, tr, td, Ri against the standard's tolerance), then connect the DUT.

| Test | Generator settings | Procedure |
|---|---|---|
| TC-09 P1 | Us = −100 V, Ri = 10 Ω, td = 2 ms, tr = 1 µs, t1 = 0.5 s | 500 pulses; monitor Vout continuously; log worst-case min/max and recovery time |
| TC-10 P2a | Us = +50 V, Ri = 2 Ω, td = 50 µs, tr = 1 µs, t1 = 0.5 s | 500 pulses; same logging |
| TC-11 P3a | Us = −150 V, Ri = 50 Ω, td = 150 ns, tr = 5 ns, burst 10 ms, t1 = 100 µs, t4 = 10 ms, t5 = 90 ms | Run 1 h; record Vout envelope every 10 min and 1 worst-case burst capture |
| TC-12 P3b | Us = +150 V, other settings as P3a | Same as TC-11 |
| TC-13 P4 | Dip 12 V → ≈ 6 V, ≈ 15 – 40 ms, then recovery | 3 repetitions; record min Vout and recovery |
| TC-14 P5b | Us\* = 35 V, td = 400 ms, Ri = 1 Ω | 10 pulses, 1 min apart |

Pass criteria per the plan. After each test, run the post-check before the next pulse test.

## 2.3 ISO 10605 ESD

Setup: DUT on 0.5 mm insulating mat on the grounded reference plane; ground strap of the gun connected to the plane; DUT powered at 14 V, load 3 A; Vout on scope (trigger on Vout < 4.85 V, single shot).

**TC-15 Contact discharge, powered**
1. Gun module 150 pF / 330 Ω, contact mode.
2. For each pin (J1-1, J1-2, J2-1, J2-2) and each level (+4, −4, +8, −8 kV): apply 3 discharges, ≥ 1 s apart.
3. Capture Vout; record min value and duration below 4.85 V; note any reset.
4. Pass: Vout OK for every discharge (Class A).

**TC-16 Air discharge, powered**
1. Same setup, air mode, approach the pin / connector body at constant speed.
2. Levels ±8, ±15 kV; 3 discharges per point.
3. Pass: no reset or latch-up; normal after each discharge (Class B).

Optional extension: repeat with 330 pF / 2 kΩ, and run unpowered handling-level discharges.

## 2.4 On failure
1. Stop; save all captures; do not power-cycle until the state is photographed/logged (this shows whether it was Class C or D).
2. Open a corrective-action record (see report §5), identify root cause, fix, **re-run the failed test and any test the fix could affect**.
