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

    Attributes
    ----------
    views: Dict[str, arcade.View]
        Holds all the views used by the game.
    """

    def __init__(self) -> None:
        super().__init__()
        self.views: Dict[str, arcade.View] = {}

    def __repr__(self) -> str:
        return f"<Window (Width={self.width}) (Height={self.height})>"


def main() -> None:
    """Initialises the game and runs it."""
    window = Window()
    window.center_window()
    new_view = StartMenu()
    window.views["StartMenu"] = new_view
    window.show_view(new_view)
    new_view.manager.enable()
    window.run()


if __name__ == "__main__":
    main()
