#!/usr/bin/env bash
# run.sh -- noise-method known-case bench (issue #115, spec/decisions/0014).
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SIM_DIR="$(cd "${HERE}/.." && pwd)"
REPO_ROOT="$(cd "${SIM_DIR}/.." && pwd)"
IA_PROBE="1e-9"

# shellcheck source=/dev/null
source "${SIM_DIR}/harness/preflight.sh"
sim_preflight

STAMP="$(date -u +%Y%m%dT%H%M%SZ)"
OUT="${NOISE_METHOD_RESULTS_DIR:-${HERE}/results/${STAMP}}"
sim_stage_inputs "${HERE}" "${OUT}" requests

submit() {
  local tag="$1" req="$2" rc=0
  sim_submit "${OUT}" "${tag}" "${req}" --backend local || rc=$?
  if [[ ${rc} -ne 0 ]]; then
    echo "run.sh: submit ${tag} exited ${rc}" >&2
  fi
  return "${rc}"
}

for tag in vth noise sr control; do
  submit "${tag}" "${OUT}/requests/${tag}.request.json"
done

rc_abort=0
submit abort "${OUT}/requests/abort.request.json" || rc_abort=$?
if [[ ${rc_abort} -ne 0 && ${rc_abort} -ne 4 ]]; then
  echo "run.sh: abort probe failed unexpectedly (exit ${rc_abort}, expected 4)" >&2
  exit "${rc_abort}"
fi

python3 -I "${HERE}/summarize.py" derive "${OUT}"

restage_deck() { # fresh copy of the pristine deck, then size @IA@ -- never a bare
  # literal substitution, which silently breaks if the deck gains another 1e-9.
  local deck="$1" amp="$2"
  cp "${HERE}/decks/${deck}" "${OUT}/decks/${deck}"
  sed -i "s/@IA@/${amp}/g" "${OUT}/decks/${deck}"
}

restage_deck nm_sigma.spice "${IA_PROBE}"
submit sigma-probe "${OUT}/requests/sigma.request.json"
IA_1="$(python3 -I "${HERE}/summarize.py" calibrate "${OUT}" sigma-probe "${IA_PROBE}")"
restage_deck nm_sigma.spice "${IA_1}"

submit sigma-refine1 "${OUT}/requests/sigma.request.json"
submit sigma-refine2 "${OUT}/requests/sigma.request.json"
IA="$(python3 -I "${HERE}/summarize.py" calibrate2 "${OUT}" "${IA_1}")"
restage_deck nm_sigma.spice "${IA}"

echo "run.sh: calibrated IA = ${IA} A" >&2
restage_deck nm_edge.spice "${IA}"

for i in 1 2 3 4 5 6 7 8; do
  submit "sigma-s${i}" "${OUT}/requests/sigma.request.json"
done
for i in 1 2 3 4 5 6 7 8; do
  submit "edge-s${i}" "${OUT}/requests/edge.request.json"
done

python3 -I "${HERE}/summarize.py" summarize "${OUT}"
echo "run.sh: PASS -- ${OUT}/record.md" >&2
