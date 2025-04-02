"""
Mario Sisters - A Satirical Platform Game
Main entry point for the game

Controls:
- Arrow Keys: Move
- Space/Up: Jump
- Z/Shift: Special ability
- ESC: Pause
"""
import pygame
from game import Game

def main():
    """Main entry point for the game"""
    # Create and run the game
    game = Game()
    game.run()
    
    # Clean up pygame
    pygame.quit()

if __name__ == "__main__":
    main()