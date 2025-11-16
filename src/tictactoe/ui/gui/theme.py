"""Theme helpers for the Tic Tac Toe GUI."""

from __future__ import annotations

from types import ModuleType


def apply_default_theme(ctk_module: ModuleType) -> None:
    """Apply the default appearance and color theme."""

    ctk_module.set_appearance_mode("light")
    ctk_module.set_default_color_theme("blue")
