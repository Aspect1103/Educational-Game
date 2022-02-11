from __future__ import annotations

# Builtin
import pathlib

# Pip
import arcade

# Create the texture path
texture_path = pathlib.Path(__file__).resolve().parent.joinpath("images")

# Create a list to hold all the filenames for the textures
filenames = {
    "background": [
        "background.png",
    ],
}

# Create the textures
textures = {}
for key, value in filenames.items():
    textures[key] = [
        arcade.load_texture(str(texture_path.joinpath(filename))) for filename in value
    ]
