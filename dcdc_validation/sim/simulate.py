"""Simulation of ISO 16750-2 load dump and reversed-voltage on a 12 V -> 5 V DC-DC board.
ALL OUTPUT IS SIMULATED (simple first-order models, not measurements).
Run:  python sim/simulate.py     (needs numpy, matplotlib)
"""
import os, numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = os.path.join(os.path.dirname(__file__), "plots")
os.makedirs(OUT, exist_ok=True)

# ---- DUT assumptions (see docs/01_test_plan.md) ----
VB, P_OUT, ETA = 14.0, 15.0, 0.90      # battery, 5 V x 3 A, efficiency
I_LOAD = P_OUT / ETA / 12.0            # ~1.4 A input current (const. approx.)
ABS_MAX = 42.0                         # converter IC abs-max input voltage
# TVS SMBJ33A (600 W, 10/1000 us): Vbr(min)=36.7 V, Vc=53.3 V @ Ipp=11.3 A
VBR, IPP = 36.7, 11.3
RD = (53.3 - VBR) / IPP                # dynamic resistance ~1.47 ohm

def load_dump(t, us, td, t_rise=0.010, t0=0.05):
    """Simplified ISO 16750-2 load dump: ramp VB->Us in 10 ms, exp. decay, td = half-value time."""
    v = np.full_like(t, VB)
    r = (t >= t0) & (t < t0 + t_rise)
    v[r] = VB + (us - VB) * (t[r] - t0) / t_rise
    d = t >= t0 + t_rise
    v[d] = VB + (us - VB) * np.exp(-(t[d] - t0 - t_rise) * np.log(2) / td)
    return v

def node(us_t, ri):
    """Voltage at converter input: source -> Ri -> node, TVS + constant-current load at node."""
    v_open = us_t - ri * I_LOAD
    v_clamp = (us_t / ri - I_LOAD + VBR / RD) / (1 / ri + 1 / RD)
    v = np.where(v_open > VBR, v_clamp, v_open)
    i_tvs = np.maximum(0, (v - VBR) / RD)
    return v, i_tvs

def run_ld(name, us, td, ri):
    t = np.linspace(0, 1.0, 20001)
    src = load_dump(t, us, td)
    v, i = node(src, ri)
    p = v * i
    e = np.trapezoid(p, t)
    return dict(name=name, t=t, src=src, v=v, i=i, vpk=v.max(), ipk=i.max(), e=e)

A = run_ld("Test A (unsuppressed) Us=101 V, Ri=2 ohm, td=400 ms", 101, 0.400, 2.0)
B = run_ld("Test B (suppressed) Us*=35 V, Ri=2 ohm, td=400 ms", 35, 0.400, 2.0)

fig, ax = plt.subplots(2, 1, figsize=(9, 7), sharex=True)
for r, c in ((A, "tab:red"), (B, "tab:blue")):
    ax[0].plot(r["t"], r["src"], "--", color=c, alpha=.5, label="source (open circuit) - " + r["name"].split()[1])
    ax[0].plot(r["t"], r["v"], color=c, label="board input node - " + r["name"].split()[1])
    ax[1].plot(r["t"], r["i"], color=c, label="TVS current - " + r["name"].split()[1])
ax[0].axhline(ABS_MAX, color="k", ls=":"); ax[0].text(0.6, ABS_MAX + 1.5, "IC abs-max 42 V", fontsize=8)
ax[1].axhline(IPP, color="k", ls=":"); ax[1].text(0.6, IPP + 0.8, "SMBJ33A Ipp 11.3 A (10/1000 us)", fontsize=8)
ax[0].set_ylabel("Voltage (V)"); ax[1].set_ylabel("Current (A)"); ax[1].set_xlabel("Time (s)")
ax[0].legend(fontsize=7); ax[1].legend(fontsize=7)
ax[0].set_title("SIMULATED - ISO 16750-2 load dump on DUT-12V5 with SMBJ33A input TVS")
for a in ax: a.grid(alpha=.3)
plt.tight_layout(); plt.savefig(os.path.join(OUT, "load_dump.png"), dpi=130); plt.close()

# ---- Reversed voltage: -14 V for 60 s, 15 A fuse, supply+harness 0.05 ohm ----
t = np.linspace(0, 0.3, 3001); ton = 0.1
R_SUP, V_BODY = 0.10, 0.7              # supply+harness+IC resistance; body-diode drop
I_unprot = (14 - V_BODY) / R_SUP       # ~133 A
t_fuse = ton + 0.004                   # assumed ~4 ms melt time at ~9x fuse rating
i_none = np.where(t < ton, 1.4, np.where(t < t_fuse, I_unprot, 0.0))
i_schottky = np.where(t < ton, 1.4, 0.002)    # 2 mA reverse leakage (assumed)
i_pfet = np.where(t < ton, 1.4, 0.0000005)    # 0.5 uA (assumed)
fig, ax = plt.subplots(1, 2, figsize=(11, 4))
ax[0].plot(t, i_none, label="No protection (fuse opens)", color="tab:red")
ax[0].plot(t, i_schottky, label="Series Schottky", color="tab:orange")
ax[0].plot(t, np.maximum(i_pfet, 1e-7), label="P-FET ideal diode (DUT)", color="tab:green")
ax[0].set_yscale("symlog", linthresh=1e-2); ax[0].set_xlabel("Time (s)"); ax[0].set_ylabel("Input current (A)")
ax[0].set_title("Reversed battery -14 V applied at t=0.1 s"); ax[0].legend(fontsize=7); ax[0].grid(alpha=.3)
vout_none = np.where(t < ton, 5.0, np.where(t < t_fuse, -0.7, 0.0))
vout_pfet = np.where(t < ton, 5.0, 0.0)
ax[1].plot(t, vout_none, color="tab:red", label="No protection"); ax[1].plot(t, vout_pfet, "--", color="tab:green", label="P-FET")
ax[1].set_xlabel("Time (s)"); ax[1].set_ylabel("5 V output (V)"); ax[1].set_title("Output rail"); ax[1].legend(fontsize=7); ax[1].grid(alpha=.3)
fig.suptitle("SIMULATED - ISO 16750-2 reversed voltage (assumed component values)", fontsize=9)
plt.tight_layout(); plt.savefig(os.path.join(OUT, "reverse_polarity.png"), dpi=130); plt.close()

# ---- Summary ----
iin = 1.5
print("LOAD DUMP (simulated)")
for r in (A, B):
    print(f"  {r['name']}: node peak {r['vpk']:.1f} V, TVS peak {r['ipk']:.1f} A, TVS energy {r['e']:.1f} J")
print(f"REVERSE: unprotected peak {I_unprot:.0f} A (15 A fuse opens), Schottky loss @1.5 A {0.45*iin*1e3:.0f} mW, "
      f"P-FET (20 mohm) loss @1.5 A {0.02*iin**2*1e3:.0f} mW")
