"""Game logic for Tic Tac Toe."""

from dataclasses import dataclass
from enum import Enum
from typing import Callable, Optional, Tuple


class Player(Enum):
    """Represents a player in the game."""

    X = "X"
    O = "O"  # noqa: E741 - keep single-letter enum for board notation


class GameState(Enum):
    """Represents the current state of the game."""

    PLAYING = "playing"
    X_WON = "x_won"
    O_WON = "o_won"
    DRAW = "draw"


BoardTuple = Tuple[Optional["Player"], ...]


@dataclass(frozen=True)
class GameSnapshot:
    """Immutable view of the current game state."""

    board: BoardTuple
    current_player: "Player"
    state: "GameState"
    winner: Optional["Player"]


class TicTacToe:
    """Main game logic for Tic Tac Toe."""

    def __init__(self):
        """Initialize a new game."""
        self._listeners: list[Callable[[GameSnapshot], None]] = []
        self._board: list[Optional[Player]] = [None for _ in range(9)]
        self.current_player: Player = Player.X
        self.state: GameState = GameState.PLAYING
        self.reset()

    def add_listener(self, listener: Callable[[GameSnapshot], None]) -> None:
        """Register a callback to be invoked whenever the game state changes."""

        self._listeners.append(listener)

    def remove_listener(self, listener: Callable[[GameSnapshot], None]) -> None:
        """Remove a previously registered listener."""

        if listener in self._listeners:
            self._listeners.remove(listener)

    @property
    def board(self) -> BoardTuple:
        """Return an immutable view of the board."""

        return tuple(self._board)

    @property
    def snapshot(self) -> GameSnapshot:
        """Return a snapshot that summarizes the current game state."""

        return GameSnapshot(
            board=self.board,
            current_player=self.current_player,
            state=self.state,
            winner=self.get_winner(),
        )

    def make_move(self, position: int) -> bool:
        """
        Make a move at the specified position.

        Args:
            position: Board position (0-8)

        Returns:
            True if move was successful, False otherwise
        """
        if self.state != GameState.PLAYING:
            return False

        if position < 0 or position > 8:
            return False

        if self._board[position] is not None:
            return False

        self._board[position] = self.current_player
        self._check_game_state()

        if self.state == GameState.PLAYING:
            self.current_player = (
                Player.O if self.current_player == Player.X else Player.X
            )

        self._notify_listeners()

        return True

    def _check_game_state(self) -> None:
        """Check if the game has been won or drawn."""
        # Check rows
        for i in range(0, 9, 3):
            if (
                self._board[i] is not None
                and self._board[i] == self._board[i + 1] == self._board[i + 2]
            ):
                self.state = (
                    GameState.X_WON if self._board[i] == Player.X else GameState.O_WON
                )
                return

        # Check columns
        for i in range(3):
            if (
                self._board[i] is not None
                and self._board[i] == self._board[i + 3] == self._board[i + 6]
            ):
                self.state = (
                    GameState.X_WON if self._board[i] == Player.X else GameState.O_WON
                )
                return

        # Check diagonals
        if (
            self._board[0] is not None
            and self._board[0] == self._board[4] == self._board[8]
        ):
            self.state = (
                GameState.X_WON if self._board[0] == Player.X else GameState.O_WON
            )
            return

        if (
            self._board[2] is not None
            and self._board[2] == self._board[4] == self._board[6]
        ):
            self.state = (
                GameState.X_WON if self._board[2] == Player.X else GameState.O_WON
            )
            return

        # Check for draw
        if all(cell is not None for cell in self._board):
            self.state = GameState.DRAW

    def reset(self) -> None:
        """Reset the game to initial state."""
        self._board = [None for _ in range(9)]
        self.current_player = Player.X
        self.state = GameState.PLAYING
        self._notify_listeners()

    def get_winner(self) -> Optional[Player]:
        """Get the winning player if any."""
        if self.state == GameState.X_WON:
            return Player.X
        elif self.state == GameState.O_WON:
            return Player.O
        return None

    def _notify_listeners(self) -> None:
        """Notify all registered listeners of the latest snapshot."""

        if not self._listeners:
            return

        snapshot = self.snapshot
        for listener in list(self._listeners):
            listener(snapshot)
