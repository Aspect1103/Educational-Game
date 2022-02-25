from __future__ import annotations

# Builtin
from typing import TYPE_CHECKING

# Pip
import arcade
import arcade.gui
from constants import BUTTON_STYLE

# Custom
from textures.textures import non_moving_textures
from views.level_selection import LevelSelection

if TYPE_CHECKING:
    from window import Window


class StartButton(arcade.gui.UIFlatButton):
    """A button which will switch to the game selection view."""

    def __repr__(self) -> str:
        return (
            f"<StartButton (Position=({self.center_x}, {self.center_y}))"
            f" (Width={self.width}) (Height={self.height})>"
        )

    def on_click(self, _) -> None:
        """Called when the button is clicked."""
        # Get the current window and view
        window: Window = arcade.get_window()
        current_view: StartMenu = window.current_view  # noqa

        # Deactivate the UI manager so the buttons can't be clicked
        current_view.manager.disable()

        # Show the level selection view
        level_selection: LevelSelection = window.views["LevelSelection"]  # noqa
        window.show_view(level_selection)

        # Enable the level selection UI manager
        level_selection.manager.enable()


class QuitButton(arcade.gui.UIFlatButton):
    """A button which when clicked will quit the game."""

    def __repr__(self) -> str:
        return (
            f"<QuitButton (Position=({self.center_x}, {self.center_y}))"
            f" (Width={self.width}) (Height={self.height})>"
        )

    def on_click(self, _) -> None:
        """Called when the button is clicked."""
        arcade.exit()


class StartMenu(arcade.View):
    """
    Creates a start menu allowing the player to pick an option.

    Attributes
    ----------
    manager: arcade.gui.UIManager
        Manages all the different UI elements.
    background: arcade.Texture
        Stores the image background.
    """

    def __init__(self) -> None:
        super().__init__()
        self.manager: arcade.gui.UIManager = arcade.gui.UIManager()
        vertical_box = arcade.gui.UIBoxLayout()

        # Create background
        self.background: arcade.Texture = non_moving_textures["background"][0]

        # Set up the level selection view
        level_selection_view = LevelSelection()
        self.window.views["LevelSelection"] = level_selection_view

        # Create the start button
        start_button = StartButton(text="Start Game", width=205, style=BUTTON_STYLE)
        vertical_box.add(start_button.with_space_around(bottom=20))

        # Create the quit button
        quit_button = QuitButton(text="Quit", width=205, style=BUTTON_STYLE)
        vertical_box.add(quit_button.with_space_around(bottom=20))

        # Register the UI elements
        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center", anchor_y="center", child=vertical_box
            )
        )

    def __repr__(self) -> str:
        return f"<StartMenu (Current window={self.window})>"

    def on_draw(self) -> None:
        """Render the screen."""
        # Clear the screen
        self.clear()

        # Draw the background image
        arcade.draw_lrwh_rectangle_textured(
            0, 0, self.window.width, self.window.height, self.background
        )

        # Draw the UI elements
        self.manager.draw()
