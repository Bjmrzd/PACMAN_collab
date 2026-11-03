from dataclasses import dataclass

@dataclass
class ScoringRules():
	pacgum: int
	super_pacgum: int
	ghost: int


class GameState():
	def __init__(self, lives: int, rules: ScoringRules) -> None:
		self.lives = lives
		self.rules = rules
		self.score = 0

	def add_points(self, points: int) -> None:
		self.score += points

	def lose_life(self) -> None:
		self.lives -= 1

	def add_life(self) -> None:
		self.lives += 1

	def game_over(self) -> bool:
		if self.lives <= 0:
			return True
		return False
	