# Testing Guide

This document explains everything you need to know to design, write, run, and extend tests for the Tic Tac Toe template. Treat it as a living testing handbook you can adapt when you fork the project for other applications.

---

## 1. Testing Philosophy

- **Template-first mindset:** Tests must be easy to reuse when the tic-tac-toe logic is replaced with a different domain. Keep assertions focused on public contracts, not implementation details.
- **Fast feedback loops:** Default test targets run in seconds and never require a GUI display. GUI coverage relies on the CustomTkinter headless shim so pipelines stay green.
- **Single-source-of-truth:** `pytest` is the orchestrator. `tox` composes repeatable environments (unit tests, lint, typing) but calls into the same pytest entry points.
- **High signal over blanket coverage:** Aim for meaningful assertions (state transitions, UI wiring, CLI wiring) rather than hitting every branch mechanically. Coverage is still enforced (>=50%) to catch drift.

---

## 2. Test Taxonomy

| Layer          | Location                | Purpose                                                                 |
|----------------|-------------------------|-------------------------------------------------------------------------|
| Domain unit    | `tests/test_logic.py`   | Deterministic checks for `tictactoe.domain.logic.TicTacToe` contracts.  |
| CLI smoke      | `tests/test_cli.py`     | Ensures the entry point loads the intended frontend.                    |
| Config sanity  | `tests/test_config.py`  | Guards template metadata (e.g., exported symbols).                      |
| GUI smoke      | `tests/test_gui.py`     | Validates widget creation, event wiring, and state rendering.           |
| Future layers  | Add sibling files under `tests/` (e.g., API, services). | Ensure each new layer adds its own focused suite.                       |

---

## 3. Toolchain Overview

- **pytest** (core runner) with built-in assertion rewriting.
- **coverage.py** through `pytest --cov` (configured in `pytest.ini`).
- **tox** for matrixed execution (`tox -e py313`, `tox -e lint`).
- **ruff**, **black**, **mypy** invoked via tox environments or directly for quality gates.
- **Custom headless widgets** (`tictactoe.ui.gui.headless`) emulate CustomTkinter so GUI tests run anywhere.
- **pytest.ini guard rails:** `--strict-config`, `--strict-markers`, `--cov=tictactoe`, and `--cov-fail-under=50` are applied automatically so every local run matches CI expectations.

---

## 4. Environment Setup

1. Create/activate the project venv (already part of the template workflow).
2. Install the editable package plus dev requirements (the pinned `requirements.txt`
already ends with `-e .`, so one command keeps everything in sync):

```pwsh
pip install -r requirements.txt
# or, if you prefer extras syntax
pip install -e .[dev]
```

3. (Optional) Pin GUI tests to headless mode to avoid real Tk dependencies or
    force a specific frontend during smoke tests:

```pwsh
$env:TICTACTOE_HEADLESS = "1"   # PowerShell
# export TICTACTOE_HEADLESS=1   # bash/zsh
$env:TICTACTOE_UI = "cli"       # Force the terminal client for scripted checks
```

4. Verify tooling versions:

```pwsh
python -m pytest --version
python -m tox --version
```

---

## 5. Running Tests

### 5.1 Run Everything (default developer loop)

```pwsh
python -m pytest
```

Outputs include coverage stats thanks to `pytest.ini`.

### 5.2 Filter by Marker

```pwsh
python -m pytest -m "not gui"   # skip GUI tests
python -m pytest -m gui         # GUI-only smoke tests
```

### 5.3 Using tox

```pwsh
python -m tox -e py313          # run unit tests on Python 3.13
python -m tox -e lint           # ruff + black check
python -m tox -e type           # mypy
python -m tox                   # run everything configured
```

### 5.4 Targeting a Single Test

```pwsh
python -m pytest tests/test_logic.py -k draw_game
```

### 5.5 Exercising the CLI Script Mode

The top-level dispatcher (`python -m tictactoe`) only accepts the `--ui` and
`--list-frontends` switches, so CLI-specific flags live on the CLI module. When
you need to reproduce `tests/test_cli.py` scenarios manually, call the module
directly:

```pwsh
# Run the CLI without rendering the ASCII board
python -m tictactoe.ui.cli.main --script 0,3,4,6,8 --quiet
```

This mirrors exactly what the tests assert: scripted move sequences raise
`SystemExit` on invalid positions and produce the same snapshots as the GUI.

