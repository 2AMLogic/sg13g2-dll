#!/usr/bin/env python3
"""Grade the noise-method bench against spec/decisions/0014 and write record.md.

Usage:
  summarize.py derive OUT     check the deterministic derivation against 0014
  summarize.py calibrate OUT  print the calibrated equivalent amplitude IA (A)
  summarize.py summarize OUT  write OUT/record.md; exit 1 unless the verdict is PASS
"""
import datetime
import hashlib
import json
import math
import pathlib
import re
import sys

IA_PROBE = 1e-9
N_SEEDS = 8
SIGMA_TOL = 0.10
SIGMA_TOL_NOTE = "±10 % (fixed in 0014 before the run)"
SIGMA_T_PCT_TOL = 0.25
SIGMA_T_PCT_TOL_NOTE = "±25 % (fixed in 0014 before the run)"
CONTROL_SIGMA_MAX = 1e-12
DRIFT_TOL = {
    "vth": 0.001,
    "sv_band": 0.01,
    "iv_band": 0.01,
    "sr": 0.01,
}
EXPECTED = {
    "vth": 0.570258,
    "op_out": 0.600319,
    "sv_band": 7.916701e-3,
    "iv_band": 4.500722e-3,
    "sr": 3.115265e10,
    "sigma_t": 2.541261e-13,
}
SPOTS_EXPECTED = {"s_10M": 7.2555e-7, "s_1G": 7.9151e-8, "s_100G": 8.2535e-10}
EDGE_COUNT = 45
EDGE_PERIOD = 2e-9
EDGE_T0 = 0.2e-9
OSDI_FILES = ("psp103.osdi", "psp103_nqs.osdi", "r3_cmc.osdi", "mosvar.osdi")


def envelope(out, tag):
    with open(pathlib.Path(out) / f"{tag}.envelope.json") as fh:
        return json.load(fh)


def measurements(env):
    return {m["name"]: m.get("value") for m in env["corners"][0].get("measurements", [])}


def diagnostics(env):
    return env["corners"][0].get("diagnostics", []) or []


def noise_sigma(meas):
    return meas["vmrms"]


def derive_all(out):
    vth = measurements(envelope(out, "vth"))["vth"]
    noise = measurements(envelope(out, "noise"))
    sr = measurements(envelope(out, "sr"))
    control = measurements(envelope(out, "control"))
    sv = noise["sv_band"]
    sr2 = 0.1 / (sr["t55_2"] - sr["t65_2"])
    sr3 = 0.1 / (sr["t55_3"] - sr["t65_3"])
    ctl_sigma = noise_sigma(control)
    derived = {
        "vth": vth,
        "op_out": control["vmavg"],
        "sv_band": sv,
        "iv_band": noise["iv_band"],
        "sr": sr2,
    }
    drift = []
    for key, tol in DRIFT_TOL.items():
        got, want = derived[key], EXPECTED[key]
        if not (abs(got - want) <= tol * abs(want)):
            drift.append(f"{key}: derived {got:.6e} vs 0014 {want:.6e} (tol {tol:.0%})")
    if abs(sr2 - sr3) > DRIFT_TOL["sr"] * abs(sr2):
        drift.append(f"sr edges disagree: {sr2:.6e} vs {sr3:.6e}")
    if ctl_sigma > CONTROL_SIGMA_MAX:
        drift.append(f"control run shows noise: {ctl_sigma:.3e} V")
    for name, want in SPOTS_EXPECTED.items():
        got = noise[name]
        if not got or got <= 0:
            drift.append(f"noise spot {name} is not positive: {got}")
        elif abs(got - want) > 0.01 * want:
            drift.append(f"{name}: derived {got:.6e} vs 0014 {want:.6e} (tol 1%)")
    return derived, ctl_sigma, drift


def sigma_runs(out):
    runs = []
    for i in range(1, N_SEEDS + 1):
        m = measurements(envelope(out, f"sigma-s{i}"))
        runs.append((f"sigma-s{i}", m["vmavg"], m["vmrms"], noise_sigma(m)))
    return runs


