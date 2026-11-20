from src.maze import Maze, Direction, Cell
from enum import Enum
from typing import Callable, Any
from abc import ABC, abstractmethod
import random
import pygame as pg
from src.helper import Images
from src.scoring import GameState


class State(Enum):
	NORMAL = "normal"

	EDIBLE = "edible"

	EATEN = "eaten"


class GhostFeatures(Enum):
	NORMAL_SPEED = 3.0

	EDIBLE_SPEED = 2.5

	CLYDE_DISTANCE = 8

	PINKY_LOOKAHEAD = 4

	INKY_SIGHT = 4

	RESPAWN_DELAY = 5.0


class Personnality(Enum):
	BLINKY = "blinky"   #Aims the player's cell

	PINKY = "pinky"	    #Aims a few cells ahead of the player

	INKY = "inky"	  	#Chaotic movements

	CLYDE = "clyde"	 	#Chases when far, goes home when close


class Mover(ABC):
	def __init__(self, maze: Maze, cell: Cell, speed: float) -> None:
		self.maze = maze
		self.speed = speed
		self.spawn = cell
		self.current_cell = cell
		self.direction: Direction | None = None
		self.target: Cell | None = None
		self.progress: float = 0.0  # 0.0 a 1.0
		# self.position_screen = None

	@property
	def position(self) -> None:
		row, col = self.current_cell
		if self.target is None:
			return float(row), float(col)
		t_row, t_col = self.target
		return (row + (t_row - row) * self.progress,
				col + (t_col - col) * self.progress)

	@position.setter
	def position(self, new_cell) -> None:
		row, col = new_cell
		if self.target is None:
			return float(row), float(col)
		t_row, t_col = self.target
		return (row + (t_row - row) * self.progress,  col + (t_col - col) * self.progress)

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

	@abstractmethod
	def choose_direction(self) -> Direction | None:
		return

	def cell_reached(self) -> None:
		return None

	def start_move(self) -> bool:
		direction = self.choose_direction()
		if direction is None:
			return False
		self.direction = direction
		self.target = self.maze.step(self.current_cell, direction)
		self.progress = 0.0
		return True

	def advance(self, dt: float) -> None:
		distance = self.speed * dt
		while distance > 0:
			if self.target is None:
				if not self.start_move():
					return
			remaining = 1.0 - self.progress
			if distance < remaining:
				self.progress += distance
				return
			distance -= remaining
			self.current_cell = self.target
			self.target = None
			self.progress = 0.0
			self.cell_reached()


class Pac_anim(Enum):
	UP = Images.PACMAN.value.subsurface((3, 74, 26, 25))

	RIGHT = Images.PACMAN.value.subsurface((2, 3, 25, 25))

	LEFT = Images.PACMAN.value.subsurface((5, 35, 25, 25))

	DOWN = Images.PACMAN.value.subsurface((3, 100, 26, 25))

	C_UP = Images.PACMAN.value.subsurface((35, 69, 25, 25))

	C_RIGHT = Images.PACMAN.value.subsurface((35, 4, 25, 25))

	C_LEFT = Images.PACMAN.value.subsurface((35, 35, 25, 25))

	C_DOWN = Images.PACMAN.value.subsurface((35, 100, 25, 25))

	CLYDE_RIGHT = Images.PACMAN.value.subsurface((3, 131, 26, 26))

	PINKY_RIGHT = Images.PACMAN.value.subsurface((3, 164, 26, 26))

	INKY_RIGHT = Images.PACMAN.value.subsurface((3, 195, 26, 26))

	BLINKY_RIGHT = Images.PACMAN.value.subsurface((3, 225, 26, 26))

	GUM = Images.SUPERGUM.value.subsurface((8, 5, 8, 8))

	SUPERGUM = Images.SUPERGUM.value.subsurface((0, 0, 21, 21))

	SCARED = Images.PACMAN.value.subsurface((275, 164, 25, 25))


class PacMan(Mover, pg.sprite.Sprite):
	def __init__(self, maze: Maze, cell: Cell, speed: float = 5.0) -> None:
		"""Create the Pac-Man. Key_direction is the direction saved each time we press a directional key"""
		super().__init__(maze, cell, speed)
		pg.sprite.Sprite.__init__(self)

		self.sprite = Images.PACMAN.value
		self.image = Pac_anim.RIGHT.value
		self.rect = self.image.get_rect()
		self.rect.center = (cell[0], cell[1])

		self.key_direction: Direction | None = None
		self.on_cell_center: Callable[[Cell], None] = None

	def check_gum(self, gum: pg.sprite.Group, state: GameState, supergum: pg.sprite.Group):
		eaten: list[Any] = pg.sprite.spritecollide(self, supergum, True)
		eaten_gum: list[Any] = pg.sprite.spritecollide(self, gum, True)

		for sprite in eaten:
			sprite.state = State.EATEN
			if isinstance(sprite, Super_gum):
				state.add_points(state.rules.super_pacgum)
		for sprite in eaten_gum:
			sprite.state = State.EATEN
			if isinstance(sprite, Pacgum):
				state.add_points(state.rules.pacgum)
		return eaten

	def move(self, direction: Direction, updated: bool) -> None:
		if self.target is not None:
			if (self.direction is not None and direction is self.direction.opposite):
				self.reverse()
			return
		if self.maze.can_move(self.current_cell, direction):
			self.direction = direction
			self.change_sprite(direction, updated)
			self.target = self.maze.step(self.current_cell, direction)
			self.progress = 0.0

	def change_sprite(self, direction: Direction, updated: bool):

		if direction is Direction.North:
			if updated:
				self.image = Pac_anim.UP.value
			else:
				self.image = Pac_anim.C_UP.value

		if direction is Direction.South:
			if updated:
				self.image = Pac_anim.DOWN.value
			else:
				self.image = Pac_anim.C_DOWN.value

		if direction is Direction.East:
			if updated:
				self.image = Pac_anim.RIGHT.value
			else:
				self.image = Pac_anim.C_RIGHT.value

		if direction is Direction.West:
			if updated:
				self.image = Pac_anim.LEFT.value
			else:
				self.image = Pac_anim.C_LEFT.value

			

	def choose_direction(self) -> Direction | None:
		return None

	def cell_reached(self) -> None:
		if self.on_cell_center is not None:
			self.on_cell_center(self.current_cell)

	def reset(self) -> None:
		super().reset()
		self.key_direction = None