---

## 6. Writing Tests

### 6.1 General Patterns

- **Arrange / Act / Assert:** Keep each phase explicit to clarify intent.
- **No global state bleed:** Instantiate fresh objects per test. If setup cost grows, use `pytest.fixture` to centralize creation.
- **Prefer public APIs:** Tests interact with `TicTacToe.make_move` or `TicTacToe.snapshot`, not internal lists.
- **Document intent:** When an assertion may look arbitrary (e.g., move sequences), add inline comments.

### 6.2 Domain Tests (`tests/test_logic.py`)

Key practices:

- Use readable move sequences and assert every critical state (`state`, `current_player`, `board` immutability).
- Cover edge cases: invalid positions, double moves, post-win moves, reset.
- When adding new domain capabilities, append dedicated tests rather than editing existing ones (preserves template clarity).

Example snippet:

```python
def test_no_moves_after_win():
    game = TicTacToe()
    for move in (0, 3, 1, 4, 2):
        assert game.make_move(move)
    assert not game.make_move(5)
    assert game.board[5] is None
```

### 6.3 GUI Tests (`tests/test_gui.py`)

- Always force headless mode (`os.environ.setdefault("TICTACTOE_HEADLESS", "1")`).
- Wrap app creation in try/except for `TclError`; skip when Tk is unavailable.
- Avoid long-running UI loops; drive widgets by invoking callbacks directly (`button.invoke()` or calling handler methods).
- Assert against widget configuration via `.cget(...)` rather than reading internal attributes.
- Destroy the root window in `finally` blocks to avoid resource leaks.

### 6.4 CLI / Entry-Point Tests (`tests/test_cli.py`)

- Use `importlib.reload` to re-run module-level code and capture side effects.
- Patch the GUI launcher with `monkeypatch` to keep the test isolated and fast.

### 6.5 Config / Metadata Tests (`tests/test_config.py`)

- Keep simple guardrails for template ergonomics, e.g., verifying `__all__` or ensuring version metadata exists.

### 6.6 Adding New Test Types

When extending the template (e.g., API backend), create a new file: `tests/test_api.py`. Common tips:

1. **Fixture placement:** Put shared fixtures in `tests/conftest.py` so pytest auto-discovers them.
2. **Data builders:** Create helper functions (e.g., `make_snapshot(...)`) near the tests or in `tests/helpers.py`.
3. **Markers:** Tag long-running suites (e.g., `@pytest.mark.integration`) to stay opt-in.

---

## 7. Working With Game Snapshots

The domain layer exposes immutable snapshots via `TicTacToe.snapshot` and listener callbacks. Tests should leverage these to avoid poking at internal lists.

```python
def test_snapshot_reflects_move_sequence():
    game = TicTacToe()
    game.make_move(0)
    snap = game.snapshot
    assert snap.board[0] == Player.X
    assert snap.state == GameState.PLAYING
```

Benefits:
- Stable contract when the underlying storage changes.
- Easier serialization/logging for debugging.
- Aligns with presentation-layer expectations.

---

## 8. Headless GUI Strategy

- `tictactoe.ui.gui.headless` mirrors the CustomTkinter API. Tests instantiate real widgets, but method bodies are no-ops.
- The module sets `__HEADLESS__ = True`; you can assert against it for sanity if needed.
- If you add new widget types or methods in the production GUI, update the headless shim simultaneously to keep tests compiling.
- Selecting the `headless` frontend via `python -m tictactoe --ui headless` (or by
    setting `TICTACTOE_UI=headless`) automatically forces
    `TICTACTOE_HEADLESS=1`, so GUI smoke tests run without talking to a real Tk
    runtime.

---

## 9. Coverage Expectations

- `pytest.ini` enforces a minimum 50% project coverage. Failing to meet the threshold breaks the test suite.
- To inspect coverage details:

```pwsh
python -m pytest --cov-report=term-missing
```

- Add targeted tests instead of blanket mocks to raise coverage meaningfully.

---

## 10. Continuous Integration Recommendations

Even though this repo does not ship a CI workflow by default, the testing strategy assumes CI will:

1. Install dependencies (same commands as Section 4).
2. Run `python -m pytest -m "not gui"` for fast feedback (this mirrors the
    command baked into `tox -e py313`).
