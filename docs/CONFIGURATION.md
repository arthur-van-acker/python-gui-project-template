# Configuration & Theming Reference

All GUI customization lives under `tictactoe.config.gui`. The dataclasses are immutable so you can safely share them across widgets or freeze instances into settings files. This guide enumerates each knob, default value, and where it flows.

## WindowConfig
| Field | Type | Default | Used By | Notes |
| --- | --- | --- | --- | --- |
| `title` | `str` | `"Tic Tac Toe"` | `TicTacToeGUI` | Window caption shown in title bar and taskbar.
| `geometry` | `str` | `"400x600"` | `TicTacToeGUI` | Standard Tk geometry string (`WIDTHxHEIGHT`).
| `resizable` | `Tuple[bool, bool]` | `(False, False)` | `TicTacToeGUI` | Toggle resizing on X/Y axes.

## FontSpec & FontConfig
`FontSpec` describes a single CustomTkinter font. `FontConfig` groups per-widget selections.

| Field | Default | Widget(s) |
| --- | --- | --- |
| `title` | `FontSpec(size=32, weight="bold")` | Title label at top of GUI.
| `status` | `FontSpec(size=20)` | Status message beneath the title.
| `cell` | `FontSpec(size=32, weight="bold")` | 3x3 grid buttons.
| `reset` | `FontSpec(size=16)` | "New Game" button.

Change size/weight pairs to match your branding. To add italics or custom families, extend `FontSpec` to include a `family` property and update `GameView` font creation.

## LayoutConfig
Spacing, sizing, and padding values (all integers unless noted):

| Field | Default | Purpose |
| --- | --- | --- |
| `title_padding` | `20` | Vertical padding above/below the title.
| `status_padding` | `10` | Space between status text and board.
| `board_padding` | `(20, 20)` | Horizontal/vertical padding surrounding the 3x3 grid.
| `cell_size` | `(100, 100)` | Width/height of each button in pixels.
| `cell_spacing` | `5` | Gap between buttons.
| `reset_padding` | `20` | Distance between the grid and reset button.

## TextConfig
User-facing copy, including template strings:

| Field | Default | Notes |
| --- | --- | --- |
| `title` | `"Tic Tac Toe"` | Top-level heading.
| `reset_button` | `"New Game"` | Text on the reset button.
| `draw_message` | `"It's a draw!"` | Status message when neither player wins.
| `win_message_template` | `"Player {winner} wins!"` | `{winner}` placeholder replaced with `X` or `O`.
| `turn_message_template` | `"Player {player}'s turn"` | `{player}` placeholder uses `snapshot.current_player`.

When localizing, duplicate this dataclass with translated strings and inject via environment flag or CLI option.

## ColorConfig
All values are hex strings or theme names accepted by CustomTkinter; `None` defers to the active theme.

| Field | Purpose |
| --- | --- |
| `title_text` | Foreground color for the title label.
| `status_text` | Foreground color for the status label.
| `board_background` | Frame background behind the grid.
| `cell_text` | Text color inside grid buttons.
| `cell_fg` | Primary button color.
| `cell_hover` | Hover/focus color.
| `reset_fg` | Reset button background.

## GameViewConfig
Aggregate used when instantiating `GameView`/`HeadlessGameView`.

```python
from tictactoe.config import GameViewConfig, FontConfig, FontSpec, ColorConfig

highlight_theme = GameViewConfig(
    fonts=FontConfig(cell=FontSpec(size=40, weight="bold")),
    colors=ColorConfig(cell_fg="#0044FF", reset_fg="#00AAFF"),
)

TicTacToeGUI(view_config=highlight_theme)
```

### Propagation Map
- `GameViewConfig.fonts` → widget `.configure(font=...)` calls inside `ui/gui/view.py`.
- `GameViewConfig.layout` → grid geometry manager padding, width/height options, and cell sizing logic.
- `GameViewConfig.text` → initial label/button text plus runtime status rendering.
- `GameViewConfig.colors` → passed into `GameView._style_button` and `HeadlessGameView` string outputs (for parity tests).

## Supplying Config at Runtime
1. **Code Injection:** Pass `window_config` / `view_config` directly into `TicTacToeGUI` when constructing custom launchers.
2. **Environment Variables:** Extend `tictactoe.__main__` to parse theme names (e.g., `TICTACTOE_THEME=solarized`). Resolve the theme into a `GameViewConfig` instance before creating the GUI.
3. **Serialized Settings:** Convert dataclasses to dictionaries with `dataclasses.asdict()` and persist as JSON/YAML. Load at startup and rebuild the dataclasses (all fields are plain Python types).

By keeping every visual tweak inside these dataclasses, you can offer end users advanced theming without touching widget code, and write automated tests that ensure themes stay consistent across releases.
