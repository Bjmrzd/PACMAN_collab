import pygame as pg
from src.parsing import parsing
from src.helper import Color, Box_Button, Font, Size, Text
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
                if keys[pg.K_c]:
                    self.cheat_screen()
            pg.display.flip()
            # need to create a user list for the buttons

    def game_over(self):
        """Game over screen"""
        pass

    def win(self):
        """Win screen"""
        running: bool = True

        while running:

    def pause_menu(self):
        """Pause Menu"""
        from src.main_menu import MainMenu
        running: bool = True
        no_resume: bool = True
        width_button: int = 100
        height_button: int = 100
        size_text: int = Size.TEXT.value
        menu = MainMenu(self.screen, self.screen_height, self.screen_width)

        while running:
            self.screen.fill(Color.BLACK.value)
            mouse = pg.mouse.get_pos()
            # maybe need to change menu button pos diff
            # the click linger and can activate the start game from the menu by accident

            exit_button = Box_Button(self.screen_width / 2, self.screen_height / 2 + 400, width_button, height_button, "Quit", size_text)
            exit_button.create_button(self.screen, mouse)

            resume_button = Box_Button(self.screen_width / 2, self.screen_height / 2 + 100, width_button, height_button, "Resume", size_text)
            resume_button.create_button(self.screen, mouse)

            menu_button = Box_Button(self.screen_width / 2, self.screen_height / 2 - 50, width_button, height_button, "Menu", size_text)
            menu_button.create_button(self.screen, mouse)

            instructions_button = Box_Button(self.screen_width / 2, self.screen_height / 2 + 250, width_button, height_button, "Instructions", size_text)
            instructions_button.create_button(self.screen, mouse)

            title_menu = Text("Pause Menu", Color.RED.value, self.screen_width / 2, self.screen_height / 2 - 500, Size.TITLE.value)
            title_menu.show_text(self.screen)

            for event in pg.event.get():
                keys = pg.key.get_pressed()
                if keys[pg.K_ESCAPE]:
                    pg.quit()
                    sys.exit()
                if event.type == pg.MOUSEBUTTONDOWN:
                    if exit_button.rect.collidepoint(mouse):
                        pg.quit()
                        sys.exit()
                    if resume_button.rect.collidepoint(mouse):
                        running = False
                    if menu_button.rect.collidepoint(mouse):
                        no_resume = False
                        menu.init_menu(no_resume)
                    if instructions_button.rect.collidepoint(mouse):
                        menu.init_tuto()

            pg.display.flip()

    def cheat_screen(self):
        """Menu to activate/deactivate the cheat"""
        running: bool = True
        width_button: int = 100
        height_button: int = 100
        size_text: int = Size.TEXT.value

        while running:
            self.screen.fill(Color.BLACK.value)
            mouse = pg.mouse.get_pos()

            speed_button = Box_Button(self.screen_width / 2, self.screen_height / 2 + 300, width_button, height_button, "Speeeeeed", size_text)
            speed_button.create_button(self.screen, mouse)

            invincible_button = Box_Button(self.screen_width / 2, self.screen_height / 2, width_button, height_button, "I am <Title Card>", size_text)
            invincible_button.create_button(self.screen, mouse)

            no_collision_button = Box_Button(self.screen_width / 2, self.screen_height / 2 - 300, width_button, height_button, "Ghost is Ghost !", size_text)
            no_collision_button.create_button(self.screen, mouse)

            for event in pg.event.get():
                keys = pg.key.get_pressed()
                if keys[pg.K_ESCAPE]:
                    running = False

            pg.display.flip()

# Need to see if the win and game over function can't be done outside of the class, same for pause menu
# see if there is a need to create cursor for the button of the menu or not (with pygame.cursor probably)