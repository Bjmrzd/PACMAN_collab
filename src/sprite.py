import pygame as pg
from typing import Any
from abc import ABC, abstractmethod


class Sprite(ABC, pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)

    @abstractmethod
    def check_collisions(self):
        pass


class Pacman(Sprite):
    def __init__(self, row, col, lives):
        super().__init__()
        self.row = row
        self.col = col
        self.lives = lives

    def check_collisions(self):
        pass


class Lives(pg.sprite.Sprite):
    def __init__(self, lives, row, col):
        super().__init__()

        self.lives = lives
        self.sprite = pg.image.load("assets/pacsprites.png").convert_alpha()
        self.lives_sprites = self.sprite.subsurface((35, 35, 25, 25))

        self.image = self.lives_sprites
        self.rect = self.image.get_rect()
        self.rect.topleft = (row, col)

    def update_sprite(self):
        no_lives = self.sprite.subsurface((470, 5, 25, 25))

# started to create the abstract class for the sprite.
# need to see if the abstract class are necessary, the init and the super should stay like this
# Sprite inherit from ABC and pg.sprite.Sprite, we init the pg.sprite.Sprite in this class
# And super in the other