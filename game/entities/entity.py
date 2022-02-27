from __future__ import annotations

# Builtin
from typing import TYPE_CHECKING, Dict, List, Tuple

# Pip
import arcade

# Custom
from constants import (
    BULLET_DAMAGE,
    BULLET_VELOCITY,
    DEAD_ZONE,
    DISTANCE_TO_CHANGE_TEXTURE,
    FACING_LEFT,
    FACING_RIGHT,
    SPRITE_SCALE,
)

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
    owner: Entity
        The entity which shot the bullet.
    """

    def __init__(
        self,
        x: float,
        y: float,
        width: int,
        height: int,
        color: Tuple[int, int, int],
        direction: int,
        owner: Entity,
    ) -> None:
        super().__init__(width=width, height=height, color=color)
        self.center_x: float = x
        self.center_y: float = y
        self.direction: int = direction
        self.owner: Entity = owner

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
    texture_dict: Dict[str, List[List[arcade.Texture, arcade.Texture]]]
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
    walk_texture_index: int
        The current walk texture index which is displayed.
    x_odometer: float
        Measures how far the entity has travelled in the x direction.
    """

    def __init__(
        self,
        x: float,
        y: float,
        texture_dict: Dict[str, List[List[arcade.Texture]]],
        health: int,
    ) -> None:
        super().__init__(scale=SPRITE_SCALE)
        self.center_x: float = x
        self.center_y: float = y
        self.texture_dict: Dict[str, List[List[arcade.Texture]]] = texture_dict
        self.health: int = health
        self.texture: arcade.Texture = self.texture_dict["idle"][0][0]
        self.time_since_last_attack: float = 0
        self.facing: int = FACING_RIGHT
        self.walk_texture_index: int = 0
        self.x_odometer: float = 0

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
            direction = 1
        else:
            center_x -= 48
            direction = -1
        new_bullet = Bullet(
            center_x, self.center_y, 50, 10, arcade.color.RED, self.facing, self
        )
        physics: PhysicsEngine = self.physics_engines[0]
        physics.add_bullet(new_bullet)
        physics.set_velocity(new_bullet, (BULLET_VELOCITY * direction, 0))
        bullet_list.append(new_bullet)

    def deal_damage(self) -> None:
        """Deals damage to the entity."""
        self.health -= BULLET_DAMAGE

    def pymunk_moved(
        self, physics_engine: PhysicsEngine, dx: float, dy: float, d_angle: float
    ) -> None:
        """
        Called by the pymunk physics engine if this entity moves.

        Parameters
        ----------
        physics_engine: PhysicsEngine
            The pymunk physics engine which manages physics for this entity.
        dx: float
            The change in x. Positive means the entity is travelling right and negative
            means left.
        dy: float
            The change in y. Positive means the entity is travelling up and negative
            means down.
        d_angle: float
            The change in the angle. This shouldn't be used in this game.
        """
        # Figure out if we need to face left or right
        if dx < -DEAD_ZONE and self.facing == FACING_RIGHT:
            self.facing = FACING_LEFT
        if dx > DEAD_ZONE and self.facing == FACING_LEFT:
            self.facing = FACING_RIGHT

        # Add to the odometer how far we've moved
        self.x_odometer += dx

        # Idle animation
        if abs(dx) <= DEAD_ZONE:
            self.texture = self.texture_dict["idle"][0][self.facing]
            return

        # Jumping/falling animation
        if not physics_engine.is_on_ground(self):
            if dy > DEAD_ZONE:
                # Jumping animation
                self.texture = self.texture_dict["jump"][0][self.facing]
                return
            elif dy < -DEAD_ZONE:
                # Falling animation
                self.texture = self.texture_dict["fall"][0][self.facing]
                return

        # Walking animation
        if abs(self.x_odometer) > DISTANCE_TO_CHANGE_TEXTURE:
            # Reset the odometer
            self.x_odometer = 0

            # Advance the walking animation
            self.walk_texture_index += 1
            if self.walk_texture_index > 7:
                self.walk_texture_index = 0
            self.texture = self.texture_dict["walk"][self.walk_texture_index][
                self.facing
            ]
            return
