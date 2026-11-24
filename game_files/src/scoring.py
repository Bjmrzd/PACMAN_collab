from dataclasses import dataclass


@dataclass
class ScoringRules():
    pacgum: int
    super_pacgum: int
    ghost: int


class GameState():
    def __init__(self, lives: int, rules: ScoringRules) -> None:
        self.lives: int = lives
        self.rules: ScoringRules = rules
        self.score: int = 0

    def add_points(self, points: int) -> None:
        """Add point to the score"""
        self.score += points

    def lose_life(self) -> None:
        """Substract a life when necessary"""
        self.lives -= 1

    def add_life(self) -> None:
        """Add a life when necessary"""
        self.lives += 1

    def game_over(self) -> bool:
        """Check for game over based on life"""
        if self.lives <= 0:
            return True
        return False
