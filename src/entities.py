from src.maze import Maze, Direction, Cell
from enum import Enum
from typing import Callable
from abc import ABC, abstractmethod
import random
import pygame as pg
from helper import Images


class State(Enum):
	NORMAL = "normal",
	EDIBLE = "edible",
	EATEN = "eaten"

class GhostFeatures(Enum):
	NORMAL_SPEED = 5.0,
	EDIBLE_SPEED = 2.5,
	CLYDE_DISTANCE = 8,
	PINKY_LOOKAHEAD = 4,
	INKY_SIGHT = 4,
	RESPAWN_DELAY = 5.0

class Personnality(Enum):
	BLINKY = "blinky",  #Aims the player's cell
	PINKY = "pinky",	#Aims a few cells ahead of the player
	INKY = "inky",	  	#Chaotic movements
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


	@abstractmethod
	def choose_direction(self) -> Direction | None:
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


class Pac_anim(Enum):
	UP = Images.PACMAN.value.subsurface((3, 74, 26, 25))
	RIGHT = Images.PACMAN.value.subsurface((2, 3, 25, 25))
	LEFT = Images.PACMAN.value.subsurface((5, 35, 25, 25))
	DOWN = Images.PACMAN.value.subsurface((3, 100, 26, 25))
	C_UP = Images.PACMAN.value.subsurface((35, 69, 25, 25))
	C_RIGHT = Images.PACMAN.value.subsurface((35, 4, 25, 25))
	C_LEFT = Images.PACMAN.value.subsurface((35, 35, 25, 25))
	C_DOWN = Images.PACMAN.value.subsurface((35, 100, 25, 25))



class PacMan(Mover, pg.sprite.Sprite):
	def __init__(self, maze: Maze, cell: Cell, speed: float = 5.0) -> None:
		"""Create the Pac-Man. Key_direction is the direction saved each time we press a directional key"""
		super.__init__(maze, cell, speed)
		pg.sprite.Sprite.__init__()
		self.sprite = Images.PACMAN.value
		self.base_sprite = Pac_anim.RIGHT.value
		self.rect = self.sprite.get_rect()
		self.rect.topleft = (Cell[0], Cell[1]) # may need to change the order for row and col
		self.key_direction: Direction | None = None
		self.on_cell_center: Callable[[Cell], None] = None


	def set_next_move(self, direction):
		"""The next direction is defined and saved by the key pressed (applied at the next cell's center)"""
		self.key_direction = direction
		if self.direction is not None and direction is self.direction.opposite:
			self.reverse()


	def choose_direction(self) -> Direction | None:
		"""Try the choosen direction, advance if direction is valid, stay still if not"""
		for direction in (self.key_direction, self.direction):
			if direction is not None and self.maze.can_move(self.cell, direction):
				return direction
		return None


	def cell_reached(self) -> None:
		if self.on_cell_center is not None:
			self.on_cell_center(self.cell)


	def reset(self) -> None:
		super().reset()
		self.key_direction = None


class Ghost(Mover):
	def __init__(self, maze: Maze, corner: Cell, personnality: Personnality, rng: random.Random) -> None:
		super().__init__(maze, corner)
		self.state: State = "normal"
		self.personnality = personnality
		self.spawn = corner
		self.speed = GhostFeatures.NORMAL_SPEED
		self.rng = rng
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
				self.speed = GhostFeatures.NORMAL_SPEED
		if self.state is not State.EATEN:
			self.advance(dt)

	def goal(self) -> Cell | None:
		distance = self.maze.distance_map(self.player_cell).get(self.cell)
		if self.personnality is Personnality.BLINKY:
			return self.player_cell
		if self.personnality is Personnality.PINKY:
			if self.player_dir is None:
				return self.player_cell
			return self.maze.steps_forward(self.player_cell, self.player_dir, GhostFeatures.PINKY_LOOKAHEAD)
		if self.personnality is Personnality.INKY:
			if distance <= GhostFeatures.INKY_SIGHT:
				return self.player_cell
			return None
		if self.personnality is Personnality.CLYDE:
			if distance > GhostFeatures.CLYDE_DISTANCE:
				return self.player_cell
			else:
				return self.home

	def choose_direction(self) -> Direction | None:
		choices = self.maze.valid_directions
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
		return self.best_choice(choices, target, retreat=False)

	def best_choice(self, choices: list[Direction], goal: Cell, retreat: bool) -> Direction:
		distance = self.maze.distance_map(goal)

		best_score: int | None = None
		best_directions: list[Direction] = []

		for direction in choices:
			neighbour = self.maze.step(self.cell, direction)
			if neighbour in distance:
				score = distance[neighbour]

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
		if self.state is State.EATEN:
			return
		self.state = State.EDIBLE
		self.timer = duration
		self.speed = GhostFeatures.EDIBLE_SPEED
		self.reverse()

	def eaten(self) -> None:
		super().reset()
		self.state = State.EATEN
		self.timer = GhostFeatures.RESPAWN_DELAY

	def reset(self) -> None:
		super().reset()
		self.state = State.NORMAL
		self.speed = GhostFeatures.NORMAL_SPEED
		self.timer = 0.0
