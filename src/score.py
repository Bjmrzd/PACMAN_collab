
class Score:
    def __init__(self, base_score: int):
        self.base_score: int = base_score

    def add_points(self, current_score: int, point: int):
        """Add point to the score"""
        return current_score + point
    # current_score += point depending on how its done in the main loop
    # can have problem of adding multiple time the same point be careful