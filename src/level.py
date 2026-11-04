from enum import Enum
import random

from src.entities import Ghost, State, Personnality
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
		self.player = Player() # A modifier quand on aura la class Player finie
		Personnalities = [Personnality.BLINKY, Personnality.PINKY, Personnality.INKY, Personnality.CLYDE]
		self.ghosts = [Ghost(maze, corner, personnality, rng) for corner in maze.ghost_corners for personnality in Personnalities]

	def update(self, dt:float) -> None:
		if self.level_state is not LevelState.PLAYING:
			return
		self.remaining_time -= dt
		if self.remaining_time <= 0:
			self.lose_life()
			return
		self.player.advance(dt)
		for ghost in self.ghosts:
			ghost.tick(dt, self.player.cell, self.player.direction)
		self.collisions()
		if self.level_state is LevelState.PLAYING and not self.pacgums:
			self.level_state = LevelState.WON

	def player_reach_cell(self, cell: Cell) -> None:
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
		p_row, p_col = self.player.position
		for ghost in self.ghosts:
			if ghost.eaten():
				continue
			g_row, g_col = ghost.position
			