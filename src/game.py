import pygame as pg
import pygvideo as pv
from src.parsing import parsing
from src.helper import Color, Box_Button, Font, Size, Text
from src.score import Score, ranking_score, valid_highscore
import json
from typing import Any
import sys
import logging


class Game:
    """Class for the pacman game"""
    def __init__(self, screen, screen_width, screen_height):
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.score: int = 0
        self.config = parsing()
        self.lives: int = self.config.lives
        self.max_time: int = self.config.lvl_max_time
        logging.basicConfig(filename="error.logs", filemode="a",
                            format="%(asctime)s - %(message)s",
                            datefmt='%m/%d/%Y %I:%M:%S %p')

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
                    list_cheat = self.cheat_screen()
                    print(list_cheat)
                if keys[pg.K_1]:
                    self.win()
                if keys[pg.K_2]:
                    self.game_over()

            display_lives = Text("Lives: " + str(self.lives), Color.RED.value, 500, 500, Size.TEXT.value)
            display_lives.show_text(self.screen)

            pg.display.flip()

        # need to do timer, levels, lives
        # display if cheat on or not
        # render maze, pacgum, pacman and ghost

    def game_over(self):
        """Game over screen"""
        from src.main_menu import MainMenu
        running: bool = True
        letter: str = ""
        no_loop: bool = False
        count: int = 0
        score_dict: dict[str, int] = {}
        lock = pg.image.load("assets/lock_test.jpg")
        islocked: bool = False

        video = pv.Video("assets/cat_laugh.mp4")
        video.set_size((400, 400))
        video.preplay(-1)

        while running:
            mouse = pg.mouse.get_pos()
            self.screen.fill(Color.BLACK.value)

            menu_button = Box_Button(self.screen_width / 2, self.screen_height / 2 + 200, 100, 100, "Go to Menu", Size.TEXT.value)
            menu_button.create_button(self.screen, mouse)

            for event in pg.event.get():
                keys = pg.key.get_pressed()
                if keys[pg.K_ESCAPE]:
                    pg.quit()
                    sys.exit()
                if event.type == pg.KEYDOWN:
                    video.handle_event(event)
                    if len(letter) < 10 and not keys[pg.K_BACKSPACE]:
                        if event.unicode.isalpha():
                            letter += event.unicode
                    if keys[pg.K_BACKSPACE]:
                        letter = letter[:-1]
                    if keys[pg.K_SPACE] and count == 0:
                        count += 1
                        no_loop = True
                        islocked = True
                if event.type == pg.MOUSEBUTTONDOWN:
                    if menu_button.rect.collidepoint(mouse):
                        menu = MainMenu(self.screen, self.screen_height, self.screen_width)
                        pv.quit_all()
                        menu.init_menu(True)

            video.draw_and_update(self.screen, (self.screen_width / 2 + 400, self.screen_height / 2))


            input_name = Box_Button(self.screen_width / 2, self.screen_height / 2, 100, 100, letter, Size.TEXT.value)
            input_name.create_button(self.screen, mouse)

            title_win = Text("LOSER !!!", Color.WHITE.value, self.screen_width / 2, self.screen_height / 2 - 400, Size.TITLE.value)
            title_win.show_text(self.screen)

            name_rules = Text("Enter your name: ", Color.RED.value, self.screen_width / 2, self.screen_height / 2 - 100, Size.TEXT.value)
            name_rules.show_text(self.screen)

            confirm_text = Text("Press Space to confirm", Color.WHITE.value, self.screen_width / 2, self.screen_height / 2 + 300, Size.TEXT.value)
            confirm_text.show_text(self.screen)

            if no_loop:
                name = letter

                highscore = valid_highscore(name, self.score)
                json_list = [highscore.player_score, highscore.player_name]
                try:
                    with open(self.config.highscore_filename, "r") as file:
                        data = json.load(file)
                        ranked = ranking_score(self.score, data, json_list)

                    with open(self.config.highscore_filename, "w") as file:
                        json.dump(ranked, file, indent=4)

                except (FileExistsError, FileNotFoundError, json.JSONDecodeError):
                    with open(self.config.highscore_filename, "w") as file:
                        score_dict.update({"0": json_list})
                        json.dump(score_dict, file, indent=4)
                finally:
                    no_loop = False

            if islocked:
                self.screen.blit(lock, (self.screen_width / 2 - 50, self.screen_height / 2 + 320))

            pg.display.flip()

    def win(self):
        """Win screen"""
        from src.main_menu import MainMenu
        running: bool = True
        letter: str = ""
        no_loop: bool = False
        count: int = 0
        score_dict: dict[str, int] = {}
        lock = pg.image.load("assets/lock_test.jpg")
        islocked: bool = False
        video = pv.Video("assets/penguin.mp4")
        video.set_size((400, 400))
        video.preplay(-1)

        while running:
            mouse = pg.mouse.get_pos()
            self.screen.fill(Color.BLACK.value)

            for event in pg.event.get():
                video.handle_event(event)
                keys = pg.key.get_pressed()
                if keys[pg.K_ESCAPE]:
                    pg.quit()
                    sys.exit()
                if event.type == pg.KEYDOWN:
                    if len(letter) < 10 and not keys[pg.K_BACKSPACE]:
                        if event.unicode.isalpha():
                            letter += event.unicode
                    if keys[pg.K_BACKSPACE]:
                        letter = letter[:-1]
                    if keys[pg.K_SPACE] and count == 0:
                        count += 1
                        no_loop = True
                        islocked = True
                if event.type == pg.MOUSEBUTTONDOWN:
                    if menu_button.rect.collidepoint(mouse):
                        menu = MainMenu(self.screen, self.screen_height, self.screen_width)
                        pv.quit_all()
                        menu.init_menu(True)
            video.draw_and_update(self.screen, (self.screen_width / 2 + 400, self.screen_height / 2))

            input_name = Box_Button(self.screen_width / 2, self.screen_height / 2, 100, 100, letter, Size.TEXT.value)
            input_name.create_button(self.screen, mouse)

            title_win = Text("You Win !", Color.WHITE.value, self.screen_width / 2, self.screen_height / 2 - 400, Size.TITLE.value)
            title_win.show_text(self.screen)

            name_rules = Text("Enter your name: ", Color.RED.value, self.screen_width / 2, self.screen_height / 2 - 100, Size.TEXT.value)
            name_rules.show_text(self.screen)

            menu_button = Box_Button(self.screen_width / 2, self.screen_height / 2 + 200, 100, 100, "Go to Menu", Size.TEXT.value)
            menu_button.create_button(self.screen, mouse)

            confirm_text = Text("Press Space to confirm", Color.WHITE.value, self.screen_width / 2, self.screen_height / 2 + 300, Size.TEXT.value)
            confirm_text.show_text(self.screen)

            if no_loop:
                name = letter

                highscore = valid_highscore(name, self.score)
                json_list = [highscore.player_score, highscore.player_name]
                try:
                    with open(self.config.highscore_filename, "r") as file:
                        data = json.load(file)
                        ranked = ranking_score(self.score, data, json_list)

                    with open(self.config.highscore_filename, "w") as file:
                        json.dump(ranked, file, indent=4)

                except (FileExistsError, FileNotFoundError, json.JSONDecodeError):
                    with open(self.config.highscore_filename, "w") as file:
                        score_dict.update({"0": json_list})
                        json.dump(score_dict, file, indent=4)
                finally:
                    no_loop = False
            if islocked:
                self.screen.blit(lock, (self.screen_width / 2 - 50, self.screen_height / 2 + 320))

            pg.display.flip()

    def pause_menu(self):
        """Pause Menu"""
        from src.main_menu import MainMenu
        running: bool = True
        no_resume: bool = True
        width_button: int = 100
        height_button: int = 100
        size_text: int = Size.TEXT.value
        menu = MainMenu(self.screen, self.screen_height, self.screen_width)

        video = pv.Video("assets/wizard.mp4")
        video.set_size((400, 400))
        video.preplay(-1)

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

            title_menu = Text("Pause Menu", Color.WHITE.value, self.screen_width / 2, self.screen_height / 2 - 500, Size.TITLE.value)
            title_menu.show_text(self.screen)

            video.draw_and_update(self.screen, (self.screen_width / 2 + 400, self.screen_height / 2))

            for event in pg.event.get():
                video.handle_event(event)
                keys = pg.key.get_pressed()
                if keys[pg.K_ESCAPE]:
                    pg.quit()
                    sys.exit()
                if event.type == pg.MOUSEBUTTONDOWN:
                    if exit_button.rect.collidepoint(mouse):
                        pg.quit()
                        sys.exit()
                    if resume_button.rect.collidepoint(mouse):
                        pv.quit_all()
                        running = False
                    if menu_button.rect.collidepoint(mouse):
                        no_resume = False
                        pv.quit_all()
                        menu.init_menu(no_resume)
                    if instructions_button.rect.collidepoint(mouse):
                        pv.quit_all()
                        menu.init_tuto()

            pg.display.flip()

    def cheat_screen(self):
        """Menu to activate/deactivate the cheat"""
        running: bool = True
        width_button: int = 100
        height_button: int = 100
        size_text: int = Size.TEXT.value
        list_cheat: list[bool] = []
        speed: bool = False
        invincible: bool = False
        no_collision: bool = False

        video = pv.Video("assets/no_brain.mp4")
        video.set_size((400, 400))
        video.preplay(-1)

        while running:
            self.screen.fill(Color.BLACK.value)
            mouse = pg.mouse.get_pos()

            speed_button = Box_Button(self.screen_width / 2, self.screen_height / 2 + 300, width_button, height_button, "Speeeeeed", size_text)
            speed_button.create_button(self.screen, mouse)

            invincible_button = Box_Button(self.screen_width / 2, self.screen_height / 2, width_button, height_button, "I am <Title Card>", size_text)
            invincible_button.create_button(self.screen, mouse)

            no_collision_button = Box_Button(self.screen_width / 2, self.screen_height / 2 - 300, width_button, height_button, "Ghost is Ghost !", size_text)
            no_collision_button.create_button(self.screen, mouse)

            title_menu = Text("Cheat Menu", Color.WHITE.value, self.screen_width / 2, self.screen_height / 2 - 600, Size.TITLE.value)
            title_menu.show_text(self.screen)

            video.draw_and_update(self.screen, (self.screen_width / 2 + 400, self.screen_height / 2))

            for event in pg.event.get():
                video.handle_event(event)
                keys = pg.key.get_pressed()
                if keys[pg.K_ESCAPE]:
                    pv.quit_all()
                    running = False
                if event.type == pg.MOUSEBUTTONDOWN:
                    if speed_button.rect.collidepoint(mouse):
                        speed = True
                        list_cheat.append(speed)
                    if invincible_button.rect.collidepoint(mouse):
                        invincible = True
                        list_cheat.append(invincible)
                    if no_collision_button.rect.collidepoint(mouse):
                        no_collision = True
                        list_cheat.append(no_collision)

            pg.display.flip()

        return list_cheat

# Need to see if the win and game over function can't be done outside of the class, same for pause menu
# see if there is a need to create cursor for the button of the menu or not (with pygame.cursor probably)