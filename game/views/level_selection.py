from __future__ import annotations

# Builtin
from typing import TYPE_CHECKING

# Pip
import arcade
import arcade.gui
from constants import BUTTON_STYLE

# Custom
from textures.textures import non_moving_textures
from views.game import Game

if TYPE_CHECKING:
    from views.start_menu import StartMenu
    from window import Window


class LevelButton(arcade.gui.UIFlatButton):
    """A button which will play a specific game level."""

    def __repr__(self) -> str:
        return (
            f"<LevelButton (Position=({self.center_x}, {self.center_y}))"
            f" (Width={self.width}) (Height={self.height})>"
        )

    def on_click(self, _) -> None:
        """Called when the button is clicked."""
        # Get the current window and view
        window: Window = arcade.get_window()
        current_view: LevelSelection = window.current_view  # noqa

        # Deactivate the UI manager so the buttons can't be clicked
        current_view.manager.disable()

        # Create the new game view
        game_view = Game()
        game_view.setup(int(self.text))
        window.views["Game"] = game_view

        # Show the game view
        window.show_view(game_view)


class BackButton(arcade.gui.UIFlatButton):
    """A button which will switch back to the start menu view."""

    def __repr__(self) -> str:
        return (
            f"<BackButton (Position=({self.center_x}, {self.center_y}))"
            f" (Width={self.width}) (Height={self.height})>"
        )

    def on_click(self, _) -> None:
        """Called when the button is clicked."""
        # Get the current window and view
        window: Window = arcade.get_window()
        current_view: LevelSelection = window.current_view  # noqa

        # Deactivate the UI manager so the buttons can't be clicked
        current_view.manager.disable()

        # Show the start menu view
        start_menu: StartMenu = window.views["StartMenu"]  # noqa
        window.show_view(start_menu)

        # Enable the start menu UI manager
        start_menu.manager.enable()


class LevelSelection(arcade.View):
    """
    Creates a level selection menu allowing the player to pick a specific level.

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

        # Create the first row of levels
        first_horizontal_box = arcade.gui.UIBoxLayout(vertical=False)
        for count in range(5):
            new_level = LevelButton(text=str(count + 1), width=50, style=BUTTON_STYLE)
            first_horizontal_box.add(new_level.with_space_around(right=20))

        # Create the second row of levels
        second_horizontal_box = arcade.gui.UIBoxLayout(vertical=False)
        for count in range(5, 10):
            new_level = LevelButton(text=str(count + 1), width=50, style=BUTTON_STYLE)
            second_horizontal_box.add(new_level.with_space_around(right=20))

        # Add rows to the vertical box
        vertical_box.add(first_horizontal_box.with_space_around(bottom=20))
        vertical_box.add(second_horizontal_box.with_space_around(bottom=20))

        # Create the back button
        back_button = BackButton(text="Back", width=205, style=BUTTON_STYLE)
        vertical_box.add(back_button.with_space_around(top=20))

        # Register the UI elements
        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center", anchor_y="center", child=vertical_box
            )
        )

    def __repr__(self) -> str:
        return f"<LevelSelection (Current window={self.window})>"

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
