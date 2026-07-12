#!/usr/bin/env python3
"""
Wolf Game - Main Entry Point
2D survival game where you play as a wolf
"""

import pygame
import sys
from config import *
from src.game import Game

def main():
    # Initialize Pygame
    pygame.init()
    
    # Create game instance
    game = Game()
    
    # Run the game
    game.run()
    
    # Cleanup
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
