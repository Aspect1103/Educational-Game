from __future__ import annotations

# Builtin
from enum import Enum

# Pip
import arcade

# Custom
from constants import SPRITE_SCALE
from textures.textures import textures


class ScoreAmount(Enum):
    """Stores the amount of points each action will give the player."""

    COIN: int = 1
    ENEMY: int = 5
    QUESTION: int = 10


class Player(arcade.Sprite):
    """
    Represents a playable character in the game.

    Parameters
    ----------
    x: int
        The x position of the player.
    y: int
        The y position of the player.

    Attributes
    ----------
    texture: arcade.Texture
        The sprite which represents this player.
    score: int
        The score for the player.
    """

    def __init__(self, x: int, y: int) -> None:
        super().__init__(scale=SPRITE_SCALE)
        self.center_x: float = x
        self.center_y: float = y
        self.texture: arcade.Texture = textures["player"][0]
        self.score: int = 0

    def __repr__(self) -> str:
        return f"<Player (Position=({self.center_x}, {self.center_y}))>"

    def update_score(self, amount: ScoreAmount) -> None:
        """
        Adds the points for an action to the player's score.

        Parameters
        ----------
        amount: ScoreAmount
            The amount of points to give to the player.
        """
        self.score += amount.value
