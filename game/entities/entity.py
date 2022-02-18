from __future__ import annotations

# Builtin
from typing import Tuple

# Pip
import arcade

# Custom
from constants import FACING_RIGHT, SPRITE_SCALE


class Bullet(arcade.SpriteSolidColor):
    """
    Represents a bullet in the game.

    Parameters
    ----------
    x: float
        The starting x position of the bullet.
    y: float
        The starting y position of the bullet.
    width: int
        Width of the bullet.
    height: int
        Height of the bullet.
    color: Tuple[int, int, int]
        The color of the bullet.
    direction: int
        The direction of the bullet. 1 is right and -1 is left.
    """

    def __init__(
        self,
        x: float,
        y: float,
        width: int,
        height: int,
        color: Tuple[int, int, int],
        direction: int,
    ) -> None:
        super().__init__(width=width, height=height, color=color)
        self.center_x: float = x
        self.center_y: float = y
        self.direction: int = direction

    def __repr__(self) -> str:
        return f"<Bullet (Position=({self.center_x}, {self.center_y}))>"


class Entity(arcade.Sprite):
    """
    Represents an entity in the game.

    Parameters
    ----------
    x: float
        The x position of the entity.
    y: float
        The y position of the entity.
    texture: arcade.Texture
        The sprite which represents this entity.

    Attributes
    ----------
    time_since_last_attack: float
        How long it has been since the last attack.
    facing: int
        The direction the player is facing. 1 is right and -1 is left.
    """

    def __init__(self, x: float, y: float, texture: arcade.Texture) -> None:
        super().__init__(scale=SPRITE_SCALE)
        self.center_x: float = x
        self.center_y: float = y
        self.texture: arcade.Texture = texture
        self.time_since_last_attack: float = 0
        self.facing: int = FACING_RIGHT

    def __repr__(self) -> str:
        return f"<Entity (Position=({self.center_x}, {self.center_y}))>"

    def ranged_attack(self, bullet_list: arcade.SpriteList) -> None:
        """
        Spawns a bullet in a specific direction.

        Parameters
        ----------
        bullet_list: arcade.SpriteList
            The sprite list to add the bullet to.
        """
        self.time_since_last_attack = 0
        bullet_list.append(
            Bullet(self.center_x, self.center_y, 54, 9, arcade.color.RED, self.facing)
        )
