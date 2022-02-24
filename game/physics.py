from __future__ import annotations

# Custom
from typing import TYPE_CHECKING, List, Tuple

# Pip
import arcade

# Custom
from constants import FRICTION, MASS
from entities.player import ScoreAmount

if TYPE_CHECKING:
    from entities.enemy import Enemy
    from entities.entity import Bullet
    from entities.player import Player
    from views.game import Game


def player_coin_pickup_handler(player: Player, coin: arcade.Sprite, *_) -> bool:
    """
    Handles collision between a player sprite and a coin sprite as they touch. This uses
    the begin_handler which processes collision when two shapes are touching for the
    first time.

    Parameters
    ----------
    player: Player
        The player sprite.
    coin: arcade.Sprite
        The coin sprite that was hit.
    """
    # Delete the coin and update the player's score
    coin.remove_from_sprite_lists()
    player.update_score(ScoreAmount.COIN)  # noqa
    # Return False so pymunk will ignore processing the collision since we just want to
    # increase the score and remove the coin
    return False


def player_blocker_begin_handler(player: Player, wall: arcade.Sprite, *_) -> bool:
    """
    Handles collision between a player sprite and a blocker wall sprite as they touch.
    This uses the begin_handler which processes collision when two shapes are touching
    for the first time.

    Parameters
    ----------
    player: Player
        The player sprite.
    wall: arcade.Sprite
        The wall sprite that the player has touched.
    """
    # Get the sprite list containing the wall sprites
    blocker_list = wall.sprite_lists[0]
    # Get the current view
    game_view: Game = arcade.get_window().current_view  # noqa
    # Set the current_question attribute
    game_view.current_question = (True, blocker_list)
    # Return True so pymunk will process the collision and stop the player going through
    # the wall
    return True


def player_blocker_separate_handler(player: Player, wall: arcade.Sprite, *_) -> bool:
    """
    Handles collision between a player sprite and a blocker wall sprite after they have
    separated. This uses the separate_handler which processes collision after two shapes
    separate.

    Parameters
    ----------
    player: Player
        The player sprite.
    wall: arcade.Sprite
        The wall sprite that the player has separated from.
    """
    # Get the current view
    game_view: Game = arcade.get_window().current_view  # noqa
    # Set the current_question attribute
    game_view.current_question = (False, None)
    # Return True so pymunk will process the collision and stop the player going through
    # the wall
    return True


def player_bullet_begin_handler(player: Player, bullet: Bullet, *_) -> bool:
    """
    Handles collision between a player sprite and a bullet sprite as they touch. This
    uses the begin_handler which processes collision when two shapes are touching for
    the first time.

    Parameters
    ----------
    player: Player
        The player sprite.
    bullet: Bullet
        The bullet sprite which hit the player.
    """
    # Deal damage to the player
    player.deal_damage()
    # Remove the bullet
    bullet.remove_from_sprite_lists()
    # Return False so pymunk will ignore processing the collision since we just want to
    # decrease the player's health and remove the bullet
    return False


def enemy_bullet_begin_handler(enemy: Enemy, bullet: Bullet, *_) -> bool:
    """
    Handles collision between an enemy sprite and a bullet sprite as they touch. This
    uses the begin_handler which processes collision when two shapes are touching for
    the first time.

    Parameters
    ----------
    enemy: Enemy
        The enemy sprite.
    bullet: Bullet
        The bullet sprite which hit the enemy.
    """
    # Deal damage to the enemy
    enemy.deal_damage()
    # Remove the bullet
    bullet.remove_from_sprite_lists()
    # Return False so pymunk will ignore processing the collision since we just want to
    # decrease the enemy's health and remove the bullet
    return False


def bullet_wall_begin_handler(bullet: Bullet, wall: arcade.Sprite, *_) -> bool:
    """
    Handles collision between a bullet and a wall sprite as they touch. This uses the
    begin_handler which processes collision when two shapes are touching for the first
    time.

    Parameters
    ----------
    bullet: Bullet
        The bullet sprite which hit the wall.
    wall: arcade.Sprite
        The wall sprite which the bullet hit
    """
    # Remove the bullet
    try:
        bullet.remove_from_sprite_lists()
    except AttributeError:
        # An error randomly occurs when a collision is detected between a bullet and a
        # wall
        pass
    # Return False so pymunk will ignore processing the collision since we just want to
    # remove the bullet
    return False


