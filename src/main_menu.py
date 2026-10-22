import pygame as pg
import pygame_menu as pm
import pygvideo as pv
import sys
from src.game import Game
from src.parsing import parsing
from src.helper import Color
import json
from typing import Any


class MainMenu():
    def __init__(self, screen, screen_height: int, screen_width: int):
        self.screen = screen
        self.screen_height = screen_height
        self.screen_width = screen_width
        self.font = pm.font.FONT_8BIT
        self.theme = pm.Theme(widget_font=self.font, background_color=Color.BLACK.value)
        self.menu = pm.menu.Menu("Main Menu", self.screen_width, self.screen_height, theme=self.theme)

    def init_menu(self, no_resume: bool):
        """Init and display the main menu"""
        running: bool = True

        start_button = self.menu.add.button("Start game", self.init_game)
        instructions_button = self.menu.add.button("Instructions", self.init_tuto)
        highscore_button = self.menu.add.button("Highscores", self.init_highscore)
        if not no_resume:
            resume_button = self.menu.add.button("Resume game", self.resume_game)
        while running:
            mouse = pg.mouse.get_pos()
            self.screen.fill(Color.BLACK.value)
            events = pg.event.get()
            for event in events:
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                keys = pg.key.get_pressed()
                if keys[pg.K_ESCAPE]:
                    pg.quit()
                    sys.exit()

            self.menu.update(events)
            self.menu.draw(self.screen)
            self.menu.center_content()

            if not no_resume:
                resume_button.set_margin(0, 100)
                resume_button.set_padding(20)
                resume_button.draw(self.screen)
                if resume_button.is_selected():
                    # need to change this part it make the game lag and sometimes crash
                    # need to find better way to do this
                    for event in pg.event.get():
                        keys = pg.key.get_pressed()
                        if keys[pg.K_RETURN]:
                            running = False
            start_button.set_margin(0, 100)
            start_button.set_padding(20)
            start_button.draw(self.screen)

            instructions_button.set_margin(0, 100)
            instructions_button.set_padding(20)
            instructions_button.draw(self.screen)

            highscore_button.set_margin(0, 100)
            highscore_button.set_padding(20)
            highscore_button.draw(self.screen)

            pg.display.flip()

    def init_game(self):
        """Display and init the game loop but do not handle the loop logic"""
        game = Game(self.screen, self.screen_width, self.screen_height)
        game.main_loop()

    def init_tuto(self):
        """Init the tuto menu with the buttons instructions and how to play"""
        running = True
        arrows = pg.image.load("assets/arrows.png")

        while running:

            self.screen.fill(Color.BLACK.value)
            mouse = pg.mouse.get_pos()

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                keys = pg.key.get_pressed()
                if keys[pg.K_ESCAPE]:
                    running = False
            pg.display.flip()

    def init_highscore(self):
        """Init the menu that display the highscore"""
        pass

    def resume_game(self):
        # maybe useful to change the crashing loop in the main menu loop
        # else can be erased
        return False
