import pygame as pg


vec = pg.math.Vector2  # 2D vector class used for position calculations


# Frame Rate Setting
FPS = 60  # Frames per second, controls the update speed of the game

# Color Definitions (RGB format)
FIELD_COLOR = (48, 39, 32)  # Background color for the game field
RED = (255, 0, 0)  # Red color for 'Game Over' text
WHITE = (255, 255, 255)  # White color for regular text
YELLOW = (255, 255, 0)  # Yellow color for pause text
BLACK = (0, 0, 0)  # Black color for drawing grid lines


PAUSE_TEXT = "Press P to Pause"  # Text displayed when the game is paused
GAME_OVER_TEXT = "GAME OVER Press R to Restart"  # Text displayed when the game is over


# Asset Paths
SPRITE_DIR_PATH = 'assets/tiles'  # Directory containing block images
FONT_PATH = 'assets/font/PartyLET-plain.ttf'  # Path to custom font used for in-game text

# Falling Speed Timers (in milliseconds)
ANIM_TIME_INTERVAL = 300  # Normal falling interval (slow descent)
FAST_ANIM_TIME_INTERVAL = 20  # Fast falling interval (when player holds Down key)


# Field and Tile Settings
TILE_SIZE = 50  # Size of each block (square tile) in pixels
FIELD_SIZE = FIELD_W, FIELD_H = 8, 16  # Field grid size: 8 columns by 16 rows
FIELD_RES = FIELD_W * TILE_SIZE, FIELD_H * TILE_SIZE  # Pixel resolution of the field area


# Game Window Settings
FIELD_SCALE_W, FIELD_SCALE_H = 2.2, 1  # Scaling factors for window width and height
WIN_RES = WIN_W, WIN_H = FIELD_RES[0] * FIELD_SCALE_W, FIELD_RES[1] * FIELD_SCALE_H  # Final game window size in pixels


INIT_POS_OFFSET = vec(FIELD_W // 2, 1)  # Starting offset for new Tetromino (spawn point)
NEXT_POS_OFFSET = vec(FIELD_W * 1.5, FIELD_H * 0.37)  # Position offset for 'Next Tetromino' preview


MOVE_DIRECTIONS = {
    'left': vec(-1, 0),  # Move one block left
    'right': vec(1, 0),  # Move one block right
    'down': vec(0, 1)  # Move one block down
}

# Tetromino Shape Definitions
# Each Tetromino is defined as a list of block positions relative to the pivot
TETROMINOES = {
    'T': [(0, 1), (-1, 1), (1, 1), (0, 0)],  # T-shape
    'O': [(0, 1), (0, 0), (1, 1), (1, 0)],  # O-shape (square)
    'J': [(0, 1), (-1, 1), (0, 0), (0, -1)],  # J-shape
    'L': [(0, 1), (1, 1), (0, 0), (0, -1)],  # L-shape
    'I': [(0, 2), (0, 1), (0, 0), (0, -1)],  # I-shape (line)
    'S': [(0, 1), (-1, 1), (0, 0), (1, 0)],  # S-shape
    'Z': [(0, 1), (1, 1), (0, 0), (-1, 0)]  # Z-shape
}