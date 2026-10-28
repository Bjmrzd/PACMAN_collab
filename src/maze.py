from enum import Enum
from collections import deque

Cell = tuple[int, int]


class MazeError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
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


class Maze: #faire des méthodes intermédiaires pour assurer qu'il n'y ait pas de conflits et d'erreurs
    def __init__(self, walls: list[list[int]]) -> None:
        self.walls = walls
        self.height = len(walls)
        self.width = len(walls[0])
        self.spawn: Cell = (self.height // 2, self.width // 2)
        self.ghost_corners: list[Cell] = [(0,0),
                                          (0, self.width),
                                          (self.height, 0),
                                          (self.height, self.width)]
        self.distances: dict[Cell, dict[Cell, int]] = {}

    def in_maze(self, cell: Cell) -> bool:
        if cell[0] < 0 or cell[0] > self.height:
            return False
        elif cell[1] < 0 or cell[1] > self.width:
            return False
        else:
            return True

    def step(self, cell: Cell, direction: Direction) -> Cell:
        dir_row, dir_col = direction.value
        return cell[0] + dir_row, cell[1] + dir_col

    def can_move(self, cell: Cell, direction: Direction) -> bool:
        row, col = cell
        if self.walls[row][col] & direction.wall_bit:  #check si il y a un mur dans cette direction
            return False
        target = self.step(cell, direction)
        if not self.in_maze(target):
            return False
        opposite_bit = direction.opposite.wall_bit
        return not self.walls[target[0]][target[1]] & opposite_bit

    def valid_directions(self, cell: Cell) -> list[Direction]:
        list_dir = []
        for d in Direction:
            if self.can_move(cell, d):
                list_dir.append(d)
        return list_dir
        # return [d for d in Direction if self.can\move(cell, d)]

    def distance_map(self, goal: Cell) -> dict[Cell, int]: #BFS
        cache = self.distances.get(goal)
        if cache is not None:
            return cache
        dist: dict[Cell, int] = {goal: 0}
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

    def steps_forward(self, cell: Cell, direction: Direction, steps: int) -> Cell:
        for i in range(steps):
            if not self.can_move(cell, direction):
                break
            cell = self.step(cell, direction)
        return cell

    def pacgum_positions(self) -> set[Cell]:
        # toutes les cells sauf corners et spawn
        valid_cells = set(self.distance_map(self.spawn))
        return valid_cells - {self.spawn, *self.ghost_corners}

    def super_pacgum_positions(self) -> set[Cell]:
        valid_cells = set[Cell] = {}
        for cell in self.ghost_corners:
            if cell in self.distance_map(self.spawn):
                valid_cells.add(cell)
        return valid_cells