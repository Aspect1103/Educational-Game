from __future__ import annotations

# Builtin
from typing import TYPE_CHECKING, Tuple

# Pip
import arcade
from constants import ENEMY_MOVEMENT_FORCE, ENEMY_VIEW_DISTANCE, SPRITE_SIZE

# Custom
from entities.entity import Entity

if TYPE_CHECKING:
    from entities.player import Player


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
    health: int
        The health of the entity.
    """

    def __init__(
        self, x: float, y: float, texture: arcade.Texture, health: int
    ) -> None:
        super().__init__(x, y, texture, health)

    def __repr__(self) -> str:
        return f"<Enemy (Position=({self.center_x}, {self.center_y}))>"

    def calculate_movement(
        self, player: Player, walls: arcade.SpriteList
    ) -> Tuple[Tuple[float, float], int]:
        """
        Moves towards the player at a constant speed if they are within 5 tiles of the
        player and the enemy has line of sight.

        Parameters
        ----------
        player: Player
            The player entity.
        walls: arcade.SpriteList
            The wall tiles which block the enemy's vision.

        Returns
        -------
        Tuple[Tuple[float, float], int]
            A tuple containing the calculated force to apply to the enemy to move it
            towards the player and the new direction the enemy should face.
        """
        if arcade.has_line_of_sight(
            (self.center_x, self.center_y),
            (player.center_x, player.center_y),
            walls,
            SPRITE_SIZE * ENEMY_VIEW_DISTANCE,
        ):
            # Calculate the direction of travel
            if self.center_x < player.center_x:
                direction = 1
            else:
                direction = -1
            # Apply the movement force
            return (direction * ENEMY_MOVEMENT_FORCE, 0), direction
        # Enemy does not have line of sight and is not within range
        return (0, 0), self.facing
