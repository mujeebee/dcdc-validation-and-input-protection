# Explained Simply

**The problem.** A car's 12 V supply is not clean. Wires get disconnected, motors switch off, the starter cranks, and mechanics sometimes connect the battery backwards. Any electronics plugged into that supply must survive it. The "input protection" is the first part of the board that sees all this.

**What I built.** A simulated input stage with three parts:
1. **TVS diode** — a pressure-relief valve for voltage. Above about 37 V it conducts and soaks up the spike.
2. **P-FET (reverse-battery protection)** — a one-way valve. Current flows in the right direction, but if the battery is backwards it blocks.
3. **10 µF capacitor** — a small water tank that smooths and absorbs quick spikes.

Behind these sits the DC-DC converter, represented by a simple resistor.

**What I tested (in the computer, using LTspice).** The standard "bad events" of a car supply:
- **Pulse 1:** a big negative spike when power to a coil/motor is cut.
- **Pulse 2a:** a positive spike when something on the same wiring switches off.
- **Pulses 3a / 3b:** extremely fast, tiny negative/positive bursts from switching.
- **Pulse 4:** the voltage sag while the starter motor cranks.
- **Pulse 5b / load dump:** the alternator throws a big voltage surge if the battery is disconnected while running. "5b" is the version after the car has already trimmed it to ~35 V. I also ran the untrimmed ~101 V version just to see.
- **Reverse battery:** connecting the battery the wrong way.

**What I found (this is the interesting part).**
- My first version (**Rev A**) *failed*. When the voltage changed very quickly, the P-FET "valve" did not shut fast enough, so for a moment it let the capacitor's charge flow backwards and the protected side went to **−7.8 V** and **−13.3 V**. That would damage a real chip.
- Making the gate resistor smaller (10 kΩ → 1 kΩ) in **Rev B** shut the valve in time and fixed both cases.
- The untrimmed 101 V load dump overloaded the TVS (625 W against a 600 W rating, and 124 J of energy against about 0.6 J) and the protected node went to 65 V. This small TVS cannot handle that; the car's wiring must trim the surge first.
- The very fast pulses 3a/3b did almost nothing in the simulation because the capacitor soaked them up. In a real board, wire inductance and other effects could change that, so treat that result with caution.

**How to read the results.** Each pulse has a table row with the highest voltage reached, the TVS's peak current, power and energy, and a PASS/FAIL against the part ratings. Plots are in `plots/`.

**What is real and what is not.**
- Real: every number in the tables was calculated by actually running LTspice (rerun `python run_sims.py` to get the same numbers).
- Assumed: the pulse sizes and the component ratings are typical values I used, not copied from the standards or datasheets (those must be checked).
- Simulation only: the models use simplified parts and ideal wiring, so real-world behaviour may differ.

**Why it matters.** Protecting a supply input and proving it with simulation first is routine work in automotive hardware design and validation. This project shows you can model it, find a weakness, fix it, and honestly state the limits of the model.
