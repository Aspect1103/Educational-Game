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


class LevelScoreButton(arcade.gui.UIFlatButton):
    """A button which will show a level's top scores."""

    def __repr__(self) -> str:
        return (
            f"<LevelScoreButton (Position=({self.center_x}, {self.center_y}))"
            f" (Width={self.width}) (Height={self.height})>"
        )

    def on_click(self, _) -> None:
        """Called when the button is clicked."""
        # Get the current window and view
        window: Window = arcade.get_window()
        current_view: Scores = window.current_view  # noqa

        # Get the top 5 scores and set the score_text
        current_view.score_text.text = window.database.get_five_scores(int(self.text))


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
        current_view: Scores = window.current_view  # noqa

        # Deactivate the UI manager so the buttons can't be clicked
        current_view.manager.disable()

        # Show the start menu view
        start_menu: StartMenu = window.views["StartMenu"]  # noqa
        window.show_view(start_menu)

        # Enable the start menu UI manager
        start_menu.manager.enable()


class ResetButton(arcade.gui.UIFlatButton):
    """A button which will reset all the saved scores on the database."""

    def __repr__(self) -> str:
        return (
            f"<ResetButton (Position=({self.center_x}, {self.center_y}))"
            f" (Width={self.width}) (Height={self.height})>"
        )

    def on_click(self, _) -> None:
        """Called when the button is clicked."""
        # Get the current window and view
        window: Window = arcade.get_window()
        current_view: Scores = window.current_view  # noqa

        # Delete all the rows
        window.database.delete_all()

        # Reset score_text back to level 1
        current_view.score_text.text = window.database.get_five_scores(1)


class Scores(arcade.View):
    """
    Displays the top scores for each level.

    Attributes
    ----------
    manager: arcade.gui.UIManager
        Manages all the different UI elements.
    score_text: arcade.gui.UITextArea
        The text area which stores the scores for each level. This is stored as an
        instance variable, so it can be modified on each button click.
    """

    def __init__(self) -> None:
        super().__init__()
        self.manager: arcade.gui.UIManager = arcade.gui.UIManager()
        vertical_box = arcade.gui.UIBoxLayout()

        # Create the level buttons
        horizontal_level_box = arcade.gui.UIBoxLayout(vertical=False)
        for count in range(10):
            new_score = LevelScoreButton(
                text=str(count + 1), width=50, style=BUTTON_STYLE
            )
            horizontal_level_box.add(new_score.with_space_around(right=10))
        vertical_box.add(horizontal_level_box.with_space_around(bottom=20))

        # Create the score text
        self.score_text: arcade.gui.UITextArea = arcade.gui.UITextArea(
            text=self.window.database.get_five_scores(1),
            width=775,
            height=450,
            text_color=arcade.color.BLACK,
            font_size=24,
        )
        vertical_box.add(self.score_text.with_space_around(bottom=20))

        # Create the button layout
        horizontal_button_box = arcade.gui.UIBoxLayout(vertical=False)
        back_button = BackButton(text="Back", width=205, style=BUTTON_STYLE)
        horizontal_button_box.add(back_button.with_space_around(right=20))
        reset_button = ResetButton(text="Reset", width=205, style=BUTTON_STYLE)
        horizontal_button_box.add(reset_button)
        vertical_box.add(horizontal_button_box)

        # Register the UI elements
        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center", anchor_y="center", child=vertical_box
            )
        )

    def __repr__(self) -> str:
        return f"<Scores (Current window={self.window})>"

    def on_draw(self) -> None:
        """Render the screen."""
        # Clear the screen
        self.clear()

        # Draw the background
        arcade.set_background_color(arcade.color.BABY_BLUE)

        # Draw the UI elements
        self.manager.draw()
