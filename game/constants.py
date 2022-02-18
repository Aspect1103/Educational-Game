# Universal button style
BUTTON_STYLE = {
    "font_size": 24,
    "font_color": (0, 0, 0),
    "bg_color": (196, 196, 196),
}

# Sprite sizes
SPRITE_SCALE = 0.5

# Player constants
PLAYER_MAX_HORIZONTAL_SPEED = 500
PLAYER_MAX_VERTICAL_SPEED = 2000
PLAYER_MOVE_FORCE = 1000
PLAYER_JUMP_FORCE = 70000

# Entity constants
ATTACK_COOLDOWN = 1
FACING_RIGHT = 1
FACING_LEFT = -1

# Physics constants
GRAVITY = (0, -2000)
DAMPING = 0.01  # This has to be set to 0.01 as 0 would make the player not move at all
FRICTION = 1.0
PLAYER_MASS = 1.0
