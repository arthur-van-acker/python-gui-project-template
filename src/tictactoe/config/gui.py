"""Configuration objects for the GUI layer."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional, Tuple


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


__all__ = [
    "GameViewConfig",
    "FontConfig",
    "FontSpec",
    "LayoutConfig",
    "TextConfig",
    "ColorConfig",
    "WindowConfig",
]
