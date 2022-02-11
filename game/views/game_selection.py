from __future__ import annotations

# Pip
import arcade
import arcade.gui

# Custom
from textures.textures import textures


class GameSelection(arcade.View):
    """Creates a game selection menu allowing the player to pick a specific game."""

    def __init__(self) -> None:
        super().__init__()
        self.manager: arcade.gui.UIManager = arcade.gui.UIManager()
        self.vertical_box: arcade.gui.UIBoxLayout = arcade.gui.UIBoxLayout()

        # Create background
        self.background: arcade.Texture = textures["background"][0]

        # # Create the quit button
        # quit_button = QuitButton(text="Quit Game", width=200)
        # self.vertical_box.add(quit_button.with_space_around(bottom=20))
        #
        # # Register the UI elements
        # self.manager.add(
        #     arcade.gui.UIAnchorWidget(
        #         anchor_x="center_x", anchor_y="center_y", child=self.vertical_box
        #     )
        # )

        # Enable the UI elements
        self.manager.enable()

    def __repr__(self) -> str:
        return f"<GameSelection (Current window={self.window})>"

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
