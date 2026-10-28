from maze import Maze, Direction, Cell
from enum import Enum

class State(Enum):
	NORMAL = "normal",
	AFRAID = "afraid",
	EATEN= "eaten"

class Personnality(Enum):
	BLINKY = "blinky",
	PINKY = "pinky",
	INKY = "inky",
	CLYDE = "clyde"

class Mover:
	def __init__(self, maze: Maze, cell: Cell, speed: float) -> None:
		self.maze = maze
		self.speed = speed
		self.spawn = cell
		self.current_cell = cell
		self.direction: Direction | None = None
		self.target: Cell | None = None
		self.progress: float = 0.0 # 0.0 a 1.0

	@property
	def position(self) -> None:
		row, col = self.current_cell
		if self.target is None:
			return float(row), float(col)
		t_row, t_col = self.target
		return (row + (t_row - row) * self.progress,
		        col + (t_col - col) * self.progress)

	def reset(self) -> None:
		self.current_cell = self.spawn
		self.target = None
		self.direction = None
		self.progress = 0.0

	def reverse(self) -> None:
		if self.target is None or self.direction is None:
			return
		self.current_cell, self.target = self.target, self.current_cell
		self.progress = 1.0 - self.progress
		self.direction = self.direction.opposite

	def choose_direction(self) -> None:
		#pac-man: en fonction des touches
		#Ghost: en fonction de la personnalite du ghost et de l'algo de deplacement
		return

	def on_cell_reached(self) -> None:
		#PAC-MAN: si cell = pacgum ou super pacgum alors point en plus / mode chasse
		#Ghosts: si cell = pacman alors vie en moins
		return

	def start_move(self) -> bool:
		direction = self.choose_direction
		if self.target is None:
			return False
		self.direction = direction
		self.target = self.maze.step(self.current_cell, direction)
		self.progress = 0.0
		return True

	def advance(self, dt: float) -> None:
		distance = self.speed * dt
		while distance > 0:
			if self.target is None or self.start_move() is False:
				return
			remaining = 1.0 - self.progress
			if distance < remaining:
				self.progress += distance
				return
			distance -= remaining
			self.current_cell = self.target
			self.target = None
			self.progress = 0.0
			self.on_cell_reached()


# class Player(Mover):


class Ghost(Mover):
	def __init__(self, maze: Maze, cell: Cell, speed: float, name: Personnality) -> None:
		super().__init__()
		self.state: State = "normal"
		self.personnality: Personnality = name