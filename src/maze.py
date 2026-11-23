from enum import Enum
from collections import deque

Cell = tuple[int, int]


class MazeError(Exception):
    def __init__(self, message: str) -> None:
        self.message = message

    def __str__(self) -> str:
        return f"{self.message}"


class Direction(Enum):
    North = (-1, 0)
    East = (0, 1)
    South = (1, 0)
    West = (0, -1)

    @property
    def opposite(self) -> "Direction":
        return Direction((-self.value[0], -self.value[1]))

    @property
    def wall_bit(self) -> int:
        return WALL_BITS[self]


WALL_BITS: dict[Direction, int] = {
        Direction.North: 1,
        Direction.East: 2,
        Direction.South: 4,
        Direction.West: 8,
    }


class Maze:
    def __init__(self, walls: list[list[int]]) -> None:
        self.walls = walls
        self.height = len(walls)
        self.width = len(walls[0])
        self.ghost_corners: list[Cell] = [(0, 0),
                                          (0, self.width - 1),
                                          (self.height - 1, 0),
                                          (self.height - 1, self.width - 1)]
        self.distances: dict[Cell, dict[Cell, int]] = {}
        self.is_init: bool = False
        self.center: Cell | None = self.valid_center()

    def valid_center(self) -> Cell | None:
        """Search for the open cell closest to the center of the maze"""
        """(in case of the center being the 42)"""
        reachable = self.distance_map(self.ghost_corners[0])
        best_cell: Cell | None = None
        best_dist: int = 0
        for cell in sorted(reachable): # type: ignore
            height: int = abs(cell[0] - self.height // 2) # type: ignore
            width: int = abs(cell[1] - self.width // 2) # type: ignore
            dist: int = height + width
            if best_cell is None or dist < best_dist:
                best_cell = cell
                best_dist = dist
        return best_cell

    def in_maze(self, cell: Cell) -> bool:
        row, col = cell
        if row < 0 or row >= self.height:
            return False
        elif col < 0 or col >= self.width:
            return False
        else:
            return True

    def step(self, cell: Cell, direction: Direction) -> Cell:
        dir_row, dir_col = direction.value
        return cell[0] + dir_row, cell[1] + dir_col

    def can_move(self, cell: Cell, direction: Direction) -> bool:
        if not self.in_maze(cell):
            return False
        row, col = cell
        if self.walls[row][col] & direction.wall_bit:
            return False
        target = self.step(cell, direction)
        if not self.in_maze(target):
            return False
        opposite_bit = direction.opposite.wall_bit
        return not (self.walls[target[0]][target[1]] & opposite_bit)

    def valid_directions(self, cell: Cell) -> list[Direction]:
        list_dir = []
        for d in Direction:
            if self.can_move(cell, d):
                list_dir.append(d)
        return list_dir

    def distance_map(self, goal: Cell | None) -> dict[Cell | None, int]:
        cache: dict[tuple[int, int], int] | None = self.distances.get(goal)
        if cache is not None:
            return cache
        dist: dict[Cell | None, int] = {goal: 0}
        queue: deque[Cell] = deque([goal])
        while queue:
            cell = queue.popleft()
            for direction in self.valid_directions(cell):
                nxt = self.step(cell, direction)
                if nxt not in dist:
                    dist[nxt] = dist[cell] + 1
                    queue.append(nxt)
        self.distances[goal] = dist
        return dist

    def steps_forward(
            self, cell: Cell, direction: Direction, steps: int) -> Cell:
        for i in range(steps):
            if not self.can_move(cell, direction):
                break
            cell = self.step(cell, direction)
        return cell

    def pacgum_positions(self) -> set[Cell | None]:
        # toutes les cells sauf corners et center
        valid_cells = set(self.distance_map(self.center))
        return valid_cells - {self.center, *self.ghost_corners}

    def super_pacgum_positions(self) -> set[Cell]:
        valid_cells: set[Cell] = set()
        for cell in self.ghost_corners:
            if cell in self.distance_map(self.center):
                valid_cells.add(cell)
        return valid_cells
