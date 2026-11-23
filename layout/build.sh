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
CURRENT=layout/runs/.current
SCRATCH=""
cleanup() { rm -f "$CURRENT" ${SCRATCH:+"$SCRATCH"}; }
trap 'cleanup' EXIT
: > "$CURRENT"

# publish_report <cell> <name> <expected-status> <cmd...>
# Stage the klt envelope in a temp file beside its destination and replace the
# committed report only after the pipeline succeeded, the JSON parses and the
# status is the expected one. On any failure the previous copy is untouched.
publish_report() {
    local cell=$1 name=$2 want=$3; shift 3
    local dest="layout/$cell/${name}_report.json" status
    SCRATCH=$(mktemp "$dest.XXXXXX")
    "$@" 2>/dev/null | json_from_stdout > "$SCRATCH" \
        || { echo "FAIL: $name command failed" >&2; exit 1; }
    status=$(python3 -c "import json,sys;print(json.load(open(sys.argv[1]))['status'])" "$SCRATCH") \
        || { echo "FAIL: $name report is not valid JSON" >&2; exit 1; }
    echo "  $name: $status"
    [ "$status" = "$want" ] || { echo "FAIL: $name status $status (want $want)" >&2; exit 1; }
    mv -f "$SCRATCH" "$dest"
    SCRATCH=""
    REPORT_STATUS=$status
}

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

    $GEN layout/check_psd.py "layout/$cell/$cell.gds"

    publish_report "$cell" drc clean "$KLT" drc --deck sg13g2 --format json "layout/$cell/$cell.gds"
    drc_status=$REPORT_STATUS
    publish_report "$cell" lvs match "$KLT" lvs "layout/$cell/lvs_request.json" --format json
    lvs_status=$REPORT_STATUS

    echo "$cell gds=$built drc=$drc_status lvs=$lvs_status" >> "$CURRENT"
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
        cat "$CURRENT"
    } > "$dir/record.md"
    echo "run record: $dir/record.md"
fi

echo "OK"
