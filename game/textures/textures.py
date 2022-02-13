from __future__ import annotations

import pathlib

# Builtin
from typing import Dict, List

# Pip
import arcade

# Create the texture path
texture_path = pathlib.Path(__file__).resolve().parent.joinpath("images")

# Create a dictionary to hold all the filenames for the textures
filenames = {
    "background": [
        "background.png",
    ],
}

# Create the textures
textures: Dict[str, List[arcade.Texture]] = {}
for key, value in filenames.items():
    textures[key] = [
        arcade.load_texture(str(texture_path.joinpath(filename))) for filename in value
    ]
