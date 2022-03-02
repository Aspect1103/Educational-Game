from __future__ import annotations

# Builtin
import json
import pathlib
from typing import Dict, List, NamedTuple, Union

# Pip
import arcade

# Custom
from constants import LEVEL_COUNT, SPRITE_SCALE


def load_tilemap(
    path: pathlib.Path, options: Dict[str, Dict[str, Union[str, bool]]]
) -> arcade.TileMap:
    """
    Initialises a tilemap.

    Parameters
    ----------
    path: pathlib.Path
        The tilemap path.
    options: Dict[str, Dict[str, Union[str, bool]]]
        Specific options to use when loading the tilemap.
    """
    return arcade.load_tilemap(str(path), SPRITE_SCALE, options)


class GameLevel(NamedTuple):
    """
    Represents a level in the game.

    tilemap: arcade.TileMap
        The loaded tilemap for the level.
    questions: List[Dict[str, Union[List[str], str]]]
        A list of questions with their correct answer and an explanation.
    """

    tilemap: arcade.TileMap
    questions: List[Dict[str, Union[List[str], str]]]


# Create the level path
level_path = (
    pathlib.Path(__file__).resolve().parent.joinpath("resources").joinpath("levels")
)

# Create a dictionary to hold all the options for each layer
layer_options: Dict[str, Dict[str, Union[str, bool]]] = {
    "Platforms": {
        "use_spatial_hash": True,
    },
    "Coins": {
        "use_spatial_hash": True,
    },
    "Door": {
        "use_spatial_hash": True,
    },
}

# Create the levels
levels: Dict[int, GameLevel] = {
    count
    + 1: GameLevel(
        load_tilemap(
            level_path.joinpath(f"Level {count+1}").joinpath("map.json"), layer_options
        ),
        json.loads(
            open(
                level_path.joinpath(f"Level {count+1}").joinpath("questions.json"),
                encoding="utf8",
            ).read()
        ),
    )
    for count in range(LEVEL_COUNT)
}
