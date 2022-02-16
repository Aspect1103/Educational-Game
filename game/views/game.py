from __future__ import annotations

# Builtin
from typing import Optional

# Pip
import arcade
from constants import DAMPING, GRAVITY, PLAYER_JUMP_IMPULSE, PLAYER_MOVE_FORCE

# Custom
from levels.levels import levels
from physics import PhysicsEngine


class Game(arcade.View):
    """
    Manages the game and its actions.

    Attributes
    ----------
    tile_map: Optional[arcade.TileMap]
        The tiled tilemap which represents the current level.
    player: Optional[arcade.Sprite]
        The sprite for the playable character in the game.
    wall_list: arcade.SpriteList
        The sprite list for the floor and crate sprites.
    coin_list: arcade.SpriteList
        The sprite list for the coin sprites.
    enemy_list: arcade.SpriteList
        The sprite list for the enemies.
    blocker_list: arcade.SpriteList
        The sprite list for the walls blocking progression.
    bullet_list: arcade.SpriteList
        The sprite list for the bullets.
    physics_engine: Optional[PhysicsEngine]
        The physics engine which processes collision and gravity.
    camera: Optional[arcade.Camera]
        The camera used for moving the viewport around the screen.
    left_pressed: bool
        Whether the left key is pressed or not.
    right_pressed: bool
        Whether the right key is pressed or not.
    """

    def __init__(self) -> None:
        super().__init__()
        self.tile_map: Optional[arcade.TileMap] = None
        self.player: Optional[arcade.Sprite] = None
        self.wall_list: arcade.SpriteList = arcade.SpriteList(use_spatial_hash=True)
        self.coin_list: arcade.SpriteList = arcade.SpriteList(use_spatial_hash=True)
        self.enemy_list: arcade.SpriteList = arcade.SpriteList(use_spatial_hash=True)
        self.blocker_list: arcade.SpriteList = arcade.SpriteList(use_spatial_hash=True)
        self.bullet_list: arcade.SpriteList = arcade.SpriteList(use_spatial_hash=True)
        self.physics_engine: Optional[PhysicsEngine] = None
        self.camera: Optional[arcade.Camera] = None
        self.left_pressed: bool = False
        self.right_pressed: bool = False

    def __repr__(self) -> str:
        return f"<Game (Current window={self.window})>"

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
        self.player = self.tile_map.sprite_lists["Player"][0]

        # Make sure the player object is assigned to
        assert self.player is not None

        # Set up the physics engine
        self.physics_engine = PhysicsEngine(GRAVITY, DAMPING)
        self.physics_engine.setup(
            self.player,
            self.wall_list,
            self.enemy_list,
            self.coin_list,
            self.blocker_list,
        )

        # Set up the Camera
        self.camera = arcade.Camera(self.window.width, self.window.height)

        # Set the background color
        arcade.set_background_color(arcade.color.BABY_BLUE)

    def on_draw(self) -> None:
        """Render the screen."""
        # Make sure variables needed are valid
        assert self.player is not None
        assert self.camera is not None

        # Clear the screen
        self.clear()

        # Activate our Camera
        self.camera.use()

        # Draw the sprite lists and the player
        self.wall_list.draw()
        self.coin_list.draw()
        self.enemy_list.draw()
        self.blocker_list.draw()
        self.player.draw()

    def on_update(self, delta_time: float) -> None:
        """
        Processes movement and game logic.

        Parameters
        ----------
        delta_time: float
            Time interval since the last time the function was called.
        """
        # Make sure variables needed are valid
        assert self.physics_engine is not None
        assert self.player is not None

        # Calculate the speed and direction of the player based on the keys pressed
        if self.left_pressed and not self.right_pressed:
            self.physics_engine.apply_force(self.player, (-PLAYER_MOVE_FORCE, 0))
            self.physics_engine.set_friction(self.player, 0)
        elif self.right_pressed and not self.left_pressed:
            self.physics_engine.apply_force(self.player, (PLAYER_MOVE_FORCE, 0))
            self.physics_engine.set_friction(self.player, 0)

        # Update the physics engine
        self.physics_engine.step()

        # Position the camera
        self.center_camera_on_player()

    def on_key_press(self, key: int, modifiers: int) -> None:
        """
        Called when the player presses a key.

        Parameters
        ----------
        key: int
            The key that was hit.
        modifiers: int
            Bitwise AND of all modifiers (shift, ctrl, num lock) pressed during this
            event.
        """
        # Make sure variables needed are valid
        assert self.player is not None
        assert self.physics_engine is not None

        if key is arcade.key.A:
            self.left_pressed = True
        elif key is arcade.key.D:
            self.right_pressed = True
        elif key is arcade.key.SPACE and self.physics_engine.is_on_ground(self.player):
            self.physics_engine.apply_impulse(self.player, (0, PLAYER_JUMP_IMPULSE))

    def on_key_release(self, key: int, modifiers: int) -> None:
        """
        Called when the player releases a key.

        Parameters
        ----------
        key: int
            The key that was hit.
        modifiers: int
            Bitwise AND of all modifiers (shift, ctrl, num lock) pressed during this
            event.
        """
        if key is arcade.key.A:
            self.left_pressed = False
        elif key is arcade.key.D:
            self.right_pressed = False

    def center_camera_on_player(self) -> None:
        """Centers the camera on the player."""
        # Make sure variables needed are valid
        assert self.camera is not None
        assert self.player is not None

        # Calculate the screen position centered on the player
        screen_center_x = self.player.center_x - (self.camera.viewport_width / 2)
        screen_center_y = self.player.center_y - (self.camera.viewport_height / 2)

        # Don't let the camera travel past 0
        if screen_center_x < 0:
            screen_center_x = 0
        if screen_center_y < 0:
            screen_center_y = 0

        # Move the camera to the new position
        self.camera.move_to((screen_center_x, screen_center_y))  # noqa
