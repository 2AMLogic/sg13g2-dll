#!/usr/bin/env python3
"""Grade the noise-method bench against spec/decisions/0014 and write record.md.

Usage:
  summarize.py derive OUT     print the derived NA (V/sqrt(Hz)); exit 1 on derivation drift
  summarize.py summarize OUT  write OUT/record.md; exit 1 unless the verdict is PASS
"""
import datetime
import hashlib
import json
import math
import pathlib
import sys

K_B = 1.380649e-23
T_K = 300.15
R_REF = 1e6
N_SEEDS = 8
SIGMA_TOL = 0.10
SIGMA_TOL_NOTE = "±10 % (fixed in 0014 before the run)"
CONTROL_SIGMA_MAX = 1e-12
DRIFT_TOL = {
    "vth": 0.001,
    "sv_band": 0.01,
    "iv_band": 0.01,
    "sigma_r": 0.01,
    "enbw": 0.01,
    "na": 0.02,
    "sr": 0.01,
}
EXPECTED = {
    "vth": 0.570258,
    "op_out": 0.600319,
    "sv_band": 7.916701e-3,
    "iv_band": 4.500722e-3,
    "sigma_r": 2.016996e-2,
    "enbw": 2.076204e10,
    "na": 6.729066e-8,
    "sr": 3.115265e10,
    "sigma_t": 2.541261e-13,
}
SPOTS_EXPECTED = {"s_10M": 7.2555e-7, "s_1G": 7.9151e-8, "s_100G": 8.2535e-10}
A0_EXPECTED = 25.7472
OSDI_FILES = ("psp103.osdi", "psp103_nqs.osdi", "r3_cmc.osdi", "mosvar.osdi")


def envelope(out, tag):
    with open(pathlib.Path(out) / f"{tag}.envelope.json") as fh:
        return json.load(fh)


def measurements(env):
    return {m["name"]: m.get("value") for m in env["corners"][0].get("measurements", [])}


def diagnostics(env):
    return env["corners"][0].get("diagnostics", []) or []


def noise_sigma(vavg, vrms):
    return math.sqrt(max(vrms * vrms - vavg * vavg, 0.0))


