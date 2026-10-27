
class Score:
    def __init__(self, base_score: int):
        self.base_score: int = base_score

    def add_points(self, current_score: int, point: int) -> int:
        """Add point to the score"""
        return current_score + point
    # current_score += point depending on how its done in the main loop
    # can have problem of adding multiple time the same point be careful

def ranking_score(score: int, data, new_score_dict):
    """Function to insert the new score with the player name in the highscore ranking"""
    classed_score: dict[str, dict] = {}
    lower_score: list[int] = []
    count: int = 0
    try:
        for keys, values in data.items():
            if values == [] or len(values) < 2:
                raise ValueError
            elif not isinstance(values[1], str) or not isinstance(values[0], int):
                raise ValueError
    except ValueError:
        print("Invalid highscore data. It could not be retrieved")
        return data
    for keys, values in data.items():
        lower_score.append(new_score_dict)
        lower_score.sort(reverse=True)
        for args in lower_score:
            if count < 10:
                classed_score.update({str(count): (args[0]. args[1])})
            count += 1
        return classed_score
