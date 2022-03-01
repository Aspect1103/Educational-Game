from __future__ import annotations

import pathlib

# Builtin
from typing import Dict

# Pip
import arcade

# Create the sound path
sound_path = pathlib.Path(__file__).resolve().parent.joinpath("sounds")

# Create a dictionary to hold all the filenames for the sounds
sound_filenames = {
    "start menu": "start menu.wav",
    "game": "game.mp3",
    "end screen": "end screen.mp3",
}

# Create the sound dictionary
sounds: Dict[str, arcade.Sound] = {
    key: arcade.load_sound(str(sound_path.joinpath(value)), True)
    for key, value in sound_filenames.items()
}
