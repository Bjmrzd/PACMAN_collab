import pygame as pg
import sys
from src.game import Game
from src.parsing import parsing
import json
from typing import Any


class MainMenu():
    def __init__(self, screen, screen_height: int, screen_width: int):
        self.screen = screen
        self.screen_height = screen_height
        self.screen_width = screen_width