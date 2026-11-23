from src.maze import Maze, MazeError


def convert_from_hexa(rows: list[list[int]]) -> list[list[int]]:
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


def generate_hex_maze(height: int, width: int, seed: int) -> list[list[int]]:

    try:
        from mazegenerator.mazegenerator import MazeGenerator
    except ImportError as err:
        raise MazeError("The A-Maze-ing package is not installed "
                        " use: pip install mazegen-*.whl") from err
    maze = MazeGenerator(
        (height, width), perfect=False, entry_cell=(0, 0),
        exit_cell=(width - 1, height - 1), seed=seed
        )
    maze.generate()

    return maze._maze


def level_maze(height: int, width: int, seed: int) -> Maze:
    try:
        walls = convert_from_hexa(generate_hex_maze(height, width, seed))
        if len(walls) != height or any(len(row) != width for row in walls):
            raise MazeError(
                "The maze given by the generator hasn't the right size")
        return Maze(walls)
    except MazeError:
        raise
    except Exception as err:
        raise MazeError(
            f"An error occured during the maze generation"
            f" ({type(err).__name__}): {err}"
            )
