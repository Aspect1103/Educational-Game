from __future__ import annotations

# Pip
import arcade


class Game(arcade.View):
    """
    Manages the game and its actions.

    Parameters
    ----------
    level: int
        The level to initialise.
    """

    def __init__(self, level: int) -> None:
        super().__init__()
        print(level)
        arcade.exit()
