from src.maze import Maze, MazeError
import numpy as np

def convert_from_hexa(rows: list[str]) -> list[list[int]]:
    try:
        walls: list[list[int]] = []
        for row in rows:
            line: list[int] = []
            for char in row.strip():
                line.append(int(char, 16))
            walls.append(line)
        return walls
    except ValueError as err:
        raise MazeError(f"Invalid conversion: {err}") from err


def generate_hex_maze(height: int, width: int, seed: int | None) -> list[str]:

    try:
        from mazegenerator.mazegenerator import MazeGenerator
    except ImportError as err:
        raise MazeError("The A-Maze-ing package is not installed "
                        " use: pip install mazegen-*.whl") from err
    # maze = MazeGenerator(height=height, width=width, entry=(0,0), exit=(width -1, height -1), isperfect=False, seed=seed)
    maze = MazeGenerator((height, width), perfect=False, entry_cell=(0,0), exit_cell=(width -1, height -1), seed=seed)
    maze.generate()
    # rows: list[str] = maze.maze_hexa()
    # return rows
    return maze._maze


def level_maze(height: int, width: int, seed: int | None) -> Maze:
    try:
        walls = convert_from_hexa(generate_hex_maze(height, width, seed))
        if len(walls) != height or any(len(row) != width for row in walls):
            raise MazeError("The maze given by the generator hasn't the right size")
        return Maze(walls)
    except MazeError:
        raise
    except Exception as err:
        raise MazeError(f"An error occured during the maze generation ({type(err).__name__}): {err}")