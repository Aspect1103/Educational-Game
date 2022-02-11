from __future__ import annotations

# Pip
import arcade
from constants import SCREEN_HEIGHT, SCREEN_WIDTH

# Custom
from views.start_menu import StartMenu


class Window(arcade.Window):
    """
    Manages the window and allows switching between views.

    Parameters
    ----------
    width: int
        The width of the window.
    height: int
        The height of the window.
    """

    def __init__(self, width: int, height: int) -> None:
        super().__init__(width=width, height=height)

    def __repr__(self) -> str:
        return f"<Window (Width={self.width}) (Height={self.height})>"


def main() -> None:
    """Initialises the game and runs it."""
    window = Window(SCREEN_WIDTH, SCREEN_HEIGHT)
    window.center_window()
    window.show_view(StartMenu())
    window.run()


if __name__ == "__main__":
    main()
