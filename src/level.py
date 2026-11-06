from enum import Enum
import random
import math

from src.entities import Ghost,PacMan, State, Personnality
from src.maze import Maze, Cell
from src.scoring import GameState


class LevelState(Enum):
	PLAYING = "playing"
	WON = "won"
	GAME_OVER = "game_over"


class LevelFeatures(Enum):
	PACMAN_HUNT = 8.0
	COLLISION_RANGE = 0.5


class Level():
	def __init__(self, maze: Maze, state: GameState, level_number: int, time: int, rng: random.Random):
		
		self.maze = maze
		self.state = state
		self.level_number = level_number
		self.time = float(time)
		self.remaining_time = float(time)
		self.level_state = LevelState.PLAYING
		self.pacgums: set[Cell] = maze.pacgum_positions()
		self.super_pacgums: set[Cell] = maze.super_pacgum_positions()
		self.pac_man = PacMan(maze, maze.spawn)
		self.pac_man.on_cell_center = self.pacman_reach_cell
		Personnalities = [Personnality.BLINKY, Personnality.PINKY, Personnality.INKY, Personnality.CLYDE]
		self.ghosts = [Ghost(maze, corner, personnality, rng) for corner in maze.ghost_corners for personnality in Personnalities]


	def update(self, dt:float) -> None:
		if self.level_state is not LevelState.PLAYING:
			return
		self.remaining_time -= dt
		if self.remaining_time <= 0:
			self.lose_life()
			return
		self.pac_man.advance(dt)
		for ghost in self.ghosts:
			ghost.tick(dt, self.pac_man.cell, self.pac_man.direction)
		self.collisions()
		if self.level_state is LevelState.PLAYING and not self.pacgums:
			self.level_state = LevelState.WON


	def pacman_reach_cell(self, cell: Cell) -> None:
		rules = self.state.rules
		if cell in self.pacgums:
			self.pacgums.discard(cell)
			self.state.add_points(rules.pacgum)
		if cell in self.super_pacgums:
			self.super_pacgums.discard(cell)
			self.state.add_points(rules.super_pacgum)
			for ghost in self.ghosts:
				ghost.is_edible(LevelFeatures.PACMAN_HUNT)


	def collisions(self) -> None:
		p_row, p_col = self.pac_man.position
		for ghost in self.ghosts:
			if ghost.state is State.EATEN:
				continue
			g_row, g_col = ghost.position

			if math.sqrt(abs(g_row - p_row)**2 + abs(g_col - p_col)**2 ) < LevelFeatures:
				if ghost.state is State.EDIBLE:
					ghost.eaten
					self.state.add_points(self.state.rules.ghost)
				else:
					self.lose_life()
					return
			else:
				continue


	def lose_life(self):
		self.state.lose_life()
		if self.state.game_over():
			self.status = LevelState.GAME_OVER
			return
		self.pac_man.reset()
		for ghost in self.ghosts:
			ghost.reset()
