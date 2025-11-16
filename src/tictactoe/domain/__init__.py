"""Domain module exposing the template-friendly placeholder layer."""

from .logic import (
	ExampleAction,
	ExampleActor,
	ExampleState,
	GameSnapshot,
	GameState,
	Player,
	TicTacToe,
)

__all__ = [
	"TicTacToe",
	"ExampleState",
	"ExampleAction",
	"ExampleActor",
	"Player",
	"GameState",
	"GameSnapshot",
]
