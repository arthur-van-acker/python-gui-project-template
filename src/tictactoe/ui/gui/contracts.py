"""Shared UI contracts to keep view adapters toolkit-agnostic."""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from tictactoe.domain.logic import GameSnapshot


@runtime_checkable
class SupportsText(Protocol):
    """Simple label-like surface that exposes read/write text."""

    def configure(self, *, text: str) -> None: ...

    def cget(self, key: str) -> str: ...

    def pack(self, *args, **kwargs) -> None: ...


@runtime_checkable
class CellButton(Protocol):
    """Minimal contract shared by cell controls across adapters."""

    def configure(self, *, text: str, state: str) -> None: ...

    def cget(self, key: str) -> str: ...


@runtime_checkable
class ResetControl(Protocol):
    """Reset button surface used by both headless and CustomTk views."""

    def configure(
        self,
        *,
        text: str | None = None,
        state: str | None = None,
    ) -> None: ...

    def cget(self, key: str) -> str: ...

    def pack(self, *args, **kwargs) -> None: ...


class GameViewPort(Protocol):
    """High-level facade the controller and tests interact with."""

    def build(self) -> None: ...

    def is_ready(self) -> bool: ...

    def render(self, snapshot: GameSnapshot) -> None: ...

    def cell_count(self) -> int: ...

    def cell_text(self, position: int) -> str: ...

    def cell_state(self, position: int) -> str: ...

    def status_text(self) -> str: ...

    def reset_button_label(self) -> str: ...
