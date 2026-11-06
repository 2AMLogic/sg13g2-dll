# cp-currents record

Charge pump (`design/cp.sch`) with `cp_bias`, VOUT held by an ideal source at 0.6 V, reduced corner set (tt/1.2 V/27 C, ss/1.08 V/125 C, ff/1.32 V/-40 C), one `klt sim` request.
Simulated, never measured. Criteria K1-K6 are in `sim/cp-currents/summarize.py`.

Delay-sanity record for K_dl: `/home/ubuntu/GitHub/sg13g2-dll/.loom/worktrees/issue-62/sim/cp-currents/results/20261106T182524Z/delay-sanity.record.md`.

| corner | I_up uA | I_dn uA | mismatch | leak nA | I(Vdd) idle uA | both-on net uA | Q_up fC (I*200ps) | Q_dn fC (I*200ps) | VDUMP-VOUT mV (0.3/0.6/0.9 V) | dump slope | K_dl ns/V | K_dl*I/C |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| mos_tt/1.2V/27C | 9.13 | 11.07 | 0.19 | -8.10 | 50.2 | -1.94 | 2.43 (1.83) | 2.85 (2.21) | 4/-8/-29 | 0.95 | 1.18 | 0.013 |
| mos_ss/1.08V/125C | 5.14 | 6.44 | 0.22 | -41.20 | 29.0 | -1.30 | 0.87 (1.03) | 1.58 (1.29) | 2/-14/-73 | 0.88 | 0.83 | 0.005 |
| mos_ff/1.32V/-40C | 16.63 | 18.55 | 0.11 | 2.70 | 87.8 | -1.92 | 5.02 (3.33) | 4.95 (3.71) | 8/-2/-14 | 0.96 | 4.91 | 0.091 |

Charge-per-pulse columns are NOT a usable result: the DN window contains an unexplained late current spike (see the qw_dn_min measurement in the envelope), the UP charge is dominated by switching injection, and neither was graded. K1-K5 do not depend on them.

K_dl is a secant between the two 1 GHz Vc points of the delay-sanity record whose mid delay is nearest T; the ss line does not reach T at 1 GHz (decision 0010), so its K_dl is at the fastest-reachable end.

RESULT: PASS
