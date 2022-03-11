from __future__ import annotations

# Builtin
from typing import TYPE_CHECKING, Dict

# Pip
import arcade.gui

# Custom
from constants import BLOCKER_WALL_HEALTH_LOSS, BUTTON_STYLE
from entities.player import ScoreAmount

if TYPE_CHECKING:
    from views.game import Game
    from window import Window


class InputButton(arcade.gui.UIFlatButton):
    """A button which will submit one of four answers when pressed."""

    def __repr__(self) -> str:
        return (
            f"<InputButton (Position=({self.center_x}, {self.center_y}))"
            f" (Width={self.width}) (Height={self.height})>"
        )

    def on_click(self, _) -> None:
        """Called when the button is clicked."""
        # Get the current view and the game view
        window: Window = arcade.get_window()
        current_view: Question = window.current_view  # noqa
        game_view: Game = window.views["Game"]  # noqa

        # Test if the user has already submitted an answer
        if current_view.submitted:
            return

        # Test if the answer is correct
        if self.text == current_view.question["correct"]:
            # Disable the blocker wall
            game_view.disable_blocker_wall()

            # Display congrats
            current_view.question_text.text = (
                f"{current_view.question_text.text}\n\nCorrect. You can now return to"
                " the game using the exit button and continue."
            )

            # Add points to the user
            game_view.player.update_score(ScoreAmount.QUESTION_CORRECT)
        else:
            # Display the correct answer
            current_view.question_text.text = (
                f"{current_view.question_text.text}\n\nIncorrect, return to the game"
                " and try again. Explanation:"
                f" {current_view.question['explanation']}"
            )

            # Remove points from the user
            game_view.player.update_score(ScoreAmount.QUESTION_WRONG)

            # Remove health from the user
            game_view.player.health -= BLOCKER_WALL_HEALTH_LOSS

        # Reveal the exit button
        current_view.vertical_box.add(
            current_view.exit_button.with_space_around(top=20)
        )

        # Set submitted so the user can't submit again
        current_view.submitted = True


class ExitButton(arcade.gui.UIFlatButton):
    """A button which will return to the game view without removing the blocker wall."""

    def __repr__(self) -> str:
        return (
            f"<ExitButton (Position=({self.center_x}, {self.center_y}))"
            f" (Width={self.width}) (Height={self.height})>"
        )

    def on_click(self, _) -> None:
        """Called when the button is clicked."""
        # Switch back to the game view
        window: Window = arcade.get_window()
        current_view: Question = window.current_view  # noqa
        game_view: Game = window.views["Game"]  # noqa
        current_view.manager.disable()
        window.show_view(game_view)


class Question(arcade.View):
    """
    Creates a question window displaying a maths question, an input field for the user
    answer and a submit button for testing if the answer is correct.

    Parameters
    ----------
    question: Dict[str, str]
        The question to display to the user with a correct answer and explanation.

    Attributes
    ----------
    submitted: bool
        Whether or not the user has already submitted an answer.
    manager: arcade.gui.UIManager
        Manages all the different UI elements.
    question_text: arcade.gui.UITextArea
        Displays the question to the user for them to answer. This is stored as an
        instance variable, so we can change its text if the user gets the question
        wrong.
    exit_button: ExitButton
        A button which will return to the main game when pressed. This will only be
        enabled once the user submits their answer.
    vertical_box: arcade.gui.UIBoxLayout
        The vertical box layout used for aligning the different UI elements. This is
        stored as an instance variable, so we can add the exit button to it once the
        user submits their answer.
    """

    def __init__(self, question: Dict[str, str]) -> None:
        super().__init__()
        self.question: Dict[str, str] = question
        self.submitted: bool = False
        self.manager: arcade.gui.UIManager = arcade.gui.UIManager()
        self.vertical_box: arcade.gui.UIBoxLayout = arcade.gui.UIBoxLayout()

        # Create the question text
        self.question_text: arcade.gui.UITextArea = arcade.gui.UITextArea(
            text=self.question["question"],
            width=750,
            height=375,
            text_color=arcade.color.BLACK,
            font_size=24,
        )
        self.vertical_box.add(self.question_text)

        # Create the input hint
        input_label = arcade.gui.UILabel(
            text="Type your answer below:",
            width=350,
            height=40,
            text_color=arcade.color.BLACK,
            font_size=24,
        )
        self.vertical_box.add(input_label)

        # Create the answers
        horizontal_box = arcade.gui.UIBoxLayout(vertical=False)
        for answer in self.question["answers"]:
            input_box = InputButton(text=answer, width=150, style=BUTTON_STYLE)
            horizontal_box.add(input_box.with_space_around(right=20))
        self.vertical_box.add(horizontal_box.with_space_around(bottom=20))

        # Create an exit button (this is hidden until the user gets the question wrong)
        self.exit_button: ExitButton = ExitButton(
            text="Exit", width=205, style=BUTTON_STYLE
        )

        # Register the UI elements
        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center", anchor_y="center", child=self.vertical_box
            )
        )

    def __repr__(self) -> str:
        return f"<Question (Current window={self.window})>"

    def on_draw(self) -> None:
        """Render the screen."""
        # Clear the screen
        self.clear()

        # Draw the background
        arcade.set_background_color(arcade.color.LIGHT_PASTEL_PURPLE)

        # Draw the UI elements
        self.manager.draw()
