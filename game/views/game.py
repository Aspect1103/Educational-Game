from __future__ import annotations

# Builtin
from typing import Optional

# Pip
import arcade

# Custom
from levels.levels import levels


class Game(arcade.View):
    """
    Manages the game and its actions.

    Attributes
    ----------
    tile_map: Optional[arcade.TileMap]
        The tiled tilemap which represents the current level.
    wall_list: arcade.SpriteList
        The sprite list for the floor and crate sprites.
    coin_list: arcade.SpriteList
        The sprite list for the coin sprites.
    enemy_list: arcade.SpriteList
        The sprite list for the enemies.
    blocker_list: arcade.SpriteList
        The sprite list for the walls blocking progression.
    player_list: arcade.SpriteList
        The sprite list for the player.
    """

    def __init__(self) -> None:
        super().__init__()
        self.tile_map: Optional[arcade.TileMap] = None
        self.wall_list: arcade.SpriteList = arcade.SpriteList(use_spatial_hash=True)
        self.coin_list: arcade.SpriteList = arcade.SpriteList(use_spatial_hash=True)
        self.enemy_list: arcade.SpriteList = arcade.SpriteList(use_spatial_hash=True)
        self.blocker_list: arcade.SpriteList = arcade.SpriteList(use_spatial_hash=True)
        self.player_list: arcade.SpriteList = arcade.SpriteList(use_spatial_hash=True)

    def setup(self, level: int) -> None:
        """
        Sets up the game based on a specific level.

        Parameters
        ----------
        level: int
            The level to load.
        """
        # Load the tilemap
        try:
            self.tile_map = levels[str(level)]
        except KeyError:
            arcade.exit()
            raise KeyError(f"No map available for level {level}")

        # Load each tilemap layer into its own sprite list
        self.wall_list = self.tile_map.sprite_lists["Platforms"]
        self.coin_list = self.tile_map.sprite_lists["Coins"]
        self.enemy_list = self.tile_map.sprite_lists["Enemies"]
        self.blocker_list = self.tile_map.sprite_lists["Walls"]
        self.player_list = self.tile_map.sprite_lists["Player"]

        # Set the background color
        arcade.set_background_color(arcade.color.BABY_BLUE)

    def on_draw(self) -> None:
        """Render the screen."""
        # Clear the screen
        self.clear()

        # Draw the sprite lists and player
        self.wall_list.draw()
        self.coin_list.draw()
        self.enemy_list.draw()
        self.blocker_list.draw()
        self.player_list.draw()
