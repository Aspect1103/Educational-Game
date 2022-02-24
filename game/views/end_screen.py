from __future__ import annotations

# Builtin
import time

# Pip
import arcade.gui


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
    end_time: float
        The time in seconds when the game ended.
    """

    def __init__(self) -> None:
        super().__init__()
        self.manager: arcade.gui.UIManager = arcade.gui.UIManager()
        self.start_time: float = time.time()
        self.end_time: float = -1
        vertical_box: arcade.gui.UIBoxLayout = arcade.gui.UIBoxLayout()

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
        """Run setup logic when the view loads."""
        # Set end_time since the game has finished
        self.end_time = time.time()
