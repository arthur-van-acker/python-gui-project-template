"""Configuration objects for the GUI layer."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Dict, Mapping, Optional, Tuple


@dataclass(frozen=True)
class WindowConfig:
    """Window sizing and layout parameters."""

    title: str = "Tic Tac Toe"
    geometry: str = "400x600"
    resizable: Tuple[bool, bool] = (False, False)


@dataclass(frozen=True)
class FontSpec:
    """Immutable description of a CustomTkinter font."""

    size: int
    weight: Optional[str] = None


@dataclass(frozen=True)
class FontConfig:
    """Font selections for the primary widgets."""

    title: FontSpec = FontSpec(size=32, weight="bold")
    status: FontSpec = FontSpec(size=20)
    cell: FontSpec = FontSpec(size=32, weight="bold")
    reset: FontSpec = FontSpec(size=16)


@dataclass(frozen=True)
class LayoutConfig:
    """Spacing and sizing for the view widgets."""

    title_padding: int = 20
    status_padding: int = 10
    board_padding: Tuple[int, int] = (20, 20)
    cell_size: Tuple[int, int] = (100, 100)
    cell_spacing: int = 5
    reset_padding: int = 20


@dataclass(frozen=True)
class TextConfig:
    """Human-readable strings rendered by the GUI."""

    title: str = "Tic Tac Toe"
    reset_button: str = "New Game"
    draw_message: str = "It's a draw!"
    win_message_template: str = "Player {winner} wins!"
    turn_message_template: str = "Player {player}'s turn"


@dataclass(frozen=True)
class ColorConfig:
    """Color hooks for easy theming. Defaults keep CustomTkinter's theme."""

    title_text: Optional[str] = None
    status_text: Optional[str] = None
    board_background: Optional[str] = None
    cell_text: Optional[str] = None
    cell_fg: Optional[str] = None
    cell_hover: Optional[str] = None
    reset_fg: Optional[str] = None


@dataclass(frozen=True)
class GameViewConfig:
    """Aggregates every tweakable aspect of the view."""

    fonts: FontConfig = field(default_factory=FontConfig)
    layout: LayoutConfig = field(default_factory=LayoutConfig)
    text: TextConfig = field(default_factory=TextConfig)
    colors: ColorConfig = field(default_factory=ColorConfig)


# Named theme presets -----------------------------------------------------------------


def _base_theme() -> GameViewConfig:
    return GameViewConfig()


def _light_theme() -> GameViewConfig:
    return GameViewConfig(
        colors=ColorConfig(
            title_text="#222222",
            status_text="#444444",
            board_background="#F5F5F5",
            cell_text="#111111",
            cell_fg="#FFFFFF",
            cell_hover="#E0E0E0",
            reset_fg="#DDDDDD",
        ),
        text=TextConfig(title="YourApp Starter"),
    )


def _dark_theme() -> GameViewConfig:
    return GameViewConfig(
        colors=ColorConfig(
            title_text="#FFFFFF",
            status_text="#CCCCCC",
            board_background="#1F1F26",
            cell_text="#FFFFFF",
            cell_fg="#2E2E38",
            cell_hover="#3C3C4A",
            reset_fg="#4A4A5A",
        ),
        text=TextConfig(title="YourApp Starter (Dark)", reset_button="Restart"),
    )


def _enterprise_theme() -> GameViewConfig:
    return GameViewConfig(
        colors=ColorConfig(
            title_text="#0A1F44",
            status_text="#1B365D",
            board_background="#D9E8FF",
            cell_text="#0A1F44",
            cell_fg="#FFFFFF",
            cell_hover="#BBD0F5",
            reset_fg="#0A84FF",
        ),
        fonts=FontConfig(title=FontSpec(size=28, weight="bold")),
        text=TextConfig(title="Enterprise Suite", reset_button="Start Over"),
        layout=LayoutConfig(board_padding=(30, 30)),
    )


NAMED_THEMES: Dict[str, GameViewConfig] = {
    "default": _base_theme(),
    "light": _light_theme(),
    "dark": _dark_theme(),
    "enterprise": _enterprise_theme(),
}


