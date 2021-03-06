from __future__ import annotations

# Builtin
import pathlib
from typing import Dict, List

# Pip
import arcade

# Create the texture path
texture_path = (
    pathlib.Path(__file__).resolve().parent.joinpath("resources").joinpath("textures")
)

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
    "boss": {
        "idle": ["boss_idle.png"],
        "jump": ["boss_jump.png"],
        "fall": ["boss_fall.png"],
        "walk": [
            "boss_walk1.png",
            "boss_walk2.png",
            "boss_walk3.png",
            "boss_walk4.png",
            "boss_walk5.png",
            "boss_walk6.png",
            "boss_walk7.png",
            "boss_walk8.png",
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
