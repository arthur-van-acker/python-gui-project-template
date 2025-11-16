# Template Usage Guide & Design Rationale

This document walks you through adopting the YourApp Starter template for your own CustomTkinter projects and details the engineering decisions baked into the current setup. Follow the steps in order; each stage explains *what* to do and *why* the template encourages that workflow.

---

## 1. Understand the Building Blocks

| Component | Location | Purpose | Why it matters |
| --- | --- | --- | --- |
| Package source | `src/tictactoe` | Shipping code, assets, entry points | `src/` layout avoids accidental imports from the repo root and mirrors Python packaging best practices. |
| Tests | `tests/` | Pytest suites for logic, config, CLI, and GUI shims | Keeps quality gates close to the code and demonstrates headless GUI verification. |
| Docs | `docs/` | Installation, technical reference, and this guide | Separates user-facing and developer-facing instructions. |
| Build scripts | `wheel-builder.bat`, `pyproject.toml` | Packaging, wheel creation, installer automation | Shows how to go from repo to distributable artifacts with one command. |

**Why start here?** Knowing how the template is organized lets you change only what you need while keeping the proven plumbing intact.

---

## 2. Bootstrap Your Copy

1. **Clone or download** the repository.
2. **Create a virtual environment** (`python -m venv .venv`) and activate it.
3. **Install the package in editable mode** (`pip install -e .`) plus dev tools (`pip install -r requirements.txt`).

> **Why this flow?** The editable install mirrors how end users will consume the wheel while still giving you hot-reload style development inside `src/`. A dedicated virtual environment keeps global Python installations clean and matches the installer’s behavior.

---

## 3. Rename the Template Safely

1. Update `pyproject.toml` metadata (`[project] name`, `description`, version, authors).
2. Rename the package directory under `src/` (e.g., `tictactoe` → `myapp`).
3. Adjust import paths, entry points in `src/<your-package>/__main__.py`, and `tictactoe.egg-info` (regenerated automatically on the next build).

> **Why these files?** `pyproject.toml` drives packaging metadata, installers, and shortcuts. Renaming the src directory keeps the module namespace aligned. Entry points are how users launch the app; changing them early prevents stray `tictactoe` references later.

---

## 4. Keep the Architecture Contracts

The template follows an MVC-inspired split:

- `domain/logic.py`: Pure game rules (Model).
- `ui/gui` & `ui/cli`: Presentation layers (View) plus light controllers.
- `config/`: Typed dataclasses controlling visuals and copy.

**Steps:**
1. Replace the sample Tic Tac Toe logic with your own business rules while preserving the existing public API (`GameState`, `make_move`, etc.) or refactor both domain and UI together so the contracts stay aligned.
2. Customize GUI behavior through `tictactoe.ui.gui.view` and `tictactoe.ui.gui.main`, keeping `HeadlessGameView` intact for tests.
3. Extend or replace the CLI client under `tictactoe.ui.cli.main` if you need automation hooks.

> **Why MVC?** Clear boundaries let you test logic without GUI scaffolding, swap UIs (CustomTkinter, headless, CLI) without touching domain code, and reuse installers for future interfaces.

---

## 5. Leverage the Multi-Frontend Entry Point

`python -m tictactoe` (rename this module after cloning) is a dispatcher that selects a frontend via `--ui` or environment variables.

**How to adapt it:**
1. Register new frontends in `tictactoe.__main__.py` by extending the `FRONTENDS` map.
2. Honor `TICTACTOE_UI` / `TICTACTOE_HEADLESS` equivalents in your code if you rename the package (these env vars are read before CLI args to support silent installers and CI).

> **Why this design?** Installers and automated tests can switch interfaces without copying multiple entry scripts. It also demonstrates how to offer both GUI and CLI experiences from a single distribution.

---

## 6. Customize Look & Feel via Config

1. Edit or extend the dataclasses in `tictactoe.config.gui` (`GameViewConfig`, `ColorConfig`, etc.).
2. Pass new configs into `TicTacToeGUI` in `ui/gui/main.py`, or expose CLI flags/env vars to load presets.
3. Replace assets in `src/tictactoe/assets`, especially `favicon.ico`, to match your branding.

> **Why config objects?** Centralized styling prevents magic numbers in widgets, makes theming testable, and enables future JSON/YAML-driven skins without rewriting the GUI.

---

## 7. Maintain Quality Gates

1. Run `python -m pytest` (use `-m "not gui"` for non-GUI suites, `-m gui` for shimmed GUI tests).
2. Execute `python -m black --check`, `python -m ruff check`, and `python -m mypy src` to match the template’s lint/type expectations.
3. Consider `python -m tox -e lint,type,py313` to mirror future CI automation.

> **Why enforce these tools?** They showcase a production-ready pipeline: formatters keep diffs small, Ruff catches common mistakes, Mypy secures interfaces between domain and UI, and pytest ensures headless GUI regressions are caught before release.

---

## 8. Build & Ship Like the Template

1. Run `./wheel-builder.bat` from PowerShell.
2. Inspect `dist/` for:
   - Wheel file (`*.whl`)
   - `installation.bat` (one-click installer)
   - `tic-tac-toe-starter.vbs` (runs without console)
   - Packaged assets/icon
3. Test the installer on a clean user account if possible.

> **Why batch + VBScript?** The batch file handles environment creation, wheel installation, and shortcuts. The VBScript launcher hides the console, giving a native desktop feel. Both scripts demonstrate Windows-friendly distribution without MSI complexity.

---

## 9. Update Docs for Your Audience

1. `README.md`: Reframe goals, features, and screenshots for your app.
2. `docs/INSTALLATION-GUIDE.md`: Keep step-by-step install instructions accurate (installer paths, shortcuts, supported OS).
3. `docs/INSTALLATION-TECHNICAL-DETAILS.md`: Document any changes to installer logic, dependencies, or required permissions.
4. Add changelog or FAQ sections if your project will see frequent releases.

> **Why so much documentation?** The template treats docs as core deliverables, ensuring that both end users and developers can understand the installer flow and make safe modifications later.

---

## 10. Optional Enhancements

- **Add Controllers:** If your app needs complex orchestration, introduce a `controller/` package and let entry points compose it.
- **Instrument Telemetry:** Hook analytics or logging in `ui/gui/main.py` where events already flow.
- **Bundle Additional Assets:** Extend `assets/` and reference them via `importlib.resources` for portability.
- **Automate CI/CD:** Use GitHub Actions or Azure Pipelines to trigger `wheel-builder.bat` and publish releases automatically.

Each enhancement follows the same philosophy: keep cross-cutting concerns (distribution, configuration, quality) decoupled from your domain logic.

---

## Recap of Design Choices

1. **`src/` Layout:** Prevents accidental imports and mirrors packaging reality.
2. **CustomTkinter + Headless View:** Balances rich UI with CI-friendly tests by providing a protocol-driven view adapter.
3. **Env-Aware Entry Point:** Makes installers, scripts, and developers share the same binary with different frontends.
4. **Typed Config Layer:** Encourages theming and copy updates without widget churn.
5. **Batch Installer:** Demonstrates how to deliver a Python app with desktop shortcuts and isolated dependencies on Windows.
6. **Comprehensive Tooling:** Black/Ruff/Mypy/Pytest show how to enforce quality gates in GUI-heavy projects.

Adopting this template means inheriting these proven decisions. Modify them deliberately—and document why—so future contributors can follow your lead.
