from __future__ import annotations

# Builtin
from typing import Dict

# Pip
import arcade

# Custom
from views.start_menu import StartMenu


class Window(arcade.Window):
    """
    Manages the window and allows switching between views.

    Parameters
    ----------
    title: str
        The title of the window.

    Attributes
    ----------
    views: Dict[str, arcade.View]
        Holds all the views used by the game.
    """

    def __init__(self, title: str) -> None:
        super().__init__(title=title)
        self.views: Dict[str, arcade.View] = {}

    def __repr__(self) -> str:
        return f"<Window (Width={self.width}) (Height={self.height})>"


def main() -> None:
    """Initialises the game and runs it."""
    window = Window("Educational Game")
    window.center_window()
    new_view = StartMenu()
    window.views["StartMenu"] = new_view
    window.show_view(new_view)
    new_view.manager.enable()
    window.run()


if __name__ == "__main__":
    main()
