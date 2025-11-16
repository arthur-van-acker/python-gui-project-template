"""Presentation layer utilities for the Tic Tac Toe GUI."""

from __future__ import annotations

from typing import Any, Callable, Dict, Optional, Sequence, cast

from tictactoe.config import FontSpec, GameViewConfig
from tictactoe.domain.logic import GameSnapshot, GameState, Player
from tictactoe.ui.gui.contracts import (
    CellButton,
    GameViewPort,
    ResetControl,
    SupportsText,
)


class GameView(GameViewPort):
    """Responsible for building and updating the widget tree."""

    def __init__(
        self,
        *,
        ctk_module,
        root,
        on_cell_click: Callable[[int], None],
        on_reset: Callable[[], None],
        view_config: GameViewConfig | None = None,
    ) -> None:
        self.ctk: Any = ctk_module
        self.root: Any = root
        self._on_cell_click = on_cell_click
        self._on_reset = on_reset
        self.config = view_config or GameViewConfig()

        self.title_label: SupportsText | None = None
        self.status_label: SupportsText | None = None
        self.board_frame: Any | None = None
        self.reset_button: ResetControl | None = None
        self.buttons: list[CellButton] = []
        self._built = False

    def build(self) -> None:
        """Construct all widgets for the application."""

        fonts = self._build_fonts()

        title_label = cast(
            SupportsText,
            self.ctk.CTkLabel(
            self.root,
            text=self.config.text.title,
            font=fonts["title"],
            **self._text_color_kwargs(self.config.colors.title_text),
            ),
        )
        self.title_label = title_label
        title_label.pack(pady=self.config.layout.title_padding)

        status_label = cast(
            SupportsText,
            self.ctk.CTkLabel(
            self.root,
            text="",
            font=fonts["status"],
            **self._text_color_kwargs(self.config.colors.status_text),
            ),
        )
        self.status_label = status_label
        status_label.pack(pady=self.config.layout.status_padding)

        board_frame_kwargs = self._frame_color_kwargs()
        self.board_frame = self.ctk.CTkFrame(self.root, **board_frame_kwargs)
        pady, padx = self.config.layout.board_padding
        self.board_frame.pack(pady=pady, padx=padx)

        self._build_board(fonts["cell"])
        self._build_reset_button(fonts["reset"])
        self._built = True

    def _build_board(self, font_button: Any) -> None:
        """Create the 3x3 grid of buttons."""

        self.buttons = []
        for position in range(9):
            button_kwargs = self._cell_button_color_kwargs()
            button = self.ctk.CTkButton(
                self.board_frame,
                text="",
                width=self.config.layout.cell_size[0],
                height=self.config.layout.cell_size[1],
                font=font_button,
                command=lambda pos=position: self._on_cell_click(pos),
                **button_kwargs,
            )
            button.grid(
                row=position // 3,
                column=position % 3,
                padx=self.config.layout.cell_spacing,
                pady=self.config.layout.cell_spacing,
            )
            self.buttons.append(button)

    def _build_reset_button(self, font_reset: Any) -> None:
        reset_kwargs = self._reset_button_color_kwargs()
        reset_button = cast(
            ResetControl,
            self.ctk.CTkButton(
            self.root,
            text=self.config.text.reset_button,
            font=font_reset,
            command=self._on_reset,
            **reset_kwargs,
            ),
        )
        self.reset_button = reset_button
        reset_button.pack(pady=self.config.layout.reset_padding)

    def render(self, snapshot: GameSnapshot) -> None:
        """Update the widget state to reflect the game snapshot."""

        if not self.is_ready():
            return

        self._ensure_built()

        self._render_board(snapshot.board)
        self._render_status(snapshot)

    def is_ready(self) -> bool:
        """Return True once build() has produced the widget tree."""

        return self._built

    def cell_count(self) -> int:
        self._ensure_built()
        return len(self.buttons)

    def cell_text(self, position: int) -> str:
        button = self._button_at(position)
        return button.cget("text")

    def cell_state(self, position: int) -> str:
        button = self._button_at(position)
        return button.cget("state")

    def status_text(self) -> str:
        if not self.status_label:
            return ""
        return self.status_label.cget("text")

    def reset_button_label(self) -> str:
        if not self.reset_button:
            return ""
        return self.reset_button.cget("text")

    def _render_board(self, board: Sequence[Optional[Player]]) -> None:
        for position, button in enumerate(self.buttons):
            cell = board[position]
            if cell is None:
                button.configure(text="", state="normal")
            else:
                button.configure(text=cell.value, state="disabled")

    def _render_status(self, snapshot: GameSnapshot) -> None:
        text = self._status_message(snapshot)
        if self.status_label is None:
            raise RuntimeError("status label is not initialized")
        self.status_label.configure(text=text)

    def _build_fonts(self) -> Dict[str, Any]:
        """Instantiate the CustomTkinter fonts from the config."""

        return {
            "title": self._create_font(self.config.fonts.title),
            "status": self._create_font(self.config.fonts.status),
            "cell": self._create_font(self.config.fonts.cell),
            "reset": self._create_font(self.config.fonts.reset),
        }

    def _create_font(self, spec: FontSpec) -> Any:
        kwargs: Dict[str, Any] = {"size": spec.size}
        if spec.weight:
            kwargs["weight"] = spec.weight
        return self.ctk.CTkFont(**kwargs)

    def _text_color_kwargs(self, color: str | None) -> Dict[str, str]:
        return {"text_color": color} if color else {}

    def _cell_button_color_kwargs(self) -> Dict[str, str]:
        colors = self.config.colors
        kwargs: Dict[str, str] = {}
        if colors.cell_text:
            kwargs["text_color"] = colors.cell_text
        if colors.cell_fg:
            kwargs["fg_color"] = colors.cell_fg
        if colors.cell_hover:
            kwargs["hover_color"] = colors.cell_hover
        return kwargs

    def _reset_button_color_kwargs(self) -> Dict[str, str]:
        colors = self.config.colors
        kwargs: Dict[str, str] = {}
        if colors.reset_fg:
            kwargs["fg_color"] = colors.reset_fg
        return kwargs

    def _frame_color_kwargs(self) -> Dict[str, str]:
        if not self.config.colors.board_background:
            return {}
        return {"fg_color": self.config.colors.board_background}

    def _status_message(self, snapshot: GameSnapshot) -> str:
        if snapshot.state == GameState.PLAYING:
            player = snapshot.current_player.value if snapshot.current_player else "?"
            return self.config.text.turn_message_template.format(player=player)
        if snapshot.state == GameState.DRAW:
            return self.config.text.draw_message
        winner = snapshot.winner.value if snapshot.winner else "Unknown"
        return self.config.text.win_message_template.format(winner=winner)

    def _ensure_built(self) -> None:
        if not self._built:
            raise RuntimeError("GameView widgets have not been built yet")

    def button_count(self) -> int:
        """Backward-compatible alias for cell_count."""

        return self.cell_count()

    def button_text(self, position: int) -> str:
        """Backward-compatible alias for cell_text."""

        return self.cell_text(position)

    def button_state(self, position: int) -> str:
        """Backward-compatible alias for cell_state."""

        return self.cell_state(position)

    def _button_at(self, position: int) -> CellButton:
        self._ensure_built()
        if position < 0 or position >= len(self.buttons):
            raise IndexError(position)
        return self.buttons[position]
