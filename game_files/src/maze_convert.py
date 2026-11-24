from game_files.src.maze import Maze, MazeError


def convert_from_hexa(rows: list[str]) -> list[list[int]]:
    """Converts the maze written in hexadecimal from A-maze-ing
    into a matrix, each cell is the bit value of the walls it has"""
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


def level_maze(height: int, width: int, seed: int) -> Maze:
    """Transform the maze obtained through the
    mazegenerator into a usable maze for Pac-man"""
    try:
        from game_files.mazegenerator.mazegenerator import MazeGenerator
    except ImportError as err:
        raise MazeError("The A-Maze-ing package is not installed "
                        " use: pip install mazegen-*.whl") from err
    maze = MazeGenerator(
        (height, width), perfect=False, entry_cell=(0, 0),
        exit_cell=(width - 1, height - 1), seed=seed
        )
    maze.generate()
    # rows: list[str] = maze.maze_hexa()
    return Maze(maze._maze)
    # try:
    #     walls= convert_from_hexa(rows)

    #     if len(walls) != height or any(len(row) != width for row in walls):
    #         raise MazeError(
    #             "The maze given by the generator hasn't the right size")
    #     return Maze(maze)
    # except MazeError:
    #     raise
    # except Exception as err:
    #     raise MazeError(
    #         f"An error occured during the maze generation"
    #         f" ({type(err).__name__}): {err}"
    #         )
