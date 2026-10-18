#!/usr/bin/env python3
"""Build `klt sim` grid requests from one base request.

A testbench is ONE base request (netlist, models, analysis, measurements).
This module turns it into a grid request by adding three independent axes,
all expressed as `klt sim` request fields so the host daemon routes the grid
to the batch fleet (no `ngspice -b` loops anywhere):

  corners  PVT matrix read from sim/corners.json (filled by the ratified spec,
           issue #2; this module chooses no values).
  ic       initial-condition (start-state) axis. `{"vic": [0.0, 0.6, 1.2]}`
           gives three start states. Each name is a voltage SOURCE in the
           deck whose value the harness sweeps through `corners.supply_v`
           (an `alter`, supported by every runner image); the deck uses it to
           pre-charge a node through a switch before the stimulus starts.
           The axis is crossed with the corner file's own `supply_v` rows.
           (`corners.params` is not used: the fleet runner image can lag
           the client and refuses it. klt has no `.ic`/`uic` axis; see
           sim/README.md "Start-state axis".)
  mc       Monte Carlo: `monte_carlo` {n, seed, vary[, seed_scope, ...]},
           orthogonal to the corner matrix (corner_count * n runs).

Stdlib only. Everything here is pure request construction; nothing simulates.
"""

from __future__ import annotations

import argparse
import copy
import json
import os
import sys

VARY = ("mismatch", "process", "both")
SEED_SCOPES = ("per_corner", "shared", "point")


class GridError(ValueError):
    pass


def load_json(path):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def load_corners(path, allow_empty=False):
    """Read and validate a corners file. An unfilled set is an error."""
    data = load_json(path)
    if data.get("schema") != 1:
        raise GridError(f"{path}: schema must be 1")
    process = data.get("process", [])
    temps = data.get("temperature_c", [])
    supply = data.get("supply_v") or {}
    if not isinstance(process, list) or not isinstance(temps, list):
        raise GridError(f"{path}: process and temperature_c must be arrays")
    if not isinstance(supply, dict):
        raise GridError(f"{path}: supply_v must be an object")
    if (not process or not temps) and not allow_empty:
        raise GridError(
            f"{path}: corner set is empty (process={len(process)}, "
            f"temperature_c={len(temps)}). It is filled by the ratified spec "
            "(issue #2); refusing to run a PVT claim on an unfilled set."
        )
    lens = {len(v) for v in supply.values()}
    if len(lens) > 1:
        raise GridError(f"{path}: supply_v arrays must have equal length")
    out = {}
    if process:
        out["process"] = process
    if temps:
        out["temperature_c"] = temps
    if supply:
        out["supply_v"] = supply
    return out


def ic_axis(ic):
    """Validate a start-state axis: {source: [value, ...]} equal length."""
    if not isinstance(ic, dict) or not ic:
        raise GridError("ic must be a nonempty {source: [values]} object")
    for name, vals in ic.items():
        if not isinstance(vals, list) or not vals:
            raise GridError(f"ic[{name!r}] must be a nonempty array")
        for x in vals:
            if isinstance(x, bool) or not isinstance(x, (int, float)):
                raise GridError(f"ic[{name!r}] values must be numbers")
    if len({len(v) for v in ic.values()}) != 1:
        raise GridError("ic arrays must have equal length (one row per start state)")
    return {k: list(v) for k, v in ic.items()}


def cross_supply(supply, ic):
    """Cross corner supply rows with start-state rows into zipped arrays.

    klt zips every `supply_v` array by index, so a start-state axis cannot sit
    beside a PVT supply axis of another length. Expand rows i x j into
    length L*R arrays (corner row outer, start state inner).
    """
    supply = supply or {}
    clash = set(supply) & set(ic)
    if clash:
        raise GridError(f"ic source(s) {sorted(clash)} also appear in corners supply_v")
    left = len(next(iter(supply.values()))) if supply else 1
    right = len(next(iter(ic.values())))
    out = {k: [v[i] for i in range(left) for _ in range(right)] for k, v in supply.items()}
    for k, v in ic.items():
        out[k] = [v[j] for _ in range(left) for j in range(right)]
    return out


def monte_carlo_block(n, seed, vary, seed_scope=None, k_sigma=None):
    if isinstance(n, bool) or not isinstance(n, int) or n < 1:
        raise GridError("monte_carlo n must be a positive integer")
    if isinstance(seed, bool) or not isinstance(seed, int):
        raise GridError("monte_carlo seed must be an integer (it is recorded)")
    if vary not in VARY:
        raise GridError(f"monte_carlo vary must be one of {VARY}")
    block = {"n": n, "seed": seed, "vary": vary}
    if seed_scope is not None:
        if seed_scope not in SEED_SCOPES:
            raise GridError(f"seed_scope must be one of {SEED_SCOPES}")
        block["seed_scope"] = seed_scope
    if k_sigma is not None:
        block["k_sigma"] = k_sigma
    return block


