import pygame as pg
from src.parsing import parsing
from src.helper import Color
import json
from typing import Any


class Game:
    """Class for the pacman game"""
    def __init__(self, screen, screen_width, screen_height):
        self.screen = screen
        self.screen_widht = screen_width
        self.screen_height = screen_height


    def main_loop(self):
        """Main game loop"""
        running: bool = True

        while running:
            self.screen.fill(Color.BLACK.value)
            for event in pg.event.get():
                keys = pg.key.get_pressed()
                if keys[pg.K_ESCAPE]:
                    pass
            pg.display.flip()

    def game_over(self):
        """Game over screen"""
        pass

    def win(self):
        """Win screen"""
        pass

    def pause_menu(self):
        """Pause Menu"""
        pass

# Need to see if the win and game over function can't be done outside of the class, same for pause menu