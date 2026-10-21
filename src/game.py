import pygame as pg
from src.parsing import parsing
from src.helper import Color, Box_Button, Font, Size
import json
from typing import Any
import sys


class Game:
    """Class for the pacman game"""
    def __init__(self, screen, screen_width, screen_height):
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height

    def main_loop(self):
        """Main game loop"""
        running: bool = True

        while running:
            self.screen.fill(Color.BLACK.value)
            for event in pg.event.get():
                keys = pg.key.get_pressed()
                if keys[pg.K_ESCAPE]:
                    self.pause_menu()
            pg.display.flip()

    def game_over(self):
        """Game over screen"""
        pass

    def win(self):
        """Win screen"""
        pass

    def pause_menu(self):
        """Pause Menu"""
        from src.main_menu import MainMenu
        running: bool = True
        no_resume: bool = True
        width_button: int = 100
        height_button: int = 100
        size_text: int = Size.TEXT.value

        while running:
            self.screen.fill(Color.BLACK.value)
            mouse = pg.mouse.get_pos()

            exit_button = Box_Button(self.screen_width / 2, self.screen_height / 2 + 200, width_button, height_button, "Quit", size_text)
            exit_button.create_button(self.screen, mouse)

            resume_button = Box_Button(self.screen_width / 2, self.screen_height / 2, width_button, height_button, "Resume", size_text)
            resume_button.create_button(self.screen, mouse)

            menu_button = Box_Button(self.screen_width / 2, self.screen_height / 2 - 200, width_button, height_button, "Menu", size_text)
            menu_button.create_button(self.screen, mouse)

            for event in pg.event.get():
                keys = pg.key.get_pressed()
                if keys[pg.K_ESCAPE]:
                    pass
                if event.type == pg.MOUSEBUTTONDOWN:
                    if exit_button.rect.collidepoint(mouse):
                        pg.quit()
                        sys.exit()
                    if resume_button.rect.collidepoint(mouse):
                        running = False
                    if menu_button.rect.collidepoint(mouse):
                        no_resume = False
                        menu = MainMenu(self.screen, self.screen_height, self.screen_width)
                        menu.init_menu(no_resume)

            pg.display.flip()

# Need to see if the win and game over function can't be done outside of the class, same for pause menu
# see if there is a need to create cursor for the button of the menu or not (with pygame.cursor probably)