class Ghost(Mover, pg.sprite.Sprite):
	def __init__(self, maze: Maze, corner: Cell, personnality: Personnality, rng: random.Random, speed: float = GhostFeatures.NORMAL_SPEED.value) -> None:
		super().__init__(maze, corner, speed)
		pg.sprite.Sprite.__init__(self)
		self.personnality = personnality
		self.spawn = corner
		self.rng = rng
		self.state = State.NORMAL
		self.timer = 0.0
		self.player_cell: Cell = corner
		self.player_dir: Direction | None = None

		self.image = self.init_sprite()
		self.rect = self.image.get_rect()
		self.rect.center = self.position

	def init_sprite(self):
		sprite: Any = None
		if self.personnality is Personnality.BLINKY:
			sprite = Pac_anim.BLINKY_RIGHT.value
		elif self.personnality is Personnality.INKY:
			sprite = Pac_anim.INKY_RIGHT.value
		elif self.personnality is Personnality.PINKY:
			sprite = Pac_anim.PINKY_RIGHT.value
		elif self.personnality is Personnality.CLYDE:
			sprite = Pac_anim.CLYDE_RIGHT.value
		return sprite

	def tick(self, dt: float, player_cell: Cell, player_dir: Direction | None) -> None:
		self.player_cell = player_cell
		self.player_dir = player_dir
		if self.state is not State.NORMAL:
			self.timer -= dt
			if self.timer <= 0:
				self.image = self.init_sprite()
				self.state = State.NORMAL
				self.speed = GhostFeatures.NORMAL_SPEED.value
		if self.state is not State.EATEN:
			self.advance(dt)

	def goal(self) -> Cell | None:
		distance = self.maze.distance_map(self.player_cell).get(self.current_cell, 10**9)
		if self.personnality is Personnality.BLINKY:
			return self.player_cell
		if self.personnality is Personnality.PINKY:
			if self.player_dir is None:
				return self.player_cell
			return self.maze.steps_forward(self.player_cell, self.player_dir, GhostFeatures.PINKY_LOOKAHEAD.value)
		if self.personnality is Personnality.INKY:
			if distance <= GhostFeatures.INKY_SIGHT.value:
				return self.player_cell
			return None
		if self.personnality is Personnality.CLYDE:
			if distance > GhostFeatures.CLYDE_DISTANCE.value:
				return self.player_cell
			return self.spawn

	def choose_direction(self) -> Direction | None:
		choices = self.maze.valid_directions(self.current_cell)
		if not choices:
			return None
		if self.direction is not None and len(choices) > 1:
			back = self.direction.opposite
			temp = []
			for i in choices:
				if i is not back:
					temp.append(i)
			choices = temp
		if self.state is State.EDIBLE:
			return self.best_choice(choices, self.player_cell, retreat=True)
		target = self.goal()
		if target is None:
			return self.rng.choice(choices)
		return self.best_choice(choices, target, retreat=False)

	def best_choice(self, choices: list[Direction], goal: Cell, retreat: bool) -> Direction:
		distance = self.maze.distance_map(goal)

		best_score: int | None = None
		best_directions: list[Direction] = []

		for direction in choices:
			neighbour = self.maze.step(self.current_cell, direction)
			if neighbour in distance:
				score = distance[neighbour]
			else:
				score = 10**9

			if best_score is None:
				is_better = True
			elif retreat:
				is_better = score > best_score
			else:
				is_better = score < best_score

			if is_better:
				best_score = score
				best_directions = [direction]
			elif score == best_score:
				best_directions.append(direction)

		return self.rng.choice(best_directions)

	def is_edible(self, duration: float) -> None:
		self.image = Pac_anim.SCARED.value
		if self.state is State.EATEN:
			return
		self.state = State.EDIBLE
		self.timer = duration
		self.speed = GhostFeatures.EDIBLE_SPEED.value
		self.reverse()

	def eaten(self) -> None:
		super().reset()
		self.state = State.EATEN
		self.timer = GhostFeatures.RESPAWN_DELAY.value
		self.image = self.init_sprite()

	def reset(self) -> None:
		super().reset()
		self.state = State.NORMAL
		self.speed = GhostFeatures.NORMAL_SPEED.value
		self.timer = 0.0


class Pacgum(pg.sprite.Sprite):
	def __init__(self, cell: Cell, state: State):
		super().__init__()

		self.position = cell
		self.state = state
		self.image = Pac_anim.GUM.value
		self.rect = self.image.get_rect()
		self.rect.center = (0, 0)


class Super_gum(pg.sprite.Sprite):
	def __init__(self, cell: Cell, state: State):
		super().__init__()

		self.position = cell
		self.state = state
		self.image = Pac_anim.SUPERGUM.value
		self.rect = self.image.get_rect()
		self.rect.center = (0, 0)

