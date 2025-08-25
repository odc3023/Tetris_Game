
# Tetris Game – Graphics & Virtual Reality Final Project (Spring 2025)

This is a classic Tetris game clone built using Python and Pygame. It was developed as the final project for the Graphics and Virtual Reality course at HIT, Spring 2025. One of the key requirements for this project was to provide extensive code comments explaining the logic and functionality of each section, making the code accessible and educational.

## Features

- Classic Tetris gameplay: real-time falling, movement, rotation, line clearing, scoring, pause/resume, and restart.
- Dynamic UI with custom background and font.
- Sprite-based block management and collision detection.
- Modular code structure with clear separation of concerns.
- All major functions and classes are thoroughly commented for clarity.

## File Structure

- `main.py`: Launches the game and manages the main loop.
- `tetris.py`: Implements game mechanics, state management, and rendering.
- `tetromino.py`: Handles Tetromino shapes, movement, rotation, and block logic.
- `settings.py`: Contains all game constants, settings, and asset paths.
- `assets/`: Includes background image, block sprites, and custom font.
- `read_me/README.md`: Project overview, instructions, and controls.

## How to Run

1. Install Python 3.11 and Pygame:
	```
	pip install pygame
	```
2. Run the game:
	```
	python main.py
	```

## Controls

- Left Arrow: Move left
- Right Arrow: Move right
- Up Arrow: Rotate tetromino
- Down Arrow: Fast fall
- P: Pause/Resume
- R: Restart (after Game Over)
- ESC: Quit

## Educational Value

The code is heavily commented to explain each step, variable, and function, fulfilling the course requirement for extensive documentation. This makes it a great resource for learning about game loops, event-driven programming, sprite management, and collision detection in Python.

