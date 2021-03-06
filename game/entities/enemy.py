from __future__ import annotations

# Builtin
from typing import TYPE_CHECKING, Dict, List, Tuple

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
    texture_dict: Dict[str, List[List[arcade.Texture]]]
        The textures which represent this enemy.
    health: int
        The health of the enemy.
    bullet_damage: int
        The amount of damage this enemy deals.

    Attributes
    ----------
    attack_cooldown: float
        The length of time an enemy has to wait before it can attack again.
    attack_counter: float
        The counter which will check if an enemy's cooldown has passed.
    """

    def __init__(
        self,
        x: float,
        y: float,
        texture_dict: Dict[str, List[List[arcade.Texture]]],
        health: int,
        bullet_damage: int,
    ) -> None:
        super().__init__(x, y, texture_dict, health, bullet_damage)
        self.attack_cooldown: float = 0
        self.attack_counter: float = 0

    def __repr__(self) -> str:
        return f"<Enemy (Position=({self.center_x}, {self.center_y}))>"

    def calculate_movement(
        self, player: Player, walls: arcade.SpriteList
    ) -> Tuple[float, float]:
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
        Tuple[float, float]
            A tuple containing the calculated force to apply to the enemy to move it
            towards the player.
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
            return direction * ENEMY_MOVEMENT_FORCE, 0
        # Enemy does not have line of sight and is not within range
        return 0, 0

    def set_cooldown(self, cooldown: float) -> None:
        """
        Sets the enemy's attack cooldown.

        Parameters
        ----------
        cooldown: float
            The enemy's attack cooldown.
        """
        self.attack_cooldown = cooldown
