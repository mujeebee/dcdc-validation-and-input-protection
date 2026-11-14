# 4. Requirements-to-Test Traceability Matrix

Requirement IDs are for the fictional DUT-12V5. Results are **SIMULATED**.

| Req ID | Requirement | Source | Test case(s) | Procedure § | Result (sim.) |
|---|---|---|---|---|---|
| REQ-01 | Vout 4.85–5.15 V for Vin 9–16 V, 0–3 A (Class A) | ISO 16750-2 DC supply | TC-01 | 2.1 | PASS |
| REQ-02 | No damage / Class A at 18 V, 60 min, 65 °C | ISO 16750-2 Overvoltage | TC-02 | 2.1 | PASS |
| REQ-03 | Class A with 1 Vpp AC ripple, 50 Hz–25 kHz | ISO 16750-2 Superimposed AC | TC-03 | 2.1 | PASS |
| REQ-04 | Controlled shutdown/restart on slow supply ramp, no overshoot > 5.5 V | ISO 16750-2 Slow ramp | TC-04 | 2.1 | PASS |
| REQ-05 | Ride through ≤ 1 ms interruptions; auto-recover after 10 ms | ISO 16750-2 Interruption | TC-05 | 2.1 | PASS |
| REQ-06 | Survive cranking dip to 4.5 V without latch (Class B) | ISO 16750-2 Starting profile | TC-06 | 2.1 | PASS |
| REQ-07 | Operate through suppressed load dump 35 V / 400 ms (Class A) | ISO 16750-2 Load dump B | TC-07, TC-14 | 2.1, 2.2 | PASS |
| REQ-08 | Survive −14 V for 60 s, reverse current < 10 mA (Class C) | ISO 16750-2 Reversed voltage | TC-08 | 2.1 | PASS |
| REQ-09 | Survive pulse 1 (−100 V), self-recover (Class C) | ISO 7637-2 P1 | TC-09 | 2.2 | PASS |
| REQ-10 | Survive pulse 2a (+50 V) with Class B | ISO 7637-2 P2a | TC-10 | 2.2 | PASS |
| REQ-11 | Class A during pulses 3a / 3b (±150 V bursts) | ISO 7637-2 P3a/3b | TC-11, TC-12 | 2.2 | PASS |
| REQ-12 | Class B during pulse 4 (cranking dip) | ISO 7637-2 P4 | TC-13 | 2.2 | PASS |
| REQ-13 | Class A during pulse 5b (clamped load dump) | ISO 7637-2 P5b | TC-14 | 2.2 | PASS |
| REQ-14 | Class A for ±4/±8 kV contact discharge on connector pins | ISO 10605 contact | TC-15 | 2.3 | **FAIL → CAR-001 → PASS on retest (rev B)** |
| REQ-15 | Class B for ±8/±15 kV air discharge | ISO 10605 air | TC-16 | 2.3 | PASS |

Coverage check: 15 requirements → 16 test cases; every requirement has ≥ 1 test and every test traces to ≥ 1 requirement (TC-07/14 both cover REQ-07).
