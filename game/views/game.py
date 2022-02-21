from __future__ import annotations

# Builtin
from typing import TYPE_CHECKING, List, Optional, Tuple

# Pip
import arcade

# Custom
from constants import (
    ATTACK_COOLDOWN,
    DAMPING,
    FACING_LEFT,
    FACING_RIGHT,
    GRAVITY,
    PLAYER_JUMP_FORCE,
    PLAYER_MOVE_FORCE,
)
from entities.enemy import Enemy
from entities.player import Player
from levels.levels import levels
from physics import PhysicsEngine
from textures.textures import textures
from views.question import Question

if TYPE_CHECKING:
    from levels.levels import GameLevel


class Game(arcade.View):
    """
    Manages the game and its actions.

    Attributes
    ----------
    level_data: Optional[GameLevel]
        The LevelInstance namedtuple which holds the data for this level.
    player: Optional[Player]
        The sprite for the playable character in the game.
    wall_list: Optional[arcade.SpriteList]
        The sprite list for the floor and crate sprites.
    coin_list: Optional[arcade.SpriteList]
        The sprite list for the coin sprites.#
    blocker_list: List[arcade.SpriteList]
        A list containing sprite lists for each of the walls blocking progression.
    enemy_list: arcade.SpriteList
        The sprite list for the enemies.
    bullet_list: arcade.SpriteList
        The sprite list for the bullets.
    physics_engine: Optional[PhysicsEngine]
        The physics engine which processes collision and gravity.
    camera: Optional[arcade.Camera]
        The camera used for moving the viewport around the screen.
    gui_camera: Optional[arcade.Camera]
        The camera used for visualising the GUI elements.
    score_text: arcade.Text
        The text object used for displaying the score.
    left_pressed: bool
        Whether the left key is pressed or not.
    right_pressed: bool
        Whether the right key is pressed or not.
    current_question: Tuple[bool, Optional[arcade.SpriteList]]
        The current question which the user can answer.
    """

    def __init__(self) -> None:
        super().__init__()
        self.level_data: Optional[GameLevel] = None
        self.player: Optional[Player] = None
        self.wall_list: Optional[arcade.SpriteList] = None
        self.coin_list: Optional[arcade.SpriteList] = None
        self.blocker_list: List[arcade.SpriteList] = []
        self.enemy_list: arcade.SpriteList = arcade.SpriteList(use_spatial_hash=True)
        self.bullet_list: arcade.SpriteList = arcade.SpriteList(use_spatial_hash=True)
        self.physics_engine: Optional[PhysicsEngine] = None
        self.camera: Optional[arcade.Camera] = None
        self.gui_camera: Optional[arcade.Camera] = None
        self.score_text: arcade.Text = arcade.Text(
            "Score: 0",
            10,
            10,
            arcade.color.BLACK,
            20,
        )
        self.left_pressed: bool = False
        self.right_pressed: bool = False
        self.current_question: Tuple[bool, Optional[arcade.SpriteList]] = (False, None)

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
            self.level_data = levels[str(level)]
        except KeyError:
            arcade.exit()
            raise KeyError(f"No map available for level {level}")

        # Load the floor and coin tilemap layer into its own sprite list
        tile_map = self.level_data.tilemap
        self.wall_list = tile_map.sprite_lists["Platforms"]
        self.coin_list = tile_map.sprite_lists["Coins"]

        # Create the player object
        player_obj = tile_map.sprite_lists["Player"][0]
        self.player = Player(
            player_obj.center_x, player_obj.center_y, textures["player"][0]
        )

        # Create the enemies
        for enemy in tile_map.sprite_lists["Enemies"]:
            self.enemy_list.append(
                Enemy(enemy.center_x, enemy.center_y, textures["enemy"][0])
            )

        # Create the blocker list
        for blocker_count in range(self.level_data.blocker_count):
            blocker = tile_map.sprite_lists[f"Walls{blocker_count+1}"]
            blocker.enable_spatial_hashing()
            self.blocker_list.append(blocker)

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
        self.gui_camera = arcade.Camera(self.window.width, self.window.height)

    def on_show(self) -> None:
        """Run setup logic when the view loads."""
        # Set the background color
        arcade.set_background_color(arcade.color.BABY_BLUE)

    def on_draw(self) -> None:
        """Render the screen."""
        # Make sure variables needed are valid
        assert self.player is not None
        assert self.camera is not None
        assert self.gui_camera is not None
        assert self.score_text is not None
        assert self.wall_list is not None
        assert self.coin_list is not None

        # Clear the screen
        self.clear()

        # Activate our sprite camera
        self.camera.use()

        # Draw the sprite lists and the player
        self.wall_list.draw()
        self.coin_list.draw()
        self.enemy_list.draw()
        self.bullet_list.draw()
        self.player.draw()
        for blocker in self.blocker_list:
            blocker.draw()

        # Draw the score on the screen
        self.gui_camera.use()
        self.score_text.value = f"Score: {self.player.score}"
        self.score_text.draw()

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

        # Update the player's time since last attack
        self.player.time_since_last_attack += delta_time

        # Calculate the speed and direction of the player based on the keys pressed
        if self.left_pressed and not self.right_pressed:
            self.player.facing = FACING_LEFT
            self.physics_engine.apply_force(self.player, (-PLAYER_MOVE_FORCE, 0))
            # Set the friction to 0 so the player doesn't stop suddenly
            self.physics_engine.set_friction(self.player, 0)
        elif self.right_pressed and not self.left_pressed:
            self.player.facing = FACING_RIGHT
            self.physics_engine.apply_force(self.player, (PLAYER_MOVE_FORCE, 0))
            # Set the friction to 0 so the player doesn't stop suddenly
            self.physics_engine.set_friction(self.player, 0)
        else:
            # The player is not moving so increase the friction making the player stop
            self.physics_engine.set_friction(self.player, 1)

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
        assert self.level_data is not None

        if key is arcade.key.A:
            self.left_pressed = True
        elif key is arcade.key.D:
            self.right_pressed = True
        elif key is arcade.key.SPACE and self.physics_engine.is_on_ground(self.player):
            self.physics_engine.apply_force(self.player, (0, PLAYER_JUMP_FORCE))
        elif (
            key is arcade.key.E
            and self.physics_engine.is_on_ground(self.player)
            and self.current_question[0]
        ):
            # Set right_pressed to False to stop the player moving after the question
            self.right_pressed = False

            # Initialise the question view
            question_view = Question(self.level_data.questions[0])
            self.window.views["Question"] = question_view

            # Enable the question UI manager
            question_view.manager.enable()

            # Show the question view
            self.window.show_view(question_view)

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

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int) -> None:
        """
        Called when the player presses the mouse button.

        Parameters
        ----------
        x: float
            The x position of the mouse.
        y: float
            The y position of the mouse.
        button: int
            Which button was hit.
        modifiers: int
            Bitwise AND of all modifiers (shift, ctrl, num lock) pressed during this
            event.
        """
        # Make sure variables needed are valid
        assert self.player is not None

        if (
            button is arcade.MOUSE_BUTTON_LEFT
            and self.player.time_since_last_attack >= ATTACK_COOLDOWN
        ):
            self.player.ranged_attack(self.bullet_list)

    def center_camera_on_player(self) -> None:
        """Centers the camera on the player."""
        # Make sure variables needed are valid
        assert self.camera is not None
        assert self.player is not None

        # Calculate the screen position centered on the player
        screen_center_x = self.player.center_x - (self.window.width / 2)
        screen_center_y = self.player.center_y - (self.window.height / 2)

        # Don't let the camera travel past 0
        if screen_center_x < 0:
            screen_center_x = 0
        if screen_center_y < 0:
            screen_center_y = 0

        # Move the camera to the new position
        self.camera.move_to((screen_center_x, screen_center_y))  # noqa

    def disable_blocker_wall(self) -> None:
        """Disables the current blocker wall stored."""
        # Make sure variables needed are valid
        assert self.physics_engine is not None

        # Remove the stored blocker wall
        blocker_wall: arcade.SpriteList = self.current_question[1]
        blocker_wall.visible = False
        for sprite in blocker_wall:
            self.physics_engine.remove_sprite(sprite)
        self.current_question = (False, None)
