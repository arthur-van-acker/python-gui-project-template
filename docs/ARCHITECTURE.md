# Architecture Deep Dive

This template layers the application so domain logic, presentation, configuration, and installers remain independently replaceable. Use this guide when swapping in new gameplay mechanics, frontends, or deployment targets.

```
┌────────────────────────────────────────────────────────────────────┐
│                       Entry Points (`python -m tictactoe`)          │
└────────────────────────────────────────────────────────────────────┘
                │ select frontend (`--ui` or env vars)
┌───────────────┴───────────────┐
│ CLI (`ui/cli/main.py`)        │ GUI (`ui/gui/main.py`)             │
│ - Rich text loop              │ - CustomTkinter widgets            │
│ - Script automation           │ - Headless adapter option          │
└───────────────┬───────────────┘                │ calls
                │                                 ▼
        `domain/logic.py` (TicTacToe engine)  ────► Game snapshots
                │                                 ▲
                │ listens for updates             │ renders
┌───────────────┴───────────────┐                │
│ Config Layer (`config/gui.py`)│◄──────────────┘
│ - Fonts, layout, copy, colors │   injected into GUI + headless view
└───────────────┬───────────────┘
                │ assets (icons)
                ▼
        Installer Scripts (`wheel-builder.bat` → `installation.bat`, `tic-tac-toe-starter.vbs`)
```

## Domain Layer
- `tictactoe.domain.logic.TicTacToe` now ships as a neutral placeholder: it publishes `ExampleState` snapshots with TODO notes and raises `NotImplementedError` from `dispatch_action` until you plug in real business rules.
- Use the placeholder to document controller contracts, then extend or replace `dispatch_action` so the GUI/CLI surfaces keep working without structural changes.
- Listeners still consume `GameSnapshot` objects, letting you evolve the domain independently from the presentation layer.

## GUI Layer
- `TicTacToeGUI` composes the domain object, loads CustomTkinter via `ui.gui.bootstrap`, and instantiates a view through `view_factory`.
- `GameView` renders actual widgets; `HeadlessGameView` mirrors widget behavior without Tk bindings for CI.
- The headless adapter implements `GameViewPort` so tests can assert widget states without a display server.

## CLI Layer
- `ui/cli/main.py` interacts with the same domain layer but renders board state in the terminal.
- Useful for scripting and regression testing when GUI dependencies are unavailable.

## Configuration Layer
- `config/gui.py` exposes immutable data classes (`GameViewConfig`, `WindowConfig`, etc.) that flow into both GUI implementations.
- Changing fonts, padding, copy, or colors happens here instead of scattering constants through widgets.

## Installer & Distribution
- `wheel-builder.bat` orchestrates builds, copies assets, and generates helper scripts inside `dist/`.
- `installation.bat` provisions a per-user install under `%LOCALAPPDATA%\Programs\yourapp-starter-<version>` (or `%TEMP%` when built with `--ci`), creates a virtual environment, installs the wheel, and registers shortcuts via `tic-tac-toe-starter.vbs`.
- All desktop integration logic lives in batch/VBScript so the Python package stays pure.

## Extensibility Hooks
- **Frontends:** register new handlers in `tictactoe.__main__.FRONTENDS` and supply a compatible `main()` or factory.
- **View Adapters:** implement `GameViewPort` for new UI toolkits (e.g., Qt) while reusing the controller logic in `TicTacToeGUI`.
- **Theme Packs:** pass custom `GameViewConfig` instances into `TicTacToeGUI` or expose CLI flags/env vars to load presets.
- **Installers:** modify `wheel-builder.bat` to copy additional payloads or emit MSIX/NSIS scripts while keeping the Python wheel untouched.

Understanding these seams lets you evolve one layer without breaking others: domain swaps leave installers untouched, new installers do not require GUI edits, and headless adapters guarantee every frontend remains testable.
