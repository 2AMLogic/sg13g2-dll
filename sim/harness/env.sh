# Source me:  source sim/harness/env.sh
#
# Resolves the SG13G2 PDK install for sim/harness/common/build-osdi.sh and
# sim/pdk-smoke/run.sh. PDK_ROOT/PDK from the environment win; otherwise the
# usual open_pdks prefixes are searched. Safe to source from any directory.
# Local file (not vendored): sim/harness/common/build-osdi.sh expects an
# env.sh one directory above itself.
# shellcheck shell=bash

export PDK="${PDK:-ihp-sg13g2}"

if [[ -z "${PDK_ROOT:-}" ]]; then
  for _sg13g2_candidate in /usr/share/pdk /usr/local/share/pdk \
                           "${HOME}/share/pdk" "${HOME}/.ciel" "${HOME}/.volare"; do
    if [[ -d "${_sg13g2_candidate}/${PDK}/libs.tech/ngspice" ]]; then
      export PDK_ROOT="${_sg13g2_candidate}"
      break
    fi
  done
fi

if [[ -n "${PDK_ROOT:-}" && -d "${PDK_ROOT}/${PDK}/libs.tech/ngspice" ]]; then
  export SG13G2_NGSPICE_MODELS="${PDK_ROOT}/${PDK}/libs.tech/ngspice/models"
  export SG13G2_OSDI_DIR="${PDK_ROOT}/${PDK}/libs.tech/ngspice/osdi"
  echo "sg13g2: PDK_ROOT=${PDK_ROOT} PDK=${PDK}" >&2
else
  echo "sg13g2: no ${PDK} install found under PDK_ROOT or the usual prefixes." >&2
  echo "sg13g2: set PDK_ROOT to an open_pdks-shaped IHP-Open-PDK checkout (see sim/pdk.json)," >&2
  echo "sg13g2: e.g. via klayout-tools' scripts/fetch-ihp-sg13g2.sh, then re-source." >&2
fi

unset _sg13g2_candidate
