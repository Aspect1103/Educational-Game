from __future__ import annotations

# Custom
from typing import TYPE_CHECKING, List, Tuple

# Pip
import arcade

# Custom
from constants import (
    FRICTION,
    PLAYER_MASS,
    PLAYER_MAX_HORIZONTAL_SPEED,
    PLAYER_MAX_VERTICAL_SPEED,
)
from entities.player import ScoreAmount

if TYPE_CHECKING:
    from entities.player import Player


def coin_hit_handler(player: Player, coin: arcade.Sprite, *_) -> bool:
    """
    Handles collision between a player sprite and a coin sprite. This uses the
    begin_handler which processes collision when two shapes are touching for the first
    time.

    Parameters
    ----------
    player: Player
        The player sprite.
    coin: arcade.Sprite
        The coin sprite that was hit.
    """
    coin.remove_from_sprite_lists()
    player.update_score(ScoreAmount.COIN)  # noqa
    # Return False so pymunk will ignore processing the collision since we just want to
    # increase the score and remove the coin
    return False


class PhysicsEngine(arcade.PymunkPhysicsEngine):
    """
    An abstracted version of the Pymunk Physics Engine which eases setting up a physics
    engine for a platformer.

    Parameters
    ----------
    gravity: Tuple[float, float]
        The direction where gravity is pointing.
    damping: float
        The amount of speed which is kept to the next tick. A value of 1.0 means no
        speed is lost, while 0.9 means 10% of speed is lost.
    """

    def __init__(self, gravity: Tuple[float, float], damping: float) -> None:
        super().__init__(gravity=gravity, damping=damping)
        self.gravity: Tuple[float, float] = gravity
        self.damping: float = damping

    def setup(
        self,
        player: arcade.Sprite,
        wall_list: arcade.SpriteList,
        enemy_list: arcade.SpriteList,
        coin_list: arcade.SpriteList,
        blocker_list: List[arcade.SpriteList],
    ) -> None:
        """
        Setups up the various sprites needed for the physics engine to work properly.

        Parameters
        ----------
        player: arcade.Sprite
            The player sprite.
        wall_list: arcade.SpriteList
            The sprite list for the wall sprites.
        enemy_list: arcade.SpriteList
            The sprite list for the enemy sprites
        coin_list: arcade.SpriteList
            The sprite list for the coin sprites.
        blocker_list: List[arcade.SpriteList]
            A list containing sprite lists for each blocker wall.
        """
        # Add the player sprite to the physics engine
        self.add_sprite(
            player,
            mass=PLAYER_MASS,
            friction=FRICTION,
            moment_of_inertia=self.MOMENT_INF,
            max_horizontal_velocity=PLAYER_MAX_HORIZONTAL_SPEED,
            max_vertical_velocity=PLAYER_MAX_VERTICAL_SPEED,
            collision_type="player",
        )

        # Add the wall sprites to the physics engine
        self.add_sprite_list(
            wall_list, friction=FRICTION, body_type=self.STATIC, collision_type="wall"
        )

        # Add the enemy sprites to the physics engine
        self.add_sprite_list(
            enemy_list,
            friction=FRICTION,
            moment_of_intertia=self.MOMENT_INF,
            collision_type="enemy",
        )

        # Add the coin sprites to the physics engine
        self.add_sprite_list(
            coin_list, friction=FRICTION, body_type=self.STATIC, collision_type="coin"
        )

        # Add the blocker sprites to the physics engine
        for blocker in blocker_list:
            self.add_sprite_list(
                blocker,
                friction=FRICTION,
                body_type=self.STATIC,
                collision_type="blocker",
            )

        # Add collision handlers
        self.add_collision_handler("player", "coin", begin_handler=coin_hit_handler)

    def __repr__(self) -> str:
        return (
            f"<PhysicsEngine (Gravity={self.gravity}) (Damping={self.damping}) (Sprite"
            f" count={len(self.sprites)})>"
        )
