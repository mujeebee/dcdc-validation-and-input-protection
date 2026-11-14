# Explained Simply

**What is this project?** A car's electrical system is rough: voltages jump around, batteries get connected backwards, and people get static shocks. Before a circuit board goes in a car, it must be tested against those events. This project is the *paper and simulation version* of that testing for a small power-supply board (12 V car battery in, 5 V out for electronics).

**What does the board do?** A DC-DC converter takes the car's messy 12 V and makes a steady 5 V for chips and sensors.

**The tests, in everyday words**
- **ISO 16750-2 (battery behaviour):** the battery isn't always 12 V. It is 9 V when cranking, 14 V when charging, 16 V in odd cases, and it can briefly drop out. The board must keep making 5 V.
- **Load dump:** if the battery cable comes loose while the engine runs, the alternator throws a big voltage spike (up to ~100 V) lasting a few hundred milliseconds. Like a water-hammer in a pipe.
- **Reverse polarity:** a mechanic connects the battery backwards. The board must not burn; a clever transistor acts like a one-way valve.
- **ISO 7637-2 (pulses):** quick spikes from switching things off — wipers, motors, relays. Pulse 1 = negative spike when power is cut from an inductive load; 2a = positive spike when a nearby load switches off; 3a/3b = very fast tiny bursts from switching; 4 = voltage sag while the starter turns; 5b = the load dump after the car's own protection trims it.
- **ISO 10605 (ESD):** static electricity — like touching a doorknob in winter — hitting the connector pins.

**Pass/fail "classes":** A = worked perfectly the whole time. B = glitched but recovered without help. C = stopped working but restarted by itself. D = needed a manual restart. E = broken.

**The deliberate failure:** In the simulated ESD test, a static zap on the 5 V output pin made the output sag to 3.9 V for 0.00018 s. That's a fail because we needed perfect (Class A). Cause: the zap's current made a noise pulse that leaked into the wire that tells the chip "what is the output right now?", so the chip was fooled. Fix: add a small protection diode, a small capacitor on that wire, and move the wire away from the connector. Retest passed.

**The simulation:** `sim/simulate.py` draws graphs of (1) a load dump hitting the board's protection part and (2) the current when the battery is connected backwards, with and without protection.

**Is the data real?** No. Everything is simulated and labelled that way. The documents show *how* a real validation would be planned, run, written up and traced to requirements.

**Why it matters for a job:** automotive companies (R&D, validation) do this every day. This shows you understand the tests, the paperwork, and how to debug a failure.
