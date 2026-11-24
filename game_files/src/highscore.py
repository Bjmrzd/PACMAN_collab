from pydantic import BaseModel, Field, ValidationError
from typing import Any
import sys


def ranking_score(
        score: int, data: Any, new_score_dict: Any
        ) -> dict[str, list[Any]] | Any:
    """Function to insert the new score with the player name"""
    """in the highscore ranking"""
    classed_score: dict[str, list[Any]] = {}
    lower_score: list[Any] = []
    count: int = 0
    try:
        for keys, values in data.items():
            if values == [] or len(values) < 2:
                raise ValueError
            elif (
                not isinstance(values[1], str)
                or not isinstance(values[0], int)
                 ):
                raise ValueError
    except ValueError:
        print("Invalid highscore data. It could not be retrieved")
        return data
    for keys, values in data.items():
        lower_score.append(values)
    lower_score.append(new_score_dict)
    lower_score.sort(reverse=True)
    for args in lower_score:
        print(args[0], args[1])
        if count < 10:
            classed_score.update({str(count): [args[0], args[1]]})
        count += 1
    return classed_score


class Highscore(BaseModel):
    player_name: str = Field(default="???")
    player_score: int = Field(default=0)


def valid_highscore(name: str, score: int) -> Highscore:
    """Validate the score and name to insert in the ranking"""
    highscore_dict = {
        "player_score": score,
        "player_name": name
    }

    try:
        valid = Highscore.model_validate(highscore_dict)
    except ValidationError as error:
        print(error.errors()[0]["msg"])
        sys.exit()
    return valid
