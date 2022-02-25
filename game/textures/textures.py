from __future__ import annotations

# Builtin
import pathlib
from typing import Dict, List, Tuple

# Pip
import arcade


def load_texture_pair(filename: pathlib.Path) -> Tuple[arcade.Texture, arcade.Texture]:
    """
    Loads a texture pair, with the second being a mirror image.

    Parameters
    ----------
    filename: pathlib.Path
        The texture path

    Returns
    -------
    Tuple[arcade.Texture, arcade.Texture]
        The texture pair.
    """
    return arcade.load_texture(filename), arcade.load_texture(
        filename, flipped_horizontally=True
    )


# Create the texture path
texture_path = pathlib.Path(__file__).resolve().parent.joinpath("images")

# Create a dictionary to hold all the filenames for the non-moving textures
non_moving_filenames = {
    "background": "background.png",
}
# Create a dictionary to hold all the filenames for the non-moving textures
moving_filenames = {
    "player": {
        "idle": ["player_idle.png"],
        "jump": ["player_jump.png"],
        "fall": ["player_fall.png"],
        "walk": [
            "player_walk1.png",
            "player_walk2.png",
            "player_walk3.png",
            "player_walk4.png",
            "player_walk5.png",
            "player_walk6.png",
            "player_walk7.png",
            "player_walk8.png",
        ],
    },
    "enemy": {
        "idle": ["enemy_idle.png"],
        "jump": ["enemy_jump.png"],
        "fall": ["enemy_fall.png"],
        "walk": [
            "enemy_walk1.png",
            "enemy_walk2.png",
            "enemy_walk3.png",
            "enemy_walk4.png",
            "enemy_walk5.png",
            "enemy_walk6.png",
            "enemy_walk7.png",
            "enemy_walk8.png",
        ],
    },
}
# Create the non-moving textures
non_moving_textures: Dict[str, arcade.Texture] = {
    key: arcade.load_texture(str(texture_path.joinpath(value)))
    for key, value in non_moving_filenames.items()
}

# Create the moving textures
moving_textures: Dict[str, Dict[str, List[List[arcade.Texture]]]] = {
    key: {
        animation_type: [
            arcade.load_texture_pair(texture_path.joinpath(filename))
            for filename in sublist
        ]
        for animation_type, sublist in value.items()
    }
    for key, value in moving_filenames.items()
}
