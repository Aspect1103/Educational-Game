# Pip
import arcade


class Game(arcade.View):
    def __init__(self, level: int) -> None:
        super().__init__()
        print(level)
        arcade.exit()
