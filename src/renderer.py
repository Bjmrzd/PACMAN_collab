import pygame as pg
from src.entities import Ghost, State, Personnality
from src.helper import Font, Color
from src.maze import Maze, Direction, WALL_BITS
from typing import Any

def render_maze(walls : list[list[int]], maze: Maze, screen):
    list_cell: list[Any] = []
    index: int = 0
    start_x: int = 50
    start_y: int = 50
    space: int = 50
    direction: dict[str | int] = {
        "top": 1,
        "bottom": 4,
        "left": 8,
        "right": 2,
    }
    for rows in range(len(walls)):
        for cols in range(len(walls[index])):
            cell = walls[rows][cols]
            list_cell.append(cell)

            start_x = cols * space
            start_y = rows * space

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
        index += 1