def player_door_begin_handler(player: Player, door: arcade.Sprite, *_) -> bool:
    """
    Handles collision between the player and a door sprite as they touch. This uses the
    begin_handler which processes collision when two shapes are touching for the first
    time.

    Parameters
    ----------
    player: Player
        The player sprite.
    door: arcade.Sprite
        The door sprite that the player has touched.
    """
    # Get the current view
    game_view: Game = arcade.get_window().current_view  # noqa
    # Set the is_touching_door attribute
    game_view.is_touching_door = True
    # Return True so pymunk will process the collision and stop the player going through
    # the wall
    return False


def player_door_separate_handler(player: Player, door: arcade.Sprite, *_) -> bool:
    """
    Handles collision between a player sprite and a door wall sprite after they have
    separated. This uses the separate_handler which processes collision after two shapes
    separate.

    Parameters
    ----------
    player: Player
        The player sprite.
    door: arcade.Sprite
        The door sprite that the player has separated from.
    """
    # Get the current view
    game_view: Game = arcade.get_window().current_view  # noqa
    # Reset the is_touching_door attribute
    game_view.is_touching_door = False
    # Return True so pymunk will process the collision and stop the player going through
    # the wall
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
        door_list: arcade.SpriteList,
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
        door_list: arcade.SpriteList
            The sprite list for the door sprites.
        """
        # Add the player sprite to the physics engine
        self.add_sprite(
            player,
            mass=MASS,
            friction=FRICTION,
            moment_of_inertia=self.MOMENT_INF,
            collision_type="player",
        )

        # Add the wall sprites to the physics engine
        self.add_sprite_list(wall_list, body_type=self.STATIC, collision_type="wall")

        # Add the enemy sprites to the physics engine
        self.add_sprite_list(
            enemy_list,
            mass=MASS,
            friction=FRICTION,
            moment_of_intertia=self.MOMENT_INF,
            collision_type="enemy",
        )

        # Add the coin sprites to the physics engine
        self.add_sprite_list(
            coin_list,
            friction=FRICTION,
            body_type=self.KINEMATIC,
            collision_type="coin",
        )

        # Add the blocker sprites to the physics engine
        for blocker in blocker_list:
            self.add_sprite_list(
                blocker,
                body_type=self.STATIC,
                collision_type="blocker",
            )

        # Add the door sprites to the physics engine
        self.add_sprite_list(
            door_list,
            body_type=self.KINEMATIC,
            collision_type="door",
        )

        # Add collision handlers
        self.add_collision_handler(
            "player", "coin", begin_handler=player_coin_pickup_handler
        )
        self.add_collision_handler(
            "player", "blocker", begin_handler=player_blocker_begin_handler
        )
        self.add_collision_handler(
            "player", "blocker", separate_handler=player_blocker_separate_handler
        )
        self.add_collision_handler(
            "player", "bullet", begin_handler=player_bullet_begin_handler
        )
        self.add_collision_handler(
            "enemy", "bullet", begin_handler=enemy_bullet_begin_handler
        )
        self.add_collision_handler(
            "bullet", "wall", begin_handler=bullet_wall_begin_handler
        )
        self.add_collision_handler(
            "bullet", "blocker", begin_handler=bullet_wall_begin_handler
        )
        self.add_collision_handler(
            "player", "door", begin_handler=player_door_begin_handler
        )
        self.add_collision_handler(
            "player", "door", separate_handler=player_door_separate_handler
        )

    def __repr__(self) -> str:
        return (
            f"<PhysicsEngine (Gravity={self.gravity}) (Damping={self.damping}) (Sprite"
            f" count={len(self.sprites)})>"
        )

    def add_bullet(self, bullet: Bullet) -> None:
        """
        Adds a bullet to the physics engine.

        Parameters
        ----------
        bullet: Bullet
            The bullet to add to the physics engine.
        """
        self.add_sprite(
            bullet,
            moment_of_inertia=self.MOMENT_INF,
            body_type=self.KINEMATIC,
            collision_type="bullet",
        )
