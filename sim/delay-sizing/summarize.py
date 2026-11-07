#!/usr/bin/env python3
"""Summarize delay-sizing envelopes into record.md (simulated, never measured).

usage: summarize.py {probe|full|mc} OUT_DIR
Per-step rule: step k = d_k - d_(k-1) with d_0 = 0 (T0 is the reference). A has
inverting stages, so rising/falling INPUT edges give different steps; steps are
split by the OUTPUT edge direction at tap k and min/max are over both.
Exit 1 on a missing/errored envelope or diagnostic; unmet targets are recorded,
not hidden (a target miss alone is not an error of the run).
"""
import glob, json, math, os, sys

PERIOD = {"1GHz": 1.0e-9, "500MHz": 2.0e-9}
RAIL = 0.1


def load(p):
    try:
        return json.load(open(p))
    except OSError:
        return None


def rows(env, bad, tag):
    out = []
    for cr in env.get("corners", []):
        for d in cr.get("diagnostics", []):
            bad.append(f"{tag} {cr['corner_id']}: [{d.get('code')}] {str(d.get('message'))[:90]}")
        m = {x["name"]: x.get("value") for x in cr.get("measurements", [])}
        out.append((cr["supply_v"].get("VC"), cr["supply_v"].get("Vdd"), m, cr))
    return sorted(out, key=lambda r: (r[0] if r[0] is not None else -1))


def steps(m, var):
    """-> (rise_out_steps, fall_out_steps, total_rise_in, total_fall_in) or None."""
    dr = [m.get(f"dr{k}") for k in range(1, 9)]
    df = [m.get(f"df{k}") for k in range(1, 9)]
    if any(x is None for x in dr + df):
        return None
    rout, fout = [], []
    for ds, in_rise in ((dr, True), (df, False)):
        prev = 0.0
        for k, d in enumerate(ds, 1):
            s = d - prev
            prev = d
            inv = var == "a" and k % 2 == 1
            out_rise = in_rise != inv
            (rout if out_rise else fout).append(s)
    return rout, fout, dr[7], df[7]


def table(env, var, bad, tag):
    L = ["| Vc (V) | d8 rise-in / fall-in (ps) | mean step (ps) | step min..max, all (ps) | rise-out min..max | fall-out min..max | I(vdd) mean (uA) |",
         "|---|---|---|---|---|---|---|"]
    pts = []
    for vc, vdd, m, cr in rows(env, bad, tag):
        s = steps(m, var)
        ia = m.get("iavg")
        iu = f"{-ia*1e6:.0f}" if ia is not None else "-"
        if s is None:
            L.append(f"| {vc:.2f} | no edge / no value | - | - | - | - | {iu} |")
            continue
        r, f, tr, tf = s
        mean = (tr + tf) / 16
        allv = r + f
        L.append(f"| {vc:.2f} | {tr*1e12:.1f} / {tf*1e12:.1f} | {mean*1e12:.1f} | {min(allv)*1e12:.1f}..{max(allv)*1e12:.1f} | "
                 f"{min(r)*1e12:.1f}..{max(r)*1e12:.1f} | {min(f)*1e12:.1f}..{max(f)*1e12:.1f} | {iu} |")
        pts.append((vc, vdd, mean, min(allv), max(allv), -ia if ia is not None else None))
    return L, pts


def dead_zone(env, vcs_all):
    """Highest Vc with no edge (-> dead zone is at/below it); None if none."""
    dead = []
    for vc, vdd, m, cr in rows(env, [], ""):
        if any(m.get(f"{n}{k}") is None for n in ("dr", "df") for k in range(1, 9)):
            dead.append(vc)
    return max(dead) if dead else None


