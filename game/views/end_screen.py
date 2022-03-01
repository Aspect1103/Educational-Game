from __future__ import annotations

# Builtin
import time
from typing import TYPE_CHECKING

# Pip
import arcade.gui

# Custom
from constants import BUTTON_STYLE

if TYPE_CHECKING:
    from views.game import Game
    from window import Window


class QuitButton(arcade.gui.UIFlatButton):
    """A button which will quit the game."""

    def __repr__(self) -> str:
        return (
            f"<QuitButton (Position=({self.center_x}, {self.center_y}))"
            f" (Width={self.width}) (Height={self.height})>"
        )

    def on_click(self, _) -> None:
        """Called when the button is clicked."""
        # Quit the game
        arcade.exit()


class EndScreen(arcade.View):
    """
    Creates an end screen displaying the level result, the player score and the time to
    complete as well as a button to exit the game.

    Attributes
    ----------
    manager: arcade.gui.UIManager
        Manages all the different UI elements.
    start_time: float
        The time in seconds when the game started.
    result_text: arcade.gui.UILabel
        Displays the result of the game. This is stored as an instance variable, so it
        can be modified when the game is finished.
    score_text: arcade.gui.UILabel
        Displays the user score. This is stored as an instance variable, so it can be
        modified when the game is finished.
    """

    def __init__(self) -> None:
        super().__init__()
        self.manager: arcade.gui.UIManager = arcade.gui.UIManager()
        self.start_time: float = time.time()
        vertical_box = arcade.gui.UIBoxLayout()

        # Create the result text
        self.result_text: arcade.gui.UILabel = arcade.gui.UILabel(
            text="Result",
            width=500,
            height=100,
            text_color=arcade.color.BLACK,
            font_size=24,
            align="center",
        )
        vertical_box.add(self.result_text.with_space_around(bottom=20))

        # Create the score text
        self.score_text: arcade.gui.UILabel = arcade.gui.UILabel(
            text="Score: 0",
            width=500,
            height=100,
            text_color=arcade.color.BLACK,
            font_size=24,
            align="center",
        )
        vertical_box.add(self.score_text.with_space_around(bottom=20))

        # Create the time to complete text
        self.time_to_complete: arcade.gui.UILabel = arcade.gui.UILabel(
            text="Time to complete: 0 minutes",
            width=1000,
            height=100,
            text_color=arcade.color.BLACK,
            font_size=24,
            align="center",
        )
        vertical_box.add(self.time_to_complete.with_space_around(bottom=20))

        # Create the quit button
        quit_button = QuitButton(text="Quit Game", width=200, style=BUTTON_STYLE)
        vertical_box.add(quit_button)

        # Register the UI elements
        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center", anchor_y="center", child=vertical_box
            )
        )

    def __repr__(self) -> str:
        return f"<EndScreen (Current window={self.window})>"

    def on_draw(self) -> None:
        """Render the screen."""
        # Clear the screen
        self.clear()

        # Draw the background
        arcade.set_background_color(arcade.color.CADMIUM_ORANGE)

        # Draw the UI elements
        self.manager.draw()

    def on_show(self) -> None:
        """Called when the view loads."""
        # Get the game view
        game: Game = self.window.views["Game"]

        # Update the result text
        self.result_text.text = "You Win" if game.level_won else "Game Over"

        # Update the score text
        self.score_text.text = f"Score: {game.player.score}"

        # Update the time to complete text
        total = time.time() - self.start_time
        self.time_to_complete.text = (
            f"Time to complete: {int(total / 60)} minutes and {int(total % 60)} seconds"
        )

        # Play the end screen music
        window: Window = self.window
        if window.current_sound is not None:
            window.current_sound.stop(window.player)
        window.current_sound = window.sounds["end screen"]
        window.player = window.current_sound.play(loop=True)

        # Enable the UI manager
        self.manager.enable()