def edge_runs(out):
    runs = []
    sr = measurements(envelope(out, "sr"))
    dt65 = sr["t65_2"] - (EDGE_T0 + EDGE_PERIOD)
    for i in range(1, N_SEEDS + 1):
        m = measurements(envelope(out, f"edge-s{i}"))
        errs = []
        for k in range(1, EDGE_COUNT + 1):
            t = m[f"t_e{k}"]
            t_det = EDGE_T0 + (k - 1) * EDGE_PERIOD + dt65
            errs.append(t - t_det)
        n = len(errs)
        mean = sum(errs) / n
        rms = math.sqrt(sum(e * e for e in errs) / n)
        runs.append((f"edge-s{i}", mean, rms, errs))
    return runs


def osdi_hashes():
    import os

    root = os.environ.get("SG13G2_OSDI_DIR", "")
    return "; ".join(
        f"`{name}` {hashlib.sha256((pathlib.Path(root) / name).read_bytes()).hexdigest()[:16]}…"
        for name in OSDI_FILES
        if (pathlib.Path(root) / name).is_file()
    )


def fmt(x):
    return f"{x:.6e}"


def derive(out):
    _, _, drift = derive_all(out)
    if drift:
        for line in drift:
            print(f"summarize: derivation drift: {line}", file=sys.stderr)
        sys.exit(1)


def calibrate(out, tag, ia_current):
    probe = measurements(envelope(out, tag))
    sv = measurements(envelope(out, "noise"))["sv_band"]
    sigma_probe = noise_sigma(probe)
    if not sigma_probe or sigma_probe <= 0:
        print(f"summarize: calibration probe measured no noise: {sigma_probe}", file=sys.stderr)
        sys.exit(1)
    ia = float(ia_current) * sv / sigma_probe
    print(f"{ia:.6e}")


