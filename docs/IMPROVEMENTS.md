# Template Improvement Plan

Keep the repository focused on being a reusable CustomTkinter starter kit instead of a Tic Tac Toe demo. The items below capture the concrete enhancements to implement next, along with the primary files they touch.

## 1. Replace the Placeholder Domain Layer
- Swap the Tic Tac Toe logic in `src/tictactoe/domain/logic.py` and `tests/test_logic.py` for a neutral "ExampleState/ExampleAction" API that documents how adopters plug in their own business rules.
- Keep the existing view/controller contracts, but mark required override points with TODOs and ensure placeholder tests fail until custom rules exist so new projects know what to implement first.

## 2. Offer Multiple Frontend Entry Points
- Extend `src/tictactoe/__main__.py` to include more than the GUI launcher: add a CLI automation mode (`src/tictactoe/ui/cli/main.py`) and a headless/service entry point that showcases scripting or batch workflows.
- Document how to register additional frontends in the `FRONTENDS` map and surface selectors via CLI flags and `TICTACTOE_UI`-style environment variables for installer/CI parity.

## 3. Promote Configuration to Named Themes
- In `tictactoe.config.gui`, bundle at least two `GameViewConfig` presets (e.g., `LightTheme`, `DarkTheme`, `EnterpriseBrand`) and describe them in `docs/CONFIGURATION.md` with before/after screenshots when possible.
- Teach `tictactoe.__main__` to load themes from environment variables or JSON files so adopters can see runtime theming patterns without editing widget code.

## 4. Make Distribution & CI Match Real Products
- Update `wheel-builder.bat`, `installation.bat`, and `tic-tac-toe-starter.vbs` to demonstrate version stamping, custom shortcut names, asset copying, and a smoke-test hook executed after install.
- Mirror those steps inside `scripts/run-ci.ps1` (and `.sh`) so the template shows how to run linting, type-checking, pytest (GUI + non-GUI markers), and installer verification in a single command.

## 5. Rewrite Docs for Template Users
- Refresh `README.md`, `docs/TEMPLATE-USAGE-GUIDE.md`, and `docs/TEMPLATE-CHECKLIST.md` to speak about "YourApp Starter" instead of Tic Tac Toe, explicitly calling out the rename steps, config knobs, and required tests.
- Link each checklist item to the exact file/section to edit, making the adoption flow linear (rename → config → UI → installer → docs) so contributors can track progress at a glance.

## 6. Optional Stretch Ideas
- Provide a `controller/` package stub and show how to register telemetry/logging hooks in `ui/gui/main.py`.
- Include sample JSON theme files plus a script that converts them into dataclasses for rapid prototyping.
- Add a GitHub Actions workflow that runs the CI script and attaches installer artifacts, illustrating how teams can publish releases automatically.
