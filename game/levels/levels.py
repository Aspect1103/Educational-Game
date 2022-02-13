from __future__ import annotations

import pathlib

# Builtin
from typing import Dict

# Pip
import arcade

# Custom
from constants import SPRITE_SCALE

# Create the level path
level_path = pathlib.Path(__file__).resolve().parent

# Create a dictionary to hold all the filenames for the levels
filenames = {
    "1": "level_one.json",
}

# Create a dictionary to hold all the options for each layer
layer_options = {
    "Platforms": {
        "use_spatial_hash": True,
    },
    "Walls": {"use_spatial_hash": True},
}

# Create the levels
levels: Dict[str, arcade.TileMap] = {
    key: arcade.load_tilemap(
        str(level_path.joinpath(value)), SPRITE_SCALE, layer_options
    )
    for key, value in filenames.items()
}
