from __future__ import annotations

# Pip
import arcade.gui


class Question(arcade.View):
    """"""

    def __init__(self) -> None:
        super().__init__()

    def __repr__(self) -> str:
        return f"<Question (Current window={self.window})>"

    def on_draw(self) -> None:
        """Render the screen."""
        # Clear the screen
        self.clear()