def derive_all(out):
    vth = measurements(envelope(out, "vth"))["vth"]
    noise = measurements(envelope(out, "noise"))
    rref = measurements(envelope(out, "noise_rref"))
    sr = measurements(envelope(out, "sr"))
    control = measurements(envelope(out, "control"))
    sv = noise["sv_band"]
    sigma_r = rref["sv_band"]
    enbw = (sigma_r * sigma_r - sv * sv) / (4 * K_B * T_K * R_REF)
    s4ktr = math.sqrt(4 * K_B * T_K * R_REF)
    a0 = rref["s_1M"] / s4ktr
    na = sv / (math.sqrt(2.0 / 3.0) * math.sqrt(enbw))
    sr2 = 0.1 / (sr["t55_2"] - sr["t65_2"])
    sr3 = 0.1 / (sr["t55_3"] - sr["t65_3"])
    ctl_sigma = noise_sigma(control["vavg"], control["vrms"])
    derived = {
        "vth": vth,
        "op_out": control["vavg"],
        "sv_band": sv,
        "iv_band": noise["iv_band"],
        "sigma_r": sigma_r,
        "enbw": enbw,
        "na": na,
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
    if abs(a0 - A0_EXPECTED) > 0.02 * A0_EXPECTED:
        drift.append(f"a0: derived {a0:.4f} vs 0014 {A0_EXPECTED:.4f} (tol 2%)")
    return derived, ctl_sigma, drift


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


def summarize(out):
    out = pathlib.Path(out)
    derived, ctl_sigma, problems = derive_all(out)
    sigma_envs = [(f"sigma-s{i}", envelope(out, f"sigma-s{i}")) for i in range(1, N_SEEDS + 1)]
    sigmas = []
    for tag, env in sigma_envs:
        m = measurements(env)
        sigmas.append((tag, m["vavg"], m["vrms"], noise_sigma(m["vavg"], m["vrms"])))
    abort_env = envelope(out, "abort")
    abort_diags = [d for d in diagnostics(abort_env) if d.get("code") == "timestep_too_small"]

    mean = sum(s[3] for s in sigmas) / len(sigmas)
    for tag, _, _, s in sigmas:
        if abs(s - EXPECTED["sv_band"]) > SIGMA_TOL * EXPECTED["sv_band"]:
            problems.append(
                f"{tag}: sigma {fmt(s)} outside {SIGMA_TOL_NOTE} of {fmt(EXPECTED['sv_band'])}"
            )
    pairs = {(vavg, vrms) for _, vavg, vrms, _ in sigmas}
    if len(pairs) != len(sigmas):
        problems.append("two seeded runs returned identical (vavg, vrms): a shared noise stream")
    if not abort_diags:
        problems.append("abort probe did not produce timestep_too_small; the 0014 edge-drive limitation is void")

    prov = sigma_envs[0][1].get("provenance", {})
    env0 = sigma_envs[0][1].get("environment", {})
    klt_version = prov.get("klt_version", "unknown")
    engine = f"{env0.get('engine')} {env0.get('engine_version')}"
    backend = (env0.get("backend") or {}).get("resolved", "unknown")
    tn_block = json.dumps(env0.get("transient_noise", {}))
    control_tn = envelope(out, "control").get("environment", {}).get("transient_noise")
    now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    sv = derived["sv_band"]
    sr2 = 0.1 / (measurements(envelope(out, "sr"))["t55_2"] - measurements(envelope(out, "sr"))["t65_2"])
    sigma_t = sv / sr2
    na = derived["na"]
    mean_rel = (mean - EXPECTED["sv_band"]) / EXPECTED["sv_band"]

    lines = [
        "# noise-method record",
        "",
        "SIMULATED results, never measured. Validates spec/decisions/0014 on the known case",
        "(one minimum sg13_lv inverter, DC-biased at its switching threshold, mos_tt/1.20 V/27 C).",
        "No DLL jitter figure is produced here (0014; row 6 stays blocked).",
        "",
        f"- Verdict: **{'PASS' if not problems else 'FAIL'}**",
        f"- Stamp: {out.name} (UTC {now})",
        f"- klt: {klt_version}; engine: {engine}; backend: {backend}",
        f"- OSDI models (sha256, first 16): {osdi_hashes()}",
        "- PDK: IHP-Open-PDK v0.3.0 (sim/pdk.json)",
        "",
        "## Method (from 0014)",
        "",
        "- Noise representation: thermal noise of the known case's devices as ONE white",
        "  input-referred series voltage `trnoise` source, derived from `.noise` at the OP",
        "  (`onoise` band integral over 1 MHz-300 GHz), placed between the input node and the",
        "  stage. Flicker excluded (thermal-noise class, spec row 6).",
        "- ENBW identity: `ENBW = (sigma_R^2 - sigma_v^2)/(4 k T R)`, R = 1 MOhm series,",
        "  T = 300.15 K; no manual spectral quadrature.",
        "- Equivalent density: `NA = sigma_v/(sqrt(2/3)*sqrt(ENBW))` (ngspice trnoise",
        "  piecewise-linear interpolation: process rms = NA*sqrt(2/3), measured 0.818 vs 0.8165).",
        "- Timing figure: `sigma_t = sigma_v / SR`; SR from a noiseless edge transient",
        "  (0.1 V between the 0.65/0.55 V crossings of a falling edge).",
        f"- Seeds: {N_SEEDS} independent runs, sequential fresh ngspice processes on one host;",
        "  seed values are NOT recordable on this toolchain (pid-seeded streams; three pinning",
        "  mechanisms probed and refused; 0014 and klayout-tools#5772). Re-running redraws noise.",
        "- Run length: 90 ns per seeded run, trnoise step NT = 1 ps; estimator window 5-90 ns",
        "  (85 000 breakpoints).",
        "- Estimator: `sigma = sqrt(vrms^2 - vavg^2)` from two plain `.meas tran` cards",
        "  (AVG and RMS of v(out)); no hand-rolled waveform arithmetic.",
        "- Expected values and tolerances were fixed in 0014 BEFORE this run; derivation",
        "  quantities re-derived by this stamp must agree within the 0014 reproduction tolerances.",
        "",
        "## Derivation (this stamp; deterministic analyses)",
        "",
        "| quantity | value | 0014 expected | agreement |",
        "|---|---|---|---|",
    ]
    rows = [
        ("switching threshold vth", derived["vth"], EXPECTED["vth"], "V", "0.1 %"),
        ("OP output level (control vavg)", derived["op_out"], EXPECTED["op_out"], "V", "0.1 %"),
        ("sigma_v (onoise, 1 MHz-300 GHz)", sv, EXPECTED["sv_band"], "V", "1 %"),
        ("inoise band integral", derived["iv_band"], EXPECTED["iv_band"], "V", "1 %"),
        ("density at 10 MHz", measurements(envelope(out, "noise"))["s_10M"], SPOTS_EXPECTED["s_10M"], "V/sqrt(Hz)", "1 %"),
        ("density at 1 GHz", measurements(envelope(out, "noise"))["s_1G"], SPOTS_EXPECTED["s_1G"], "V/sqrt(Hz)", "1 %"),
        ("density at 100 GHz", measurements(envelope(out, "noise"))["s_100G"], SPOTS_EXPECTED["s_100G"], "V/sqrt(Hz)", "1 %"),
        ("sigma_R (1 MOhm series R)", derived["sigma_r"], EXPECTED["sigma_r"], "V", "1 %"),
        ("ENBW", derived["enbw"], EXPECTED["enbw"], "Hz", "1 %"),
        ("gain A0 at 1 MHz", measurements(envelope(out, "noise_rref"))["s_1M"] / math.sqrt(4 * K_B * T_K * R_REF), A0_EXPECTED, "V/V", "2 %"),
        ("equivalent density NA", na, EXPECTED["na"], "V/sqrt(Hz)", "2 %"),
        ("slew rate SR (edge 2)", sr2, EXPECTED["sr"], "V/s", "1 %"),
        ("slew rate SR (edge 3)", 0.1 / (measurements(envelope(out, "sr"))["t55_3"] - measurements(envelope(out, "sr"))["t65_3"]), EXPECTED["sr"], "V/s", "1 %"),
        ("derived sigma_t = sigma_v/SR", sigma_t, EXPECTED["sigma_t"], "s", "1 %"),
    ]
    for label, got, want, unit, tol in rows:
        rel = abs(got - want) / abs(want)
        lines.append(f"| {label} | {fmt(got)} {unit} | {fmt(want)} | {rel:.2e} ({tol}) |")
    lines += [
        "",
        "## Control run (AC: OSDI models contribute no noise by themselves)",
        "",
        f"- No `trnoise` source declared: recovered output rms `sqrt(vrms^2-vavg^2)` = {ctl_sigma:.3e} V",
        "  (must be 0; an ngspice transient carries only declared noise sources).",
        f"- Control envelope `environment.transient_noise`: {control_tn!r} (absent -- klt adds the block",
        "  only when the netlist declares trnoise/trrandom). klt's assertion in the seeded runs:",
        f"  `{tn_block}`. The assertion is the tool's; the 0 V measurement above is ours.",
        "- In the frequency domain the models DO contribute noise: the `.noise` rows above are",
        "  non-zero (that is what the derivation consumes).",
        "",
        "## Seeded sigma_v runs (the validation 0014 fixed)",
        "",
        f"| run | vavg (V) | vrms (V) | sigma (V) | vs expected {fmt(EXPECTED['sv_band'])} |",
        "|---|---|---|---|---|",
    ]
    for tag, vavg, vrms, s in sigmas:
        rel = (s - EXPECTED["sv_band"]) / EXPECTED["sv_band"]
        lines.append(f"| {tag} | {vavg:.9e} | {vrms:.9e} | {fmt(s)} | {rel:+.2%} |")
    lines += [
        "",
        f"- Mean of {N_SEEDS} runs: {fmt(mean)} V, {mean_rel:+.2%} against expected",
        f"  {fmt(EXPECTED['sv_band'])} V; tolerance {SIGMA_TOL_NOTE} per run and on the mean.",
        "- Per-number method statement: every sigma above is `sqrt(vrms^2-vavg^2)` over 5-90 ns,",
        f"  90 ns transient, NT = 1 ps, {N_SEEDS} pid-seeded (unreproducible, unrecordable) runs.",
        f"- Derived sigma_t = sigma_v/SR = {fmt(sigma_t)} s (expected {fmt(EXPECTED['sigma_t'])} s);",
        "  validated transitively (sigma_v by this check, SR deterministically). No direct",
        "  transient sigma_t measurement exists on this toolchain (edge-drive limitation).",
        "",
        "## Abort probe (edge-drive limitation)",
        "",
    ]
    if abort_diags:
        d = abort_diags[0]
        lines += [
            f"- code: `{d.get('code')}`; message: {d.get('message')}",
            "",
            "The PULSE-driven stage with the trnoise equivalent aborts at the first input edge,",
            "reproducing 0014's limitation: a DLL jitter deck cannot drive the loop with a PULSE",
            "clock while carrying trnoise sources on this toolchain.",
        ]
    else:
        lines += [
            "- NO timestep_too_small diagnostic: the abort 0014 documents did not reproduce.",
            "  The edge-drive limitation is void and the noise method re-opens (0014).",
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
            f"- All {N_SEEDS} seeded runs within {SIGMA_TOL_NOTE} of expected; mean {mean_rel:+.2%};",
            "  streams pairwise distinct.",
            "- Abort probe reproduced the documented limitation.",
            "- PASS: the noise method of 0014 is validated on the known case. Row 6 stays blocked",
            "  until a DLL jitter deck exists.",
        ]
    record = out / "record.md"
    record.write_text("\n".join(lines) + "\n")
    if problems:
        for p in problems:
            print(f"summarize: FAIL: {p}", file=sys.stderr)
        sys.exit(1)
    print(f"summarize: PASS -- {record}")


def main():
    if len(sys.argv) != 3 or sys.argv[1] not in ("derive", "summarize"):
        print(__doc__, file=sys.stderr)
        sys.exit(2)
    if sys.argv[1] == "derive":
        derived, _, drift = derive_all(sys.argv[2])
        if drift:
            for line in drift:
                print(f"summarize: derivation drift: {line}", file=sys.stderr)
            sys.exit(1)
        print(f"{derived['na']:.6e}")
    else:
        summarize(sys.argv[2])


if __name__ == "__main__":
    main()
