"""Headless stand-ins that mimic the CustomTkinter API for testing."""

from __future__ import annotations

from typing import Any, Callable, Dict, Optional

__HEADLESS__ = True


class CTkFont:
    """Minimal font placeholder used by tests."""

    def __init__(self, size: int = 12, weight: str = "normal") -> None:
        self.size = size
        self.weight = weight


class _Widget:
    def __init__(self, master: Optional["_Widget"] = None, **kwargs: Any) -> None:
        self.master = master
        self._options: Dict[str, Any] = dict(kwargs)
        self._grid: Dict[str, Any] = {}
        self._packed: Dict[str, Any] = {}

    # Layout no-ops ---------------------------------------------------------
    def pack(self, **kwargs: Any) -> None:
        self._packed = dict(kwargs)

    def grid(self, **kwargs: Any) -> None:
        self._grid = dict(kwargs)

    # Configuration helpers -------------------------------------------------
    def configure(self, **kwargs: Any) -> None:
        self._options.update(kwargs)

    def cget(self, key: str) -> Any:
        return self._options.get(key)

    # Lifecycle -------------------------------------------------------------
    def destroy(self) -> None:  # pragma: no cover - trivial
        self._options.clear()


class CTk(_Widget):
    """Simplified CTk root window."""

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self._title = ""
        self._geometry = ""

    def title(self, value: str) -> None:
        self._title = value

    def geometry(self, value: str) -> None:
        self._geometry = value

    def resizable(self, *_: Any) -> None:
        return None

    def iconbitmap(
        self, *args: Any, **kwargs: Any
    ) -> None:  # pragma: no cover - no behavior
        return None

    def after(self, _delay: int, callback: Callable[[], None]) -> None:
        callback()

    def mainloop(self) -> None:  # pragma: no cover - no GUI loop in tests
        return None


class CTkFrame(_Widget):
    pass


class CTkLabel(_Widget):
    pass


class CTkButton(_Widget):
    def __init__(
        self, *args: Any, command: Optional[Callable[[], None]] = None, **kwargs: Any
    ) -> None:
        super().__init__(**kwargs)
        self._command = command

    def invoke(self) -> None:
        if self._command:
            self._command()


def set_appearance_mode(_mode: str) -> None:  # pragma: no cover - compatibility shim
    return None


def set_default_color_theme(
    _theme: str,
) -> None:  # pragma: no cover - compatibility shim
    return None
