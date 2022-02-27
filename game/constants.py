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
FACING_RIGHT = 0
FACING_LEFT = 1
DEAD_ZONE = 0.1  # Needed since the physics engine often flips above and below zero
DISTANCE_TO_CHANGE_TEXTURE = 20  # How far the entity needs to travel to change texture

# Player constants
PLAYER_MOVE_FORCE = 1000
PLAYER_JUMP_FORCE = 70000
PLAYER_ATTACK_COOLDOWN = 1
BLOCKER_WALL_HEALTH_LOSS = 20

# Enemy constants
ENEMY_VIEW_DISTANCE = 5
ENEMY_MOVEMENT_FORCE = 500
ENEMY_ATTACK_COOLDOWN_MIN = 2
ENEMY_ATTACK_COOLDOWN_MAX = 4

# Bullet constants
BULLET_VELOCITY = 500
BULLET_DAMAGE = 10
