from settings import *  # Import all configuration settings
import math  # Import math functions for color animation
from tetromino import Tetromino  # Import Tetromino and Block classes
import pygame.freetype as ft  # Import Pygame freetype module for rendering text

class Text:
    """Class responsible for rendering dynamic UI text (title, score, next piece) in the game."""
    def __init__(self, app):
        self.app = app  # Reference to the main App object
        self.font = ft.Font(FONT_PATH)  # Load custom font for rendering text

    def get_color(self):
        """Generate dynamic color values based on sine waves over time."""
        time = pg.time.get_ticks() * 0.001  # Get elapsed time in seconds
        n_sin = lambda t: (math.sin(t) * 0.5 + 0.5) * 255  # Normalize sine wave output to 0-255 range
        return n_sin(time * 0.5), n_sin(time * 0.2), n_sin(time * 0.9)  # Return dynamic RGB color values

    def draw(self):
        """Render the Tetris title, next piece label, and score display on the screen."""
        self.font.render_to(self.app.screen, (WIN_W * 0.595, WIN_H * 0.02),
                            text='TETRIS', fgcolor=self.get_color(),
                            size=TILE_SIZE * 1.65, bgcolor='black')
        self.font.render_to(self.app.screen, (WIN_W * 0.65, WIN_H * 0.22),
                            text='next', fgcolor=self.get_color(),
                            size=TILE_SIZE * 1.4, bgcolor='black')
        self.font.render_to(self.app.screen, (WIN_W * 0.64, WIN_H * 0.67),
                            text='score', fgcolor=self.get_color(),
                            size=TILE_SIZE * 1.4, bgcolor='black')
        self.font.render_to(self.app.screen, (WIN_W * 0.64, WIN_H * 0.8),
                            text=f'{self.app.tetris.score}', fgcolor='white',
                            size=TILE_SIZE * 1.8)

