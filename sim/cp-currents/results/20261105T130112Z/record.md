# cp-currents record

Charge pump (`design/cp.sch`) with `cp_bias`, VOUT held by an ideal source at 0.6 V, reduced corner set (tt/1.2 V/27 C, ss/1.08 V/125 C, ff/1.32 V/-40 C), one `klt sim` request.
Simulated, never measured. Criteria K1-K6 are in `sim/cp-currents/summarize.py`.

Delay-sanity record for K_dl: `sim/cp-currents/results/20261105T130112Z//delay-sanity.record.md`.

| corner | I_up uA | I_dn uA | mismatch | leak nA | I(Vdd) idle uA | both-on net uA | Q_up fC (I*200ps) | Q_dn fC (I*200ps) | VDUMP-VOUT mV (0.3/0.6/0.9 V) | dump slope | K_dl ns/V | K_dl*I/C |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| mos_tt/1.2V/27C | 3.51 | 3.65 | 0.04 | -61.29 | 12.2 | -0.14 | -0.89 (0.70) | 529.58 (0.73) | -460/-528/-76 | 1.64 | 1.18 | 0.004 |
| mos_ss/1.08V/125C | 2.09 | 2.12 | 0.02 | -43.75 | 7.2 | -0.04 | -1.78 (0.42) | 396.36 (0.42) | -475/-544/-79 | 1.66 | 0.83 | 0.002 |
| mos_ff/1.32V/-40C | 6.18 | 5.98 | 0.03 | -81.89 | 20.4 | 0.19 | 0.05 (1.24) | 684.89 (1.20) | -437/-502/-74 | 1.61 | 4.91 | 0.030 |

Charge-per-pulse columns are NOT a usable result: the DN window contains an unexplained late current spike (see the qw_dn_min measurement in the envelope), the UP charge is dominated by switching injection, and neither was graded. K1-K5 do not depend on them.

K_dl is a secant between the two 1 GHz Vc points of the delay-sanity record whose mid delay is nearest T; the ss line does not reach T at 1 GHz (decision 0010), so its K_dl is at the fastest-reachable end.

RESULT: FAIL
- mos_tt/1.2V/27C: K1 current 3.5/3.7 uA outside 5..40 uA
- mos_tt/1.2V/27C: K5 dump slope 1.64
- mos_ss/1.08V/125C: K1 current 2.1/2.1 uA outside 5..40 uA
- mos_ss/1.08V/125C: K3 leakage -43.8 nA
- mos_ss/1.08V/125C: K5 dump slope 1.66
- mos_ff/1.32V/-40C: K5 dump slope 1.61
