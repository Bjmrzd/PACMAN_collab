import os
import pygame as pg
from game_files.src.main_menu import MainMenu
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"


def main() -> None:
    """Main function to init everything and start the menu"""
    pg.init()

    size: list[tuple[int, int]] = pg.display.get_desktop_sizes()
    screen_height: int = int(size[0][1])
    screen_width: int = int(size[0][0])
    screen = pg.display.set_mode((screen_width, screen_height))
    no_resume: bool = True
    menu: MainMenu = MainMenu(screen, screen_height, screen_width)
    menu.init_menu(no_resume)


if __name__ == "__main__":
    main()