def main_grid(mode, out):
    Ls = ["# delay-sizing record" + (" (probe)" if mode == "probe" else ""), "",
          "SIMULATED results, never measured. Reduced corner set (`sim/corners.json` reduced_set), NOT the 45-corner grade. "
          "Delay = single-event T0->Tk first edge at 50 % of Vdd (rising input = `dr`, falling input = `df`), ideal control "
          "sources (VBN=Vc, VBP=Vdd-Vc), 20 fF ideal load on every tap buffer, the delay-sanity method. "
          "Current = mean supply current over 6..10 ns (integer clock periods, line toggling). "
          "Tool versions: " + (open(os.path.join(out, "tool-versions.txt")).read().strip() if os.path.exists(os.path.join(out, "tool-versions.txt")) else "?"), ""]
    bad, verdict = [], []
    envs = sorted(glob.glob(os.path.join(out, "*.envelope.json")))
    for p in envs:
        tag = os.path.basename(p)[:-len(".envelope.json")]
        env = load(p)
        parts = tag.split("_")
        var = parts[0][0] if parts[0][0] in "ab" else parts[0]
        if parts[0].startswith("base"):
            var = "base"
        if env is None or "error" in env:
            bad.append(f"{tag}: missing/error {None if env is None else env['error']}"); continue
        fq = "500MHz" if "500MHz" in tag else "1GHz"
        target = PERIOD[fq] / 8
        e = env.get("environment") or {}
        Ls += [f"## {tag} (variant {parts[0]}; T/8 = {target*1e12:.0f} ps; status {env.get('status')}, "
               f"{env.get('passed')}/{env.get('corner_count')} pass; backend {(e.get('backend') or {}).get('resolved','?')}; "
               f"job {(e.get('remote') or {}).get('job_id','-')})", ""]
        L, pts = table(env, var, bad, tag)
        Ls += L + [""]
        dz = dead_zone(env, None)
        usable = [p for p in pts if RAIL <= p[0] <= p[1] - RAIL]
        if usable:
            lo = min(p[2] for p in usable); hi = max(p[2] for p in usable)
            st_lo = min(p[3] for p in usable); st_hi = max(p[4] for p in usable)
            cov = lo <= target <= hi
            win = [p[0] for p in usable if p[2] <= 1e30]
            Ls += [f"Usable Vc window (>=100 mV from both rails, edge present): {min(win):.2f}..{max(win):.2f} V; dead zone: "
                   + (f"no edge at Vc <= {dz:.2f} V" if dz is not None else "none in the swept range")
                   + f". Mean step {lo*1e12:.1f}..{hi*1e12:.1f} ps; individual step min/max over the window {st_lo*1e12:.1f}..{st_hi*1e12:.1f} ps; "
                   f"T/8 **{'covered' if cov else 'NOT covered'}**. Fastest mean step (any Vc) {min(p[2] for p in pts)*1e12:.1f} ps.", ""]
            verdict.append((tag, cov, min(p[2] for p in pts), dz))
        else:
            Ls += ["No usable delay points.", ""]
            verdict.append((tag, False, None, dz))
    Ls += ["## Target check (mean tap step span contains T/8, usable window)", ""]
    Ls += [f"- {t}: {'covered' if c else 'NOT covered'}; fastest mean step "
           + (f"{f*1e12:.1f} ps" if f else "n/a") + f"; dead zone top {dz}" for t, c, f, dz in verdict]
    Ls += ["", "## Run status", "", ("ERRORS:" if bad else "no diagnostics / errors")] + [f"- {b}" for b in bad]
    open(os.path.join(out, "record.md"), "w").write("\n".join(Ls) + "\n")
    print("\n".join(Ls[-(len(verdict) + len(bad) + 6):]))
    return 1 if bad else 0


def sd(v):
    n = len(v)
    mu = sum(v) / n
    return math.sqrt(sum((x - mu) ** 2 for x in v) / (n - 1)) if n > 1 else 0.0