3. Optionally run GUI tests in headless mode (set `TICTACTOE_HEADLESS=1` or invoke
    `python -m tictactoe --ui headless` before launching the suite).
4. Execute `python -m tox -e lint,type` to enforce formatting and typing standards.
5. Archive coverage XML/HTML if needed for dashboards.

When adding a workflow (`.github/workflows/tests.yml`), remember to install `python -m pip install tox` and set `TICTACTOE_HEADLESS=1`.

---

## 11. Debugging Failures

- **Re-run with `-vv`:** `python -m pytest -vv tests/test_gui.py::test_gui_win_updates_status_message`.
- **Drop into pdb:** `python -m pytest --maxfail=1 --pdb` to inspect state mid-test.
- **Log snapshots:** Temporarily insert `print(game.snapshot)` when diagnosing logic issues (pytest captures stdout nicely).
- **Recreate GUI issues manually:** Launch `python -m tictactoe` with `TICTACTOE_HEADLESS=0` to observe the real interface.

---

## 12. Linting, Formatting, Typing

Keep the suite healthy by running quality gates frequently:

```pwsh
python -m ruff check src tests
python -m black src tests
python -m mypy src
```

Tox environments (`lint`, `type`) already wrap these, but direct invocation is faster during active development.

---

## 13. Local CI Shortcuts & Hooks

### 13.1 Run the entire pipeline locally

Use the helper scripts to rehearse the CI steps (editable install + lint + type + tests) with one command:

```pwsh
pwsh scripts/run-ci.ps1
```

```bash
bash scripts/run-ci.sh
```

Set `SKIP_REQUIREMENTS_INSTALL=1` (or pass `-SkipRequirementsInstall`) when you only want to re-run the tox stages.

### 13.2 Pre-commit / pre-push automation

Install the hooks once so Black, Ruff, mypy, and the fast pytest suite run automatically before code leaves your machine:

```pwsh
python -m pip install pre-commit
pre-commit install
pre-commit install --hook-type pre-push
```

- **Commit-time hooks:** enforce formatting, lint rules, TOML/YAML hygiene, and run `python -m pytest -m "not gui"` before the commit is recorded.
- **Pre-push hooks:** replay `python -m pytest -m "not gui"` plus `python -m tox -e lint,type` (matching the GitHub Actions workflow).

Temporarily bypass hooks with `SKIP=hook-id pre-commit run hook-id` as documented at [pre-commit.com](https://pre-commit.com/), but always rerun the skipped command manually before opening a PR.

---

## 14. Extending the Template

When replacing Tic Tac Toe with your own application:

1. **Rename domain modules** but keep the public contracts (e.g., snapshot interfaces) so GUI/CLI tests remain intact.
2. **Duplicate and adapt existing tests** as regression guards for the new domain.
3. **Add integration tests early** for new dependencies (APIs, databases).
4. **Document custom fixtures** inside this file so future contributors understand how to drive your new components.

---

## 15. Future Enhancements (Testing Roadmap)

- [ ] Introduce snapshot-based golden tests for complex layouts.
- [ ] Add property-based tests (Hypothesis) for board validation.
- [ ] Provide a pytest plugin for reusable GUI fixtures.
- [ ] Wire up GitHub Actions workflow with caching and parallel jobs.
- [ ] Integrate `pytest-xdist` for sharding once the suite grows.

---

## 16. Quick Reference Commands

| Task                        | Command (PowerShell)                                      |
|-----------------------------|-----------------------------------------------------------|
| Run full suite              | `python -m pytest`                                        |
| Skip GUI tests              | `python -m pytest -m "not gui"`                          |
| GUI-only smoke              | `python -m pytest -m gui`                                 |
| Coverage details            | `python -m pytest --cov-report=term-missing`              |
| Single test                 | `python -m pytest tests/test_logic.py -k reset`           |
| Tox all envs               | `python -m tox`                                           |
| Lint + format via tox       | `python -m tox -e lint`                                   |
| Type check via tox          | `python -m tox -e type`                                   |
| List registered frontends   | `python -m tictactoe --list-frontends`                    |
| Scripted CLI smoke          | `python -m tictactoe.ui.cli.main --script 0,3,4,6,8 --quiet` |

Keep this table handy when onboarding new contributors.

---

Happy testing! Update this guide whenever the project gains new layers, tooling, or workflows so the template continues to serve as a complete reference.
