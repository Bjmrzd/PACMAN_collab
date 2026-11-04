import pygame as pg
from src.entities import Ghost, State, Personnality
from src.helper import Font, Color
from src.maze import Maze, Direction


def render_maze(walls : list[list[int]]):
    print(walls)
