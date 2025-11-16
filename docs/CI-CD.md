# CI/CD Overview

This template ships with repeatable local tooling plus hooks you can adapt to any continuous integration platform.

## Local Automation Stack

| Tool | Location | Purpose |
| --- | --- | --- |
| **pre-commit** | `.pre-commit-config.yaml` | Runs formatting, linting, typing, and pytest (non-GUI marker) on each commit/push. Mirrors the checks enforced in CI.
| **tox** | `tox.ini` | Defines shared environments: `lint` (Ruff, Black), `type` (Mypy), and `py313` (pytest suite). Use it when you want hermetic virtualenvs; the default CI runs the underlying tools directly.
| **run-ci.ps1 / run-ci.sh** | `scripts/` | Convenience wrappers that install requirements, run Black/Ruff/Mypy, execute both pytest marker sets, and perform installer smoke tests (Windows) or sandboxed wheel runs (POSIX).
| **pytest markers** | `pytest.ini` | Split GUI vs. non-GUI tests so headless environments can skip UI smoke tests by default.

## Recommended Developer Workflow
1. Install pre-commit hooks: `pre-commit install`.
2. Use `scripts/run-ci.ps1` (PowerShell) or `./scripts/run-ci.sh` (Bash) before pushing.
3. For GUI regressions, run `python -m pytest -m gui` which exercises the CustomTkinter headless shim.

## Sample GitHub Actions Workflow
If you prefer a tox-driven pipeline, start from the following example (adjust Python versions as needed):

```yaml
name: CI

on:
  push:
    branches: [ main ]
  pull_request:

jobs:
  tests:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.11", "3.12", "3.13"]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
      - name: Install tooling
        run: |
          python -m pip install --upgrade pip
          python -m pip install -r requirements.txt
      - name: Run tox matrix
        run: python -m tox -e lint,type,py313
      - name: Upload coverage (optional)
        if: matrix.python-version == '3.13'
        run: python -m pytest --cov=tictactoe --cov-report=xml
```

> The repository’s checked-in `.github/workflows/ci.yml` currently mirrors the `run-ci` scripts by running the linters/type checker/pytest directly instead of invoking tox. Use whichever style matches your team’s conventions.

## Extending to Release Pipelines
- Add a `release` job that depends on `tests`, runs `wheel-builder.bat` (or PowerShell equivalent on Windows runners), and uploads `dist/` as an artifact.
- Gate GitHub Releases on successful CI by requiring the workflow status check.
- For corporate deployments, integrate with Azure Pipelines or Jenkins by invoking `scripts/run-ci.ps1`/`run-ci.sh` and `wheel-builder.bat` from the respective job steps.

## Secrets & Environment Variables
- GUI tests rely on the headless adapter and should succeed without display servers. If you introduce real GUI smoke tests, configure CI to use xvfb (`xvfb-run`).
- Store code-signing certificates, PyPI tokens, or GitHub release tokens in the platform’s secret store and reference them in release jobs.

By standardizing on pre-commit + tox + the run-ci wrappers, every developer and CI environment executes the same checks, reducing “works on my machine” drift and making it trivial to port the template into other organizations.
