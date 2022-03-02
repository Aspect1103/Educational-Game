from __future__ import annotations

# Builtin
import pathlib
import sqlite3
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from window import Window

# Get the path to the sqlite database
database_path = (
    pathlib.Path(__file__).resolve().parent.joinpath("resources").joinpath("scores.db")
)


class Database:
    """
    An abstracted class which provides an easy way to interact with the database.

    Parameters
    ----------
    window: Window
        The window which this class belong too.

    Attributes
    ----------
    connection: sqlite3.Connection
        The connection to the sqlite database.
    """

    def __init__(self, window: Window) -> None:
        self.window: Window = window
        self.connection: sqlite3.Connection = sqlite3.connect(database_path)

    def __repr__(self) -> str:
        return f"<Database (Connection={self.connection})>"

    def commit_score(self, score: int, time: float, win: bool, level: int) -> None:
        """
        Commits a score to the database

        Parameters
        ----------
        score: int
            The level score.
        time: float
            How long the level took to complete.
        win: bool
            Whether the player won or not.
        level: int
            The level number.
        """
        self.connection.execute(
            """
            INSERT INTO Scores(Score, Time_to_complete, Win, Level_ID)
            VALUES(?, ?, ?, ?)""",
            (score, time, win, level),
        )
        self.connection.commit()

    def get_five_scores(self, level: int) -> str:
        """
        Gets the top five scores for a specific level.

        Parameters
        ----------
        level: int
            The level to get the top five scores for.

        Returns
        -------
        str
            The score text which will be displayed to the user.
        """
        final = []
        cursor = self.connection.cursor()
        for count, result in enumerate(
            cursor.execute(
                """
                SELECT Score, Time_to_complete
                FROM Scores
                WHERE Level_ID = ?
                ORDER BY Score DESC, Time_to_complete ASC
                LIMIT 5""",
                (level,),
            )
        ):
            result = list(result)
            final.append(
                f"{count + 1}. Score: {result[0]}."
                f" {self.window.seconds_to_string(result[1])}."
            )
        if final:
            final.insert(0, f"Top 5 Scores (Level {level}):\n\n")
            return "\n".join(final)
        return "No scores saved. Play the level to generate some."
