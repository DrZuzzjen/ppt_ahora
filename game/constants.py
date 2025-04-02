"""
Constants for Mario Sisters game.
A satirical twist on the classic game.
"""

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Mario Sisters"
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
PINK = (255, 192, 203)
PURPLE = (128, 0, 128)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
SKY_BLUE = (135, 206, 235)

# Player properties
PLAYER_ACC = 0.5
PLAYER_FRICTION = -0.12
PLAYER_GRAVITY = 0.5
PLAYER_JUMP = -16

# Game properties
TITLE_FONT_SIZE = 48
NORMAL_FONT_SIZE = 22
SMALL_FONT_SIZE = 16

# Sprite sizes
TILE_SIZE = 32
PLAYER_WIDTH = 32
PLAYER_HEIGHT = 64

# Game states
STATE_INTRO = 0
STATE_PLAYING = 1
STATE_GAME_OVER = 2
STATE_WIN = 3
STATE_PAUSE = 4