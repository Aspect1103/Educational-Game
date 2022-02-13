from __future__ import annotations

# Pip
import arcade

# Custom
from levels.levels import levels


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
        self.tile_map: arcade.TileMap = levels[str(level)]
        self.scene: arcade.Scene = arcade.Scene.from_tilemap(self.tile_map)

        # Set the background color
        arcade.set_background_color(arcade.color.BABY_BLUE)

    def on_draw(self) -> None:
        """ "Render the screen."""
        # Clear the screen
        self.clear()

        # Draw the tilemap
        self.scene.draw()
