#!/usr/bin/env bash
set -euo pipefail

detect_python() {
  if [[ -n "${PYTHON:-}" ]]; then
    printf '%s' "${PYTHON}"
    return
  fi

  if [[ -n "${VIRTUAL_ENV:-}" ]]; then
    if [[ -x "${VIRTUAL_ENV}/bin/python" ]]; then
      printf '%s' "${VIRTUAL_ENV}/bin/python"
      return
    fi
    if [[ -x "${VIRTUAL_ENV}/Scripts/python.exe" ]]; then
      printf '%s' "${VIRTUAL_ENV}/Scripts/python.exe"
      return
    fi
  fi

  printf '%s' "python"
}

PYTHON_BIN="$(detect_python)"
SKIP_REQUIREMENTS_INSTALL="${SKIP_REQUIREMENTS_INSTALL:-0}"

echo "Running local CI checks with ${PYTHON_BIN}" >&2

if [[ "${SKIP_REQUIREMENTS_INSTALL}" != "1" ]]; then
  echo "Syncing requirements.txt (installs -e . automatically)" >&2
  "${PYTHON_BIN}" -m pip install -r requirements.txt
fi

echo "Executing tox lint/type/test matrix" >&2
"${PYTHON_BIN}" -m tox -e lint,type,py313

echo "All local CI checks completed successfully." >&2
