#!/usr/bin/env bash
# layout/build.sh -- rebuild all three cell layouts, verify the committed
# GDS streams reproduce byte-for-byte, refresh the committed klt drc / klt
# lvs envelopes, and append a run record under layout/runs/ (issue #190).
#
# Usage (from anywhere; the script locates the repo root itself):
#   layout/build.sh            rebuild + verify + refresh envelopes
#   layout/build.sh --record   also append the run record
#   LAYOUT_REGEN=1 layout/build.sh   accept a deliberate stream change
#
# Environment: PDK / PDK_ROOT default to ihp-sg13g2 / ~/share/pdk (the same
# resolution sim/pdk.json pins). klt comes from scripts/klt.sh (pinned
# klayout-tools==0.8.0); the wiring pass pins klayout==0.30.13, the engine
# version the pinned klt resolves in this fleet environment.
set -euo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(dirname "$HERE")"
cd "$ROOT"

export PDK="${PDK:-ihp-sg13g2}"
export PDK_ROOT="${PDK_ROOT:-$HOME/share/pdk}"
KLT=scripts/klt.sh
GEN="uv run --with klayout==0.30.13 python3"
CELLS="loop_filter cp_bias cp"

record=0
[ "${1:-}" = "--record" ] && record=1

json_from_stdout() {  # strip any uvx install notices before the first '{'
    python3 -c 'import sys; s=sys.stdin.read(); sys.stdout.write(s[s.index("{"):])'
}

mkdir -p layout/runs
: > layout/runs/.current

for cell in $CELLS; do
    echo "== $cell"
    $GEN "layout/$cell/generate.py" >/dev/null

    # A clean-clone rebuild must reproduce each committed stream. Compare
    # against HEAD when the stream is committed; record the fresh hash either
    # way so a first run doubles as the provenance record.
    built=$(sha256sum "layout/$cell/$cell.gds" | cut -d' ' -f1)
    if git ls-files --error-unmatch "layout/$cell/$cell.gds" >/dev/null 2>&1; then
        committed=$(git show "HEAD:layout/$cell/$cell.gds" | sha256sum | cut -d' ' -f1)
        if [ "$built" != "$committed" ] && [ "${LAYOUT_REGEN:-0}" = 1 ]; then
            echo "  gds changed vs HEAD (LAYOUT_REGEN=1; commit the new stream): $built"
        elif [ "$built" != "$committed" ]; then
            echo "FAIL: layout/$cell/$cell.gds drifted from HEAD" >&2
            echo "  committed $committed" >&2
            echo "  rebuilt   $built" >&2
            exit 1
        else
            echo "  gds reproduces HEAD (sha256 $built)"
        fi
        :
    else
        echo "  gds not yet committed (sha256 $built)"
    fi

    $GEN layout/check_psd.py "layout/$cell/$cell.gds" || { echo "FAIL: pfet S/D without pSD" >&2; exit 1; }

    "$KLT" drc --deck sg13g2 --format json "layout/$cell/$cell.gds" 2>/dev/null \
        | json_from_stdout > "layout/$cell/drc_report.json"
    drc_status=$(python3 -c "import json;print(json.load(open('layout/$cell/drc_report.json'))['status'])")
    echo "  drc sg13g2: $drc_status"
    [ "$drc_status" = "clean" ] || { echo "FAIL: drc not clean" >&2; exit 1; }

    "$KLT" lvs "layout/$cell/lvs_request.json" --format json 2>/dev/null \
        | json_from_stdout > "layout/$cell/lvs_report.json"
    lvs_status=$(python3 -c "import json;print(json.load(open('layout/$cell/lvs_report.json'))['status'])")
    echo "  lvs: $lvs_status"
    [ "$lvs_status" = "match" ] || { echo "FAIL: lvs not match" >&2; exit 1; }

    echo "$cell gds=$built drc=$drc_status lvs=$lvs_status" >> layout/runs/.current
done

if [ "$record" = 1 ]; then
    stamp=$(date -u +%Y%m%dT%H%M%SZ)
    dir="layout/runs/$stamp"
    mkdir -p "$dir"
    klt_ver=$("$KLT" version 2>/dev/null | head -1)
    {
        echo "# layout run record $stamp"
        echo
        echo "- repo HEAD: $(git rev-parse HEAD)"
        echo "- klt: $klt_ver (scripts/klt.sh pin)"
        echo "- klayout (wiring): 0.30.13 (\`uv run --with klayout==0.30.13\`)"
        echo "- PDK: $PDK (fetched:0.3.0, sim/pdk.json; root resolved by klt pdk find)"
        echo
        echo "Per-cell evidence: the committed drc_report.json / lvs_report.json"
        echo "next to each GDS are this run's envelopes; the sha256 below binds"
        echo "them to the stream that produced them."
        echo
        cat layout/runs/.current
    } > "$dir/record.md"
    echo "run record: $dir/record.md"
fi

rm -f layout/runs/.current
echo "OK"
