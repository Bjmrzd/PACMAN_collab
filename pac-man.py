import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame as pg
from src.main_menu import MainMenu
from src.game import Game


def main():
    """Main function to init everything and start the menu"""
    pg.init()

    size = pg.display.get_desktop_sizes()
    screen_height = int(size[0][1])
    screen_width = int(size[0][0])
    screen = pg.display.set_mode((screen_width, screen_height))
    no_resume: bool = True
    font = pg.font.Font("assets/ByteBounce.ttf", 40)
    menu = MainMenu(screen, screen_height, screen_width)
    menu.init_menu(no_resume)


if __name__ == "__main__":
    main()
