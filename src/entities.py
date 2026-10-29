from maze import Maze, Direction, Cell
from enum import Enum
import random


class State(Enum):
	NORMAL = "normal",
	EDIBLE = "edible",
	EATEN = "eaten"

class GhostCaracteristiques(Enum):
	NORMAL_SPEED = 5.0,
	EDIBLE_SPEED = 2.5,
	CLYDE_DISTANCE = 8,
	PINKY_LOOKAHEAD = 4,
	RESPAWN_DELAY = 5.0

class Personnality(Enum):
	BLINKY = "blinky",  #Aims the player's cell
	PINKY = "pinky",	#Aims a few cells ahead of the player
	INKY = "inky",	  #Chases the player if close, wanders randomly otherwise (need to verify)
	CLYDE = "clyde"	 #Chases when far, goes home when close


class Mover:
	def __init__(self, maze: Maze, cell: Cell, speed: float) -> None:
		self.maze = maze
		self.speed = speed
		self.spawn = cell
		self.current_cell = cell
		self.direction: Direction | None = None
		self.target: Cell | None = None
		self.progress: float = 0.0  # 0.0 a 1.0

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
	def __init__(self, maze: Maze, corner: Cell, personnality: Personnality, rng: random.Random) -> None:
		super().__init__(maze, corner)
		self.state: State = "normal"
		self.personnality = personnality
		self.spawn = corner
		self.speed = GhostCaracteristiques.NORMAL_SPEED
		self.rng = rng
		self.respawn_delay = GhostCaracteristiques.RESPAWN_DELAY
		self.state = State.NORMAL
		self.timer = 0.0
		self.player_cell: Cell = corner
		self.player_dir: Direction | None = None


	def tick(self, dt: float, player_cell: Cell, player_dir: Direction | None) -> None:
		self.player_cell = player_cell
		self.player_dir = player_dir
		if self.state is not State.Normal:
			self.timer -= dt
			if self.timer <= 0:
				self.state = State.NORMAL
				self.speed = GhostCaracteristiques.NORMAL_SPEED
		if self.state is not State.EATEN:
			self.advance(dt)

	def goal(self) -> Cell | None:
		if self.personnality is Personnality.BLINKY:
			return self.player_cell
		if self.personnality is Personnality.PINKY:
			if self.player_dir is None:
				return self.player_cell
			return self.maze.steps_forward(self.player_cell, self.player_dir, GhostCaracteristiques.PINKY_LOOKAHEAD)
		if self.personnality is Personnality.INKY:
			if self.rng.random() < 0.5:
				return None
			else:
				return self.player_cell
		if self.personnality is Personnality.CLYDE:
			distance = self.maze.distance_map(self.player_cell).get(self.cell)
			if distance > GhostCaracteristiques.CLYDE_DISTANCE:
				return self.player_cell
			else:
				return self.home
	
	def choose_direction(self) -> Direction | None:
		return

	def path_algorithm() -> Direction:
		return

	def is_edible(self, duration: float) -> None:
		if self.state is State.EATEN:
			return
		self.state = State.EDIBLE
		self.timer = duration
		self.speed = GhostCaracteristiques.EDIBLE_SPEED
		self.reverse()


	def eaten(self) -> None:
		super().reset()
		self.state = State.NORMAL
		self.speed = GhostCaracteristiques.NORMAL_SPEED
		self.timer = 0.0

	def reset(self) -> None:
		super().reset()
		self.state = State.NORMAL
		self.speed = GhostCaracteristiques.NORMAL_SPEED
		self.timer = 0.0