def build_request(base, corners=None, ic=None, mc=None, lib_section=None):
    """Return a new request dict: `base` plus the requested axes.

    The base owns netlist/models/analysis/measurements; it must not declare
    `corners` or `monte_carlo` (the harness owns those axes). `lib_section`
    optionally replaces the process corners with a fixed section list.
    """
    for key in ("corners", "monte_carlo"):
        if key in base:
            raise GridError(f"base request declares {key!r}; the harness owns that axis")
    req = copy.deepcopy(base)
    grid = {}
    if corners:
        grid.update(copy.deepcopy(corners))
    if lib_section is not None:
        grid["process"] = [lib_section] if isinstance(lib_section, str) else lib_section
    if ic is not None:
        grid["supply_v"] = cross_supply(grid.get("supply_v"), ic_axis(ic))
    if grid:
        req["corners"] = grid
    if mc is not None:
        req["monte_carlo"] = monte_carlo_block(**mc)
    return req


def negative_control(mc_request, quiet_process):
    """The deterministic MC negative control for a request.

    Same request, same seed, same n, same temperatures, but every process
    corner replaced by `quiet_process`: model sections that draw no mismatch
    (SG13G2: `mos_tt` in place of `mos_tt_mismatch`). Every measurement's
    sigma must then come back exactly 0, and re-running with the same seed
    must reproduce the result on one engine build. SG13G2 draws mismatch from
    ngspice's own RNG (`agauss`), which `monte_carlo.vary` alone does not pin
    (klt sim docs, "Deterministic negative control"), so the quiet section is
    the working control. It guards against a sampler that silently varies
    from an unrelated source.
    """
    if "monte_carlo" not in mc_request:
        raise GridError("negative control needs a request with monte_carlo")
    if not quiet_process or not isinstance(quiet_process, list):
        raise GridError("quiet_process must be a nonempty list of model sections")
    ctl = copy.deepcopy(mc_request)
    ctl.setdefault("corners", {})["process"] = list(quiet_process)
    return ctl


def rebase_netlist(req, src_dir, out_path):
    """Make `netlist` (relative to src_dir) relative to the written file."""
    net = req.get("netlist")
    if isinstance(net, str) and not os.path.isabs(net):
        absolute = os.path.normpath(os.path.join(src_dir, net))
        req["netlist"] = os.path.relpath(absolute, os.path.dirname(os.path.abspath(out_path)))
    return req


def write_request(req, path):
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(req, fh, indent=2, sort_keys=False)
        fh.write("\n")


def _parse_ic(items):
    ic = {}
    for item in items or []:
        name, _, vals = item.partition("=")
        if not name or not vals:
            raise GridError(f"--ic expects NAME=v1,v2,...; got {item!r}")
        try:
            ic[name] = [float(v) for v in vals.split(",")]
        except ValueError as exc:
            raise GridError(f"--ic {item!r}: {exc}") from exc
    return ic or None


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("base", help="base request JSON (no corners / monte_carlo)")
    ap.add_argument("-o", "--out", required=True, help="grid request path to write")
    ap.add_argument("--corners", help="corners file (default: sim/corners.json)")
    ap.add_argument("--no-corners", action="store_true", help="single process/temperature point from the base's models")
    ap.add_argument("--ic", action="append", metavar="SOURCE=v1,v2", help="start-state axis: voltage source swept via supply_v (repeatable; equal lengths)")
    ap.add_argument("--mc-n", type=int)
    ap.add_argument("--mc-seed", type=int)
    ap.add_argument("--mc-vary", choices=VARY)
    ap.add_argument("--mc-seed-scope", choices=SEED_SCOPES)
    ap.add_argument("--control-process", action="append", metavar="SECTION", help="also write <out minus .json>.control.json: same MC request on these non-mismatch model sections (repeatable)")
    args = ap.parse_args(argv)
    here = os.path.dirname(os.path.abspath(__file__))
    try:
        base = load_json(args.base)
        corners = None
        if not args.no_corners:
            corners = load_corners(args.corners or os.path.join(here, "..", "corners.json"))
        mc = None
        if args.mc_n is not None or args.mc_seed is not None or args.mc_vary:
            mc = monte_carlo_block(args.mc_n, args.mc_seed, args.mc_vary, args.mc_seed_scope)
        req = build_request(base, corners, _parse_ic(args.ic), mc)
        src_dir = os.path.dirname(os.path.abspath(args.base))
        write_request(rebase_netlist(req, src_dir, args.out), args.out)
        if args.control_process:
            ctl = negative_control(req, args.control_process)
            write_request(ctl, args.out[:-5] + ".control.json" if args.out.endswith(".json") else args.out + ".control.json")
    except (GridError, OSError, TypeError, json.JSONDecodeError) as exc:
        print(f"gridspec: FAIL -- {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
