from __future__ import annotations

# Pip
import arcade

# Custom
from entities.entity import Entity


class Enemy(Entity):
    """
    Represents a hostile character in the game.

    Parameters
    ----------
    x: float
        The x position of the enemy.
    y: float
        The y position of the enemy.
    texture: arcade.Texture
        The sprite which represents this enemy.
    """

    def __init__(self, x: float, y: float, texture: arcade.Texture) -> None:
        super().__init__(x, y, texture)

    def __repr__(self) -> str:
        return f"<Enemy (Position=({self.center_x}, {self.center_y}))>"
