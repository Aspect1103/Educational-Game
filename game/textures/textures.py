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
    "background": ["background.png"],
    "bullet": ["bullet.png"],
}
# Create a dictionary to hold all the filenames for the non-moving textures
moving_filenames = {
    "player": {"idle": ["player.png"], "walking": ["player.png"]},
    "enemy": {"idle": ["enemy.png"], "walking": ["enemy.png"]},
}
# Create the non-moving textures
non_moving_textures: Dict[str, List[arcade.Texture]] = {
    key: [
        arcade.load_texture(str(texture_path.joinpath(filename))) for filename in value
    ]
    for key, value in non_moving_filenames.items()
}

# Create the moving textures
moving_textures: Dict[str, Dict[str, List[Tuple[arcade.Texture, arcade.Texture]]]] = {
    key: {
        animation_type: [
            load_texture_pair(texture_path.joinpath(filename)) for filename in sublist
        ]
        for animation_type, sublist in value.items()
    }
    for key, value in moving_filenames.items()
}
