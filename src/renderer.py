import pygame as pg
from src.entities import Ghost, State, Personnality
from src.helper import Font, Color
from src.maze import Maze, Direction, WALL_BITS
from typing import Any

def render_maze(walls : list[list[int]], maze: Maze, screen, screen_width, screen_height, pacman):
    list_cell: list[Any] = []
    index: int = 0
    # start_x: int = 50
    # start_y: int = 50
    space: int = 50
    middle_x: int = (screen_width - len(walls[0]) * space) // 2
    middle_y: int = (screen_height - len(walls) * space) // 2
    direction: dict[str | int] = {
        "top": 1,
        "bottom": 4,
        "left": 8,
        "right": 2,
    }
    # print(maze.width, maze.height)

    for rows in range(len(walls)):
        for cols in range(len(walls[0])):
            cell = walls[rows][cols]
            print(rows, cols)
            list_cell.append(cell)

            start_x = middle_x + cols * space
            start_y = middle_y + rows * space

            end_x = start_x + space
            end_y = start_y + space

            if (cell & direction["top"]):
                pg.draw.line(screen, Color.WHITE.value, (start_x, start_y), (end_x , start_y), 5)
            if (cell & direction["bottom"]):
                pg.draw.line(screen, Color.WHITE.value, (start_x, end_y), (end_x, end_y), 5)
            if (cell & direction["left"]):
                pg.draw.line(screen, Color.WHITE.value, (start_x, start_y ), (start_x, end_y), 5)
            if (cell & direction["right"]):
                pg.draw.line(screen, Color.WHITE.value, (end_x, start_y), (end_x, end_y), 5)

            # if maze.spawn == (cols, rows):
            if cols == 5 and rows == 5:
                # print(start_x, start_y) # + 50 each movement
                pacman.rect.center = (start_x, start_y)

            if cols == 5 and rows == 5:
                # print("test")
                pg.draw.circle(screen, Color.RED.value, (start_x, start_y), 5.0)



