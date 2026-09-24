import pygame as pg
from src.main_menu import MainMenu
from src.game import Game


def main():
    pg.init()

    size = pg.display.get_desktop_sizes()
    screen_height = int(size[0][1])
    screen_width = int(size[0][0])
    screen = pg.display.set_mode(screen_width, screen_height)
    # pg.display.set_caption("Pacman")
    # icon = pg.image.load("assets/pacman.png")
    # title = pg.image.load("assets/title.jpg")
    # pac = pg.image.load("assets/pac.jpg")
    # ghost = pg.image.load("assets/ghosts.png")
    # pg.display.set_icon(icon)
    font = pg.font.Font("assets/ByteBounce.ttf", 40)
    menu = MainMenu(screen, screen_height, screen_width)
    menu.init_menu()


if __name__ == "__main__":
    main()
