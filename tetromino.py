from settings import *  # Import all game settings and constants
import random  # Import random module for randomizing Tetromino shapes and effects

class Block(pg.sprite.Sprite):
    """A single square block that forms part of a Tetromino piece."""
    def __init__(self, tetromino, pos):
        self.tetromino = tetromino  # Reference to the parent Tetromino object
        self.pos = vec(pos) + INIT_POS_OFFSET  # Initial position on the grid
        self.next_pos = vec(pos) + NEXT_POS_OFFSET  # Position for the 'next piece' preview
        self.alive = True  # Status to determine if block is active

        super().__init__(tetromino.tetris.sprite_group)  # Add block to the sprite group
        self.image = tetromino.image  # Visual appearance of the block
        self.rect = self.image.get_rect()  # Rect object for positioning on screen

        # Special effects for disappearing animation
        self.sfx_image = self.image.copy()  # Create a faded version of the block for effects
        self.sfx_image.set_alpha(110)  # Set transparency for effect image
        self.sfx_speed = random.uniform(0.2, 0.6)  # Random speed for the disappearing effect
        self.sfx_cycles = random.randrange(6, 8)  # Number of animation cycles
        self.cycle_counter = 0  # Counter for tracking animation cycles

    def sfx_end_time(self):
        """Handle timing for the disappearing animation."""
        if self.tetromino.tetris.app.anim_trigger:
            self.cycle_counter += 1
            if self.cycle_counter > self.sfx_cycles:
                self.cycle_counter = 0
                return True
        return False

    def sfx_run(self):
        """Apply the fading and rotation animation."""
        self.image = self.sfx_image  # Switch to the semi-transparent image
        self.pos.y -= self.sfx_speed  # Move the block upwards slowly
        self.image = pg.transform.rotate(self.image, pg.time.get_ticks() * self.sfx_speed)  # Rotate the block

    def is_alive(self):
        """Manage the block’s status: animate when dead, remove when finished."""
        if not self.alive:
            if not self.sfx_end_time():
                self.sfx_run()
            else:
                self.kill()  # Remove the block from the game

    def rotate(self, pivot_pos):
        """Rotate the block 90 degrees around the pivot position."""
        translated = self.pos - pivot_pos  # Move relative to pivot
        rotated = translated.rotate(90)  # Rotate the position
        return rotated + pivot_pos  # Move back to field coordinates

    def set_rect_pos(self):
        """Update the block’s rect position for drawing based on current or preview position."""
        pos = [self.next_pos, self.pos][self.tetromino.current]
        self.rect.topleft = pos * TILE_SIZE  # Update top-left corner position

    def update(self):
        """Update the block each frame: handle status and position."""
        if self.alive:
            self.is_alive()
            self.set_rect_pos()

    def is_collide(self, pos):
        """Check if a block at the given position would collide with walls or other blocks."""
        x, y = int(pos.x), int(pos.y)
        if x < 0 or x >= FIELD_W or y >= FIELD_H:
            return True  # Colliding with walls or bottom
        if y >= 0 and self.tetromino.tetris.field_array[y][x]:
            return True  # Colliding with existing block
        return False

class Tetromino:
    """Class representing a complete Tetromino composed of multiple Blocks."""
    def __init__(self, tetris, current=True):
        self.tetris = tetris  # Reference to the Tetris game logic
        self.shape = random.choice(list(TETROMINOES.keys()))  # Randomly select a shape
        print(tetris.app.images) 
        self.image = random.choice(tetris.app.images) if tetris.app.images else None  # Randomly select a block image
        self.blocks = [Block(self, pos) for pos in TETROMINOES[self.shape]]  # Create the blocks based on the shape definition
        self.landing = False  # Flag indicating whether the Tetromino has landed
        self.current = current  # Is this the active (falling) Tetromino?

    def rotate(self):
        """Attempt to rotate the Tetromino 90 degrees around the pivot block."""
        pivot_pos = self.blocks[0].pos  # Use the first block as the rotation center
        new_block_positions = [block.rotate(pivot_pos) for block in self.blocks]

        if not self.is_collide(new_block_positions):
            for i, block in enumerate(self.blocks):
                block.pos = new_block_positions[i]  # Apply new rotated positions

    def is_collide(self, block_positions):
        """Check if the rotated or moved positions collide with walls or existing blocks."""
        for block, new_pos in zip(self.blocks, block_positions):
            if block.is_collide(new_pos):
                return True
        return False

    def move(self, direction):
        """Move the Tetromino in the specified direction (left, right, or down)."""
        move_direction = MOVE_DIRECTIONS[direction]  # Get movement vector
        new_block_positions = [block.pos + move_direction for block in self.blocks]

        if not self.is_collide(new_block_positions):
            for block in self.blocks:
                block.pos += move_direction  # Move all blocks
            self.landing = False
        elif direction == 'down':
            self.landing = True  # If moving down and cannot move further, mark as landed
            print("Tetromino landed!")
            self.tetris.speed_up = False  # Reset fast falling mode

    def update(self):
        """Update the Tetromino by moving it down automatically each frame."""
        self.move(direction='down')
