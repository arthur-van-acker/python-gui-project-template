"""GUI implementation for Tic Tac Toe using CustomTkinter."""

from __future__ import annotations

import json
import os
from typing import Any, Callable, Optional, Protocol

from tictactoe.controller import (
    ControllerHooks,
    logging_hooks,
    telemetry_logging_requested,
)
from tictactoe.config import GameViewConfig, WindowConfig, deserialize_game_view_config
from tictactoe.domain.logic import GameSnapshot, TicTacToe
from tictactoe.ui.gui import bootstrap
from tictactoe.ui.gui.contracts import GameViewPort
from tictactoe.ui.gui.theme import apply_default_theme
from tictactoe.ui.gui.view import GameView

bootstrap.configure_windows_app_model()

_THEME_PAYLOAD_ENV_VAR = "TICTACTOE_THEME_PAYLOAD"
_GUI_TELEMETRY_ENV_VAR = "TICTACTOE_GUI_LOGGING"


def _telemetry_logging_requested() -> bool:
    return telemetry_logging_requested(_GUI_TELEMETRY_ENV_VAR)


def _theme_from_env() -> Optional[GameViewConfig]:
    payload = os.environ.get(_THEME_PAYLOAD_ENV_VAR)
    if not payload:
        return None
    try:
        data = json.loads(payload)
    except json.JSONDecodeError:
        return None
    try:
        return deserialize_game_view_config(data)
    except Exception:
        return None

GameFactory = Callable[[], TicTacToe]


class ViewFactory(Protocol):
    def __call__(
        self,
        *,
        ctk_module: Any,
        root: Any,
        on_cell_click: Callable[[int], None],
        on_reset: Callable[[], None],
        view_config: GameViewConfig,
    ) -> GameViewPort: ...


def _build_default_view(
    *,
    ctk_module: Any,
    root: Any,
    on_cell_click: Callable[[int], None],
    on_reset: Callable[[], None],
    view_config: GameViewConfig,
) -> GameView:
    """Create the default GameView instance."""

    return GameView(
        ctk_module=ctk_module,
        root=root,
        on_cell_click=on_cell_click,
        on_reset=on_reset,
        view_config=view_config,
    )


class TicTacToeGUI:
    """Main GUI application for Tic Tac Toe."""

    def __init__(
        self,
        *,
        game_factory: Optional[GameFactory] = None,
        view_factory: Optional[ViewFactory] = None,
        window_config: Optional[WindowConfig] = None,
        view_config: Optional[GameViewConfig] = None,
        controller_hooks: Optional[ControllerHooks] = None,
    ):
        """Initialize the GUI application with injectable hooks."""

        self._game_factory = game_factory or TicTacToe
        self._view_factory = view_factory or _build_default_view
        self._controller_hooks = controller_hooks
        self.window_config = window_config or WindowConfig()
        env_view_config = _theme_from_env()
        self.view_config = view_config or env_view_config or GameViewConfig()

        self.game = self._game_factory()
        self._ctk_env = bootstrap.load_customtkinter()
        self.ctk = self._ctk_env.module
        self._ctk_headless = self._ctk_env.headless
        self.root = self._create_root()

        self.root.title(self.window_config.title)
        self.root.geometry(self.window_config.geometry)
        self.root.resizable(*self.window_config.resizable)

        apply_default_theme(self.ctk)

        self.icon_path = bootstrap.locate_icon_file()
        bootstrap.apply_window_icon(
            self.root, self.icon_path, headless=self._ctk_headless
        )

        self.view = self._view_factory(
            ctk_module=self.ctk,
            root=self.root,
            on_cell_click=self._on_cell_click,
            on_reset=self._reset_game,
            view_config=self.view_config,
        )
        self.view.build()
        self._emit_view_event(
            "initialized",
            view=self.view.__class__.__name__,
            theme=self.view_config.text.title,
        )

        self.game.add_listener(self._on_game_updated)
        self._on_game_updated(self.game.snapshot)

    def _create_root(self):
        """Create the root window with fallback to headless widgets."""

        module, root, env = bootstrap.create_root(self._ctk_env)
        self.ctk = module
        self._ctk_env = env
        self._ctk_headless = env.headless
        return root

    def _on_cell_click(self, position: int):
        """Handle cell button click."""
        self._emit_view_event("cell_click", position=position)
        try:
            self.game.make_move(position)
        except Exception as exc:
            self._report_controller_error(exc, action="cell_click", position=position)
            raise

    def _on_game_updated(self, snapshot: GameSnapshot) -> None:
        """Render the latest game snapshot to the UI widgets."""

        self._emit_domain_event(
            "snapshot",
            state=snapshot.state.value,
            current_player=snapshot.current_player.value
            if snapshot.current_player
            else None,
            winner=snapshot.winner.value if snapshot.winner else None,
            notes=len(snapshot.notes),
        )
        if not self.view.is_ready():
            return

        self.view.render(snapshot)

    def _reset_game(self):
        """Reset the game to initial state."""
        self._emit_view_event("reset_requested")
        try:
            self.game.reset()
        except Exception as exc:
            self._report_controller_error(exc, action="reset")
            raise

    def run(self):
        """Start the GUI application."""
        # Set icon after everything is initialized (CustomTkinter workaround)
        bootstrap.schedule_icon_refresh(
            self.root, self.icon_path, headless=self._ctk_headless
        )
        self.root.mainloop()

    def _emit_view_event(self, action: str, **payload: Any) -> None:
        if not self._controller_hooks:
            return
        self._controller_hooks.emit("view", action, **payload)

    def _emit_domain_event(self, action: str, **payload: Any) -> None:
        if not self._controller_hooks:
            return
        self._controller_hooks.emit("domain", action, **payload)

    def _report_controller_error(
        self, exc: Exception, *, action: str, **payload: Any
    ) -> None:
        if not self._controller_hooks:
            return
        self._controller_hooks.emit_error(exc, action=action, **payload)


def main():
    """Entry point for the GUI application."""
    hooks = logging_hooks() if _telemetry_logging_requested() else None
    app = TicTacToeGUI(controller_hooks=hooks)
    app.run()


if __name__ == "__main__":
    main()
