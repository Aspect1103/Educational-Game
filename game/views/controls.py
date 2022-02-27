from __future__ import annotations

# Builtin
from typing import TYPE_CHECKING

# Pip
import arcade
import arcade.gui
from constants import BUTTON_STYLE

if TYPE_CHECKING:
    from views.start_menu import StartMenu
    from window import Window


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
        current_view: Controls = window.current_view  # noqa

        # Deactivate the UI manager so the buttons can't be clicked
        current_view.manager.disable()

        # Show the start menu view
        start_menu: StartMenu = window.views["StartMenu"]  # noqa
        window.show_view(start_menu)

        # Enable the start menu UI manager
        start_menu.manager.enable()


class Controls(arcade.View):
    """
    Creates a controls window showing the player the different keyboard and mouse
    controls.

    Attributes
    ----------
    manager: arcade.gui.UIManager
        Manages all the different UI elements.
    """

    def __init__(self) -> None:
        super().__init__()
        self.manager: arcade.gui.UIManager = arcade.gui.UIManager()
        vertical_box = arcade.gui.UIBoxLayout()

        # Display the keyboard controls
        controls = arcade.gui.UITextArea(
            text="""Keyboard controls:\n\nWASD - Movement.\nSpace - Jump\nE - Answer
question/activate door.\nLeft mouse button - Shoot.""",
            width=450,
            height=250,
            text_color=arcade.color.BLACK,
            font_size=24,
        )
        vertical_box.add(controls)

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
        return f"<Controls (Current window={self.window})>"

    def on_draw(self) -> None:
        """Render the screen."""
        # Clear the screen
        self.clear()

        # Draw the background
        arcade.set_background_color(arcade.color.ANDROID_GREEN)

        # Draw the UI elements
        self.manager.draw()