class Tetris:
    """Main class that implements Tetris game mechanics, state management, and drawing."""
    def __init__(self, app):
        self.app = app  # Reference to the main App object
        self.sprite_group = pg.sprite.Group()  # Group to manage and render all block sprites
        self.field_array = self.get_field_array()  # 2D list representing the playing field
        self.tetromino = Tetromino(self)  # Current falling Tetromino
        self.next_tetromino = Tetromino(self, current=False)  # Next Tetromino preview
        self.speed_up = False  # Flag to speed up falling when Down key is pressed

        self.score = 0  # Player's current score
        self.full_lines = 0  # Number of full lines cleared
        self.points_per_lines = {0: 0, 1: 100, 2: 300, 3: 700, 4: 1500}  # Points awarded based on lines cleared

        self.paused = False  # Flag to track pause state
        self.initialized = False  # Flag to track if the game has started
        self.game_over = False  # Flag to track game over state

    def toggle_pause(self):
        """Toggle the paused state of the game."""
        self.paused = not self.paused

    def get_score(self):
        """Update the total score based on the number of lines cleared."""
        self.score += self.points_per_lines[self.full_lines]
        self.full_lines = 0  # Reset full lines counter after adding to score

    def check_full_lines(self):
        """Check and clear any completed full lines on the field."""
        row = FIELD_H - 1  # Start checking from the bottom row
        for y in range(FIELD_H - 1, -1, -1):  # Traverse rows upward
            for x in range(FIELD_W):
                self.field_array[row][x] = self.field_array[y][x]  # Move rows downward
                if self.field_array[y][x]:
                    self.field_array[row][x].pos = vec(x, y)  # Update block positions

            if sum(map(bool, self.field_array[y])) < FIELD_W:
                row -= 1  # If the row is not full, move up
            else:
                for x in range(FIELD_W):
                    self.field_array[row][x].alive = False  # Mark blocks as inactive
                    self.field_array[row][x] = 0  # Clear the blocks
                self.full_lines += 1  # Increment full lines counter

    def put_tetromino_blocks_in_array(self):
        """Place the Tetromino blocks into the field array after landing."""
        for block in self.tetromino.blocks:
            x, y = int(block.pos.x), int(block.pos.y)
            if y >= 0:  # Only update if inside the visible field
                self.field_array[y][x] = block

    def get_field_array(self):
        """Initialize an empty playing field."""
        return [[0 for x in range(FIELD_W)] for y in range(FIELD_H)]

    def check_tetromino_landing(self):
        """Handle landing of a Tetromino and prepare the next Tetromino."""
        if self.tetromino.landing:
            self.put_tetromino_blocks_in_array()  # Save Tetromino blocks into field
            self.next_tetromino.current = True  # Make next Tetromino active
            self.tetromino = self.next_tetromino  # Switch to next Tetromino
            self.next_tetromino = Tetromino(self, current=False)  # Generate a new next Tetromino

            # Check if new Tetromino collides immediately (game over condition)
            for block in self.tetromino.blocks:
                x, y = int(block.pos.x), int(block.pos.y)
                if y < 0 or (y >= 0 and self.field_array[y][x]):
                    self.game_over = True  # Set game over flag
                    return

            self.check_full_lines()  # Check and clear full lines

    def update(self):
        """Update the game logic each frame."""
        if self.paused or self.game_over:
            return  # Do not update if game is paused or over

        trigger = [self.app.anim_trigger, self.app.fast_anim_trigger][self.speed_up]
        if trigger:
            self.tetromino.update()  # Move the Tetromino down
            if self.tetromino.landing:
                self.check_tetromino_landing()

        if not self.initialized:
            self.initialized = True  # Mark the game as started

        self.get_score()  # Update score
        self.sprite_group.update()  # Update all block sprites

    def stop_tetromino(self):
        """Stop the current Tetromino movement (used when game is over)."""
        if self.tetromino:
            for block in self.tetromino.blocks:
                block.pos.y = block.pos.y  # Keep block positions fixed
            self.tetromino = None  # Remove reference to current Tetromino

    def control(self, pressed_key):
        """Handle keyboard input for Tetromino movement and rotation."""
        if pressed_key == pg.K_LEFT:
            self.tetromino.move(direction='left')
        elif pressed_key == pg.K_RIGHT:
            self.tetromino.move(direction='right')
        elif pressed_key == pg.K_UP:
            self.tetromino.rotate()
        elif pressed_key == pg.K_DOWN:
            self.speed_up = True
        elif pressed_key == pg.K_p:
            self.toggle_pause()

    def draw_grid(self):
        """Draw the grid lines on the field."""
        for x in range(FIELD_W):
            for y in range(FIELD_H):
                pg.draw.rect(self.app.screen, 'black',
                             (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE), 1)

    def draw(self):
        """Draw the entire game field and handle pause/game over screens."""
        self.draw_grid()
        self.sprite_group.draw(self.app.screen)

        if self.paused:
            self.draw_pause()
        elif self.game_over:
            self.draw_game_over()

    def draw_pause(self):
        """Draw the pause message on the screen."""
        pause_msg = self.app.font.render(PAUSE_TEXT, True, YELLOW)
        self.app.screen.blit(pause_msg, (WIN_W // 2 - pause_msg.get_width() // 2, WIN_H // 2))

    def draw_game_over(self):
        """Draw the Game Over screen with restart instructions."""
        large_font = pg.font.SysFont('Arial', 50)  # Font for Game Over message
        small_font = pg.font.SysFont('Arial', 30)  # Font for Restart message

        # Render text
        game_over_msg = large_font.render("GAME OVER", True, RED)
        restart_msg = small_font.render("Press R to Restart", True, WHITE)

        # Center text on the screen
        game_over_x = WIN_W // 2 - game_over_msg.get_width() // 2
        game_over_y = WIN_H // 2 - game_over_msg.get_height() - 20
        restart_x = WIN_W // 2 - restart_msg.get_width() // 2
        restart_y = WIN_H // 2 + 20

        # Draw text on screen
        self.app.screen.blit(game_over_msg, (game_over_x, game_over_y))
        self.app.screen.blit(restart_msg, (restart_x, restart_y))
