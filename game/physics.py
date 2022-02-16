from __future__ import annotations

# Pip
import arcade


class PhysicsEngine(arcade.PhysicsEnginePlatformer):
    """
    An abstracted version of the Platformer Physics Engine which eases setting up a
    physics engine for a platformer. I'll probably change this to Pymunk later on.

    Parameters
    ----------
    player: arcade.Sprite
        The player sprite.
    gravity: float
        The downward acceleration per frame.
    walls: arcade.SpriteList
        The sprite list for the wall sprites.
    """

    def __init__(
        self, player: arcade.Sprite, gravity: float, walls: arcade.SpriteList
    ) -> None:
        super().__init__(player_sprite=player, gravity_constant=gravity, walls=walls)

    def __repr__(self) -> str:
        return "<PhysicsEngine>"