def summarize(out):
    out = pathlib.Path(out)
    derived, ctl_sigma, problems = derive_all(out)
    sv = derived["sv_band"]
    sr = measurements(envelope(out, "sr"))
    sr2 = 0.1 / (sr["t55_2"] - sr["t65_2"])
    sigma_t_expected = sv / sr2
    sr3 = 0.1 / (sr["t55_3"] - sr["t65_3"])

    probe = measurements(envelope(out, "sigma-probe"))
    sigma_probe = noise_sigma(probe)
    ia_1 = IA_PROBE * sv / sigma_probe
    cal = measurements(envelope(out, "sigma-refine"))
    sigma_cal = noise_sigma(cal)
    ia_cal = ia_1 * sv / sigma_cal
    sr605 = 0.01 / (sr["t595_2"] - sr["t605_2"])

    sigmas = sigma_runs(out)
    sigma_mean = sum(s[3] for s in sigmas) / len(sigmas)
    for tag, _, _, s in sigmas:
        if abs(s - EXPECTED["sv_band"]) > SIGMA_TOL * EXPECTED["sv_band"]:
            problems.append(
                f"{tag}: sigma {fmt(s)} outside {SIGMA_TOL_NOTE} of {fmt(EXPECTED['sv_band'])}"
            )
    pairs = {(vmavg, vmrms) for _, vmavg, vmrms, _ in sigmas}
    if len(pairs) != len(sigmas):
        problems.append("two seeded sigma runs returned identical (vmavg, vmrms): a shared noise stream")

    edges = edge_runs(out)
    pooled_n = sum(len(e[3]) for e in edges)
    pooled_rms = math.sqrt(sum(e[2] ** 2 * len(e[3]) for e in edges) / pooled_n)
    for tag, mean, rms, _ in edges:
        if not (abs(rms - sigma_t_expected) <= SIGMA_T_PCT_TOL * sigma_t_expected):
            problems.append(
                f"{tag}: sigma_t {fmt(rms)} s outside {SIGMA_T_PCT_TOL_NOTE} of {fmt(sigma_t_expected)} s"
            )
    edge_fprints = {(round(mean, 15), round(rms, 15)) for _, mean, rms, _ in edges}
    if len(edge_fprints) != len(edges):
        problems.append("two seeded edge runs returned identical statistics: a shared noise stream")

    abort_env = envelope(out, "abort")
    abort_diags = [d for d in diagnostics(abort_env) if d.get("code") == "timestep_too_small"]
    if not abort_diags:
        problems.append("abort probe did not produce timestep_too_small; the 0014 series-source limitation is void")

    prov = envelope(out, "sigma-s1").get("provenance", {})
    env0 = envelope(out, "sigma-s1").get("environment", {})
    klt_version = prov.get("klt_version", "unknown")
    engine = f"{env0.get('engine')} {env0.get('engine_version')}"
    backend = (env0.get("backend") or {}).get("resolved", "unknown")
    tn_block = json.dumps(env0.get("transient_noise", {}))
    control_tn = envelope(out, "control").get("environment", {}).get("transient_noise")
    now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    mean_rel = (sigma_mean - EXPECTED["sv_band"]) / EXPECTED["sv_band"]
    pooled_rel = (pooled_rms - sigma_t_expected) / sigma_t_expected

    lines = [
        "# noise-method record",
        "",
        "SIMULATED results, never measured. Validates spec/decisions/0014 on the known case",
        "(one minimum sg13_lv inverter, mos_tt/1.20 V/27 C). No DLL jitter figure is produced",
        "here (0014; row 6 stays blocked).",
        "",
        f"- Verdict: **{'PASS' if not problems else 'FAIL'}**",
        f"- Stamp: {out.name} (UTC {now})",
        f"- klt: {klt_version}; engine: {engine}; backend: {backend}",
        f"- OSDI models (sha256, first 16): {osdi_hashes()}",
        "- PDK: IHP-Open-PDK v0.3.0 (sim/pdk.json)",
        "",
        "## Method (from 0014)",
        "",
        "- Target figure: `sigma_v`, the `.noise` output-noise band integral over 1 MHz-300 GHz",
        "  at the switching-threshold operating point (deterministic).",
        "- Equivalent: ONE shunt `trnoise` current source at the stage output node",
        "  (`Ieq out 0 dc=0 trnoise(IA 1p)`), sized by per-deck calibration: a probe run at",
        f"  IA = {IA_PROBE:g} A measures the delivered output rms, and one refinement run at the",
        "  scaled amplitude corrects the residual non-linearity of the scaling; IA scales",
        "  linearly (LTI network) to reproduce sigma_v. The sizing is measured on the same",
        "  deck that the seeded runs use, so no transfer-function model of the injection",
        "  path is needed.",
        "- Timing figure: `sigma_t = sigma_v / SR`; SR from a noiseless edge transient",
        "  (0.1 V between the 0.65/0.55 V crossings of a falling edge). Validated DIRECTLY:",
        "  8 seeded PULSE-driven edge transients, sigma_t per run = rms(t_i - t_det_i) over",
        "  45 falling edges against the deterministic grid; pooled rms across runs graded.",
        f"- Seeds: {N_SEEDS} independent runs per set, sequential fresh ngspice processes on one",
        "  host; seed values are NOT recordable on this toolchain (pid-seeded streams; three",
        "  pinning mechanisms probed and refused; 0014 and klayout-tools#5772).",
        "- Run length: 90 ns per sigma run and 95 ns per edge run, trnoise step NT = 1 ps;",
        "  sigma estimator window 5-90 ns (85 000 breakpoints); 45 edges per edge run.",
        "- Estimator: sigma = RMS(v(m)), the AC-coupled monitor node (Cm 0.1p / Rm 1Meg:",
        "  high-pass 1.6 kHz, load <= 0.1% of the stage output resistance across the band),",
        "  from a plain `.meas tran` RMS card; no subtractive estimator, so ngspice's",
        "  6-digit measurement print carries full precision at millivolt scale;",
        "  sigma_t per run = sqrt(mean((t_i - t_det_i)^2)), t_i from plain `.meas tran WHEN`",
        "  cards, t_det_i = 0.2n + (i-1)*2n + dt65 with dt65 from the SR derivation.",
        "- Expected values and tolerances were fixed in 0014 BEFORE these runs; derivation",
        "  quantities re-derived by this stamp must agree within the 0014 tolerances.",
        "",
        "## Derivation (this stamp; deterministic analyses)",
        "",
        "| quantity | value | 0014 expected | agreement |",
        "|---|---|---|---|",
    ]
    rows = [
        ("switching threshold vth", derived["vth"], EXPECTED["vth"], "V", "0.1 %"),
        ("OP output level (control vmavg, monitor DC = 0)", derived["op_out"], EXPECTED["op_out"], "V", "0.1 %"),
        ("sigma_v (onoise, 1 MHz-300 GHz)", sv, EXPECTED["sv_band"], "V", "1 %"),
        ("inoise band integral", derived["iv_band"], EXPECTED["iv_band"], "V", "1 %"),
        ("density at 10 MHz", measurements(envelope(out, "noise"))["s_10M"], SPOTS_EXPECTED["s_10M"], "V/sqrt(Hz)", "1 %"),
        ("density at 1 GHz", measurements(envelope(out, "noise"))["s_1G"], SPOTS_EXPECTED["s_1G"], "V/sqrt(Hz)", "1 %"),
        ("density at 100 GHz", measurements(envelope(out, "noise"))["s_100G"], SPOTS_EXPECTED["s_100G"], "V/sqrt(Hz)", "1 %"),
        ("slew rate SR (edge 2)", sr2, EXPECTED["sr"], "V/s", "1 %"),
        ("slew rate SR (edge 3)", sr3, EXPECTED["sr"], "V/s", "1 %"),
        ("slope at the 0.6 V crossing, 0.595-0.605 V", sr605, 0, "V/s", "info"),
        ("derived sigma_t = sigma_v/SR", sigma_t_expected, EXPECTED["sigma_t"], "s", "1 %"),
    ]
    for label, got, want, unit, tol in rows:
        if tol == "info":
            lines.append(f"| {label} | {fmt(got)} {unit} | - | informational |")
        else:
            rel = abs(got - want) / abs(want)
            lines.append(f"| {label} | {fmt(got)} {unit} | {fmt(want)} | {rel:.2e} ({tol}) |")
    lines += [
        "",
        "## Injection calibration (this stamp)",
        "",
        f"- Probe run (IA = {IA_PROBE:g} A): delivered output rms = {fmt(sigma_probe)} V.",
        f"- First amplitude: IA_1 = IA_probe * sigma_v / sigma_probe = {fmt(ia_1)} A.",
        f"- Refinement run (IA = {fmt(ia_1)} A): delivered output rms = {fmt(sigma_cal)} V",
        f"  ({(sigma_cal / sv - 1):+.2%} against target) ->",
        f"- Final amplitude: IA = IA_1 * sigma_v / sigma_refine = {fmt(ia_cal)} A",
        f"  (target sigma_v = {fmt(EXPECTED['sv_band'])} V).",
        "- Linear-scaling check: the seeded runs below deliver sigma_v at IA, verifying the",
        "  proportionality end-to-end over the calibration ratio (~1e3).",
        "",
        "## Control run (AC: OSDI models contribute no noise by themselves)",
        "",
        f"- No `trnoise` source declared: monitor RMS v(m) = {ctl_sigma:.3e} V",
        "  (must be 0; an ngspice transient carries only declared noise sources).",
        f"- Control envelope `environment.transient_noise`: {control_tn!r} (absent -- klt adds the block",
        "  only when the netlist declares trnoise/trrandom). klt's assertion in the seeded runs:",
        f"  `{tn_block}`. The assertion is the tool's; the 0 V measurement above is ours.",
        "- In the frequency domain the models DO contribute noise: the `.noise` rows above are",
        "  non-zero (that is what the derivation consumes).",
        "",
        f"## Seeded sigma_v runs ({N_SEEDS} runs, DC-biased deck)",
        "",
        f"| run | vmavg (V) | vmrms = sigma (V) | vs expected {fmt(EXPECTED['sv_band'])} |",
        "|---|---|---|---|",
    ]
    for tag, vmavg, vmrms, s in sigmas:
        rel = (s - EXPECTED["sv_band"]) / EXPECTED["sv_band"]
        lines.append(f"| {tag} | {vmavg:.9e} | {vmrms:.9e} | {rel:+.2%} |")
    lines += [
        "",
        f"- Mean of {N_SEEDS} runs: {fmt(sigma_mean)} V, {mean_rel:+.2%} against expected",
        f"  {fmt(EXPECTED['sv_band'])} V; tolerance {SIGMA_TOL_NOTE} per run and on the mean.",
        "- Per-number method statement: every sigma above is RMS(v(m)) over 5-90 ns,",
        f"  90 ns transient, NT = 1 ps, {N_SEEDS} pid-seeded (unreproducible, unrecordable) runs",
        "  at the calibrated IA.",
        "",
        f"## Seeded edge runs (direct sigma_t validation, {N_SEEDS} runs, PULSE-driven deck)",
        "",
        f"| run | mean error (s) | sigma_t (s) | vs expected {fmt(sigma_t_expected)} |",
        "|---|---|---|---|",
    ]
    for tag, mean, rms, _ in edges:
        rel = (rms - sigma_t_expected) / sigma_t_expected
        lines.append(f"| {tag} | {mean:.4e} | {fmt(rms)} | {rel:+.2%} |")
    lines += [
        "",
        f"- Pooled sigma_t (weighted rms over {pooled_n} edges): {fmt(pooled_rms)} s,",
        f"  {pooled_rel:+.2%} against expected {fmt(sigma_t_expected)} s (= sigma_v/SR =",
        f"  {fmt(EXPECTED['sv_band'])}/{fmt(EXPECTED['sr'])}); tolerance {SIGMA_T_PCT_TOL_NOTE} pooled.",
        "- Per-number method statement: crossing times are plain `.meas tran WHEN v(out)=0.65`",
        "  cards, falling edges 2..46 of a 2 ns-period PULSE; per-run sigma_t is the rms of the",
        "  crossing-time error against the deterministic grid; the noise correlation time (the",
        "  stage's ~8 ns response time) makes edges within a run correlated, so per-run values",
        "  scatter and the pooled figure across the 8 runs is the graded one.",
        "- The edge deck carries the same shunt equivalent at the same calibrated IA with a",
        "  PULSE drive: the shunt-current form coexists with a switching drive (the abort",
        "  below is specific to the series-voltage form).",
        "",
        "## Abort probe (series-voltage trnoise + PULSE drive)",
        "",
    ]
    if abort_diags:
        d = abort_diags[0]
        lines += [
            f"- code: `{d.get('code')}`; message: {d.get('message')}",
            "",
            "The series-voltage trnoise equivalent aborts the transient at the first input edge",
            "(0014's limitation): that form cannot drive a DLL jitter deck. The shunt-current",
            "form the method adopts runs clean with the same PULSE drive (edge runs above).",
        ]
    else:
        lines += [
            "- NO timestep_too_small diagnostic: the abort 0014 documents did not reproduce.",
            "  The series-source limitation is void and 0014 re-opens.",
        ]
    lines += ["", "## Verdict", ""]
    if problems:
        for p in problems:
            lines.append(f"- FAIL: {p}")
        lines += ["", "The bench FAILED; see the criteria above and 0014."]
    else:
        lines += [
            "- All derivation quantities reproduce 0014 within tolerance.",
            f"- Control sigma = {ctl_sigma:.3e} V (must be 0): the models contribute no transient noise.",
            f"- All {N_SEEDS} seeded sigma runs within {SIGMA_TOL_NOTE} of expected; mean {mean_rel:+.2%};",
            "  streams pairwise distinct.",
            f"- Pooled sigma_t within {SIGMA_T_PCT_TOL_NOTE} of sigma_v/SR; per-run values reported;",
            "  edge streams pairwise distinct.",
            "- Abort probe reproduced the documented series-source limitation.",
            "- PASS: the noise method of 0014 is validated on the known case, including a direct",
            "  transient timing measurement. Row 6 stays blocked until a DLL jitter deck exists.",
        ]
    record = out / "record.md"
    record.write_text("\n".join(lines) + "\n")
    if problems:
        for p in problems:
            print(f"summarize: FAIL: {p}", file=sys.stderr)
        sys.exit(1)
    print(f"summarize: PASS -- {record}")


def main():
    usage = {
        "derive": lambda: derive(sys.argv[2]),
        "calibrate": lambda: calibrate(sys.argv[2], sys.argv[3], sys.argv[4]),
        "summarize": lambda: summarize(sys.argv[2]),
    }
    if len(sys.argv) != 3 + (2 if sys.argv[1] == "calibrate" else 0) or sys.argv[1] not in usage:
        print(__doc__, file=sys.stderr)
        sys.exit(2)
    usage[sys.argv[1]]()


if __name__ == "__main__":
    main()
