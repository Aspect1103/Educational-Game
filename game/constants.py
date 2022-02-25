# Game constants
BUTTON_STYLE = {
    "font_size": 24,
    "font_color": (0, 0, 0),
    "bg_color": (196, 196, 196),
}
LEVEL_COUNT = 10

# Sprite sizes
SPRITE_SCALE = 0.5
SPRITE_SIZE = 128 * SPRITE_SCALE

# Physics constants
GRAVITY = (0, -2000)
DAMPING = 0.01  # This has to be set to 0.01 as 0 would make the player not move at all
FRICTION = 0.4
MASS = 1.0

# Entity constants
FACING_RIGHT = 1
FACING_LEFT = -1

# Player constants
PLAYER_MOVE_FORCE = 1000
PLAYER_JUMP_FORCE = 70000
PLAYER_ATTACK_COOLDOWN = 1

# Enemy constants
ENEMY_VIEW_DISTANCE = 5
ENEMY_MOVEMENT_FORCE = 500
ENEMY_ATTACK_COOLDOWN = 2

# Bullet constants
BULLET_VELOCITY = 500
BULLET_DAMAGE = 10
