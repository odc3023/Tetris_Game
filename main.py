from settings import *  # Import all configuration settings
from tetris import Tetris, Text  # Import Tetris game logic and Text display class
import sys  # System-specific parameters and functions
import pathlib  # For file and directory path manipulations


class App:
    """Main application class for running the Tetris game."""
    
    def __init__(self):
        pg.init()  # Initialize all Pygame modules
        pg.display.set_caption('Tetris')  # Set the window title
        self.screen = pg.display.set_mode(WIN_RES)  # Set the game screen resolution
        self.clock = pg.time.Clock()  # Initialize the clock for frame rate control
        self.set_timer()  # Set up timer events for animation
        self.font = pg.font.SysFont('Arial', 20)  # Load a system font for rendering text
        self.images = self.load_images()  # Load and scale block images
        self.tetris = Tetris(self)  # Create an instance of the Tetris game
        self.text = Text(self)  # Create an instance of the Text rendering class

    def load_images(self):
        """Load all PNG images from the sprite directory and scale them."""
        files = [item for item in pathlib.Path(SPRITE_DIR_PATH).rglob('*.png') if item.is_file()]
        images = [pg.image.load(file).convert_alpha() for file in files]  # Load images with alpha transparency
        images = [pg.transform.scale(image, (TILE_SIZE, TILE_SIZE)) for image in images]  # Resize images
        return images

    def set_timer(self):
        """Set timers for regular and fast falling animation events."""
        self.user_event = pg.USEREVENT + 0  # Custom event for normal fall
        self.fast_user_event = pg.USEREVENT + 1  # Custom event for fast fall
        self.anim_trigger = False  # Flag for normal fall animation
        self.fast_anim_trigger = False  # Flag for fast fall animation
        pg.time.set_timer(self.user_event, ANIM_TIME_INTERVAL)  # Set timer for normal fall
        pg.time.set_timer(self.fast_user_event, FAST_ANIM_TIME_INTERVAL)  # Set timer for fast fall

    def update(self):
        """Update the game state and control the frame rate."""
        self.tetris.update()  # Update Tetris game logic
        self.clock.tick(FPS)  # Limit the frame rate

    def draw(self):
        """Render the background, game field, and text to the screen."""
        bg_image = pg.image.load("assets/bg.png").convert()  # Load and convert background image
        bg_image = pg.transform.scale(bg_image, WIN_RES)  # Scale background image to screen size
        self.screen.blit(bg_image, (0, 0))  # Draw the background
        self.tetris.draw()  # Draw the Tetris field
        self.text.draw()  # Draw the text (e.g., score, title)
        pg.display.flip()  # Update the full display

    def check_events(self):
        """Handle all incoming Pygame events."""
        self.anim_trigger = False  # Reset normal animation trigger
        self.fast_anim_trigger = False  # Reset fast animation trigger
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                # Exit the game cleanly
                pg.quit()
                sys.exit()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_p:
                    self.tetris.toggle_pause()  # Pause or resume the game
                elif event.key == pg.K_r and self.tetris.game_over:
                    self.__init__()  # Reinitialize the game after Game Over
                else:
                    self.tetris.control(pressed_key=event.key)  # Handle Tetromino movement and rotation
            elif event.type == self.user_event:
                self.anim_trigger = True  # Trigger normal falling
            elif event.type == self.fast_user_event:
                self.fast_anim_trigger = True  # Trigger fast falling

    def run(self):
        """Main game loop."""
        while True:
            self.check_events()  # Handle user input and system events
            self.update()  # Update game logic
            self.draw()  # Draw everything on the screen

# Start the game when the script is executed
if __name__ == '__main__':
    app = App()
    app.run()