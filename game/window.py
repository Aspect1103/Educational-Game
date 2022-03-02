from __future__ import annotations

# Builtin
from typing import TYPE_CHECKING, Dict, Optional

# Pip
import arcade

# Custom
from database import Database
from sounds import sounds
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
    sounds: Dict[str, arcade.Sound]
        The dictionary which holds all the music for the game.
    current_sound: Optional[arcade.Sound]
        The currently playing sound.
    player: Optional[Player]
        The pyglet media player which actually plays the music.
    database: Database
        The connection to the sqlite database.
    """

    def __init__(self, title: str) -> None:
        super().__init__(title=title)
        self.views: Dict[str, arcade.View] = {}
        self.sounds: Dict[str, arcade.Sound] = sounds
        self.current_sound: Optional[arcade.Sound] = None
        self.player: Optional[Player] = None
        self.database: Database = Database(self)

    def __repr__(self) -> str:
        return f"<Window (Width={self.width}) (Height={self.height})>"

    @staticmethod
    def seconds_to_string(seconds: float) -> str:
        """
        Converts seconds into a minutes and seconds formatted in a string.

        Parameters
        ----------
        seconds: float
            The seconds to convert to a string.

        Returns
        -------
        str
            The formatted string.
        """
        return f"Time: {int(seconds / 60)} minutes and {int(seconds % 60)} seconds"


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
