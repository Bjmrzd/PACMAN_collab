import pygame as pg
from src.parsing import parsing
from src.helper import Color
import json
from typing import Any


class Game:
    def __init__(self, screen, screen_width, screen_height):
        self.screen = screen


    def main_loop(self):
        running: bool = True

        while running:
            self.screen.fill()
            pg.display.flip()