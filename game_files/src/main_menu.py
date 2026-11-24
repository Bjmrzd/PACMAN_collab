import pygame as pg
import pygame_menu as pm
import sys
from game_files.src.game import Game
from game_files.src.parsing import parsing
from game_files.src.helper import Color, Text, Size, Font
import json
from typing import Any


class MainMenu():
    def __init__(self, screen: Any, screen_height: int, screen_width: int):
        self.screen: Any = screen
        self.screen_height: int = screen_height
        self.screen_width: int = screen_width
        self.font = pm.font.FONT_8BIT
        self.theme = pm.Theme(
            widget_font=self.font, background_color=Color.BLACK.value)
        self.menu: Any = pm.menu.Menu(
            "Main Menu", self.screen_width,
            self.screen_height, theme=self.theme
            )
        self.running: bool = True

    def init_menu(self, no_resume: bool) -> None:
        """Init and display the main menu"""

        title_image = self.menu.add.image("game_files/assets/title.jpg")
        start_button = self.menu.add.button("Start game", self.init_game)
        instructions_button = self.menu.add.button(
            "Instructions", self.init_tuto)
        highscore_button = self.menu.add.button(
            "Highscores", self.init_highscore)

        if not no_resume:
            resume_button = self.menu.add.button(
                "Resume game", self.resume_game)

        while self.running:
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
                resume_button.set_margin(0, 50)
                resume_button.set_padding(15)
                resume_button.translate(0, 150)

            start_button.set_margin(0, 50)
            start_button.set_padding(15)
            start_button.translate(0, 0)

            instructions_button.set_margin(0, 50)
            instructions_button.set_padding(15)
            instructions_button.translate(0, 50)

            highscore_button.set_margin(0, 50)
            highscore_button.set_padding(15)
            highscore_button.translate(0, 100)

            title_image.translate(0, -300)

            pg.display.flip()
        self.running = True

    def init_game(self) -> None:
        """Display and init the game loop but do not handle the loop logic"""
        game = Game(self.screen, self.screen_width, self.screen_height)
        game.main_loop()

    def init_tuto(self) -> None:
        """Init the tuto menu with the buttons instructions and how to play"""
        running = True
        arrows = pg.image.load("game_files/assets/arrows.png")

        rules_font = pg.font.Font(Font.FONT1.value, 45)

        while running:

            self.screen.fill(Color.BLACK.value)

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                keys = pg.key.get_pressed()
                if keys[pg.K_ESCAPE]:
                    running = False
            self.screen.blit(arrows, (200, 200))

            command_text = Text(
                "Movements: WASD or keypad arrows",
                Color.RED.value, 500, 150, Size.TEXT.value)
            command_text.show_text(self.screen)

            surface1 = rules_font.render("To complete a level,"
                                         " all the gums must be eaten.",
                                         False, Color.RED.value)
            rect = surface1.get_rect(center=(550, 700))
            self.screen.blit(surface1, rect)

            surface2 = rules_font.render("Beware of the ghost"
                                         " for they will try to eat you.",
                                         False, Color.RED.value)
            rect = surface2.get_rect(center=(550, 750))
            self.screen.blit(surface2, rect)

            surface3 = rules_font.render("If your time runs out or if "
                                         "you lose the lives you are given,",
                                         False, Color.RED.value)
            rect = surface3.get_rect(center=(550, 800))
            self.screen.blit(surface3, rect)

            surface4 = rules_font.render("failure in your trial"
                                         " will awaits you.",
                                         False, Color.RED.value)
            rect = surface4.get_rect(center=(550, 850))
            self.screen.blit(surface4, rect)

            cheat_screen = Text(
                "Press C for the cheat screen",
                Color.RED.value, 2100, 150, Size.TEXT.value)
            cheat_screen.show_text(self.screen)

            win_lose = Text(
                "Press 1 to win or 2 to lose",
                Color.RED.value, 2100, 350, Size.TEXT.value
                )
            win_lose.show_text(self.screen)

            skip_level = Text(
                "Press n to skip to the next level",
                Color.RED.value, 2100, 550, Size.TEXT.value
                )
            skip_level.show_text(self.screen)

            pg.display.flip()

    def init_highscore(self) -> None:
        """Init the menu that display the highscore"""
        running: bool = True
        config: Any = parsing()
        count: int = 0
        start_y: int = 250
        display_score: str = ""
        list_highscore: list[str] = []
        list_text_highscore: list[Any] = []
        isdone: bool = False

        try:
            with open(config.highscore_filename, "r") as file:
                data = json.load(file)
                for keys, values in data.items():
                    count += 1
                    display_score += str(count) + ". " + values[1] + ": "
                    display_score += str(values[0]) + " points"
                    list_highscore.append(display_score)
                    display_score = ""

        except (FileNotFoundError, json.JSONDecodeError):
            print("Invalid Highscore data. It Could not be retrieved")
        while running:
            self.screen.fill(Color.BLACK.value)

            command_text = Text(
                "Highscores: ", Color.RED.value, 500, 150, Size.TITLE.value)
            command_text.show_text(self.screen)
            if not isdone:
                for index in range(len(list_highscore)):
                    show_score = Text(
                        list_highscore[index],
                        Color.RED.value, 500, start_y, Size.TEXT.value
                        )
                    start_y += 100
                    list_text_highscore.append(show_score)
                isdone = True

            for args in list_text_highscore:
                args.show_text(self.screen)

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                keys = pg.key.get_pressed()
                if keys[pg.K_ESCAPE]:
                    running = False

            pg.display.flip()

    def resume_game(self) -> None:
        """Go back to the current game when the resume button is clicked"""
        self.running = False
