from __future__ import annotations

# Builtin
from enum import Enum
from typing import Dict, List, Tuple

# Pip
import arcade

# Custom
from entities.entity import Entity


class ScoreAmount(Enum):
    """Stores the amount of points each action will give the player."""

    COIN: int = 1
    ENEMY: int = 5
    QUESTION_CORRECT: int = 10
    QUESTION_WRONG: int = -5


class Player(Entity):
    """
    Represents a playable character in the game.

    Parameters
    ----------
    x: float
        The x position of the player.
    y: float
        The y position of the player.
    texture_dict: Dict[str, List[Tuple[arcade.Texture, arcade.Texture]]]
        The textures which represent this entity.
    health: int
        The health of the entity.

    Attributes
    ----------
    score: int
        The score for the player.
    """

    def __init__(
        self,
        x: float,
        y: float,
        texture_dict: Dict[str, List[Tuple[arcade.Texture, arcade.Texture]]],
        health: int,
    ) -> None:
        super().__init__(x, y, texture_dict, health)
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
