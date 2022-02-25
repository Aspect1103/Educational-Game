from __future__ import annotations

# Builtin
from typing import TYPE_CHECKING, Dict, List, Tuple

# Pip
import arcade

# Custom
from constants import BULLET_DAMAGE, BULLET_VELOCITY, FACING_RIGHT, SPRITE_SCALE

if TYPE_CHECKING:
    from physics import PhysicsEngine


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
    texture_dict: Dict[str, List[Tuple[arcade.Texture, arcade.Texture]]]
        The textures which represent this entity.
    health: int
        The health of the entity.

    Attributes
    ----------
    texture: arcade.Texture
        The sprite which represents this entity.
    time_since_last_attack: float
        How long it has been since the last attack.
    facing: int
        The direction the entity is facing. 1 is right and -1 is left.
    """

    def __init__(
        self,
        x: float,
        y: float,
        texture_dict: Dict[str, List[Tuple[arcade.Texture, arcade.Texture]]],
        health: int,
    ) -> None:
        super().__init__(scale=SPRITE_SCALE)
        self.center_x: float = x
        self.center_y: float = y
        self.texture_dict: Dict[
            str, List[Tuple[arcade.Texture, arcade.Texture]]
        ] = texture_dict
        self.health: int = health
        self.texture: arcade.Texture = self.texture_dict["idle"][0][0]
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
        center_x = self.center_x
        if self.facing is FACING_RIGHT:
            center_x += 48
        else:
            center_x -= 48
        new_bullet = Bullet(
            center_x, self.center_y, 50, 10, arcade.color.RED, self.facing
        )
        physics: PhysicsEngine = self.physics_engines[0]
        physics.add_bullet(new_bullet)
        physics.set_velocity(new_bullet, (BULLET_VELOCITY * new_bullet.direction, 0))
        bullet_list.append(new_bullet)

    def deal_damage(self) -> None:
        """Deals damage to the entity."""
        self.health -= BULLET_DAMAGE

    def update_animation(self, delta_time: float = 1 / 60) -> None:
        """
        Updates the entity's sprite making it animated.

        Parameters
        ----------
        delta_time: float
            Time interval since the last time the function was called.
        """