def list_themes() -> list[str]:
    """Return the names of bundled presets for discovery in CLIs/docs."""

    return sorted(NAMED_THEMES.keys())


def serialize_game_view_config(config: GameViewConfig) -> Dict[str, Any]:
    """Convert a GameViewConfig into basic Python types (JSON friendly)."""

    return asdict(config)


def _font_spec_from(data: Mapping[str, Any] | None, fallback: FontSpec) -> FontSpec:
    if not data:
        return fallback
    return FontSpec(size=data.get("size", fallback.size), weight=data.get("weight", fallback.weight))


def _layout_from(data: Mapping[str, Any] | None, fallback: LayoutConfig) -> LayoutConfig:
    if not data:
        return fallback
    return LayoutConfig(
        title_padding=data.get("title_padding", fallback.title_padding),
        status_padding=data.get("status_padding", fallback.status_padding),
        board_padding=tuple(data.get("board_padding", fallback.board_padding)),
        cell_size=tuple(data.get("cell_size", fallback.cell_size)),
        cell_spacing=data.get("cell_spacing", fallback.cell_spacing),
        reset_padding=data.get("reset_padding", fallback.reset_padding),
    )


def _text_from(data: Mapping[str, Any] | None, fallback: TextConfig) -> TextConfig:
    if not data:
        return fallback
    return TextConfig(
        title=data.get("title", fallback.title),
        reset_button=data.get("reset_button", fallback.reset_button),
        draw_message=data.get("draw_message", fallback.draw_message),
        win_message_template=data.get("win_message_template", fallback.win_message_template),
        turn_message_template=data.get("turn_message_template", fallback.turn_message_template),
    )


def _color_from(data: Mapping[str, Any] | None, fallback: ColorConfig) -> ColorConfig:
    if not data:
        return fallback
    return ColorConfig(
        title_text=data.get("title_text", fallback.title_text),
        status_text=data.get("status_text", fallback.status_text),
        board_background=data.get("board_background", fallback.board_background),
        cell_text=data.get("cell_text", fallback.cell_text),
        cell_fg=data.get("cell_fg", fallback.cell_fg),
        cell_hover=data.get("cell_hover", fallback.cell_hover),
        reset_fg=data.get("reset_fg", fallback.reset_fg),
    )


def deserialize_game_view_config(payload: Mapping[str, Any]) -> GameViewConfig:
    """Rebuild GameViewConfig (and nested dataclasses) from a dictionary."""

    defaults = GameViewConfig()
    fonts_data = payload.get("fonts", {}) if isinstance(payload, Mapping) else {}
    layout_data = payload.get("layout", {}) if isinstance(payload, Mapping) else {}
    text_data = payload.get("text", {}) if isinstance(payload, Mapping) else {}
    color_data = payload.get("colors", {}) if isinstance(payload, Mapping) else {}

    fonts = FontConfig(
        title=_font_spec_from(fonts_data.get("title"), defaults.fonts.title),
        status=_font_spec_from(fonts_data.get("status"), defaults.fonts.status),
        cell=_font_spec_from(fonts_data.get("cell"), defaults.fonts.cell),
        reset=_font_spec_from(fonts_data.get("reset"), defaults.fonts.reset),
    )

    layout = _layout_from(layout_data, defaults.layout)
    text = _text_from(text_data, defaults.text)
    colors = _color_from(color_data, defaults.colors)
    return GameViewConfig(fonts=fonts, layout=layout, text=text, colors=colors)


def get_theme(name: str) -> GameViewConfig:
    """Fetch a cloned theme so callers can mutate without affecting globals."""

    key = name.strip().lower()
    try:
        theme = NAMED_THEMES[key]
    except KeyError as exc:
        available = ", ".join(list_themes())
        raise KeyError(f"Unknown theme '{name}'. Available: {available}.") from exc
    return deserialize_game_view_config(serialize_game_view_config(theme))


__all__ = [
    "GameViewConfig",
    "FontConfig",
    "FontSpec",
    "LayoutConfig",
    "TextConfig",
    "ColorConfig",
    "WindowConfig",
    "NAMED_THEMES",
    "get_theme",
    "list_themes",
    "serialize_game_view_config",
    "deserialize_game_view_config",
]
