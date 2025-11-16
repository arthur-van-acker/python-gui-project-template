"""Configuration module for Tic Tac Toe application."""

from __future__ import annotations

from .gui import (
    ColorConfig,
    FontConfig,
    FontSpec,
    GameViewConfig,
    LayoutConfig,
    TextConfig,
    WindowConfig,
)

# The package intentionally keeps an empty __all__ so wildcard imports stay lean
# while direct attribute access (tictactoe.config.GameViewConfig) remains
# available for template consumers and aligns with the existing tests/docs.
__all__: list[str] = []
