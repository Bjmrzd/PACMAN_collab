from enum import Enum
import random
import math
from typing import Any

from src.entities import Ghost, PacMan, State, Personnality, Pacgum, Super_gum, Pac_anim
from src.maze import Maze, Cell
from src.scoring import GameState


class LevelState(Enum):
	PLAYING = "playing"
	WON = "won"
	GAME_OVER = "game_over"
	PAUSE = "pause"


class LevelFeatures(Enum):
	PACMAN_HUNT = 8.0
	COLLISION_RANGE = 0.5


class Level():
	def __init__(self, maze: Maze, state: GameState, level_number: int, time: int, rng: random.Random, pac: PacMan):
		
		self.maze = maze
		self.state = state
		self.level_number = level_number
		self.time = float(time)
		self.remaining_time = float(time)
		self.level_state = LevelState.PLAYING
		self.pacgum_done: bool = False
		self.pacgum: dict[str, Any] = {}
		self.super_pacgum_done: set[Cell] = maze.super_pacgum_positions()
		self.pac_man = pac
		self.pac_base_speed: float = 5.0
		self.cheat_speed: bool = False
		self.cheat_invincible: bool = False
		self.cheat_time: bool = False
		# self.pac_man.on_cell_center = self.pacman_reach_cell(self.pac_man, self.pacgum) # besoin de faire passer pacman et list pacgum ici
		Personnalities = [Personnality.BLINKY, Personnality.PINKY, Personnality.INKY, Personnality.CLYDE]
		self.ghosts = [Ghost(maze, corner, personnality, rng) for corner, personnality in zip(maze.ghost_corners, Personnalities)]

	def update(self, dt:float) -> None:
		count: int = 0
		if self.cheat_speed:
			self.pac_man.speed += 15.0
		if self.level_state is not LevelState.PLAYING:
			return
		if not self.cheat_time:
			self.remaining_time = max(0, self.remaining_time - dt)
		if self.remaining_time <= 0:
			self.remaining_time = 0
			self.lose_life()
			return
		self.pac_man.advance(dt)
		for ghost in self.ghosts:
			ghost.tick(dt, self.pac_man.current_cell, self.pac_man.direction)
			if ghost.timer <= 0.0:
				count += 1
			if count == 4:
				self.pac_man.speed = self.pac_base_speed

		self.collisions()
		if self.level_state is LevelState.PLAYING and self.pacgum_done:
			self.level_state = LevelState.WON

	def pacman_reach_cell(self, pac: PacMan, gum) -> None:
		if self.level_state is not LevelState.PLAYING:
			return
		if len(gum) < 1:
			gum = self.pacgum
			return
		eaten = pac.check_gum(gum.get("sprite"), self.state, gum.get("super"))
		super_pacgum_eaten: bool = False
		for sprite in eaten:
			if isinstance(sprite, Super_gum):
				super_pacgum_eaten = True
				break
		if super_pacgum_eaten:
			pac.speed += 1.0
			for ghost in self.ghosts:
				ghost.is_edible(LevelFeatures.PACMAN_HUNT.value)
		self.pacgum_done = self.is_pacgum(gum.get("entities"))

	def is_pacgum(self, gum: Any) -> bool:
		index: int = 0
		for args in gum:
			if args.state is State.EATEN:
				index += 1
		if index == len(gum):
			return True
		return False

	def collisions(self) -> None:
		p_row, p_col = self.pac_man.position
		for ghost in self.ghosts:
			if ghost.state is State.EATEN:
				continue
			g_row, g_col = ghost.position
			if math.sqrt(abs(g_row - p_row)**2 + abs(g_col - p_col)**2 ) < LevelFeatures.COLLISION_RANGE.value:
				if ghost.state is State.EDIBLE:
					ghost.eaten()
					self.state.add_points(self.state.rules.ghost)
				else:
					if not self.cheat_invincible:
						self.lose_life()
						return
			else:
				continue

	def lose_life(self):
		self.state.lose_life()
		if self.state.game_over():
			self.level_state = LevelState.GAME_OVER
			self.remaining_time = 0
			return
		self.pac_man.reset()
		for ghost in self.ghosts:
			ghost.reset()
