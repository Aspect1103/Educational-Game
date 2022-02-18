from __future__ import annotations

# Builtin
import pathlib
from typing import Dict, NamedTuple, Union

# Pip
import arcade

# Custom
from constants import SPRITE_SCALE


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
    blocker_count: int
        The amount of blocker walls the level contains.
    """

    tilemap: arcade.TileMap
    blocker_count: int


# Create the level path
level_path = pathlib.Path(__file__).resolve().parent

# Create a dictionary to hold all the options for each layer
layer_options: Dict[str, Dict[str, Union[str, bool]]] = {
    "Platforms": {
        "use_spatial_hash": True,
    },
    "Walls": {
        "use_spatial_hash": True,
    },
    "Enemies": {
        "use_spatial_hash": True,
    },
    "Coins": {
        "use_spatial_hash": True,
    },
}

# Create the levels
levels: Dict[str, GameLevel] = {
    "1": GameLevel(
        load_tilemap(level_path.joinpath("level_one.json"), layer_options), 3
    )
}
