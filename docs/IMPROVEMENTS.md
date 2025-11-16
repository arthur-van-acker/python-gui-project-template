# Template Improvement Plan

Keep the repository focused on being a reusable CustomTkinter starter kit instead of a Tic Tac Toe demo. The items below capture the concrete enhancements to implement next, along with the primary files they touch.

## 1. Replace the Placeholder Domain Layer
- Swap the Tic Tac Toe logic in `src/tictactoe/domain/logic.py` and `tests/test_logic.py` for a neutral "ExampleState/ExampleAction" API that documents how adopters plug in their own business rules.
- Keep the existing view/controller contracts, but mark required override points with TODOs and ensure placeholder tests fail until custom rules exist so new projects know what to implement first.
- ✅ Implemented: `ExampleState`, `ExampleAction`, and `ExampleActor` now power the domain placeholder while `tests/test_logic.py` verifies the snapshot contract and documents that `dispatch_action` raises `NotImplementedError` until adopters supply real rules.

## 2. Offer Multiple Frontend Entry Points
- Extend `src/tictactoe/__main__.py` to include more than the GUI launcher: add a CLI automation mode (`src/tictactoe/ui/cli/main.py`) and a headless/service entry point that showcases scripting or batch workflows.
- Document how to register additional frontends in the `FRONTENDS` map and surface selectors via CLI flags and `TICTACTOE_UI`-style environment variables for installer/CI parity.
- ✅ Implemented: `tictactoe.__main__` now dispatches `gui`, `headless`, `cli`, and `service` targets. The CLI gained script/file/JSON automation helpers while the new `tictactoe.ui.service.main` entry point consumes env vars (`TICTACTOE_SCRIPT`, etc.) so CI and installers can trigger headless runs without extra flags. README documents the new flags and environment overrides.

## 3. Promote Configuration to Named Themes
- In `tictactoe.config.gui`, bundle at least two `GameViewConfig` presets (e.g., `LightTheme`, `DarkTheme`, `EnterpriseBrand`) and describe them in `docs/CONFIGURATION.md` with before/after screenshots when possible.
- Teach `tictactoe.__main__` to load themes from environment variables or JSON files so adopters can see runtime theming patterns without editing widget code.
- ✅ Implemented: Added `NAMED_THEMES`, serialization helpers, README/CONFIGURATION docs, and updated `tictactoe.__main__`/GUI bootstrap to honor `--theme`, `--theme-file`, and `TICTACTOE_THEME*` environment variables.

## 4. Make Distribution & CI Match Real Products
- Update `wheel-builder.bat`, `installation.bat`, and `tic-tac-toe-starter.vbs` to demonstrate version stamping, custom shortcut names, asset copying, and a smoke-test hook executed after install.
- Mirror those steps inside `scripts/run-ci.ps1` (and `.sh`) so the template shows how to run linting, type-checking, pytest (GUI + non-GUI markers), and installer verification in a single command.
- ✅ Implemented: `wheel-builder.bat` now reads the project version, copies `assets/`, emits helper docs, and writes an `installation.bat` that installs into a stamped path, copies assets, creates shortcuts, and runs a `--ui service` smoke script before writing `install-info.json`. The PowerShell and Bash CI scripts install deps, run black/ruff/mypy plus both pytest marker sets, then perform installer verification (Windows invokes `wheel-builder.bat --ci`/`installation.bat`, POSIX shells build the wheel and exercise it inside a throwaway virtualenv sandbox).

## 5. Rewrite Docs for Template Users
- Refresh `README.md`, `docs/TEMPLATE-USAGE-GUIDE.md`, and `docs/TEMPLATE-CHECKLIST.md` to speak about "YourApp Starter" instead of Tic Tac Toe, explicitly calling out the rename steps, config knobs, and required tests.
- Link each checklist item to the exact file/section to edit, making the adoption flow linear (rename → config → UI → installer → docs) so contributors can track progress at a glance.
- ✅ Implemented: `README.md` now leads with the YourApp Starter branding, adds an adoption roadmap, and highlights the required config knobs/tests. `docs/TEMPLATE-USAGE-GUIDE.md` explains how to rename the package and swap the sample logic, while `docs/TEMPLATE-CHECKLIST.md` is reorganized into a linear workflow with direct links to the referenced files/sections.

## 6. Optional Stretch Ideas
- ✅ Provide a `controller/` package stub and show how to register telemetry/logging hooks in `ui/gui/main.py`. `tictactoe.controller` now ships with `ControllerHooks` plus a `logging_hooks()` helper, and every frontend honors the shared `TICTACTOE_LOGGING` flag (with legacy `*_LOGGING` env vars still supported) so teams can flip on telemetry without changing code.
- ✅ Include sample JSON theme files (`src/tictactoe/assets/themes/*.json`) plus the `python -m tictactoe.tools.theme_codegen` helper that converts them into `GameViewConfig` dataclasses for rapid prototyping.
- ✅ Add a GitHub Actions workflow (`.github/workflows/release.yml`) that runs `scripts/run-ci.ps1`, zips `dist/`, and uploads the installer bundle plus release assets so teams can publish automatically.
