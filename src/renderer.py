import pygame as pg
from src.entities import Ghost, State, Personnality, PacMan
from src.helper import Font, Color
from src.maze import Maze, Direction, WALL_BITS
from typing import Any
from src.entities import Pacgum, Super_gum


def render_maze(walls: list[list[int]], maze: Maze, screen: Any, screen_width: int, screen_height: int, pacman: PacMan, index: int, level) -> dict[str, Any]:
    list_cell: list[Any] = []
    # index: int = 0
    # start_x: int = 50
    # start_y: int = 50
    space: int = 50
    middle_x: int = (screen_width - len(walls[0]) * space) // 2
    middle_y: int = (screen_height - len(walls) * space) // 2
    iseven: bool = True
    gum_grp = pg.sprite.Group()
    supergum_grp = pg.sprite.Group()
    base_state = State.EDIBLE
    list_gum: list[Any] = []
    super_list: list[Any] = []
    if maze.spawn[0] % 2 == 0 and maze.spawn[1] % 2 == 0 and index < 1:
        # print(maze.spawn[0], maze.spawn[1])
        iseven = True
    elif not maze.spawn[0] % 2 == 0 and not maze.spawn[1] % 2 == 0 and index < 1:
        maze.spawn = (maze.spawn[0] - 1, maze.spawn[1] - 1)
    direction: dict[str | int] = {
        "top": 1,
        "bottom": 4,
        "left": 8,
        "right": 2,
    }
    # pacman_pos: (0, 0)
    # print(maze.width, maze.height)
    for rows in range(len(walls)):
        for cols in range(len(walls[0])):
            cell = walls[rows][cols]
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

            if maze.spawn == (cols, rows) and index < 1 and not iseven:
                pacman.rect.center = (start_x + 25, start_y + 25)

            if maze.spawn == (cols, rows) and index < 1 and iseven:
                pacman.rect.center = (start_x + 25, start_y + 25)

            if rows <= len(walls) and cols <= len(walls[0]) and maze.is_init is False:
                if cell != 15:
                    if (rows, cols) != (0, 0) and (rows, cols) != (len(walls) - 1, len(walls[0]) - 1) and (rows, cols) != (len(walls) - 1, 0) and (rows, cols) != (0, len(walls[0]) - 1):
                        gum = Pacgum(cell, base_state)
                        gum.rect.center = (start_x + 25, start_y + 25)
                        gum_grp.add(gum)
                        list_gum.append(gum)
                    else:
                        supergum = Super_gum(cell, base_state)
                        supergum.rect.center = (start_x + 25, start_y + 25)
                        supergum_grp.add(supergum)
                        super_list.append(supergum)

            if rows == len(walls) and cols == len(walls[0]):
                maze.is_init = True

    row, col = pacman.position
    pacman.rect.center = (int(middle_x + (col + 0.5) * space), int(middle_y + (row + 0.5) * space))

    for ghost in level.ghosts:
        row, col = ghost.position
        ghost.rect.center = (int(middle_x + (col + 0.5) * space), int(middle_y + (row + 0.5) * space))

    return {"sprite": gum_grp, "entities": list_gum, "super": supergum_grp, "super_list": super_list}

