import pygame as pg
import pygvideo as pv
from src.parsing import parsing, Config
from src.helper import Color, Box_Button, Font, Size, Text
from src.highscore import ranking_score, valid_highscore
from src.renderer import render_maze
from src.maze import Maze, Direction
from src.level import Level, LevelState
from src.scoring import GameState, ScoringRules
from src.maze_convert import generate_hex_maze
from src.entities import PacMan
import json
from typing import Any
import sys
import random
import logging


class Game:
    """Class for the pacman game"""
    def __init__(self, screen, screen_width, screen_height) -> None:
        self.fps: int = 60

        self.screen = screen

        self.screen_width = screen_width

        self.screen_height = screen_height

        self.score: int = 0

        self.config: Config = parsing()

        self.lives: int = self.config.lives

        self.max_time: int = 0

        self.rng = random.Random(self.config.seed)

        logging.basicConfig(filename="error.logs", filemode="a",
                            format="%(asctime)s - %(message)s",
                            datefmt='%m/%d/%Y %I:%M:%S %p')

        self.level_list: list[Any] = [
            self.config.level_1,
            self.config.level_2,
            self.config.level_3,
            self.config.level_4,
            self.config.level_5,
            self.config.level_6,
            self.config.level_7,
            self.config.level_8,
            self.config.level_9,
            self.config.level_10,
        ]

        self.keys: dict[int, Direction] = {
                    pg.K_UP: Direction.North,
                    pg.K_w: Direction.North,
                    pg.K_RIGHT: Direction.East,
                    pg.K_d: Direction.East,
                    pg.K_DOWN: Direction.South,
                    pg.K_s: Direction.South,
                    pg.K_LEFT: Direction.West,
                    pg.K_a: Direction.West
                     }

        self.is_paused: bool = True

        self.cheat_speed: bool = False

        self.cheat_invincible: bool = False

        self.cheat_time: bool = False

    def main_loop(self) -> None:
        """Switch level and call the main loop for each of them"""

        rules = ScoringRules(
            self.config.pacgum_pts,
            self.config.super_pacgum_pts, self.config.ghost_pts
            )

        state = GameState(self.lives, rules)

        timer = pg.time.Clock()

        nb_levels: int = len(self.level_list)

        for n in range(1, nb_levels + 1):
            level_state = self.play_level(n, state, timer)

            if level_state is None:
                return

            self.score = state.score

            if level_state is LevelState.GAME_OVER:
                self.game_over()
                return

            state.lives = self.lives

        self.win()
        return

    def play_level(
            self, level_number: int, state: GameState, timer: pg.time.Clock
            ) -> LevelState | None:
        """Handle the main logic of the game loop"""
        index: int = 0

        resume_freeze: float = 2.0
        restart_pause: float = resume_freeze

        maze: list[str] = generate_hex_maze(
            self.level_list[level_number - 1].get("height"),
            self.level_list[level_number - 1].get("width"), self.config.seed
            )
        maze_class: Maze = Maze(maze)

        sprites_grp = pg.sprite.Group()

        updated: bool = False
        self.max_time = abs((maze_class.width*maze_class.height / 5) * 2.5)
        # 5 being the speed of the PacMan,
        #  if we change the speed we have to change the value

        level: Level = Level(
            maze_class, state, level_number,
            self.max_time, self.rng, PacMan(maze_class, maze_class.center)
            )
        level.level_state = LevelState.READY
        pac = level.pac_man
        start_text = Text("Press any key to start", Color.WHITE.value, self.screen_width // 2, self.screen_height // 3, Size.TEXT.value * 2)

        dt = 0.0

        sprite_timer = pg.USEREVENT

        pg.time.set_timer(sprite_timer, 20)

        sprites_grp.add(pac)

        ghost_grp = pg.sprite.Group()

        for ghost in level.ghosts:
            ghost_grp.add(ghost)

        while (
            level.level_state in (LevelState.READY, LevelState.PLAYING, LevelState.PAUSE)
             ):
            countdown_font = pg.font.Font(Font.FONT1.value, 400)
            self.screen.fill(Color.BLACK.value)

            dict_gum: dict[str, Any] = render_maze(
                maze_class.walls, maze_class, self.screen,
                self.screen_width, self.screen_height, pac, index, level
                )

            if level.level_state is LevelState.PLAYING:
                dt = timer.tick(self.fps) / 1000
            elif level.level_state is LevelState.READY:
                timer.tick(self.fps)
                dt = 0.0
            elif not self.is_paused:
                dt = timer.tick(self.fps) / 1000
                restart_pause -= dt
                if restart_pause <= 0.0:
                    level.level_state = LevelState.PLAYING
                    self.is_paused = True
                    restart_pause = resume_freeze
                    dt = 0.0

            if index < 1:
                level.pacgum = dict_gum
            else:
                dict_gum = level.pacgum
            index += 1

            for event in pg.event.get():
                if event.type == sprite_timer:
                    updated = True
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == pg.KEYDOWN:
                    if (level.level_state is LevelState.READY and event.key not in (pg.K_ESCAPE, pg.K_c)):
                        level.level_state = LevelState.PLAYING
                    if event.key == pg.K_ESCAPE:
                        level.level_state = LevelState.PAUSE
                        self.is_paused = self.pause_menu()
                        restart_pause = resume_freeze
                        timer.tick()
                        pg.event.clear()
                        break
                    if event.key == pg.K_c:
                        level.level_state = LevelState.PAUSE
                        self.cheat_screen()
                        restart_pause = resume_freeze
                        timer.tick()
                        pg.event.clear()
                        break
                    if event.key == pg.K_1:
                        self.score = state.score
                        self.win()
                        return None
                    if event.key == pg.K_2:
                        self.score = state.score
                        self.game_over()
                        return None
                    if event.key == pg.K_n:
                        level.level_state = LevelState.WON
                    elif event.key in self.keys:
                        level.pac_man.move(self.keys[event.key], updated)

            pressed = pg.key.get_pressed()
            for key, direction in self.keys.items():
                if pressed[key]:
                    pac.move(direction, updated)

            if level.level_state is LevelState.PLAYING:
                level.update(dt)
                level.pacman_reach_cell(pac, dict_gum)

            if updated:
                updated = False

            accurate_time = round(level.remaining_time, 2)

            display_score = Text(
                "Score: " + str(state.score),
                Color.RED.value, 1500, 40, Size.TEXT.value
                )
            display_score.show_text(self.screen)

            if self.cheat_speed:
                display_speed = Text(
                    "Speed boost", Color.RED.value, 500, 500, Size.TEXT.value)
                display_speed.show_text(self.screen)
                level.cheat_speed = True
            else:
                level.cheat_speed = False

            if self.cheat_invincible:
                display_inv = Text(
                    "Invincible", Color.WHITE.value, 500, 700, Size.TEXT.value)
                display_inv.show_text(self.screen)
                level.cheat_invincible = True
            else:
                level.cheat_invincible = False

            if self.cheat_time:
                display_col = Text(
                    "Time Stop", Color.GREY.value, 500, 900, Size.TEXT.value)
                display_col.show_text(self.screen)
                level.cheat_time = True
            else:
                level.cheat_time = False

            display_lives = Text(
                "Lives: " + str(state.lives),
                Color.RED.value, 800, 40, Size.TEXT.value
                )
            display_lives.show_text(self.screen)

            display_time = Text(
                "Timer: " + str(accurate_time),
                Color.RED.value, 1800, 40, Size.TEXT.value
                )
            display_time.show_text(self.screen)

            display_level = Text(
                "Level " + str(level_number),
                Color.RED.value, 1150, 40, Size.TITLE.value
                )
            display_level.show_text(self.screen)

            sprites_grp.draw(self.screen)
            dict_gum.get("sprite").draw(self.screen)
            dict_gum.get("super").draw(self.screen)
            ghost_grp.draw(self.screen)

            if level.level_state is LevelState.PAUSE and not self.is_paused:
                digit = str(int(restart_pause) + 1)
                surface = countdown_font.render(
                    digit, False, Color.WHITE.value)
                rect = surface.get_rect(
                    center=(self.screen_width // 2, self.screen_height // 2))
                self.screen.blit(surface, rect)

            if level.level_state is LevelState.READY:
                start_text.show_text(self.screen)
            pg.display.flip()

        self.cheat_speed = False
        self.cheat_time = False
        self.cheat_invincible = False

        return level.level_state

    def game_over(self) -> None:
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

            menu_button = Box_Button(
                self.screen_width / 2, self.screen_height / 2 + 200, 100, 100,
                "Go to Menu", Size.TEXT.value)
            menu_button.create_button(self.screen, mouse)

            for event in pg.event.get():
                keys = pg.key.get_pressed()
                if keys[pg.K_ESCAPE]:
                    pg.quit()
                    sys.exit()
                if keys[pg.K_RETURN] and count == 0:
                    count += 1
                    no_loop = True
                    islocked = True
                if not no_loop and count >= 1:
                    menu = MainMenu(
                        self.screen, self.screen_height, self.screen_width)
                    pv.quit_all()
                    menu.init_menu(True)
                if event.type == pg.KEYDOWN:
                    # video.handle_event(event)
                    if len(letter) < 10 and not keys[pg.K_BACKSPACE]:
                        if (event.unicode.isalpha() or event.unicode.isspace()) and not event.unicode == "\r":
                            letter += event.unicode

                    if keys[pg.K_BACKSPACE]:
                        letter = letter[:-1]
                if event.type == pg.MOUSEBUTTONDOWN:
                    if menu_button.rect.collidepoint(mouse):
                        menu = MainMenu(
                            self.screen, self.screen_height, self.screen_width)
                        pv.quit_all()
                        menu.init_menu(True)

            video.draw_and_update(
                self.screen,
                (self.screen_width / 2 + 400, self.screen_height / 2)
                )

            input_name = Box_Button(
                self.screen_width / 2,
                self.screen_height / 2, 100, 100, letter, Size.TEXT.value
                )
            input_name.create_button(self.screen, mouse)

            title_win = Text(
                "LOSER !!!", Color.WHITE.value,
                self.screen_width / 2,
                self.screen_height / 2 - 400, Size.TITLE.value
                )
            title_win.show_text(self.screen)

            name_rules = Text(
                "Enter your name: ", Color.RED.value, self.screen_width / 2,
                self.screen_height / 2 - 100, Size.TEXT.value)
            name_rules.show_text(self.screen)

            confirm_text = Text(
                "Press Space to confirm", Color.WHITE.value,
                self.screen_width / 2,
                self.screen_height / 2 + 300, Size.TEXT.value)
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

                except (
                    FileExistsError, FileNotFoundError, json.JSONDecodeError
                      ):
                    with open(self.config.highscore_filename, "w") as file:
                        score_dict.update({"0": json_list})
                        json.dump(score_dict, file, indent=4)
                finally:
                    no_loop = False

            if islocked:
                self.screen.blit(
                    lock,
                    (self.screen_width / 2 - 50, self.screen_height / 2 + 320)
                    )

            pg.display.flip()

    def win(self) -> None:
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

            menu_button = Box_Button(
                self.screen_width / 2, self.screen_height / 2 + 200, 100, 100,
                "Go to Menu", Size.TEXT.value
                )
            menu_button.create_button(self.screen, mouse)

            for event in pg.event.get():
                # video.handle_event(event)
                keys = pg.key.get_pressed()
                if keys[pg.K_ESCAPE]:
                    pg.quit()
                    sys.exit()
                if keys[pg.K_RETURN] and count == 0:
                    count += 1
                    no_loop = True
                    islocked = True
                if not no_loop and count >= 1:
                    menu = MainMenu(
                        self.screen, self.screen_height, self.screen_width)
                    pv.quit_all()
                    menu.init_menu(True)

                if event.type == pg.KEYDOWN:
                    if len(letter) < 10 and not keys[pg.K_BACKSPACE]:
                        if (
                            (
                                event.unicode.isalpha()
                                or event.unicode.isspace()
                                ) and not event.unicode == "\r"
                           ):
                            letter += event.unicode
                    if keys[pg.K_BACKSPACE]:
                        letter = letter[:-1]

                if event.type == pg.MOUSEBUTTONDOWN:
                    if menu_button.rect.collidepoint(mouse):
                        menu = MainMenu(
                            self.screen, self.screen_height, self.screen_width)
                        pv.quit_all()
                        menu.init_menu(True)
            video.draw_and_update(
                self.screen,
                (self.screen_width / 2 + 400, self.screen_height / 2)
                )

            input_name = Box_Button(
                self.screen_width / 2, self.screen_height / 2,
                100, 100, letter, Size.TEXT.value)
            input_name.create_button(self.screen, mouse)

            title_win = Text(
                "You Win !", Color.WHITE.value, self.screen_width / 2,
                self.screen_height / 2 - 400, Size.TITLE.value)
            title_win.show_text(self.screen)

            name_rules = Text(
                "Enter your name: ", Color.RED.value, self.screen_width / 2,
                self.screen_height / 2 - 100, Size.TEXT.value)
            name_rules.show_text(self.screen)

            confirm_text = Text(
                "Press Space to confirm", Color.WHITE.value,
                self.screen_width / 2,
                self.screen_height / 2 + 300, Size.TEXT.value)
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

                except (
                    FileExistsError, FileNotFoundError, json.JSONDecodeError
                       ):
                    with open(self.config.highscore_filename, "w") as file:
                        score_dict.update({"0": json_list})
                        json.dump(score_dict, file, indent=4)
                finally:
                    no_loop = False
            if islocked:
                self.screen.blit(
                    lock,
                    (self.screen_width / 2 - 50, self.screen_height / 2 + 320)
                    )

            pg.display.flip()

    def pause_menu(self) -> bool:
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

            exit_button = Box_Button(
                self.screen_width / 2, self.screen_height / 2 + 400,
                width_button, height_button, "Quit", size_text)
            exit_button.create_button(self.screen, mouse)

            resume_button = Box_Button(
                self.screen_width / 2, self.screen_height / 2 + 100,
                width_button, height_button, "Resume", size_text)
            resume_button.create_button(self.screen, mouse)

            menu_button = Box_Button(
                self.screen_width / 2, self.screen_height / 2 - 50,
                width_button, height_button, "Menu", size_text)
            menu_button.create_button(self.screen, mouse)

            instructions_button = Box_Button(
                self.screen_width / 2, self.screen_height / 2 + 250,
                width_button, height_button, "Instructions", size_text)
            instructions_button.create_button(self.screen, mouse)

            display_enter = Text(
                "Press Enter to resume", Color.WHITE.value,
                self.screen_width / 2,
                self.screen_height / 2 - 200, Size.TEXT.value)
            display_enter.show_text(self.screen)

            title_menu = Text(
                "Pause Menu", Color.WHITE.value, self.screen_width / 2,
                self.screen_height / 2 - 500, Size.TITLE.value)
            title_menu.show_text(self.screen)

            video.draw_and_update(
                self.screen,
                (self.screen_width / 2 + 400, self.screen_height / 2))

            for event in pg.event.get():

                if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                    running = False
                    self.is_paused = False
                    pv.quit_all()

                if event.type == pg.MOUSEBUTTONDOWN:

                    if exit_button.rect.collidepoint(mouse):
                        pv.quit_all()
                        pg.quit()
                        sys.exit()

                    if resume_button.rect.collidepoint(mouse):
                        pv.quit_all()
                        running = False

                    if menu_button.rect.collidepoint(mouse):
                        no_resume = False
                        pv.quit_all()
                        menu.init_menu(no_resume)

                        video = pv.Video("assets/wizard.mp4")
                        video.set_size((400, 400))
                        video.preplay(-1)

                    if instructions_button.rect.collidepoint(mouse):
                        pv.quit_all()
                        menu.init_tuto()

                        video = pv.Video("assets/wizard.mp4")
                        video.set_size((400, 400))
                        video.preplay(-1)

            pg.display.flip()

        return running

    def cheat_screen(self) -> None:
        """Menu to activate/deactivate the cheat"""
        running: bool = True

        width_button: int = 100

        height_button: int = 100

        size_text: int = Size.TEXT.value

        video = pv.Video("assets/no_brain.mp4")
        video.set_size((400, 400))
        video.preplay(-1)

        while running:
            self.screen.fill(Color.BLACK.value)
            mouse = pg.mouse.get_pos()

            speed_button = Box_Button(
                self.screen_width / 2,
                self.screen_height / 2 + 300, width_button,
                height_button, "Speeeeeed", size_text
                )
            speed_button.create_button(self.screen, mouse)

            if self.cheat_speed:
                active_text = Text(
                    "Active", Color.WHITE.value, self.screen_width / 2 - 500,
                    self.screen_height / 2 + 300, Size.TITLE.value)
                active_text.show_text(self.screen)

            invincible_button = Box_Button(
                self.screen_width / 2, self.screen_height / 2,
                width_button, height_button, "I am <Title Card>", size_text)
            invincible_button.create_button(self.screen, mouse)

            if self.cheat_invincible:
                inv_text = Text(
                    "Active", Color.WHITE.value, self.screen_width / 2 - 500,
                    self.screen_height / 2, Size.TITLE.value)
                inv_text.show_text(self.screen)

            no_time_button = Box_Button(
                self.screen_width / 2, self.screen_height / 2 - 300,
                width_button, height_button, "Stop Time", size_text)
            no_time_button.create_button(self.screen, mouse)

            if self.cheat_time:
                time_text = Text(
                    "Active", Color.WHITE.value, self.screen_width / 2 - 500,
                    self.screen_height / 2 - 300, Size.TITLE.value)
                time_text.show_text(self.screen)

            title_menu = Text(
                "Cheat Menu", Color.WHITE.value,
                self.screen_width / 2,
                self.screen_height / 2 - 600, Size.TITLE.value)
            title_menu.show_text(self.screen)

            video.draw_and_update(
                self.screen,
                (self.screen_width / 2 + 400, self.screen_height / 2))

            for event in pg.event.get():

                keys = pg.key.get_pressed()

                if keys[pg.K_ESCAPE]:
                    running = False
                    self.is_paused = False
                    pv.quit_all()
                if event.type == pg.MOUSEBUTTONDOWN:

                    if speed_button.rect.collidepoint(mouse):
                        if self.cheat_speed is True:
                            self.cheat_speed = False
                        else:
                            self.cheat_speed = True

                    if invincible_button.rect.collidepoint(mouse):
                        if self.cheat_invincible is True:
                            self.cheat_invincible = False
                        else:
                            self.cheat_invincible = True

                    if no_time_button.rect.collidepoint(mouse):
                        if self.cheat_time is True:
                            self.cheat_time = False
                        else:
                            self.cheat_time = True

            pg.display.flip()