def main_mc(out):
    Ls = ["# delay-sizing Monte Carlo matching record", "",
          "SIMULATED, never measured. ss/1.08 V/125 C, 1 GHz, one Vc, mismatch-only Monte Carlo (`mos_ss_mismatch`); "
          "negative control on `mos_ss` (no mismatch) must give sigma exactly 0 and repeat identically.", ""]
    bad = []
    for v in ("a", "b"):
        env = load(os.path.join(out, f"{v}_mc_ss_1GHz.envelope.json"))
        ctl = load(os.path.join(out, f"{v}_ctl_ss_1GHz.envelope.json"))
        rep = load(os.path.join(out, f"{v}_ctl_repeat_ss_1GHz.envelope.json"))
        if env is None or "error" in env:
            bad.append(f"{v} mc missing/error"); continue
        mc = (env.get("environment") or {}).get("monte_carlo")
        Ls += [f"## candidate {v.upper()}: n={len(env.get('corners', []))} runs, monte_carlo {json.dumps(mc)}; "
               f"job {((env.get('environment') or {}).get('remote') or {}).get('job_id','-')}", ""]
        ds = []
        for cr in env["corners"]:
            for d in cr.get("diagnostics", []):
                bad.append(f"{v} mc {cr['corner_id']}: [{d.get('code')}]")
            m = {x["name"]: x.get("value") for x in cr.get("measurements", [])}
            s = steps(m, v)
            if s is None:
                bad.append(f"{v} mc {cr['corner_id']}: missing edge"); continue
            ds.append((m, s))
        if not ds:
            continue
        # per-tap step vector for the rising-input edge; sigma over samples
        Ls += ["| tap k | mean step (ps) | sigma step (ps) | sigma / mean (%) | mean d_k (ps) | sigma d_k (ps) |", "|---|---|---|---|---|---|"]
        worst = 0
        for k in range(1, 9):
            st = [m[f"dr{k}"] - (m[f"dr{k-1}"] if k > 1 else 0.0) for m, _ in ds]
            dk = [m[f"dr{k}"] for m, _ in ds]
            mu, sg = sum(st) / len(st), sd(st)
            worst = max(worst, sg / mu)
            Ls.append(f"| {k} | {mu*1e12:.1f} | {sg*1e12:.2f} | {100*sg/mu:.2f} | {sum(dk)/len(dk)*1e12:.1f} | {sd(dk)*1e12:.2f} |")
        # DNL-like: per-sample spread of the 8 steps relative to their mean (rising-input)
        dnl = []
        for m, _ in ds:
            st = [m[f"dr{k}"] - (m[f"dr{k-1}"] if k > 1 else 0.0) for k in range(1, 9)]
            mean = sum(st) / 8
            dnl.append(max(abs(x - mean) for x in st))
        Ls += ["", f"Worst per-tap step sigma/mean: {100*worst:.2f} %. Per-sample max |step - line-mean step| (rising input): "
               f"mean {sum(dnl)/len(dnl)*1e12:.2f} ps, max {max(dnl)*1e12:.2f} ps (n={len(dnl)}). "
               + ("Note: for A the rising-input steps alternate fall/rise outputs, so this includes the systematic tpHL/tpLH step alternation." if v == "a" else ""), ""]
        if ctl is not None and "error" not in ctl:
            cm = [[x.get("value") for x in cr["measurements"] if x["name"].startswith(("dr", "df"))] for cr in ctl["corners"]]
            allsame = all(c == cm[0] for c in cm)
            rm = None if rep is None or "error" in rep else [[x.get("value") for x in cr["measurements"] if x["name"].startswith(("dr", "df"))] for cr in rep["corners"]]
            Ls += [f"Negative control (`mos_ss`, same seed/n): {len(cm)} runs, sigma exactly 0 across samples: **{allsame}**; "
                   f"repeat run identical: **{rm == cm}**.", ""]
            if not allsame or rm != cm:
                bad.append(f"{v}: negative control failed")
        else:
            bad.append(f"{v}: control missing")
    Ls += ["## Run status", "", ("ERRORS:" if bad else "no diagnostics / errors")] + [f"- {b}" for b in bad]
    open(os.path.join(out, "record.md"), "w").write("\n".join(Ls) + "\n")
    print("\n".join(Ls[-6:]))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main_mc(sys.argv[2]) if sys.argv[1] == "mc" else main_grid(sys.argv[1], sys.argv[2]))
