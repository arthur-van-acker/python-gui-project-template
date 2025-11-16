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

run_step() {
  local label="$1"
  shift
  printf '\n>>> %s\n' "$label" >&2
  "$@"
}

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
smoke_script="0,4,8"
PYTHON_BIN="$(detect_python)"
SKIP_REQUIREMENTS_INSTALL="${SKIP_REQUIREMENTS_INSTALL:-0}"

sandbox_dir=""

echo "Running local CI checks with ${PYTHON_BIN}" >&2

pushd "${repo_root}" >/dev/null
trap 'if [[ -n "${sandbox_dir}" && -d "${sandbox_dir}" ]]; then rm -rf "${sandbox_dir}"; fi; popd >/dev/null' EXIT

if [[ "${SKIP_REQUIREMENTS_INSTALL}" != "1" ]]; then
  run_step "Sync requirements" "${PYTHON_BIN}" -m pip install -r requirements.txt
fi

run_step "Formatting (black --check)" "${PYTHON_BIN}" -m black --check src tests
run_step "Linting (ruff check)" "${PYTHON_BIN}" -m ruff check src tests
run_step "Type checking (mypy)" "${PYTHON_BIN}" -m mypy src
run_step "Pytest (non-GUI markers)" "${PYTHON_BIN}" -m pytest tests -m "not gui" --maxfail=1 --disable-warnings -q
run_step "Pytest (GUI markers)" "${PYTHON_BIN}" -m pytest tests/test_gui.py -m gui -q

run_step "Build wheel bundle" "${PYTHON_BIN}" -m build --wheel

wheel_path="$(ls -1t dist/*.whl 2>/dev/null | head -n 1 || true)"
if [[ -z "${wheel_path}" ]]; then
  echo "No wheel artifact found in dist/." >&2
  exit 1
fi

sandbox_dir="$(mktemp -d 2>/dev/null || mktemp -d -t yourapp-sandbox)"
run_step "Create sandbox virtual environment" "${PYTHON_BIN}" -m venv "${sandbox_dir}"

sandbox_python="${sandbox_dir}/bin/python"

run_step "Install wheel into sandbox" "${sandbox_python}" -m pip install "${wheel_path}"
run_step "Installer smoke test (service UI)" "${sandbox_python}" -m tictactoe --ui service --script "${smoke_script}" --quiet --label ci-smoke

run_step "Cleanup sandbox" rm -rf "${sandbox_dir}"
sandbox_dir=""

echo "\nAll local CI checks completed successfully." >&2
