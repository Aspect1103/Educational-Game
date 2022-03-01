from __future__ import annotations

# Builtin
from typing import TYPE_CHECKING, Dict, Optional

# Pip
import arcade

# Custom
from resources.sounds import sounds
from views.start_menu import StartMenu

if TYPE_CHECKING:
    from pyglet.media import Player


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
        self.sounds: Dict[str, arcade.Sound] = sounds
        self.current_sound: Optional[arcade.Sound] = None
        self.player: Optional[Player] = None

    def __repr__(self) -> str:
        return f"<Window (Width={self.width}) (Height={self.height})>"


def main() -> None:
    """Initialises the game and runs it."""
    # Initialise the window
    window = Window("Educational Game")
    window.center_window()

    # Initialise and load the start menu view
    new_view = StartMenu()
    window.views["StartMenu"] = new_view
    window.show_view(new_view)
    new_view.manager.enable()

    # Play the start menu music
    window.current_sound = window.sounds["start menu"]
    window.player = window.current_sound.play(loop=True)

    # Run the game
    window.run()


if __name__ == "__main__":
    main()
