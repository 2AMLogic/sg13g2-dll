#!/usr/bin/env bash
# design/export.sh -- regenerate (or check) the committed SPICE netlists from
# the xschem sources, through `klt netlist` (never raw xschem).
#
#   design/export.sh            # rewrite design/netlist/*.spice
#   design/export.sh --check    # write nothing; exit 3 if any netlist is stale
#
# Each top is exported with `klt netlist --block` into a scratch directory, the
# absolute checkout path xschem stamps into `** sch_path:` / `** sym_path:`
# comment lines is rewritten to a repo-relative `design/...` path (so the
# committed file is the same in every clone), and the result is written to, or
# compared with, design/netlist/<top>.spice.
#
# Why not `klt netlist --check` directly: its comparison is byte-exact against
# the raw export, which embeds the absolute checkout path, so a committed
# netlist can only ever "match" in the one directory it was generated in
# (tool gap, 2AMLogic/klayout-tools#4091; see design/NOTES.md).
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TOPS=(delay_cell tap_buffer delay_line)
CHECK=0
case "${1:-}" in
  "") ;;
  --check) CHECK=1 ;;
  *) echo "usage: design/export.sh [--check]" >&2; exit 2 ;;
esac

WORK="$(mktemp -d)"
trap 'rm -rf "${WORK}"' EXIT
mkdir -p "${HERE}/netlist"

stale=0
for top in "${TOPS[@]}"; do
  raw="${WORK}/${top}.raw.spice"
  klt netlist "${HERE}/${top}.sch" --rcfile "${HERE}/xschemrc" --block \
      -o "${raw}" >"${WORK}/${top}.log" 2>&1 || {
    echo "export.sh: klt netlist failed for ${top}:" >&2
    cat "${WORK}/${top}.log" >&2
    exit 1
  }
  # No auto-named nets in a port list, no xschem-reported unconnected pins.
  if grep -E '^\.subckt ' "${raw}" | grep -qE '\bnet[0-9]+\b'; then
    echo "export.sh: auto-generated net name in a .subckt port list (${top})" >&2
    exit 1
  fi
  norm="${WORK}/${top}.spice"
  sed -E "s#^(\*\* (sch|sym)_path: ).*/design/#\1design/#" "${raw}" >"${norm}"
  dest="${HERE}/netlist/${top}.spice"
  if [[ ${CHECK} -eq 1 ]]; then
    if cmp -s "${norm}" "${dest}"; then
      echo "export.sh: ${top}: match"
    else
      echo "export.sh: ${top}: STALE (design/netlist/${top}.spice differs from the schematic export)" >&2
      stale=1
    fi
  else
    cp "${norm}" "${dest}"
    echo "export.sh: ${top}: written"
  fi
done

if [[ ${stale} -ne 0 ]]; then
  echo "export.sh: run design/export.sh and commit the result" >&2
  exit 3
fi
