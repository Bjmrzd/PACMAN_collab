import json
from pydantic import Field, BaseModel, ValidationError, model_validator
from typing import Any
import logging


class Config(BaseModel):
    highscore_filename: str = Field(default="highscore.json")
    lives: int = Field(gt=0, default=3)
    seed: int = Field(gt=0, default=42)
    lvl_max_time: int = Field(ge=60, le=180, default=90)
    pacgum_pts: int = Field(gt=0, le=100, default=25)
    super_pacgum_pts: int = Field(gt=0, le=200, default=100)
    ghost_pts: int = Field(gt=0, le=1000, default=200)
    level_1: dict[str, int] = Field(default_factory=dict)
    level_2: dict[str, int] = Field(default_factory=dict)
    level_3: dict[str, int] = Field(default_factory=dict)
    level_4: dict[str, int] = Field(default_factory=dict)
    level_5: dict[str, int] = Field(default_factory=dict)
    level_6: dict[str, int] = Field(default_factory=dict)
    level_7: dict[str, int] = Field(default_factory=dict)
    level_8: dict[str, int] = Field(default_factory=dict)
    level_9: dict[str, int] = Field(default_factory=dict)
    level_10: dict[str, int] = Field(default_factory=dict)

    @model_validator(mode="after")
    def validate_infos(self):
        level = [
            self.level_1,
            self.level_2,
            self.level_3,
            self.level_4,
            self.level_5,
            self.level_6,
            self.level_7,
            self.level_8,
            self.level_9,
            self.level_10,
        ]
        for args in level:
            if not args.get("width") or not args.get("height"):
                raise ValueError("Error: Levels must have both a height and width")
            elif args.get("width") != args.get("height"):
                raise ValueError("Error: The Pacman Maze must be a square")
            elif (args.get("width") or args.get("height")) >= 19 or (args.get("width") or args.get("height")) < 9:
                raise ValueError("Error: The maze width and height can't be higher than 18 or lower than 10")
        return self


def parsing() -> Config:
    file = "config.json"
    logging.
    necessary_keys: list[Any] = ["highscore_filename", "lives", "pacgum_pts", "seed", "super_pacgum_pts", "ghost_pts", "lvl_max_time"]
    try:
        with open(file, "r") as config:
            data = json.load(config)
    except (FileNotFoundError, json.JSONDecodeError):
        print(f"The file {file} was not found or failed to decode data from JSON file")
        exit()
    try:
        if not all(keys in data for keys in necessary_keys):
            raise KeyError
    except KeyError:
        print("Missing or invalid config values")
        exit()

    try:
        valid_config = Config.model_validate(data)
    except ValidationError as error:
        print(error.errors()[0]["msg"])
        exit()
    return valid_config
